from utils.vec2i import Vec2i

NORTH_DIR = Vec2i(0, 1)
EAST_DIR = Vec2i(1, 0)
SOUTH_DIR = Vec2i(0, -1)
WEST_DIR = Vec2i(-1, 0)


def get_nearby_tiles(tile_map, x, y, radius:int=2, epsilon=0.5):
    """Get all the tiles within a given radius around a point."""
    nearby_tiles = []
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            tile_x = int(x + dx + 0.5)
            tile_y = int(y + dy + 0.5)
            if 0 <= tile_x < len(tile_map[0]) and 0 <= tile_y < len(tile_map):
                if abs(x - tile_x) < epsilon and abs(y - tile_y) < epsilon:
                    nearby_tiles.append(tile_map[tile_y][tile_x])
    return nearby_tiles


def move_character(character, dx, dy, tile_map, all_characters, epsilon=0.8):
    """Move a character by a given amount and prevent it from colliding with walls or water."""
    new_x = character.x + dx
    new_y = character.y + dy

    nearby_tiles = get_nearby_tiles(tile_map, new_x, new_y, 2, epsilon)
    for tile in nearby_tiles:
        if tile.type.blocks_movement:
            return  # Character cannot move here, return without updating position

    for other_character in all_characters:
        if other_character is not character and abs(new_x - other_character.x) < epsilon and abs(new_y - other_character.y) < epsilon:
            return  # Character is too close to another character, return without updating position

    character.x = new_x
    character.y = new_y


def is_character_in_doorway(character, room):
    # North exit
    if room.north_exit is not None and character.vy < 0 and abs(character.y - 0) < 0.5 and room.north_exit - room.north_door_size / 2 <= character.x < room.north_exit + room.north_door_size / 2:
        return True, NORTH_DIR
    # East exit
    if room.east_exit is not None and character.vx > 0 and abs(character.x - room.width) < 1.5 and room.east_exit - room.east_door_size / 2 <= character.y < room.east_exit + room.east_door_size / 2:
        return True, EAST_DIR
    # South exit
    if room.south_exit is not None and character.vy > 0 and abs(character.y - room.height) < 1.5 and room.south_exit - room.south_door_size / 2 <= character.x < room.south_exit + room.south_door_size / 2:
        return True, SOUTH_DIR
    # West exit
    if room.west_exit is not None and character.vx < 0 and abs(character.x - 0) < 0.5 and room.west_exit - room.west_door_size / 2 <= character.y < room.west_exit + room.west_door_size / 2:
        return True, WEST_DIR
    return False, Vec2i(0, 0)