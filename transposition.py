import numpy as np
from zobristhash import zobristHash

#A Transposition Table that uses Zobrish hashing for storing the values
class TranspositionTable(object):
    def __init__(self,x,y,states):
        #hash-map
        self.dict = {}
        self.zobristHash = zobristHash(x,y,states)
        self.zobristHash.precomupte()
        
    #Return an Entry or None 
    def get_entry(self,node,x,y,state):
        
        board_key = self.zobristHash.calculate_hash(node.parent.hash,x,y,state-1)
        obj = self.dict.get(board_key)
        
        if obj == None or obj.node == node:
            return None 
        else:
            return self.dict[board_key] 

	#Add a new Entry in the Transposition Table
    def add_entry(self,node,x,y,state):
       board_key = self.zobristHash.calculate_hash(node.parent.hash,x,y,state-1)
       node.hash = board_key
       self.dict[board_key] = TranspositionEntry(node)
    
    #Calculates the hash of the board (using Zobrish Hashing)   
    def calculate_board_hash(self,board): 
        return self.zobristHash.calculate_board_hash(board)

#Represents a singe Transposition Entry        
class TranspositionEntry:
    def __init__(self,node):
        self.node = node
