import sys
from os.path import dirname, abspath
sys.path.append(dirname(abspath(__file__)) + "/../PokemonAdventure")

import MySQLdb
from sys import exit
from download_data import download_data
from create_tables import create_tables
import sys
import getopt
from export_data import export_to_database, export_to_file
from load_data import load_data
from private import database_passwd, database_user

def print_err(err):
    print(err, file = sys.stderr)
    exit()


def connect2host():
    try:
        db = MySQLdb.connect(host="localhost", user=database_user, passwd=database_passwd, charset='utf8')
    except MySQLdb.Error as err:
        print_err(err)
    else:
        cursor = db.cursor()
        return db, cursor


def createdb(cursor, database):
    try:
        cursor.execute("CREATE DATABASE %s" % database)
        cursor.execute("USE %s" % database)
    except MySQLdb.Error as err:
        if err.args[0] == 1007:
            try:
                cursor.execute("DROP DATABASE %s" % database)
                cursor.execute("CREATE DATABASE %s" % database)
                cursor.execute("USE %s" % database)
            except MySQLdb.Error as err:
                print_err(err)
        else:
            print_err(err)


def disconnect(db, cursor):
    cursor.close()
    db.close()


def parse_paramaters(argv):
    i_download = False
    i_local = False
    o_local = False
    o_database = False
    i_file = None
    o_file = None
    o_db_name = None
    inp = False
    outp = False
    help = 'downloader.py -i <download/local-raw/local> -o <local/database/all> [--if <inputfile> --of <outputfile>' \
           ' --db <database>]'
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["input=", "output=", "if=", "of=", "ifile=", "ofile=", "db=",
                                                   "database="])
    except getopt.GetoptError:
        print(help)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(help)
            sys.exit()
        elif opt in ("-i", "--input"):
            if inp:
                print(help)
                sys.exit()
            else:
                if arg == "download":
                    i_download = True
                elif arg == "local":
                    i_local = True
                else:
                    print(help)
                    sys.exit()
            inp = True
        elif opt in ("-o", "--output"):
            if outp:
                print(help)
                sys.exit()
            else:
                if arg == "database":
                    o_database = True
                elif arg == "local":
                    o_local = True
                elif arg == "all":
                    o_database = True
                    o_local = True
                else:
                    print(help)
                    sys.exit()
            outp = True
        elif opt in ("--if", "--ifile"):
            i_file = arg
        elif opt in ("--of", "--ofile"):
            o_file = arg
        elif opt in ("--db", "--database"):
            o_db_name = arg
    if not(inp and outp) or (i_local and i_file is None) or (o_local and o_file is None) or\
            (o_database and o_db_name is None):
        print(help)
        sys.exit()

    return i_download, i_local, o_local, o_database, i_file, o_file, o_db_name


def main(argv):
    i_dl, i_loc, o_loc, o_db, i_file, o_file, o_db_name = parse_paramaters(argv)

    if i_dl:
        data = download_data()
    else:
        file = open(i_file, "r")
        data = load_data(file)
    if o_db:
        db, cursor = connect2host()
        createdb(cursor, o_db_name)
        create_tables(cursor)
        export_to_database(data, cursor)
        db.commit()
        disconnect(db, cursor)
    if o_loc and not i_loc:
        file = open(o_file, "w")
        export_to_file(data, file)


if __name__ == '__main__':
    main(sys.argv[1:])
