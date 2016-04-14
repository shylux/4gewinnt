from supibot import SupiBot
import numpy as np
import sys
import shelve

#create valid boards for opening position
class boardCreator:
    
    def __init__(self,level):
        self.board = np.zeros((6, 7), dtype=np.uint8)
        self.boards = list(range(level+1))
        self.level = level
        self.filename = 'stored_boards.db'
        for i in self.boards:
            self.boards[i] = {}
            
        self.boards[0][(str(self.board))] = self.board
        self.bot = SupiBot()
        
    def create_boards(self):
        for y in range(self.level):
            for k,current_board in self.boards[y].items():          
                for i in range(7):
                    try:
                        player_id = self.bot.id() if y% 2 != 0 else self.bot.opponent_id()
                            
                        board = self.bot.simulate_place_disc(current_board,i,player_id )
                        self.boards[y+1][(str(board))] = board
                    except SupiBot.ColumnFullException:
                        continue
    def remove_invalid_boards(self):
        for y in range(self.level+1):
            keys = set(self.boards[y].keys())
            for key in keys:
                board = self.boards[y][key]
                value = self.bot.rate_state(board)
                #remove all boards with 4 or more connected lines
                if value == -sys.maxsize or value == sys.maxsize:
                    del self.boards[y][str(board)]

    def store_boards(self):
        d = shelve.open(self.filename) 
        d['opening_boards'] = self.boards
        d.close()
    def restore_boards(self):
        d = shelve.open(self.filename)
        self.boards = d['opening_boards']
    
                
        
level = 3
creator = boardCreator(level)
creator.bot.settings['your_botid'] = 1
creator.bot.settings['field_columns'] = 7
creator.bot.settings['field_rows'] = 6
creator.create_boards()
print(len(creator.boards[level]))
creator.remove_invalid_boards()
print(len(creator.boards[level]))
creator.store_boards()
creator.restore_boards()
print(len(creator.boards[level]))

