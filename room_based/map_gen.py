import random
import threading
from noise import snoise2  # You need to install the noise module

from gpt.file_cache_manager import StringCache
from room_based.location_utils import *
from room_based.map_data import *
from room_based.location_utils import *
from gpt.gpt import *

string_cache = StringCache(cache_file="../gpt/cache.json")

class TileMapGenerator:
    def __init__(self, room, seed=None):
        self.room: Room = room
        self.width: int = room.width
        self.height: int = room.height
        self.seed = seed if seed is not None else random.randint(0, 65535)
        self.water_scale: int = 100
        self.tree_scale: int = 50

    def generate_map(self, room: Room, water_level=0.1, tree_density=0.9, wall_density=0.05, rock_density=0.1, forest_level=.4):
        # Initialize the map with grass tiles
        tile_map = [[Tile(GRASS) for _ in range(self.width)] for _ in range(self.height)]

        # Generate the Perlin noise map for water placement
        water_map = [[snoise2((self.room.room_pos.x*self.room.width+x) / self.water_scale, (-self.room.room_pos.y*self.room.height+y) / self.water_scale, octaves=4, persistence=0.5, lacunarity=2, base=1089234) for x in range(self.width)] for y in range(self.height)]

        tree_map = [[snoise2((self.room.room_pos.x*self.room.width+x-987141) / self.tree_scale, (-self.room.room_pos.y*self.room.height+y+81720) / self.tree_scale, octaves=3, persistence=0.5, lacunarity=2.0, base=1089234) for x in range(self.width)] for y in range(self.height)]

        # Place water tiles based on the water map
        for y in range(self.height):
            for x in range(self.width):
                if water_map[y][x] < water_level:
                    tile_map[y][x] = Tile(WATER, room.biome.format_name(random.choice(self.room.biome.water_images)))

        # Place trees randomly
        for y in range(self.height):
            for x in range(self.width):
                if tile_map[y][x].type == GRASS and abs(tree_map[y][x]) < forest_level and random.random() < tree_density:
                    tile_map[y][x] = Tile(TREE, room.biome.format_name(random.choice(self.room.biome.tree_images)))

        # Place walls randomly
        for y in range(self.height):
            for x in range(self.width):
                if tile_map[y][x].type == GRASS and random.random() < wall_density:
                    tile_map[y][x] = Tile(WALL, room.biome.format_name(random.choice(self.room.biome.wall_images)))

        # Place rocks randomly
        for y in range(self.height):
            for x in range(self.width):
                if tile_map[y][x].type == GRASS and random.random() < rock_density:
                    tile_map[y][x] = Tile(ROCK, room.biome.format_name(random.choice(self.room.biome.rock_images)))

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

    def generate_characters(self, room: Room, num_characters=5, character_types=None):
        if character_types is None:
            character_types = [room.biome.format_name(ch) for ch in room.biome.monster_types]
        characters = []
        for _ in range(num_characters):
            character_type = random.choice(character_types)
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            for _ in range(100):
                x = random.uniform(0, self.width)
                y = random.uniform(0, self.height)
                nearby_tiles = get_nearby_tiles(room.tile_map, x, y, epsilon=1.0)
                if all(not tile.type.blocks_movement for tile in nearby_tiles):
                    character = Character(character_type, x, y, self.room)
                    character.description = string_cache.get(character_type)
                    characters.append(character)
                    break
        return characters

    def generate_items(self, room, num_items=5, item_types=None):
        if item_types is None:
            item_types = [room.biome.format_name(it) for it in room.biome.object_types]
        items = []
        for _ in range(num_items):
            item_type = random.choice(item_types)
            x = int(random.uniform(0, self.width))
            y = int(random.uniform(0, self.height))
            item = InanimateObject(item_type, x, y, self.room)
            item.description = string_cache.get(item_type)
            items.append(item)
        return items


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


def _room_description_helper(room: Room, map_data: MapData):
    prompt = "Here is a place with " + room.landscape_description + ".\nIt contains these things:\n"
    dedup = []
    for th in room.things:
        if th.type not in dedup:
            dedup.append(th.type)
            prompt += "A " + th.type + ": " + th.description + "\n"
    prompt += "\nPlease write a short one sentence description of this room in the style of JRR Tolkien."
    room.description = prompt_completion_chat(prompt, n=1, temperature=0.1)


def initialize_new_room(room: Room, map_data):
    room.initialized = True
    add_exits_to_room(room, map_data)
    map_generator = TileMapGenerator(room, seed=random.randint(0, 1000000))
    room.tile_map = map_generator.generate_map(room, water_level=room.biome.water_level, forest_level=room.biome.tree_level, tree_density=0.9, wall_density=0.0, rock_density=room.biome.rock_density)
    map_generator.wall_in_map(room.tile_map, WALL, room)
    room.characters = map_generator.generate_characters(room, num_characters=5)
    room.things = map_generator.generate_items(room, num_items=random.randint(2, 6))
    t = threading.Thread(target=_room_description_helper, args=(room, map_data))
    t.start()


def initialize_room_and_neighbors(room, map_data):
    initialize_new_room(room, map_data)
    for direction in (NORTH_DIR, EAST_DIR, SOUTH_DIR, WEST_DIR):
        adj_room, initialized = map_data.get_room(room.room_pos + direction)
        if adj_room is not None and not initialized:
            initialize_new_room(adj_room, map_data)
