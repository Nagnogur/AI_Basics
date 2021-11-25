from position import *

class Minimax:

    def __init__(self):
        self.MAX, self.MIN = 10000, -10000
        self.best_pos = []
        self.best_score = -10000

    def minimax(self, depth, maximizing_player,
                position, alpha, beta, path):

        if depth == 6:
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
                val = self.minimax(depth + 1, False, p, alpha, beta, path)
                path.pop()
                if val > best:
                    best = val
                    best_pos = p.player_position
                alpha = max(alpha, best)

                '''if beta <= alpha:
                    break'''

            return best

        else:
            best = self.MAX
            best_pos = (0, 0)

            for p in position.get_children_enemies():
                val = self.minimax(depth + 1, True, p, alpha, beta, path)
                if val < best:
                    best = val
                    best_pos = p.player_position
                beta = min(beta, best)

                '''if beta <= alpha:
                    break'''
            return best
