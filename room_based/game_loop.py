import pygame

from room_based.map_render import TileMapRenderer
from room_based.game_logic import Game
from room_based.think_gen import update_thought_timers


def main_game_loop(game: Game, screen, renderer: TileMapRenderer):
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
        game.check_player_door()

        # Render the tile map and characters
        screen.fill((0, 0, 0))
        renderer.render_map(screen, game.room)
        renderer.render_thoughts(screen, game)
        pygame.display.flip()

        # Handle thoughts
        update_thought_timers(game.player, game)

        # Cap the frame rate
        clock.tick(60)
