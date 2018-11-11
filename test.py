from goboard import GomokuGameHandler
from goboard.judge import Win, Lose
from goboard.logger import log
from ai.easy_ai import Ai as EasyAi
from ai.random_ai import Ai as RandomAi
from ai.normal_ai import Ai as NormalAi
from ai.alphabeta_ai import AlphaBetaAi
#from ai.hard_ai2 import Ai as HardAi
from ai.group_23 import Ai as Group23Ai
import time

# black = NormalAi("black", board_size=(13, 13))
# white = Group23Ai("white", board_size=(13, 13))

AIs = [EasyAi, RandomAi, NormalAi, AlphaBetaAi]

if __name__ == "__main__":
