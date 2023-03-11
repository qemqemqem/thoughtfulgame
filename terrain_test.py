import pygame
import random
from noise import pnoise2

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Set the size of the tiles
TILE_SIZE = 32

# Define the number of tiles in the world
NUM_TILES_X = int(WINDOW_WIDTH / TILE_SIZE)
NUM_TILES_Y = int(WINDOW_HEIGHT / TILE_SIZE)

# Define the terrain types
TERRAIN_GRASS = 0
TERRAIN_WATER = 1

# Define the colors for each terrain type
TERRAIN_COLORS = {
    TERRAIN_GRASS: (100, 200, 100),
    TERRAIN_WATER: (0, 0, 200),
}

# Define the player's starting position
player_x = random.randint(0, NUM_TILES_X - 1)
player_y = random.randint(0, NUM_TILES_Y - 1)

# Define the Perlin noise settings
NOISE_SCALE = 5.0
NOISE_OCTAVES = 4
NOISE_PERSISTENCE = 0.5
NOISE_LACUNARITY = 2.0

seed = random.randint(-100000, 100000)

# Define the Perlin noise function
def get_terrain(x, y):
    value = pnoise2(x / NOISE_SCALE, y / NOISE_SCALE,
                    octaves=NOISE_OCTAVES,
                    persistence=NOISE_PERSISTENCE,
                    lacunarity=NOISE_LACUNARITY,
                    repeatx=NUM_TILES_X,
                    repeaty=NUM_TILES_Y,
                    base=seed)
    if value < -0.2:
        return TERRAIN_WATER
    else:
        return TERRAIN_GRASS


# Create the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Set the title of the window
pygame.display.set_caption("Fantasy World")

# Set up the font
font = pygame.font.Font(None, 32)

# Set up the game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and player_y > 0:
                player_y -= 1
            elif event.key == pygame.K_DOWN and player_y < NUM_TILES_Y - 1:
                player_y += 1
            elif event.key == pygame.K_LEFT and player_x > 0:
                player_x -= 1
            elif event.key == pygame.K_RIGHT and player_x < NUM_TILES_X - 1:
                player_x += 1

    # Black out the screen
    screen.fill((0, 0, 0))

    # Draw the tiles
    for x in range(NUM_TILES_X):
        for y in range(NUM_TILES_Y):
            terrain = get_terrain(x, y)
            color = TERRAIN_COLORS[terrain]
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, color, rect)

    # Draw the player
    player_rect = pygame.Rect(player_x * TILE_SIZE, player_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, (255, 255, 255), player_rect)

    # Update the screen
    pygame.display.flip()

    # Wait for the next frame
    pygame.time.wait