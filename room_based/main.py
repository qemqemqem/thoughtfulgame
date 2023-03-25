import pygame
import random

from room_based.map_data import *
from room_based.map_render import TileMapRenderer
from room_based.game_logic import Game
from room_based.map_gen import initialize_room_and_neighbors
from room_based.game_loop import main_game_loop
from utils.pygame_writer import PygameWriter
from room_based.think_gen import generate_thoughts
from room_based.config_loader import get_map_gen_config, create_cache_files_for_config

# Room dimensions, needed to initialize pygame
width = 30
height = 20
tile_size = 32

# Visual
extra_space_on_right = 300

# Initialize pygame first because it's used to load images
pygame.init()
writer = PygameWriter(lines_of_text=14)
screen = pygame.display.set_mode((width * tile_size + extra_space_on_right, height * tile_size + writer.text_space))
pygame.display.set_caption("Thoughtful Game")

# Generation
map_gen_config = get_map_gen_config()
create_cache_files_for_config(map_gen_config)
player = PlayerData()
map_data = MapData(map_gen_config, width, height)
room, _ = map_data.get_room(player.room_pos)
initialize_room_and_neighbors(room, map_data)
player.character = room.characters[0]  # The first character is the player character
player.character.player_character = True
generate_thoughts(player.character, room)
renderer = TileMapRenderer(writer, tile_size=tile_size, extra_space_on_right=extra_space_on_right)
game = Game(map_data, room)

main_game_loop(game, screen, renderer)

pygame.quit()