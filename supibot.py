from starterbot import Bot
from minmax import  MinMax
import sys
import numpy as np


class SupiBot(Bot, MinMax):

    root = None

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

    def rate_state(self, board):
        """ Rates the board. Positive outcomes means better vor player 1; negative better for player 2. """
        board_sum = 0
        for line in self.double_lines(board):
            value = SupiBot.rate_line(line)
            board_sum += value
            if value == sys.maxsize or value == -sys.maxsize:  # return if someone won
                return value
        return board_sum

    @staticmethod
    def rate_line(line_values):
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
