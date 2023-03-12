import pygame
import random

from map_gen import TileMapGenerator
from map_data import *
from map_render import TileMapRenderer
from game_logic import Game

# Room dimensions, needed to initialize pygame
width = 30
height = 20
tile_size = 32

# Initialize pygame first because it's used to load images
pygame.init()
screen = pygame.display.set_mode((width * tile_size, height * tile_size))
pygame.display.set_caption("Tile Map Renderer")

# Generation
player = PlayerData()
map_data = MapData(width, height)
room, _ = map_data.get_room(player.room_pos)
room.set_exits(random.randint(1,width-1), random.randint(1,height-1), random.randint(1,width-1), random.randint(1,height-1))
map_generator = TileMapGenerator(room, seed=random.randint(0, 1000000))
tile_map = map_generator.generate_map(water_level=0.35, tree_density=0.05, wall_density=0.0, rock_density=0.03)
map_generator.wall_in_map(tile_map, 2, room.north_exit, room.east_exit, room.south_exit, room.west_exit)
characters = map_generator.generate_characters(tile_map, num_characters=5, character_types=("elf", "goblin", "human"))
renderer = TileMapRenderer(tile_map, characters, tile_size=tile_size)
game = Game(room, tile_map, characters)

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the game state
    game.handle_input()
    game.update()

    # Render the tile map and characters
    screen.fill((0, 0, 0))
    renderer.render_map(screen)
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()