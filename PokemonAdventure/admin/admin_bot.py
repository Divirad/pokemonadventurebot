import threading

from telegram.ext import Dispatcher, CommandHandler
from telegram import Bot, Update, ParseMode
from telegram.error import TelegramError
import logging
import logging.config
import sys
import traceback
import os

from private import admin_token, admins, admin_channel, log_file
from admin.admin_bot_active import AdminBotActive
from admin.admin_bot_commands import AdminBotCommands
from admin.admin_bot_passive import AdminBotPassive
from telegram_utilities.base_bot import BaseBot
from telegram_utilities.main_bot import MainBot

LOG_ERROR = logging.ERROR + 1
logging.addLevelName(LOG_ERROR, "LOG_ERROR")


def error_in_log(self, message, *args, **kws):
    # Yes, logger takes its '*args' as 'args'.
    if self.isEnabledFor(LOG_ERROR):
        self._log(LOG_ERROR, message, args, **kws)


logging.Logger.error_in_log = error_in_log

logger = logging.getLogger(__name__)


class AdminBot(BaseBot):

    def __init__(self):
        BaseBot.__init__(self, admin_token)
        self.activeCommands = AdminBotActive(self)
        self.passiveCommands = AdminBotPassive(self)
        self.mainBot = MainBot()
        self.old_excepthook = None

        class InfoFilter(logging.Filter):
            def filter(self, rec):
                return rec.levelno < logging.ERROR

        class MultiLineFormatter(logging.Formatter):
            def format(self, record):
                msg = logging.Formatter.format(self, record)
                header_len = msg.find(" - ", msg.find(" - ") + 1) + len(" - ")
                return msg.replace('\n', '\n' + ' ' * header_len)

        logging.config.dictConfig(dict(
            version=1,
            formatters={
                'f': {
                    '()': MultiLineFormatter,
                    'format': '%(asctime)s - %(levelname)-9s - %(message)s'
                },
                'ft': {
                    'format': ' %(levelname)s: %(message)s'
                }
            },
            filters={
                'info_filter': {
                    '()': InfoFilter
                }
            },
            handlers={
                'file': {
                    'class': 'logging.FileHandler',
                    'filename': log_file,
                    'level': logging.INFO,
                    'formatter': 'f'
                },
                'console_info': {
                    'class': 'logging.StreamHandler',
                    'stream': sys.stdout,
                    'filters': ['info_filter'],
                    'formatter': 'f',
                    'level': logging.INFO,
                },
                'console_err': {
                    'class': 'logging.StreamHandler',
                    'stream': sys.stderr,
                    'level': logging.ERROR,
                    'formatter': 'f'
                },
                'telegram': {
                    'class': self.LoggingHandler.__module__ + "." + self.LoggingHandler.__qualname__,
                    'bot': self,
                    'formatter': 'ft',
                    'level': logging.INFO,
                }
            },
            root={
                'handlers': ['file', 'console_info', 'console_err', 'telegram'],
                'level': logging.DEBUG
            },
            disable_existing_loggers=False
        ))

    def get_commands(self) -> AdminBotCommands:
        if self.mainBot.is_started:
            return self.activeCommands
        else:
            return self.passiveCommands

    class LoggingHandler(logging.Handler):
        def __init__(self, bot):
            super().__init__()
            self.bot = bot

        def emit(self, record):
            # log message in telegram
            if record.levelname != "LOG_ERROR" and self.bot.is_started and admin_channel is not None:
                try:
                    self.bot.updater.bot.send_message(admin_channel, '```' + self.format(record) + '```',
                                                      parse_mode = ParseMode.MARKDOWN)
                except Exception as e:
                    logger.error_in_log('{0}While logging {1}.{2}: {3}'.format(
                        ''.join(traceback.format_tb(e.__traceback__)),
                        e.__class__.__module__, e.__class__.__name__, e, ))

    def setup(self) -> bool:
        self.add_handlers(self.updater.dispatcher)
        self.old_excepthook = sys.excepthook
        sys.excepthook = self.handle_exception
        return True

    def unset(self):
        self.mainBot.stop()

    def restart(self):
        self.stop()
        os.execv(sys.argv[0], sys.argv)

    @staticmethod
    def is_valid(bot: Bot, update: Update) -> bool:
        if update.message.from_user.id in admins:
            return True
        else:
            bot.send_message(update.message.chat_id, "You do not have the permission to use this bot.\n"
                                                     "If you think this is an error please contact the admin."
                                                     " Your ID is %d" % update.message.chat_id)
            return False

    def add_handlers(self, dispatcher: Dispatcher):
        for name in dir(AdminBotCommands):
            if name.startswith("comm_"):

                @self.run_async()
                def handler(bot: Bot, update: Update, _name=name):
                    if AdminBot.is_valid(bot, update):
                        try:
                            getattr(self.get_commands(), _name)(bot, update)
                        except NotImplementedError:
                            bot.send_message(update.message.chat_id, "Command is not implemented")
                            raise

                dispatcher.add_handler(CommandHandler(name[len("comm_"):], handler))

    def handle_exception(self, ex_cls, ex, tb):
        logger.critical('{0}Uncatched {1}.{2}: {3}'.format(''.join(traceback.format_tb(tb)),
                                                           ex_cls.__module__, ex_cls.__name__, ex, ))

        if not issubclass(ex_cls, TelegramError):
            self.mainBot.stop()
            self.stop()
            self.old_excepthook(ex_cls, ex, tb)
