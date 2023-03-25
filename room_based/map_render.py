import os
import pygame

from room_based.game_logic import Game
from room_based.map_data import Room
from utils.pygame_writer import PygameWriter

IMAGES_FOLDER = "../images/generated"


class TileMapRenderer:
    TILE_SIZE = 32

    def __init__(self, writer:PygameWriter, tile_size=32, extra_space_on_right=0):
        self.TILE_SIZE = tile_size
        self.images = {}
        self.portraits = {}
        self.extra_space_on_right = extra_space_on_right

        # Load tile images from the 'images' folder
        for filename in os.listdir(IMAGES_FOLDER):
            name, extension = os.path.splitext(filename)
            if extension == ".png":
                image_path = os.path.join(IMAGES_FOLDER, filename)
                image = pygame.image.load(image_path).convert_alpha()
                portrait = pygame.transform.scale(image, (self.extra_space_on_right, self.extra_space_on_right))
                self.portraits[name.replace("-", " ")] = portrait
                smaller_image = pygame.transform.scale(image, (self.TILE_SIZE, self.TILE_SIZE))
                self.images[name.replace("-", " ")] = smaller_image

        self.writer = writer

    def render_map(self, screen, room: Room):
        for y in range(room.height):
            for x in range(room.width):
                tile_type = room.tile_map[y][x].get_file_name()
                image = self.images[tile_type]
                rect = pygame.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                screen.blit(image, rect)

        for thing in room.things:
            image = self.images[thing.type]
            rect = pygame.Rect(thing.x * self.TILE_SIZE, thing.y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
            screen.blit(image, rect)

        for character in room.characters:
            image = self.images[character.type]
            rect = pygame.Rect(character.x * self.TILE_SIZE, character.y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
            screen.blit(image, rect)

    def render_portrait(self, screen, game: Game, chars, things):
        subject = None
        if len(things) > 0:
            subject = things[0]
        elif len(chars) > 0:
            subject = chars[0]
        if subject is not None:
            image = self.portraits[subject.type]
            rect = pygame.Rect(game.room.width * self.TILE_SIZE, 0, self.extra_space_on_right, self.extra_space_on_right)
            screen.blit(image, rect)

    def render_descriptions(self, screen, game: Game):
        room: Room = game.room
        text = []
        text.append(room.description)
        text.append("")
        for i in range(len(game.player.thought_brain.current_thought_options)):
            text.append(f"{'ABCDEFGH'[i]}) {game.player.thought_brain.current_thought_options[i].text}")
        text.append("")
        text.append("Nearby:")
        chars, things = room.get_nearby(game.player.x, game.player.y, distance=3)
        self.render_portrait(screen, game, chars, things)
        for thing in things:
            text.append(" * " + thing.type + ", " + thing.description)
        for character in chars:
            text.append(" * " + character.type + ", " + character.description)
        self.writer.write_break_long_lines(text, screen, top_left=(0, room.height * self.TILE_SIZE))
