from telegram import Bot, Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup

from telegram_utilities.handler import Handler
from telegram_utilities.registry import Registry
from typing import List

from database.db import Database
from errorhandling.errorhandling import delete_message
from gamelogic.menu_id import MenuId
from gamelogic.getdata.trainer import Trainer

from gamelogic.button_id import ButtonId as ButtonId

donate_message = """
Thank you for using this bot. We appreciate that you are interested into donating this project! 
We are very thankful to all donations! Every cent will keep this bot and the server up! 
Click on the button to get to our website. You can choose between 
"PayPal", "Bitcoin", "BitcoinCash", "Ethereum" and "LiteCoin".

If you want to support us without spending money use the daily-reward links.
we will gain ~$0.00005 for one click.

Grateful:
Your Divirad Team."""

class DonateHandler(Handler):

    def get_sub_handler(self) -> List['Handler']:
        return []

    def register(self, registry: Registry):

        # Main-Menu
        registry.add_button_handler(ButtonId.DAILY_DONATE, self.donate, [MenuId.MAIN_MENU])

    def donate(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        delete_message(bot, update)
        buttons = [[InlineKeyboardButton("Donate!",
                        url= "http://www.divirad.com/pokemonadventurebot/donate.html")],
                   [InlineKeyboardButton("⏪ Info", callback_data = str(ButtonId.MENU_INFO))]]
        markup = InlineKeyboardMarkup(buttons)
        bot.send_message(trainer.id, donate_message, ParseMode.MARKDOWN, reply_markup = markup)
