import os
import pygame


class TileMapRenderer:
    TILE_SIZE = 32

    def __init__(self, tile_size=32):
        self.TILE_SIZE = tile_size
        self.images = {}

        # Load tile images from the 'images' folder
        for filename in os.listdir("../images"):
            name, extension = os.path.splitext(filename)
            if extension == ".png":
                image_path = os.path.join("../images", filename)
                image = pygame.image.load(image_path).convert_alpha()
                image = pygame.transform.scale(image, (self.TILE_SIZE, self.TILE_SIZE))
                self.images[name] = image

    def render_map(self, screen, room):
        for y in range(room.height):
            for x in range(room.width):
                tile_type = room.tile_map[y][x].type
                image = self.images[tile_type.name]
                rect = pygame.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                screen.blit(image, rect)

        for character in room.characters:
            image = self.images[character.type]
            rect = pygame.Rect(character.x * self.TILE_SIZE, character.y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
            screen.blit(image, rect)
