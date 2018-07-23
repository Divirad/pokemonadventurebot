from threading import Lock

import MySQLdb

from AtomicInteger import AtomicInteger
from deprecated_decorator import deprecated
from private import database_passwd, database_user


class Database(object):
    __mutex = Lock()
    __databases = []
    __database_count = AtomicInteger()

    def __init__(self):
        self.db = None
        self.cursor = None
        self.dict_cursor = None
        # self.execute("USE " + database)

    def __enter__(self):
        with Database.__mutex:
            if Database.__databases:
                db = Database.__databases.pop()
                db.__move(self)
            else:
                self.__open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with Database.__mutex:
            db = Database()
            self.__move(db)
            Database.__databases.append(db)

    def __open(self):
        self.db = MySQLdb.connect("localhost", user=database_user, passwd=database_passwd, db="pokemon")
        self.cursor = self.db.cursor()
        self.dict_cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        Database.__database_count.inc()

    def __close(self):
        self.cursor.close()
        self.dict_cursor.close()
        self.db.close()
        self.db = None
        self.cursor = None
        self.dict_cursor = None
        Database.__database_count.dec()

    def __move(self, new: 'Database'):
        new.db = self.db
        new.cursor = self.cursor
        new.dict_cursor = self.dict_cursor
        self.db = None
        self.cursor = None
        self.dict_cursor = None

    @classmethod
    def close_all(cls):
        with cls.__mutex:
            if cls.__database_count.value != len(cls.__databases):
                raise ValueError("While trying to close database connections: still databases in use")
        cls.close_unused()

    @classmethod
    def close_unused(cls):
        with cls.__mutex:
            while cls.__databases:
                cls.__databases.pop().__close()

    @classmethod
    def get_count(cls) -> (int, int, int):
        """
        Gets the count of the current database connections

        :return: (total count, count of currently used, count of currently unused)
        """
        return cls.__database_count.value, cls.__database_count.value - len(cls.__databases), len(cls.__databases)

    def execute(self, query, args=()):
        try:
            self.cursor.execute(query, args)
        except MySQLdb.OperationalError:
            self.__close()
            self.__open()
            raise

    def dict_execute(self, query, args=()):
        try:
            self.dict_cursor.execute(query, args)
        except MySQLdb.OperationalError:
            self.__close()
            self.__open()
            raise

    def cmd(self, c, p=None):
        if p is None:
            self.execute(c)
        else:
            self.execute(c, p)
        self.db.commit()

    def get_data(self, c, p=None):
        if p is None:
            self.execute(c)
        else:
            self.execute(c, p)
        s = self.cursor.fetchall()
        return s

    def get_data_sorted(self, c, p=None):
        if p is None:
            self.dict_execute(c)
        else:
            self.dict_execute(c, p)
        s = self.dict_cursor.fetchall()
        return s

    @deprecated
    def get_data_1row(self, c, p=None):
        if p is None:
            self.dict_execute(c)
        else:
            self.dict_execute(c, p)
        s = self.dict_cursor.fetchall()
        if len(s) != 1:
            raise RuntimeError("Mysql fetch one returned %d entries" % len(s))
        return s[0]

    def update(self, table, values, where=None):
        if where is None:
            self.execute("UPDATE %s SET %s" % (table, values))
        else:
            self.execute("UPDATE %s SET %s WHERE %s" % (table, values, where))
        self.db.commit()

    def update_values(self, table, columns, values, where=None):
        column_text = ""
        splitted_columns = columns.split(", ")
        for c in splitted_columns:
            column_text += c + " = %s,"
        if where is None:
            self.execute("UPDATE %s SET %s" % (table, column_text[:-1]), values)
        else:
            self.execute("UPDATE %s SET %s WHERE %s" % (table, column_text[:-1], where), values)
        self.db.commit()

    def update_one(self, table, column, value, where=None):
        if where is None:
            self.execute("UPDATE %s SET %s = %s" % (table, column, value))
        else:
            self.execute("UPDATE %s SET %s = %s WHERE %s" % (table, column, value, where))
        self.db.commit()

    def insert(self, table, columns, values):
        self.execute("INSERT INTO %s (%s) VALUES (%s)" % (table, columns, ("%s," * len(values))[:-1]), values)
        self.db.commit()

    def select(self, columns, table, where=None, order=None):
        if where is None:
            if order is None:
                return self.get_data("SELECT %s FROM %s" % (columns, table))
            else:
                return self.get_data("SELECT %s FROM %s ORDER BY %s" % (columns, table, order))
        else:
            if order is None:
                return self.get_data("SELECT %s FROM %s WHERE %s" % (columns, table, where))
            else:
                return self.get_data("SELECT %s FROM %s WHERE %s ORDER BY %s" % (columns, table, where, order))

    def select_sorted(self, columns, table, where=None, order=None):
        if where is None:
            if order is None:
                return self.get_data_sorted("SELECT %s FROM %s" % (columns, table))
            else:
                return self.get_data_sorted("SELECT %s FROM %s ORDER BY %s" % (columns, table, order))
        else:
            if order is None:
                return self.get_data_sorted("SELECT %s FROM %s WHERE %s" % (columns, table, where))
            else:
                return self.get_data_sorted("SELECT %s FROM %s WHERE %s ORDER BY %s" % (columns, table, where, order))

    def select_all(self, table, where=None, order=None):
        if where is None:
            if order is None:
                return self.get_data_sorted("SELECT * FROM %s" % (table,))
            else:
                return self.get_data_sorted("SELECT * FROM %s ORDER BY %s" % (table, order))
        else:
            if order is None:
                return self.get_data_sorted("SELECT * FROM %s WHERE %s" % (table, where))
            else:
                return self.get_data_sorted("SELECT * FROM %s WHERE %s ORDER BY %s" % (table, where, order))

    def test_exist(self, table, where):
        return self.get_data("SELECT EXISTS(SELECT NULL FROM %s WHERE %s)" % (table, where))[0][0]

    def last_id(self):
        return self.get_data("SELECT LAST_INSERT_ID()")[0]
