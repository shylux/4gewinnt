import numpy as np
class debugHelper:

    def __init__(self):
        self.board = np.zeros((6, 7), dtype=np.uint8)
        
    def read_board_from_string(self,board_string):
        board_rows =  board_string.split(';')
        
        for idy,board_row in enumerate(board_rows):
            splitted_board_row = board_row.split(',')
            for idx,board_cell in enumerate(splitted_board_row):
                self.board[idy,idx] = board_cell
        np.rot90(self.board)
