import numpy as np
import random


class Game:
    def __init__(self, num_rows, num_columns, num_mines):
        self.EMPTY = 0
        self.MINE = 9
        self.UNCHECKED = 10

        self.num_rows = num_rows
        self.num_columns = num_columns
        self.num_mines = num_mines

        self.revealed = np.full((num_rows, num_columns), False)
        self.game_grid = np.full((num_rows, num_columns), self.EMPTY)

        self.set_mine_positions()
        self.set_tile_numbers()

        self.game_over = False
        self.won = False


    def set_mine_positions(self):
        num_tiles = self.num_rows * self.num_columns
        tile_indices = random.sample(range(num_tiles), self.num_mines)
        mine_indices = np.unravel_index(tile_indices, (self.num_rows, self.num_columns))
        self.game_grid[mine_indices] = self.MINE


    def set_tile_numbers(self):
        for row in range(self.num_rows):
            for col in range(self.num_columns):
                if self.game_grid[row, col] != self.MINE:
                    self.game_grid[row, col] = self.count_surrounding_mines(row, col)


    def count_surrounding_mines(self, row, col):
        surrounding_tiles = self.game_grid[
               max(0, row - 1): min(self.num_rows, row + 2),
               max(0, col - 1): min(self.num_columns, col + 2)]
        surrounding_mines = np.count_nonzero(surrounding_tiles == self.MINE)
        return surrounding_mines


    def click_tile(self, row, col):
        tile = self.game_grid[row, col]

        if self.revealed[row, col]:
            return self.game_over
        self.revealed[row, col] = True

        # Clicking on an empty tile also reveals surrounding tiles
        if tile == self.EMPTY:
            self.revealed[row, col] = True
            for r in range(max(0, row - 1), min(self.num_rows, row + 2), ):
                for c in range(max(0, col - 1), min(self.num_columns, col + 2)):
                    self.click_tile(r, c)
            self.check_has_won()

        elif tile == self.MINE:
            self.game_over = True
        else:
            self.check_has_won()
        return self.game_over


    def check_has_won(self):
        if self.game_over:
            return
        # Game is won if all tiles except mines are revealed
        mine_locations = self.game_grid == self.MINE
        self.won = np.all(np.logical_xor(mine_locations, self.revealed))
        self.game_over = self.won


    def get_tile_type(self, row, col):
        if self.revealed[row, col]:
            return self.game_grid[row, col]
        else:
            return self.UNCHECKED
