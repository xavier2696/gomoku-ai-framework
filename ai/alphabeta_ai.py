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
TIE = EMPTY = 0
WHITE = -1

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

    # Bubble might update self.result.
    def step(self, x, y):
        assert self.result == None
        assert self.board[x][y][0] == 0

        self.board[x][y][0] = self.turn
        self.swipeAll()

        # swipeAll might have updated the result.
        # if self.result == None and self.tied():
        #     self.result = TIE
        #     return

        self.turn = -self.turn
        self.index = 3 - self.index

    # swipeAll swipes all positions in all directions and updates the state
    # saving for each possible move, the potential stack. And also saves the
    # "best move" for each player, the most greedy move.
    def swipeAll(self):
        self.bbest = None
        self.wbest = None
        self.swipe((1, 0), [(0, y) for y in range(MAX_Y)])
        self.swipe((-1, 0), [(12, y) for y in range(MAX_Y)])
        self.swipe((0, 1), [(x, 0) for x in range(MAX_X)])
        self.swipe((0, -1), [(x, 12) for x in range(MAX_X)])
        self.swipe((1, 1), [(0, y) for y in range(MAX_Y)] + [(x, 0) for x in range(1, MAX_X)])
        self.swipe((-1, -1), [(x, 12) for x in range(MAX_X)] + [(12, y) for y in range(0, MAX_Y - 1)])
        self.swipe((-1, 1), [(x, 12) for x in range(MAX_X)] + [(12, y) for y in range(0, MAX_Y - 1)])
        self.swipe((1, -1), [(0, y) for y in range(MAX_Y)] + [(x, 12) for x in range(1, MAX_X)])

    def swipe(self, dir, roots):
        for x, y in roots:
            self.bstack = 0
            self.wstack = 0
            while 0 <= x < MAX_X and 0 <= y < MAX_Y:
                # Update the potential stack in that direction for b&w.
                self.board[x][y][1][dir] = self.bstack + 1
                self.board[x][y][2][dir] = self.wstack + 1

                # Check if black or white won.
                if self.bstack + 1 == 6:
                    self.result = BLACK;
                elif self.wstack + 1 == 6:
                    self.result = WHITE;

                # Update best move for w&b.
                if self.board[x][y][0] == EMPTY:
                    if self.bbest == None or self.bstack + 1 > self.bbest[0]:
                        self.bbest = (self.bstack + 1, (x, y))
                    if self.wbest == None or self.wstack + 1 > self.wbest[0]:
                        self.wbest = (self.wstack + 1, (x, y))

                # Increment or clear the current stack.
                if self.board[x][y][0] == BLACK:
                    self.bstack += 1
                    self.wstack = 0
                elif self.board[x][y][0] == WHITE:
                    self.bstack = 0
                    self.wstack += 1
                else:
                    self.bstack = 0
                    self.wstack = 0
                x += dir[0]
                y += dir[1]
        if self.bbest == None and self.wbest == None:
            self.result = TIE

    # def tied(self):
    #     for x in range(MAX_X):
    #         for y in range(MAX_Y):
    #             if self.board[x][y][0] == 0:
    #                 return False
    #     return True

    def evaluate():
        # Evaluate function: f(state) = value
        # value tells us how much this state is good to be in.
        #
        # TODO: the other shat
        pass

    def __str__(self):
        stone = "○" if self.turn == BLACK else "●"
        if self.result == BLACK:
            result = "** ○ won! **"
        elif self.result == WHITE:
            result = "** ● won! **"
        elif self.result == TIE:
            result = "it's a tie!"
        else:
            result = ""
        state = "turn: %s\t\t%s\n" % (stone, result)
        return state + super(State, self).__str__()

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
