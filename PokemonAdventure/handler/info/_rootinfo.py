from handler.info import about, news
from telegram_utilities.handler import Handler
from telegram_utilities.registry import Registry
from typing import List

class RootInfo(Handler):

    def get_sub_handler(self) -> List['Handler']:
        return [about.About(),
                news.NewsHandler()]

    def register(self, registry: Registry):
        pass