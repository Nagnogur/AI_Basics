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

    def update(self):
        pass

    def draw(self):
        surf = pygame.Surface((PLAYER_SPRITE_WIDTH, PLAYER_SPRITE_HEIGHT), pygame.SRCALPHA, 32)
        surf.blit(self.sprite_sheet, (0, 0),
                             (0, 0, PLAYER_SPRITE_WIDTH, PLAYER_SPRITE_HEIGHT))
        surf = pygame.transform.scale(surf, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.app.screen.blit(surf, self.pixel_pos)