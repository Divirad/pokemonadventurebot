import re
from time import sleep
import requests
import json

from import_data import import_json


def gethtml(link):
    tries = 0
    html = None
    while tries < 5:
        try:
            html = requests.get(link, timeout=1).text
        except requests.exceptions.Timeout:
            sleep(1)
            tries += 1
        else:
            break
    if tries == 5:
        raise requests.exceptions.Timeout("'%s' timed out" % link)
    else:
        return html


def download_data():
    smogon_site = gethtml("http://www.smogon.com/dex/rb/pokemon/")
    smogon_dex = re.search(r'<script type="text/javascript">\W*dexSettings = (.*)\W*</script>\W*</head>', smogon_site)\
        .group(1)
    add_data = read_pokemon_db()
    learnable_moves, yellow_moves, prior_moves, other_moves = get_learnable_moves(add_data)
    check_learnable_moves(add_data, learnable_moves, yellow_moves, prior_moves, other_moves)
    return import_json(json.loads(smogon_dex), add_data, get_catch_rates(), learnable_moves)


def check_learnable_moves(names, learnable_moves, yellow_moves, prior_moves, other_moves):
    exceptions = [("Oddish", "Leech Seed"), ("Gloom", "Leech Seed"), ("Vileplume", "Leech Seed"),
                  ("Tentacool", "Confuse Ray"), ("Tentacruel", "Confuse Ray"),
                  ("Ponyta", "Low Kick"), ("Rapidash", "Low Kick"),
                  ("Exeggutor", "Poison Powder")]

    for name in names:
        id = names[name][0]

        smogon_site = gethtml("http://www.smogon.com/dex/rb/pokemon/" + name.replace('♀', '-F').replace('♂', '-M'))
        smogon_dex = json.loads(re.search(r'<script type="text/javascript">\W*dexSettings = (.*)\W*</script>\W*</head>',
                                          smogon_site).group(1))
        try:
            moves_smogon = smogon_dex["injectRpcs"][2][1]["learnset"]
        except IndexError as err:
            print(err)
        moves_bulbapedia = learnable_moves[id]
        yellow_moves_bulbapedia = yellow_moves[id]
        prior_moves_bulbapedia = prior_moves[id]
        other_moves_bulbapedia = other_moves[id]

        for m_b in moves_bulbapedia:
            if (name, m_b[0]) in exceptions:
                break
            for m_s in moves_smogon:
                if m_b[0].replace('Hi ', 'High ').lower().replace('-', '').replace(' ', '') == m_s.lower().replace('-', '').replace(' ', ''):
                    break
            else:
                raise RuntimeError("Unequal moves for pokemon {}: {} not in smogon dex".format(id, m_b[0]))

        for m_s in moves_smogon:
            if (name, m_s) in exceptions:
                break
            for m_b in moves_bulbapedia + yellow_moves_bulbapedia + prior_moves_bulbapedia + other_moves_bulbapedia:
                if m_b[0].replace('Hi ', 'High ').lower().replace('-', '').replace(' ', '') == m_s.lower().replace('-', '').replace(' ', ''):
                    break
            else:
                raise RuntimeError("Unequal moves for pokemon {}: {} not in bulbapedia".format(id, m_s))


