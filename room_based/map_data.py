
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
    def __init__(self, character_type, x, y):
        self.type = character_type
        self.x = x
        self.y = y
        self.vx = 0  # velocity in the x direction
        self.vy = 0  # velocity in the y direction


class Room:
    def __init__(self, width, height):
        self.tile_map = None
        self.characters = []
        self.width = width
        self.height = height
        self.north_exit = None
        self.east_exit = None
        self.south_exit = None
        self.west_exit = None

    def set_exits(self, north_exit=None, east_exit=None, south_exit=None, west_exit=None):
        self.north_exit = north_exit
        self.east_exit = east_exit
        self.south_exit = south_exit
        self.west_exit = west_exit


class MapData:
    def __init__(self):
        self.rooms: dict[Vec2i, Room] = {}