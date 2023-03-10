import pygame
import random

from map_data import *
from map_render import TileMapRenderer
from game_logic import Game
from map_gen import initialize_room_and_neighbors
from game_loop import main_game_loop
from utils.pygame_writer import PygameWriter
from think_gen import generate_thoughts

# Room dimensions, needed to initialize pygame
width = 30
height = 20
tile_size = 32

# Initialize pygame first because it's used to load images
pygame.init()
writer = PygameWriter(lines_of_text=14)
screen = pygame.display.set_mode((width * tile_size, height * tile_size + writer.text_space))
pygame.display.set_caption("Tile Map Renderer")

# Generation
player = PlayerData()
map_data = MapData(width, height)
room, _ = map_data.get_room(player.room_pos)
initialize_room_and_neighbors(room, map_data)
player.character = room.characters[0]  # The first character is the player character
player.character.player_character = True
generate_thoughts(player.character, room)
renderer = TileMapRenderer(writer, tile_size=tile_size)
game = Game(map_data, room)

main_game_loop(game, screen, renderer)

pygame.quit()