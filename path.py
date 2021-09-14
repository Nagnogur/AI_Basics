import pygame
from pygame.math import Vector2 as vec
from settings import *
import queue


class Path:
    def __init__(self, level, enemies):
        self.visited = [[False for i in range(GRID_HEIGHT)] for j in range(GRID_WIDTH)]
        self.level = level
        self.enemies = enemies
        self.dir = [(1, 0), (0, -1), (-1, 0),  (0, 1)]
        self.found = False
        self.st = [[], [], []]
        self.algorithms = ['dfs', 'bfs', 'ucs', 'none']
        self.cur_alg = 0

    def change_alg(self):
        self.cur_alg = (self.cur_alg + 1) % len(self.algorithms)

    def is_valid(self, row, col):
        if self.visited[row][col]:
            return False
        if self.level[row][col] == 'W':
            return False
        return True

    def print(self):
        for i in self.st:
            print(i)

    def find_path(self, cur_row, cur_col):
        for enemy_id in range(3):
            if self.algorithms[self.cur_alg] == 'none':
                self.st[enemy_id] = []
            elif self.algorithms[self.cur_alg] == 'dfs':
                self.start_dfs(cur_row, cur_col, self.enemies[enemy_id].grid_pos[0],
                               self.enemies[enemy_id].grid_pos[1], enemy_id)
            elif self.algorithms[self.cur_alg] == 'bfs':
                self.start_bfs(cur_row, cur_col, self.enemies[enemy_id].grid_pos[0],
                               self.enemies[enemy_id].grid_pos[1], enemy_id)

    def start_dfs(self, cur_row, cur_col, target_row, target_col, enemy_id):
        self.visited = [[False for i in range(GRID_HEIGHT)] for j in range(GRID_WIDTH)]
        self.found = False
        self.st[enemy_id] = []
        self.dfs(cur_row, cur_col, target_row, target_col, enemy_id)

    def dfs(self, cur_row, cur_col, target_row, target_col, enemy_id):
        self.visited[cur_row][cur_col] = True
        self.st[enemy_id].append((cur_row, cur_col))
        if cur_row == target_row and cur_col == target_col:
            self.found = True
            return
        for i in self.dir:
            row = (cur_row + i[0]) % GRID_WIDTH
            col = (cur_col + i[1]) % GRID_HEIGHT
            if not self.visited[row][col] and self.level[row][col] != 'W':
                self.dfs(row, col, target_row, target_col, enemy_id)
                if self.found:
                    return
        self.st[enemy_id].pop()

    def start_bfs(self, cur_row, cur_col, target_row, target_col, enemy_id):
        self.st[enemy_id] = self.bfs(cur_row, cur_col, target_row, target_col)

    def bfs(self, cur_row, cur_col, target_row, target_col):
        q = queue.Queue()
        q.put((cur_row, cur_col))
        path = []
        used = [[False for i in range(GRID_HEIGHT)] for j in range(GRID_WIDTH)]
        while not q.empty():
            current = q.get()
            used[current[0]][current[1]] = True
            if current == (target_row, target_col):
                break
            else:
                for i in self.dir:
                    row = (current[0] + i[0]) % GRID_WIDTH
                    col = (current[1] + i[1]) % GRID_HEIGHT
                    if not used[row][col] and self.level[row][col] != 'W':
                        q.put((row, col))
                        path.append((current, (row, col)))
        target = (target_row, target_col)
        shortest = [target]
        while target != (cur_row, cur_col):
            for i in path:
                if i[1] == target:
                    target = i[0]
                    shortest.insert(0, i[0])
        return shortest
