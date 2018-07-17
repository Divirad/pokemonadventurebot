
class Data:
    def __init__(self):
        self.pokespecies = []
        self.types = []
        self.type_efficiencies = []
        self.growth_rates = []
        self.moves = []
        self.move_effects = []
        self.learnable_moves = []
        self.states = []

        self.by_name_types = {}
        self.by_name_moves = {}
        self.by_name_move_effects = {}
        self.by_name_growth_rates = {}


class State:
    def __init__(self):
        self.id = None
        self.name = None


class Type:
    def __init__(self):
        self.id = None
        self.name = None
        self.is_physical = None


class TypeEfficiency:
    def __init__(self):
        self.attack = None
        self.defense = None
        self.effective = None


class GrowthRate:
    def __init__(self):
        self.id = None
        self.name = None


class Pokespecies:
    def __init__(self):
        self.id = None
        self.type1 = None
        self.type2 = None
        self.name = None
        self.catchrate = None
        self.pokedextext = None
        self.hp_base = None
        self.attack_base = None
        self.defense_base = None
        self.special_base = None
        self.speed_base = None
        self.exp_base = None
        self.growth_rate = None
        self.gender = None


class MoveEffect:
    def __init__(self):
        self.id = None
        self.name = None


class Move:
    def __init__(self):
        self.id = None
        self.name = None
        self.type = None
        self.priority = None
        self.power = None
        self.accuracy = None
        self.pp = None
        self.effect = None


class LearnableMove:
    def __init__(self):
        self.species_id = None
        self.move_id = None
        self.learning_by = None
        self.level = None
