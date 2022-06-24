# -*- coding: utf-8 -*-
# @Author: Matthieu LAURENT
# @Date:   2022-06-24 22:56:48
# @Last Modified by:   Matthieu LAURENT
# @Last Modified time: 2022-06-24 23:38:58

# -*- coding: utf-8 -*-
# @Author: Matthieu LAURENT
# @Date:   2022-06-24 14:07:47
# @Last Modified by:   Matthieu LAURENT
# @Last Modified time: 2022-06-24 23:00:03

import random
import time
from typing import Optional
from minesweeper import Minesweeper, GameState, GridCell

m = Minesweeper(
    width = 15,
    height = 15,
    mines = 20,
    auto_reveal = True,
    free_start = True,
    gui=True
)

# ===== Start of the actual code =====

def main():
    print("Starting to solve")

    # You can use free_start to get one free tile to start with, so you don't
    # have to rely on luck.
    # random_cell = m.get_cell(random.randrange(0, m.width), random.randrange(0, m.height))
    # random_cell.reveal()
    # print(m.grid_string)
    
    while m.gamestate == GameState.playing:
        # Do solving here
        pass

        # GUI is auto refreshed when you reveal a cell
        # You can also use the terminal to display the grid with
        # print(m.grid_string)

    print("Finished solving!")
    print(f"Result: {m.gamestate}")
    m._reveal_all()
    print(m.grid_string)
    input()

if __name__ == "__main__":
    main()