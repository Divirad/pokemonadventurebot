from database.DBObject import DBObject


class DBIdObject(DBObject):
    def __init__(self, id):
        self.id = id

    def identificator(self):
        return "id = %s" % self.id

    @classmethod
    def from_dic(cls, data):
        return cls(data['id'])

    def insert_new(self, database, names):
        DBObject.insert_new(self, database, names)
        return database.last_id()
