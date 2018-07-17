
import data


def import_json(raw_data, add_data, catch_rates, learnable_moves):
    result = data.Data()
    dex = raw_data["injectRpcs"][1][1]

    load_types(result, dex["types"])
    load_growth_rates(result, add_data)
    load_pokemon(result, dex["pokemon"], add_data, catch_rates)
    load_move_effects(result, dex["moves"])
    load_moves(result, dex["moves"])
    load_learnable_moves(result, learnable_moves)
    load_stats(result)

    return result


def load_stats(result):
    stat0 = data.State()
    stat0.id = 0
    stat0.name = "Healthy"
    result.states.append(stat0)
    stat1 = data.State()
    stat1.id = 1
    stat1.name = "Asleep1"
    result.states.append(stat1)
    stat2 = data.State()
    stat2.id = 2
    stat2.name = "Asleep2"
    result.states.append(stat2)
    stat3 = data.State()
    stat3.id = 3
    stat3.name = "Poisoned"
    result.states.append(stat3)
    stat4 = data.State()
    stat4.id = 4
    stat4.name = "Burned"
    result.states.append(stat4)
    stat5 = data.State()
    stat5.id = 5
    stat5.name = "Frozen"
    result.states.append(stat5)
    stat6 = data.State()
    stat6.id = 6
    stat6.name = "Paralyzed"
    result.states.append(stat6)
    stat7 = data.State()
    stat7.id = 7
    stat7.name = "Badly Poisoned"  # mabye unused, not real pokemon state
    result.states.append(stat7)


def load_move_effects(result, move_data):
    id = 0
    for m in move_data:
        effect = data.MoveEffect()
        effect.id = id
        effect.name = m["description"]
        result.move_effects.append(effect)
        result.by_name_move_effects[effect.name] = effect
        id += 1


def load_moves(result, move_data):
    id = 0
    for m in move_data:
        move = data.Move()
        move.name = m["name"]
        move.type = result.by_name_types[m["type"]].id
        move.accuracy = m["accuracy"]
        move.pp = m["pp"]
        move.power = m["power"]
        move.priority = 1 if move.name == "Quick Attack" else -1 if move.name == "Counter" else 0
        move.effect = result.by_name_move_effects[m["description"]].id
        move.id = id
        result.by_name_moves[move.name.replace('Hi ', 'High ').lower().replace('-', '').replace(' ', '')] = move
        result.moves.append(move)
        id += 1


def load_types(result, raw_types):
    id = 0
    for raw_type in raw_types:
        type = data.Type()
        type.name = raw_type["name"]
        type.id = id
        type.is_physical = type.name in ["Bug", "Fighting", "Flying", "Ghost", "Ground", "Normal", "Poison", "Rock"]
        if not type.is_physical and type.name not in ["Dragon", "Electric", "Fire", "Grass", "Ice", "Psychic", "Water"]:
            raise RuntimeError("Unsupported type: " + type.name)
        result.types.append(type)
        result.by_name_types[type.name] = type
        id += 1

    for t in raw_types:
        for e in t["atk_effectives"]:
            efficiency = data.TypeEfficiency()
            efficiency.attack = result.by_name_types[t["name"]].id
            efficiency.defense = result.by_name_types[e[0]].id
            efficiency.effective = e[1]
            result.type_efficiencies.append(efficiency)


def load_growth_rates(result, add_data):
    id = 0
    for d in add_data.values():
        g = d[3]
        if g not in result.by_name_growth_rates:
            growth_rate = data.GrowthRate()
            growth_rate.name = g
            growth_rate.id = id
            result.growth_rates.append(growth_rate)
            result.by_name_growth_rates[g] = growth_rate
            id += 1


def load_pokemon(result, raw_pokemon, id_data, catch_rates):
    for raw_poke in raw_pokemon:
        if "RB" not in raw_poke["genfamily"]:
            continue
        poke = data.Pokespecies()
        poke.name = raw_poke["name"].replace('-F', '♀').replace('-M', '♂')
        infos = raw_poke["alts"][0]
        poke.defense_base = infos["def"]
        poke.hp_base = infos["hp"]
        poke.attack_base = infos["atk"]
        poke.special_base = infos["spd"]
        poke.speed_base = infos["spe"]
        poke.type1 = result.by_name_types[infos["types"][0]].id
        poke.type2 = None if len(infos["types"]) <= 1 else result.by_name_types[infos["types"][1]].id
        if poke.name not in id_data:
            raise RuntimeError("Pokemon name error: " + poke.name)
        add_data = id_data[poke.name]
        poke.id = add_data[0]
        poke.pokedextext = add_data[1]
        poke.exp_base = add_data[2]
        poke.growth_rate = result.by_name_growth_rates[add_data[3]].id
        poke.catchrate = catch_rates[poke.id]
        result.pokespecies.append(poke)


def load_learnable_moves(result, learnable_moves):
    for id, moves in learnable_moves.items():
        for move in moves:
            learnable_move = data.LearnableMove()
            learnable_move.species_id = id
            move_name = move[0].replace('Hi ', 'High ').lower().replace('-', '').replace(' ', '')
            if move_name not in result.by_name_moves:
                raise RuntimeError("Move name error: {} not in {}".format(move[0], result.by_name_moves.keys()))
            learnable_move.move_id = result.by_name_moves[move_name].id
            learnable_move.level = int(move[1])
            learnable_move.learning_by = move[2]
            result.learnable_moves.append(learnable_move)
