import io
import random
import string
from typing import List
from PIL import Image, ImageDraw, ImageFont

from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode

from database.db import Database
from gamelogic.button_id import ButtonId
from gamelogic.fighting import battle
from gamelogic.fighting import battle_message
from gamelogic.getdata.trainer import Trainer
from gamelogic.menu_id import MenuId
from telegram_utilities.handler import Handler
from telegram_utilities.registry import Registry


class BattleHandler(Handler):
    def get_sub_handler(self) -> List['Handler']:
        return []

    def register(self, registry: Registry):
        registry.add_command_handler("test_battle", self.test_cmd, [MenuId.MAIN_MENU])
        registry.add_command_handler("menu", self.reset_fight, [MenuId.BATTLE])

        registry.add_command_handler("sticker", lambda b, u, t: self.sticker(b, u, t, True), [MenuId.MAIN_MENU])
        registry.add_command_handler("photo", lambda b, u, t: self.sticker(b, u, t, False), [MenuId.MAIN_MENU])

        registry.add_button_handler(ButtonId.BATTLE_MENU_FIGHT, self.menu_fight, [MenuId.BATTLE])
        registry.add_button_handler(ButtonId.BATTLE_MENU_POKEMON, self.menu_pokemon, [MenuId.BATTLE])
        registry.add_button_handler(ButtonId.BATTLE_MENU_BACK, self.menu_back, [MenuId.BATTLE])

        registry.add_button_handler(ButtonId.BATTLE_MENU_ITEMS, self.not_implemented_yet, [MenuId.BATTLE])
        registry.add_button_handler(ButtonId.BATTLE_MENU_RUN, self.not_implemented_yet, [MenuId.BATTLE])
        registry.add_button_handler(ButtonId.BATTLE_MENU_MOVE, self.not_implemented_yet, [MenuId.BATTLE])
        registry.add_button_handler(ButtonId.BATTLE_MENU_NEW_POKEMON, self.not_implemented_yet, [MenuId.BATTLE])

    button_back = InlineKeyboardButton("Back", callback_data=ButtonId.BATTLE_MENU_BACK + '')
    button_none = InlineKeyboardButton(" ", callback_data=ButtonId.NONE + '')
    menu_main = InlineKeyboardMarkup(
        [[InlineKeyboardButton('FIGHT', callback_data=ButtonId.BATTLE_MENU_FIGHT + ''),
          InlineKeyboardButton('POKEMON', callback_data=ButtonId.BATTLE_MENU_POKEMON + '')],
         [InlineKeyboardButton('ITEM', callback_data=ButtonId.BATTLE_MENU_ITEMS + ''),
          InlineKeyboardButton('RUN', callback_data=ButtonId.BATTLE_MENU_RUN + '')]],
        one_time_keyboard=True)

    @classmethod
    def test_cmd(cls, bot: Bot, update: Update, trainer: Trainer, database: Database):
        args = update.message.text.split(" ")
        if len(args) == 1:
            species_id = 15
            level = 15
            bot.send_message(update.message.chat_id, "Using default args: species id=15, level=15")
        else:
            try:
                assert len(args) == 3
                species_id = int(args[1])
                level = int(args[2])
            except (AssertionError, ValueError):
                bot.send_message(update.message.chat_id, "Usage: /test_battle [species id] [level]")
                return

        success, msg = battle.start_wild(trainer, species_id, level, database)
        if success:
            battle_message.send(bot, trainer.id, cls.menu_main, trainer.fight.wildPokemon, trainer.fight.trainerPokemon,
                                msg)
        else:
            bot.send_message(trainer.id, msg)

    @classmethod
    def menu_fight(cls, bot: Bot, update: Update, trainer: Trainer, database: Database):
        trainer.load_values(database, "fight")
        trainer.fight.load_values(database, "trainerPokemon")
        trainer.fight.trainerPokemon.load_values(database, "move0, move1, move2, move3")

        bttns = []
        for i in range(4):
            m = trainer.fight.trainerPokemon.get_move(i)
            if m is None:
                bttns.append(cls.button_none)
            else:
                m.load_values(database, "move_id, currentap")
                bttns.append(InlineKeyboardButton(
                    "%s  %d/%d" % (m.move.name, m.currentap, m.move.pp),
                    callback_data=ButtonId.BATTLE_MENU_MOVE + str(i)))

        battle_message.edit_menu(bot, update.callback_query.message, InlineKeyboardMarkup(
            [[bttns[0], bttns[1]], [bttns[2], bttns[3]], [cls.button_back]]))

    @classmethod
    def menu_pokemon(cls, bot: Bot, update: Update, trainer: Trainer, database: Database):
        team = trainer.get_team(database, "id, name, level")
        buttons = []
        for i, t in enumerate(team):
            buttons.append([InlineKeyboardButton(
                t.name + " - lvl. " + str(t.level), callback_data=ButtonId.BATTLE_MENU_NEW_POKEMON + str(i))])
        buttons.append([cls.button_back])
        battle_message.edit_menu(bot, update.callback_query.message, InlineKeyboardMarkup(buttons))

    @classmethod
    def menu_back(cls, bot: Bot, update: Update, trainer: Trainer):
        battle_message.edit_menu(bot, update.callback_query.message, cls.menu_main)

    @staticmethod
    def reset_fight(bot: Bot, update: Update, trainer: Trainer, database: Database):
        trainer.menu_id = int(MenuId.MAIN_MENU)
        trainer.fight = None
        trainer.update_values(database, "fight, menu_id")

    @staticmethod
    def not_implemented_yet(bot: Bot, update: Update, trainer: Trainer):
        bot.answerCallbackQuery(callback_query_id=update.callback_query.id,
                                text="Not implemented yet", parse_mode=ParseMode.MARKDOWN, show_alert=True)

    @classmethod
    def sticker(cls, bot: Bot, update: Update, trainer: Trainer, use_sticker: bool):
        args = update.message.text.split(" ")
        try:
            assert len(args) in range(3, 8)
            species_0 = int(args[1])
            assert species_0 in range(1, 152)
            species_1 = int(args[2])
            assert species_1 in range(1, 152)
            text_0 = str(args[3]) if len(args) >= 4 else "Text 1"
            text_1 = str(args[4]) if len(args) >= 5 else "Text 2"
            lvl_0 = "Lv %02d" % int(args[5]) if len(args) >= 6 else "Lv 00"
            lvl_1 = "Lv %02d" % int(args[6]) if len(args) >= 7 else "Lv 99"
        except (AssertionError, ValueError):
            bot.send_message(update.message.chat_id, "Usage: /%s <species id 1> <species id 2> [text 1] [text 2]"
                                                     " [Lvl 1] [Lvl 2]" % ("sticker" if use_sticker else "photo"))
            return

        new_image = Image.open("res/images/scene.png").convert('RGBA')

        image0 = Image.open("res/images/%d.png" % species_0).convert('RGBA').resize((128, 128), Image.ANTIALIAS)
        image1 = Image.open("res/images/%d.png" % species_1).convert('RGBA').resize((128, 128), Image.ANTIALIAS)

        new_image.paste(image0, (82, 122), image0)
        new_image.paste(image1, (350, 30), image1)

        d = ImageDraw.Draw(new_image)
        font = ImageFont.truetype('res/fonts/pokemon_pixel_font.ttf', 28)

        d.text((45, 45), text_0, font=font, fill=(0, 0, 0))
        d.text((327, 177), text_1, font=font, fill=(0, 0, 0))

        d.text((227 - d.textsize(lvl_0, font=font)[0], 45), lvl_0, font=font, fill=(0, 0, 0))
        d.text((510 - d.textsize(lvl_1, font=font)[0], 177), lvl_1, font=font, fill=(0, 0, 0))

        byte_image = io.BytesIO()
        new_image.save(byte_image, format='PNG')
        byte_image.seek(0)

        if use_sticker:
            bot.send_sticker(trainer.id, byte_image)
        else:
            bot.send_photo(trainer.id, byte_image)
