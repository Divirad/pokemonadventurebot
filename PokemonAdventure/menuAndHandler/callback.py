import logging

from Database.db import get_database, free_database
from menuAndHandler import center
from menuAndHandler.choosestarter import choosestarter, renamestarter
from menuAndHandler.dexter import dexcb
from menuAndHandler.shop import shopcb
from gamelogic.fighting.battle import battle_cb
from gamelogic.getdata.trainer import Trainer

logger = logging.getLogger(__name__)

def textcb(bot, update):
    # Get Data
    d = get_database()
    try:
        cid = update.message.from_user.id
        trainer = Trainer(cid)
        trainer.get_values(d, "id, menu_id")

        if trainer.menu_id == 2:
            renamestarter(bot, update, d, trainer)
    finally:
        free_database(d)


def cb(bot, update):
    data = update.callback_query.data
    if data[0] == 'F':
        battle_cb(bot, update, data)

    elif data[0] == 'S':
        choosestarter(bot, update)

    elif data.find("heal") != -1 or data.find("pickuppkmn") != -1:
        center.healcb(bot, update)

    elif data.find("box") != -1:
        center.comcb(bot, update)
    # elif data.find("loc") !=-1:
    # Walk.walkcb(bot, update)
    elif data[0] != 'X':
        shopcb(bot, update)
        dexcb(bot, update)

    update.callback_query.answer()


def replacestr(text, list):
    res = text
    for l in list:
        tempres = res.replace(l, "")
        res = tempres
    return res
