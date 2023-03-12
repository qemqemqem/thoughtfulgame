import random

import pygame

from location_utils import move_character

class Game:
    PLAYER_SPEED = 0.5
    NPC_SPEED = 0.2

    def __init__(self, room, tile_map, characters):
        self.room = room
        self.tile_map = tile_map
        self.player = characters[0]
        self.npcs = characters[1:]
        self.all_characters = characters

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
        move_character(self.player, self.player.vx * self.PLAYER_SPEED, self.player.vy * self.PLAYER_SPEED, self.tile_map, self.all_characters, epsilon = 1.0)

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
            move_character(npc, npc.vx * self.NPC_SPEED, npc.vy * self.NPC_SPEED, self.tile_map, self.all_characters, epsilon=1.0)

            # Prevent the NPC from moving off the screen
            self.bound_character_to_room(npc)
