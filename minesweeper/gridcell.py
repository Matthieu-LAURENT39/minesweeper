# -*- coding: utf-8 -*-
# @Author: Matthieu LAURENT
# @Date:   2022-06-24 17:00:47
# @Last Modified by:   Matthieu LAURENT
# @Last Modified time: 2022-06-24 22:58:32

from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from dataclasses import dataclass
if TYPE_CHECKING:
    from minesweeper.minesweeper import Minesweeper

@dataclass
class GridCell:
    """A cell on the minesweeper's grid"""
    x: int
    """The column of the cell (counter starts at 0)"""
    y: int
    """The line of the cell (counter starts at 0)"""

        # Private attributes, you shouldn't be using those unless you 
    _revealed: bool
    """Used to make revealed read only"""
    _grid: Minesweeper
    """The grid this cell is a part of"""
    _has_mine: bool
    """Whether the cell has a mine. READING THIS ATTRIBUTE IS CHEATING!!!"""
    flagged: bool = False
    """Used by the player to mark a cell he thinks has a mine"""
    
    @property
    def revealed(self) -> bool:
        """True if the cell has already been revealed."""
        return self._revealed

    @property
    def neighbours(self) -> list[GridCell]:
        """
        The direct neighbours of this cell, from left to right then top to bottom
        The list's lenght can be less than 8
        """
        def _get_cell(x: int, y: int) -> Optional[GridCell]:
            """Returns a cell, or None if the coordinates are outsite the grid"""
            try:
                return self._grid.get_cell(x, y)
            except ValueError:
                return None

        return [c for c in (
                _get_cell(self.x-1, self.y-1),
                _get_cell(self.x, self.y-1),
                _get_cell(self.x+1, self.y-1),
                _get_cell(self.x-1, self.y),
                _get_cell(self.x+1, self.y),
                _get_cell(self.x-1, self.y+1),
                _get_cell(self.x, self.y+1),
                _get_cell(self.x+1, self.y+1),
            ) if c is not None]

    @property
    def revealed_neighbours(self) -> list[GridCell]:
        """Like neighbours, but with only revealed cells"""
        return [c for c in self.neighbours if c.revealed]
        
    @property
    def unrevealed_neighbours(self) -> list[GridCell]:
        """Like neighbours, but with only non-revealed cells"""
        return [c for c in self.neighbours if not c.revealed]

    @property
    def flagged_neighbours(self) -> list[GridCell]:
        """Like neighbours, but with only flagged cells"""
        return [c for c in self.neighbours if c.flagged]
        
    @property
    def unflagged_neighbours(self) -> list[GridCell]:
        """Like neighbours, but with only non-flagged cells"""
        return [c for c in self.neighbours if not c.flagged]

    @property
    def revealable_neighbours(self) -> list[GridCell]:
        return self.get_neighbours(revealed=False, flagged=False)

    def get_neighbours(self, *, revealed: bool = None, flagged: bool = None) -> list[GridCell]:
        """
        Like neighbours, but allows to set filters.
        Set a filter to None to disable it.
        """
        neighbours = self.neighbours
        if revealed is not None:
            neighbours = list(filter(lambda c: c.revealed == revealed, neighbours))
        if flagged is not None:
            neighbours = list(filter(lambda c: c.flagged == flagged, neighbours))
        return neighbours

    @property
    def value(self) -> Optional[int]:
        """
        The number of mines directly next to the cell. 
        None if the cell isn't revealed
        """
        def _has_bomb(x: int, y: int) -> bool:
            """
            True if the cell at those coordinates has a bomb. 
            False if it doesn't have a bomb, or if the coordinates
            are outsite the grid
            """
            try:
                return self._grid.get_cell(x, y)._has_mine
            except ValueError:
                return False

        if not self.revealed:
            return None
            
        # We get the number of bombs in all 8 directions using bool summing
        return sum((
            _has_bomb(self.x-1, self.y-1),
            _has_bomb(self.x, self.y-1),
            _has_bomb(self.x+1, self.y-1),
            _has_bomb(self.x-1, self.y),
            _has_bomb(self.x+1, self.y),
            _has_bomb(self.x-1, self.y+1),
            _has_bomb(self.x, self.y+1),
            _has_bomb(self.x+1, self.y+1),
        ))

    @property
    def symbol(self) -> str:
        if not self._revealed:
            return '*' if self.flagged else 'x'
        if self._has_mine:
            return '!'
        # Revealed and without a mine
        return str(self.value)

    def reveal(self, *, update_gui = True):
        """Reveals the cell. Can cause gamestate to change to game_over"""
        return self._grid.reveal_cell(self.x, self.y, update_gui = update_gui)