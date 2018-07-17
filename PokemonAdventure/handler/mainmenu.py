from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup  # , TelegramError, ParseMode

from telegram_utilities.handler import Handler
from telegram_utilities.registry import Registry
from typing import List

from database.db import Database
from errorhandling.errorhandling import delete_message
from gamelogic.menu_id import MenuId
from gamelogic.getdata.trainer import Trainer

from gamelogic.button_id import ButtonId


class Menu(Handler):

    def get_sub_handler(self) -> List['Handler']:
        return []

    def register(self, registry: Registry):
        # Commands
        registry.add_command_handler("menu", self.send_new_menu, [MenuId.MAIN_MENU])  # command for menu_ids 1 and 2

        # Main-Menu
        registry.add_button_handler(ButtonId.MAINMENU, self.mainmenu, [MenuId.MAIN_MENU])

        # Sub-Menu
        registry.add_button_handler(ButtonId.MENU_PROFILE, self.profile, [MenuId.MAIN_MENU])
        registry.add_button_handler(ButtonId.MENU_GOOUT, self.gout, [MenuId.MAIN_MENU])
        registry.add_button_handler(ButtonId.MENU_DAILY, self.daily, [MenuId.MAIN_MENU])
        registry.add_button_handler(ButtonId.MENU_INFO, self.info, [MenuId.MAIN_MENU])


    def mainmenu(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        """MainMenu"""
        delete_message(bot, update)
        self.send_main_menu(bot, trainer)

    def send_new_menu(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        self.send_main_menu(bot, trainer)

    def send_main_menu(self, bot: Bot, trainer: Trainer):
        buttons = [[InlineKeyboardButton("Profile", callback_data = str(ButtonId.MENU_PROFILE))],
                   [InlineKeyboardButton("Go Out", callback_data = str(ButtonId.MENU_GOOUT))],
                   [InlineKeyboardButton("Daily Reward", callback_data = str(ButtonId.MENU_DAILY))],
                   [InlineKeyboardButton("Information", callback_data = str(ButtonId.MENU_INFO))]]
        markup = InlineKeyboardMarkup(buttons)
        bot.send_message(trainer.id, "Ⓜ Ⓔ Ⓝ Ⓤ", reply_markup = markup)

    @staticmethod
    def print_sub_menu(bot, update, trainer, menu: str, buttons):
        """Prints a Sub-Menu"""
        delete_message(bot, update)
        markup = InlineKeyboardMarkup(buttons)
        bot.send_message(trainer.id, menu, reply_markup = markup)

    def profile(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        """Profile-Menu"""
        # TODO implement Bag
        buttons = [[InlineKeyboardButton("Team", callback_data = str(ButtonId.PROFILE_POKEMON))],
                   [InlineKeyboardButton("Pokedex", callback_data = str(ButtonId.PROFILE_POKEDEX))],
                   [InlineKeyboardButton("Bag", callback_data = str(ButtonId.PROFILE_BAG))],
                   [InlineKeyboardButton("Trainer-Card", callback_data = str(ButtonId.PROFILE_TRAINERCARD))],
                   [InlineKeyboardButton("⏪ Menu", callback_data = str(ButtonId.MAINMENU))]]
        self.print_sub_menu(bot, update, trainer, "Ⓟ Ⓡ Ⓞ Ⓕ Ⓘ Ⓛ Ⓔ", buttons)

    def gout(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        """GoOut-Menu"""
        # TODO implement Center
        # TODO implement Shop
        # TODO implement Gyms
        buttons = [[InlineKeyboardButton("Walk around", callback_data = str(ButtonId.GOOUT_WALK))],
                   [InlineKeyboardButton("Center", callback_data = str(ButtonId.GOOUT_CENTER))],
                   [InlineKeyboardButton("Shop", callback_data = str(ButtonId.GOOUT_SHOP))],
                   [InlineKeyboardButton("Gyms", callback_data = str(ButtonId.GOOUT_GYMS))],
                   [InlineKeyboardButton("⏪ Menu", callback_data = str(ButtonId.MAINMENU))]]
        self.print_sub_menu(bot, update, trainer, "Ⓖ Ⓞ - Ⓞ Ⓤ Ⓣ", buttons)

        # TODO implement Reward

    def daily(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        """Daily-Menu"""
        buttons = [[InlineKeyboardButton("Daily Reward", callback_data = str(ButtonId.DAILY_REWARD))],
                   [InlineKeyboardButton("Donate", callback_data = str(ButtonId.DAILY_DONATE))],
                   [InlineKeyboardButton("⏪ Menu", callback_data = str(ButtonId.MAINMENU))]]
        self.print_sub_menu(bot, update, trainer, "Ⓓ Ⓐ Ⓘ Ⓛ Ⓨ", buttons)

    def info(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        """Info-Menu"""
        # TODO implement News
        buttons = [[InlineKeyboardButton("About", callback_data = str(ButtonId.INFO_ABOUT))],
                   [InlineKeyboardButton("News", callback_data = str(ButtonId.INFO_NEWS))],
                   [InlineKeyboardButton("Donate", callback_data = str(ButtonId.DAILY_DONATE))],
                   [InlineKeyboardButton("⏪ Menu", callback_data = str(ButtonId.MAINMENU))]]
        self.print_sub_menu(bot, update, trainer, "Ⓘ Ⓝ Ⓕ Ⓞ Ⓡ Ⓜ Ⓐ Ⓣ Ⓘ Ⓞ Ⓝ Ⓢ", buttons)
