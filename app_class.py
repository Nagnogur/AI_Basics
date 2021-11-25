from datetime import *
import sys
import time
from random import randrange

import pygame
from settings import *
from player import *
import numpy as np
from enemy import *
from path import *
from minimax import *

pygame.init()
pygame.display.set_caption("Terra-Man")
pygame.display.set_icon(pygame.image.load('Icon.png'))


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = 'playing'
        self.map = list()
        self.hearts_pos = list()
        self.enemies = []
        self.heart_number = 0
        self.picked_hearts = 0
        self.PLAYER_START_POS = (0, 0)
        self.load_level()
        self.ENEMY_START_POS = self.position_of_enemies(1)
        self.heart_image = self.load_heart_img()
        self.player = Player(self, self.PLAYER_START_POS)
        self.path = Path(self.map, self.enemies, self)
        self.make_enemies()
        self.frame = 0
        self.t = 0
        self.firstheartpath = []
        self.moves = 0
        self.next_hearth = self.hearts_pos[random.randrange(0, len(self.hearts_pos))]
        self.minimax = Minimax()
        self.time = datetime.now()

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
            elif self.game_state == 'game over':
                self.game_over_events()
                self.game_over_draw()
            elif self.game_state == 'victory':
                self.victory_events()
                self.victory_draw()
            else:
                self.running = False
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def draw_text(self, text, screen, size, colour, x, y, centered):
        font = pygame.font.SysFont('arial', size)
        text = font.render(text, False, colour)
        text_size = text.get_size()
        offset = [0, 0]
        if centered:
            offset = [text_size[0]//2, text_size[1]//2]
        screen.blit(text, (x-offset[0], y-offset[1]))

    def position_of_symbol(self, l, v):
        for i, x in enumerate(l):
            if v in x:
                return i, x.index(v)
        return None

    def position_of_enemies(self, start_num):
        pos = []
        p = self.position_of_symbol(self.map, str(start_num))
        while p is not None:
            pos.append(vec(p))
            start_num += 1
            p = self.position_of_symbol(self.map, str(start_num))
        return pos

    def load_level(self):
        #.level = pygame.image.load("map.png")
        '''wall = [['0' for i in range(GRID_HEIGHT)] for j in range(GRID_WIDTH)]
        for i in range(GRID_WIDTH):
            wall[i][0] = 'W'
            wall[i][GRID_HEIGHT - 1] = 'W'
        for i in range(GRID_HEIGHT):
            if i != 15:
                wall[0][i] = 'W'
                wall[GRID_WIDTH - 1][i] = 'W'
        for i in range(400):
            x = randrange(0, GRID_WIDTH)
            y = randrange(0, GRID_HEIGHT)
            if wall[x][y] != 'W':
                wall[x][y] = 'W'
        i = 0
        item = ['P', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        while i <= NUMBER_OF_ENEMIES:
            x = randrange(0, GRID_WIDTH)
            y = randrange(0, GRID_HEIGHT)
            if wall[x][y] == '0':
                wall[x][y] = item[i]
                i += 1'''

        self.level = pygame.Surface((MAP_WIDTH, MAP_HEIGHT))
        self.level = pygame.transform.scale(self.level, (MAP_WIDTH, MAP_HEIGHT))
        with open('map1.txt') as level:
            for row in level:
                row = row.strip()
                r = []
                for char in row:
                    r.append(char)
                self.map.append(r)
        self.map = np.array(self.map).T.tolist()

        self.PLAYER_START_POS = vec(self.position_of_symbol(self.map, 'P'))
        '''for i in range(100):
            pos = (randrange(0, GRID_WIDTH), randrange(0, GRID_HEIGHT))
            if self.map[pos[0]][pos[1]] not in ['P', '5', '6', '7']:
                if self.map[pos[0]][pos[1]] != 'W':
                    self.map[pos[0]][pos[1]] = 'W'
                else:
                    self.map[pos[0]][pos[1]] = '0' '''
        #self.map = wall
        #self.heart_number = self.count_hearts()
        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                if self.map[i][j] == 'h':
                    self.hearts_pos.append((i, j))
                    self.heart_number += 1

    def load_level_from_txt(self):
        self.level = pygame.image.load("map.png")
        self.level = pygame.transform.scale(self.level, (MAP_WIDTH, MAP_HEIGHT))
        with open('map1.txt') as level:
            for row in level:
                row = row.strip()
                r = []
                for char in row:
                    r.append(char)
                self.map.append(r)
        self.map = np.array(self.map).T.tolist()
        self.heart_number = self.count_hearts()

    def make_enemies(self):
        for i in range(NUMBER_OF_ENEMIES):
            self.enemies.append(Enemy(self, self.ENEMY_START_POS[i], i, i % 3))

    def grid(self):
        for i in range(28):
            pygame.draw.line(self.screen, (100, 100, 100), (i * CELL_WIDTH, TOP_BUFFER),
                             (i * CELL_WIDTH, MAP_HEIGHT + TOP_BUFFER))
        for i in range(31):
            pygame.draw.line(self.screen, (100, 100, 100), (0, i * CELL_HEIGHT + TOP_BUFFER),
                             (MAP_WIDTH, i * CELL_HEIGHT + TOP_BUFFER))
        '''pygame.draw.rect(self.level, (255, 84, 74), (CELL_WIDTH * (i + 3/8),
                                                        CELL_HEIGHT * (j + 3/8),
                                                                   CELL_WIDTH//4, CELL_HEIGHT//4))'''

    def load_heart_img(self):
        heart = pygame.image.load("Heart.png")
        heart = pygame.transform.scale(heart, (CELL_WIDTH//2, CELL_HEIGHT//2))
        return heart

    def count_hearts(self):
        return sum(row.count('h') for row in self.map)

    def make_level(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == 'W':
                    drawn = False
                    if i + 1 < len(self.map) and self.map[(i + 1) % GRID_WIDTH][j] == 'W':
                        pygame.draw.rect(self.level, (0, 90, 173), (CELL_WIDTH * i + CELL_WIDTH // 2,
                                                                    CELL_HEIGHT * (j + 3 / 8),
                                                                    CELL_WIDTH // 2, CELL_HEIGHT // 4))
                        drawn = True
                    if i - 1 >= 0 and self.map[(i - 1) % GRID_WIDTH][j] == 'W':
                        pygame.draw.rect(self.level, (0, 90, 173), (CELL_WIDTH * i,
                                                                    CELL_HEIGHT * (j + 3 / 8),
                                                                    CELL_WIDTH // 2, CELL_HEIGHT // 4))
                        drawn = True
                    if j + 1 < len(self.map[i]) and self.map[i][(j + 1) % GRID_HEIGHT] == 'W':
                        pygame.draw.rect(self.level, (0, 90, 173), (CELL_WIDTH * (i + 3 / 8),
                                                                    CELL_HEIGHT * j + CELL_HEIGHT // 2,
                                                                    CELL_WIDTH // 4, CELL_HEIGHT // 2))
                        drawn = True
                    if j - 1 >= 0 and self.map[i][(j - 1) % GRID_HEIGHT] == 'W':
                        pygame.draw.rect(self.level, (0, 90, 173), (CELL_WIDTH * (i + 3 / 8),
                                                                    CELL_HEIGHT * j,
                                                                    CELL_WIDTH // 4, CELL_HEIGHT // 2))
                        drawn = True
                    if not drawn:
                        pygame.draw.rect(self.level, (0, 90, 173), (CELL_WIDTH * (i + 3 / 8),
                                                                    CELL_HEIGHT * (j + 3 / 8),
                                                                    CELL_WIDTH // 4, CELL_HEIGHT // 4))
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
        self.draw_text("PRESS ENTER", self.screen, 16, (255, 255, 255),
                       APP_WIDTH//2, APP_HEIGHT//2, True)
        pygame.display.update()

# ---------------------------------------

    def draw_hearts(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == 'h':
                    self.screen.blit(self.heart_image,
                                     (i*CELL_WIDTH+CELL_WIDTH//4, j*CELL_HEIGHT+CELL_HEIGHT//4+TOP_BUFFER))

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
                if event.key == pygame.K_z:
                    self.path.change_alg()
                    self.t = 0

    def draw_enemy_path(self, l):
        color = [(254, 255, 71), (78, 255, 72), (255, 116, 60), (254, 255, 71), (78, 255, 72), (255, 116, 60), (254, 255, 71), (78, 255, 72), (255, 116, 60)]
        col = 0
        for path in l:
            self.draw_path(path, color[col])
            col += 1

        '''for i in path:
            surf = pygame.Surface((CELL_WIDTH // 4, CELL_HEIGHT // 4))
            pygame.Surface.fill(surf, (254, 255, 71))
            self.screen.blit(surf,
                             ((i[0] + 3/8) * CELL_WIDTH, (i[1] + 3/8) * CELL_HEIGHT + TOP_BUFFER))'''
        '''pygame.draw.rect(self.level, (254, 255, 71), (CELL_WIDTH * i[0],
                                                          CELL_HEIGHT * i[1],
                                                          CELL_WIDTH, CELL_HEIGHT))'''

    def draw_path(self, path, color):
        if path is None:
            return
        for i in range(len(path) - 1):
            if path[i + 1][0] == (path[i][0] + 1) % GRID_WIDTH:
                surf = pygame.Surface((CELL_WIDTH, CELL_HEIGHT // 5))
                pygame.Surface.fill(surf, color)
                self.screen.blit(surf,
                                 ((path[i][0] + 1 / 2) * CELL_WIDTH,
                                  (path[i][1] + 2 / 5) * CELL_HEIGHT + TOP_BUFFER))
            elif path[i + 1][1] == (path[i][1] + 1) % GRID_HEIGHT:
                surf = pygame.Surface((CELL_WIDTH // 5, CELL_HEIGHT))
                pygame.Surface.fill(surf, color)
                self.screen.blit(surf,
                                 ((path[i][0] + 2 / 5) * CELL_WIDTH,
                                  (path[i][1] + 1 / 2) * CELL_HEIGHT + TOP_BUFFER))
            elif path[i + 1][0] == (path[i][0] - 1) % GRID_WIDTH:
                surf = pygame.Surface((CELL_WIDTH, CELL_HEIGHT // 5))
                pygame.Surface.fill(surf, color)
                self.screen.blit(surf,
                                 ((path[i][0] - 1 / 2) * CELL_WIDTH,
                                  (path[i][1] + 2 / 5) * CELL_HEIGHT + TOP_BUFFER))
            elif path[i + 1][1] == (path[i][1] - 1) % GRID_HEIGHT:
                surf = pygame.Surface((CELL_WIDTH // 5, CELL_HEIGHT))
                pygame.Surface.fill(surf, color)
                self.screen.blit(surf,
                                 ((path[i][0] + 2 / 5) * CELL_WIDTH,
                                  (path[i][1] - 1 / 2) * CELL_HEIGHT + TOP_BUFFER))

    def playing_update(self):
        if self.picked_hearts == self.heart_number:
            self.game_state = 'victory'

        #if not self.firstheartpath:

        # MAKE THIS IN PLAYER CLASS (LIST OF DIRECTIONS)
        '''if self.moves == 0:
            position = Position(self, self.map, player_pos(self.player), self.enemies, self.heart_number,
                                self.picked_hearts, False)
            self.minimax.best_pos = []
            self.minimax.minimax(0, True, position, 1000, -1000, [position.player_position])
            self.minimax.best_pos.pop(0)
            self.moves = (self.moves + 1) % 20
        print(self.minimax.best_pos)
        print(player_pos(self.player))
        if self.minimax.best_pos:
            x = int(self.player.grid_pos[0]) - self.minimax.best_pos[0][0]
            y = int(self.player.grid_pos[1]) - self.minimax.best_pos[0][1]
            if self.player.can_move(vec(-x, -y)):
                self.player.move(vec(-x, -y))
                self.moves = (self.moves + 1) % 20'''
        # -------------------------
        '''self.firstheartpath = self.path.astar(self.map,
                                              (int(self.player.grid_pos[0]), int(self.player.grid_pos[1])),
                                              self.next_hearth)
        if self.firstheartpath is not None:
            self.firstheartpath.pop(0)
        # -------------------------------
        if self.firstheartpath is not None:
            x = int(self.player.grid_pos[0]) - self.firstheartpath[0][0]
            y = int(self.player.grid_pos[1]) - self.firstheartpath[0][1]
            if self.player.can_move(vec(-x, -y)):
                self.player.move(vec(-x, -y))'''
        self.player.update()
        for i in self.enemies:
            i.update()
            if i.grid_pos == self.player.grid_pos:
                self.game_state = 'game over'
                return

        start = time.time()
        self.path.find_path(int(self.player.grid_pos[0]), int(self.player.grid_pos[1]))
        self.t = max(time.time() - start, self.t)


    def playing_draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_text("Hearts {}/{}".format(self.picked_hearts, self.heart_number), self.screen, 18,
                       (255, 255, 255), APP_WIDTH//3, TOP_BUFFER//3, False)
        self.draw_text(str(self.t), self.screen, 18, (255, 255, 255), 0, 0, False)
        self.screen.blit(self.level, (0, TOP_BUFFER))
        self.make_level()
        self.grid()
        self.draw_hearts()
        #self.draw_enemy_path(self.path.st)
        self.draw_path(self.firstheartpath, (255, 138, 120))
        self.player.draw(int(self.frame))
        for i in range(NUMBER_OF_ENEMIES):
            self.enemies[i].draw()

        pygame.display.update()
        self.frame = (self.frame + 0.5) % 14

    def victory_draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_text("Victory", self.screen, 26, (100, 255, 90), APP_WIDTH // 2, TOP_BUFFER, True)
        self.draw_text("{} / {}".format(self.picked_hearts, self.heart_number),
                       self.screen, 26, (255, 255, 255), APP_WIDTH // 2, APP_HEIGHT // 2, True)
        pygame.display.update()

    def victory_events(self):
        time2 = datetime.now() - self.time
        f = open("results.txt", "a")
        f.write("\nvictory, " + str(time2.total_seconds()) + ", " + str(self.picked_hearts) + ", expectimax")
        f.close()
        '''for event in pygame.event.get():
            if event.type == pygame.QUIT:'''
        self.running = False

    def game_over_draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_text("GAME OVER", self.screen, 26, (255, 255, 255), APP_WIDTH//2, TOP_BUFFER, True)
        self.draw_text("{} / {}".format(self.picked_hearts, self.heart_number),
                       self.screen, 26, (255, 255, 255), APP_WIDTH//2, APP_HEIGHT//2, True)
        pygame.display.update()

    def game_over_events(self):
        time2 = datetime.now() - self.time
        f = open("results.txt", "a")
        f.write("\ndefeat, " + str(time2.total_seconds()) + ", " + str(self.picked_hearts) + ", expectimax")
        f.close()
        '''for event in pygame.event.get():
            if event.type == pygame.QUIT:'''
        self.running = False
