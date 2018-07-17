from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup

from telegram_utilities.handler import Handler
from telegram_utilities.registry import Registry
from typing import List

from errorhandling.errorhandling import delete_message

from database.db import Database
from database.Data import all_species

from gamelogic.getdata.trainer import Trainer
from gamelogic.getdata.pokemon import Pokemon
from gamelogic.getdata.pokedex import Pokedex

from gamelogic.button_id import ButtonId
from gamelogic.menu_id import MenuId
from res import Stickerpacks

import logging

logger = logging.getLogger(__name__)


class Start(Handler):
    """/Start handler class,
    User Registration, Daily-Reward Handling and Invitations"""

    def get_sub_handler(self) -> List['Handler']:
        return []

    def register(self, registry: Registry):
        """Registers start commands"""
        registry.add_command_handler("start", self.start, [None])

        registry.add_command_handler("start", self.already_registered, [MenuId.MAIN_MENU])

        registry.add_button_handler(ButtonId.SWITCH_TO_STARTER, self.switch_to_starter, [MenuId.CHOOSE_STARTER])
        registry.add_button_handler(ButtonId.CHOOSE_STARTER, self.choosed, [MenuId.CHOOSE_STARTER])

        registry.add_button_handler(ButtonId.YES_RENAME, self.yes_name, [MenuId.CHOOSE_IF_RENAME])
        registry.add_button_handler(ButtonId.NO_RENAME, self.no_name, [MenuId.CHOOSE_IF_RENAME])

        registry.add_message_handler(self.rename, [MenuId.ENTER_NAME]) # MenuId.ENTER_NAME

    def start(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        """Start cmd"""
        id = update.message.from_user.id

        name = update.message.from_user.first_name
        data = update.message.text
        invcode = data[7:]

        if trainer.does_exist(database):
            if data.find("fancycode") != -1:
                self.daily_code(bot, update, trainer, database)
            else:
                self.already_registered(bot, update, trainer)

        else:
            if invcode != None and invcode != " " and invcode != "" and int(invcode) != id:
                inviter = Trainer(int(invcode))
                if inviter.does_exist(database):
                    self.invite_code(bot, update, trainer, inviter, database)
                else:
                    self.invalid_invitation(bot, update, trainer, database)
            else:
                Trainer.create_new(database, id, name, 800)

            self.register_user(bot, update, trainer, database)

    def switch_to_starter(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        """Switch Pokemon Buttons"""
        data = update.callback_query.data

        species = int(data.replace(str(ButtonId.SWITCH_TO_STARTER), ""))
        bot.sendSticker(trainer.id, Stickerpacks.get_starter(species), reply_markup = self.return_starter_buttons()[species])

        delete_message(bot, update)

    def choosed(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        """Choose Pokemon"""
        data = update.callback_query.data
        species = int(data.replace(str(ButtonId.CHOOSE_STARTER), ""))

        poke = Pokemon.create_new(database, all_species[species], 5, trainer)
        delete_message(bot, update)
        bot.sendSticker(trainer.id, Stickerpacks.get_item(0))
        bot.send_message(trainer.id,
                         text = "Nice, " + poke.name + " is your first Pokémon!\n" + poke.species.pokedextext
                                + "\nDo you want to give your Pokémon a nickname?",
                         reply_markup = self.return_rename_buttons())
        trainer.menu_id = int(MenuId.CHOOSE_IF_RENAME)
        trainer.lastcatched = poke.id
        trainer.update_values(database, "menu_id, lastcatched")
        dexter = Pokedex(poke.id, trainer.id)
        dexter.create_new(database, poke.species.id, trainer)

    def yes_name(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        """Rename Message"""
        delete_message(bot, update)
        bot.send_message(trainer.id, text = "Okay nice! How do you want to call your little friend?"
                                         " (Please only use normal character [A-Z, a-z], maximal 16 chars)")
        trainer.load_values(database = database, values = "menu_id")
        trainer.menu_id = int(MenuId.ENTER_NAME)
        trainer.update_values(database, "menu_id")

    def rename(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        """Rename Pokemon"""
        trainer.load_values(database = database, values = "lastcatched")
        poke = Pokemon(trainer.lastcatched)
        poke.load_values(database, "species_id")

        name = update.message.text[0:16].replace(" ", "")

        c = True

        for c in name:
            if (not (c.isupper() or c.islower())):
                c = False

        if c:
            poke.name = name
            trainer.menu_id = int(MenuId.MAIN_MENU)
            trainer.lastcatched = None
            trainer.update_values(database, "menu_id, lastcatched")
            poke.update_values(database, "name")
            bot.send_message(trainer.id,
                             text = "You want to call your {1} {0}? Great! I think you will become good friends. Your {0} seems very strong! Click on the button bellow to show the Mainmenu."
                             .format(poke.name, poke.species.name), reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Menu", callback_data=str(ButtonId.MAINMENU))]]))

        else:
            bot.send_message(trainer.id,
                             text = "Youuuu little rascal. There were bad character in this name, try it again.")

    def no_name(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        """Dont want to Rename"""
        delete_message(bot, update)
        bot.send_message(trainer.id, text = "Nice! Have fun with your new friend! You two seem very strong!"
                                         " Click on the button bellow to show the Mainmenu.",
                         reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Menu", callback_data=str(ButtonId.MAINMENU))]]))

        trainer.menu_id = int(MenuId.MAIN_MENU)
        trainer.lastcatched = None
        trainer.update_values(database, "menu_id, lastcatched")

    def invite_code(self, bot, update, invcode, trainer: Trainer, inviter: Trainer, database: Database):
        """Handles Invite Code"""
        inviter.load_values(database, "pokedollar")
        inviter.pokedollar = inviter.pokedollar + 400
        inviter.update_values(database, "pokedollar")
        Trainer.create_new(database, id, update.message.from_user.first_name, 1200)
        bot.send_message(update.message.chat_id,
                         text = "Invited by {0}! You both got 400₱ as gift!".format(inviter.name))
        logger.info(
            "{0} with ID {1} was recuted by {2} with ID {3}".format(update.message.from_user.first_name, id, inviter.name, inviter.id))

    def invalid_invitation(self, bot, update, trainer, database):
        """Handes Invalid Invidation"""
        bot.send_message(update.message.chat_id,
                         text = "Invalid Invitationcode :( Maybe... IT WAS A TRAP?!")
        Trainer.create_new(database, trainer.id, update.message.from_user.first_name, 800)

    def daily_code(self, bot, update, trainer: Trainer, database: Database):
        """Compares and handles generated daily codes in database"""
        # TODO check Daily Code

        trainer.load_values(database, "pokedollar")
        trainer.pokedollar = trainer.pokedollar + 100
        bot.send_message(update.message.chat_id,
                         text = "You used a fancy secret code!\nNext link will be active tomorrow! :) " +
                                "Thank you for playing! WE LOVE YOU!! WE LOVE EVERYBODY!!!! AGJDHKS!!!!\n" +
                                "PS: Pokedollar are no Cryptocurrency!!! (Not Yet ;) ) " +
                                "But you can send us some crypto with /donate to keep this project alive :) <3")
        trainer.update_values(database, "pokedollar")

    def already_registered(self, bot, update, trainer):
        """handles already registered user"""

        buttons = [[InlineKeyboardButton("Delete Your Account", callback_data = str(ButtonId.PROFILE_POKEMON))],
                   [InlineKeyboardButton("⏪ Menu", callback_data = str(ButtonId.MAINMENU))]]
        markup = InlineKeyboardMarkup(buttons)
        bot.send_message(update.message.chat_id,
                         text = "Ehm... {0}, you are already a Pokémon-Trainer. Do you want to delete your"
                                " account? Your Pokemon and all your achievements will be deleted. "
                                " This operation cannot be undone.".format(update.message.from_user.first_name),
                         reply_markup = markup)

    def register_user(self, bot, update, trainer, database):
        """registers user in database"""
        bot.send_message(update.message.chat_id,
                         text = ("Hello {0}! Welcome to the world of Pokémon! My name is Oak! People call me the" +
                                 "Pokémon Prof! This world is inhabited by creatures called Pokémon! For some people," +
                                 "Pokémon are pets. Others use them for fights. Myself... I study pokémon as a" +
                                 "profession. You want to be a Pokémontrainer? Thats awesome! Please choose your" +
                                 "first Pokémon!").format(update.message.from_user.first_name))
        bot.sendSticker(update.message.chat_id, Stickerpacks.get_starter(1),
                        reply_markup = self.return_starter_buttons()[1])
        logger.info("{0} with ID {1} is now a fancy Pokémon-Trainer".format(update.message.from_user.first_name, trainer.id))

        trainer.menu_id = int(MenuId.CHOOSE_STARTER)
        trainer.update_values(database, "menu_id")

    def return_rename_buttons(self):
        """returns InlineKeyboardMarkup"""
        return InlineKeyboardMarkup([[InlineKeyboardButton("Yes", callback_data=str(ButtonId.YES_RENAME)),
                                        InlineKeyboardButton("No", callback_data=str(ButtonId.NO_RENAME))]])

    def return_starter_buttons(self):
        """returns InlineKeyboardMarkup"""
        return [InlineKeyboardMarkup([[InlineKeyboardButton("Bulbasaur",
                                                            callback_data = str(ButtonId.SWITCH_TO_BULBASAUR)),
                                       InlineKeyboardButton("Squirtle",
                                                            callback_data = str(ButtonId.SWITCH_TO_SQUIRTLE))],
                                      [InlineKeyboardButton("Charmander, I choose you!",
                                                            callback_data = str(ButtonId.CHOOSE_CHARMANDER))]]),
                InlineKeyboardMarkup([[InlineKeyboardButton("Charmander",
                                                            callback_data = str(ButtonId.SWITCH_TO_CHARMANDER)),
                                       InlineKeyboardButton("Bulbasaur",
                                                            callback_data = str(ButtonId.SWITCH_TO_BULBASAUR))],
                                      [InlineKeyboardButton("Squirtle, I choose you!",
                                                            callback_data = str(ButtonId.CHOOSE_SQUIRTLE))]]),
                InlineKeyboardMarkup([[InlineKeyboardButton("Squirtle",
                                                            callback_data = str(ButtonId.SWITCH_TO_SQUIRTLE)),
                                       InlineKeyboardButton("Charmander",
                                                            callback_data = str(ButtonId.SWITCH_TO_CHARMANDER))],
                                      [InlineKeyboardButton("Bulbasaur, I choose you!",
                                                            callback_data = str(ButtonId.CHOOSE_BULBASAUR))]])]
