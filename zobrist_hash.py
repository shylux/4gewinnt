from random import randint
import sys
import numpy as np

class zobristHash:

    def __init__(self,states,x,y):
        self.states = states
        self.x = x
        self.y = y
        self.map = np.zeros((x*y,states), dtype=np.int)    
    def precomupte(self):
        
        for i in range(self.x*self.y):
            for y in range(self.states):
                self.map[i][y] = randint(0,sys.maxsize)
    def calculate_hash(self,last_hash,position,state):
        return last_hash ^ self.map[position][state]

zh = zobristHash(2,7,6)
zh.precomupte()
print(zh.map)
print(zh.calculate_hash(zh.calculate_hash(0,15,0),37,1))
print(zh.calculate_hash(zh.calculate_hash(0,37,1),15,0))
