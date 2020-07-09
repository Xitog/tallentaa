# -----------------------------------------------------------
# MIT Licence (Expat License Wording)
# -----------------------------------------------------------
# Copyright © 2020, Damien Gouteux
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# For more information about transitions see:
# https://xitog.github.io/dgx/passetemps/tech_transitions.html (in French)

"""Transitions of tilesets"""

#-------------------------------------------------------------------------------
# Encoding
#-------------------------------------------------------------------------------

# Calc from Env return a result on 12 bits

# The 3 first bits indicated from which tilesets we are transiting
# [D]eep < [W]ater < [M]ud < [G]rass < dark g[R]ass
#                          < dr[Y] mud
# no trans 0 000
# D < W    1 001
# W < M    2 010
# M < Y    3 011
# M < G    4 100
# G < R    5 101
# unused   6 110
# error    7 111

# The 4 next bits indicated the borders on which we are transiting
# Only 1 or 2 borders can be transiting:
# 1. North 1000/8, East 0100/4, South 0010/2, West 0001/1 => 4
# 2. North+East 1100/12, East+South 0110/6, South+West 0011/3, West+North 1001/9 => 4
# It could be put on 3 bits but we are keeping an extra bit to make more human-readable

# The 4 next bits indicated the corners on which we are transiting
# Only 1 or 2 corners can be transiting:
# 1. Northwest 1000/8, Northeast 0100/4, Southeast 0010/2, Southwest 0001/1 => 4
# 2. Northwest + Southeast 1010/10, Northeast + Southwest 0101/5 => 2

# The final bit is to indicated if we use an alternate tile, for more variety.

# Tweaks

# "Normal" case are encoded on 8 bits. But normal tiles are also encoded into the transition matrix:
# No transitive tiles are encoded as : 0000 then the 8 bits of the normal.
# The 8 bits of base tile:
# Deep   0001 1
# Water  0010 2
# Mud    0011 3
# Dry    0100 4
# Grass  0101 5
# Dark   0110 6
# Unused 0111 7
# Unused 1000 8... (we can have 16 tilesets)
# Then a code designating its tiles:
# 0000 (we can have 16 variants)

# ==RULE: IF THERE IS NO BORDERS WE CONSIDER THE CORNERS==
# Corners are then translated into unused border slot
# 0000 Unused
# 0001 BORDER WEST
# 0010 BORDER SOUTH
# 0011 BORDERS SOUTH + WEST
# 0100 BORDER EAST
# 0101 We can't have East+West ==> Northwest
# 0110 BORDERS EAST + SOUTH
# 0111 We can't have West+South+East ==> Northeast
# 1000 BORDER NORTH
# 1001 BORDERS NORTH + WEST
# 1010 We can't have North+South ==> Southeast
# 1011 We can't have North+South+West ==> Southwest
# 1100 BORDERS NORTH + EAST
# 1101 We can't have North+East+West ==> Northwest + Southeast
# 1110 We can't have North+East+South ==> Northeast + Southwest
# 1111 We can't have all borders ==> Unused

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

from PIL import Image
from PIL import ImageDraw
from os.path import join
from collections import namedtuple
#from random import randint

#-------------------------------------------------------------------------------
# Constants and globals
#-------------------------------------------------------------------------------

DEEP  = 0b00000000 #  0
WATER = 0b00010000 # 16
MUD   = 0b00100000 # 32
DRY   = 0b00110000 # 48
GRASS = 0b01000000 # 64
DARK  = 0b01010000 # 80

ALLOWED_TRANSITIONS = {
    WATER: {DEEP:  0b001},
    MUD:   {WATER: 0b010},
    DRY:   {MUD:   0b011},
    GRASS: {MUD:   0b100},
    DARK:  {GRASS: 0b101}
}

TRANSITIONS = {}
ERROR = None

DEBUG = 0 #0, 1 or 2

RANDOM=[0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0]
COUNT=0

