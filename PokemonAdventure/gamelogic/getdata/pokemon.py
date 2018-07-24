import random

from database import Data
from database.DBIdObject import DBIdObject
from gamelogic.fighting.learned_move import LearnedMove


# noinspection PyAttributeOutsideInit
class Pokemon(DBIdObject):
    """
    A Class that symbolizes a Pokemon with every Value.
    """
    table = 'pokemon'
    teamnr: int
    name: str
    level: int
    currenthp: int

    def __init__(self, p_id):
        """
        Initializes a Pokemonobject with the Pokemon-ID
        :param p_id: Pokemon-ID
        """
        DBIdObject.__init__(self, p_id)

    @classmethod
    def create_new(cls, database, species, level: int, owner = None, name: str = None) -> 'Pokemon':
        """
        creates a new Pokemon and inserts it to th database
        :param database: database to insert Pokemon
        :param species: Species Of the Pokemon
        :param level: Level Of the Pokemon
        :param owner: Owner of Pokemon
        :param name: Nickname of the pokemon
        :return: created Pokemon
        """

        result = Pokemon(None)

        result.species = species
        result.level = level
        result.ownedby = result.originaltrainer = owner
        result.species = species
        if name is None:
            result.name = species.name.upper()
        else:
            result.name = name

        result.hp_exp = 0
        result.generate_genes()
        result.generate_gender()

        result.currenthp = result.calculate_max_hp()
        result.current_status = "0"

        if owner is None:
            result.teamnr = None
        else:
            owner.menu_id = 2
            team = owner.get_team(database, "id")
            if len(team) < 6:
                result.teamnr = len(team) + 1
            else:
                result.teamnr = None
            owner.update_values(database, "menu_id")

        moves = species.get_last_moves(level)
        result.move0 = LearnedMove.create_new(database, moves[0]) if len(moves) >= 1 else None
        result.move1 = LearnedMove.create_new(database, moves[1]) if len(moves) >= 2 else None
        result.move2 = LearnedMove.create_new(database, moves[2]) if len(moves) >= 3 else None
        result.move3 = LearnedMove.create_new(database, moves[3]) if len(moves) >= 4 else None

        result.id = result.insert_new(database, 'ownedby, originaltrainer, species_id, name, level, currenthp,'
                                                ' current_status, hp_dv, attack_dv, defense_dv, special_dv, speed_dv,'
                                                ' gender, teamnr, move0, move1, move2, move3')

        return result

    def generate_genes(self):
        """
        generates genes of a pokemon object
        """
        self.attack_dv = random.randint(0, 15)
        self.defense_dv = random.randint(0, 15)
        self.special_dv = random.randint(0, 15)
        self.speed_dv = random.randint(0, 15)
        hptemp = 0
        if self.attack_dv % 2 == 0:
            hptemp += 8
        if self.defense_dv % 2 == 0:
            hptemp += 4
        if self.special_dv % 2 == 0:
            hptemp += 2
        if self.speed_dv % 2 == 0:
            hptemp += 1

        self.hp_dv = hptemp

    def generate_gender(self):
        """
        generates gender
        """
        if self.species.gender is not None:
            self.gender = self.species.gender
        else:
            g = random.randint(0, 65000)
            if g == 65000:
                self.gender = 't'  # GET A FANCY ULTRA RARE
            else:  # TRANSSEXUAL POKEMON
                perc = (self.attack_dv / 15) * 100  # CHANCE: 1:65000
                if random.randint(0, 100) >= int(perc):
                    self.gender = 'f'
                else:
                    self.gender = 'm'

    # noinspection PyUnresolvedReferences
    def calculate_max_hp(self) -> int:
        """
        Calculates the max hp, this pokemon can have.

        :needs: species, hp_dv, hp_ev, level
        :return: the max hp
        """
        return int((((self.species.hp_base + self.hp_dv) * 2 + ((self.hp_exp ** (1 / 2)) / 4)) / 100) + self.level + 10)

    def get_attribute(self, name):
        """
        gets an attribute of the pokemon object in the MySQL database
        :param name: name of the column
        :return: data of the field
        """
        if name == "species_id":
            return self.species.id
        elif name == "ownedby":
            return None if self.ownedby is None else self.ownedby.id
        elif name == "originaltrainer":
            return None if self.originaltrainer is None else self.originaltrainer.id
        elif name == "move0":
            return None if self.move0 is None else self.move0.id
        elif name == "move1":
            return None if self.move1 is None else self.move1.id
        elif name == "move2":
            return None if self.move2 is None else self.move2.id
        elif name == "move3":
            return None if self.move3 is None else self.move3.id
        else:
            return getattr(self, name)

    def has_attribute(self, name):
        """
        has the object an attribute?
        :param name: name of the column
        :return: boolean
        """
        if name == "species_id":
            return hasattr(self, "species")
        else:
            return hasattr(self, name)

    def set_attribute(self, name, value):
        """
        sets attribute
        :param name: name of the column
        :param value: value of the field
        """
        if name == "species_id":
            self.species = Data.all_species[value - 1]
        elif name == "ownedby":
            self.ownedby = trainer.Trainer(value)
        elif name == "originaltrainer":
            self.originaltrainer = trainer.Trainer(value)
        elif name == "move0":
            self.move0 = LearnedMove(value) if value is not None else None
        elif name == "move1":
            self.move1 = LearnedMove(value) if value is not None else None
        elif name == "move2":
            self.move2 = LearnedMove(value) if value is not None else None
        elif name == "move3":
            self.move3 = LearnedMove(value) if value is not None else None
        else:
            setattr(self, name, value)

    def get_move(self, i: int):
        return getattr(self, "move%d" % i)


from gamelogic.getdata import trainer
