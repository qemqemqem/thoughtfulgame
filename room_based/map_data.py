# DON'T DEPEND ON ANY NON-DATA FILES FROM HERE

from vec2i import Vec2i


class TileType:
    def __init__(self, name, blocks_movement):
        self.name = name
        self.blocks_movement = blocks_movement


GRASS = TileType("grass", False)
WATER = TileType("water", True)
TREE = TileType("tree", False)
WALL = TileType("wall", True)
ROCK = TileType("rock", False)


class Tile:
    def __init__(self, tile_type):
        self.type = tile_type


class Character:
    def __init__(self, character_type, x, y, room):
        self.type = character_type
        self.x = x
        self.y = y
        self.vx = 0  # velocity in the x direction
        self.vy = 0  # velocity in the y direction
        self.player_character = False
        self.room = room


class Room:
    def __init__(self, width, height):
        self.tile_map = None
        self.characters = []
        self.width = width
        self.height = height
        self.room_pos = None

        # Exits
        self.north_exit = None
        self.east_exit = None
        self.south_exit = None
        self.west_exit = None
        self.north_door_size = 1
        self.east_door_size = 1
        self.south_door_size = 1
        self.west_door_size = 1
        self.set_all_door_sizes(2)

    def set_all_door_sizes(self, door_size):
        self.north_door_size = door_size
        self.east_door_size = door_size
        self.south_door_size = door_size
        self.west_door_size = door_size

    def set_exits(self, north_exit=None, east_exit=None, south_exit=None, west_exit=None):
        self.north_exit = north_exit
        self.east_exit = east_exit
        self.south_exit = south_exit
        self.west_exit = west_exit


class PlayerData:
    def __init__(self, room_pos:Vec2i=None, character=None):
        if room_pos is None:
            room_pos = Vec2i(0, 0)
        self.room_pos = room_pos
        self.character = character


class MapData:
    def __init__(self, default_room_width=16, default_room_height=10):
        self.default_room_width = default_room_width
        self.default_room_height = default_room_height
        self.rooms: dict[Vec2i, Room] = {}

    def get_room(self, room_pos:Vec2i):
        initialized = True
        if room_pos not in self.rooms:
            self.rooms[room_pos] = Room(self.default_room_width, self.default_room_height)
            self.rooms[room_pos].room_pos = room_pos
            initialized = False
        return self.rooms[room_pos], initialized


    def has_room(self, room_pos:Vec2i):
        return room_pos in self.rooms