from telegram import Bot

dex1 = dex2 = starter = items = itemms = None


def init(bot: Bot):  # bot to get stickerpacks from
    """Inits the Sticker-IDs"""
    global dex1, dex2, starter, items, forrest, cave
    dex1 = bot.get_sticker_set('pokemonadventure')
    dex2 = bot.get_sticker_set('pokemonadventure2')
    starter = bot.get_sticker_set('starteradventure')
    items = bot.get_sticker_set('item4adventure')

    forrest = bot.get_sticker_set('forrestpath')
    cave = bot.get_sticker_set('cavepath')


def get_potions(id: int):
    """0 - Potions | 1 - SuperPotion
    2 - HyperPotion| 3 - MaxPotion
    4 - Full Restore
    :param id: Potion-ID
    :return: real Sticker"""
    temp_id = 4 + id
    if id > 4:
        temp_id = 4
    return items.stickers[temp_id]


def get_balls(id: int):
    """0 - Ball | 1 - SuperBall
    2 - HyperBall| 3 - Masterball
    :param id: Ball-ID
    :param id: Ball-ID
    :return: real Sticker"""
    balls = id
    if balls > 3:
        balls = 0
    return items.stickers[balls]


def get_pokemon(id: int):
    """
    gets Pokemon Sticker by real DexID
    :param id: Pokedex-ID of Pokemon
    :return: real Sticker"""
    id -= 1
    if id > 120:
        tempid = id - 120  # id minus stickerpack1
        global dex2
        return dex2.stickers[tempid]
    else:
        global dex1
        return dex1.stickers[id]


def get_forrestpath(left: bool, right: bool, up: bool, down: bool):
    """gets forrest-Path Sticker
    :return: real Sticker"""
    if not up and left and not right and not down:
        sticker = get_forrest(0)
    elif not up and not left and right and not down:
        sticker = get_forrest(1)
    elif up and not left and not right and not down:
        sticker = get_forrest(2)
    elif not up and not left and not right and down:
        sticker = get_forrest(3)

    elif not up and left and right and not down:
        sticker = get_forrest(4)
    elif up and not left and not right and down:
        sticker = get_forrest(5)
    elif up and left and not right and not down:
        sticker = get_forrest(6)
    elif not up and left and not right and down:
        sticker = get_forrest(7)
    elif up and not left and right and not down:
        sticker = get_forrest(8)
    elif not up and not left and right and down:
        sticker = get_forrest(9)
    elif not up and left and right and down:
        sticker = get_forrest(10)
    elif up and left and not right and down:
        sticker = get_forrest(11)
    elif up and left and right and not down:
        sticker = get_forrest(12)
    elif up and not left and right and down:
        sticker = get_forrest(13)
    elif left and up and down and right:
        sticker = get_forrest(14)
    else:
        sticker = get_forrest(15)

    return sticker

def get_forrest(id: int):
    """gets forrest-Sticker by ID
    :return: real Sticker"""
    global forrest
    return forrest.stickers[id]

def get_cavepath(left: bool, right: bool, up: bool, down: bool):
    """gets forrest-Path Sticker
    :return: real Sticker"""
    if not up and left and not right and not down:
        sticker = get_cave(0)
    elif not up and not left and right and not down:
        sticker = get_cave(1)
    elif up and not left and not right and not down:
        sticker = get_cave(2)
    elif not up and not left and not right and down:
        sticker = get_cave(3)

    elif not up and left and right and not down:
        sticker = get_cave(4)
    elif up and not left and not right and down:
        sticker = get_cave(5)
    elif up and left and not right and not down:
        sticker = get_cave(6)
    elif not up and left and not right and down:
        sticker = get_cave(7)
    elif up and not left and right and not down:
        sticker = get_cave(8)
    elif not up and not left and right and down:
        sticker = get_cave(9)
    elif not up and left and right and down:
        sticker = get_cave(10)
    elif up and left and not right and down:
        sticker = get_cave(11)
    elif up and left and right and not down:
        sticker = get_cave(12)
    elif up and not left and right and down:
        sticker = get_cave(13)
    elif left and up and down and right:
        sticker = get_cave(14)
    else:
        sticker = get_cave(15)

    return sticker

def get_cave(id: int):
    """gets forrest-Sticker by ID
    :return: real Sticker"""
    global cave
    return cave.stickers[id]

def get_starter(id: int):
    """gets Starter-Sticker by ID
    :return: real Sticker"""
    global starter
    return starter.stickers[id]

def get_item(id: int):
    """gets Item-Sticker by ID
    :return: real Sticker"""
    global items
    return items.stickers[id]


def item():
    """get item"""
    global items
    return items
