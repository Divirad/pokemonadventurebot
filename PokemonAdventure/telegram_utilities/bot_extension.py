from telegram import ParseMode
from telegram.constants import MAX_MESSAGE_LENGTH
from time import sleep


def send_large_message(bot, chat_id, text: str, **kwargs):
    """
    sends a large message
    """
    if len(text) <= MAX_MESSAGE_LENGTH:
        return bot.send_message(chat_id, text, **kwargs)

    parts = []
    while len(text) > 0:
        if len(text) > MAX_MESSAGE_LENGTH:
            part = text[:MAX_MESSAGE_LENGTH]
            first_lnbr = part.rfind('\n')
            if first_lnbr != -1:
                parts.append(part[:first_lnbr])
                text = text[first_lnbr:]
            else:
                parts.append(part)
                text = text[MAX_MESSAGE_LENGTH:]
        else:
            parts.append(text)
            break

    msg = None
    for part in parts:
        msg = bot.send_message(chat_id, part, **kwargs)
        sleep(1)
    return msg  # return only the last message


def send_large_code_message(bot, chat_id, text: str, **kwargs):
    """sends a large code message"""
    if len(text) <= MAX_MESSAGE_LENGTH:
        return bot.send_message(chat_id, "```" + text + "```", parse_mode=ParseMode.MARKDOWN, **kwargs)

    parts = []
    while len(text) > 0:
        if len(text) > MAX_MESSAGE_LENGTH:
            part = text[:MAX_MESSAGE_LENGTH]
            first_lnbr = part.rfind('\n')
            if first_lnbr != -1:
                parts.append(part[:first_lnbr])
                text = text[first_lnbr:]
            else:
                parts.append(part)
                text = text[MAX_MESSAGE_LENGTH:]
        else:
            parts.append(text)
            break

    msg = None
    for part in parts:
        msg = bot.send_message(chat_id, "```" + part + "```", parse_mode=ParseMode.MARKDOWN, **kwargs)
        sleep(1)
    return msg  # return only the last message
