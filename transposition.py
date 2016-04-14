import numpy as np
class TranspositionTable(object):
    def __init__(self):
        #hash-map
        self.dict = {}
        
    #Return 
    def get_entry(self,node):
        
        board_key = str(node.state)
        obj = self.dict.get(board_key)
        
        if obj == None or obj.node == node:
            return None 
        else:
            return self.dict[board_key] 
            
    def add_entry(self,node):
       board_key = str(node.state)
       self.dict[board_key] = TranspositionEntry(node) 
            
class TranspositionEntry:
    def __init__(self,node):
        self.node = node
