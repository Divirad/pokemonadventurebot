from enum import Enum, unique, auto
import hashlib
from base64 import b64encode


ID_LENGTH = 3

@unique
class ButtonId(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return str(b64encode(hashlib.md5(name.encode()).digest()))[2:ID_LENGTH+2]

    @classmethod
    def from_string(cls, s: str) -> 'ButtonId':
        return ButtonId(s[0:ID_LENGTH])

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)

    def __str__(self):
        return self.value

    def __add__(self, other) -> str:
        return str(self) + other

    CHOOSE_STARTER = auto()
    SWITCH_TO_STARTER = auto()

    SWITCH_TO_CHARMANDER = SWITCH_TO_STARTER + "0"
    SWITCH_TO_SQUIRTLE = SWITCH_TO_STARTER + "1"
    SWITCH_TO_BULBASAUR = SWITCH_TO_STARTER + "2"

    CHOOSE_CHARMANDER = CHOOSE_STARTER + "3"
    CHOOSE_SQUIRTLE = CHOOSE_STARTER + "6"
    CHOOSE_BULBASAUR = CHOOSE_STARTER + "0"

    NONE = "___"

    YES_RENAME = auto()
    NO_RENAME = auto()

    MAINMENU = auto()

    POKEDEX_FLIP = auto()
    POKEDEX_SWITCH_PAGE = auto()

    POKEDEX_PLS = POKEDEX_SWITCH_PAGE + "pls"
    POKEDEX_MIN = POKEDEX_SWITCH_PAGE + "min"

    POKEDEX_PAGES = auto()
    POKEDEX_SEARCH = auto()
    POKEDEX_MOREINFO = auto()
    POKEDEX_EXIT_SEARCH = auto()

    MENU_PROFILE = auto()
    MENU_GOOUT = auto()
    MENU_DAILY = auto()
    MENU_INFO = auto()

    DAILY_DONATE = auto()
    DAILY_REWARD = auto()

    DONATE_PAYPAL = auto()
    DONATE_BTC = auto()
    DONATE_ETH = auto()
    DONATE_LTC = auto()

    PROFILE_POKEMON = auto()
    PROFILE_POKEDEX = auto()
    PROFILE_BAG = auto()
    PROFILE_TRAINERCARD = auto()

    INFO_ABOUT = auto()
    INFO_NEWS = auto()

    GOOUT_WALK = auto()

    WALK_LEFT = auto()
    WALK_RIGHT = auto()
    WALK_UP = auto()
    WALK_DOWN = auto()
    WALK_INTERACT = auto()
    WALK_WARP = auto()
    WALK_INFO = auto()

    GOOUT_CENTER = auto()
    GOOUT_SHOP = auto()
    GOOUT_GYMS = auto()

    SHOP_BALLS = auto()
    SHOP_BALLS_MIN = SHOP_BALLS + "min"
    SHOP_BALLS_PLS = SHOP_BALLS + "pls"
    SHOP_BALLS_BUY = auto()

    SHOP_POTIONS = auto()
    SHOP_POTIONS_MIN = SHOP_POTIONS + "min"
    SHOP_POTIONS_PLS = SHOP_POTIONS + "pls"
    SHOP_POTIONS_BUY = auto()