import copy
import itertools
import random

from enemy import Enemy
from helper import *
from settings import *


class Position:
    def __init__(self, app, level, player_position, enemies, hearths, cur_points, defeat):
        self.app = app
        self.level = level
        self.player_position = player_position
        self.enemies = enemies
        self.hearths = hearths
        self.cur_points = cur_points
        self.defeat = defeat
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.children = []
        self.evaluation = 0

    def get_children_enemies(self):
        if self.defeat:
            return []
        new_enemies = []
        defeat = False
        for e in self.enemies:
            pos = enemy_pos(e)
            # if e.enemy_class % 2 == 0:
            dir = e.to_player_position(self.player_position)
            '''else:
                dir = e.get_random_direction()'''
            enemy = Enemy(self.app, (pos[0] + dir[0], pos[1] + dir[1]), e.id, e.enemy_class)
            new_enemies.append(enemy)
            if enemy_pos(enemy) == self.player_position:
                defeat = True

        self.children.append(Position(self.app, copy.deepcopy(self.level), self.player_position, new_enemies,
                                      self.hearths, self.cur_points, defeat))
        return self.children

    def get_children_enemies_expect(self):
        if self.defeat:
            return []
        #new_enemies = []
        defeat = False
        enemies = []
        for e in self.enemies:
            pos = enemy_pos(e)
            enemy_dir = []
            # if e.enemy_class % 2 == 0:
            for dir in self.directions:
                dir = e.to_player_position(self.player_position)
                '''else:
                    dir = e.get_random_direction()'''
                enemy = Enemy(self.app, (pos[0] + dir[0], pos[1] + dir[1]), e.id, e.enemy_class)
                enemy_dir.append(enemy)
                if enemy_pos(enemy) == self.player_position:
                    defeat = True
            enemies.append(enemy_dir)

        for new_enemies in list(itertools.product(*enemies)):
            if random.random() > 0.5:
                continue
            self.children.append(Position(self.app, copy.deepcopy(self.level), self.player_position, new_enemies,
                                          self.hearths, self.cur_points, defeat))
        return self.children

    def get_children_player(self):
        if self.defeat:
            return []
        for d in self.directions:
            new_player_position = (self.player_position[0] + d[0], self.player_position[1] + d[1])
            next_cell = self.level[new_player_position[0]][new_player_position[1]]
            if next_cell != 'W':
                defeat = False
                new_level = copy.deepcopy(self.level)
                points = self.cur_points
                hearths = self.hearths
                for e in self.enemies:
                    if new_player_position == enemy_pos(e):
                        defeat = True
                        break
                if next_cell == 'h':
                    points += 1
                    hearths -= 1
                    new_level[new_player_position[0]][new_player_position[1]] = '0'

                self.children.append(Position(self.app, new_level, new_player_position, self.enemies, hearths, points, defeat))
        return self.children

    def get_children(self):
        if self.defeat:
            return []
        new_enemies = []
        for e in self.enemies:
            pos = enemy_pos(e)
            # if e.enemy_class % 2 == 0:
            dir = e.to_player_position(self.player_position)
            '''else:
                dir = e.get_random_direction()'''
            new_enemies.append(Enemy(self.app, (pos[0] + dir[0], pos[1] + dir[1]), e.id, e.enemy_class))
        for d in self.directions:
            new_player_position = (self.player_position[0] + d[0], self.player_position[1] + d[1])
            next_cell = self.level[new_player_position[0]][new_player_position[1]]
            if next_cell != 'W':
                defeat = False
                new_level = copy.deepcopy(self.level)
                points = self.cur_points
                hearths = self.hearths
                for e in new_enemies:
                    if new_player_position == enemy_pos(e):
                        defeat = True
                        break
                if next_cell == 'h':
                    points += 1
                    hearths -= 1
                    new_level[new_player_position[0]][new_player_position[1]] = '0'

                self.children.append(Position(self.app, new_level, new_player_position, new_enemies, hearths, points, defeat))
        return self.children

    def evaluate(self, path):
        if self.defeat:
            self.evaluation = -10000
            return self.evaluation
        '''if path[0] == path[2] or path[1] == path[3]:
            self.evaluation = -10000
            return self.evaluation'''
        if self.hearths == 0:
            self.evaluation = 10000
            return self.evaluation
        min_dist = 10000
        for e in self.enemies:
            min_dist = min(min_dist,
                           abs(self.player_position[0] - e.grid_pos[0]) + abs(self.player_position[1] - e.grid_pos[1]))
        self.evaluation = self.cur_points + min_dist
        return self.evaluation



