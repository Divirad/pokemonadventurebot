from telegram_utilities.handler import Handler
from telegram_utilities.registry import Registry
from typing import List

from handler.info.donatehandler import DonateHandler


class RootDaily(Handler):

    def get_sub_handler(self) -> List['Handler']:
        return [DonateHandler()]

    def register(self, registry: Registry):
        pass