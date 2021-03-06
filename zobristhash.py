from random import getrandbits
import numpy as np


class zobristHash:

    def __init__(self, x, y, states):
        self.states = states
        self.x = x
        self.y = y
        self.map = np.zeros((x, y, states), dtype=np.long)
           
    def precomupte(self):
        
        for x in range(self.x):
            for y in range(self.y):
                for state in range(self.states):
                    self.map[x][y][state] = getrandbits(32)

    def calculate_hash(self, last_hash, x, y, state):
        return last_hash ^ self.map[x][y][state]
    
    def calculate_board_hash(self, board):
        h = 0
        for x in range(self.x):
            for y in range(self.y):
                if board[x][y] != 0:
                    h = h ^ self.map[x][y][board[x][y] - 1]
        return h

# zh = zobristHash(2,7,6)
# zh.precomupte()
# print(zh.map)
# print(zh.calculate_hash(zh.calculate_hash(0,1,5,0),3,1,1))
# print(zh.calculate_hash(zh.calculate_hash(0,3,1,1),1,5,0))
