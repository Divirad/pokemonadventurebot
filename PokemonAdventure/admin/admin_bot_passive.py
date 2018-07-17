from telegram import Bot, Update
import MySQLdb
from private import database_user, database_passwd
import sys
from requests.exceptions import Timeout
from os.path import dirname, abspath

sys.path.append(dirname(abspath(__file__)) + "/../../Downloader")
sys.path.append(dirname(abspath(__file__)) + "/../../CreateDatabase")
import downloader
from CreateTables import create_tables
from FillTables import fill_tables
from admin.admin_bot_commands import AdminBotCommands


class AdminBotPassive(AdminBotCommands):

    def __init__(self, admin_bot):
        super().__init__(admin_bot)

    def comm_start_bot(self, bot: Bot, update: Update):
        bot.send_message(update.message.chat_id, "Starting bot...")
        if self.adminBot.mainBot.start():
            bot.send_message(update.message.chat_id, "Started bot.")
        else:
            bot.send_message(update.message.chat_id, "Failed to start bot. Check the log for more information.")

    def comm_stop_bot(self, bot: Bot, update: Update):
        bot.send_message(update.message.chat_id, "Bot already stopped")

    def comm_status(self, bot: Bot, update: Update):
        bot.send_message(update.message.chat_id, "Bot is stopped")

    def comm_create_database(self, bot: Bot, update: Update):
        bot.send_message(update.message.chat_id, "Creating DB")
        try:
            db = MySQLdb.connect(host="localhost", user=database_user, passwd=database_passwd, charset='utf8')
        except MySQLdb.Error as err:
            bot.send_message(update.message.chat_id, "{0}".format(err))
        else:
            cursor = db.cursor()
            try:
                downloader.main(['-i', 'local', '-o', 'database', '--if',
                                 dirname(abspath(__file__)) + '/../../CreateDatabase/pokemon_data.json',
                                 '--db', 'pokemon'])
                cursor.execute("USE pokemon")
            except MySQLdb.Error as err:
                return err.args[1]
            try:  # fill database
                create_tables(cursor)
                fill_tables(cursor)
                db.commit()
            except MySQLdb.Error as err:
                bot.send_message(update.message.chat_id, "{0}".format(err))
            except Timeout as err:
                bot.send_message(update.message.chat_id, "{0}".format(err))
            else:
                bot.send_message(update.message.chat_id, "Created DB succesfull new")
