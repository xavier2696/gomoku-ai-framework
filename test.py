from ai.alphabeta_ai import Board, State

if __name__ == "__main__":
    board = State()
    board.step(0, 0)
    print(board)
    board.step(12, 12)
    print(board)
    board.step(12, 11)
    print(board)
    board.step(11, 12)
    print(board)
    board.step(11, 11)
    print(board)
