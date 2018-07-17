import json
import data


def read_list(lst, type):
    result = []
    for l in lst:
        t = type()
        for k, v in l.items():
            setattr(t, k, v)
        result.append(t)
    return result


def load_data(file):
    raw = json.load(file)

    result = data.Data()
    result.pokespecies = read_list(raw["pokespecies"], data.Pokespecies)
    result.types = read_list(raw["types"], data.Type)
    result.type_efficiencies = read_list(raw["type_efficiencies"], data.TypeEfficiency)
    result.growth_rates = read_list(raw["growth_rates"], data.GrowthRate)
    result.moves = read_list(raw["moves"], data.Move)
    result.move_effects = read_list(raw["move_effects"], data.MoveEffect)
    result.learnable_moves = read_list(raw["learnable_moves"], data.LearnableMove)
    result.states = read_list(raw["states"], data.State)

    return result
