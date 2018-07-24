import logging
from inspect import signature

from telegram import Update, Bot
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, Filters

from database.db import Database
from gamelogic.button_id import ButtonId
from gamelogic.getdata.trainer import Trainer
from telegram_utilities.base_bot import BaseBot

logger = logging.getLogger(__name__)

ids_in_use = set()


def call_with_safe_id(id: int, bot: BaseBot, func, *args, **kwargs):
    @bot.run_async()
    def async_call():
        try:
            func(*args, **kwargs)
        finally:
            ids_in_use.remove(id)

    if id not in ids_in_use:  # only used on one thread therefor no lock needed
        ids_in_use.add(id)
        async_call()
    else:
        logger.info("Ignored update for id %d" % id)


class Registry:
    def __init__(self):
        self.commandHandlers = {}  # key: command,   value: { key: menu_id, value: func }
        self.buttonHandlers = {}  # key: button_id, value: { key: menu_id, value: func }
        self.messageHandlers = {}  # key: menu_id,   value: func

    @staticmethod
    def verify_func(func):
        if not callable(func):
            raise ValueError("func is not callable")
        if len(signature(func).parameters) not in (3, 4):
            raise ValueError("func must take 3 or 4 arguments: Bot, Update, Trainer and optional database")

    @staticmethod
    def uses_db(func):
        return len(signature(func).parameters) == 4

    def add_command_handler(self, command: str, func, menu_ids: list):
        self.verify_func(func)

        dic = {}
        if command in self.commandHandlers:
            dic = self.commandHandlers[command]
        else:
            self.commandHandlers[command] = dic
        for id in menu_ids:
            if id in dic:
                raise ValueError("Command '{}' with menu id {} is already registered".format(command, id))
            dic[id] = func

    def add_button_handler(self, button_id: ButtonId, func, menu_ids: list):
        self.verify_func(func)

        dic = {}
        if button_id in self.buttonHandlers:
            dic = self.buttonHandlers[button_id]
        else:
            self.buttonHandlers[button_id] = dic

        for id in menu_ids:
            if id in dic:
                raise ValueError("Button '{}' with menu id {} is already registered".format(button_id, id))
            dic[id] = func

    def add_message_handler(self, func, menu_ids: list):
        self.verify_func(func)

        for id in menu_ids:
            if id in self.messageHandlers:
                raise ValueError("Message handler with menu id {} is already registered".format(id))
            self.messageHandlers[id] = func

    def create_telegram_handler(self, bot: BaseBot):
        for command, cmd_handlers in self.commandHandlers.items():
            def handle(bot_p: Bot, update: Update, _cmd_handlers):
                with Database() as database:
                    trainer = Trainer(update.message.from_user.id)
                    menu_id = None
                    if trainer.does_exist(database):
                        trainer.load_values(values="menu_id", database=database)
                        menu_id = trainer.menu_id
                    if menu_id not in _cmd_handlers:
                        return
                    func = _cmd_handlers[menu_id]
                    use_db = self.uses_db(func)
                    if use_db:
                        func(bot_p, update, trainer, database)
                if not use_db:
                    func(bot_p, update, trainer)

            def handle_safe(bot_p: Bot, update: Update, _bot=bot, _cmd_handlers=cmd_handlers):
                call_with_safe_id(update.message.from_user.id, _bot, handle, bot_p, update, _cmd_handlers)

            bot.updater.dispatcher.add_handler(CommandHandler(command, handle_safe))

        def button_handle(bot_p: Bot, update: Update):
            id = ButtonId.from_string(update.callback_query.data)
            if id not in self.buttonHandlers:
                return
            bttn_handlers = self.buttonHandlers[id]
            with Database() as database:
                trainer = Trainer(update.callback_query.from_user.id)

                menu_id = None
                if trainer.does_exist(database):
                    trainer.load_values(values="menu_id", database=database)
                    menu_id = trainer.menu_id
                if menu_id not in bttn_handlers:
                    return
                func = bttn_handlers[menu_id]
                use_db = self.uses_db(func)
                if use_db:
                    func(bot_p, update, trainer, database)
            if not use_db:
                func(bot_p, update, trainer)

        def button_handle_safe(bot_p: Bot, update: Update, _bot=bot):
            call_with_safe_id(update.callback_query.from_user.id, _bot, button_handle, bot_p, update)

        bot.updater.dispatcher.add_handler(CallbackQueryHandler(button_handle_safe))

        def message_handle(bot_p: Bot, update: Update):
            with Database() as database:
                trainer = Trainer(update.message.from_user.id)
                menu_id = None
                if trainer.does_exist(database):
                    trainer.load_values(values="menu_id", database=database)
                    menu_id = trainer.menu_id
                if menu_id not in self.messageHandlers:
                    return
                func = self.messageHandlers[menu_id]
                use_db = self.uses_db(func)
                if use_db:
                    func(bot_p, update, trainer, database)
            if not use_db:
                func(bot_p, update, trainer)

        def message_handle_safe(bot_p: Bot, update: Update, _bot=bot):
            call_with_safe_id(update.message.from_user.id, _bot, message_handle, bot_p, update)

        bot.updater.dispatcher.add_handler(MessageHandler(Filters.text, message_handle_safe))
