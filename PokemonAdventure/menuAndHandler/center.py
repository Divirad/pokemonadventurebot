import datetime as dt

from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, TelegramError

# from database.db import get_database, free_database
from gamelogic.getdata.pokemon import Pokemon
from gamelogic.getdata.trainer import Trainer
from res import Stickerpacks
from database import Data

def com(bot, update):
    """
    if menu_id==3:
    Ask the player if the trainer wants to heal his Pokemonteam and prints the time the pokemon need to heal.
    Gets id and teamnr from database.
    Yes = menu_id -> 11

    :param bot: bot-param
    :param update: update-param
    :return: nothing
    """
    d = get_database()
    try:
        id = update.message.from_user.id
        trainer = Trainer(id)
        trainer.load_values(d, "menu_id")
        if trainer.menu_id == 3:
            center_buttons = [[InlineKeyboardButton("Heal, please!", callback_data='heal_y'),
                               InlineKeyboardButton("Nope.", callback_data='heal_n')]]

            center_keys = InlineKeyboardMarkup(center_buttons)
            bot.send_message(id, """B E E P  b o O o p  B e E P...""")
            bot.send_message(id, """.  .  .""")
            bot.send_message(id, """W E L C O M E!""")
            box_buttons = [
                [InlineKeyboardButton("Open Box", callback_data='center_box')],
                [InlineKeyboardButton("Phone with Oak", callback_data='center_oak')],]
            box_keys = InlineKeyboardMarkup(box_buttons)
            bot.send_message(id, """C O M P U T E R   M E N U""", reply_markup = box_keys)
            pass

    finally:
        free_database(d)

def comcb(bot, update):
    d = get_database()
    try:
        query = update.callback_query
        data = query.data
        cid = query.from_user.id
        if data.find('box') != -1:
            result = "B O X \n====================\n"
            trainer = Trainer(cid)
            #trainer.load_values(d, "id")
            pokes = trainer.get_all_pkmn(d, "id, name, level, currenthp, gender, hp_exp, hp_dv, species_id, current_status") #all_pkmn
            id = 1
            if pokes==[]:
                result+="Nothing here...\n"
            for poke in pokes:#[startval:startval+19]:
                #poke.load_values(d, "name, level, currenthp, gender, hp_exp, hp_dv, species_id, current_status")
                result += """ ({0}) {1} [{5}] Lv. {2} \n    HP: {3}/{4}\n""".format(id, poke.name, poke.level,
                                                                                         poke.currenthp,
                                                                                         poke.calculate_max_hp(),
                                                                                         poke.gender)
                id += 1
            result+="""====================\n
/binfo <boxnumber> 
  to get more information 
  about your Pokémon
  in the box
/tinfo <boxnumber> 
  to get more information 
  about your Pokémon
  in tyour team
/box2team <box id>
  move a pokemon from 
  your box to your team
/team2box <team idr>
  move a pokemon from 
  your team to your box
/change <from> <to>
  change the team id 
  of your Pokémon
/release <box id>
  release a pokemon
/trade <box id> <user id>
  trade pokemon"""
            bot.send_message(cid, result)
    finally:
        free_database(d)

def binfo(bot, update):
    """

    :param bot:
    :param update:
    :return:
    """
    d = get_database()
    try:
        data =  update.message.text
        id = update.message.from_user.id
        trainer = Trainer(id)
        trainer.load_values(d, "menu_id")
        print(data[7:])
        if trainer.menu_id == 3:
            pokes = trainer.get_all_pkmn(d, "id, name, level, currenthp, gender, hp_exp, hp_dv, species_id, current_status")
            show_poke_info(bot, id, data, pokes)
    finally:
        free_database(d)

def tinfo(bot, update):
    """

        :param bot:
        :param update:
        :return:
        """
    d = get_database()
    try:
        data = update.message.text
        id = update.message.from_user.id
        trainer = Trainer(id)
        trainer.load_values(d, "menu_id")
        if trainer.menu_id == 3:
            pokes = trainer.get_team(d, "id, name, level, currenthp, gender, hp_exp, hp_dv, species_id, current_status")
            show_poke_info(bot, id, data, pokes)
    finally:
        free_database(d)

def show_poke_info(bot, id, data, pokes):
    """
    Shows pokemon info Sticker + Message
    :param bot: botstuff
    :param id: trainer id
    :param data: text
    :param pokes: list of pokemon
    """
    try:
        pid = int(data[7:])
        poke = pokes[pid - 1]
        calc_attack = 0
        calc_defense = 0
        calc_speed = 0
        calc_spec = 0
        data = Data.all_species[poke.species.id]
        t1 = "-"
        t2 = "-"
        if data.type1 != None:
            t1 = data.type1.name
        if data.type2 != None:
            t2 = data.type2.name

        pokesticker = Stickerpacks.get_pokemon(poke.species.id)
        result = "*NAME:* " + poke.name + ", *LEVEL:* " + str(poke.level) + "\n" + \
                 "*No.:* " + "[%03d] " % poke.species.id + ", *HP:* " + str(poke.currenthp) + "/" + str(
            poke.calculate_max_hp()) + "\n" + \
                 "*STATUS:* " + str(poke.current_status) + "\n" + \
                 "*TYPE 1:* " + t1 + ", *TYPE 2:* " + t2 + "\n" + \
                 "*ATTACK:* " + str(calc_attack) + ", *DEFENSE:* " + str(calc_defense) + "\n" + \
                 "*SPECIAL:* " + str(calc_spec) + "\n*ID:* " + str(poke.id)
        bot.send_sticker(id, pokesticker)
        bot.send_message(id, result, ParseMode.MARKDOWN)
    except:
        bot.send_message(id, "Nope... Something went wrong.")