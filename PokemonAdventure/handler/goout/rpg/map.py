import json
from handler.goout.rpg.location import Location
from private import map_file

class Map():
    def __init__(self, path: str):
        self.map = []

        mapfile = open(path).read()
        data = None
        try:
            data = json.loads(mapfile)

        except json.JSONDecodeError as e:
            # TODO log:
            print("Error in Loading the map because of: "+ e.msg)

        i = 0
        for l in data["locations"]:
            if i is not l["id"]:
                raise ValueError('locations are not sorted and dont match the ID!')

            self.map.append(Location(id = l["id"],
                                     name = l["name"],
                                     width = l["width"],
                                     height = l["height"],
                                     description = l["description"],
                                     fields = l["fields"]))
            i += 1

    def get_location_by_id(self, id: int) -> Location:
        return self.map[id]

    def test(self):
        print("test")

def load_map():
    global map
    map = Map(map_file)

def get_map() -> Map:
    global map
    return map