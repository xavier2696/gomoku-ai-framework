from goboard import Player, BoardInfo
import numpy as np

class RandomAi(Player):
    def get_action(self, board: BoardInfo, timeout) -> (int, int):
        x = np.random.randint(board.size_x)
        y = np.random.randint(board.size_y)
        while not board.is_legal_action(x, y):
            x = np.random.randint(board.size_x)
            y = np.random.randint(board.size_y)
        return x, y
