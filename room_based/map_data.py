# DON'T DEPEND ON ANY NON-DATA FILES FROM HERE
import random
import json

from room_based.thought_data import ThoughtBrain
from utils.vec2i import Vec2i


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
    def __init__(self, tile_type, asset_name = None):
        self.type = tile_type
        self.asset_name = asset_name

    def get_file_name(self):
        if self.asset_name is not None:
            return self.asset_name
        else:
            return self.type.name


class Character:
    def __init__(self, character_type, x, y, room):
        self.type = character_type
        self.x = x
        self.y = y
        self.vx = 0  # velocity in the x direction
        self.vy = 0  # velocity in the y direction
        self.player_character: bool = False
        self.room: Room = room
        self.description: str = ""
        self.thought_brain: ThoughtBrain = ThoughtBrain()


class InanimateObject:
    def __init__(self, object_type, x, y, room):
        self.type = object_type
        self.x = x
        self.y = y
        self.room = room
        self.description = ""


class Biome:
    def __init__(self, name):
        self.name = name
        self.monster_types: list[str] = []
        self.object_types: list[str] = []
        self.tree_images: list[str] = []
        self.rock_images: list[str] = []
        self.ground_images: list[str] = []
        self.water_images: list[str] = []
        self.wall_images: list[str] = []
        # "Level" here refers to a threshold for perlin noise
        self.tree_level: float = 0.4
        self.water_level: float = -0.4
        self.rock_density: float = 0.05

    def format_name(self, image_name):
        return "A " + image_name + " in the " + self.name


class MapGenConfig:
    def __init__(self):
        self.biomes: list[Biome] = []


class Room:
    def __init__(self, width, height, biome: Biome = None):
        if biome is None:
            biome = Biome("default")
        self.tile_map = None
        self.characters: list[Character] = []
        self.things: list[InanimateObject] = []
        self.biome = biome
        self.width = width
        self.height = height
        self.room_pos = None
        self.initialized = False
        self.description = "Use arrow keys to move, press Q to quit."
        self.landscape_description = random.choice(("a lot of trees", "a lot of rocks", "a lot of grass", "a lot of water"))

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

    def get_nearby(self, x, y, distance=1):
        nearby_characters = []
        for character in self.characters:
            if character.player_character:
                continue
            if abs(character.x - x) <= distance and abs(character.y - y) <= distance:
                nearby_characters.append(character)
        nearby_things = []
        for thing in self.things:
            if abs(thing.x - x) <= distance and abs(thing.y - y) <= distance:
                nearby_things.append(thing)
        return nearby_characters, nearby_things


class PlayerData:
    def __init__(self, room_pos:Vec2i=None, character=None):
        if room_pos is None:
            room_pos = Vec2i(0, 0)
        self.room_pos: Vec2i = room_pos
        self.character: Character = character


class MapData:
    def __init__(self, map_gen_config: MapGenConfig, default_room_width=16, default_room_height=10):
        self.map_gen_config = map_gen_config
        self.default_room_width = default_room_width
        self.default_room_height = default_room_height
        self.rooms: dict[Vec2i, Room] = {}

    def get_room(self, room_pos:Vec2i):
        initialized = True
        if room_pos not in self.rooms:
            self.rooms[room_pos] = Room(self.default_room_width, self.default_room_height, random.choice(self.map_gen_config.biomes))
            self.rooms[room_pos].room_pos = room_pos
            initialized = False
        elif not self.rooms[room_pos].initialized:
            initialized = False
        return self.rooms[room_pos], initialized


    def has_room(self, room_pos:Vec2i):
        return room_pos in self.rooms
