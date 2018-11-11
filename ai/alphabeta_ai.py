from goboard import Player, BoardInfo
import numpy as np
from copy import deepcopy

# Minimax with alpha-beta Pruning
# "ply" parameter (look ahead tree depth)
AB_DEPTH = 20

BOARD_SIZE = (13, 13)
MAX_X = BOARD_SIZE[0]
MAX_Y = BOARD_SIZE[1]
DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]

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
            # Bij = (stone, potentialsBlack, potentialsWhite)
            # pb = [(potentialStackVal, origin), ..., (ps, origin)]
            # pw = [(potentialStackVal, origin), ..., (ps, origin)]
            self.board = np.full((*BOARD_SIZE, 3), np.array([EMPTY, None, None]))
            for x in range(MAX_X):
                for y in range(MAX_X):
                    potentials = {}
                    for dx, dy in DIRECTIONS:
                        _x, _y = x + dx, y + dy
                        if _x < 0 or _x >= MAX_X or _y < 0 or _y > MAX_Y:
                            continue
                        potentials[(dx, dy)] = 1
                    self.board[x][y][1] = potentials
                    self.board[x][y][2] = deepcopy(potentials)
        else:
            self.board = deepcopy(board)

    def __str__(self):
        _str = ""
        for y in range(MAX_Y):
            for x in range(MAX_X):
                stone = "○" if self.board[x][y][0] == BLACK else "●" if self.board[x][y][0] == WHITE else "_"
                maxb = max(self.board[x][y][1].values())
                maxw = max(self.board[x][y][2].values())
                if stone == "○" or stone == "●":
                    maxb = maxw = "_"
                _str += stone + str(maxb) + str(maxw) + " "
            _str += "\n"
        return _str

class State(Board):
    def __init__(self, board=None):
        super(State, self).__init__(board)
        self.turn = BLACK
        self.index = 1 # black is 1, white is 2, each Bij = (stone, b, w)
        self.result = None

    # Can update self.result.
    def step(self, x, y):
        assert self.board[x][y][0] == 0

        self.board[x][y][0] = self.turn
        self.updated = np.full((MAX_X, MAX_Y), False)
        self.bubble(x, y)

        self.turn = -self.turn
        self.index = 3 - self.index

    def bubble(self, x, y):
        for dx, dy in DIRECTIONS:
            _x, _y = x + dx, y + dy
            if _x < 0 or _x >= MAX_X or _y < 0 or _y >= MAX_Y:
                continue # Board border reached.
            print("updating", (_x, _y))
            # self.board[x][y][self.index][(dx, dy)] = self.board[_x][_y][self.index][(dx, dy)] + 1
            self.updated[x][y] = True
            if not self.updated[_x][_y]:
                if self.board[_x][_y][0] == EMPTY:
                    self.board[_x][_y][self.index][(dx, dy)] = self.board[x][y][self.index][(dx, dy)] + 1
                    self.updated[_x][_y] = True
                elif self.board[_x][_y][0] == self.turn:
                    # If we're stacking our own stones.
                    self.bubble(_x, _y)
                else:
                    # If it's an enemy stone, there's nothing to do.
                    pass

    def evaluate():
        # TODO: the other shat
        pass

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
            abValue, abAction = alphabeta(child, depth - 1, alpha, beta, False)
            value = max(value, abValue)
            action = node.action if value > abValue else abAction
            alpha = max(alpha, value)
            if alpha >= beta:
                #* β cut-off *#
                break
        return (value, action)
    else:
        value = float("inf")
        for child in node.children():
            abValue, abAction = alphabeta(child, depth - 1, alpha, beta, True)
            action = node.action if value > abValue else abAction
            value = min(value, abValue)
            beta = min(beta, value)
            if alpha >= beta:
                #* α cut-off *#
                break
        return (value, action)

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
        root = AlphaBetaNode(self.board)
        value, action = alphabeta(root, AB_DEPTH, -float("inf"), float("inf"), True)
        self.board.step(action)
        return action

    def convert_action(self, position, color):
        return (position, BLACK if color == "black" else WHITE)
