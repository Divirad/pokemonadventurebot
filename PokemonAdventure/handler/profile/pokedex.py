from gamelogic.button_id import ButtonId
from gamelogic.menu_id import MenuId
from gamelogic.getdata.trainer import Trainer

from errorhandling.errorhandling import delete_message

from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, TelegramError
from telegram_utilities.handler import Handler
from telegram_utilities.registry import Registry
from typing import List

from gamelogic.getdata.pokedex import Pokedex

from database.db import Database
from database import Data
from res import Stickerpacks


class PokedexHandler(Handler):

    def get_sub_handler(self) -> List['Handler']:
        return []

    def register(self, registry: Registry):

        registry.add_button_handler(ButtonId.PROFILE_POKEDEX, self.pokedex, [MenuId.MAIN_MENU])

        registry.add_button_handler(ButtonId.POKEDEX_FLIP, self.flip_charts, [MenuId.MAIN_MENU])
        registry.add_button_handler(ButtonId.POKEDEX_PAGES, self.pages, [MenuId.MAIN_MENU])

        registry.add_button_handler(ButtonId.POKEDEX_SWITCH_PAGE, self.switch_pages, [MenuId.MAIN_MENU])
        registry.add_button_handler(ButtonId.POKEDEX_MOREINFO, self.more_info, [MenuId.MAIN_MENU, MenuId.POKEDEX_SEARCH])

        registry.add_button_handler(ButtonId.POKEDEX_SEARCH, self.search, [MenuId.MAIN_MENU])

        registry.add_message_handler(self.search_for, [MenuId.POKEDEX_SEARCH])
        registry.add_button_handler(ButtonId.POKEDEX_EXIT_SEARCH, self.exit_search, [MenuId.POKEDEX_SEARCH])

    def exit_search(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        trainer.menu_id = int(MenuId.MAIN_MENU)
        trainer.update_values(database, "menu_id")
        self.send_menu(bot, trainer)


    def pokedex(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        delete_message(bot, update)
        self.send_menu(bot, trainer)

    def flip_charts(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        delete_message(bot, update)
        self.dexentry(database,bot, update,trainer.id, 1)

    def switch_pages(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        # ButtonId.POKEDEX_PAGES
        # delete_message(bot, update)
        temp = update.callback_query.data
        data = temp.replace(str(ButtonId.SWITCH_TO_STARTER), "")

        # if data.find('pls') != -1:
        if data.find('pls') != -1:
            #dexnum = int(data[8:])
            dexnum = int(temp.replace(str(ButtonId.POKEDEX_PLS), ""))
            total = dexnum + 1
            if total >= 152:
                total = 1
            delete_message(bot, update)
            self.dexentry(database, bot, update, trainer.id, total)

        elif data.find('min') != -1:
            dexnum = int(temp.replace(str(ButtonId.POKEDEX_MIN), ""))
            total = dexnum - 1
            if total <= 0:
                total = 151
            delete_message(bot, update)
            self.dexentry(database, bot, update, trainer.id, total)

    def more_info(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        dexnum = int(update.callback_query.data.replace(str(ButtonId.POKEDEX_MOREINFO), ""))

        # TODO optimize code
        dexterraw = Pokedex.get_all(database,
                                    columns = "id, trainerid",
                                    where = "id = " + str(dexnum),
                                    order = "id")
        rows = len(dexterraw)
        if rows != 0:
            data = Data.all_species[dexnum-1]
        if rows != 0:
            if data.type1 is not None:
                type1 = data.type1.name
            else:
                type1 = " - "
            if data.type2 is not None:
                type2 = data.type2.name
            else:
                type2 = " - "
            name = data.name
            text = data.pokedextext
        else:
            type1 = '???'
            type2 = '???'
            name = '???'
            text = '???'
        bot.answerCallbackQuery(callback_query_id = update.callback_query.id,
                                text = "Name: %s \nType 1: %s Type 2: %s\n%s" %
                                       (name, type1, type2, text), parse_mode = ParseMode.MARKDOWN, show_alert = True)

    def pages(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        """Sends Pokedex Entries as Pages to User"""

        data = update.callback_query.data
        num = int(data.replace(str(ButtonId.POKEDEX_PAGES), ""))
        result = ""
        if num == 1:
            result = self.getallentries(database, trainer.id, 1, 30)
        elif num == 31:
            result = self.getallentries(database, trainer.id, 31, 60)
        elif num == 61:
            result = self.getallentries(database, trainer.id, 61, 90)
        elif num == 91:
            result = self.getallentries(database, trainer.id, 91, 120)
        elif num == 121:
            result = self.getallentries(database, trainer.id, 121, 151)

        dex_but = [[InlineKeyboardButton("1-30", callback_data = str(ButtonId.POKEDEX_PAGES)+"1"),
                    InlineKeyboardButton("31-60", callback_data = str(ButtonId.POKEDEX_PAGES)+"31")],
                   [InlineKeyboardButton("61-90", callback_data = str(ButtonId.POKEDEX_PAGES)+"61"),
                    InlineKeyboardButton("91-120", callback_data = str(ButtonId.POKEDEX_PAGES)+"91")],
                   [InlineKeyboardButton("121-151", callback_data = str(ButtonId.POKEDEX_PAGES)+"121")],
                   [InlineKeyboardButton("⏪ Pokedex", callback_data = str(ButtonId.PROFILE_POKEDEX))]]
        dex_keys = InlineKeyboardMarkup(dex_but)

        try:
            bot.edit_message_text(text = result,
                                  chat_id = update.callback_query.message.chat_id,
                                  message_id = update.callback_query.message.message_id,
                                  reply_markup = dex_keys)
        except TelegramError:
            bot.answerCallbackQuery(callback_query_id = update.callback_query.id,
                                    text = "You are already here...",
                                    show_alert = False)
        pass

    def search(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        """sets earch MenuID and sends instructions"""
        delete_message(bot, update)

        dex_but = [[InlineKeyboardButton("⏪ Exit Search", callback_data = str(ButtonId.POKEDEX_EXIT_SEARCH))]]
        dex_keys = InlineKeyboardMarkup(dex_but)

        bot.send_message(trainer.id,
                         "Here you can search for a Pokemon-Species-ID or a Pokemon-Species-Name."
                         " So please send me a name or number from 1 to 151 now! Write "
                         " \"exit\"  to leave or click here: ", reply_markup = dex_keys)

        trainer.menu_id = int(MenuId.POKEDEX_SEARCH)
        trainer.update_values(database, "menu_id")

    def search_for(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        """searches for a pokemon"""
        input_data =  update.message.text

        # Exit Search
        if input_data.upper() == "EXIT":
            trainer.menu_id = int(MenuId.MAIN_MENU)
            trainer.update_values(database, "menu_id")
            self.send_menu(bot, trainer)

        # If Input is a number
        elif input_data.isdigit():
            dexnum = int(update.message.text)
            if dexnum > 151 or dexnum < 1:
                bot.send_message(trainer.id, "Invalid Dex number...")
            else:
                self.search_entry(database, bot, update, trainer.id, dexnum)

        # searches for a Name
        else:
            dexterraw = Pokedex.get_all(database,
                                        columns = "id, trainerid",
                                        where = "trainerid = " + str(trainer.id),
                                        order = "id")
            idar = {'null': None}

            for j in dexterraw:
                idar[Data.all_species[j.id - 1].name.upper()] = j.id
            input_dex = update.message.text.upper()

            keylist = []
            for k in idar.keys():
                keylist.append(str(k))

            if input_dex in keylist:
                self.search_entry(database, bot, update, trainer.id, idar[input_dex])
            else:
                bot.send_message(trainer.id,
                         "There is no entry with " +
                         input_dex +
                         " Do this Pokémon really exist? Check your spelling and try it one more time!")

    def search_entry(self, database, bot, update, id, dexnum):
        """Sends Pokemon-Sticker to user.  a Pokedex-entry"""
        dexterraw = Pokedex.get_all(database, columns = "id, trainerid",
                                    where = "id = " + str(dexnum) + " AND trainerid = " + str(id), order = "id")
        rows = len(dexterraw)

        if rows != 0:
            species = Data.all_species[dexnum-1]
            pokesticker = Stickerpacks.get_pokemon(dexnum)
            name = species.name
            if species.type1 is not None:
                type1 = species.type1.name
            else:
                type1 = " - "
            if species.type2 is not None:
                type2 = species.type2.name
            else:
                type2 = " - "

        else:
            pokesticker = Stickerpacks.get_item(9)
            name = '???'
            type1 = '???'
            type2 = '???'

        dex_but = [[InlineKeyboardButton("ID: %s" % dexnum, callback_data = str(ButtonId.NONE))],
                      [InlineKeyboardButton("Name: %s" % name, callback_data = str(ButtonId.NONE))],
                      [InlineKeyboardButton("Type1: %s" % type1, callback_data = str(ButtonId.NONE))],
                      [InlineKeyboardButton("Type2: %s" % type2, callback_data = str(ButtonId.NONE))],
                      [InlineKeyboardButton('More information', callback_data = str(ButtonId.POKEDEX_MOREINFO) + str(dexnum))],
                       [InlineKeyboardButton("⏪ Exit Search", callback_data = str(ButtonId.POKEDEX_EXIT_SEARCH))]]
        dex_keys = InlineKeyboardMarkup(dex_but)
        bot.send_sticker(id, pokesticker, reply_markup = dex_keys)


    def dexentry(self, database, bot, update, id, dexnum):
        """Sends Pokemon-Sticker to user.  a Pokedex-entry"""
        dexterraw = Pokedex.get_all(database, columns = "id, trainerid",
                                    where = "id = " + str(dexnum) + " AND trainerid = " + str(id), order = "id")
        rows = len(dexterraw)
        if rows != 0:
            species = Data.all_species[dexnum - 1]
            pokesticker = Stickerpacks.get_pokemon(dexnum)
            name = species.name
            if species.type1 is not None:
                type1 = species.type1.name
            else:
                type1 = " - "
            if species.type2 is not None:
                type2 = species.type2.name
            else:
                type2 = " - "

        else:
            pokesticker = Stickerpacks.get_item(9)
            name = '???'
            type1 = '???'
            type2 = '???'

        dex_but = [[InlineKeyboardButton("ID: %s" % dexnum, callback_data = str(ButtonId.NONE))],
                      [InlineKeyboardButton("Name: %s" % name, callback_data = str(ButtonId.NONE))],
                      [InlineKeyboardButton("Type1: %s" % type1, callback_data = str(ButtonId.NONE))],
                      [InlineKeyboardButton("Type2: %s" % type2, callback_data = str(ButtonId.NONE))],
                      [InlineKeyboardButton('More information', callback_data = str(ButtonId.POKEDEX_MOREINFO) + str(dexnum))],
                      [InlineKeyboardButton("◀️", callback_data = str(ButtonId.POKEDEX_MIN) + str(dexnum)),
                       InlineKeyboardButton("▶️", callback_data =  str(ButtonId.POKEDEX_PLS) + str(dexnum))],
                       [InlineKeyboardButton("⏪ Pokedex", callback_data = str(ButtonId.PROFILE_POKEDEX))]]
        dex_keys = InlineKeyboardMarkup(dex_but)
        bot.send_sticker(id, pokesticker, reply_markup = dex_keys)

    def getallentries(self, database, trainerid: int, numfrom: int, numto: int):
        """Gets all entries in a string to send it to the user"""

        z = 0
        result = ""
        dexterraw = Pokedex.get_all(database,
                                    columns = "id, trainerid",
                                    where = "trainerid = " +
                                            str(trainerid) +
                                            " AND " +
                                            str(numfrom) +
                                            " <= id AND id <= " + str(numto),
                                    order = "id")
        idar = []
        for j in dexterraw:
            idar.append(j.id)

        for i in range(numfrom, numto + 1):
            z += 1
            owned = """🔸"""
            if i in idar:
                owned = """🔹"""
            result += "[%03d] " % i + owned + " | "
            if z == 3:
                result += "\n"
                z = 0
        return result

    def send_menu(self, bot, trainer):

        bot.send_message(trainer.id, "Ⓟ Ⓞ Ⓚ Ⓔ Ⓓ Ⓔ Ⓧ",
                         reply_markup =
                         InlineKeyboardMarkup(
                             [[InlineKeyboardButton("Full Entries", callback_data = str(ButtonId.POKEDEX_FLIP))],
                              [InlineKeyboardButton("Chart", callback_data = str(ButtonId.POKEDEX_PAGES) + "1")],
                              [InlineKeyboardButton("Search", callback_data = str(ButtonId.POKEDEX_SEARCH))],
                              [InlineKeyboardButton("⏪ Profile", callback_data = str(ButtonId.MENU_PROFILE))]]))