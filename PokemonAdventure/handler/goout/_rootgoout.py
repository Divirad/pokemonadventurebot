from telegram_utilities.handler import Handler
from telegram_utilities.registry import Registry
from typing import List

from handler.goout import center,gymshandler,shophandler
from handler.goout.rpg import walkhandler


class RootGoOut(Handler):

    def get_sub_handler(self) -> List['Handler']:
        return [center.PokemonCenterHandler(),
                gymshandler.GymsHandler(),
                shophandler.ShopHandler(),
                walkhandler.WalkAround()]

    def register(self, registry: Registry):
        pass