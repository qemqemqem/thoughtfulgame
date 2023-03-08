import pygame
import os
import random

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
WINDOW_WIDTH = 800
TEXT_SPACE = 200
WINDOW_HEIGHT = 600

# Create the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT + TEXT_SPACE))

# Set the title of the window
pygame.display.set_caption("RPG Map")

# Set up the clock
clock = pygame.time.Clock()

# Set up the font
font = pygame.font.Font(None, 32)

# Define the directory where the images are stored
IMAGE_DIR = "images/"

# Define the size of each tile
TILE_SIZE = 64

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
character_x = int(NUM_TILES_X / 2)
character_y = int(NUM_TILES_Y / 2)

# Define the size of the map
MAP_WIDTH = 800
MAP_HEIGHT = 800

# Define the number of tiles in each direction
NUM_TILES_X = int(MAP_WIDTH / TILE_SIZE)
NUM_TILES_Y = int(MAP_HEIGHT / TILE_SIZE)

# Define the sparse factor (lower values result in a more sparse map)
SPARSE_FACTOR = 0.1

# Define the map
map_tiles = []
for x in range(NUM_TILES_X):
    row = []
    for y in range(NUM_TILES_Y):
        if random.random() < SPARSE_FACTOR:
            terrain_tile = random.choice(list(terrain_images.keys()))
        else:
            terrain_tile = None
        row.append(terrain_tile)
    map_tiles.append(row)

# Define the size of the view
VIEW_WIDTH = int(WINDOW_WIDTH / TILE_SIZE)
VIEW_HEIGHT = int(WINDOW_HEIGHT / TILE_SIZE)

# Set up the game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                character_y -= 1
            elif event.key == pygame.K_DOWN:
                character_y += 1
            elif event.key == pygame.K_LEFT:
                character_x -= 1
            elif event.key == pygame.K_RIGHT:
                character_x += 1
            elif event.key == pygame.K_q:
                running = False

    # Calculate the position of the top-left tile of the view
    view_x = max(0, character_x - int(VIEW_WIDTH / 2))
    view_y = max(0, character_y - int(VIEW_HEIGHT / 2))

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
            image_name = map_tiles[x][y]
            if image_name is not None:
                tile_image = terrain_images[image_name]
                on_screen.append(map_tiles[x][y])
                screen.blit(tile_image, ((x - view_x) * TILE_SIZE, (y - view_y) * TILE_SIZE))

    # Draw the character
    character_position = ((character_x - view_x) * TILE_SIZE, (character_y - view_y) * TILE_SIZE)
    screen.blit(character_image, character_position)

    # Draw the text
    texts = ["Things that are nearby:", ", ".join(on_screen), "", "Press Q to quit, arrow keys to move"]
    y = WINDOW_HEIGHT + 20
    for line in texts:
        text = font.render(line, True, (255, 255, 255))
        text_rect = text.get_rect(topleft=(20, y))
        screen.blit(text, text_rect)
        y += 32

    # Update the screen
    pygame.display.flip()

    # Wait for the next frame
    clock.tick(60)

# Quit Pygame
pygame.quit()
