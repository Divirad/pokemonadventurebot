from telegram import Bot, Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, TelegramError

from typing import List

from database.db import Database
from gamelogic.getdata.trainer import Trainer
from gamelogic.menu_id import MenuId
from gamelogic.button_id import ButtonId

from telegram_utilities.handler import Handler
from telegram_utilities.registry import Registry

from database import Data
from res import Stickerpacks
import datetime as dt

from errorhandling.errorhandling import delete_message


from settings import minutes_to_heal

from errorhandling.errorhandling import not_implemented_yet

class PokemonCenterHandler(Handler):
    def get_sub_handler(self) -> List['Handler']:
        return []

    def register(self, registry: Registry):
        registry.add_command_handler("/center", self.print_menu, [MenuId.MAIN_MENU])  # command for menu_ids 1 and 2
        registry.add_command_handler("/heal", self.heal, [MenuId.MAIN_MENU])  # command for not registered Trainer
        registry.add_command_handler("/com", self.computer, [MenuId.MAIN_MENU])  # command for not registered Trainer

        registry.add_button_handler(ButtonId.GOOUT_CENTER, not_implemented_yet, [MenuId.MAIN_MENU])

        # ButtonId.HEAL_YES
        registry.add_button_handler("heal_y", self.heal_yes, [MenuId.POKEMON_CENTER])
        registry.add_button_handler("heal_n", self.heal_no, [MenuId.POKEMON_CENTER])
        registry.add_button_handler("pickuppkmn", self.pickuppkmn, [MenuId.CENTER_HEAL_BLOCKER])
        registry.add_button_handler("box", self.pickuppkmn, [MenuId.MAIN_MENU])


    def menu(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        buttons = [[InlineKeyboardButton("Heal", callback_data = str(ButtonId.MAINMENU))],
                   [InlineKeyboardButton("Heal", callback_data = str(ButtonId.MAINMENU))],
            [InlineKeyboardButton("⏪ Menu", callback_data = str(ButtonId.MAINMENU))]
        ]

        bot.send_message(trainer.id, reply_markup = InlineKeyboardMarkup(buttons))
        pass

    def print_menu(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        """
        if menu_id==3:
        Prints the POKECENTER-Menu
        """
        update.message.reply_text("""
        ⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️
        /heal Heal your 
        ️  Pokémon
        ️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️
        ️/com Start the 
          computer and 
          manage your 
          PKMN-Team
        ️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️
        """)

    def heal(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        """
        if menu_id==3:
        Ask the player if the trainer wants to heal his Pokemonteam and prints the time the pokemon need to heal.
        Gets id and teamnr from database.
        Yes = menu_id -> MenuId.POKEMON_CENTER
        """
        pokemon = trainer.get_team(database, "id, teamnr")
        row_count = database.dict_cursor.rowcount
        healtime = row_count * minutes_to_heal
        center_buttons = [[InlineKeyboardButton("Heal, please!", callback_data = 'heal_y'),
                           InlineKeyboardButton("Nope.", callback_data = 'heal_n')]]

        center_keys = InlineKeyboardMarkup(center_buttons)
        bot.send_message(id,
                        "Welcome to our Pokémon Center! We heal your Pokémon back to perfect health! Shall we heal your Pokémon? We will need {0} minutes to heal every Pokémon in your team.".format(
                        healtime), reply_markup = center_keys)
        trainer.menu_id = MenuId.POKEMON_CENTER
        trainer.update_values(database, "menu_id")


    # BUTTONS

    def heal_yes(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        delete_message(bot, update)

        pokeraw = trainer.get_team(database, "id, species_id, level, name, teamnr, currenthp, hp_dv, hp_exp")  # blocktimer
        row_count = database.dict_cursor.rowcount
        healtime = row_count * 5

        #   "UPDATE trainer SET blocktimer = NOW() + INTERVAL %s MINUTE WHERE id = %  s;", (healtime, cid,))
        # trainer.set_attribute("blocktimer", "NOW() + INTERVAL {0} MINUTE".format(healtime))
        trainer.blocktimer = dt.datetime.now() + dt.timedelta(minutes = healtime)
        # d.cmd("UPDATE pokemon SET currenthp = %s WHERE id = %s", (temppoke.calculate_max_hp(), temppoke.id,))
        for poke in pokeraw:
            poke.currenthp = poke.calculate_max_hp()
            poke.update_values(database, "currenthp")
            # poke.set_attribute("currenthp", "{0}".format(poke.calculate_max_hp()))

        center_buttons = [[InlineKeyboardButton("Pick up!", callback_data = 'pickuppkmn')]]

        center_keys = InlineKeyboardMarkup(center_buttons)

        bot.send_message(Trainer.id,
                         "Ok. We'll need your Pokémon. Come back in {0} minutes and pick up your Pokémon. You can't do anything while we are healing your Pokémon. Please take a seat in our waiting room...".format(
                             healtime), reply_markup = center_keys)
        trainer.menu_id = MenuId.CENTER_HEAL_BLOCKER

        trainer.update_values(database, "blocktimer")
        trainer.update_values(database, "menu_id")

    def heal_no(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        trainer.menu_id = MenuId.MAIN_MENU
        trainer.update_values(database, "menu_id")
        try:
            update.callback_query.message.delete()
        except TelegramError:
            bot.answerCallbackQuery(callback_query_id = update.callback_query.id, text = "Don't click that fast...",
                                    show_alert = False)
        bot.send_message(Trainer.id, "We hope to see you again! Write or click on /handler to show the handler")

    def pickuppkmn(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        trainer.get_values(database, "blocktimer")
        blocktime = trainer.blocktimer
        if blocktime <= dt.datetime.now():
            bot.send_message(Trainer.id,
                             text = """Thank you! Your Pokémon are fighting fit! We hope to see you again! Hehe... What? I'm not a sadist... Click or write /handler to show the handler!""")
            # d.cmd("UPDATE trainer SET blocktimer = NULL WHERE id = %s;", (cid,))
            trainer.blocktime = None
            trainer.menu_id = 3
            trainer.update_values(database, "menu_id, blocktimer")
            pass
        else:
            waitfor = blocktime - dt.datetime.now()
            minutes = (waitfor.days * 1440) + (waitfor.seconds / 60) + 1  # + waitfor.minute
            bot.answerCallbackQuery(callback_query_id = update.callback_query.id, text = "Wait for %d min..." % minutes,
                                    show_alert = False)

    def computer(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        center_buttons = [[InlineKeyboardButton("Heal, please!", callback_data = 'heal_y'),
                           InlineKeyboardButton("Nope.", callback_data = 'heal_n')]]

        center_keys = InlineKeyboardMarkup(center_buttons)

        box_buttons = [
            [InlineKeyboardButton("Open Box", callback_data = 'center_box')],
            [InlineKeyboardButton("Phone with Oak", callback_data = 'center_oak')],
            [InlineKeyboardButton("Phone with Oak", callback_data = 'center_oak')]]

        box_keys = InlineKeyboardMarkup(box_buttons)
        bot.send_message(id, """B E E P  b o O o p  B e E P...\n
                .  .  .
                W E L C O M E!
                C O M P U T E R   M E N U""", reply_markup = box_keys)

    def com_button(self, bot: Bot, update: Update, trainer: Trainer, database: Database):
        query = update.callback_query
        data = query.data
        cid = query.from_user.id
        if data.find('box') != -1:
            result = "B O X \n====================\n"
            trainer = Trainer(cid)
            # trainer.load_values(d, "id")
            pokes = trainer.get_all_pkmn(d,
                                         "id, name, level, currenthp, gender, hp_exp, hp_dv, species_id, current_status")  # all_pkmn
            id = 1
            if pokes == []:
                result += "Nothing here...\n"
            for poke in pokes:  # [startval:startval+19]:
                # poke.load_values(d, "name, level, currenthp, gender, hp_exp, hp_dv, species_id, current_status")
                result += """ ({0}) {1} [{5}] Lv. {2} \n    HP: {3}/{4}\n""".format(id, poke.name, poke.level,
                                                                                    poke.currenthp,
                                                                                    poke.calculate_max_hp(),
                                                                                    poke.gender)
                id += 1
            result += """====================\n
        /binfo <boxnumber> 
          to get more information 
          about your Pokémon
          in the box
        /tinfo <boxnumber> 
          to get more information 
          about your Pokémon
          in tyour team
        /box2team <box id>
          move a pokemon from 
          your box to your team
        /team2box <team idr>
          move a pokemon from 
          your team to your box
        /change <from> <to>
          change the team id 
          of your Pokémon
        /release <box id>
          release a pokemon
        /trade <box id> <user id>
          trade pokemon"""
            bot.send_message(cid, result)

    # HELP FUNCTIONS
    def show_poke_info(self, bot, id, data, pokes):
        """
        Shows pokemon info Sticker + Message
        :param bot: botstuff
        :param id: trainer id
        :param data: text
        :param pokes: list of pokemon
        """
        pid = int(data[7:])
        poke = pokes[pid - 1]
        calc_attack = 0
        calc_defense = 0
        calc_speed = 0
        calc_spec = 0
        data = Data.all_species[poke.species.id]
        t1 = "-"
        t2 = "-"
        if data.type1 != None:
            t1 = data.type1.name
        if data.type2 != None:
            t2 = data.type2.name

        pokesticker = Stickerpacks.get_pokemon(poke.species.id)
        result = "*NAME:* " + poke.name + ", *LEVEL:* " + str(poke.level) + "\n" + \
                "*No.:* " + "[%03d] " % poke.species.id + ", *HP:* " + str(poke.currenthp) + "/" + str(
                poke.calculate_max_hp()) + "\n" + \
                "*STATUS:* " + str(poke.current_status) + "\n" + \
                "*TYPE 1:* " + t1 + ", *TYPE 2:* " + t2 + "\n" + \
                "*ATTACK:* " + str(calc_attack) + ", *DEFENSE:* " + str(calc_defense) + "\n" + \
                "*SPECIAL:* " + str(calc_spec) + "\n*ID:* " + str(poke.id)
        bot.send_sticker(id, pokesticker)
        bot.send_message(id, result, ParseMode.MARKDOWN)