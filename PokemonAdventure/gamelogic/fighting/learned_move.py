from database.DBIdObject import DBIdObject
from database import Data
from database.db import Database


class LearnedMove(DBIdObject):
    """
    A move learned by a pokemon synchronized with the database. It contains additional information for a move that is
    different between pokemon
    """
    table = "learned_move"

    def __init__(self, id):
        DBIdObject.__init__(self, id)

    @classmethod
    def create_new(cls, database: Database, move: Data.Move) -> 'LearnedMove':
        """
        Creates a new object of LearnedMove that will be inserted into the database

        :param database: pokemon database
        :param move: the referenced move
        :return: the new LearnedMove object
        """
        result = LearnedMove(None)
        result.move = move
        result.blocked = False
        result.blockedforrounds = 0
        result.currentap = move.pp
        result.id = result.insert_new(database, "move_id, currentap, blocked, blockedforrounds")
        return result

    def get_attribute(self, name):
        if name == "move_id":
            return self.move.id if self.move is not None else None
        else:
            return getattr(self, name)

    def has_attribute(self, name):
        if name == "move_id":
            return hasattr(self, "move")
        else:
            return hasattr(self, name)

    # noinspection PyAttributeOutsideInit
    def set_attribute(self, name, value):
        if name == "move_id":
            self.move = Data.all_moves[value] if value is not None else None
        else:
            setattr(self, name, value)
