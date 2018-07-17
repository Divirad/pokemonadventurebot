from telegram import Bot, Update

from gamelogic.getdata.trainer import Trainer
from telegram_utilities.handler import Handler
from telegram_utilities.registry import Registry
from typing import List

from gamelogic.button_id import ButtonId
from gamelogic.menu_id import MenuId

from database.db import Database
from errorhandling.errorhandling import not_implemented_yet


class BagHandler(Handler):

    def get_sub_handler(self) -> List['Handler']:
        return[]

    def register(self, registry: Registry):
        registry.add_button_handler(ButtonId.PROFILE_BAG, not_implemented_yet, [MenuId.MAIN_MENU])

    def bag(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        pass
