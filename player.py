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
        self.sprites = []
        self.sprites_dir = -1
        for i in range(16):
            surf = pygame.Surface((PLAYER_SPRITE_WIDTH, PLAYER_SPRITE_HEIGHT), pygame.SRCALPHA, 32)
            surf.blit(self.sprite_sheet, (0, 0),
                      (0, i*PLAYER_SPRITE_HEIGHT, PLAYER_SPRITE_WIDTH, PLAYER_SPRITE_HEIGHT))
            surf = pygame.transform.scale(surf, (PLAYER_WIDTH, PLAYER_HEIGHT))
            self.sprites.append(surf)
        standing_sprite = self.sprites[0]
        del self.sprites[:2]
        self.sprites.append(standing_sprite)
        self.dir = vec(0, 0)
        self.stored_direction = None
        self.able_to_move = True
        self.speed = 2


    def update(self):
        if self.able_to_move:
            self.pixel_pos += self.dir*self.speed
            self.pixel_pos[0] %= MAP_WIDTH
            self.pixel_pos[1] %= MAP_HEIGHT + TOP_BUFFER
        if self.correct_pos():
            if self.stored_direction is not None:
                self.dir = self.stored_direction
                if self.app.firstheartpath:
                    self.app.firstheartpath.pop(0)
            self.able_to_move = self.can_move(self.dir)
        self.grid_pos[0] = ((self.pixel_pos[0] + PLAYER_WIDTH//2+PLAYER_X_INDENT) // CELL_WIDTH) % 28
        self.grid_pos[1] = ((self.pixel_pos[1] - TOP_BUFFER + CELL_HEIGHT//2+PLAYER_Y_INDENT) // CELL_HEIGHT) % GRID_HEIGHT
        if self.on_heart_tile():
            self.pick_up_heart()

    def draw(self, i):
        if self.dir == (0, 0):
            self.app.screen.blit(self.sprites[14], self.pixel_pos)
            return
        if self.dir.x != self.sprites_dir and self.dir.x != 0:
            for j in range(len(self.sprites)):
                self.sprites[j] = pygame.transform.flip(self.sprites[j], True, False)
            self.sprites_dir = self.dir.x
        if not self.able_to_move:
            self.app.screen.blit(self.sprites[14], self.pixel_pos)
        else:
            self.app.screen.blit(self.sprites[i % 14], self.pixel_pos)

        '''pygame.draw.rect(self.app.screen, (200, 0, 0),
                         (self.grid_pos[0]*CELL_WIDTH,
                          self.grid_pos[1]*CELL_HEIGHT + TOP_BUFFER, CELL_WIDTH, CELL_HEIGHT), 1)
'''

    def move(self, dir):
        if self.dir == (0, 0):
            self.dir = dir
        self.stored_direction = dir

    def correct_pos(self):
        if int(self.pixel_pos[0] + PLAYER_X_INDENT) % CELL_WIDTH == 0:
            if self.dir == vec(1, 0) or self.dir == vec(-1, 0):
                return True
        if int(self.pixel_pos[1]+TOP_BUFFER + PLAYER_Y_INDENT) % CELL_HEIGHT == 0:
            if self.dir == vec(0, 1) or self.dir == vec(0, -1):
                return True
        return False

    def can_move(self, dir):
        next_cell = self.app.map[int(self.grid_pos[0] + dir[0])%GRID_WIDTH][int(self.grid_pos[1] + dir[1])%GRID_HEIGHT]
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
        self.app.hearts_pos.remove((x, y))

