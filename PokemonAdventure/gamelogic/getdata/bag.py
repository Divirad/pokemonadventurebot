from database.DBIdObject import DBIdObject

class Bag(DBIdObject):
    """
    Super cool Wrapper to get Data from the MySQL-database
    """

    table = "bag"

    def __init__(self, id):
        DBIdObject.__init__(self, id)

    @classmethod
    def create_new(cls):
        pass
