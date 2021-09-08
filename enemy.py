import pygame
from settings import *
from pygame.math import Vector2 as vec
import random

ENEMY_SPRITES = [pygame.image.load("Supreme_Calamitas.png"),
                 pygame.image.load("Supreme_Cataclysm.png"),
                 pygame.image.load("Supreme_Catastrophe.png")]


class Enemy:
    def __init__(self, app, pos, enemy_class):
        self.app = app
        self.grid_pos = pos
        self.enemy_class = enemy_class
        self.pixel_pos = vec(self.grid_pos.x * CELL_WIDTH - ENEMY_X_INDENT,
                             self.grid_pos.y * CELL_HEIGHT + TOP_BUFFER - ENEMY_Y_INDENT)
        self.sprite_sheet = ENEMY_SPRITES[self.enemy_class]
        self.dir = vec(-1, 0)
        self.speed = 1

    def update(self):
        self.pixel_pos += self.dir*self.speed
        self.pixel_pos[0] %= MAP_WIDTH
        self.pixel_pos[1] %= MAP_HEIGHT
        if self.time_to_move():
            self.move()
        self.grid_pos[0] = ((self.pixel_pos[0] + ENEMY_WIDTH // 2) // CELL_WIDTH) % 28
        self.grid_pos[1] = ((self.pixel_pos[1] - TOP_BUFFER + ENEMY_HEIGHT // 2) // CELL_WIDTH) % 30

    def draw(self):
        surf = pygame.Surface((ENEMY_SPRITE_WIDTH, ENEMY_SPRITE_HEIGHT), pygame.SRCALPHA, 32)
        surf.blit(self.sprite_sheet, (0, 0),
                  (0, 0, ENEMY_SPRITE_WIDTH, ENEMY_SPRITE_HEIGHT))
        surf = pygame.transform.rotate(self.sprite_sheet, -90)
        surf = pygame.transform.scale(surf, (ENEMY_WIDTH, ENEMY_HEIGHT))
        self.app.screen.blit(surf, self.pixel_pos)

        '''pygame.draw.rect(self.app.screen, (200, 0, 0),
                         (self.grid_pos[0]*CELL_WIDTH,
                          self.grid_pos[1]*CELL_HEIGHT + TOP_BUFFER, CELL_WIDTH, CELL_HEIGHT), 1)'''

    def time_to_move(self):
        if int(self.pixel_pos[0] + ENEMY_X_INDENT) % CELL_WIDTH == 0:
            if self.dir == vec(1, 0) or self.dir == vec(-1, 0):
                return True
        if int(self.pixel_pos[1] - ENEMY_Y_INDENT) % CELL_HEIGHT == 0:
            if self.dir == vec(0, 1) or self.dir == vec(0, -1):
                return True
        return False

    def move(self):
        self.dir = self.get_random_direction()

    def get_random_direction(self):
        while True:
            rand = random.random()
            if rand < 0.25:
                x = -1
                y = 0
            elif rand < 0.5:
                x = 1
                y = 0
            elif rand < 0.75:
                x = 0
                y = -1
            else:
                x = 0
                y = 1
            next_cell = self.app.map[int(self.grid_pos[0] + x) % 28][int(self.grid_pos[1] + y) % 30]
            if next_cell != 'W':
                break
        return vec(x, y)
