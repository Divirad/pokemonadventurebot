class DBObject(object):

    def identificator(self):
        raise NotImplementedError("Identificator of %s not implemented" % type(self))

    @classmethod
    def from_dic(cls, data):
        raise NotImplementedError("from_data of %s not implemented" % cls)

    def load_values(self, database, values):
        data = database.select_sorted(values, type(self).table, self.identificator())[0]
        for d in data:
            self.set_attribute(d, data[d])

            # Load values if attribute is non-existing

    def get_values(self, database, values):
        splitted = values.split(", ")
        real_values = []
        for s in splitted:
            if not self.has_attribute(s):
                real_values.append(s)
        self.load_values(database, ", ".join(real_values))

    def does_exist(self, database):
        return database.test_exist(type(self).table, self.identificator())

    def update_values(self, database, names):
        splitted = names.split(", ")
        values = []
        for n in splitted:
            values.append(self.get_attribute(n))

        database.update_values(type(self).table, names, values, self.identificator())

    def insert_new(self, database, names):
        splitted = names.split(", ")
        values = []
        for n in splitted:
            values.append(self.get_attribute(n))

        database.insert(type(self).table, names, values)

    def get_attribute(self, name):
        return getattr(self, name)

    def has_attribute(self, name):
        return hasattr(self, name)

    def set_attribute(self, name, value):
        setattr(self, name, value)

    @classmethod
    def get_all(cls, database, columns, where=None, order=None):
        data = database.select_sorted(columns, cls.table, where, order)
        result = []
        for d in data:
            obj = cls.from_dic( d)
            for name in d:
                obj.set_attribute(name, d[name])
            result.append(obj)
        return result
