import pygame
from pygame.math import Vector2 as vec
from settings import *


class Player:
    def __init__(self, app, pos):
        self.app = app
        self.grid_pos = pos
        self.pixel_pos = vec(self.grid_pos.x * CELL_WIDTH - PLAYER_X_INDENT,
                             self.grid_pos.y * CELL_HEIGHT + TOP_BUFFER - PLAYER_Y_INDENT)
        self.sprite_sheet = pygame.image.load("NPC_22.png")
        self.dir = vec(1, 0)
        self.stored_direction = None
        self.able_to_move = True


    def update(self):
        if self.able_to_move:
            self.pixel_pos += self.dir
            self.pixel_pos[0] %= MAP_WIDTH
            self.pixel_pos[0] %= MAP_HEIGHT
        if self.correct_pos():
            if self.stored_direction is not None:
                self.dir = self.stored_direction
            self.able_to_move = self.can_move(self.dir)
        self.grid_pos[0] = ((self.pixel_pos[0] + PLAYER_WIDTH//2) // CELL_WIDTH) % 28
        self.grid_pos[1] = ((self.pixel_pos[1] - TOP_BUFFER + PLAYER_HEIGHT//2) // CELL_WIDTH) % 30
        if self.on_heart_tile():
            self.pick_up_heart()

    def draw(self):
        surf = pygame.Surface((PLAYER_SPRITE_WIDTH, PLAYER_SPRITE_HEIGHT), pygame.SRCALPHA, 32)
        surf.blit(self.sprite_sheet, (0, 0),
                  (0, 0, PLAYER_SPRITE_WIDTH, PLAYER_SPRITE_HEIGHT))
        surf = pygame.transform.scale(surf, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.app.screen.blit(surf, self.pixel_pos)

        '''pygame.draw.rect(self.app.screen, (200, 0, 0),
                         (self.grid_pos[0]*CELL_WIDTH,
                          self.grid_pos[1]*CELL_HEIGHT + TOP_BUFFER, CELL_WIDTH, CELL_HEIGHT), 1)'''

    def move(self, dir):
        self.stored_direction = dir

    def correct_pos(self):
        if int(self.pixel_pos[0] + PLAYER_X_INDENT) % CELL_WIDTH == 0:
            if self.dir == vec(1, 0) or self.dir == vec(-1, 0):
                return True
        if int(self.pixel_pos[1] - PLAYER_Y_INDENT) % CELL_HEIGHT == 0:
            if self.dir == vec(0, 1) or self.dir == vec(0, -1):
                return True

    def can_move(self, dir):
        next_cell = self.app.map[int(self.grid_pos[0] + dir[0])%28][int(self.grid_pos[1] + dir[1])%30]
        if next_cell == 'W' or next_cell == 'G':
            return False
        return True

    def on_heart_tile(self):
        if self.app.map[int(self.grid_pos[0])][int(self.grid_pos[1])] == 'h':
            return True
        return False

    def pick_up_heart(self):
        x = int(self.grid_pos[0])
        y = int(self.grid_pos[1])
        self.app.map[x][y] = '0'
        self.app.picked_hearts += 1
