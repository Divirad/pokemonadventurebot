from random import randint, getrandbits
from enum import Enum

from database.db import Database
from database.Data import Move
from gamelogic.getdata.pokemon import Pokemon
from data import State
from gamelogic.fighting.fight import Fight

# TODO Please fix Errors :)

def run_turn(fight: Fight, database: Database, trainer_move_index: int) -> str:
    """
    Runs one complete turn of the battle

    :param fight: current Fight object
    :param database: pokemon database
    :param trainer_move_index: selected move of the trainer
    :return: message for the trainer
    :needs: all fields
    """
    trainer_move = fight.prepare_battle(database, fight.trainerPokemon, trainer_move_index)
    wild_move = fight.prepare_battle(database, fight.wildPokemon, randint(0, 3))
    if fight.does_trainer_start(trainer_move, wild_move):
        trainer_damage, trainer_effectivity, trainer_ = fight.calc_attack(trainer_move)
        if (fight.wildPokemon)
            wild_move = fight.calc_attack(wild_move)
    else:
        wild_move = fight.calc_attack(wild_move)
        trainer_damage = fight.calc_attack(trainer_move)


class Outcome(Enum):
    """
    Enum, that describes the outcome of one Turn. It is used to determine which action after a turn has to occur
    """
    FAINTED = 0
    LOST = 1
    WON = 2


def trainer_turn(fight: Fight, move: Move) -> (Outcome, str):
    """
    Runs the turn of the trainer. The trainer pokemon attacks

    :param fight: current Fight object
    :param move: move of the pokemon
    :return: outcome, message for the trainer
    """
    damage, effectivity, new_state = fight.calc_attack(move)


def prepare_battle(database: Database, pokemon: Pokemon, move_index) -> Move:
    """
    Loads all neccessarry values from the database

    :param database: pokemon database
    :param pokemon: the pokemon, which data should be loaded
    :param move_index: move index of the used move
    :return: the used move
    """
    if move_index == 0:
        pokemon.load_values(database, "move0")
        move = pokemon.move0
    elif move_index == 1:
        pokemon.load_values(database, "move1")
        move = pokemon.move1
    elif move_index == 2:
        pokemon.load_values(database, "move2")
        move = pokemon.move2
    else:
        pokemon.load_values(database, "move3")
        move = pokemon.move3
    return move


def turn_move_wild(fight: Fight, database: Database):
    """
    Runs the turn of the wild pokemon. Wild pokemon randomly select a move and executes it

    :param fight: current Fight object
    :param database: pokemon database
    """


def calc_attack(move: Move, level: int, attack: int, defense: int, attack_stage: int, defense_stage: int) -> (int, str, State):
    """
    Calculates the attack of one pokemon

    :param move: used move of the attacking pokemon
    :return: damage, effectivity, new state
    """
    attack_modifier = calc_stage_modifier(attack_stage)
    defense_modifier = calc_stage_modifier(defense_stage)
    # TODO: badge
    attack_badge_bonus = 1
    defense_badge_bonus = 1

    attack = min(int(int(int(attack * attack_modifier) * attack_badge_bonus) * burn_modifier), 999)
    defense = min(int(int(int(defense * defense_modifier) * defense_badge_bonus) * self_ko_modifier), 999)

    if attack > 255 or defense > 255:
        attack = (attack / 4) % 255
        defense = (defense / 4) % 255

    damage = int(int(int((min(int(int(
        (int((level * critical_modifier % 256) * 0.4) + 2) * max(int(attack * B), 1) * move.power / max(
            int(defense * E), 1)) / 50), 997) + 2) * stab) * type_effectivness) * R / 255)
    return 5, "not very effective", 7


def does_trainer_start(fight: Fight, trainer_move: Move, wild_move: Move):
    if trainer_move.priority > wild_move.priority:
        return True
    elif trainer_move.priority < wild_move.priority:
        return False
    else:
        if fight.trainer_speed > fight.wild_speed:
            return True
        elif fight.trainer_speed < fight.wild_speed:
            return False
        else:
            return getrandbits(1)


def does_hit(move, accuracy_stage, evade_stage):
    r = randint(0, 255)
    accuracy_modifier = (accuracy_stage + 2) / 2 if accuracy_stage >= 0 else 2 / (-accuracy_stage + 2)
    evade_modifier = (evade_stage + 2) / 2 if evade_stage >= 0 else 2 / (-evade_stage + 2)
    return r < int(int(move.accuracy * accuracy_modifier) / evade_modifier)


def calc_stage_modifier(stage: int) -> float:
    """
    converts the stage value of a stat into a factor

    :param stage: stage of a value
    :return: factor for that stage
    """
    return (stage + 2) / 2 if stage >= 0 else 2 / (-stage + 2)