import pygame


def main_game_loop(game, screen, renderer):
    # Main game loop
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
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)
