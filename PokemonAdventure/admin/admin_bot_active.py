from telegram import Bot, Update
import logging

from admin.admin_bot_commands import AdminBotCommands

logger = logging.getLogger(__name__)


class AdminBotActive(AdminBotCommands):
    """Admin Bot - Active State"""

    def __init__(self, admin_bot):
        super().__init__(admin_bot)

    def comm_start_bot(self, bot: Bot, update: Update):
        bot.send_message(update.message.chat_id, "Bot already started")

    def comm_stop_bot(self, bot: Bot, update: Update):
        bot.send_message(update.message.chat_id, "Stopping bot...")
        self.adminBot.mainBot.stop()
        bot.send_message(update.message.chat_id, "Stopped bot.")

    def comm_status(self, bot: Bot, update: Update):
        bot.send_message(update.message.chat_id, "Bot is currently running")

    def comm_create_database(self, bot: Bot, update: Update):
        bot.send_message(update.message.chat_id, "Bot must be stopped for this action")
