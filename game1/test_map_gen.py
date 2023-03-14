import noise
import random

# Map parameters
MAP_WIDTH = 30
MAP_HEIGHT = 20
TILE_SIZE = 1

# Perlin noise parameters
NOISE_SCALE = 20.0
OCTAVES = 6
PERSISTENCE = 0.5
LACUNARITY = 2.0

# Room parameters
MAX_ROOMS = 10
MIN_ROOM_SIZE = 4
MAX_ROOM_SIZE = 8

# Tile types
TILE_GRASS = "'"
TILE_DIRT = ","
TILE_WATER = "~"
TILE_WALL = "#"
TILE_FURNITURE = "+"
TILE_ITEM = "*"

# Initialize the map
map_data = [[TILE_GRASS for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]

def intersect(rect1, rect2):
    return (rect1[0] < rect2[0] + rect2[2] and
            rect1[0] + rect1[2] > rect2[0] and
            rect1[1] < rect2[1] + rect2[3] and
            rect1[1] + rect1[3] > rect2[1])

# Generate Perlin noise
for x in range(MAP_WIDTH):
    for y in range(MAP_HEIGHT):
        value = noise.snoise2(x/NOISE_SCALE, y/NOISE_SCALE, octaves=OCTAVES, persistence=PERSISTENCE, lacunarity=LACUNARITY)
        if value < -0.2:
            map_data[x][y] = TILE_WATER
        elif value < 0.3:
            map_data[x][y] = TILE_DIRT

# Generate rooms
rooms = []
for i in range(MAX_ROOMS):
    room_width = random.randint(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
    room_height = random.randint(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
    x = random.randint(0, MAP_WIDTH - room_width - 1)
    y = random.randint(0, MAP_HEIGHT - room_height - 1)
    new_room = (x, y, room_width, room_height)
    overlap = False
    for other_room in rooms:
        if intersect(new_room, other_room):
            overlap = True
            break
    if not overlap:
        rooms.append(new_room)
        # Carve out the room
        for x in range(new_room[0], new_room[0] + new_room[2]):
            for y in range(new_room[1], new_room[1] + new_room[3]):
                if x == new_room[0] or x == new_room[0] + new_room[2] - 1 or y == new_room[1] or y == new_room[1] + new_room[3] - 1:
                    map_data[x][y] = TILE_WALL
                else:
                    map_data[x][y] = TILE_GRASS

# Render the map
for y in range(MAP_HEIGHT):
    for ty in range(TILE_SIZE):
        for x in range(MAP_WIDTH):
            for tx in range(TILE_SIZE):
                print(map_data[x][y], end='')
            if map_data[x][y] == TILE_WALL:
                print(TILE_WALL, end='')
            else:
                print(' ', end='')
        print()