RANDOM_BASE = {
    DEEP:  [0, 0, 1],
    WATER: [0, 0, 1, 1, 0, 2, 3, 4, 5, 0, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 0, 0, 4, 3, 3, 2, 2, 1, 7,
            0, 0, 1, 1, 0, 2, 3, 4, 5, 0, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 0, 0, 4, 3, 3, 2, 2, 1, 8],
    MUD:   [0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    DRY:   [0, 0, 1],
    GRASS: [0, 0, 1],
    DARK:  [0, 0, 1]
}
COUNT_BASE = {DEEP: 0, WATER: 0, MUD: 0, DRY: 0, GRASS: 0, DARK: 0}

NORTHWEST = 0
NORTH     = 1
NORTHEAST = 2
EAST      = 3
SOUTHEAST = 4
SOUTH     = 5
SOUTHWEST = 6
WEST      = 7

#-------------------------------------------------------------------------------
# Types
#-------------------------------------------------------------------------------

# Classes TransitionException, Map, Named tuples Transition and Diff

Transition = namedtuple('Transition', ['transition', 'borders', 'corners', 'merged', 'alternate'])
Diff = namedtuple('Diff', ['first', 'last', 'length'])

class TransitionException(Exception):
    pass

class Map:

    def __init__(self, title, width=None, height=None, default=0):
        self.title = title
        if (width is None or height is None) and not isinstance(default, list) and len(default) == 0:
            raise Exception(f'You must provide a valid default if width or height are None')
        self.width = width if width is not None else len(default[0])
        self.height = height if height is not None else len(default)
        self.content = []
        if isinstance(default, int):
            for col in range(self.width):
                self.content.append([])
                for row in range(self.height):
                    self.content[-1].append(default)
        elif isinstance(default, list):
            for col in range(self.width):
                self.content.append([])
                for row in range(self.height):
                    self.content[-1].append(default[row][col])
        else:
            raise Exception(f'Cannot build a Map from {type(default)}')

    def invert(self):
        inverted = []
        for row in range(self.height):
            inverted.append([])
            for col in range(self.width):
                inverted[-1].append(self.content[col][row])
        return inverted

    def info(self):
        print(f'= {self.title} =')
        display = self.invert()
        for row in range(self.height):
            print(f'row={row}', display[row])

    def __getitem__(self, val):
        return self.content[val]

    def set(self, col, row, val):
        self.content[col][row] = val

#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------

# randint (supervized randomness), load (texture), calc_num_from_env (map => code environment),
# calc_trans_from_num (code environment => trans), produce_one_image, map_to_image

def seq_rand_int():
    global COUNT
    res = RANDOM[COUNT]
    COUNT += 1
    if COUNT >= len(RANDOM):
        COUNT = 0
    return res


def seq_rand_base(base):
    global RANDOM_BASE, COUNT_BASE
    res = RANDOM_BASE[base][COUNT_BASE[base]]
    COUNT_BASE[base] += 1
    if COUNT_BASE[base] >= len(RANDOM_BASE[base]):
        COUNT_BASE[base] = 0
    return res

def load(constructor=Image.open):
    global TRANSITIONS, ERROR
    origin = r'..\..\assets\sets\rts\tiles'
    # ERROR
    ERROR = constructor(join(origin, 'base', 'error.png'))
    # No transition
    TRANSITIONS[0] = {DEEP: {}, WATER: {}, MUD: {}, DRY: {}, GRASS: {}, DARK: {}}
    # Water tiles
    TRANSITIONS[0][DEEP][0]  = constructor(join(origin, 'base', 'deep-1.png'))
    TRANSITIONS[0][DEEP][1]  = constructor(join(origin, 'base', 'deep-2.png'))
    TRANSITIONS[0][WATER][0] = constructor(join(origin, 'base', 'water-1.png'))
    TRANSITIONS[0][WATER][1] = constructor(join(origin, 'base', 'water-2.png'))
    TRANSITIONS[0][WATER][2] = constructor(join(origin, 'base', 'water-2.png'))
    TRANSITIONS[0][WATER][3] = constructor(join(origin, 'base', 'water-2.png'))
    TRANSITIONS[0][WATER][4] = constructor(join(origin, 'base', 'water-2.png'))
    TRANSITIONS[0][WATER][5] = constructor(join(origin, 'base', 'water-6.png'))
    TRANSITIONS[0][WATER][6] = constructor(join(origin, 'base', 'water-7.png'))
    TRANSITIONS[0][WATER][7] = constructor(join(origin, 'base', 'water-8.png'))
    TRANSITIONS[0][WATER][8] = constructor(join(origin, 'base', 'water-9.png'))
    TRANSITIONS[0][MUD][0]   = constructor(join(origin, 'base', 'mud-1.png'))
    TRANSITIONS[0][MUD][1]   = constructor(join(origin, 'base', 'mud-2.png'))
    TRANSITIONS[0][MUD][2]   = constructor(join(origin, 'base', 'mud-3.png'))
    TRANSITIONS[0][MUD][3]   = constructor(join(origin, 'base', 'mud-4.png'))
    TRANSITIONS[0][MUD][4]   = constructor(join(origin, 'base', 'mud-5.png'))
    TRANSITIONS[0][MUD][5]   = constructor(join(origin, 'base', 'mud-6.png'))
    TRANSITIONS[0][DRY][0]   = constructor(join(origin, 'base', 'dry-1.png'))
    TRANSITIONS[0][DRY][1]   = constructor(join(origin, 'base', 'dry-2.png'))
    TRANSITIONS[0][GRASS][0] = constructor(join(origin, 'base', 'grass-1.png'))
    TRANSITIONS[0][GRASS][1] = constructor(join(origin, 'base', 'grass-2.png'))
    TRANSITIONS[0][DARK][0]  = constructor(join(origin, 'base', 'dark-1.png'))
    TRANSITIONS[0][DARK][1]  = constructor(join(origin, 'base', 'dark-2.png'))
    # Water > Deep
    TRANSITIONS[1] = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}, 8: {}, 9: {}, 10: {}, 11: {}, 12: {}, 13: {}, 14: {}}
    TRANSITIONS[1][0][0]  = constructor(join(origin, 'base', 'blank-1.png'))
    TRANSITIONS[1][0][1]  = constructor(join(origin, 'base', 'blank-1.png'))
    TRANSITIONS[1][1][0]  = constructor(join(origin, '01_water_deep', 'water-w-deep-1.png'))
    TRANSITIONS[1][1][1]  = constructor(join(origin, '01_water_deep', 'water-w-deep-2.png'))
    TRANSITIONS[1][2][0]  = constructor(join(origin, '01_water_deep', 'water-s-deep-1.png'))
    TRANSITIONS[1][2][1]  = constructor(join(origin, '01_water_deep', 'water-s-deep-2.png'))
    TRANSITIONS[1][3][0]  = constructor(join(origin, '01_water_deep', 'water-sw-deep-1.png'))
    TRANSITIONS[1][3][1]  = constructor(join(origin, '01_water_deep', 'water-sw-deep-2.png'))
    TRANSITIONS[1][4][0]  = constructor(join(origin, '01_water_deep', 'water-e-deep-1.png'))
    TRANSITIONS[1][4][1]  = constructor(join(origin, '01_water_deep', 'water-e-deep-2.png'))
    TRANSITIONS[1][5][0]  = constructor(join(origin, '01_water_deep', 'water-cnw-deep-1.png'))
    TRANSITIONS[1][5][1]  = constructor(join(origin, '01_water_deep', 'water-cnw-deep-2.png'))
    TRANSITIONS[1][6][0]  = constructor(join(origin, '01_water_deep', 'water-es-deep-1.png'))
    TRANSITIONS[1][6][1]  = constructor(join(origin, '01_water_deep', 'water-es-deep-2.png'))
    TRANSITIONS[1][7][0]  = constructor(join(origin, '01_water_deep', 'water-cne-deep-1.png'))
    TRANSITIONS[1][7][1]  = constructor(join(origin, '01_water_deep', 'water-cne-deep-2.png'))
    TRANSITIONS[1][8][0]  = constructor(join(origin, '01_water_deep', 'water-n-deep-1.png'))
    TRANSITIONS[1][8][1]  = constructor(join(origin, '01_water_deep', 'water-n-deep-2.png'))
    TRANSITIONS[1][9][0]  = constructor(join(origin, '01_water_deep', 'water-nw-deep-1.png'))
    TRANSITIONS[1][9][1]  = constructor(join(origin, '01_water_deep', 'water-nw-deep-2.png'))
    TRANSITIONS[1][10][0] = constructor(join(origin, '01_water_deep', 'water-ces-deep-1.png'))
    TRANSITIONS[1][10][1] = constructor(join(origin, '01_water_deep', 'water-ces-deep-2.png'))
    TRANSITIONS[1][11][0] = constructor(join(origin, '01_water_deep', 'water-csw-deep-1.png'))
    TRANSITIONS[1][11][1] = constructor(join(origin, '01_water_deep', 'water-csw-deep-2.png'))
    TRANSITIONS[1][12][0] = constructor(join(origin, '01_water_deep', 'water-ne-deep-1.png'))
    TRANSITIONS[1][12][1] = constructor(join(origin, '01_water_deep', 'water-ne-deep-2.png'))
    TRANSITIONS[1][13][0] = constructor(join(origin, '01_water_deep', 'water-cnwces-deep-1.png'))
    TRANSITIONS[1][13][1] = constructor(join(origin, '01_water_deep', 'water-cnwces-deep-2.png'))
    TRANSITIONS[1][14][0] = constructor(join(origin, '01_water_deep', 'water-cnecsw-deep-1.png'))
    TRANSITIONS[1][14][1] = constructor(join(origin, '01_water_deep', 'water-cnecsw-deep-2.png'))
    # Mud > Water
    TRANSITIONS[2] = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}, 8: {}, 9: {}, 10: {}, 11: {}, 12: {}, 13: {}, 14: {}}
    TRANSITIONS[2][0][0]  = constructor(join(origin, 'base', 'blank-1.png'))
    TRANSITIONS[2][0][1]  = constructor(join(origin, 'base', 'blank-1.png'))
    TRANSITIONS[2][1][0]  = constructor(join(origin, '02_mud_water', 'mud-w-water-1.png'))
    TRANSITIONS[2][1][1]  = constructor(join(origin, '02_mud_water', 'mud-w-water-2.png'))
    TRANSITIONS[2][2][0]  = constructor(join(origin, '02_mud_water', 'mud-s-water-1.png'))
    TRANSITIONS[2][2][1]  = constructor(join(origin, '02_mud_water', 'mud-s-water-2.png'))
    TRANSITIONS[2][3][0]  = constructor(join(origin, '02_mud_water', 'mud-sw-water-1.png'))
    TRANSITIONS[2][3][1]  = constructor(join(origin, '02_mud_water', 'mud-sw-water-2.png'))
    TRANSITIONS[2][4][0]  = constructor(join(origin, '02_mud_water', 'mud-e-water-1.png'))
    TRANSITIONS[2][4][1]  = constructor(join(origin, '02_mud_water', 'mud-e-water-2.png'))
    TRANSITIONS[2][5][0]  = constructor(join(origin, '02_mud_water', 'mud-cnw-water-1.png'))
    TRANSITIONS[2][5][1]  = constructor(join(origin, '02_mud_water', 'mud-cnw-water-2.png'))
    TRANSITIONS[2][6][0]  = constructor(join(origin, '02_mud_water', 'mud-es-water-1.png'))
    TRANSITIONS[2][6][1]  = constructor(join(origin, '02_mud_water', 'mud-es-water-2.png'))
    TRANSITIONS[2][7][0]  = constructor(join(origin, '02_mud_water', 'mud-cne-water-1.png'))
    TRANSITIONS[2][7][1]  = constructor(join(origin, '02_mud_water', 'mud-cne-water-2.png'))
    TRANSITIONS[2][8][0]  = constructor(join(origin, '02_mud_water', 'mud-n-water-1.png'))
    TRANSITIONS[2][8][1]  = constructor(join(origin, '02_mud_water', 'mud-n-water-2.png'))
    TRANSITIONS[2][9][0]  = constructor(join(origin, '02_mud_water', 'mud-nw-water-1.png'))
    TRANSITIONS[2][9][1]  = constructor(join(origin, '02_mud_water', 'mud-nw-water-2.png'))
    TRANSITIONS[2][10][0] = constructor(join(origin, '02_mud_water', 'mud-ces-water-1.png'))
    TRANSITIONS[2][10][1] = constructor(join(origin, '02_mud_water', 'mud-ces-water-2.png'))
    TRANSITIONS[2][11][0] = constructor(join(origin, '02_mud_water', 'mud-csw-water-1.png'))
    TRANSITIONS[2][11][1] = constructor(join(origin, '02_mud_water', 'mud-csw-water-2.png'))
    TRANSITIONS[2][12][0] = constructor(join(origin, '02_mud_water', 'mud-ne-water-1.png'))
    TRANSITIONS[2][12][1] = constructor(join(origin, '02_mud_water', 'mud-ne-water-2.png'))
    TRANSITIONS[2][13][0] = constructor(join(origin, '02_mud_water', 'mud-cnwces-water-1.png'))
    TRANSITIONS[2][13][1] = constructor(join(origin, '02_mud_water', 'mud-cnwces-water-2.png'))
    TRANSITIONS[2][14][0] = constructor(join(origin, '02_mud_water', 'mud-cnecsw-water-1.png'))
    TRANSITIONS[2][14][1] = constructor(join(origin, '02_mud_water', 'mud-cnecsw-water-2.png'))
    # Dry > Mud
    TRANSITIONS[3] = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}, 8: {}, 9: {}, 10: {}, 11: {}, 12: {}, 13: {}, 14: {}}
    TRANSITIONS[3][0][0]  = constructor(join(origin, 'base', 'blank-1.png'))
    TRANSITIONS[3][0][1]  = constructor(join(origin, 'base', 'blank-1.png'))
    TRANSITIONS[3][1][0]  = constructor(join(origin, '03_dry_mud', 'dry-w-mud-1.png'))
    TRANSITIONS[3][1][1]  = constructor(join(origin, '03_dry_mud', 'dry-w-mud-2.png'))
    TRANSITIONS[3][2][0]  = constructor(join(origin, '03_dry_mud', 'dry-s-mud-1.png'))
    TRANSITIONS[3][2][1]  = constructor(join(origin, '03_dry_mud', 'dry-s-mud-2.png'))
    TRANSITIONS[3][3][0]  = constructor(join(origin, '03_dry_mud', 'dry-sw-mud-1.png'))
    TRANSITIONS[3][3][1]  = constructor(join(origin, '03_dry_mud', 'dry-sw-mud-2.png'))
    TRANSITIONS[3][4][0]  = constructor(join(origin, '03_dry_mud', 'dry-e-mud-1.png'))
    TRANSITIONS[3][4][1]  = constructor(join(origin, '03_dry_mud', 'dry-e-mud-2.png'))
    TRANSITIONS[3][5][0]  = constructor(join(origin, '03_dry_mud', 'dry-cnw-mud-1.png'))
    TRANSITIONS[3][5][1]  = constructor(join(origin, '03_dry_mud', 'dry-cnw-mud-2.png'))
    TRANSITIONS[3][6][0]  = constructor(join(origin, '03_dry_mud', 'dry-es-mud-1.png'))
    TRANSITIONS[3][6][1]  = constructor(join(origin, '03_dry_mud', 'dry-es-mud-2.png'))
    TRANSITIONS[3][7][0]  = constructor(join(origin, '03_dry_mud', 'dry-cne-mud-1.png'))
    TRANSITIONS[3][7][1]  = constructor(join(origin, '03_dry_mud', 'dry-cne-mud-2.png'))
    TRANSITIONS[3][8][0]  = constructor(join(origin, '03_dry_mud', 'dry-n-mud-1.png'))
    TRANSITIONS[3][8][1]  = constructor(join(origin, '03_dry_mud', 'dry-n-mud-2.png'))
    TRANSITIONS[3][9][0]  = constructor(join(origin, '03_dry_mud', 'dry-nw-mud-1.png'))
    TRANSITIONS[3][9][1]  = constructor(join(origin, '03_dry_mud', 'dry-nw-mud-2.png'))
    TRANSITIONS[3][10][0] = constructor(join(origin, '03_dry_mud', 'dry-ces-mud-1.png'))
    TRANSITIONS[3][10][1] = constructor(join(origin, '03_dry_mud', 'dry-ces-mud-2.png'))
    TRANSITIONS[3][11][0] = constructor(join(origin, '03_dry_mud', 'dry-csw-mud-1.png'))
    TRANSITIONS[3][11][1] = constructor(join(origin, '03_dry_mud', 'dry-csw-mud-2.png'))
    TRANSITIONS[3][12][0] = constructor(join(origin, '03_dry_mud', 'dry-ne-mud-1.png'))
    TRANSITIONS[3][12][1] = constructor(join(origin, '03_dry_mud', 'dry-ne-mud-2.png'))
    TRANSITIONS[3][13][0] = constructor(join(origin, '03_dry_mud', 'dry-cnwces-mud-1.png'))
    TRANSITIONS[3][13][1] = constructor(join(origin, '03_dry_mud', 'dry-cnwces-mud-2.png'))
    TRANSITIONS[3][14][0] = constructor(join(origin, '03_dry_mud', 'dry-cnecsw-mud-1.png'))
    TRANSITIONS[3][14][1] = constructor(join(origin, '03_dry_mud', 'dry-cnecsw-mud-2.png'))
    # Grass > Mud
    TRANSITIONS[4] = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}, 8: {}, 9: {}, 10: {}, 11: {}, 12: {}, 13: {}, 14: {}}
    TRANSITIONS[4][0][0]  = constructor(join(origin, 'base', 'blank-1.png'))
    TRANSITIONS[4][0][1]  = constructor(join(origin, 'base', 'blank-1.png'))
    TRANSITIONS[4][1][0]  = constructor(join(origin, '04_grass_mud', 'grass-w-mud-1.png'))
    TRANSITIONS[4][1][1]  = constructor(join(origin, '04_grass_mud', 'grass-w-mud-2.png'))
    TRANSITIONS[4][2][0]  = constructor(join(origin, '04_grass_mud', 'grass-s-mud-1.png'))
    TRANSITIONS[4][2][1]  = constructor(join(origin, '04_grass_mud', 'grass-s-mud-2.png'))
    TRANSITIONS[4][3][0]  = constructor(join(origin, '04_grass_mud', 'grass-sw-mud-1.png'))
    TRANSITIONS[4][3][1]  = constructor(join(origin, '04_grass_mud', 'grass-sw-mud-2.png'))
    TRANSITIONS[4][4][0]  = constructor(join(origin, '04_grass_mud', 'grass-e-mud-1.png'))
    TRANSITIONS[4][4][1]  = constructor(join(origin, '04_grass_mud', 'grass-e-mud-2.png'))
    TRANSITIONS[4][5][0]  = constructor(join(origin, '04_grass_mud', 'grass-cnw-mud-1.png'))
    TRANSITIONS[4][5][1]  = constructor(join(origin, '04_grass_mud', 'grass-cnw-mud-2.png'))
    TRANSITIONS[4][6][0]  = constructor(join(origin, '04_grass_mud', 'grass-es-mud-1.png'))
    TRANSITIONS[4][6][1]  = constructor(join(origin, '04_grass_mud', 'grass-es-mud-2.png'))
    TRANSITIONS[4][7][0]  = constructor(join(origin, '04_grass_mud', 'grass-cne-mud-1.png'))
    TRANSITIONS[4][7][1]  = constructor(join(origin, '04_grass_mud', 'grass-cne-mud-2.png'))
    TRANSITIONS[4][8][0]  = constructor(join(origin, '04_grass_mud', 'grass-n-mud-1.png'))
    TRANSITIONS[4][8][1]  = constructor(join(origin, '04_grass_mud', 'grass-n-mud-2.png'))
    TRANSITIONS[4][9][0]  = constructor(join(origin, '04_grass_mud', 'grass-nw-mud-1.png'))
    TRANSITIONS[4][9][1]  = constructor(join(origin, '04_grass_mud', 'grass-nw-mud-2.png'))
    TRANSITIONS[4][10][0] = constructor(join(origin, '04_grass_mud', 'grass-ces-mud-1.png'))
    TRANSITIONS[4][10][1] = constructor(join(origin, '04_grass_mud', 'grass-ces-mud-2.png'))
    TRANSITIONS[4][11][0] = constructor(join(origin, '04_grass_mud', 'grass-csw-mud-1.png'))
    TRANSITIONS[4][11][1] = constructor(join(origin, '04_grass_mud', 'grass-csw-mud-2.png'))
    TRANSITIONS[4][12][0] = constructor(join(origin, '04_grass_mud', 'grass-ne-mud-1.png'))
    TRANSITIONS[4][12][1] = constructor(join(origin, '04_grass_mud', 'grass-ne-mud-2.png'))
    TRANSITIONS[4][13][0] = constructor(join(origin, '04_grass_mud', 'grass-cnwces-mud-1.png'))
    TRANSITIONS[4][13][1] = constructor(join(origin, '04_grass_mud', 'grass-cnwces-mud-2.png'))
    TRANSITIONS[4][14][0] = constructor(join(origin, '04_grass_mud', 'grass-cnecsw-mud-1.png'))
    TRANSITIONS[4][14][1] = constructor(join(origin, '04_grass_mud', 'grass-cnecsw-mud-2.png'))
    # Dark > Grass
    TRANSITIONS[5] = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}, 8: {}, 9: {}, 10: {}, 11: {}, 12: {}, 13: {}, 14: {}}
    TRANSITIONS[5][0][0]  = constructor(join(origin, 'base', 'blank-1.png'))
    TRANSITIONS[5][0][1]  = constructor(join(origin, 'base', 'blank-1.png'))
    TRANSITIONS[5][1][0]  = constructor(join(origin, '05_dark_grass', 'dark-w-grass-1.png'))
    TRANSITIONS[5][1][1]  = constructor(join(origin, '05_dark_grass', 'dark-w-grass-2.png'))
    TRANSITIONS[5][2][0]  = constructor(join(origin, '05_dark_grass', 'dark-s-grass-1.png'))
    TRANSITIONS[5][2][1]  = constructor(join(origin, '05_dark_grass', 'dark-s-grass-2.png'))
    TRANSITIONS[5][3][0]  = constructor(join(origin, '05_dark_grass', 'dark-sw-grass-1.png'))
    TRANSITIONS[5][3][1]  = constructor(join(origin, '05_dark_grass', 'dark-sw-grass-2.png'))
    TRANSITIONS[5][4][0]  = constructor(join(origin, '05_dark_grass', 'dark-e-grass-1.png'))
    TRANSITIONS[5][4][1]  = constructor(join(origin, '05_dark_grass', 'dark-e-grass-2.png'))
    TRANSITIONS[5][5][0]  = constructor(join(origin, '05_dark_grass', 'dark-cnw-grass-1.png'))
    TRANSITIONS[5][5][1]  = constructor(join(origin, '05_dark_grass', 'dark-cnw-grass-2.png'))
    TRANSITIONS[5][6][0]  = constructor(join(origin, '05_dark_grass', 'dark-es-grass-1.png'))
    TRANSITIONS[5][6][1]  = constructor(join(origin, '05_dark_grass', 'dark-es-grass-2.png'))
    TRANSITIONS[5][7][0]  = constructor(join(origin, '05_dark_grass', 'dark-cne-grass-1.png'))
    TRANSITIONS[5][7][1]  = constructor(join(origin, '05_dark_grass', 'dark-cne-grass-2.png'))
    TRANSITIONS[5][8][0]  = constructor(join(origin, '05_dark_grass', 'dark-n-grass-1.png'))
    TRANSITIONS[5][8][1]  = constructor(join(origin, '05_dark_grass', 'dark-n-grass-2.png'))
    TRANSITIONS[5][9][0]  = constructor(join(origin, '05_dark_grass', 'dark-nw-grass-1.png'))
    TRANSITIONS[5][9][1]  = constructor(join(origin, '05_dark_grass', 'dark-nw-grass-2.png'))
    TRANSITIONS[5][10][0] = constructor(join(origin, '05_dark_grass', 'dark-ces-grass-1.png'))
    TRANSITIONS[5][10][1] = constructor(join(origin, '05_dark_grass', 'dark-ces-grass-2.png'))
    TRANSITIONS[5][11][0] = constructor(join(origin, '05_dark_grass', 'dark-csw-grass-1.png'))
    TRANSITIONS[5][11][1] = constructor(join(origin, '05_dark_grass', 'dark-csw-grass-2.png'))
    TRANSITIONS[5][12][0] = constructor(join(origin, '05_dark_grass', 'dark-ne-grass-1.png'))
    TRANSITIONS[5][12][1] = constructor(join(origin, '05_dark_grass', 'dark-ne-grass-2.png'))
    TRANSITIONS[5][13][0] = constructor(join(origin, '05_dark_grass', 'dark-cnwces-grass-1.png'))
    TRANSITIONS[5][13][1] = constructor(join(origin, '05_dark_grass', 'dark-cnwces-grass-2.png'))
    TRANSITIONS[5][14][0] = constructor(join(origin, '05_dark_grass', 'dark-cnecsw-grass-1.png'))
    TRANSITIONS[5][14][1] = constructor(join(origin, '05_dark_grass', 'dark-cnecsw-grass-2.png'))


