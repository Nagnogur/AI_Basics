import sys
import pygame
from settings import *

pygame.init()


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = 'start_screen'  ################
        self.load_level()

    def run(self):
        while self.running:
            if self.game_state == 'start_screen':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.game_state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            else:
                self.running = False
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def draw_text(self, text, screen, size, colour):
        font = pygame.font.SysFont('arial', size)
        text = font.render(text, False, colour)
        text_size = text.get_size()
        screen.blit(text, (200, 200))

    def load_level(self):
        self.level = pygame.image.load("map.png")
        self.level = pygame.transform.scale(self.level, (MAP_WIDTH, MAP_HEIGHT))

    def grid(self):
        for i in range(28):
            pygame.draw.line(self.screen, (100, 100, 100), (i * CELL_WIDTH, TOP_BUFFER),
                             (i * CELL_WIDTH, MAP_HEIGHT + TOP_BUFFER))
        for i in range(30):
            pygame.draw.line(self.screen, (100, 100, 100), (0, i * CELL_HEIGHT + TOP_BUFFER),
                             (MAP_WIDTH, i * CELL_HEIGHT + TOP_BUFFER))
# ---------------------------------------

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.game_state = 'playing'

    def start_update(self):
        pass

    def start_draw(self):
        self.draw_text("PRESS ENTER", self.screen, 16, (170, 130, 50))
        pygame.display.update()

# ---------------------------------------

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def playing_update(self):
        pass

    def playing_draw(self):
        self.screen.blit(self.level, (0, TOP_BUFFER))
        self.grid()
        pygame.display.update()
