import pygame
from settings import *

pygame.init()


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'intro'  ################

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
