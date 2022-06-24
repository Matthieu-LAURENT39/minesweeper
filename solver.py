# -*- coding: utf-8 -*-
# @Author: Matthieu LAURENT
# @Date:   2022-06-24 14:07:47
# @Last Modified by:   Matthieu LAURENT
# @Last Modified time: 2022-06-24 23:06:51

import random
import time
from typing import Optional
from minesweeper import Minesweeper, GameState, GridCell

DELAY = 0.5
"""How long to wait between each cell reveal, in seconds"""

m = Minesweeper(
    width = 15,
    height = 15,
    mines = 20,
    auto_reveal = True,
    gui=True
)

# m = Minesweeper(
#     width = 15,
#     height = 15,
#     mines = 30,
#     auto_reveal = True,
#     seed = "desuwa",
#     gui=True
# )

# ===== Start of the actual code =====


def find_cell_to_reveal(m: Minesweeper) -> Optional[GridCell]:
    """Returns a cell that is 100% safe to reveal, if any"""
    for cell in m:
        cell: GridCell
        # we do various checks
        
        # Checks if the cell is already revealed
        if cell.revealed:
            if cell.value == len(cell.neighbours):
                # That means all neighbours are mines
                for c in cell.neighbours:
                    c.flagged = True
            
            if cell.value == len(cell.unrevealed_neighbours):
                # We know there are x mines around this cell, and there are also x unrevealed
                # neighbours. Therefore, they must all have mines
                for c in cell.unrevealed_neighbours:
                    c.flagged = True

            if cell.value == len(cell.flagged_neighbours) and cell.revealable_neighbours:
                # If we already know where all the flagged cells are, and there are other neighbors
                # then we know those are safe to reveal
                return cell.revealable_neighbours[0]

            # If we already flagged all mines
            if m.mines_amount == len( m.get_cells(flagged=True) ):
                # then all the other cells are good
                return m.get_cells(revealed=False, flagged=False)[0]


def find_best_unrevealed_cell(m: Minesweeper) -> GridCell:
    """
    Finds the least dangerous unrevealed unflagged cell to reveal
    It could probably be improved a lot
    """
    # The cell and ods that a mine is in it (based on neighbors)
    cells_danger: list[ tuple[int, GridCell] ] = []
    remaining_mines = m.mines_amount - len( m.get_cells(flagged=True) )
    for cell in m.get_cells(revealed=True):
        for potential_cell in cell.get_neighbours(revealed=False, flagged=False):
            # For all cell we could potentially reveal
            # We find the highest odd from every of it's neighbours that it has a mine
            danger = max(
                n.value / len(n.revealable_neighbours)
                for n in potential_cell.get_neighbours(revealed=True, flagged=False)
            )
            cells_danger.append( (danger, potential_cell) )
            
    # We shuffle then sort, so that we get a random one with the lowest value
    # we can do that since sorting is stable
    random.shuffle(cells_danger)
    cells_danger.sort(key=lambda a: a[0])

    return cells_danger[0][1]
    # return random.choice(list(m))


def main():
    print("Starting to solve")

    random_cell = m.get_cell(random.randrange(0, m.width), random.randrange(0, m.height))
    # random_cell = m.get_cell(12,7)
    step = 1
    random_cell.reveal()
    print(f"Step 1: Random cell at {random_cell.x};{random_cell.y}")
    print(m.grid_string)
    
    while m.gamestate == GameState.playing:
        # Do solving here
        print('=' * 20 + '\n')
        step += 1
        cell = find_cell_to_reveal(m)
        if cell is not None:
            # print(repr(cell))
            cell.reveal()
            print(f"Step {step}: Cell {cell.x};{cell.y}")
        else:
            print("Softlock!")
            cell = find_best_unrevealed_cell(m)
            cell.reveal()
            print(f"Step {step}: Trying safest cell at {cell.x};{cell.y}")
            
        print(m.grid_string)
        time.sleep(DELAY)

    print("Finished solving!")
    print(f"Result: {m.gamestate}")
    m._reveal_all()
    print(m.grid_string)
    input()

if __name__ == "__main__":
    main()
