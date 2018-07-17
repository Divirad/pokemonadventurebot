from database.DBObject import DBObject
from gamelogic.getdata.pokemon import Pokemon

# noinspection PyAttributeOutsideInit
# from gamelogic.getdata.pokemon import Pokemon
from gamelogic.getdata.trainer import Trainer


class Pokedex(DBObject):
    """
    A Pokedex Entry with SpeciesID and TrainerID
    """
    species: int
    pokemon: Pokemon
    table = 'pokedex'

    def __init__(self, id: int, trainer: Trainer):
        """
        Initializes a Pokedex entry
        :param id: id of the species
        :param trainer: a Trainer-object
        """
        self.id = id
        self.trainer = trainer

    def identificator(self):
        """
        String that identifies a pokedex entry
        :return: String Tuple
        """
        return "id = %s AND trainerid = %s" % self.pokemon.id, self.trainer.id

    def get_attribute(self, name):
        """
        gets attribute
        :param name: name of the attribute
        :return: atribute value
        """
        if name == "id":
            return self.id
        elif name == "trainerid":
            return self.trainer.id
        else:
            return getattr(self, name)

    def has_attribute(self, name) -> bool:
        """
        Has the object this attribute?
        :param name: name of the attribute
        :return: True if has attribute
        """
        if name == "id":
            return hasattr(self, "id")
        if name == "trainerid":
            return hasattr(self, "trainerid")
        else:
            return hasattr(self, name)

    def set_attribute(self, name, value):
        """
        sets attribute
        :param name: Name of the attribute
        :param value: Value of the attribute
        """
        if name == "id":
            self.species = value
        elif name == "trainerid":
            self.trainer = Trainer(value)

        else:
            setattr(self, name, value)

    @classmethod
    def create_new(cls, database, id: int, trainer: Trainer):
        """
        creates a new pokedex entry
        :param database: database to write in
        :param id: species id of the pokemon
        :param trainer: trainerobject
        :return: returns the new created pokedexentry
        """
        result = Pokedex(id, trainer)
        result.insert_new(database, 'id, trainerid')
        return result

    @classmethod
    def from_dic(cls, data):
        """gets data as dictionary"""
        return cls(int(data['id']), Trainer(data['trainerid']))
