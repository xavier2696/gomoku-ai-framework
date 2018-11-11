from goboard import GomokuGameHandler
from goboard.judge import Win, Lose
from goboard.logger import log
from ai.easy_ai import Ai as EasyAi
from ai.normal_ai import Ai as NormalAi
from ai.alphabeta_ai import AlphaBetaAi
from ai.group_23 import Ai as Group23Ai
#from ai.hard_ai2 import Ai as HardAi
import time

black_player = NormalAi("black", board_size=(13, 13))
# black_player = AlphaBetaAi("black", board_size=(13, 13))
white_player = AlphaBetaAi("white", board_size=(13, 13))
# white_player = NormalAi("white", board_size=(13, 13))

with GomokuGameHandler(black_player, white_player, board_size=(13, 13), game_file='ai1_vs_ai2.json',
                       log_file='ai1_vs_ai2.txt') as (black_round, white_round, board):
    try:
        for _ in range(13 * 13 // 2):
            black_round()
            time.sleep(0.3)
            white_round()
            time.sleep(0.3)

    except Win as e:
        time.sleep(5)
        log('[end game] %s' % e)

    except Lose as e:
        time.sleep(5)
        log('[end game] %s' % e)

    except KeyboardInterrupt as e:
        log('[end game] KeyboardInterrupt!! , stop by user')

    except Exception as e:
        log('[end game] Terminated by unexpected exception!! %s' % e)
