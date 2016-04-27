from starterbot import Bot
from minmax import Node
from minmax import MinMax
import sys
import numpy as np
import time
from transposition import TranspositionTable


class SupiBot(Bot, MinMax):

    def __init__(self, debugMode = False):
        self.root = None
        self.debugMode = debugMode
        self.player_id_made_last_turn = None
        self.cached_lines_coords = None
        self.transTable = TranspositionTable(6,7,2)
        self.lastDepth = 0
        self.col_order = list(range(0,7))
        self.col_order[0] = 3
        self.col_order[1] = 4
        self.col_order[2] = 2
        self.col_order[3] = 5
        self.col_order[4] = 1
        self.col_order[5] = 6
        self.col_order[6] = 0
        
    def make_turn(self):
        
        # do this in the first turn
        if not self.root:
            self.root = Node(self.board)
            self.root.max_node = True
            self.root.value = 0
            self.root.hash = None
        
        board_hash = self.transTable.calculate_board_hash(self.board)

        # update board state (reuse the before calculated treee)
        if self.root.hash and board_hash != self.root.hash:
            for his_turn in self.root.children:
                if his_turn.hash == board_hash:
                    self.root = his_turn
        else:
            self.root.hash = board_hash

        start = time.time()
        
        # fixed search time per turn: 0.5s
        time_slice = 0.5

        # reduce time_slice if we have to hurry up
        if self.time_left() < 4000:
            time_slice = 0.3

        lBoundRange = max(1,self.lastDepth-1)
        dephSearchRange = range(lBoundRange,42)
        for i in dephSearchRange:
            self.minmax(i, self.root)
            self.lastDepth = i
            if time.time() - start > time_slice:
                if self.debugMode:
                    print('current depth '+str(i)+' time:'+str(time.time() - start))
                break

        best_option = self.root.children[0]
        self.place_disc(best_option.play_col)
        self.root = best_option

    def expand_node(self, node):
        if node.value == sys.maxsize or node.value == -sys.maxsize:  # leaf node
            return

        player_id = self.id() if node.max_node else self.opponent_id()  # other player than node
        for col_nr in self.col_order:
            try:
                new_state = self.simulate_place_disc(node.state, col_nr, player_id)
            except Bot.ColumnFullException:
                continue
            new_node = Node(new_state, node)
            new_node.play_col = col_nr
            
            # do not calculate the same positions twice
            draft_node = self.transTable.get_entry(new_node,
                                                   self.last_played_stone_row,
                                                   self.last_played_stone_col,
                                                   player_id)
            
            if not draft_node:
                new_node.value = self.rate_state(new_node.state)
                
                self.transTable.add_entry(new_node,
                                          self.last_played_stone_row,
                                          self.last_played_stone_col,
                                          player_id)
                
            else:
                # if the board sate is already calculated: use the value from the Transposition Table
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
        win_chances = set()

        for line in self.lines(board):
            value, wcs = SupiBot.rate_line(line)

            win_chances |= wcs

            if self.id() == 2:  # invert value if we are player 2
                value = -value
                        
            if value == sys.maxsize or value == -sys.maxsize:  # return if someone won
                return value

            board_sum += value

        # evaluate win chances
        # check for 2 win chances on top of each other. This will force a win
        win_chances_value = 0

        def get_double_win_chances(win_chances):
            double_win_chances = []
            for wc in win_chances:
                for wc2 in win_chances:
                    if wc[0][0]-1 == wc2[0][0] and wc[0][1] == wc2[0][1] and wc[1] == wc2[1]:
                        double_win_chances.append(wc)
            return double_win_chances

        dwcs = get_double_win_chances(win_chances)
        cut_win_chances = []
        for wc in win_chances:
            cut = False
            for dwc in dwcs:
                if dwc[0][0] > wc[0][0]+1 and dwc[0][1] == wc[0][1]:
                    cut = True
            if not cut:
                cut_win_chances.append(wc)
        dwcs = get_double_win_chances(cut_win_chances)

        for wc in cut_win_chances:
            win_chances_value += 20 if wc[1] == 1 else -20
        for dwc in dwcs:
            win_chances_value += 100 if wc[1] == 1 else -100

        board_sum += win_chances_value if self.id() == 1 else -win_chances_value
        return board_sum

    @staticmethod
    def rate_line(line):
        """ Rates the line from the perspective of player 1. """
        line_sum = 0
        win_chances = set()

        curr_player = 0  # the current owner of the last non-empty spot in the line
        take_over_idx = 0  # the index where the player took over
        win_spot = []  # placing a stone in this place will win the player the game

        consecutive_stones = 0
        player_stones = 0  # amount of stones of the curr player in the last 4 spots
        last_stone = 0

        for idx, (player, (row, col)) in enumerate(line):

            # add stones
            if player != 0:
                if player != curr_player:
                    # the other player takes over
                    if curr_player != 0:
                        take_over_idx = idx  # if there was not an earlier stone its all mine!
                    consecutive_stones = 1
                    player_stones = 1
                    curr_player = player

                else:
                    player_stones += 1

                    if last_stone == player:
                        consecutive_stones += 1

            # remove stones > 4 spaces away
            if idx >= 4 and idx - take_over_idx >= 3:
                rm_idx = idx - 4
                removed_stone = line[rm_idx][0]
                if removed_stone == curr_player:
                    player_stones -= 1
                    if line[rm_idx+1][0] == curr_player:  # check if we removed a consecutive stone
                        consecutive_stones -= 1

            # check the winn chance
            if curr_player != 0 and idx - take_over_idx >= 3:
                # check for win
                if player_stones == 4:
                    line_sum = sys.maxsize if curr_player == 1 else -sys.maxsize
                    return line_sum, set()

                # handle win chances in view of whole board
                elif player_stones == 3:
                    for i in range(take_over_idx, idx+1):
                        if line[i][0] == 0:  # found the free space
                            win_chance = tuple([line[i][1], curr_player])
                            win_chances |= set([win_chance])

                else:
                    value = player_stones * consecutive_stones
                    line_sum += value if curr_player == 1 else -value

            # save last stone
            last_stone = player

        return line_sum, win_chances

    def lines_coords_arrays(self):
        """ Generates all lines on the board (also diagonals) and yields the  coordinates of those lines as lists.
        """

        idxs = np.indices((6, 7))

        for row in range(self.rows()):
            yield idxs[:, row]

        for col in range(self.cols()):
            yield idxs[:, :, col]

        for diag_nr in range(-(self.rows() - 4), self.cols() - 3):
            yield [np.diag(idxs[0], diag_nr), np.diag(idxs[1], diag_nr)]

        idxs[1] = np.fliplr(idxs[1])

        for diag_nr in range(-(self.rows() - 4), self.cols() - 3):
            yield [np.diag(idxs[0], diag_nr), np.diag(idxs[1], diag_nr)]

    def lines_coords(self):
        """ Generates coordinates of line segments
        """
        if self.cached_lines_coords:
            return self.cached_lines_coords
        self.cached_lines_coords = []
        for line in self.lines_coords_arrays():
            line_coords = []
            for idx in range(len(line[0])):
                line_coords.append(tuple([line[0][idx], line[1][idx]]))
            self.cached_lines_coords.append(line_coords)
        return self.cached_lines_coords

    def lines(self, board):
        for line in self.lines_coords():
            yield [tuple([board[coord[0], coord[1]], coord]) for coord in line]

if __name__ == '__main__':
    """ Run the bot! """
    SupiBot().run()
