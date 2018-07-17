from database.db import Database

all_species = []
all_types = []
all_moves = []
all_growth_rates = []
all_move_effects = []


def unload_data():
    global all_species, all_types, all_moves, all_growth_rates, all_move_effects
    all_species = []
    all_types = []
    all_moves = []
    all_growth_rates = []
    all_move_effects = []


class CorruptedDataError(RuntimeError):
    pass


def get_const_data_from_database():
    global all_species, all_types, all_moves, all_growth_rates, all_move_effects
    with Database() as database:

        types_data = database.get_data_sorted("SELECT * FROM type ORDER BY id")
        i = 0
        for t_data in types_data:
            if i != t_data['id']:
                raise CorruptedDataError("database got corrupted table 'type'. No entry for id %d" % i)
            all_types.append(Type(t_data))
            i += 1

        effectives = database.get_data_sorted("SELECT * FROM type_efficiencies ORDER BY attack, defense")
        if len(effectives) != len(all_types) * len(all_types):
            raise CorruptedDataError("database got corrupted type_efficiencies. %d entries instead of expected %d entries" % (
                len(effectives), len(all_types) * len(all_types)))
        for e in effectives:
            all_types[e['attack']].effectives[all_types[e['defense']]] = e['effective']

        growth_rates_data = database.get_data_sorted("SELECT * FROM growth_rate ORDER BY id")
        i = 0
        for g_data in growth_rates_data:
            if i != g_data['id']:
                raise CorruptedDataError("database got corrupted table 'growth_rate'. No entry for id %d" % i)
            all_growth_rates.append(GrowthRate(g_data))
            i += 1

        species_data = database.get_data_sorted("SELECT * FROM pokespecies ORDER BY id")
        i = 1
        for s_data in species_data:
            if i != s_data['id']:
                raise CorruptedDataError("database got corrupted table 'pokespecies'. No entry for id %d" % i)
            all_species.append(Pokespecies(s_data))
            i += 1

        move_effect_data = database.get_data_sorted("SELECT * FROM move_effect ORDER BY id")
        i = 0
        for m_data in move_effect_data:
            if i != m_data['id']:
                raise CorruptedDataError("database got corrupted table 'move_effect'. No entry for id %d" % i)
            all_move_effects.append(MoveEffect(m_data))
            i += 1

        moves_data = database.get_data_sorted("SELECT * FROM move ORDER BY id")
        i = 0
        for m_data in moves_data:
            if i != m_data['id']:
                raise CorruptedDataError("database got corrupted table 'move'. No entry for id %d" % i)
            all_moves.append(Move(m_data))
            i += 1

        learnable_moves_data = database.get_data_sorted("SELECT * FROM learnable_moves ORDER BY species_id, level")
        for m_data in learnable_moves_data:
            all_species[m_data['species_id'] - 1].learnable_moves.append(LearnableMove(m_data))

        status_data = database.get_data_sorted("SELECT * FROM states ORDER BY id")
        for s_data in status_data:
            setattr(State, s_data['name'], s_data['id'])


class State(object):
    pass


class MoveEffect(object):
    def __init__(self, data):
        self.id = data['id']
        self.name = data['id']


class Move(object):
    def __init__(self, data):
        global all_types, all_move_effects
        self.id = data['id']
        self.name = data['name']
        self.type = all_types[data['type']]
        self.priority = data['priority']
        self.power = data['power']
        self.accuracy = data['accuracy']
        self.pp = data['pp']
        self.effect = all_move_effects[data['effect']] if data['effect'] is not None else None


class LearnableMove:
    def __init__(self, data):
        global all_moves
        self.move = all_moves[data['move_id']]
        self.learning_by = data['learning_by']
        self.level = data['level']


class Type(object):
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.is_physical = bool(data['is_physical'])
        self.effectives = {}


class GrowthRate(object):
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']


class Pokespecies(object):
    def __init__(self, data):
        global all_types, all_growth_rates

        self.id = data['id']
        self.type1 = all_types[data['type1']]
        self.type2 = all_types[data['type2']] if data['type2'] is not None else None
        self.name = data['name']
        self.catchrate = data['catchrate']
        self.pokedextext = data['pokedextext']
        self.hp_base = data['hp_base']
        self.attack_base = data['attack_base']
        self.defense_base = data['defense_base']
        self.special_base = data['special_base']
        self.speed_base = data['speed_base']
        self.exp_base = data['exp_base']
        self.growth_rate = all_growth_rates[data['growth_rate']]
        self.learnable_moves = []
        self.gender = data['gender']

    def get_last_moves(self, level):
        moves = []
        c = 0
        for m in reversed(self.learnable_moves):
            if c >= 4:
                break
            if m.learning_by == 0 and m.level <= level:
                moves.append(m.move)
                c += 1
        moves.reverse()
        return moves
