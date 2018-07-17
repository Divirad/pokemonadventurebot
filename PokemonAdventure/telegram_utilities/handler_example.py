from typing import List

from telegram import Bot, Update

from database.db import Database
from gamelogic.getdata.trainer import Trainer
from telegram_utilities.handler import Handler
from telegram_utilities.registry import Registry


class HandlerExample(Handler):
    def get_sub_handler(self) -> List['Handler']:
        return []

    def register(self, registry: Registry):
        registry.add_command_handler("/comm1", self.command1, [1, 2])  # command for menu_ids 1 and 2
        registry.add_command_handler("/comm2", self.command2, [None])  # command for not registered Trainer

    def command1(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        pass

    def command2(self, bot: Bot, update: Update, trainer: Trainer):
        pass
