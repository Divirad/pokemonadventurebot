from math import floor
from random import randint

from gamelogic.getdata import pokemon
from database.DBIdObject import DBIdObject
from database.db import Database


class Fight(DBIdObject):
    """
    Current fight between two pokemons synchronized with the database
    """
    table = "pokemonfight"

    def __init__(self, id):
        DBIdObject.__init__(self, id)

    @classmethod
    def create_new(cls, database: Database, wild_poke: pokemon.Pokemon, trainer_poke: pokemon.Pokemon)-> 'Fight':
        """
        Creates a new object of Fight and inserts it into the database

        :param database: pokemon database
        :param wild_poke: wild pokemon
        :param trainer_poke: pokemon owned by the trainer 
        :return: the new Fight object
        """
        result = Fight(None)
        result.wildPokemon = wild_poke
        result.trainerPokemon = trainer_poke

        result.wild_attack = Fight.calc_stat(wild_poke.species.attack_base, wild_poke.attack_dv, wild_poke.level)
        result.wild_defense = Fight.calc_stat(wild_poke.species.defense_base, wild_poke.defense_dv, wild_poke.level)
        result.wild_special = Fight.calc_stat(wild_poke.species.special_base, wild_poke.special_dv, wild_poke.level)
        result.wild_speed = Fight.calc_stat(wild_poke.species.speed_base, wild_poke.speed_dv, wild_poke.level)

        result.trainer_attack = Fight.calc_stat(trainer_poke.species.attack_base, trainer_poke.attack_dv,
                                                trainer_poke.level)
        result.trainer_defense = Fight.calc_stat(trainer_poke.species.defense_base, trainer_poke.defense_dv,
                                                 trainer_poke.level)
        result.trainer_special = Fight.calc_stat(trainer_poke.species.special_base, trainer_poke.special_dv,
                                                 trainer_poke.level)
        result.trainer_speed = Fight.calc_stat(trainer_poke.species.speed_base, trainer_poke.speed_dv,
                                               trainer_poke.level)

        result.wild_attack_stage = 0
        result.wild_defense_stage = 0
        result.wild_special_stage = 0
        result.wild_speed_stage = 0
        result.trainer_attack_stage = 0
        result.trainer_defense_stage = 0
        result.trainer_special_stage = 0
        result.trainer_speed_stage = 0

        result.id = result.insert_new(database,
                                      "wildPokemon, trainerPokemon, wild_attack, wild_defense, wild_special,"
                                      " wild_speed, trainer_attack, trainer_defense, trainer_special, trainer_speed,"
                                      " wild_attack_stage, wild_defense_stage, wild_special_stage, wild_speed_stage,"
                                      " trainer_attack_stage, trainer_defense_stage, trainer_special_stage,"
                                      " trainer_speed_stage")
        return result

    def turn_move_wild(self, database, trainer_move):
        wild_move_index = randint(0, 3)
        if wild_move_index == 0:
            self.wildPokemon.load_values(database, "move0")
            wild_move = self.wildPokemon.move0
        if wild_move_index == 1:
            self.wildPokemon.load_values(database, "move1")
            wild_move = self.wildPokemon.move1
        if wild_move_index == 2:
            self.wildPokemon.load_values(database, "move2")
            wild_move = self.wildPokemon.move2
        if wild_move_index == 3:
            self.wildPokemon.load_values(database, "move3")
            wild_move = self.wildPokemon.move3

    @staticmethod
    def calc_stat(base, dv, level):
        return floor(((base + dv) * 2 + 63) * level / 100) + 5

    @staticmethod
    def does_hit(move, accuracy_stage, evade_stage):
        r = randint(0, 255)
        accuracy_modifier = (accuracy_stage+2) / 2 if accuracy_stage >= 0 else 2 / (-accuracy_stage+2)
        evade_modifier = (evade_stage+2) / 2 if evade_stage >= 0 else 2 / (-evade_stage+2)
        return r < int(int(move.accuracy * accuracy_modifier)/evade_modifier)

    @staticmethod
    def calc_stage_modifier(stage):
        return (stage+2) / 2 if stage >= 0 else 2 / (-stage+2)

    def get_attribute(self, name):
        if name == "wildPokemon":
            return self.wildPokemon.id
        elif name == "trainerPokemon":
            return self.trainerPokemon.id
        else:
            return getattr(self, name)

    # noinspection PyAttributeOutsideInit
    def set_attribute(self, name, value):
        if name == "wildPokemon":
            self.wildPokemon = pokemon.Pokemon(value)
        elif name == "trainerPokemon":
            self.trainerPokemon = pokemon.Pokemon(value)
        else:
            setattr(self, name, value)