def code_from_env(x, y, matrix):
    msg = []
    try:
        # Get the tilesets
        center = matrix[x][y] & 0b11110000
        north_west = matrix[x-1][y-1] & 0b11110000 if y-1 >= 0 and x-1 >= 0 else center
        north = matrix[x][y-1] & 0b11110000 if y-1 >= 0 else center
        north_east = matrix[x+1][y-1] & 0b11110000 if y-1 >= 0 and x+1 < matrix.width else center
        east = matrix[x+1][y] & 0b11110000 if x+1 < matrix.width else center
        south_east = matrix[x+1][y+1] & 0b11110000 if y+1 < matrix.height and x+1 < matrix.width else center
        south = matrix[x][y+1] & 0b11110000 if y+1 < matrix.height else center
        south_west = matrix[x-1][y+1] & 0b11110000 if y+1 < matrix.height and x-1 >= 0 else center
        west = matrix[x-1][y] & 0b11110000 if x-1 >= 0 else center
        values = [north_west, north, north_east, east, south_east, south, south_west, west]
        modifying_by_val = [] # unique modifying values
        modifying_by_pos = [] # masked surrounding values (if not modifying => center)
        for val in values:
            if val != center:
                if val in ALLOWED_TRANSITIONS and center in ALLOWED_TRANSITIONS[val]:
                    modifying_by_pos.append(val)
                    if val not in modifying_by_val:
                        modifying_by_val.append(val)
                elif center in ALLOWED_TRANSITIONS and val in ALLOWED_TRANSITIONS[center]:
                    # Allowed pair
                    modifying_by_pos.append(center)
                else:
                    # Not an allowed pair
                    msg.append(f'This tileset: {center} has no allowed transitions towards {val}.')
                    raise TransitionException(msg[-1])
            else:
                modifying_by_pos.append(center)
        if DEBUG > 1:
            print()
            print(f'col|x={x}, row|y={y}')
            print(f'center={center}, values={values}')
            print(f'modifying_by_val={modifying_by_val}')
            print(f'modifying_by_pos={modifying_by_pos}')
        # Check only one impacting different tile around me
        if len(modifying_by_val) > 1:
            msg.append(f'Too many modifying tilesets around center at {x} {y}: {modifying_by_val}')
            raise TransitionException(msg[-1])
        elif len(modifying_by_val) == 0:
            # variant
            variant = seq_rand_base(center)
            return center | variant
        elif len(modifying_by_val) == 1:
            diff = modifying_by_val[0]
        # if ok
        trans = ALLOWED_TRANSITIONS[diff][center]
        # Check no sandwiches
        if modifying_by_pos[NORTH] != center and modifying_by_pos[SOUTH] != center:
            msg.append(f'No sandwich North-South at {x},{y}')
            raise TransitionException(msg[-1])
        elif modifying_by_pos[EAST] != center and modifying_by_pos[WEST] != center:
            msg.append(f'No sandwich East-Weast at {x},{y}')
            raise TransitionException(msg[-1])
        # Check no discontinuities
        diff_list = []
        start = None
        for index in range(len(modifying_by_pos)):
            val = modifying_by_pos[index]
            if val != center and start is None:
                start = index
            elif val != center and start is not None:
                pass
            elif val == center and start is None:
                pass
            elif val == center and start is not None:
                diff_list.append(Diff(start, index - 1, index - start)) # first, last, length
                start = None
        #print(f'{diff_list=}')
        if len(diff_list) > 1:
            # Exception: opposite corners
            if len(diff_list) == 2 and diff_list[0].length == 1 and diff_list[1].length == 1 and \
               ((north_west != center and south_east != center) or (north_east != center and south_west != center)):
                pass
            else:
                msg.append('No discontinuities allowed except opposite corners')
                raise TransitionException(msg)
        # Make a binary repr
        code = trans << 9
        if modifying_by_pos[NORTH] != center:
            code |= 0b000100000000
        if modifying_by_pos[EAST] != center:
            code |= 0b000010000000
        if modifying_by_pos[SOUTH] != center:
            code |= 0b000001000000
        if modifying_by_pos[WEST] != center:
            code |= 0b000000100000
        if modifying_by_pos[NORTHWEST] != center:
            code |= 0b000000010000
        if modifying_by_pos[NORTHEAST] != center:
            code |= 0b000000001000
        if modifying_by_pos[SOUTHEAST] != center:
            code |= 0b000000000100
        if modifying_by_pos[SOUTHWEST] != center:
            code |= 0b000000000010
        if DEBUG > 1:
            print(f'diff_list={diff_list} len={len(diff_list)}')
            print(f'code={code:012b}')
    except TransitionException as e:
        if hasattr(e, 'message'):
            print('Exception:', e.message)
        else:
            print('Exception:', e)
        if DEBUG > 0:
            for i, m in enumerate(msg):
                print(f'>>> {x}, {y} | {i}.', m)
        code = 0b111111111111
    return code


