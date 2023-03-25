import os
import pygame
from pygame import time

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
        self.thought_timer_space = 50

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
        is_player = False
        if len(things) > 0:
            subject = things[0]
        elif len(chars) > 0:
            subject = chars[0]
        if subject is None:
            subject = game.player
            is_player = True

        # Draw the portrait
        image = self.portraits[subject.type]
        rect = pygame.Rect(game.room.width * self.TILE_SIZE, 0, self.extra_space_on_right, self.extra_space_on_right)
        screen.blit(image, rect)

        # Text about the thing
        if is_player:
            text = [
                "You are a " + subject.type.capitalize() + " in the " + game.room.biome.name.capitalize(),
                "",
                game.room.description
            ]
        else:
            text = [
                subject.type.capitalize(),
                "",
                subject.description
            ]
        self.writer.write_break_long_lines(text, screen, top_left=(game.room.width * self.TILE_SIZE + self.writer.buffer_size, self.extra_space_on_right + self.writer.buffer_size))

    def draw_timer(self, screen, rect, percent_left):
        fill_width = int(rect.width * percent_left)

        # Draw the filled and empty portions of the rectangle
        fill_rect = pygame.Rect(rect.left, rect.top, fill_width, rect.height)
        empty_rect = pygame.Rect(rect.left + fill_width, rect.top, rect.width - fill_width, rect.height)
        pygame.draw.rect(screen, (0, 0, 0), fill_rect)
        pygame.draw.rect(screen, (20, 200, 20), empty_rect, 0)

    def render_thoughts(self, screen, game: Game):
        room: Room = game.room
        text = []
        for i in range(len(game.player.thought_brain.current_thought_options)):
            text.append(f"{'123456789'[i]}) {game.player.thought_brain.current_thought_options[i]}")
            text.append("")
        text.append("")
        # text.append("Nearby:")
        chars, things = room.get_nearby(game.player.x, game.player.y, distance=3)
        self.render_portrait(screen, game, chars, things)
        # for thing in things:
        #     text.append(" * " + thing.type + ", " + thing.description)
        # for character in chars:
        #     text.append(" * " + character.type + ", " + character.description)
        self.writer.write_break_long_lines(text, screen, top_left=(self.writer.buffer_size + self.thought_timer_space, room.height * self.TILE_SIZE + self.writer.buffer_size))

        # Draw the timer
        if game.player.thought_brain.default_thought is not None and game.player.thought_brain.default_thought.time_start_countdown is not None:
            for i in range(len(game.player.thought_brain.current_thought_options)):
                if game.player.thought_brain.default_thought == game.player.thought_brain.current_thought_options[i]:
                    perc_done = (time.get_ticks() - game.player.thought_brain.default_thought.time_start_countdown) / game.player.thought_brain.default_thought.appear_duration
                    rect = pygame.Rect(self.writer.buffer_size, room.height * self.TILE_SIZE + self.writer.buffer_size + i * self.writer.font_size * 2, self.thought_timer_space, self.writer.font_size)
                    self.draw_timer(screen, rect, perc_done)
