import numpy as np
from zobristhash import zobristHash
class TranspositionTable(object):
    def __init__(self,x,y,states):
        #hash-map
        self.dict = {}
        self.zobristHash = zobristHash(x,y,states)
        self.zobristHash.precomupte()
        
    #Return 
    def get_entry(self,node,x,y,state):
        
        board_key = self.zobristHash.calculate_hash(node.parent.hash,x,y,state-1)
        obj = self.dict.get(board_key)
        
        if obj == None or obj.node == node:
            return None 
        else:
            return self.dict[board_key] 
            
    def add_entry(self,node,x,y,state):
       board_key = self.zobristHash.calculate_hash(node.parent.hash,x,y,state-1)
       node.hash = board_key
       self.dict[board_key] = TranspositionEntry(node)
       
    def calculate_board_hash(self,board): 
        return self.zobristHash.calculate_board_hash(board)
        
class TranspositionEntry:
    def __init__(self,node):
        self.node = node
