import json
import re


def jdefault(o):
    if type(o) is dict or type(o) is list:
        return o
    else:
        d = dict(o.__dict__)
        deletes = []
        for x in d:
            if re.match(r'__.*__', x) or re.match(r'by_name_.*', x):
                deletes.append(x)
        for x in deletes:
            del d[x]
        return d


def export_to_file(data, file):
    file.write(json.dumps(data, default=jdefault, indent=4))
    file.close()


def export_to_database(data, cursor):
    for t in data.types:
        cursor.execute("INSERT INTO type (id, name, is_physical) VALUES (%s, %s, %s)", (t.id, t.name, t.is_physical))

    for t in data.type_efficiencies:
        cursor.execute("INSERT INTO type_efficiencies (attack, defense, effective) VALUES (%s, %s, %s)",
                       (t.attack, t.defense, t.effective))

    for g in data.growth_rates:
        cursor.execute("INSERT INTO growth_rate (id, name) VALUES (%s, %s)", (g.id, g.name))

    for p in data.pokespecies:
        cursor.execute("INSERT INTO pokespecies (id, name, type1, type2, catchrate, pokedextext, hp_base, attack_base, "
                       "defense_base, special_base, speed_base, growth_rate, exp_base, gender) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (p.id, p.name, p.type1, p.type2, p.catchrate, p.pokedextext, p.hp_base, p.attack_base,
                        p.defense_base, p.special_base, p.speed_base, p.growth_rate, p.exp_base, p.gender))

    for m in data.move_effects:
        cursor.execute("INSERT INTO move_effect (id, name) VALUES (%s, %s)", (m.id, m.name))

    for m in data.moves:
        cursor.execute("INSERT INTO move (id, name, type, priority, power, accuracy, pp, effect) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                       (m.id, m.name, m.type, m.priority, m.power, m.accuracy, m.pp, m.effect))

    for l in data.learnable_moves:
        cursor.execute("INSERT INTO learnable_moves (species_id, move_id, learning_by, level) VALUES (%s, %s, %s, %s)",
                       (l.species_id, l.move_id, l.learning_by, l.level))

    for s in data.states:
        cursor.execute("INSERT INTO states (id, name) VALUES (%s, %s)", (s.id, s.name))
