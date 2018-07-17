from typing import List
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode

from database.db import Database
from res import Stickerpacks
from telegram_utilities.handler import Handler
from telegram_utilities.registry import Registry

from errorhandling.errorhandling import delete_message
from gamelogic.button_id import ButtonId
from gamelogic.getdata.trainer import Trainer
from gamelogic.menu_id import MenuId
from handler.goout.rpg.constants import WAYTYPE
from errorhandling.pokemonboterror import PokemonBotError
from handler.goout.rpg.map import get_map



class WalkAround(Handler):

    def get_sub_handler(self) -> List['Handler']:
        return []

    def register(self, registry: Registry):
        registry.add_button_handler(ButtonId.GOOUT_WALK , self.send_actual_position, [MenuId.MAIN_MENU])

        registry.add_button_handler(ButtonId.WALK_LEFT , self.left, [MenuId.MAIN_MENU])
        registry.add_button_handler(ButtonId.WALK_RIGHT , self.right, [MenuId.MAIN_MENU])
        registry.add_button_handler(ButtonId.WALK_UP , self.up, [MenuId.MAIN_MENU])
        registry.add_button_handler(ButtonId.WALK_DOWN , self.down, [MenuId.MAIN_MENU])

        registry.add_button_handler(ButtonId.WALK_INTERACT , self.interact, [MenuId.MAIN_MENU])
        registry.add_button_handler(ButtonId.WALK_WARP , self.warp, [MenuId.MAIN_MENU])
        registry.add_button_handler(ButtonId.WALK_INFO, self.information_popup, [MenuId.MAIN_MENU])

    def interact(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        pass

    def warp(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        pass

    def left(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        self.move_player(trainer, database, -1, 0)
        self.send_actual_position(bot, update, trainer, database)

    def right(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        self.move_player(trainer, database, 1, 0)
        self.send_actual_position(bot, update, trainer, database)

    def up(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        self.move_player(trainer, database, 0, -1)
        self.send_actual_position(bot, update, trainer, database)

    def down(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        self.move_player(trainer, database, 0, 1)
        self.send_actual_position(bot, update, trainer, database)

    def move_player(self, trainer, database, x:int, y:int):
        trainer.load_values(database, "game_pos_x, game_pos_y")
        trainer.game_pos_x += x
        trainer.game_pos_y += y
        trainer.update_values(database, "game_pos_x, game_pos_y")

    def information_popup(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        """displays information in a pop up"""
        trainer.load_values(database, "game_pos_x, game_pos_y, game_location_id")
        interact = False
        actual_location = get_map().get_location_by_id(trainer.game_location_id)


        text = "You're currently here: " + actual_location.name + "\n\n" + actual_location.description + "\n" + \
        "_________\n🆗: Interact\n🔄: Warp to next location"

        bot.answerCallbackQuery(callback_query_id = update.callback_query.id,
                                text = text, parse_mode = ParseMode.MARKDOWN, show_alert = True)

    def send_actual_position(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        """sends the loaded rpg piece"""
        trainer.load_values(database, "game_pos_x, game_pos_y, game_location_id")

        interact = False

        actual_location = get_map().get_location_by_id(trainer.game_location_id)
        actual_tile = actual_location.get_tile(trainer.game_pos_x, trainer.game_pos_y)

        sticker = None
        if actual_tile == WAYTYPE.NONE:
            # TODO log Error
            pass

        left = actual_location.can_walk(trainer.game_pos_x - 1, trainer.game_pos_y)
        right = actual_location.can_walk(trainer.game_pos_x + 1, trainer.game_pos_y)
        up = actual_location.can_walk(trainer.game_pos_x , trainer.game_pos_y - 1)
        down = actual_location.can_walk(trainer.game_pos_x, trainer.game_pos_y + 1)

        if actual_tile is None:
            # TODO Raise Error!
            trainer.load_values(database, "name")
            bot.send_message(trainer.id, "Hello "+ trainer.name+ "! Sadly there occured an error in this bot" + \
                ":( Please go to your trainercard write down your trainer-ID and inform @kurodevs that you "+ \
                             " have an \"invalid position in the map\". We will fix it soon! "+\
                             "Thank you for using our bot! <3")
            raise PokemonBotError("Trainer: "+ str(trainer.id) +" has no valid position in the map!")

        if actual_tile.type == WAYTYPE.FOREST:
            sticker = Stickerpacks.get_forrestpath(left, right, up, down)

        markup = self.create_markup(left, right, up, down, interact)

        delete_message(bot, update)
        bot.sendSticker(trainer.id, sticker = sticker, reply_markup = markup)

    def create_markup(self, left:bool, right:bool, up:bool, down:bool, interact: bool,
                      info: str = "Click for more info",
                      callback_interact = ButtonId.NONE) -> InlineKeyboardMarkup:
        """creates a InlineKeyboardMarkup for interaction"""
        b_info = InlineKeyboardButton(info, callback_data = str(ButtonId.WALK_INFO))
        b_left = InlineKeyboardButton("❌", callback_data = str(ButtonId.NONE))
        b_right = InlineKeyboardButton("❌", callback_data = str(ButtonId.NONE))
        b_up = InlineKeyboardButton("❌", callback_data = str(ButtonId.NONE))
        b_down = InlineKeyboardButton("❌", callback_data = str(ButtonId.NONE))
        b_interact = InlineKeyboardButton(" ", callback_data = str(ButtonId.NONE))
        back_to_menu = InlineKeyboardButton("⏪ Back to Menu", callback_data = str(ButtonId.MAINMENU))

        if left:
            b_left = InlineKeyboardButton("⬅️", callback_data = str(ButtonId.WALK_LEFT))
        if right:
            b_right = InlineKeyboardButton("️️➡️", callback_data = str(ButtonId.WALK_RIGHT))
        if up:
            b_up = InlineKeyboardButton("⬆", callback_data = str(ButtonId.WALK_UP))
        if down:
            b_down = InlineKeyboardButton("⬇️", callback_data = str(ButtonId.WALK_DOWN))
        if interact:
            b_interact = InlineKeyboardButton("🆗️", callback_data = str(callback_interact))

        buttons = [[b_info],
                   [b_up],
                   [b_left, b_interact, b_right],
                   [b_down],
                   [back_to_menu]]
        markup = InlineKeyboardMarkup(buttons)
        return markup

    def wild_pokemon_popup(self, bot: Bot, update: Update):
        """displays information in a pop up"""
        text = "A WILD POKéMON APPEARS"

        bot.answerCallbackQuery(callback_query_id = update.callback_query.id,
                                text = text, show_alert = True)
