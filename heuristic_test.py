from supibot import SupiBot
import numpy as np

def test_state(board):
    print "Score: %s" % bot.rate_state(board)
    print board

bot = SupiBot()
bot.settings = {
    'your_botid': 1,
    'field_columns': 7,
    'field_rows': 6
}
board = np.zeros((6, 7), dtype=np.uint8)

test_state(board)

board = bot.simulate_place_disc(board, 3, 1)
test_state(board)

board = bot.simulate_place_disc(board, 3, 2)
test_state(board)

board = bot.simulate_place_disc(board, 1, 1)
test_state(board)
