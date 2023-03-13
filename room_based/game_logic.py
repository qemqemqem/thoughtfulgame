import random

import pygame

from location_utils import move_character, is_character_in_doorway
from map_gen import initialize_room_and_neighbors


class Game:
    PLAYER_SPEED = 0.2
    NPC_SPEED = 0.15

    def __init__(self, map_data, current_room):
        self.map_data = map_data
        self.room = current_room
        self.tile_map = self.room.tile_map
        self.player = self.room.characters[0]
        self.npcs = self.room.characters[1:]
        self.all_characters = self.room.characters

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        if keys[pygame.K_q]:
            pygame.quit()
            exit()
        if keys[pygame.K_LEFT]:
            dx = -1
        elif keys[pygame.K_RIGHT]:
            dx = 1
        if keys[pygame.K_UP]:
            dy = -1
        elif keys[pygame.K_DOWN]:
            dy = 1

        self.player.vx = dx
        self.player.vy = dy


    def bound_character_to_room(self, character):
        character.x = max(0, min(character.x, self.room.width - 1))
        character.y = max(0, min(character.y, self.room.height - 1))

    def update(self):
        # Update the player's position based on its velocity
        move_character(self.player, self.player.vx * self.PLAYER_SPEED, self.player.vy * self.PLAYER_SPEED, self.tile_map, self.all_characters)

        # Prevent the player from moving off the screen
        self.bound_character_to_room(self.player)

        for npc in self.npcs:
            # Change the NPC's direction randomly
            dx = random.uniform(-1, 1) * 1
            dy = random.uniform(-1, 1) * 1
            npc.vx += dx
            npc.vy += dy
            length = (npc.vx ** 2 + npc.vy ** 2) ** 0.5
            if length > 0:
                npc.vx /= length
                npc.vy /= length

            # Update the NPC's position based on its velocity
            move_character(npc, npc.vx * self.NPC_SPEED, npc.vy * self.NPC_SPEED, self.tile_map, self.all_characters)

            # Prevent the NPC from moving off the screen
            self.bound_character_to_room(npc)

    def move_character_to_new_room(self, character, old_room, new_room):
        old_room.characters.remove(character)
        new_room.characters.append(character)
        character.room = new_room
        # Move the character to the opposite side of the new room
        direction = new_room.room_pos - old_room.room_pos
        # Note that these signs are different and that might cause problems later
        character.x = character.x - direction.x * (old_room.width - 1)
        character.y = character.y + direction.y * (old_room.height - 1)
        if character.player_character:
            new_room.player_character = character
            old_room.player_character = None

    def move_to_new_room(self, room):
        old_room = self.room
        self.room = room
        self.tile_map = self.room.tile_map
        # self.player = self.room.characters[0]
        self.npcs = self.room.characters[:]
        self.move_character_to_new_room(self.player, old_room, self.room)
        self.all_characters = self.room.characters

    def check_player_door(self):
        room_change, direction = is_character_in_doorway(self.player, self.room)
        if not room_change:
            return
        new_room, initialized = self.map_data.get_room(self.room.room_pos + direction)
        if not initialized:
            initialize_room_and_neighbors(new_room, self.map_data)
        self.move_to_new_room(new_room)
