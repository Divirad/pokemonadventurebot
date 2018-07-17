from gamelogic.button_id import ButtonId
from gamelogic.menu_id import MenuId
from gamelogic.getdata.trainer import Trainer

from errorhandling.errorhandling import delete_message

from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram_utilities.handler import Handler
from telegram_utilities.registry import Registry
from typing import List

from database.db import Database

class TrainerCardHandler(Handler):

    def get_sub_handler(self) -> List['Handler']:
        return []

    def register(self, registry: Registry):
        registry.add_button_handler(ButtonId.PROFILE_TRAINERCARD, self.trainercard, [MenuId.MAIN_MENU])

    def trainercard(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        delete_message(bot, update)
        trainer.load_values(database = database, values = "name, draws, wins, badges, looses, pokedollar")
        trainer.load_values(database = database, values = "registeredsince")
        bot.send_message(trainer.id, """
```Ⓣ Ⓡ Ⓐ Ⓘ Ⓝ Ⓔ Ⓡ - Ⓒ Ⓐ Ⓡ Ⓓ
═══════════════
  Name: {0}
  TrainerID:{1}
  Pokédollar:
  {2}₱
═══════════════
  Registered Since:
  {3}
═══════════════
  Badges: {4}
═══════════════
  Wins: {5}
  Looses: {6}
  Draws: {7}
═══════════════```""".format(
                trainer.name, trainer.id,
                trainer.pokedollar,
                trainer.registeredsince.strftime('%Y-%m-%d'),
                trainer.badges,
                trainer.wins,
                trainer.looses,
                trainer.draws),
                         parse_mode = ParseMode.MARKDOWN,
                         reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("⏪ Profile", callback_data = str(ButtonId.MENU_PROFILE))]]))