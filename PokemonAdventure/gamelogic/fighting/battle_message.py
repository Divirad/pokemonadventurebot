from math import ceil

from telegram import InlineKeyboardMarkup, Bot, Message

from res.Stickerpacks import get_pokemon
from gamelogic.getdata.pokemon import Pokemon


def send(bot: Bot, chat_id: int, menu: InlineKeyboardMarkup, wild: Pokemon, you: Pokemon, msg: str):
    """
    Send a new battle message to the user. The message contains a sticker of the wild pokemon and for each pokemon a
    life bar. This message will be used for further battle interaction

    :param bot: telegram bot, which send the message
    :param chat_id: id of the chat, in which the message should be send
    :param menu: keyboard, which will be attached to the message
    :param wild: wild attacking pokemon; Needs (species, currenthp, hp_dv, hp_ev, name, level)
    :param you: pokemon of the trainer; Needs (species, currenthp, hp_dv, hp_ev, name, level)
    :param msg: string content of the message
    """
    bot.sendSticker(chat_id, get_pokemon(wild.species.id))
    wild_percent = round(100 * wild.currenthp / wild.calculate_max_hp(), 0)
    wild_bar = '█' * int(ceil(wild_percent / 5))
    you_percent = round(100 * you.currenthp / you.calculate_max_hp(), 0)
    you_bar = '█' * int(ceil(you_percent / 5))
    bot.send_message(chat_id, "{} - lvl {} (wild)\n{}% ~ {}\n{} - lvl {}\n{}% ~ {}\n---------------------------------"
                              "----------------\n{}".format(wild.name, wild.level, int(wild_percent), wild_bar,
                                                            you.name, you.level, int(you_percent), you_bar, msg),
                     reply_markup=menu)


def update(bot: Bot, old_msg: Message, menu: InlineKeyboardMarkup, wild: Pokemon, you: Pokemon, msg: str):
    """
    Updates a battle message. The new message contains the updated life bars and a new handler and string message

    :param bot: telegram bot, which updates the message
    :param old_msg: message, that will be updated
    :param menu: the new keyboard handler
    :param wild: wild attacking pokemon; Needs (species, currenthp, hp_dv, hp_ev, name, level)
    :param you: pokemon of the trainer; Needs (species, currenthp, hp_dv, hp_ev, name, level)
    :param msg: string content of the message
    """
    wild_percent = round(100 * wild.currenthp / wild.calculate_max_hp(), 0)
    wild_bar = '█' * int(ceil(wild_percent / 5))
    you_percent = round(100 * you.currenthp / you.calculate_max_hp(), 0)
    you_bar = '█' * int(ceil(you_percent / 5))
    bot.edit_message_text("{} - lvl {} (wild)\n{}% ~ {}\n{} - lvl {}\n{}% ~ {}\n---------------------------------------"
                          "----------\n{}".format(wild.name, wild.level, int(wild_percent),
                                                  wild_bar, you.name, you.level, int(you_percent), you_bar, msg),
                          old_msg.chat_id, old_msg.message_id, reply_markup=menu)


def edit(bot: Bot, old_msg: Message, menu: InlineKeyboardMarkup, msg: str):
    """
    Edits a battle message. The new message contains a new handler and string message but still conatins the old life bars

    :param bot: telegram bot, which edits the message
    :param old_msg: message, that will be edited
    :param menu: the new keyboard handler
    :param msg: string content of the message
    """
    new_msg = "\n".join(old_msg.text.splitlines()[0:5]) + '\n' + msg
    bot.edit_message_text(new_msg, old_msg.chat_id, old_msg.message_id, reply_markup=menu)


def edit_menu(bot: Bot, old_msg: Message, menu: InlineKeyboardMarkup):
    """
    Changes the handler of a battle message. The new message contains the same message text, only a new keyboard

    :param bot: telegram bot, which edits the message
    :param old_msg: message, that will be edited
    :param menu: the new keyboard handler
    """
    bot.edit_message_text(old_msg.text, old_msg.chat_id, old_msg.message_id, reply_markup=menu)
