import os
from sys import platform


def printmenu1(isconnected, activedb, db, message):
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        os.system('clear')  
    elif platform == "win32":
        os.system('cls') 
    print("""
###########################################
#   PokemonAdventureBot Databasemanager   #
###########################################
    Is Host Con: %s | Is DB. Con.: %s
    Connected to: %s
    [1] - Connect to Local Host
    [2] - Connect to database
    [3] - Create Pokemon database
    [4] - Create Trainer
    [5] - Give  trainer an item
    [6] - Give  trainer a pokemon
    [7] - Get Data from Table
    [8] - Disconnect
    [cmd] - SQL-CMD manually
    [exit] - Exit



    %s""" % (isconnected, activedb, db, ("" if message is None else message)))