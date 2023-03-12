import os
import pygame


class TileMapRenderer:
    TILE_SIZE = 32

    def __init__(self, tile_map, characters=None):
        self.tile_map = tile_map
        self.characters = characters if characters is not None else []
        self.width = len(tile_map[0])
        self.height = len(tile_map)
        self.images = {}

        # Load tile images from the 'images' folder
        for filename in os.listdir("../images"):
            name, extension = os.path.splitext(filename)
            if extension == ".png":
                image_path = os.path.join("../images", filename)
                image = pygame.image.load(image_path).convert_alpha()
                image = pygame.transform.scale(image, (self.TILE_SIZE, self.TILE_SIZE))
                self.images[name] = image

    def render_map(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                tile_type = self.tile_map[y][x].type
                image = self.images[tile_type]
                rect = pygame.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                screen.blit(image, rect)

        for character in self.characters:
            image = self.images[character.type]
            rect = pygame.Rect(character.x * self.TILE_SIZE, character.y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
            screen.blit(image, rect)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Tile Map Renderer")

    from room_gen import *
    map_generator = TileMapGenerator(width=30, height=20, seed=random.randint(0, 1000000))
    tile_map = map_generator.generate_map(water_level=0.4, tree_density=0.2, wall_density=0.05, rock_density=0.1)
    characters = map_generator.generate_characters(num_characters=5, character_types=("elf", "goblin", "human"))
    renderer = TileMapRenderer(tile_map, characters)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        renderer.render_map(screen)
        pygame.display.flip()

    pygame.quit()