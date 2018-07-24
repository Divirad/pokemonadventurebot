from datetime import datetime
from database.DBIdObject import DBIdObject
from gamelogic.getdata import pokemon
from gamelogic.fighting import fight
from gamelogic.math import Vector2d

class Trainer(DBIdObject):
    table = "trainer"
    name: str
    menu_id: int
    pokedollar: int
    badges: int
    wins: int
    looses: int
    draws: int
    game_pos_x: int
    game_pos_y: int
    game_location_id: int

    def __init__(self, id):
        DBIdObject.__init__(self, id)

    @classmethod
    def create_new(cls, database, id, name, pokedollar):
        result = Trainer(id)
        result.name = name
        result.pokedollar = pokedollar
        result.registeredsince = datetime.today()
        result.insert_new(database, "id, name, pokedollar, registeredsince")
        return result

# not tested
    def catch_pokemon(self, database, pokemon):
        """

        :param database:
        :param pokemon:
        :return: inserted pokemon
        """
        pokeraw = self.get_team(database, "teamnr")  # blocktimer
        row_count = len(pokeraw)
        if row_count < 6:
            pokemon.teamnr = row_count+1
        else:
            pokemon.teamnr = 0

        pokemon.ownedby = self.id
        pokemon.update_values(database, "ownedby, teamnr")
        return pokemon

    def get_team(self, database, columns):
        """
        returns a list with all 6 pkmn in the team
        :param database: database where you want to load from
        :param columns: Values to load
        :return: a list of all pokemon in the team of a trainer
        """
        return pokemon.Pokemon.get_all(database, columns, "teamnr > 0 AND ownedby = %d" % self.id, "teamnr")

    def get_all_pkmn(self, database, columns):
        """
        returns a list with all
        :param database: database where you want to load from
        :param columns: Values to load
        :return: a list of all pokemon of a trainer"""
        return pokemon.Pokemon.get_all(database, columns, "teamnr = 0 AND ownedby = %d" % self.id, "id")

    def get_coords(self) -> Vector2d:
        return Vector2d(self.game_pos_x, self.game_pos_y)

    def get_location( self ):
        return self.game_map_id

    def get_attribute(self, name):
        if name == "fight":
            return self.fight.id if self.fight is not None else None
        else:
            return getattr(self, name)

    def get_menu_id(self):
        return self.menu_id

    # noinspection PyAttributeOutsideInit
    def set_attribute(self, name, value):
        if name == "fight":
            self.fight = fight.Fight(value)
        else:
            setattr(self, name, value)
