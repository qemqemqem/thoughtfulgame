import random
from noise import snoise2  # You need to install the noise module

from room_based.location_utils import *
from map_data import *
from location_utils import *


class TileMapGenerator:
    def __init__(self, room, seed=None):
        self.room = room
        self.width = room.width
        self.height = room.height
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

    def wall_in_map(self, tile_map, wall_type=WALL, room=None, north_exit=None, east_exit=None, south_exit=None, west_exit=None, north_door_size=1, east_door_size=1, south_door_size=1, west_door_size=1):
        width = len(tile_map[0])
        height = len(tile_map)
        if room is not None:
            north_exit = room.north_exit
            east_exit = room.east_exit
            south_exit = room.south_exit
            west_exit = room.west_exit
            north_door_size = room.north_door_size
            east_door_size = room.east_door_size
            south_door_size = room.south_door_size
            west_door_size = room.west_door_size

        for x in range(width):
            # Add north and south walls
            if north_exit is None or (x < north_exit - north_door_size / 2 or x >= north_exit + north_door_size / 2):
                tile_map[0][x] = Tile(wall_type)
            if south_exit is None or (x < south_exit - south_door_size / 2 or x >= south_exit + south_door_size / 2):
                tile_map[height - 1][x] = Tile(wall_type)

        for y in range(height):
            # Add east and west walls
            if west_exit is None or (y < west_exit - west_door_size / 2 or y >= west_exit + west_door_size / 2):
                tile_map[y][0] = Tile(wall_type)
            if east_exit is None or (y < east_exit - east_door_size / 2 or y >= east_exit + east_door_size / 2):
                tile_map[y][width - 1] = Tile(wall_type)

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


def add_exits_to_room(room: Room, map_data: MapData, door_chance=1.0):
    if len(map_data.rooms) == 1:
        # The first room has 4 exits
        room.set_exits(random.randint(1, room.width - 1), random.randint(1, room.height - 1), random.randint(1, room.width - 1), random.randint(1, room.height - 1))
        return
    north_exit = None if random.random() > door_chance else random.randint(1, room.width - 1)
    east_exit = None if random.random() > door_chance else random.randint(1, room.height - 1)
    south_exit = None if random.random() > door_chance else random.randint(1, room.width - 1)
    west_exit = None if random.random() > door_chance else random.randint(1, room.height - 1)
    north_exit = map_data.get_room(room.room_pos + NORTH_DIR)[0].south_exit if map_data.has_room(room.room_pos + NORTH_DIR) else north_exit
    east_exit = map_data.get_room(room.room_pos + EAST_DIR)[0].west_exit if map_data.has_room(room.room_pos + EAST_DIR) else east_exit
    south_exit = map_data.get_room(room.room_pos + SOUTH_DIR)[0].north_exit if map_data.has_room(room.room_pos + SOUTH_DIR) else south_exit
    west_exit = map_data.get_room(room.room_pos + WEST_DIR)[0].east_exit if map_data.has_room(room.room_pos + WEST_DIR) else west_exit
    room.set_exits(north_exit, east_exit, south_exit, west_exit)


def initialize_new_room(room, map_data):
    add_exits_to_room(room, map_data)
    map_generator = TileMapGenerator(room, seed=random.randint(0, 1000000))
    room.tile_map = map_generator.generate_map(water_level=0.35, tree_density=0.05, wall_density=0.0, rock_density=0.03)
    map_generator.wall_in_map(room.tile_map, WALL, room)
    room.characters = map_generator.generate_characters(room.tile_map, num_characters=5,
                                                        character_types=("elf", "goblin", "human"))
