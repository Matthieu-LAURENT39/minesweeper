# -*- coding: utf-8 -*-
# @Author: Matthieu LAURENT
# @Date:   2022-06-24 21:17:29
# @Last Modified by:   Matthieu LAURENT
# @Last Modified time: 2022-06-24 21:17:40

from enum import Enum, auto

class GameState(Enum):
    playing = auto()
    game_over = auto()
    victory = auto()