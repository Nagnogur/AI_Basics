import pygame
from pygame.math import Vector2 as vec
from settings import *
import queue


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


class Path:
    def __init__(self, level, enemies, app):
        self.app = app
        self.visited = [[False for i in range(GRID_HEIGHT)] for j in range(GRID_WIDTH)]
        self.level = level
        self.enemies = enemies
        self.dir = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        self.found = False
        self.st = [[] for i in range(NUMBER_OF_ENEMIES)]
        self.algorithms = ['bfs', 'dfs', 'ucs', 'none']
        self.cur_alg = 0

    def change_alg(self):
        self.cur_alg = (self.cur_alg + 1) % len(self.algorithms)

    def print(self):
        for i in self.st:
            print(i)

    def find_path(self, cur_row, cur_col):
        for enemy_id in range(NUMBER_OF_ENEMIES):
            if self.algorithms[self.cur_alg] == 'none':
                self.st[enemy_id] = []
            elif self.algorithms[self.cur_alg] == 'bfs':
                self.st[enemy_id] = self.start_bfs(cur_row, cur_col, self.enemies[enemy_id].grid_pos[0],
                                                   self.enemies[enemy_id].grid_pos[1], enemy_id)
            elif self.algorithms[self.cur_alg] == 'dfs':
                self.st[enemy_id] = self.start_dfs(cur_row, cur_col, self.enemies[enemy_id].grid_pos[0],
                                                   self.enemies[enemy_id].grid_pos[1])
            elif self.algorithms[self.cur_alg] == 'ucs':
                self.st[enemy_id] = self.start_ucs(cur_row, cur_col, self.enemies[enemy_id].grid_pos[0],
                                                   self.enemies[enemy_id].grid_pos[1], enemy_id)

    def start_dfs(self, cur_row, cur_col, target_row, target_col):
        self.visited = [[False for i in range(GRID_HEIGHT)] for j in range(GRID_WIDTH)]
        self.found = False
        st_dfs = []
        self.dfs(cur_row, cur_col, target_row, target_col, st_dfs)
        return st_dfs

    def dfs(self, cur_row, cur_col, target_row, target_col, st_dfs):
        self.visited[cur_row][cur_col] = True
        st_dfs.append((cur_row, cur_col))
        if cur_row == target_row and cur_col == target_col:
            self.found = True
            return
        for i in self.dir:
            row = (cur_row + i[0]) % GRID_WIDTH
            col = (cur_col + i[1]) % GRID_HEIGHT
            if not self.visited[row][col] and self.level[row][col] != 'W':
                self.dfs(row, col, target_row, target_col, st_dfs)
                if self.found:
                    return
        st_dfs.pop()

    def start_bfs(self, cur_row, cur_col, target_row, target_col, enemy_id):
        self.st[enemy_id] = self.bfs(cur_row, cur_col, target_row, target_col)
        return self.bfs(cur_row, cur_col, target_row, target_col)

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
        return self.ucs(cur_row, cur_col, int(target_row), int(target_col))

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
                    q.append([p[0] * -1 - 1, (row, col), p[2] + [(row, col)]])
                    used[row][col] = True
            used[p[1][0]][p[1][1]] = True
        return []

    def astar(self, maze, start, end):
        """Returns a list of tuples as a path from the given start to the given end in the given maze"""

        # Create start and end node
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0
        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        # Loop until you find the end
        while len(open_list) > 0:

            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)
            '''pygame.draw.rect(self.app.level, (255, 84, 74), (CELL_WIDTH * (current_node.position[0]),
                                                         CELL_HEIGHT * (current_node.position[1]),
                                                         CELL_WIDTH, CELL_HEIGHT))'''
            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1]  # Return reversed path

            # Generate children
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares
                # Get node position
                node_position = ((current_node.position[0] + new_position[0]),
                                 (current_node.position[1] + new_position[1]))

                # Make sure within range
                if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                        len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                    continue

                '''if Node(current_node, node_position) in closed_list:
                    continue'''

                # Make sure walkable terrain
                if maze[node_position[0]][node_position[1]] == 'W':
                    continue

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)
            # Loop through children
            for child in children:
                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        break
                else:
                    # Create the f, g, and h values
                    child.g = current_node.g + 1
                    # H: Manhattan distance to end point
                    child.h = abs(child.position[0] - end_node.position[0]) + abs(
                        child.position[1] - end_node.position[1])
                    child.f = child.g + child.h

                    # Child is already in the open list
                    for open_node in open_list:
                        # check if the new path to children is worst or equal
                        # than one already in the open_list (by measuring g)
                        if child == open_node and child.g >= open_node.g:
                            break
                    else:
                        # Add the child to the open list
                        open_list.append(child)
