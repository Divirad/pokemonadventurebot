from gamelogic.button_id import ButtonId
from gamelogic.fighting.fight import Fight
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Bot, Update, Message
from sys import stderr

from database import Data
from database.db import Database
from gamelogic.fighting import battle_message as battle_message
from gamelogic.getdata.pokemon import Pokemon
from gamelogic.getdata.trainer import Trainer
from gamelogic.menu_id import MenuId


def move_chosen(database: Database, trainer: Trainer, bot: Bot, old_msg: Message, data: str):
    """
    Handles the click on a move button. Therefor runs one round of the battle and updates the battle message.

    :param database: pokemon database
    :param trainer: trainer of the message
    :param bot: telegram bot
    :param old_msg: old telegram message, that will be updated
    :param data: callback data, describing which button was pressed
    """
    trainer.load_values(database, "fight")
    trainer.fight.load_values(database, "trainerPokemon, wildPokemon, wild_attack, wild_defense, wild_special, "
                                        "wild_special, wild_speed, trainer_attack, trainer_defense, trainer_special, "
                                        "trainer_speed")
    msg = trainer.fight.run_turn(database, int(data[2]))
    battle_message.update(bot, old_msg, menu_main, trainer.fight.wildPokemon, trainer.fight.trainerPokemon, msg)


def start_wild(trainer: Trainer, species_id: int, level: int, database: Database) -> (bool, str):
    """
    Starts a new fight between a trainer and a new wild pokemon, that will be spawned. The bot send a new battle message
    to the trainer

    :param database: pokemon database
    :param bot: telegram bot, which send the message
    :param trainer: trainer in the fight
    :param species_id: species of the wild pokemon
    :param level: level of the wild pokemon
    """
    wild_pokemon = Pokemon.create_new(database, Data.all_species[species_id - 1], level)
    trainer_team = trainer.get_team(database, "id, currenthp")
    for p in trainer_team:
        if p.currenthp > 0:
            trainer_pokemon = p
            break
    else:
        return False, "Trainer in fight with no available pokemon!"
    trainer_pokemon.load_values(database, "hp_dv, attack_dv, defense_dv, special_dv, speed_dv, hp_exp, attack_exp, "
                                          "defense_exp, special_exp, speed_exp, species_id, currenthp, level, "
                                          "name")
    trainer.fight = Fight.create_new(database, wild_pokemon, trainer_pokemon)
    trainer.menu_id = int(MenuId.BATTLE)
    trainer.update_values(database, "fight, menu_id")

    return True, "Wild %s appeared!" % wild_pokemon.name
