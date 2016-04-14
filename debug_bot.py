from debug_helper import debugHelper
from starterbot import Bot
from minmax import Node
from minmax import MinMax
from supibot import SupiBot

debug = debugHelper()
debug.read_board_from_string('0,0,0,0,0,0,0;0,0,0,0,0,0,0;0,0,0,0,0,0,0;0,0,0,0,1,0,1;0,2,0,0,1,0,1;2,2,0,0,2,0,1')
bot = SupiBot(True)
bot.board = debug.board.copy()
#bot.board[5,0] = 0
#bot.board[3,1] = 2
#print(bot.board)
#print(debug.board)
#print((bot.board-bot.board).all())
#print((bot.board-debug.board).all())
#print((str(bot.board) == str(debug.board)))
#print((str(bot.board) == str(bot.board)))

bot.settings['your_botid'] = 2
bot.settings['field_columns'] = 7
bot.settings['field_rows'] = 6
print(bot.make_turn())
