import sys
from os.path import dirname, abspath
sys.path.append(dirname(abspath(__file__)) + "/../Downloader")
sys.path.append(dirname(abspath(__file__)) + "/../PokemonAdventure")

import MySQLdb
from CreateTables import create_tables
from FillTables import fill_tables
import manager_menu
from datetime import date
import random
from math import floor, sqrt
from requests.exceptions import Timeout
from sys import exit
import downloader
from private import database_passwd, database_user

global db, cursor, isconnected, isdbactive, activedb

def connect2host():
    global db, cursor, isconnected
    try:
        db = MySQLdb.connect(host="localhost", user=database_user, passwd=database_passwd, charset='utf8')
    except MySQLdb.Error as err:
        return err.args[1]
    else:
        cursor = db.cursor()
        isconnected = True
        return "Connected to host"


def connect2db():
    global db, cursor, isconnected, isdbactive, activedb
    if isconnected:
        try:
            cursor.execute('USE Pokemon')
        except MySQLdb.Error as err:
            return err.args[1]
        else:
            activedb = 'Pokemon'
            isdbactive = True
            return "Connected to the database"
    else:
        try:
            db = MySQLdb.connect(host="localhost", user=database_user, passwd=database_passwd, database="Pokemon", charset='utf8')
        except MySQLdb.Error as err:
            return err.args[1]
        else:
            cursor = db.cursor()
            isconnected = True
            activedb = 'Pokemon'
            isdbactive = True
            return "Connected to host and the database"


def createdb():
    global cursor, isconnected
    if not isconnected:
        return "You need to connect with a database first!"
    else:
        try:
            downloader.main(['-i', 'local', '-o', 'database', '--if', 'pokemon_data.json', '--db', 'pokemon'])
            cursor.execute("USE pokemon")
        except MySQLdb.Error as err:
            return err.args[1]
        try: #fill database
            create_tables(cursor)
            fill_tables(cursor)
            db.commit()
        except MySQLdb.Error as err:
            return err.args[1]
        except Timeout as err:
            return err.args[0]
        else:
            return "Created DB succesfull new"


def give_trainer_item():
    inp = input('<<[ItemID] [TrainerID]\nInput>>')


def give_trainer_pokemon():
    if not isconnected:
        return "You need to connect with a database first!"
    else:
        if not isdbactive:
            return "You need to select a database first!"
        else:
            id = int(input('Pokedex id: '))
            trainer = int(input('Trainer id: '))
            name = input('Name: ')
            level = max(1, int(input('Level: ')))
            gender = input('Gender: ')[0]
            if gender != 'f' and gender != 'm' and gender != 'n':
                gender = 'n'

            if input("Custom Dv's: ").lower() == "y":
                attack_dv = min(15, max(0, int(input("Attack DV: "))))
                defense_dv = min(15, max(0, int(input("Defense DV: "))))
                special_dv = min(15, max(0, int(input("Special DV: "))))
                speed_dv = min(15, max(0, int(input("Speed DV: "))))
            else:
                attack_dv = random.randint(0, 15)
                defense_dv = random.randint(0, 15)
                special_dv = random.randint(0, 15)
                speed_dv = random.randint(0, 15)

            if input("Custom Ev's: ").lower() == "y":
                hp_ev = min(65535, max(0, int(input("HP EV: "))))
                attack_ev = min(65535, max(0, int(input("Attack EV: "))))
                defense_ev = min(65535, max(0, int(input("Defense EV: "))))
                special_ev = min(65535, max(0, int(input("Special EV: "))))
                speed_ev = min(65535, max(0, int(input("Speed EV: "))))
            else:
                hp_ev = 0
                attack_ev = 0
                defense_ev = 0
                special_ev = 0
                speed_ev = 0

            hp_dv = 0
            if attack_dv % 2 == 0:
                hp_dv += 8
            if defense_dv % 2 == 0:
                hp_dv += 4
            if special_dv % 2 == 0:
                hp_dv += 2
            if speed_dv % 2 == 0:
                hp_dv += 1

            global cursor
            try:
                cursor.execute("SELECT hp_base FROM pokespecies WHERE id = %s", (str(id)))
                hp_base = cursor.fetchall()[0][0]
            except MySQLdb.Error as err:
                return err.args[1]

            currenthp = int(floor(((((hp_base + hp_dv) * 2) + floor(sqrt(hp_ev)/4)) * level) / 100) + level + 10)

            try:
                cursor.execute("""INSERT INTO pokemon 
                    (ownedby, originaltrainer, species_id, name, teamnr, currenthp, currentstats, level, hp_ev, attack_ev,
                   defense_ev, special_ev, speed_ev, hp_dv, attack_dv, defense_dv, special_dv, speed_dv, gender) VALUES
                  (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (trainer, trainer, id, name, 0, currenthp, "", level, hp_ev, attack_ev, defense_ev, special_ev, speed_ev,
                    hp_dv, attack_dv, defense_dv, special_dv, speed_dv, gender))
                db.commit()
            except MySQLdb.Error as err:
                return err.args[1]
            else:
                return "Created new pokemon"


def get_data():
    inp = input('<<From what Primarykey\nInput>>')


def create_trainer():
    if not isconnected:
        return "You need to connect with a database first!"
    else:
        if not isdbactive:
            return "You need to select a database first!"
        else:
            id = input("Id: ")
            name = input("Name: ")

            try:
                global cursor
                cursor.execute("INSERT INTO trainer (id, name, registeredsince) VALUES (%s, %s, %s)",
                    (id, name, date.today()))
                db.commit()
            except MySQLdb.Error as err:
                return err.args[1]
            else:
                return "Created new trainer"


def disconnect():
    global db, cursor, isconnected, isdbactive, activedb
    if isconnected:
        cursor.close()
        db.close()
        isconnected = False
        isdbactive = False
        activedb = ""
        cursor = None
        db = None
        return "Disconnected from database"
    else:
        return "You are not connected"


def main():
    global db, cursor, isconnected, isdbactive, activedb
    isconnected = False
    isdbactive = False
    activedb = 'NONE'
    message = ""
    while True:
        manager_menu.printmenu1(str(isconnected), str(isdbactive), activedb, message)
        inp = input('Input>>')
        if inp == '1':
            message = connect2host()
        elif inp == '2':
            message = connect2db()
        elif inp == '3':
            message = createdb()
        elif inp == '4':
            message = create_trainer()
        elif inp == '5':
            message = give_trainer_item()
        elif inp == '6':
            message = give_trainer_pokemon()
        elif inp == '7':
            message = get_data()
        elif inp == '8':
            message = disconnect()
        elif inp == 'cmd':
            inp = input('Input>>')
            cursor.execute(inp)
        elif inp == 'exit':
            exit(0)


if __name__ == '__main__':
    main()
