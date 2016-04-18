from starterbot import Bot
from minmax import Node
from minmax import MinMax
import sys
import numpy as np
import time
from transposition import TranspositionTable

class SupiBot(Bot, MinMax):

    def __init__(self,debugMode = False):
        self.root = None
        self.debugMode = debugMode
        self.player_id_made_last_turn = None
        self.transTable = TranspositionTable(6,7,2)

        
    def make_turn(self):
        
        
        if not self.root:
            self.root = Node(self.board)
            self.root.max_node = True
            self.root.value = 0
        
        self.root.hash = self.transTable.calculate_board_hash(self.board)
        # update board state
        #TODO: FIX these here...
        #if not (self.root.state - self.board).all():
        #    for his_turn in self.root.children:
        #        if (self.board - his_turn.state).all():
        #            self.root = his_turn
        #            break
                    
        
        start = time.time()
        
		#fixed search time per turn: 0.5s
        time_slice = 0.5

		#reduce time_slice if we have to hurry up        
        if self.time_left() < 4000:
            time_slice = 0.3
            
        for i in range(42):
            self.minmax(i, self.root)
            if time.time() - start > time_slice:
                if self.debugMode:
                    print('current depth '+str(i)+' time:'+str(time.time() - start))
                break

        best_option = self.root.children[0]
        self.place_disc(best_option.play_col)
        self.root = best_option
        #there are some crazy behaviors when the three and TransTable remains, and it's easier to debug
        self.root = None 

    def expand_node(self, node):
        if node.value == sys.maxsize or node.value == -sys.maxsize:  # leaf node
            return

        player_id = self.id() if node.max_node else self.opponent_id()  # other player than node
        for col_nr in range(self.cols()):
            try:
                new_state = self.simulate_place_disc(node.state, col_nr, player_id)
            except Bot.ColumnFullException:
                continue
            new_node = Node(new_state, node)
            new_node.play_col = col_nr
            
            #do not calculate the same positions twice
            draft_node = self.transTable.get_entry(new_node,self.last_played_stone_row,self.last_played_stone_col,player_id)
            
            if draft_node == None:
                new_node.value = self.rate_state(new_node.state)
                
                self.transTable.add_entry(new_node,self.last_played_stone_row,self.last_played_stone_col,player_id)
                
            else:
                #if the board sate is already calculated: use the value from the Transposition Table
                new_node.value = draft_node.node.value
                new_node.hash = draft_node.node.hash
                
            node.children.append(new_node)

    def opponent_id(self):
        return 2 if self.id() == 1 else 1

    def heuristic(self, node):
        return node.value

    def rate_state(self, board):
        """ Rates the board. A higher value means a better chance to win. """
        board_sum = 0
        for line in self.double_lines(board):
            value = SupiBot.rate_line(line)
            if self.id() == 2:  # invert value if we are player 2
                value = -value
            
                        
            if value == sys.maxsize or value == -sys.maxsize:  # return if someone won
                return value

            board_sum += value
        return board_sum

    @staticmethod
    def rate_line(line_values):
        """ Rates the line from the perspective of player 1. """
        line_sum = 0
        curr_player = 0  # the current owner of the last non-empty spot in the line
        possible_fours = []  # eg. [(idx, my_stone_count)]
        for idx, val in enumerate(line_values):
            if val != 0:
                if val != curr_player:
                    # the other player takes over
                    possible_fours = []
                    curr_player = val
                else:
                    for fidx, four_chance in enumerate(possible_fours):
                        possible_fours[fidx] = (four_chance[0], four_chance[1] + 1)

                # add a new possible chance
                possible_fours.append((idx, 1))

            if len(possible_fours) > 0:
                if idx - possible_fours[0][0] == 3:
                    four_chance = possible_fours.pop(0)
                    # positive vor player one, negative for player 2
                    value = four_chance[1] ** 2  # one stone = 1, two stones = 4, three stones = 9
                    if curr_player == 1:
                        line_sum += value
                    else:
                        line_sum -= value

                    # check if someone won
                    if four_chance[1] == 4:  # four stone = win
                        if curr_player == 1:
                            return sys.maxsize
                        else:
                            return -sys.maxsize
        return line_sum

    def lines(self, board):
        """ Generates all lines on the board (also diagonals) and yields the values on those lines as lists.
        """
        # all rows
        for row in board:
            yield row
        # all columns
        for col_nr in range(self.cols()):
            yield board[:, col_nr]
        # diagonals from top left to bottom right
        for diag_nr in range(-(self.rows() - 4), self.cols() - 3):
            yield np.diag(board, diag_nr)
        # diagonals from top right to bottom left
        board = np.fliplr(board)
        for diag_nr in range(-(self.rows() - 4), self.cols() - 3):
            yield np.diag(board, diag_nr)

    def double_lines(self, board):
        """ Generates all lines plus their reverse. """
        for line in self.lines(board):
            yield line
            yield line[::-1]


if __name__ == '__main__':
    """ Run the bot! """
    SupiBot().run()
