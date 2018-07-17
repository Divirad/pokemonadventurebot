import os
import threading

from telegram import Bot, Update  # , ParseMode
from MySQLdb import MySQLError
import json
from datetime import datetime
import logging
from os.path import dirname, abspath
import _thread
import git
from threading import Lock

from database.db import Database
from telegram_utilities.bot_extension import send_large_code_message

logger = logging.getLogger(__name__)


class AdminBotCommands:
    """
    Base class for all admin commands.
    All command handling methods must be declared in this class and start with 'comm_'. They will be automatically added
    as handler to the telegram bot. If functionallity needs to be implemented in a super class, the methods can be
    abstract. The doc string of the base method is added to the help page.
    """

    def __init__(self, admin_bot):
        """
        Initializes the Adminbot Commands
        :param admin_bot:
        """
        self.adminBot = admin_bot
        self.updateLock = Lock()
        if AdminBotCommands.help_page is None:
            AdminBotCommands.help_page = AdminBotCommands.create_help_page()

    def comm_update(self, bot: Bot, update: Update):
        """/update updates all files of the bot from the git repo and restarts the bot"""
        if self.updateLock.acquire(blocking=False):
            try:
                directory = dirname(abspath(__file__)) + "/../../"
                g = git.cmd.Git(directory)
                msg = g.pull()
                if msg != "Already up-to-date.":
                    send_large_code_message(bot, update.message.chat_id, msg)
                    logger.info(msg)
                    bot.send_message(update.message.chat_id, "Restarting...")
                    _thread.start_new_thread(self.adminBot.restart, ())
                else:
                    bot.send_message(update.message.chat_id, msg)
            finally:
                self.updateLock.release()
        else:
            bot.send_message(update.message.chat_id, "Bot is currently updating")

    @staticmethod
    def jdefault(o: datetime):  # Changed by Max from "o" to "o: datetime"
        """formats datetime if type is datetime"""
        return o.isoformat()
        # if type(o) is datetime:
        #    return o.isoformat()
        # else:
        #    return o

    def comm_sql_get(self, bot: Bot, update: Update):
        """/sql executes a mysql select command on the pokemon database"""
        txt = update.message.text
        if len(txt) <= len("/sql_get "):
            return  # no parameter given

        cmd = txt[len("/sql_get "):]

        with Database() as database:
            try:
                result = database.get_data_sorted(cmd)
                send_large_code_message(bot, update.message.chat_id,
                                        json.dumps(result, default=self.jdefault, indent=4))
            except MySQLError as e:
                bot.send_message(update.message.chat_id, "{0}".format(e))

    @staticmethod
    def comm_sql_cmd(bot: Bot, update: Update):
        """/sql executes a mysql insert/update command on the pokemon database"""
        txt = update.message.text
        if len(txt) <= len("/sql_cmd "):
            return  # no parameter given

        cmd = txt[len("/sql_cmd "):]

        with Database() as database:
            try:
                database.cmd(cmd)
                bot.send_message(update.message.chat_id, "Executed command without errors")
            except MySQLError as e:
                bot.send_message(update.message.chat_id, "{0}".format(e))

    def comm_start(self, bot: Bot, update: Update):
        """prints a message and the /help manual"""
        bot.send_message(update.message.chat_id, "Welcome to this epic bot!\n"
                                                 "You can use this bot to manage the @PokemonAdventureBot")
        self.comm_help(bot, update)

    @staticmethod
    def comm_help(bot: Bot, update: Update):
        """/help for this help page"""
        bot.send_message(update.message.chat_id, AdminBotCommands.help_page)

    def comm_stats(self, bot: Bot, update: Update):
        """/stats for info about the current process"""
        bot.send_message(update.message.chat_id,
                         "Thread count: %d\n"
                         "database total connection count: %d\n"
                         "database active connection count: %d\n"
                         "Process id: %d"
                         % (threading.active_count(), Database.get_count()[0], Database.get_count()[1], os.getpid()))

    def comm_start_bot(self, bot: Bot, update: Update):
        """/start_bot to start the bot, admin bot needs to run in passive mode"""
        raise NotImplementedError("abstract comm_start_bot not implemented")

    def comm_stop_bot(self, bot: Bot, update: Update):
        """/stop_bot to stop the bot and start the admin bot in passive mode"""
        raise NotImplementedError("abstract comm_stop_bot not implemented")

    def comm_status(self, bot: Bot, update: Update):
        """/status to get the current state of the bot"""
        raise NotImplementedError("abstract comm_status not implemented")

    def comm_create_database(self, bot: Bot, update: Update):
        """/create_database creates a new database with the DatabaseManager script"""
        raise NotImplementedError("abstract comm_create_database not implemented")

    def comm_delete_user(self, bot: Bot, update: Update):
        """/reset_user"""
        raise NotImplementedError("abstract delete_user not implemented")

    def comm_give_item(self, bot: Bot, update: Update):
        """/gi"""

        raise NotImplementedError("abstract give_item not implemented")

    def comm_give_money(self, bot: Bot, update: Update):
        """/gm"""

        raise NotImplementedError("abstract give_money not implemented")

    def comm_give_pokemon(self, bot: Bot, update: Update):
        """/dp"""

        raise NotImplementedError("abstract give_pokemon not implemented")

    def comm_del_item(self, bot: Bot, update: Update):
        """/di"""

        raise NotImplementedError("abstract del_item not implemented")

    def comm_del_money(self, bot: Bot, update: Update):
        """/dm"""

        raise NotImplementedError("abstract del_money not implemented")

    def comm_del_pokemon(self, bot: Bot, update: Update):
        """/dp"""

        raise NotImplementedError("abstract del_pokemon not implemented")

    @classmethod
    def create_help_page(cls) -> str:
        """Creates a /help manual"""
        page = ""
        for name in dir(cls):
            if name.startswith("comm_"):
                doc = getattr(cls, name).__doc__
                if doc is not None:
                    page += "\n" + doc
                    # page += "\n" + doc
                else:
                    page += "\n/" + name[len("comm_"):] + " is undocumented"
                    # page += "\n/" + name[len("comm_"):] + " is undocumented"
        return page

    help_page = None
