from telegram import Bot, Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup

from database.db import Database
from errorhandling.errorhandling import delete_message
from gamelogic.button_id import ButtonId
from gamelogic.getdata.trainer import Trainer
from gamelogic.menu_id import MenuId
from telegram_utilities.handler import Handler
from telegram_utilities.registry import Registry
from typing import List

class About(Handler):

    def get_sub_handler(self) -> List['Handler']:
        return []

    def register(self, registry: Registry):
        registry.add_button_handler(ButtonId.INFO_ABOUT, self.printtext, [MenuId.MAIN_MENU])

    def printtext(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        delete_message(bot, update)
        buttons = [[InlineKeyboardButton("⏪ Info", callback_data = str(ButtonId.MENU_INFO))]]
        markup = InlineKeyboardMarkup(buttons)
        bot.send_message(trainer.id,
"""
*Privacy policy*
With using this Bot you agreed to follow terms:

_General_
`This bot` (@PokemonAdventureBot) `uses reasonable precautions to keep the personal information disclosed to us secure 
and to disclose such information only to responsible third parties after permission from the user.
This bot is not responsible for the content or the privacy policies of websites to which we may provide links or the 
websites of our affiliates or advertisers.`

_Information collected by this bot_
`This bot collects information about users during their registration for this game and during their participation in 
certain activities on our bot, including contests. When users request a message from our server, 
our Web server automatically collects some information about the users, 
including their Telegram-IDs and the first name or their nickname. 
These IDs are used by Telegram on the network to send the requested messages and media to users.`

*Copyrights*

_General disclaimer_
`Pokémon (c) 2002-2017 Pokémon. 
(c) 1995-2017 Nintendo/Creatures Inc./GAME FREAK inc. TM, (c) and Pokémon character names are trademarks of Nintendo. 
This bot is not licensed from Nintendo or GameFreak and a non-comercial fan-project. 
It is only for users to have fun and was developed by Divirad for and with fun. ;)

If you like this bot please buy the original games! They are great! ;)`
(Or donate us with this command /donate to keep the server up. 
Save the home of every single pokemon with just a little donation)

*Used sources for gamedata:*
[Bulbapedia](bulbapedia.bulbagarden.net)
[PokemonDB](pokemondb.net)

*Contact*
divirad@gmx.de
@kurodevs""", ParseMode.MARKDOWN, reply_markup = markup)