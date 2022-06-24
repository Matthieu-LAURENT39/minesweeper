# -*- coding: utf-8 -*-
# @Author: Matthieu LAURENT
# @Date:   2022-06-24 17:50:36
# @Last Modified by:   Matthieu LAURENT
# @Last Modified time: 2022-06-24 23:00:37

from __future__ import annotations

from tkinter import *
from turtle import color
from typing import TYPE_CHECKING

from minesweeper.gamestate import GameState

if TYPE_CHECKING:
    from minesweeper.minesweeper import Minesweeper
    from minesweeper.gridcell import GridCell

COLORS = {
    0: '#C1C0BE',
    1: '#0305ED',
    2: '#017F04',
    3: '#F20500',
    4: '#030576',
    5: '#820201',
    6: '#087D86',
    7: '#010101',
    8: '#81807E',
}

def get_cell_colors(cell: GridCell) -> dict[str, int]:
    """Gives the kwargs for the colors of the labels"""
    colors = {}
    if cell.revealed:
        if cell._has_mine:
            if cell._grid.gamestate == GameState.victory:
                colors['bg'] = 'green'
                colors['fg'] = 'green'
            else:
                colors['bg'] = 'red'
                colors['fg'] = 'red'
        else:
            colors['bg'] = '#C1C0BE'
            colors['fg'] = COLORS[cell.value]
    else:
        colors['bg'] = '#FFFFFF'
        if cell.flagged:
            colors['fg'] = 'orange'
            colors['bg'] = 'orange'
        else:
            colors['fg'] = '#FFFFFF'

    return colors
    

class MinesweeperDisplay:
    def __init__(self, m: Minesweeper) -> None:
        self.minesweeper = m

        self.tk = Tk()
        # self.tk.grid_columnconfigure(0, minsize=50, weight=1)
        # self.tk.grid_rowconfigure(0, minsize=50, weight=1)
    
        # label_width = round(70 / m.width)
        # label_height = round(label_width / 1.90)

        self.labels: dict[ tuple[int, int], Label ] = {
            (cell.x, cell.y): Label(self.tk, text=str(cell), borderwidth=1, relief="solid", 
                                    width=4, height=2, padx=0, pady=0)
            for cell in m
        }

        for (x, y), l in self.labels.items():
            l.grid(column=x, row=y)

    def update(self) -> None:
        for cell in self.minesweeper:
            self.labels[(cell.x, cell.y)].config(text = cell.symbol, **get_cell_colors(cell))
        self.tk.update()