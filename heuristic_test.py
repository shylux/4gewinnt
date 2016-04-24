from supibot import SupiBot
import numpy as np

def test_state(board):
    print("Score: %s" % bot.rate_state(board))
    print(board)

def test_line(line):
    print("Score: %s" % bot.rate_line(line))
    print(line)

bot = SupiBot()
bot.settings = {
    'your_botid': 1,
    'field_columns': 7,
    'field_rows': 6
}
board_null = np.zeros((6, 7), dtype=np.uint8)

# test_line([1, 1, 0, 1, 0, 0, 0])
# test_line([1, 0, 1, 1, 0, 0, 0])

test_state(board_null)

board = bot.simulate_place_disc(board_null, 3, 1)
test_state(board)

board2 = bot.simulate_place_disc(board_null, 2, 1)
test_state(board2)

board = bot.simulate_place_disc(board, 3, 2)
test_state(board)

board0 = bot.simulate_place_disc(board, 0, 1)
test_state(board0)
board1 = bot.simulate_place_disc(board, 1, 1)
test_state(board1)
board2 = bot.simulate_place_disc(board, 2, 1)
test_state(board2)

board = bot.simulate_place_disc(board, 0, 1)
board = bot.simulate_place_disc(board, 1, 1)
test_state(board)

board_win = bot.simulate_place_disc(board, 2, 1)
test_state(board_win)

board = board_null
board = bot.simulate_place_disc(board, 0, 1)
board = bot.simulate_place_disc(board, 0, 1)
board = bot.simulate_place_disc(board, 1, 1)
board = bot.simulate_place_disc(board, 1, 1)
board = bot.simulate_place_disc(board, 3, 1)
board = bot.simulate_place_disc(board, 3, 1)
board = bot.simulate_place_disc(board, 0, 2)
board = bot.simulate_place_disc(board, 0, 2)
board = bot.simulate_place_disc(board, 1, 2)
board = bot.simulate_place_disc(board, 1, 2)
board = bot.simulate_place_disc(board, 3, 2)
board = bot.simulate_place_disc(board, 3, 2)
test_state(board)