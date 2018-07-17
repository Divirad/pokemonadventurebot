from telegram import Bot, Update, TelegramError, ParseMode

from gamelogic.getdata.trainer import Trainer


def delete_message(bot: Bot, update: Update):
    "deletes Message and Prints Error-Message if user Clicks to fast"
    try:
        update.callback_query.message.delete()
    except TelegramError:
        bot.answerCallbackQuery(callback_query_id = update.callback_query.id, text = "Don't click that fast...",
                                show_alert = False)

def not_implemented_yet(bot: Bot, update: Update, trainer: Trainer):
    bot.answerCallbackQuery(callback_query_id = update.callback_query.id,
                            text = "Not implemented yet", parse_mode = ParseMode.MARKDOWN, show_alert = True)

class PokemonBotError(Exception):
    pass