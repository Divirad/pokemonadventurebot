from telegram import InlineKeyboardButton, InlineKeyboardMarkup, TelegramError
from gamelogic.button_id import ButtonId as BI
from res import Stickerpacks
from database.db import get_database

class Item(object):
    def __init__(self, _id=None, _name=None, _price=None, _text=None, _discount=0, _effect=0):
        self.id = _id
        self.name = _name
        self.price = _price
        self.discount = _discount
        self.text = _text
        self.effect = _effect
        pass

    def LoadPotionFromD(self, id, db):
        self.LoadItemFromD(id + 5, db)

    def LoadBallsFromD(self, id, db):
        self.LoadItemFromD(id + 1, db)

    def LoadItemFromD(self, id, db):
        itemraw = db.get_data_1row("SELECT name, price, productdescription, discount, effect FROM shop WHERE id = %s",
                                   (id,))
        self.name = itemraw['name']
        self.price = itemraw['price']
        self.text = itemraw['productdescription']
        self.discount = itemraw['discount']
        self.effect = itemraw['effect']

def shopcb(bot, update):
    query = update.callback_query
    data = query.data
    cid = query.message.chat_id
    d = get_database()

    if data.find('shop') != -1:
        userinfo = d.get_data_1row("SELECT menu_id, pokedollar FROM trainer WHERE id = %s", (cid,))
        if userinfo['menu_id'] == 3:
            if data.find('balls') != -1:
                # TODO DID
                pass
            elif data.find('potions') != -1:
                pass

            elif data.find('exit') != -1:
                userinfo = d.get_data_1row("SELECT menu_id FROM trainer WHERE id = %s", (cid,))

                if userinfo['menu_id'] == 3:
                    try:
                        update.callback_query.message.delete()
                    except TelegramError:
                        bot.answerCallbackQuery(callback_query_id=update.callback_query.id,
                                                text="Don't click that fast...", show_alert=False)
                    shop_but = [[InlineKeyboardButton("Pokéballs", callback_data=BI.SHOP_GOTO_BALLS)], [
                        InlineKeyboardButton("Potions", callback_data=BI.SHOP_GOTO_POTIONS)]]
                    shop_keys = InlineKeyboardMarkup(shop_but)
                    bot.send_message(cid,
                                     text="""Hi there! May I help you? To exit the shop just send or click on \menu""",
                                     reply_markup=shop_keys)