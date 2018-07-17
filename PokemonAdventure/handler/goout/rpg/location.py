from gamelogic.math import Array2d

class Tile:
    def __init__(self, x: int, y: int, type: int = None, spawn_to = None):
        if spawn_to is not None:
            self.spawn_on = spawn_to
        self.x = x
        self.y = y
        self.type = type


class Location:
    def __init__(self, id:int, name: str, width: int, height: int, description: str, fields):
        self.id = id
        self.name = name
        self.width = width
        self.description = description

        self.fields = Array2d(width + 1 ,height + 1)

        for f in fields:
            porter = None

            if "linkedTo" in f:
                porter = Tile(f["linkedTo"]["spawn_x"], f["linkedTo"]["spawn_y"], spawn_to = f["linkedTo"]["spawn_map"])
            tile = Tile(f["x"], f["y"], f["type"],spawn_to = porter)

            self.fields.set(f["x"], f["y"], tile)

    def get_tile(self, x:int, y:int) -> Tile:
        return self.fields.get(x, y)

    def can_walk(self,x:int, y:int) -> bool:
        if x < 0 or y < 0:
            return False
        elif self.fields.get(x, y) is not None:
            return True
        else:
            return False