import random
from noise import snoise2  # You need to install the noise module


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

    def generate_characters(self, num_characters=5, character_types=("elf", "goblin", "human")):
        characters = []
        for _ in range(num_characters):
            character_type = random.choice(character_types)
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            character = Character(character_type, x, y)
            characters.append(character)
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

if __name__ == "__main__":
    map_generator = TileMapGenerator(width=30, height=20, seed=1234)
    tile_map = map_generator.generate_map(water_level=0.4, tree_density=0.05, wall_density=0.1, rock_density=0.03)
    characters = map_generator.generate_characters(num_characters=5, character_types=("elf", "goblin", "human"))
    room = Room(tile_map, characters, map_generator.width, map_generator.height)

    # Print the map to the console
    for row in tile_map:
        print("".join([tile.type[0] for tile in row]))