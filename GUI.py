import tkinter as tk
from tkinter import messagebox
from functools import partial

from Game import Game


class Tile:
    def __init__(self, button, row, col):
        self.button = button
        self.row = row
        self.col = col


class GUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("Minesweeper")
        settings_frame = tk.Frame(self)

        tk.Label(settings_frame, text="Number of rows: ").grid(row=0)
        tk.Label(settings_frame, text="Number of columns: ").grid(row=1)
        tk.Label(settings_frame, text="Number of mines: ").grid(row=2)

        self.num_rows_field = tk.Entry(settings_frame)
        self.num_columns_field = tk.Entry(settings_frame)
        self.num_mines_field = tk.Entry(settings_frame)

        self.num_rows_field.insert(tk.END, "15")
        self.num_columns_field.insert(tk.END, "30")
        self.num_mines_field.insert(tk.END, "50")

        self.num_rows_field.grid(row=0, column=1)
        self.num_columns_field.grid(row=1, column=1)
        self.num_mines_field.grid(row=2, column=1)

        settings_frame.pack()
        tk.Button(self, text="Play", command=lambda: self.parse_input_play_new_game()).pack()

        self.game, self.game_frame, self.game_tiles = None, None, None
        self.parse_input_play_new_game()
        self.draw_grid()

        self.mainloop()


    def parse_input_play_new_game(self):
        game_args = [self.num_rows_field.get(), self.num_columns_field.get(), self.num_mines_field.get()]

        if not all([x.isdigit() for x in game_args]):
            return error_msg("Hmm those aren't numbers...")

        game_args = [int(x) for x in game_args]
        if not all([x > 1 for x in game_args]):
            return error_msg("Hmm that probably won't be a very good game...")

        if game_args[2] >= game_args[1] * game_args[0]:
            return error_msg("Hmm that's a few too many mines...")

        self.game = Game(*game_args)
        self.draw_grid()


    def draw_grid(self):
        if self.game_frame is not None:
            self.game_frame.destroy()
        self.game_frame = tk.Frame(self)

        self.game_tiles = []
        for r in range(self.game.num_rows):
            for c in range(self.game.num_columns):
                click_action = partial(self.click_tile, r, c)
                button = tk.Button(self.game_frame, text="  ", command=click_action)
                button.grid(row=r, column=c)
                self.game_tiles.append(Tile(button, r, c))
        self.game_frame.pack()
        self.update_grid()


    def update_grid(self):
        for tile in self.game_tiles:
            tile_type = self.game.get_tile_type(tile.row, tile.col)

            if tile_type == self.game.UNCHECKED:
                tile.button.config(text="   ")
            elif tile_type == self.game.EMPTY:
                tile.button.config(text="   ")
                tile.button.config(state="disabled", relief="sunken")
            else:
                tile.button.config(text=tile_type)


    def click_tile(self, row, col):
        game_over = self.game.click_tile(row, col)
        self.update_grid()
        if game_over:
            self.end_game()


    def end_game(self):
        game_over_msg(self.game.won)
        for tile in self.game_tiles:
            tile.button.config(state="disabled")


def game_over_msg(won):
    msg = "You won!" if won else "You lose :("
    tk.messagebox.showinfo("Game over", msg)


def error_msg(error):
    tk.messagebox.showwarning("Error", error)


if __name__ == '__main__':
    gui = GUI()
