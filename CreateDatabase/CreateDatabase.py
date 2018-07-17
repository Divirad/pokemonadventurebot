
import MySQLdb
from CreateTables import create_tables
import FillTables
from private import database_passwd, database_user

def main():
	db = MySQLdb.connect(host = "localhost", user = database_user, passwd = database_passwd)
	cursor = db.cursor()
	cursor.execute("DROP DATABASE Pokemon")
	cursor.execute("CREATE DATABASE Pokemon")
	cursor.execute("USE Pokemon")
	create_tables(cursor)

	FillTables(cursor)

if __name__ == '__main__':
	main()