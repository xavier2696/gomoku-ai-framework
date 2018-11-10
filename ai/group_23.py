from goboard import Player, BoardInfo, GuiManager
import random
from math import *
import time

class Ai(Player):
    def __init__(self, color, **kwargs):
        super(Ai, self).__init__(color)
        self.state = GomokuState()
        self.state.color = color
        self.action_number = 0
        try:
            size_x, size_y = kwargs['board_size']
            self.state.n = size_x
        except IndexError:
            self.state.n = 13

    def get_action(self, board: BoardInfo, timeout) -> (int, int):
        self.action_number = self.action_number + 1
        self.state.update_with_board_info(board)
        maxtime = 2
        move = UCT(rootstate=self.state, maxtime=maxtime, verbose=False)
        print("Best Move: " + str(move))
        possible_x = int(move / self.state.n)
        possible_y = int(move % self.state.n)
        if board.is_legal_action(possible_x, possible_y):
            print("Move possible: %d,%d" % (possible_x, possible_y))
            self.state.last_player_move = move
            return possible_x, possible_y
        else:
            print("Move not possible: %d,%d" % (possible_x, possible_y))
            # default to easy ai for now, need another solution
            for x in range(0, board.size_x):
                for y in range(0, board.size_y):
                    if board.is_legal_action(x, y):
                        return x, y
                    else:
                        continue


class GomokuState:

    def update_with_board_info(self, board_info):
        new_board = [0 for element in range(self.n * self.n)]
        for x in range(0, board_info.size_x):
            for y in range(0, board_info.size_y):
                if board_info.is_black(x, y):
                    if self.color == "black":
                        new_board[int(x * self.n) + y] = 1
                    else:
                        new_board[int(x * self.n) + y] = 2
                else:
                    if board_info.is_white(x, y):
                        if self.color == "white":
                            new_board[int(x * self.n) + y] = 1
                        else:
                            new_board[int(x * self.n) + y] = 2

        for i in range(self.n * self.n):
            if self.board[i] != new_board[i] and new_board[i] == 2:
                self.last_opponent_move = i
        self.board = new_board
        #print(self)

    def __init__(self):
        self.color = "white"
        self.playerJustMoved = 2  # At the root pretend the player just moved is p2 - p1 has the first move
        self.n = 13  # board size
        self.board = [0 for element in range(self.n * self.n)]  # 0 = empty, 1 = player 1, 2 = player 2
        self.win_positions = []
        self.win_positions += self.generate_diagonal_win_positions()
        self.win_positions += self.generate_horizontal_win_positions()
        self.win_positions += self.generate_vertical_win_positions()
        self.last_opponent_move = -1
        self.last_player_move = -1

    def Clone(self):
        """ Create a deep clone of this game state.
        """
        st = GomokuState()
        st.playerJustMoved = self.playerJustMoved
        st.board = self.board[:]
        st.n = self.n
        st.win_positions = self.win_positions
        st.color = self.color
        st.last_opponent_move = self.last_opponent_move
        st.last_player_move = self.last_player_move
        return st

    def DoMove(self, move):
        """ Update a state by carrying out the given move.
            Must update playerToMove.
        """
        assert move >= 0 and move < (self.n * self.n) and move == int(move) and self.board[move] == 0
        self.playerJustMoved = 3 - self.playerJustMoved
        self.board[move] = self.playerJustMoved

    def GetMoves(self):
        """ Get all possible moves from this state.
        """
        if self.player_has_won():
            #print(self)
            return []
        return [i for i in range(self.n * self.n) if self.board[i] == 0]

    def GetAdjacentMoves(self, radius):
        if self.player_has_won():
            return []
        if self.last_opponent_move == -1 and self.last_player_move == -1:
            return self.GetMoves()
        adjacent_indexes = []
        if self.last_opponent_move != -1:
            opp_last_move_x = int(self.last_opponent_move / self.n)
            opp_last_move_y = int(self.last_opponent_move % self.n)
            adjacent_indexes += self.get_adjacent_moves(opp_last_move_x, opp_last_move_y, radius)

        if self.last_player_move != -1:
            player_last_move_x = int(self.last_player_move / self.n)
            player_last_move_y = int(self.last_player_move % self.n)
            adjacent_indexes += self.get_adjacent_moves(player_last_move_x, player_last_move_y, radius)

        if len(adjacent_indexes) == 0:
            return self.GetMoves()
        return adjacent_indexes

    def get_adjacent_moves(self, x_move, y_move, radius):
        adjacent_moves = []
        for x in range(x_move - radius, x_move + radius + 1):
            if x >= 0 and x < self.n:
                for y in range(y_move - radius, y_move + radius + 1):
                    if y >= 0 and y < self.n:
                        board_position = int(x * self.n) + y
                        if board_position >=0 and board_position < (self.n * self.n) and self.board[board_position] == 0:
                            adjacent_moves += [board_position]
        return adjacent_moves

    def GetResult(self, playerjm):
        """ Get the game result from the viewpoint of playerjm.
        """
        for (v, w, x, y, z) in self.win_positions:
            if self.board[v] == self.board[w] == self.board[x] == self.board[y] == self.board[z]:
                if self.board[v] == playerjm:
                    return 1.0
                else:
                    return 0.0
        if self.GetMoves() == []: return 0.5  # draw
        assert False  # Should not be possible to get here

    def player_has_won(self):
        for (v, w, x, y, z) in self.win_positions:
            if (self.board[v] == 1 or self.board[v] == 2) and (
                    self.board[v] == self.board[w] == self.board[x] == self.board[y] == self.board[z]):
                return True
        return False

    def generate_horizontal_win_positions(self):
        h_win_positions = []
        for i in range(0, (self.n * self.n)):
            if ((i % self.n) < self.n) and (((i % self.n) + 5) < self.n):
                h_win_positions += [(i, i + 1, i + 2, i + 3, i + 4)]
        return h_win_positions

    def generate_vertical_win_positions(self):
        v_win_positions = []
        for i in range(0, (self.n * self.n)):
            if ((i % self.n) < self.n) and ((i + 5 * self.n) < self.n * self.n):
                v_win_positions += [(i, i + 1 * self.n, i + 2 * self.n, i + 3 * self.n, i + 4 * self.n)]
        return v_win_positions

    def generate_diagonal_win_positions(self):
        d_win_positions = []
        n = self.n
        for i in range(0, (self.n * self.n)):
            if ((i % n) < n) and ((i + 4 * n + 4) <= (n * n - 1) and (i % n) + 4 < n):
                d_win_positions += [(i, i + 1 * n + 1, i + 2 * n + 2, i + 3 * n + 3, i + 4 * n + 4)]
            if ((i % n) < n) and ((i + 4 * n - 4) <= (n * n - 1) and (i % n) - 4 >= 0):
                d_win_positions += [(i, i + 1 * n - 1, i + 2 * n - 2, i + 3 * n - 3, i + 4 * n - 4)]
        return d_win_positions

    def __repr__(self):
        s = ""
        for i in range(self.n * self.n):
            if self.board[i] == 0:
                s += '[ ]'
            else:
                if self.board[i] == 1:
                    s += '[1]'
                else:
                    if self.board[i] == 2:
                        s += '[2]'
            if i % self.n == self.n - 1:
                s += '\n'
        return s