def trans_from_code(code):
    global RANDOM
    # Error: rules are broken
    if code == 0b111111111111:
        return Transition(0b111, 0, 0, 0, 0)
    # Which tilesets in this transition?
    transition = (code & 0b111000000000) >> 9
    if transition != 0:
        # Which transition?
        borders = (code & 0b000111100000) >> 5
        corners = (code & 0b000000011110) >> 1
        #alternate = (case & 0b000000000001)
        #alternate = 0 if randint(1, 100) < 50 else 1
        alternate = seq_rand_int()
        # Merge borders & corners, we are storing the corners into unused border slot
        match = {8:0b0101, 4: 0b0111, 2: 0b1010, 1: 0b1011, 10: 0b1101, 5: 0b1110}
        merged = match[corners] if borders == 0 else borders
        return Transition(transition, borders, corners, merged, alternate)
    else:
        # We are storing the tileset into merged and the variant into alternate
        return Transition(transition, 0, 0, (code & 0b11110000), (code & 0b00001111))


def produce_one_image(trans):
    img = Image.new('RGBA', (32, 32))
    img.paste(TRANSITIONS[trans.tilesets][trans.merged][trans.alternate], (0, 0))
    img.save('out.png')


def make_transition(amap, force=False):
    transitive_matrix = []
    for col in range(amap.width):
        transitive_matrix.append([])
        for row in range(amap.height):
            try:
                case = code_from_env(col, row, amap)
                trans = trans_from_code(case)
                transitive_matrix[-1].append(trans)
            except TransitionException as e:
                if not force:
                    raise e
                else:
                    transitive_matrix[-1].append(Transition(0b111, 0, 0, 0, 0))
    return transitive_matrix


