
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

def is_collision(tile_type):
    """Determine if a character cannot walk on a given tile type."""
    return tile_type in ["wall", "water"]#, "tree", "rock"]

def move_character(character, dx, dy, tile_map, all_characters, epsilon=1.0):
    """Move a character by a given amount and prevent it from colliding with walls or water."""
    new_x = character.x + dx
    new_y = character.y + dy

    nearby_tiles = get_nearby_tiles(tile_map, new_x, new_y, 2, epsilon)
    for tile in nearby_tiles:
        if is_collision(tile.type):
            return  # Character cannot move here, return without updating position

    for other_character in all_characters:
        if other_character is not character and abs(new_x - other_character.x) < epsilon and abs(new_y - other_character.y) < epsilon:
            return  # Character is too close to another character, return without updating position

    character.x = new_x
    character.y = new_y
