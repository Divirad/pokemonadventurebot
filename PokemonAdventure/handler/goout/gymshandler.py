from errorhandling.errorhandling import not_implemented_yet
from gamelogic.button_id import ButtonId
from gamelogic.menu_id import MenuId
from telegram_utilities.handler import Handler
from telegram_utilities.registry import Registry
from typing import List


class GymsHandler(Handler):

    def get_sub_handler(self) -> List['Handler']:
        return []

    def register(self, registry: Registry):
        registry.add_button_handler(ButtonId.GOOUT_GYMS, not_implemented_yet, [MenuId.MAIN_MENU])
        pass