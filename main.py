import pygame
import os
import random
import threading

from gpt import prompt_completion
from gpt_thoughts_prompter import generate_prompt_from_unknown_items
from thing_class import Thing
from thought_manager import ThoughtManager
from file_cache_manager import StringCache, DEFAULT_CACHE_FILE_NAME
from action_log_manager import ActionLogManager
from vec2i import Vec2i
# Initialize Pygame
pygame.init()

# Set the dimensions of the window
WINDOW_WIDTH = 800
FONT_SIZE = 32
TEXT_SPACE = FONT_SIZE * 12
WINDOW_HEIGHT = 600

# Define the size of each tile
TILE_SIZE = 64

# Create the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT + TEXT_SPACE))

# Set the title of the window
pygame.display.set_caption("RPG Map")

# Set up the clock
clock = pygame.time.Clock()

# Set up the font
font = pygame.font.Font(None, FONT_SIZE)

# Define the directory where the images are stored
IMAGE_DIR = "images/"

# Thinking Parameters
GENERATE_THOUGHT_EVERY = 4000
thought_man = ThoughtManager()

# Create the action log
action_logger = ActionLogManager()

# Load the character image
character_image = pygame.image.load(os.path.join(IMAGE_DIR, "character.png")).convert_alpha()
character_image = pygame.transform.scale(character_image, (TILE_SIZE, TILE_SIZE))

# Load the terrain images
terrain_images = {}
for image_file in os.listdir(IMAGE_DIR):
    if image_file != "character.png":
        terrain_image = pygame.image.load(os.path.join(IMAGE_DIR, image_file)).convert_alpha()
        terrain_image = pygame.transform.scale(terrain_image, (TILE_SIZE, TILE_SIZE))
        terrain_images[image_file[:-4].replace("-", " ")] = terrain_image

# Define the number of tiles in each direction
NUM_TILES_X = int(WINDOW_WIDTH / TILE_SIZE)
NUM_TILES_Y = int(WINDOW_HEIGHT / TILE_SIZE)

# Define the character's position
character_pos = Vec2i(int(NUM_TILES_X / 2), int(NUM_TILES_Y / 2))
UP = Vec2i(0, 1)
RIGHT = Vec2i(1, 0)
DOWN = Vec2i(0, -1)
LEFT = Vec2i(-1, 0)
character_orientation = UP

# Define the size of the map
MAP_WIDTH = 800
MAP_HEIGHT = 800

# Define the number of tiles in each direction
NUM_TILES_X = int(MAP_WIDTH / TILE_SIZE) * 10
NUM_TILES_Y = int(MAP_HEIGHT / TILE_SIZE) * 10

# Define the sparse factor (lower values result in a more sparse map)
SPARSE_FACTOR = 0.04

# Load the cache
cache = StringCache(DEFAULT_CACHE_FILE_NAME)

# Define the map
map_tiles = []
for x in range(NUM_TILES_X):
    row = []
    for y in range(NUM_TILES_Y):
        if random.random() < SPARSE_FACTOR:
            terrain_tile_name = random.choice(list(terrain_images.keys()))
            terrain_tile = Thing(terrain_tile_name, cache)
        else:
            terrain_tile = None
        row.append(terrain_tile)
    map_tiles.append(row)

# Define the size of the view
VIEW_WIDTH = int(WINDOW_WIDTH / TILE_SIZE)
VIEW_HEIGHT = int(WINDOW_HEIGHT / TILE_SIZE)

# The thought only updates sometimes
# These need to be global for the thread to access it
thought = "STARTING..."
thought_prompt = ""
prompt_completion_done = True
time_since_last_thought = 10000  # milliseconds


def call_prompt_completion():
    global thought
    global thought_prompt
    global prompt_completion_done
    if not prompt_completion_done:
        print("I can't think right now! I'm already thinking!")
        return
    prompt_completion_done = False
    thought = prompt_completion(thought_prompt)
    thought_man.think_thought(thought)
    prompt_completion_done = True


# Set up the game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            action_logger.log_action("Quitting")
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                character_pos = character_pos.add(DOWN)
                character_orientation = DOWN
                action_logger.log_action("Character Moves North")
            elif event.key == pygame.K_DOWN:
                action_logger.log_action("Character Moves South")
                character_orientation = UP
                character_pos = character_pos.add(UP)
            elif event.key == pygame.K_LEFT:
                action_logger.log_action("Character Moves West")
                character_orientation = LEFT
                character_pos = character_pos.add(LEFT)
            elif event.key == pygame.K_RIGHT:
                action_logger.log_action("Character Moves East")
                character_orientation = RIGHT
                character_pos = character_pos.add(RIGHT)
            elif event.key == pygame.K_e:
                #TODO wrap the map tiles in an object or create a method to prevent out of bounds
                #map_tiles[character_x][character_y]
                action_logger.log_action("Character Attacks "+character_orientation)

    # Calculate the position of the top-left tile of the view
    view_x = max(0, character_pos.x - int(VIEW_WIDTH / 2))
    view_y = max(0, character_pos.y - int(VIEW_HEIGHT / 2))

    # Calculate the position of the bottom-right tile of the view
    view_x2 = min(NUM_TILES_X, view_x + VIEW_WIDTH)
    view_y2 = min(NUM_TILES_Y, view_y + VIEW_HEIGHT)

    # Black out the screen
    screen.fill((0, 0, 0))

    # Track what is on screen
    on_screen = []

    # Draw the map
    for x in range(view_x, view_x2):
        for y in range(view_y, view_y2):
            thing = map_tiles[x][y]
            if thing is not None:
                tile_image = terrain_images[thing.name]
                on_screen.append(map_tiles[x][y])
                screen.blit(tile_image, ((x - view_x) * TILE_SIZE, (y - view_y) * TILE_SIZE))

    # Draw the character
    character_position = ((character_pos.x - view_x) * TILE_SIZE, (character_pos.y - view_y) * TILE_SIZE)
    screen.blit(character_image, character_position)

    # Draw the text
    if time_since_last_thought > GENERATE_THOUGHT_EVERY:
        # Start a new thread to run prompt_completion()
        thought_prompt = generate_prompt_from_unknown_items(on_screen, action_log=action_logger.get_action_history(5), thoughts_log=list(reversed(thought_man.get_thought_history(5))))
        prompt_thread = threading.Thread(target=call_prompt_completion)
        prompt_thread.start()
        # thought = prompt_completion("I see some things around me: " + things_on_screen + " and I think that...")
        time_since_last_thought = 0
    time_since_last_thought += 60
    texts = ["Things that are nearby:", ", ".join([th.name for th in on_screen]), "", "THOUGHT: " + thought + "\n\n"] + thought_man.get_thought_history(5)
    y = WINDOW_HEIGHT + 20
    for line in texts:
        text = font.render(line, True, (255, 255, 255))
        text_rect = text.get_rect(topleft=(20, y))
        screen.blit(text, text_rect)
        y += FONT_SIZE

    # Update the screen
    pygame.display.flip()

    # Wait for the next frame
    clock.tick(60)

# Quit Pygame
pygame.quit()
