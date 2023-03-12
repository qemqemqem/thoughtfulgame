import random
from noise import snoise2  # You need to install the noise module

from room_based.location_utils import *


class Room:
    def __init__(self, tile_map, characters, width, height):
        self.tile_map = tile_map
        self.characters = characters
        self.width = width
        self.height = height


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


class TileMapGenerator:
    def __init__(self, width, height, seed=None):
        self.width = width
        self.height = height
        self.seed = seed if seed is not None else random.randint(0, 65535)

    def generate_map(self, water_level=0.4, tree_density=0.2, wall_density=0.05, rock_density=0.1):
        # Initialize the map with grass tiles
        tile_map = [[Tile(GRASS) for _ in range(self.width)] for _ in range(self.height)]

        # Generate the Perlin noise map for water placement
        water_map = [[snoise2(x / 20, y / 20, octaves=3, persistence=0.5, lacunarity=2.0, base=self.seed)
                      for x in range(self.width)] for y in range(self.height)]

        # Place water tiles based on the water map
        for y in range(self.height):
            for x in range(self.width):
                if water_map[y][x] > water_level:
                    tile_map[y][x] = Tile(WATER)

        # Place trees randomly
        for y in range(self.height):
            for x in range(self.width):
                if tile_map[y][x].type == GRASS and random.random() < tree_density:
                    tile_map[y][x] = Tile(TREE)

        # Place walls randomly
        for y in range(self.height):
            for x in range(self.width):
                if tile_map[y][x].type == GRASS and random.random() < wall_density:
                    tile_map[y][x] = Tile(WALL)

        # Place rocks randomly
        for y in range(self.height):
            for x in range(self.width):
                if tile_map[y][x].type == GRASS and random.random() < rock_density:
                    tile_map[y][x] = Tile(ROCK)

        return tile_map

    def wall_in_map(self, tile_map, door_size=1, north_exit=None, east_exit=None, south_exit=None, west_exit=None):
        width = len(tile_map[0])
        height = len(tile_map)

        for x in range(width):
            # Add north and south walls
            if north_exit is not None and (x < north_exit - door_size / 2 or x >= north_exit + door_size / 2):
                tile_map[0][x] = Tile(WALL)
            if south_exit is not None and (x < south_exit - door_size / 2 or x >= south_exit + door_size / 2):
                tile_map[height - 1][x] = Tile(WALL)

        for y in range(height):
            # Add east and west walls
            if west_exit is not None and (y < west_exit - door_size / 2 or y >= west_exit + door_size / 2):
                tile_map[y][0] = Tile(WALL)
            if east_exit is not None and (y < east_exit - door_size / 2 or y >= east_exit + door_size / 2):
                tile_map[y][width - 1] = Tile(WALL)

    def generate_characters(self, tile_map, num_characters=5, character_types=("elf", "goblin", "human")):
        characters = []
        for _ in range(num_characters):
            character_type = random.choice(character_types)
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            while True:
                x = random.uniform(0, self.width)
                y = random.uniform(0, self.height)
                nearby_tiles = get_nearby_tiles(tile_map, x, y, epsilon=1.0)
                if all(not tile.type.blocks_movement for tile in nearby_tiles):
                    character = Character(character_type, x, y)
                    characters.append(character)
                    break
        return characters

class Character:
    def __init__(self, character_type, x, y):
        self.type = character_type
        self.x = x
        self.y = y
        self.vx = 0  # velocity in the x direction
        self.vy = 0  # velocity in the y direction
