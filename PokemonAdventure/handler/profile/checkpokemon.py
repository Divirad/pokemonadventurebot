from errorhandling.errorhandling import delete_message
from gamelogic.button_id import ButtonId
from gamelogic.getdata.pokemon import Pokemon
from gamelogic.menu_id import MenuId
from gamelogic.getdata.trainer import Trainer

from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram_utilities.handler import Handler
from telegram_utilities.registry import Registry
from typing import List

from database.db import Database

class PokemonTeamHandler(Handler):

    def get_sub_handler(self) -> List['Handler']:
        return []

    def register(self, registry: Registry):
        registry.add_button_handler(ButtonId.PROFILE_POKEMON, self.pokemon_team, [MenuId.MAIN_MENU])

    def pokemon_team(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        delete_message(bot, update)

        team = trainer.get_team(database, "id, name, level, teamnr, currenthp, gender")
        msg = ""
        for p in team:
            poke = Pokemon(p.id)
            poke.load_values(database, "teamnr, name, level, currenthp")
            poke.load_values(database, "gender, hp_exp, hp_dv, species_id, current_status")
            msg += """ ({0}) {1} [{5}] Lv. {2} \n    HP: {3}/{4}\n""".format(
                poke.teamnr,
                poke.name,
                poke.level,
                poke.currenthp,
                poke.calculate_max_hp(),
                poke.gender)
        bot.send_message(trainer.id,
                         "Your Pokémon-Team:\n" + msg,
                         reply_markup =
                         InlineKeyboardMarkup([[InlineKeyboardButton("⏪ Profile",
                                                                     callback_data = str(ButtonId.MENU_PROFILE))]]))