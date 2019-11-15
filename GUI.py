import tkinter as tk
from tkinter import messagebox

from Game import Game


class GUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.game = Game(3, 3, 3)

        self.title("Minesweeper")
        settings_frame = tk.Frame(self)

        tk.Label(settings_frame, text="Number of rows: ").grid(row=0)
        tk.Label(settings_frame, text="Number of columns: ").grid(row=1)
        tk.Label(settings_frame, text="Number of mines: ").grid(row=2)

        self.num_rows_field = tk.Entry(settings_frame)
        self.num_columns_field = tk.Entry(settings_frame)
        self.num_mines_field = tk.Entry(settings_frame)

        self.num_rows_field.insert(tk.END, "3")
        self.num_columns_field.insert(tk.END, "5")
        self.num_mines_field.insert(tk.END, "4")

        self.num_rows_field.grid(row=0, column=1)
        self.num_columns_field.grid(row=1, column=1)
        self.num_mines_field.grid(row=2, column=1)

        self.t1 = tk.Entry(settings_frame)
        self.t2 = tk.Entry(settings_frame)
        self.t1.grid(row=3)
        self.t2.grid(row=3, column=1)

        settings_frame.pack()

        tk.Button(self, text="Play", command=lambda: self.parse_input_play_new_game()).pack()

        tk.Button(self, text="Test", command=lambda: self.test()).pack()

        self.mainloop()


    def test(self):
        self.game.click_tile(row=int(self.t1.get()), col=int(self.t2.get()))
        print("-----")
        print(self.game.game_grid)
        print(self.game.revealed)
        print(self.game.game_over)
        print()


    def parse_input_play_new_game(self):
        game_args = [self.num_rows_field.get(), self.num_columns_field.get(), self.num_mines_field.get()]

        if not all([x.isdigit() for x in game_args]):
            return error_msg("Those aren't numbers")

        game_args = [int(x) for x in game_args]
        if not all([x > 1 for x in game_args]):
            return error_msg("Hmm that probably won't work very well")

        self.new_game(*game_args)


    def new_game(self, num_rows, num_columns, num_mines):
        self.game = Game(num_rows, num_columns, num_mines)


def error_msg(error):
    tk.messagebox.showwarning("Error", error)


if __name__ == '__main__':
    gui = GUI()
