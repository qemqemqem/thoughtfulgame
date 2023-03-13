import pygame

class PygameWriter:
    def __init__(self):
        self.font_size = 24
        self.lines_of_text = 10
        self.text_space = self.font_size * self.lines_of_text
        self.font = pygame.font.Font(None, self.font_size)

    def write(self, text: list[str], screen, top_left: tuple[int, int] = (0, 0)):
        for i, line in enumerate(text):
            text_surface = self.font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (top_left[0], top_left[1] + i * self.font_size))