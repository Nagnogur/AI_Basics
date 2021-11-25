from position import *


class Expectimax:

    def __init__(self):
        self.MAX, self.MIN = 10000, -10000
        self.best_pos = []
        self.best_score = -10000

    def expectimax(self, depth, maximizing_player,
                   position, path):

        if depth == 3:
            eval = position.evaluate(path)

            if eval >= self.best_score:
                self.best_pos = path.copy()
                self.best_score = eval
            return eval

        if maximizing_player:

            best = self.MIN
            best_pos = (0, 0)

            for p in position.get_children_player():
                '''if p.player_position in path:
                    continue'''
                path.append(p.player_position)
                val = self.expectimax(depth + 1, False, p, path)
                path.pop()
                if val > best:
                    best = val
                    best_pos = p.player_position

            return best

        else:
            best = self.MAX
            best_pos = (0, 0)
            avg = 0
            num = 0
            for p in position.get_children_enemies_expect():
                val = self.expectimax(depth + 1, True, p, path)
                avg += val
                num += 1
            if num == 0:
                num = 1
            return avg/num
