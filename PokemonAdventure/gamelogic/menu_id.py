from enum import IntEnum, unique, auto
import hashlib


@unique
class MenuId(IntEnum):
    def _generate_next_value_(name, start, count, last_values):
        hash_value = hashlib.md5(name.encode()).digest()
        # use first 4 bytes as id
        return int.from_bytes(hash_value[:4], byteorder="little", signed=True)

    CHOOSE_STARTER = auto()
    CHOOSE_IF_RENAME = auto()

    ENTER_NAME = auto()

    MAIN_MENU = auto()

    POKEMON_CENTER = auto()
    CENTER_HEAL_BLOCKER = auto()

    POKEDEX_SEARCH = auto()



