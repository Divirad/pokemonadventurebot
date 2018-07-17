from gamelogic.math import Vector2d


class EVENT(enumerate):
    NONE = 0
    WILD_POKEMON = 1
    ITEM = 2


class DATA(enumerate):
    TYPE = 0
    NAME = 1


class WAYTYPE:
    NONE = None
    FOREST = 0
    CITY = 1
    CAVE = 2
    WATER = 3
    VICTORYROAD = 4
    MANSION = 5
    POKETOWER = 6
    POWERPLANT = 7
    SAFARIZONE = 8


class DIRECTION_VECTORS():
    LEFT = Vector2d(-1, 0)
    RIGHT = Vector2d(1, 0)
    UP = Vector2d(0, 1)
    DOWN = Vector2d(0, -1)

class DIRECTION(enumerate):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
