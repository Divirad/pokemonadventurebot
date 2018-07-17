from telegram import Bot, Update

from database.db import Database
from telegram_utilities.handler import Handler
from telegram_utilities.registry import Registry
from typing import List
from gamelogic.menu_id import MenuId
from gamelogic.getdata.trainer import Trainer

from gamelogic.button_id import ButtonId as ButtonId
from errorhandling.errorhandling import not_implemented_yet

class NewsHandler(Handler):

    def get_sub_handler(self) -> List['Handler']:
        return []

    def register(self, registry: Registry):

        # Main-Menu
        registry.add_button_handler(ButtonId.INFO_NEWS, self.donate, [MenuId.MAIN_MENU])

    def donate(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        not_implemented_yet(bot, update, trainer)