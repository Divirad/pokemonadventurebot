from telegram import Bot, Update

from telegram_utilities.handler import Handler
from telegram_utilities.registry import Registry
from typing import List

from database.db import Database
from gamelogic.menu_id import MenuId
from gamelogic.getdata.trainer import Trainer


class Donate(Handler):
    def get_sub_handler(self) -> List['Handler']:
        return []

    def register(self, registry: Registry):
        # Main-Menu
        registry.add_button_handler("daily_reward", self.mainmenu, [MenuId.MAIN_MENU])

    def reward(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        pass

