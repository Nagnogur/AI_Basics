import sys
import pygame
from settings import *
from player import *
from spritesheet import *


pygame.init()


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = 'start_screen'  ################
        self.player = Player(self, PLAYER_START_POS)
        self.map = []
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
        with open('map1.txt') as level:
            for row in level:
                row = row.strip()
                r = []
                for char in row:
                    r.append(char)
                self.map.append(r)
        self.map = [*zip(*self.map)]

    def grid(self):
        for i in range(28):
            pygame.draw.line(self.screen, (100, 100, 100), (i * CELL_WIDTH, TOP_BUFFER),
                             (i * CELL_WIDTH, MAP_HEIGHT + TOP_BUFFER))
        for i in range(31):
            pygame.draw.line(self.screen, (100, 100, 100), (0, i * CELL_HEIGHT + TOP_BUFFER),
                             (MAP_WIDTH, i * CELL_HEIGHT + TOP_BUFFER))
        '''for wall in self.walls:
            pygame.draw.rect(self.level, (87, 121, 255),
                             (wall[0]*CELL_WIDTH+(3*CELL_WIDTH//8),
                              wall[1]*CELL_HEIGHT+(3*CELL_HEIGHT//8),
                              CELL_WIDTH//4, CELL_HEIGHT//4))'''
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.player.can_move(vec(-1, 0)):
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT and self.player.can_move(vec(1, 0)):
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP and self.player.can_move(vec(0, -1)):
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN and self.player.can_move(vec(0, 1)):
                    self.player.move(vec(0, 1))

    def playing_update(self):
        self.player.update()

    def playing_draw(self):
        self.screen.blit(self.level, (0, TOP_BUFFER))
        self.grid()
        self.player.draw()
        pygame.display.update()