def get_img(trans):
    if trans.transition == 0b111:
        return ERROR
    else:
        return TRANSITIONS[trans.transition][trans.merged][trans.alternate]

def map_to_image(amap, output, force=False):
    transtive_matrix = make_transition(amap, force)
    img = Image.new('RGBA', (amap.width * 32, amap.height * 32))
    for col in range(amap.width):
        for row in range(amap.height):
            trans = transtive_matrix[col][row]
            tex = get_img(trans)
            img.paste(tex, (col * 32, row * 32))
            if DEBUG > 0:
                draw = ImageDraw.Draw(img)
                draw.rectangle((col * 32, row * 32, (col + 1) * 32, (row + 1) * 32), fill=None, outline=(0, 0, 0, 255))
    if DEBUG > 0:
        output = output.replace('.png', '_debug.png')
    img.save(output)


if __name__ == '__main__':
    load()

    print()
    mymap = Map('Map 1', 3, 3, [ [WATER, MUD, WATER], [WATER, WATER, WATER], [WATER, WATER, WATER] ])
    mymap.info()
    #map_to_image(mymap, 'out1.png')
    
    print()
    mymap = Map('Map 2', 5, 5, [
        [WATER, WATER, WATER, WATER, WATER],
        [WATER, MUD,   MUD,   MUD,   WATER],
        [WATER, MUD,   GRASS, MUD,   WATER],
        [WATER, MUD,   MUD,   MUD,   WATER],
        [WATER, WATER, WATER, WATER, WATER]
    ])
    mymap.info()
    #map_to_image(mymap, 'out2.png')
    
    print()
    mymap = Map('Map 3', 7, 7, [
        [GRASS, MUD,   MUD,   WATER, WATER, MUD,   GRASS],
        [GRASS, MUD,   MUD,   WATER, WATER, MUD,   GRASS],
        [GRASS, MUD,   MUD,   WATER, WATER, MUD,   GRASS],
        [GRASS, MUD,   MUD,   WATER, WATER, MUD,   GRASS],
        [GRASS, MUD,   MUD,   WATER, WATER, MUD,   MUD  ],
        [GRASS, GRASS, MUD,   WATER, WATER, WATER, MUD  ],
        [GRASS, GRASS, MUD,   MUD,   WATER, WATER, MUD  ]
    ])
    mymap.info()
    #map_to_image(mymap, 'out3.png')

    print()
    mymap = Map('Error Map 1', 3, 3, [
            [MUD,   MUD,   MUD  ],
            [GRASS, MUD,   GRASS],
            [GRASS, GRASS, GRASS]
    ])
    mymap.info()
    #map_to_image(mymap, 'error_map_1.png')

    print()
    mymap = Map('Dry on mud 1 (out 4)', 3, 3, [
            [MUD, MUD, DRY],
            [MUD, DRY, DRY],
            [MUD, MUD, MUD]
    ])
    mymap.info()
    #map_to_image(mymap, 'out_4.png')

    print()
    mymap = Map('All (out 5)', 12, 8, [
            [DEEP, DEEP, WATER, WATER, WATER, MUD,   DRY,   MUD,   MUD, GRASS, DARK,  DARK ],
            [DEEP, DEEP, WATER, WATER, WATER, MUD,   DRY,   MUD,   MUD, GRASS, GRASS, DARK ],
            [DEEP, DEEP, WATER, WATER, WATER, MUD,   MUD,   MUD,   MUD, GRASS, GRASS, DARK ],
            [DEEP, DEEP, WATER, WATER, WATER, MUD,   MUD,   MUD,   MUD, GRASS, GRASS, DARK ],
            [DEEP, DEEP, DEEP,  DEEP,  WATER, WATER, WATER, MUD,   MUD, MUD,   GRASS, GRASS],
            [DEEP, DEEP, DEEP,  DEEP,  DEEP,  WATER, WATER, WATER, MUD, MUD,   GRASS, GRASS],
            [DEEP, DEEP, DEEP,  DEEP,  DEEP,  WATER, WATER, WATER, MUD, MUD,   GRASS, GRASS],
            [DEEP, DEEP, DEEP,  DEEP,  DEEP,  WATER, WATER, WATER, MUD, MUD,   GRASS, GRASS]
    ])
    mymap.info()
    #map_to_image(mymap, 'out_5_variant.png')

    print()
    mymap = Map('Variants (out 6)', 10, 10, [
        [WATER, WATER, WATER, WATER, WATER, WATER, WATER, WATER, WATER, WATER],
        [WATER, WATER, WATER, WATER, WATER, WATER, WATER, WATER, WATER, WATER],
        [WATER, WATER, WATER, WATER, WATER, WATER, WATER, WATER, WATER, WATER],
        [WATER, WATER, WATER, WATER, WATER, WATER, WATER, WATER, WATER, WATER],
        [WATER, WATER, WATER, WATER, WATER, WATER, WATER, WATER, WATER, WATER],
        [WATER, WATER, WATER, WATER, WATER, WATER, WATER, WATER, WATER, WATER],
        [WATER, WATER, WATER, WATER, WATER, WATER, WATER, WATER, WATER, WATER],
        [WATER, WATER, WATER, WATER, WATER, WATER, WATER, WATER, WATER, WATER],
        [WATER, WATER, WATER, WATER, WATER, WATER, WATER, WATER, WATER, WATER],
        [WATER, WATER, WATER, WATER, WATER, WATER, WATER, WATER, WATER, WATER],
    ])
    mymap.info()
    #map_to_image(mymap, 'out_6.png')

    print()
    mymap = Map('Variant mud big (out 7)', 20, 20, MUD)
    mymap.info()
    #map_to_image(mymap, 'out_7.png')
    
    print()
    import example
    mymap = Map('Very big map (out 8)', default=example.mymap)
    map_to_image(mymap, 'out_8.png', force=True)
    
    print()
    #code = code_from_env(1, 1, mymap)
    code = 0b010100000000 # 12 bits : mud on water at N - BORDERS : NESW CORNERS : NW NE SE SW - alternate or not
    trans = trans_from_code(code)
    #print(f'{trans.transition=:b}')
    if trans.transition == 2:
        print('2: mud on water (m > w)')
    #print(f'{trans.borders=:b}')
    #print(f'{trans.corners=:b}')
    #print(f'{trans.alternate=:b}')    
    #produce_one_image(trans)