class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    """

    def __init__(self, move=None, parent=None, state=None):
        self.move = move  # the move that got us to this node - "None" for the root node
        self.parentNode = parent  # "None" for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.GetAdjacentMoves(3)  # future child nodes
        #the parameter is the limit for how spaced out the next piece will be placed
        self.playerJustMoved = state.playerJustMoved  # the only part of the state that the Node needs later

    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        s = sorted(self.childNodes, key=lambda c: c.wins / c.visits + sqrt(2 * log(self.visits) / c.visits))[-1]
        return s


    def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move=m, parent=self, state=s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n

    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
        self.visits += 1
        self.wins += result

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(
            self.untriedMoves) + "]"

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
            s += c.TreeToString(indent + 1)
        return s

    def IndentString(self, indent):
        s = "\n"
        for i in range(1, indent + 1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
            s += str(c) + "\n"
        return s


def UCT(rootstate, maxtime, verbose=False):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

    rootnode = Node(state=rootstate)
    end_time = time.time() + maxtime
    while time.time() < end_time:
    #for i in range(itermax):
        node = rootnode
        state = rootstate.Clone()

        # Select
        while node.untriedMoves == [] and node.childNodes != []:  # node is fully expanded and non-terminal
            node = node.UCTSelectChild()
            state.DoMove(node.move)

        # Expand
        if node.untriedMoves != []:  # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.untriedMoves)
            state.DoMove(m)
            node = node.AddChild(m, state)  # add child and descend tree

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while state.GetAdjacentMoves(3) != []:  # while state is non-terminal
            state.DoMove(random.choice(state.GetAdjacentMoves(3)))

        # Backpropagate
        while node != None:  # backpropagate from the expanded node and work back to the root node
            node.Update(state.GetResult(
                node.playerJustMoved))  # state is terminal. Update node with result from POV of node.playerJustMoved
            node = node.parentNode

    # Output some information about the tree - can be omitted
    #if (verbose):
        #print(rootnode.TreeToString(0))
    #else:
        #print(rootnode.ChildrenToString())

    return sorted(rootnode.childNodes, key=lambda c: c.visits)[-1].move  # return the move that was most visited
