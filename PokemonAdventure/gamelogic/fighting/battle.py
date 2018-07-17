
from gamelogic.fighting.fight import Fight
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Bot, Update, Message
from sys import stderr

from database import Data
from database.db import get_database, free_database, Database
from gamelogic.fighting import battle_message as battle_message
from gamelogic.getdata.pokemon import Pokemon
from gamelogic.getdata.trainer import Trainer


# Menu IDs
# F - Fight
# P - Pokemon
# I - Items
# R - Run
# M0 - Move0
# M1 - Move1M
# M2 - Move2
# M3 - Move3
# N - New Pokemon
# B - Back

def battle_cb(bot: Bot, update: Update, data: str):
    """
    Calls Battle UI Methods, depending on the callback data

    :param bot: telegram bot
    :param update: current update with message
    :param data: callback data containing the handler id
    """
    clicked_menu = data[1]
    msg = update.callback_query.message

    if clicked_menu == 'B':
        battle_message.edit_menu(bot, msg, menu_main)
    else:
        database = get_database()
        trainer = Trainer(msg.chat_id)
        try:
            if clicked_menu == 'P':
                menu_pokemon(database, trainer, bot, msg)
            elif clicked_menu == 'F':
                menu_fight(database, trainer, bot, msg)
            elif clicked_menu == 'M':
                move_chosen(database, trainer, bot, msg, data)
        finally:
            free_database(database)


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


def menu_pokemon(database: Database, trainer: Trainer, bot: Bot, msg: Message):
    """
    Handles the click on the pokemon button. Therefore changing the current keyboard to the list of pokemons in the team

    :param database: pokemon database
    :param trainer: trainer of the message
    :param bot: telegram bot
    :param msg: old telegram message, which keyboard will be updated
    """
    team = trainer.get_team(database, "id, name, level")
    buttons = []
    for i, t in enumerate(team):
        buttons.append([InlineKeyboardButton(
            t.name + " - lvl. " + str(t.level), callback_data='FN' + str(i))])
    buttons.append([InlineKeyboardButton("Back", callback_data='FB')])
    battle_message.edit_menu(bot, msg, InlineKeyboardMarkup(buttons))


def menu_fight(database, trainer, bot, msg):
    """
    Handles a click on the fight button. Therefor changing the current keyboard to the list of available moves

    :param database: pokemon database
    :param trainer: trainer of the message
    :param bot: telegram bot
    :param msg: old telegram message, which keyboard will be updated
    :return:
    """
    trainer.load_values(database, "fight")
    trainer.fight.load_values(database, "trainerPokemon")
    trainer.fight.trainerPokemon.load_values(database, "move0, move1, move2, move3")
    m0 = trainer.fight.trainerPokemon.move0
    m1 = trainer.fight.trainerPokemon.move1
    m2 = trainer.fight.trainerPokemon.move2
    m3 = trainer.fight.trainerPokemon.move3
    if m0 is not None:
        m0.load_values(database, "move_id, currentap")
    if m1 is not None:
        m1.load_values(database, "move_id, currentap")
    if m2 is not None:
        print(m2.id)
        m2.load_values(database, "move_id, currentap")
    if m3 is not None:
        m3.load_values(database, "move_id, currentap")
    battle_message.edit_menu(bot, msg, InlineKeyboardMarkup([
        [InlineKeyboardButton(" " if m0 is None else "%s  %d/%d" % (m0.move.name, m0.currentap, m0.move.pp),
                              callback_data='FM0' if m0 is not None else 'X'),
         InlineKeyboardButton(" " if m1 is None else "%s  %d/%d" % (m1.move.name, m1.currentap, m1.move.pp),
                              callback_data='FM1' if m1 is not None else 'X')],
        [InlineKeyboardButton(" " if m2 is None else "%s  %d/%d" % (m2.move.name, m2.currentap, m2.move.pp),
                              callback_data='FM2' if m2 is not None else 'X'),
         InlineKeyboardButton(" " if m3 is None else "%s  %d/%d" % (m3.move.name, m3.currentap, m3.move.pp),
                              callback_data='FM3' if m3 is not None else 'X')],
        [InlineKeyboardButton("Back", callback_data='FB')]]))


menu_main = InlineKeyboardMarkup(
    [[InlineKeyboardButton('FIGHT', callback_data='FF'), InlineKeyboardButton('POKEMON', callback_data='FP')],
     [InlineKeyboardButton('ITEM', callback_data='FI'), InlineKeyboardButton('RUN', callback_data='FR')]],
    one_time_keyboard=True)


def start_wild(bot: Bot, chat_id: int, user_id: int, species_id: int, level: int):
    """
    Starts a new fight between a trainer and a new wild pokemon, that will be spawned. The bot send a new battle message
    to the trainer

    :param bot: telegram bot, which send the message
    :param chat_id: chat where the new battle message will be sent to
    :param user_id: id of the trainer
    :param species_id: species of the wild pokemon
    :param level: level of the wild pokemon
    """
    database = get_database()
    try:
        trainer = Trainer(user_id)
        wild_pokemon = Pokemon.create_new(database, Data.all_species[species_id - 1], level)
        trainer_team = trainer.get_team(database, "id, currenthp")
        for p in trainer_team:
            if p.currenthp > 0:
                trainer_pokemon = p
                break
        else:
            print("Trainer in fight with no available pokemon!", file=stderr)
            return
        trainer_pokemon.load_values(database, "hp_dv, attack_dv, defense_dv, special_dv, speed_dv, hp_exp, attack_exp, "
                                              "defense_exp, special_exp, speed_exp, species_id, currenthp, level, "
                                              "name, hp_ev")
        trainer.fight = Fight.create_new(database, wild_pokemon, trainer_pokemon)
        trainer.menu_id = 4
        trainer.update_values(database, "fight, menu_id")
    finally:
        free_database(database)
    battle_message.send(bot, chat_id, menu_main, wild_pokemon, trainer_pokemon, "Wild %s appeared!" % wild_pokemon.name)
