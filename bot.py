#---------------------------------------------------------------------#
# Four In A Row AI Challenge - Starter Bot                            #
# ============                                                        #
#                                                                     #
# Last update: 30 Mar, 2016                                           #
#                                                                     #
# @author Lukas Knoepfel <shylux@gmail.com>                           #
# @version 1.0                                                        #
# @license MIT License (http://opensource.org/licenses/MIT)           #
#---------------------------------------------------------------------#

from sys import stdin, stdout
import numpy as np
import time


class Bot(object):

    settings = dict()
    round = -1
    board = np.zeros((6, 7), dtype=np.uint8)  # Access with [row_nr, col_nr]. [0,0] is on the top left.
    timeout = -1

    def make_turn(self):
        """ This method is for calculating and executing the next play.
            Make the play by calling place_disc exactly once.
        """
        raise NotImplementedError()

    def place_disc(self, column):
        """ Writes your next play in stdout. """
        stdout.write("place_disc %d\n" % column)
        stdout.flush()

    def simulate_place_disc(self, board, col_nr, curr_player):
        """ Returns a board state after curr_player placed a disc in col_nr.
            This is a simulation and doesn't update the actual playing board. """
        if board[0, col_nr] != 0:
            raise Bot.ColumnFullException()
        new_board = np.copy(board)
        for row_nr in reversed(range(self.rows())):
            if new_board[row_nr, col_nr] == 0:
                new_board[row_nr, col_nr] = curr_player
                return new_board

    def id(self):
        """ Returns own bot id. """
        return self.settings['your_botid']

    def rows(self):
        """ Returns amount of rows. """
        return self.settings['field_rows']

    def cols(self):
        """ Returns amount of columns. """
        return self.settings['field_columns']

    def current_milli_time(self):
        """ Returns current system time in milliseconds. """
        return int(round(time.time() * 1000))

    def set_timeout(self, millis):
        """ Sets time left until timeout in milliseconds. """
        self.timeout = self.current_milli_time() + millis

    def time_left(self):
        """ Get how much time is left until a timeout. """
        return self.timeout - self.current_milli_time()

    def run(self):
        """ Main loop.
        """
        while not stdin.closed:
            try:
                rawline = stdin.readline()

                # End of file check
                if len(rawline) == 0:
                    break

                line = rawline.strip()

                # Empty lines can be ignored
                if len(line) == 0:
                    continue

                parts = line.split()

                command = parts[0]

                self.parse_command(command, parts[1:])

            except EOFError:
                return

    def parse_command(self, command, args):
        if command == 'settings':
            key, value = args
            if key in ('timebank', 'time_per_move', 'your_botid', 'field_columns', 'field_rows'):
                value = int(value)
            self.settings[key] = value

        elif command == 'update':
            sub_command = args[1]
            args = args[2:]

            if sub_command == 'round':
                self.round = int(args[0])
            elif sub_command == 'field':
                self.parse_field(args[0])

        elif command == 'action':
            self.set_timeout(int(args[1]))
            self.make_turn()

    def parse_field(self, str_field):
        self.board = np.fromstring(str_field.replace(';', ','), sep=',', dtype=np.uint8).reshape(self.rows(), self.cols())

    class ColumnFullException(Exception):
        """ Raised when attempting to place disk in full column. """
import sys


class Node(object):

    def __init__(self, state, parent=None):
        if parent:
            self.max_node = not parent.max_node
            if(self.max_node):
                self.value = -sys.maxsize
            else:
                self.value = sys.maxsize
        self.state = state
        self.children = []
        self.parent = parent


    def __repr__(self):
        if len(self.children) == 0:
            return str(self.state)
        else:
            return "(" + ", ".join([str(child) for child in self.children]) + ")"


class MinMax(object):
    def __init__(self):
        self.root = None
    def heuristic(self, node):
        raise NotImplementedError()

    def expand_node(self, state):
        raise NotImplementedError()

    def minmax(self, max_depth, node=None, alpha=-sys.maxsize, beta=sys.maxsize):
        
        if max_depth == 0:  # leaf node
            return self.heuristic(node)

        if len(node.children) == 0:
            self.expand_node(node)

        if len(node.children) == 0:
            node.value = self.heuristic(node)
            return node.value

        node.value = -sys.maxsize if node.max_node else sys.maxsize  # initialize with worst value
        for child in node.children:
            child_value = self.minmax(max_depth-1, child, alpha, beta)
            if node.max_node:
                node.value = max(node.value, child_value)
                alpha = node.value
                if alpha >= beta:  # check for pruning
                    break
            else:
                node.value = min(node.value, child_value)
                beta = node.value
                if beta <= alpha:
                    break

        # sort for optimization
        node.children.sort(key=lambda n: -getattr(n, "value", sys.maxsize))
        if not node.max_node:
            node.children = list(reversed(node.children))

        return node.value
import sys
import numpy as np
import operator


class SupiBot(Bot, MinMax):

    def __init__(self):
        self.root = None
        self.player_id_made_last_turn = None
    def make_turn(self):
        # if not self.root:
        self.root = Node(self.board)
        self.root.max_node = True
        self.root.value = 0

        # update board state
        # if not (self.root.state - self.board).all():
        #     for his_turn in self.root.children:
        #         if (self.board - his_turn.state).all():
        #             self.root = his_turn
        #             break

        self.minmax(6,self.root)

        best_option = self.root.children[0]
        self.place_disc(best_option.play_col)
        self.root = best_option


        # best_col = 0
        # best_rating = -sys.maxsize
        # for col_nr in range(self.cols()):
        #     try:
        #         sim = self.simulate_place_disc(self.board, col_nr, self.id())
        #     except Bot.ColumnFullException:
        #         continue
        #     sim_rating = self.rate_state(sim)
        #     if self.id() == 2:
        #         sim_rating = -sim_rating  # the rating is done from view of player 1
        #
        #     if sim_rating > best_rating:
        #         best_col = col_nr
        #         best_rating = sim_rating
        #
        # self.place_disc(best_col)

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
            node.children.append(new_node)

    def opponent_id(self):
        return 2 if self.id() == 1 else 1

    def heuristic(self, node):
        node.value = self.rate_state(node.state)
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
