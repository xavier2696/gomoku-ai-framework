from goboard import Player, BoardInfo
import numpy as np
from copy import deepcopy

# Minimax with alpha-beta Pruning
# "ply" parameter (look ahead tree depth)
AB_DEPTH = 20

BOARD_SIZE = (13, 13)
MAX_X = BOARD_SIZE[0]
MAX_Y = BOARD_SIZE[1]

BLACK = 1
EMPTY = 0
WHITE = -1

BLACK_WIN = 1
TIE = 0
WHITE_WIN = -1

class Board:
    def __init__(self, board=None):
        if board == None:
            # 13 x 13 matrix B
            # Bij = (stone, pb, pw), pb and pw are the max potential resulting
            # stack if black or white play that move respectively.
            self.board = np.full((*BOARD_SIZE, 3), np.array([EMPTY, 1, 1]))
        else
            self.board = deepcopy(board)

class State(Board):
    def __init__(self, board=None):
        super(Board, self).__init__(board)
        self.turn = BLACK
        self.result = None

    def step(self, color, x, y):
        self.turn = -self.turn
        # TODO: the shat

    def evaluate():
        # TODO: the other shat

class AlphaBetaNode(State):
    def isLeaf(self):
        return self.result != None

    def children(self):
        children = []
        for x in range(MAX_X):
            for y in range(MAX_Y):
                if self.board[x][y][0] == 0:
                    child = AlphaBetaNode(self.board)
                    child.step(x, y)
                    child.action = (x, y)
                    children.append(child)
        return children

def alphabeta(node, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or node.isLeaf():
        return (node.evaluate(), node.action)
    if maximizingPlayer:
        value = -float("inf")
        for child in node.children():
            alphabeta, action = alphabeta(child, depth - 1, alpha, beta, False)
            value = max(value, alphabeta)
            action = node.action if value > alphabeta else action
            alpha = max(alpha, value)
            if alpha >= beta:
                #* β cut-off *#
                break
        return (value, action)
    else:
        value = float("inf")
        for child in node.children():
            value = min(value, alphabeta(child, depth − 1, alpha, beta, True))
            beta = min(beta, value)
            if alpha >= beta:
                #* α cut-off *#
                break
        return value

class AlphaBetaAi(Player):
    def __init__(self, color):
        super(Ai, self).__init__(color)
        self.state = State()

    def get_action(self, board: BoardInfo) -> (int, int):
        try:
            lastAction = self.convert_action(*board.steps[-1])
            self.state.step(lastAction)
        except IndexError:
            # Game has just began.
            pass

        x = np.random.randint(board.size_x)
        y = np.random.randint(board.size_y)
        while is not board.is_legal_action(x, y):
            x = np.random.randint(board.size_x)
            y = np.random.randint(board.size_y)
        return x, y

    def convert_action(self, position, color):
        return (position, BLACK if color == "black" else WHITE)
