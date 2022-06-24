# -*- coding: utf-8 -*-
# @Author: Matthieu LAURENT
# @Date:   2022-06-23 21:58:16
# @Last Modified by:   Matthieu LAURENT
# @Last Modified time: 2022-06-24 23:35:37

from __future__ import annotations

from itertools import chain
from random import Random, choice
from typing import Iterable

from minesweeper.gridcell import GridCell
from minesweeper.gamestate import GameState
from minesweeper.gui import MinesweeperDisplay


class Minesweeper:
    """A X by Y minesweeper grid, containing N mines"""
    def __init__(self, width: int, height: int, mines: int, *, auto_reveal: bool = False, 
                    gui: bool = False, free_start: bool = False, seed = None) -> None:
        self.width = int(width)
        self.height = int(height)
        self.mines_amount = int(mines)
        self.auto_reveal = bool(auto_reveal)
        self._show_gui = gui


        # For conveniance
        cell_count = width * height

        # ===== Fool-proofing =====
        if width <= 0 or height <= 0 or mines <= 0:
            raise ValueError("Width, height, and the amount of mines must all be stricly positive")

        if cell_count <= mines:
            raise ValueError("There are too many mines to fit in the grid")

        # We make a list with N True (True = a bomb will be there)
        bomb_bools = ([True] * mines) + ([False] * (cell_count - mines))
        # We use a Random instance to not have side-effects on the whole random lib when seeding
        r = Random()
        r.seed(seed)
        r.shuffle(bomb_bools)

        # Then we innitialise the 2d array that represents the grid.
        # We use a tuple and not a list because the grid itself
        # shouldn't change, just the cells inside the grid;
        self.grid = tuple(
            tuple(
                GridCell(
                    x = column,
                    y = line,
                    _revealed = False,
                    _grid = self,
                    _has_mine = bomb_bools[(line*width) + column]
                ) for column in range(width)
            ) for line in range(height)
        )
        
        self._window = MinesweeperDisplay(self)

        if free_start:
            self._safe_cell()._revealed = True
        
        self.gamestate = GameState.playing
        # In case it was an instant-win
        self.gamestate = self._check_gamestate()
    
        
    def _update_gui(self) -> None:
        if self._show_gui:
            self._window.update()

    def __iter__(self) -> Iterable[GridCell]:
        """Returns all cells, from left to right then top to bottom"""
        for y in range(self.height):
            for x in range(self.width):
                yield self.get_cell(x, y)

    @property
    def grid_string(self) -> str:
        """Makes a pretty representation of the grid"""

        s = ''
        for y in range(self.height):
            for x in range(self.width):
                # For each cell
                cell = self.get_cell(x, y)
                s += f"{cell.symbol} "
            s += '\n'
        return s

    def _check_gamestate(self) -> GameState:
        # If we won or lost, we can't change state
        if self.gamestate != GameState.playing:
            return self.gamestate

        # We check if we lost        
        if any(cell.revealed and cell._has_mine for cell in self):
            return GameState.game_over
        # Check if all non-bomb cells are revealed (aka a victory)
        if all(cell.revealed or cell._has_mine for cell in self):
            return GameState.victory
        return GameState.playing

    def _reveal_all(self) -> None:
        """Reveals all the cells, useful to show results after a victory"""
        for c in self:
            c._revealed = True
        self._update_gui()

    def _safe_cell(self) -> GridCell:
        """Returns a random cell that isn't revealed and doesn't have a mine"""
        return choice([c for c in self if not c.revealed and not c._has_mine])

    # ======= Start of the useful methods for solving =======
    def get_cell(self, x: int, y: int) -> GridCell:
        """Gets a cell at coordinates x;y (coordiates start at 0;0)"""
        # If we don't do that, using negative ints would wrap around
        if x < 0 or y < 0:
            raise ValueError(f"Cell {x};{y} is outside the grid")

        try:
            return self.grid[y][x]
        except IndexError as e:
            raise ValueError(f"Cell {x};{y} is outside the grid") from e

    def get_cells(self, *, revealed: bool = None, flagged: bool = None) -> list[GridCell]:
        """
        Get all cells that matches some criterias.
        Set a filter to None to disable it.
        """
        all_cells = list(chain.from_iterable(self.grid))
        if revealed is not None:
            all_cells = list(filter(lambda c: c.revealed == revealed, all_cells))
        if flagged is not None:
            all_cells = list(filter(lambda c: c.flagged == flagged, all_cells))
        return all_cells

    def reveal_cell(self, x: int, y: int, *, update_gui = True):
        """
        Reveals a cell at coordinates x;y (coordiates start at 0;0).
        Can cause gamestate to change to game_over
        """
        cell = self.get_cell(x, y)
        cell._revealed = True
        self.gamestate = self._check_gamestate()
        if self.auto_reveal and cell.value == 0 and not cell._has_mine:
            for c in cell.unrevealed_neighbours:
                # Yeah recursion is bad ikik
                # Also we only update the GUI when everything is revealed, for a
                # significant perfomance boost
                c.reveal(update_gui = False)
        if update_gui:
            self._update_gui()

# def main():
#     m = Minesweeper(10, 10, 20, auto_reveal = True, seed="desuwa")
#     m.get_cell(0, 0)._revealed = True
#     for cell in m:
#         cell._revealed = True
#     print(m.grid_string)

#     print()


# if __name__ == "__main__":
#     main()
