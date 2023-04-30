import tkinter as tk
from tkinter import messagebox

import info
from info import *
import time


class Cell:
    all = []
    num_of_flags = info.grid_size**2 // 7
    mine_label = None
    start_time =None
    end_time = None
    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.cell_btn = None
        self.x = x
        self.y = y

        Cell.all.append(self)

    def create_bnt(self, location):
        btn = tk.Button(
            location,
            text=("-"),
            bg='light gray',
            width=4,
            height=2,
            font=("Arial", 10)
        )
        btn.bind('<Button-1>', self.left_click)
        btn.bind('<Button-2>', self.middle_click)
        btn.bind('<Button-3>', self.right_click)

        self.cell_btn = btn

    def left_click(self, event=None):
        if not Cell.start_time:
            Cell.start_time = time.time()
        if self.is_mine:
            self.cell_btn.configure(text="*", bg="red")
            self.show_all()
            self.lose()
        else:
            res = self.count_mines_around()
            if res == 0:
                self.cell_btn.configure(text=' ')
                self.open_around_middle()
            else:
                self.cell_btn.configure(text=str(res))

    def right_click(self, event):
        if not Cell.start_time:
            Cell.start_time = time.time()
        if self.cell_btn.cget('text') == "F":
            self.cell_btn.configure(text="-", bg="light gray")
            Cell.num_of_flags += 1
        else:
            if Cell.num_of_flags > 0 and self.cell_btn.cget("text") == '-':
                self.cell_btn.configure(text="F", bg="yellow")
                Cell.num_of_flags -= 1
                if Cell.num_of_flags == 0:
                    if self.check_win():
                        self.win()
            Cell.mine_label.configure(text=str(Cell.num_of_flags))

    def middle_click(self, event):
        if self.cell_btn.cget('text') != "F" and self.cell_btn.cget('text') != "-" and self.cell_btn.cget(
                'text') != ' ':
            self.open_around_middle()

    def count_mines_around(self):
        counter = 0
        if self.x > 0:
            if self.get_cell_by_x_y(self.x - 1, self.y).is_mine:
                counter += 1
            if self.y > 0:
                if self.get_cell_by_x_y(self.x - 1, self.y - 1).is_mine:
                    counter += 1
            if self.y != info.grid_size - 1:
                if self.get_cell_by_x_y(self.x - 1, self.y + 1).is_mine:
                    counter += 1
        if self.x != info.grid_size - 1:
            if self.get_cell_by_x_y(self.x + 1, self.y).is_mine:
                counter += 1
            if self.y > 0:
                if self.get_cell_by_x_y(self.x + 1, self.y - 1).is_mine:
                    counter += 1
            if self.y != info.grid_size - 1:
                if self.get_cell_by_x_y(self.x + 1, self.y + 1).is_mine:
                    counter += 1
        if self.y > 0:
            if self.get_cell_by_x_y(self.x, self.y - 1).is_mine:
                counter += 1
        if self.y != info.grid_size - 1:
            if self.get_cell_by_x_y(self.x, self.y + 1).is_mine:
                counter += 1

        return counter

    def open_around_middle(self):
        if self.x > 0:
            temp = self.get_cell_by_x_y(self.x - 1, self.y)
            if temp.cell_btn.cget('text') == "-":
                temp.left_click()
        if self.x != info.grid_size - 1:
            temp = self.get_cell_by_x_y(self.x + 1, self.y)
            if temp.cell_btn.cget('text') == "-":
                temp.left_click()
        if self.y > 0:
            temp = self.get_cell_by_x_y(self.x, self.y - 1)
            if temp.cell_btn.cget('text') == "-":
                temp.left_click()
        if self.y != info.grid_size - 1:
            temp = self.get_cell_by_x_y(self.x, self.y + 1)
            if temp.cell_btn.cget('text') == "-":
                temp.left_click()
        if self.x > 0 and self.y > 0:
            temp = self.get_cell_by_x_y(self.x - 1, self.y - 1)
            if temp.cell_btn.cget('text') == "-":
                temp.left_click()
        if self.x != info.grid_size - 1 and self.y > 0:
            temp = self.get_cell_by_x_y(self.x + 1, self.y - 1)
            if temp.cell_btn.cget('text') == "-":
                temp.left_click()
        if self.y != info.grid_size - 1 and self.x != info.grid_size - 1:
            temp = self.get_cell_by_x_y(self.x + 1, self.y + 1)
            if temp.cell_btn.cget('text') == "-":
                temp.left_click()
        if self.y != info.grid_size - 1 and self.x > 0:
            temp = self.get_cell_by_x_y(self.x - 1, self.y + 1)
            if temp.cell_btn.cget('text') == "-":
                temp.left_click()

    def get_cell_by_x_y(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    def show_all(self):
        for cell in Cell.all:
            if cell.is_mine:
                if cell.cell_btn.cget("text") == "F":
                    cell.cell_btn.configure(text="*")
                else:
                    cell.cell_btn.configure(text="*", bg="red")
            else:
                temp = cell.count_mines_around()
                cell.cell_btn.configure(text=str(temp if temp else ' '), bg="light grey")

    def check_win(self):
        for cell in Cell.all:
            if (cell.is_mine and cell.cell_btn.cget('text') != 'F') or (
                    not cell.is_mine and cell.cell_btn.cget('text') == 'F'):
                return False
        return True

    def win(self):
        Cell.end_time = time.time()
        messagebox.showinfo(title="Win", message="You Won!\n time: %.2f sec" %(Cell.end_time - Cell.start_time))

    def lose(self):
        Cell.end_time = time.time()
        messagebox.showinfo(
            title="Win",
            message="Lose!\ntime: %.2f sec" %(Cell.end_time - Cell.start_time),


        )

    def update_mine(self):
        self.mineLabel.set(str(Cell.num_of_flags))
