import random
import tkinter as tk
from tkinter import messagebox

import info
from cell import Cell
from info import *




class Game():
    def __init__(self):

        self.root = tk.Tk()
      #  self.root.geometry("400x600")
        self.root.title("MineSweeper")
        self.root.resizable(False, False)
        self.root.configure(bg="light gray")

        self.set_menubar()

        self.set_info_frame()

        self.gameboard = tk.Frame(self.root, borderwidth=5)

        self.set_board()
        self.gameboard.pack()

        self.root.protocol("WM_DELETE_WINDOW", exit)
        self.root.mainloop()

    def set_menubar(self):
        self.menubar = tk.Menu(self.root)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Help", command=self.send_help)
        self.filemenu.add_command(label="Exit", command=exit)
        self.menubar.add_cascade(menu=self.filemenu, label="File")

        self.gamemenu = tk.Menu(self.menubar, tearoff=0)
        self.gamemenu.add_command(label="Easy", command=self.go_easy)
        self.gamemenu.add_command(label="medium", command=self.go_medium)
        self.gamemenu.add_command(label="Hard", command=self.go_hard)
        self.menubar.add_cascade(menu=self.gamemenu, label="Game")


        self.root.config(menu=self.menubar)

    def set_info_frame(self):
        self.infoframe = tk.Frame(self.root, bg="light gray")
        self.infoframe.pack(padx=10, pady=10)

        self.space = tk.Label(
            self.infoframe,
            text=str("Mines left:"),
            borderwidth=1,
            # bg="light gray",
            padx=10,
            pady=10,
            font=("Arial", 13)
        )
        self.space.grid(row=0, column=0)
        self.mineLabel = tk.Label(
            self.infoframe,
            text=str(info.mine_number),
            borderwidth=1,
            padx=10,
            pady=10,
            font=("Arial", 13)
        )
        self.mineLabel.grid(row=0, column=1)

        self.space = tk.Label(
            self.infoframe,
            text=str("          "),
            bg="light gray"
        )
        self.space.grid(row=0, column=2)

        self.restartButton = tk.Button(
            self.infoframe,
            text="Restart",
            borderwidth=1,
            padx=10,
            pady=10
        )
        self.restartButton.bind('<Button-1>', self.set_board)
        self.restartButton.grid(row=0, column=3)

    def set_board(self, event= None):
        Cell.all = []
        for widget in self.gameboard.winfo_children():
            widget.destroy()
        for x in range(info.grid_size):
            for y in range(info.grid_size):
                self.c = Cell(x, y)
                self.c.create_bnt(self.gameboard)
                self.c.cell_btn.grid(row=x, column=y)
        self.randomm()
        Cell.mine_label = self.mineLabel
        Cell.num_of_flags = info.mine_number
        self.mineLabel.configure(text=str(info.mine_number))
        Cell.start_time = None

    def randomm(self):
        random_cells = random.sample(Cell.all, info.mine_number)
        for cell in random_cells:
            cell.is_mine = True


    def go_easy(self):
        info.grid_size = 9
        info.mine_number =info.grid_size**2 // 7
        self.set_board()
    def go_medium(self):
        info.grid_size = 13
        info.mine_number =info.grid_size**2 // 7
        self.set_board()
    def go_hard(self):
        info.grid_size = 16
        info.mine_number =info.grid_size**2 // 7
        self.set_board()
    def send_help(self):
        messagebox.showinfo(title="Help", message="Help!!!!")


Game()
