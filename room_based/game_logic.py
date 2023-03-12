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

        # Update the player's velocity based on the input
        move_character(self.player, dx * self.PLAYER_SPEED, dy * self.PLAYER_SPEED, self.tile_map, self.all_characters, epsilon = 1.0)

    def bound_character_to_room(self, character):
        character.x = max(0, min(character.x, self.room.width - 1))
        character.y = max(0, min(character.y, self.room.height - 1))

    def update(self):
        # Update the player's position based on its velocity
        self.player.x += self.player.vx
        self.player.y += self.player.vy

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

if __name__ == "__main__":
    from map_gen import TileMapGenerator
    from map_data import Room, MapData
    from map_render import TileMapRenderer

    width = 30
    height = 20
    tile_size = 32

    # Initialize pygame first because it's used to load images
    pygame.init()
    screen = pygame.display.set_mode((width * tile_size, height * tile_size))
    pygame.display.set_caption("Tile Map Renderer")

    room = Room(width, height)
    room.set_exits(random.randint(1,width-1), random.randint(1,height-1), random.randint(1,width-1), random.randint(1,height-1))
    map_generator = TileMapGenerator(room, seed=random.randint(0, 1000000))
    tile_map = map_generator.generate_map(water_level=0.35, tree_density=0.05, wall_density=0.0, rock_density=0.03)
    map_generator.wall_in_map(tile_map, 2, room.north_exit, room.east_exit, room.south_exit, room.west_exit)
    characters = map_generator.generate_characters(tile_map, num_characters=5, character_types=("elf", "goblin", "human"))
    renderer = TileMapRenderer(tile_map, characters, tile_size=tile_size)
    game = Game(room, tile_map, characters)


    running = True
    clock = pygame.time.Clock()
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update the game state
        game.handle_input()
        game.update()

        # Render the tile map and characters
        screen.fill((0, 0, 0))
        renderer.render_map(screen)
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()