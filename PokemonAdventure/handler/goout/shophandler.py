from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot, Update

from errorhandling.errorhandling import delete_message, not_implemented_yet
from gamelogic.button_id import ButtonId
from gamelogic.getdata.trainer import Trainer
from gamelogic.menu_id import MenuId
from telegram_utilities.handler import Handler
from telegram_utilities.registry import Registry
from typing import List
from database.db import Database

from res import Stickerpacks

class ShopHandler(Handler):

    class ShopItem(object):
        def __init__(self, _id = None, _name = None, _price = None, _text = None, _discount = 0, _effect = 0):
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
            itemraw = db.get_data_1row(
                "SELECT name, price, productdescription, discount, effect FROM shop WHERE id = %s",
                (id,))
            self.name = itemraw['name']
            self.price = itemraw['price']
            self.text = itemraw['productdescription']
            self.discount = itemraw['discount']
            self.effect = itemraw['effect']

    def get_sub_handler(self) -> List['Handler']:
        return []

    def register(self, registry: Registry):
        registry.add_button_handler(ButtonId.GOOUT_SHOP, not_implemented_yet, [MenuId.MAIN_MENU])
        # registry.add_button_handler(ButtonId.GOOUT_SHOP, self.shopmenu, [MenuId.MAIN_MENU])

        registry.add_button_handler(ButtonId.SHOP_BALLS, self.balls, [MenuId.MAIN_MENU])
        registry.add_button_handler(ButtonId.SHOP_POTIONS, self.potions, [MenuId.MAIN_MENU])
        pass

    def shopmenu(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        delete_message(bot, update)
        shop_but = [[InlineKeyboardButton("Pokéball", callback_data = str(ButtonId.SHOP_BALLS))],
                    [InlineKeyboardButton("Potions", callback_data = str(ButtonId.SHOP_POTIONS))],
                    [InlineKeyboardButton("⏪ Go Out", callback_data = str(ButtonId.MENU_GOOUT))]]
        shop_keys = InlineKeyboardMarkup(shop_but)
        bot.send_message(trainer.id, text = "Hi there! May I help you?",
                         reply_markup = shop_keys)

    def balls(self, bot: Bot, update: Update, trainer: Trainer, database: Database):

        trainer.load_values(database, "pokedollar")

        data = update.callback_query.data.replace(str(ButtonId.SHOP_BALLS), "")
        delete_message(bot, update)

        num = self.num_calc(3,data)

        item = self.ShopItem()
        item.LoadBallsFromD(num, database)

        bot.sendSticker(trainer.id, Stickerpacks.get_balls(num),
                        reply_markup =
                        self.create_buttons(item,
                                            str(ButtonId.SHOP_BALLS_MIN),
                                            str(ButtonId.SHOP_BALLS_PLS),
                                            str(ButtonId.SHOP_BALLS_BUY),
                                            num,
                                            trainer.pokedollar)) #num, userinfo['pokedollar'], "balls"))

    def potions(self, bot: Bot, update: Update, trainer: Trainer, database: Database):


        trainer.load_values(database, "pokedollar")

        data = update.callback_query.data.replace(str(ButtonId.SHOP_POTIONS), "")
        delete_message(bot, update)

        num = self.num_calc(4,data)

        item = self.ShopItem()
        item.LoadPotionFromD(num, database)
        bot.sendSticker(trainer.id, Stickerpacks.get_potions(num),
                        reply_markup =
                        self.create_buttons(item,
                                            str(ButtonId.SHOP_POTIONS_MIN),
                                            str(ButtonId.SHOP_POTIONS_PLS),
                                            str(ButtonId.SHOP_POTIONS_BUY),
                                            num,
                                            trainer.pokedollar))

    def num_calc(self, max, data):
        num = None
        if data.find("min") != -1:
            num = int(data.replace("min", ""))
            num = num - 1
            if num < 0:
                num = max
        elif data.find("pls") != -1:
            num = int(data.replace("pls", ""))
            num = num + 1
            if num > 4:
                num = max
        else:
            num = 0
        return num

    def create_buttons(self, item: ShopItem, buttonid_min, buttonid_pls, buttonid_shop, num, pokedollar):

        shop_but = [[InlineKeyboardButton( str(item.text), callback_data = str(ButtonId.NONE))],
                    [InlineKeyboardButton("Price: %d₱" % (item.price - item.discount), callback_data = str(ButtonId.NONE)),
                     InlineKeyboardButton("Your ₱s': %d₱" % int(pokedollar), callback_data = str(ButtonId.NONE))],
                    [InlineKeyboardButton("""◀️""", callback_data = str(buttonid_min) + str(num)),
                     InlineKeyboardButton("""▶️""", callback_data = str(buttonid_pls) + str(num))],
                    [InlineKeyboardButton("[ BUY ]", callback_data = str(buttonid_shop)),
                     InlineKeyboardButton("⏪ EXIT", callback_data = str(ButtonId.GOOUT_SHOP))]]
        shop_keys = InlineKeyboardMarkup(shop_but)
        return shop_keys