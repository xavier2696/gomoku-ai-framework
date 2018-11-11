from ai.alphabeta_ai import Board, State

if __name__ == "__main__":
    board = State()
    board.step(0, 0)
    board.step(9, 3)
    board.step(9, 2)
    board.step(8, 3)
    board.step(8, 2)
    board.step(7, 3)
    board.step(7, 2)
    board.step(6, 3)
    board.step(5, 3)
    board.step(5, 2)
    board.step(5, 4)
    board.step(6, 2)
    board.step(3, 10)
    board.step(10, 10)
    print(board)
