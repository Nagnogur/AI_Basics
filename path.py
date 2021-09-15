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
        self.algorithms = ['bfs', 'dfs', 'ucs', 'none']
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
            elif self.algorithms[self.cur_alg] == 'bfs':
                self.start_bfs(cur_row, cur_col, self.enemies[enemy_id].grid_pos[0],
                               self.enemies[enemy_id].grid_pos[1], enemy_id)
            elif self.algorithms[self.cur_alg] == 'dfs':
                self.start_dfs(cur_row, cur_col, self.enemies[enemy_id].grid_pos[0],
                               self.enemies[enemy_id].grid_pos[1], enemy_id)
            elif self.algorithms[self.cur_alg] == 'ucs':
                self.start_ucs(cur_row, cur_col, self.enemies[enemy_id].grid_pos[0],
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
        flag = False
        q = queue.Queue()
        used = [[False for i in range(GRID_HEIGHT)] for j in range(GRID_WIDTH)]
        q.put((cur_row, cur_col))
        path = []
        used[cur_row][cur_col] = True
        while not q.empty():
            current = q.get()
            if current == (target_row, target_col):
                flag = True
                break
            else:
                for i in self.dir:
                    row = (current[0] + i[0]) % GRID_WIDTH
                    col = (current[1] + i[1]) % GRID_HEIGHT
                    if not used[row][col] and self.level[row][col] != 'W':
                        q.put((row, col))
                        used[row][col] = True
                        path.append((current, (row, col)))
        if not flag:
            return []
        target = (target_row, target_col)
        shortest = [target]
        while target != (cur_row, cur_col):
            for i in path:
                if i[1] == target:
                    target = i[0]
                    shortest.insert(0, i[0])
        return shortest

    def start_ucs(self, cur_row, cur_col, target_row, target_col, enemy_id):
        self.st[enemy_id] = self.ucs(cur_row, cur_col, int(target_row), int(target_col))

    def ucs(self, cur_row, cur_col, target_row, target_col):
        path = 10000000
        q = [[0, (cur_row, cur_col), [(cur_row, cur_col)]]]
        used = [[False for i in range(GRID_HEIGHT)] for j in range(GRID_WIDTH)]
        count = 0
        while len(q) > 0:
            q = sorted(q)
            p = q[-1]
            del q[-1]
            p[0] *= -1
            if (p[1][0], p[1][1]) == (target_row, target_col):
                if path > p[0]:
                    path = p[0]
                return p[2]
            for i in self.dir:
                row = (p[1][0] + i[0]) % GRID_WIDTH
                col = (p[1][1] + i[1]) % GRID_HEIGHT
                if not used[row][col] and self.level[row][col] != 'W':
                    q.append([p[0]*-1 - 1, (row, col), p[2] + [(row, col)]])
                    used[row][col] = True
            used[p[1][0]][p[1][1]] = True
        return []
