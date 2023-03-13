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

    def write_break_long_lines(self, text: list[str], screen, top_left: tuple[int, int] = (0, 0), max_width: int = None):
        if max_width is None:
            max_width = screen.get_width() - top_left[0]
        lines = []
        for i, line in enumerate(text):
            words = line.split()
            wrapped_lines = []
            current_line = ''
            for word in words:
                if self.font.size(current_line + ' ' + word)[0] < max_width:
                    current_line += ' ' + word if current_line else word
                else:
                    wrapped_lines.append(current_line)
                    current_line = word
            wrapped_lines.append(current_line)
            lines.extend(wrapped_lines)
        for i, line in enumerate(lines):
            text_surface = self.font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (top_left[0], top_left[1] + i * self.font_size))
