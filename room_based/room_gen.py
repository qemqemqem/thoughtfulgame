import random
from noise import snoise2  # You need to install the noise module

from room_based.location_utils import *


class Room:
    def __init__(self, tile_map, characters, width, height):
        self.tile_map = tile_map
        self.characters = characters
        self.width = width
        self.height = height


class TileMapGenerator:
    def __init__(self, width, height, seed=None):
        self.width = width
        self.height = height
        self.seed = seed if seed is not None else random.randint(0, 65535)

    def generate_map(self, water_level=0.4, tree_density=0.2, wall_density=0.05, rock_density=0.1):
        # Initialize the map with grass tiles
        tile_map = [[Tile("grass") for _ in range(self.width)] for _ in range(self.height)]

        # Generate the Perlin noise map for water placement
        water_map = [[snoise2(x / 20, y / 20, octaves=3, persistence=0.5, lacunarity=2.0, base=self.seed)
                      for x in range(self.width)] for y in range(self.height)]

        # Place water tiles based on the water map
        for y in range(self.height):
            for x in range(self.width):
                if water_map[y][x] > water_level:
                    tile_map[y][x] = Tile("water")

        # Place trees randomly
        for y in range(self.height):
            for x in range(self.width):
                if tile_map[y][x].type == "grass" and random.random() < tree_density:
                    tile_map[y][x] = Tile("tree")

        # Place walls randomly
        for y in range(self.height):
            for x in range(self.width):
                if tile_map[y][x].type == "grass" and random.random() < wall_density:
                    tile_map[y][x] = Tile("wall")

        # Place rocks randomly
        for y in range(self.height):
            for x in range(self.width):
                if tile_map[y][x].type == "grass" and random.random() < rock_density:
                    tile_map[y][x] = Tile("rock")

        return tile_map

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
                if all(not is_collision(tile.type) for tile in nearby_tiles):
                    character = Character(character_type, x, y)
                    characters.append(character)
                    break
        return characters

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