def get_learnable_moves(names):
    moves = {}
    yellow_moves = {}
    prior_moves = {}
    other_moves = {}

    for name in names:
        id = names[name][0]
        moves[id] = []
        yellow_moves[id] = []
        prior_moves[id] = []
        other_moves[id] = []

        site = gethtml(
          'https://bulbapedia.bulbagarden.net/wiki/{}_(Pok%C3%A9mon)/Generation_I_learnset#By_leveling_up'.format(name))

        iter = re.finditer(r'style="display:none">(\d+)</span>\d+\n</td>\n<td style="background:#FFFFFF; border:1px sol'
                           r'id #D8D8D8;"> .{0,3}<a href="/wiki/[^\(]*\(move\)" [^<>]*title="[^\(]* \(move\)"><span s'
                           r'tyle="color:#000;">([^<]*)</span>', site)
        for m in iter:
            if not m.group(1).isdigit():
                raise RuntimeError(
                    "Pokemon {} has invalid learnable move: '{}' with level '{}'".format(name, m.group(2), m.group(1)))
            moves[id].append((m.group(2), m.group(1), 0))

        iter = re.finditer(
            r'color:#000;"> (\d+)\n</td>\n<td style="background:#FFF; text-align:center; border:1px solid #D8D8D8; back'
            r'ground:#FFE57A; color:#000"> [^<]*\n</td>\n<td style="background:#FFF; border:1px solid #D8D8D8;"> .{0,3}<a'
            r' href="/wiki/[^(]*\(move\)" [^<>]*title="[^(]*\(move\)"><span style="color:#000;">([^<]*)</span></a>',
            site)
        for m in iter:
            if not m.group(1).isdigit():
                raise RuntimeError(
                    "Pokemon {} has invalid learnable move: '{}' with level '{}'".format(name, m.group(2), m.group(1)))
            moves[id].append((m.group(2), m.group(1), 0))

        iter = re.finditer(
            r'>(T?H?)M(\d+)</span></a>[^()]*\n</td>\n<td style="background:#FFFFFF; border:1px solid #D8D8D8;"> .{0,3}<a href'
            r'="/wiki/.*\(move\)" [^<>]*title="[^(]* \(move\)"><span style="color:#000;">([^<]*)</span></a>', site)
        for m in iter:
            if not m.group(2).isdigit():
                raise RuntimeError("Pokemon {} has invalid learnable move: '{}' with level '{}'".format(name, m.group(3), m.group(2)))
            moves[id].append((m.group(3), m.group(2), 1 if m.group(1)[0] == 'T' else 2))

        iter = re.finditer(
            r'>(T?H?)M(\d+)</span></a>.*Yellow.*\n</td>\n<td style="background:#FFFFFF; border:1px solid #D8D8D8;"> .{0'
            r',3}<a href="/wiki/.*\(move\)" [^<>]*title="[^(]* \(move\)"><span style="color:#000;">([^<]*)</span></a>',
            site)
        for m in iter:
            yellow_moves[id].append((m.group(3), m.group(2), 1 if m.group(1)[0] == 'T' else 2))

        iter = re.finditer(
            r'color:#000;"> N/A\n</td>\n<td style="background:#FFF; text-align:center; border:1px solid #D8D8D8; backgr'
            r'ound:#FFE57A; color:#000"> (\d*)\n</td>\n<td style="background:#FFF; border:1px solid #D8D8D8;"> .{0,3}<a'
            r' href="/wiki/[^(]*\(move\)" title="[^(]*\(move\)"><span style="color:#000;">([^<]*)</span></a>', site)
        for m in iter:
            yellow_moves[id].append((m.group(2), m.group(1), 0))

        iter = re.finditer(
            r'png" width="40" height="40" /></a>[^()]*</span>\n</td>\n<td style="background:#FFFFFF; border:1px solid #'
            r'D8D8D8;"> .{0,3}<a href="/wiki/[^(]*\(move\)" title="[^(]*\(move\)"><span style="color:#000;">([^<]*)</sp'
            r'an></a>', site)
        for m in iter:
            prior_moves[id].append((m.group(1), -1, -1))

        iter = re.finditer(
            r'</th></tr>\n<tr>\n<td style="background:#FFFFFF; border:1px solid #D8D8D8;"> .{0,3}<a href="/wiki/[^(]*\('
            r'move\)" [^<>]*title="([^(]*) \(move\)"><span style="color:#000;">[^<]*</span>', site)
        for m in iter:
            other_moves[id].append((m.group(1), -1, -1))  # Event moves

        iter = re.finditer(
            r'(Power</a>|</sup></b>)\n</td>\n<td style="background:#FFFFFF; border:1px solid #D8D8D8;"> <a href="/wiki/'
            r'[^(]*\(move\)" title="[^(]*\(move\)"><span style="color:#000;">([^<]*)</span></a>\n</td>', site)
        for m in iter:
            other_moves[id].append((m.group(2), -1, -1))  # Tutoring & Event moves

    return moves, yellow_moves, prior_moves, other_moves


def read_pokemon_db():
    add_data = {}

    site = gethtml('https://pokemondb.net/pokedex/game/firered-leafgreen')
    iter = re.finditer(
        r'<span class="infocard-tall "><a class="pkg " data-sprite=" pkgG1 n\d{1,3} \" href=\"(\/pokedex\/[-\w]*)\"><\/'
        r'a><br><small>#(\d{1,3})<\/small><br><a class="ent-name" href="\/pokedex\/[-\w]*">(.{0,12})<\/a><br><small cla'
        r'ss="aside"><a href="\/type\/\w*" class="itype \w*\">\w*<\/a>( &middot; <a href="\/type\/\w*" class="itype '
        r'\w*\">\w*<\/a>)?<\/small><\/span>',
        site)

    for m in iter:
        id = int(m.group(2))
        name = m.group(3)

        dex = gethtml('https://pokemondb.net/%s' % m.group(1))

        dextext = re.search(
            r'<table class="vitals-table"><tbody><tr> <th><span class="igame red">Red</span><br><span class="igame blue'
            r'">Blue</span></th> <td>(.*)</td></tr><tr> <th><span class="igame yellow">',
            dex).group(1)

        training_part = re.search(
            r'<th>Base EXP<\/th>\n<td>(\d{1,10})<\/td>\n<\/tr>\n<tr>\n<th>Growth Rate<\/th>\n<td>([ \w]*)<\/td>', dex)
        exp_base = training_part.group(1)
        growth_rate = training_part.group(2)

        add_data[name] = (id, dextext, exp_base, growth_rate)
    return add_data


def get_catch_rates():
    catchrates = {}
    site = gethtml('https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_catch_rate')
    iter = re.finditer(
        r'<tr>\n<th> (\d{3})\n<\/th>\n<td><a href="\/wiki\/.{1,18}\(Pok%C3%A9mon\)" title="(.{1,18})"><img alt=".{1,18}'
        r' src="\/\/cdn.bulbagarden.net\/upload\/.{10}\.png" width="40" height="40" \/><\/a>\n<\/td>\n<td> <a href="\/w'
        r'iki\/.{1,18}\(Pok%C3%A9mon\)" title=".{1,18} \(Pokémon\)">.{1,18}<\/a>\n<\/td>\n<td class="r"> (\d{1,4})',
        site)
    for m in iter:
        catchrates[int(m.group(1))] = m.group(3)
    return catchrates
