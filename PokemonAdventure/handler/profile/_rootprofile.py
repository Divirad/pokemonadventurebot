from telegram_utilities.handler import Handler
from telegram_utilities.registry import Registry
from typing import List

from handler.profile import baghandler, checkpokemon, pokedex, trainercardhandler

class RootProfile(Handler):

    def get_sub_handler(self) -> List['Handler']:
        return [baghandler.BagHandler(),
                checkpokemon.PokemonTeamHandler(),
                pokedex.PokedexHandler(),
                trainercardhandler.TrainerCardHandler()]

    def register(self, registry: Registry):
        pass