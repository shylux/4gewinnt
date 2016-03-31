import numpy as np
import sys
from sys import stdin, stdout


class Bot(object):

    settings = {}
    round = -1
    board = np.zeros((6, 7), dtype=np.uint8)

    def make_turn(self):
        best_col = 0
        best_rating = -sys.maxsize
        for col_nr in range(self.cols()):
            try:
                sim = self.simulate_place_disc(self.board, col_nr, self.id())
            except Bot.ColumnFullException:
                continue
            sim_rating = self.rate_state(sim)
            if self.id() == 2:
                sim_rating = -sim_rating  # the rating is done from view of player 1

            if sim_rating > best_rating:
                best_col = col_nr
                best_rating = sim_rating

        self.place_disc(best_col)

    def place_disc(self, column):
        stdout.write("place_disc %d\n" % column)
        stdout.flush()

    def rate_state(self, board):
        """ Rates the board. Positive outcomes means better vor player 1; negative better for player 2. """
        board_sum = 0
        for line in self.double_lines(board):
            value = self.rate_line(line)
            board_sum += value
            if value == sys.maxsize or value == -sys.maxsize:  # return if someone won
                return value
        return board_sum

    def rate_line(self, line_values):
        """ Rates the line. """
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
                        possible_fours[fidx] = (four_chance[0], four_chance[1]+1)

                # add a new possible chance
                possible_fours.append((idx, 1))

            if len(possible_fours) > 0:
                if idx - possible_fours[0][0] == 3:
                    four_chance = possible_fours.pop(0)
                    # positive vor player one, negative for player 2
                    value = four_chance[1]**2  # one stone = 1, two stones = 4, three stones = 9
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
        for diag_nr in range(-(self.rows()-4), self.cols()-3):
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

    def simulate_place_disc(self, board, col_nr, curr_player):
        if board[0, col_nr] != 0:
            raise Bot.ColumnFullException()
        new_board = np.copy(board)
        for row_nr in range(self.rows()-1, -1, -1):
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

    def run(self):
        """ Main loop.
        """
        # self.settings['field_rows'] = 6
        # self.settings['field_columns'] = 7
        # aa = self.simulate_place_disc(self.board, 0, 1)
        # self.rate_state(aa)
        # import pdb; pdb.set_trace()
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
            self.make_turn()

    def parse_field(self, str_field):
        self.board = np.fromstring(str_field.replace(';', ','), sep=',', dtype=np.uint8).reshape(6, 7)

    class ColumnFullException(Exception):
        """ Raised when attempting to place disk in full column. """

if __name__ == '__main__':
    '''
    Not used as module, so run
    '''
    Bot().run()
