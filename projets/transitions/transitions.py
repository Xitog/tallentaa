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

# On 12 bits

# The 3 first bits indicated from which tilesets we are transiting
# [D]eep < [W]ater < [M]ud < [G]rass < dark g[R]ass
#                          < dr[Y] mud
# no trans 0 000
# D < W    1 001
# W < M    2 010
# M < Y    3 011
# M < G    4 100
# G < R    5 101

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

DEBUG = 0 #0, 1 or 2

RANDOM=[0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1]
COUNT=0

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

# Classes Map, Named tuples Transition and Diff

Transition = namedtuple('Transition', ['transition', 'borders', 'corners', 'merged', 'alternate'])
Diff = namedtuple('Diff', ['first', 'last', 'length'])

class Map:

    def __init__(self, width, height, default):
        self.width = width
        self.height = height
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
        display = self.invert()
        for row in range(self.height):
            print(f'{row=}', display[row])

    def __getitem__(self, val):
        return self.content[val]

#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------

# randint (supervized randomness), load (texture), calc_num_from_env (map => code environment),
# calc_trans_from_num (code environment => trans), produce_one_image, map_to_image

def randint():
    global COUNT
    res = RANDOM[COUNT]
    COUNT += 1
    if COUNT >= len(RANDOM):
        COUNT = 0
    return res


def load(TRANSITIONS):
    origin = r'..\..\assets\sets\rts\tiles'
    # No transition
    TRANSITIONS[0] = {DEEP: {}, WATER: {}, MUD: {}, DRY: {}, GRASS: {}, DARK: {}}
    # Water tiles
    TRANSITIONS[0][WATER][0] = Image.open(join(origin, 'base', 'water-1.png'))
    TRANSITIONS[0][WATER][1] = Image.open(join(origin, 'base', 'water-2.png'))
    TRANSITIONS[0][MUD][0] = Image.open(join(origin, 'base', 'mud-1.png'))
    TRANSITIONS[0][MUD][1] = Image.open(join(origin, 'base', 'mud-2.png'))
    TRANSITIONS[0][GRASS][0] = Image.open(join(origin, 'base', 'grass-1.png'))
    # Water > Deep
    #
    # Mud > Water
    TRANSITIONS[2] = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}, 8: {}, 9: {}, 10: {}, 11: {}, 12: {}, 13: {}, 14: {}}
    TRANSITIONS[2][0][0] = Image.open(join(origin, 'base', 'blank-1.png'))
    TRANSITIONS[2][0][1] = Image.open(join(origin, 'base', 'blank-1.png'))
    TRANSITIONS[2][1][0] = Image.open(join(origin, '02_mud_water', 'mud-w-water-1.png'))
    TRANSITIONS[2][1][1] = Image.open(join(origin, '02_mud_water', 'mud-w-water-2.png'))
    TRANSITIONS[2][2][0] = Image.open(join(origin, '02_mud_water', 'mud-s-water-1.png'))
    TRANSITIONS[2][2][1] = Image.open(join(origin, '02_mud_water', 'mud-s-water-2.png'))
    TRANSITIONS[2][3][0] = Image.open(join(origin, '02_mud_water', 'mud-sw-water-1.png'))
    TRANSITIONS[2][3][1] = Image.open(join(origin, '02_mud_water', 'mud-sw-water-2.png'))
    TRANSITIONS[2][4][0] = Image.open(join(origin, '02_mud_water', 'mud-e-water-1.png'))
    TRANSITIONS[2][4][1] = Image.open(join(origin, '02_mud_water', 'mud-e-water-2.png'))
    TRANSITIONS[2][5][0] = Image.open(join(origin, '02_mud_water', 'mud-cnw-water-1.png'))
    TRANSITIONS[2][5][1] = Image.open(join(origin, '02_mud_water', 'mud-cnw-water-2.png'))
    TRANSITIONS[2][6][0] = Image.open(join(origin, '02_mud_water', 'mud-es-water-1.png'))
    TRANSITIONS[2][6][1] = Image.open(join(origin, '02_mud_water', 'mud-es-water-2.png'))
    TRANSITIONS[2][7][0] = Image.open(join(origin, '02_mud_water', 'mud-cne-water-1.png'))
    TRANSITIONS[2][7][1] = Image.open(join(origin, '02_mud_water', 'mud-cne-water-2.png'))
    TRANSITIONS[2][8][0] = Image.open(join(origin, '02_mud_water', 'mud-n-water-1.png'))
    TRANSITIONS[2][8][1] = Image.open(join(origin, '02_mud_water', 'mud-n-water-2.png'))
    TRANSITIONS[2][9][0] = Image.open(join(origin, '02_mud_water', 'mud-nw-water-1.png'))
    TRANSITIONS[2][9][1] = Image.open(join(origin, '02_mud_water', 'mud-nw-water-2.png'))
    TRANSITIONS[2][10][0] = Image.open(join(origin, '02_mud_water', 'mud-ces-water-1.png'))
    TRANSITIONS[2][10][1] = Image.open(join(origin, '02_mud_water', 'mud-ces-water-2.png'))
    TRANSITIONS[2][11][0] = Image.open(join(origin, '02_mud_water', 'mud-csw-water-1.png'))
    TRANSITIONS[2][11][1] = Image.open(join(origin, '02_mud_water', 'mud-csw-water-2.png'))
    TRANSITIONS[2][12][0] = Image.open(join(origin, '02_mud_water', 'mud-ne-water-1.png'))
    TRANSITIONS[2][12][1] = Image.open(join(origin, '02_mud_water', 'mud-ne-water-2.png'))
    TRANSITIONS[2][13][0] = Image.open(join(origin, '02_mud_water', 'mud-cnwces-water-1.png'))
    TRANSITIONS[2][13][1] = Image.open(join(origin, '02_mud_water', 'mud-cnwces-water-2.png'))
    TRANSITIONS[2][14][0] = Image.open(join(origin, '02_mud_water', 'mud-cnecsw-water-1.png'))
    TRANSITIONS[2][14][1] = Image.open(join(origin, '02_mud_water', 'mud-cnecsw-water-2.png'))
    # Dry > Mud
    #
    # Grass > Mud
    TRANSITIONS[4] = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}, 8: {}, 9: {}, 10: {}, 11: {}, 12: {}, 13: {}, 14: {}}
    TRANSITIONS[4][0][0] = Image.open(join(origin, 'base', 'blank-1.png'))
    TRANSITIONS[4][0][1] = Image.open(join(origin, 'base', 'blank-1.png'))
    TRANSITIONS[4][1][0] = Image.open(join(origin, '04_grass_mud', 'grass-w-mud-1.png'))
    TRANSITIONS[4][1][1] = Image.open(join(origin, '04_grass_mud', 'grass-w-mud-2.png'))
    TRANSITIONS[4][2][0] = Image.open(join(origin, '04_grass_mud', 'grass-s-mud-1.png'))
    TRANSITIONS[4][2][1] = Image.open(join(origin, '04_grass_mud', 'grass-s-mud-2.png'))
    TRANSITIONS[4][3][0] = Image.open(join(origin, '04_grass_mud', 'grass-sw-mud-1.png'))
    TRANSITIONS[4][3][1] = Image.open(join(origin, '04_grass_mud', 'grass-sw-mud-2.png'))
    TRANSITIONS[4][4][0] = Image.open(join(origin, '04_grass_mud', 'grass-e-mud-1.png'))
    TRANSITIONS[4][4][1] = Image.open(join(origin, '04_grass_mud', 'grass-e-mud-2.png'))
    TRANSITIONS[4][5][0] = Image.open(join(origin, '04_grass_mud', 'grass-cnw-mud-1.png'))
    TRANSITIONS[4][5][1] = Image.open(join(origin, '04_grass_mud', 'grass-cnw-mud-2.png'))
    TRANSITIONS[4][6][0] = Image.open(join(origin, '04_grass_mud', 'grass-es-mud-1.png'))
    TRANSITIONS[4][6][1] = Image.open(join(origin, '04_grass_mud', 'grass-es-mud-2.png'))
    TRANSITIONS[4][7][0] = Image.open(join(origin, '04_grass_mud', 'grass-cne-mud-1.png'))
    TRANSITIONS[4][7][1] = Image.open(join(origin, '04_grass_mud', 'grass-cne-mud-2.png'))
    TRANSITIONS[4][8][0] = Image.open(join(origin, '04_grass_mud', 'grass-n-mud-1.png'))
    TRANSITIONS[4][8][1] = Image.open(join(origin, '04_grass_mud', 'grass-n-mud-2.png'))
    TRANSITIONS[4][9][0] = Image.open(join(origin, '04_grass_mud', 'grass-nw-mud-1.png'))
    TRANSITIONS[4][9][1] = Image.open(join(origin, '04_grass_mud', 'grass-nw-mud-2.png'))
    TRANSITIONS[4][10][0] = Image.open(join(origin, '04_grass_mud', 'grass-ces-mud-1.png'))
    TRANSITIONS[4][10][1] = Image.open(join(origin, '04_grass_mud', 'grass-ces-mud-2.png'))
    TRANSITIONS[4][11][0] = Image.open(join(origin, '04_grass_mud', 'grass-csw-mud-1.png'))
    TRANSITIONS[4][11][1] = Image.open(join(origin, '04_grass_mud', 'grass-csw-mud-2.png'))
    TRANSITIONS[4][12][0] = Image.open(join(origin, '04_grass_mud', 'grass-ne-mud-1.png'))
    TRANSITIONS[4][12][1] = Image.open(join(origin, '04_grass_mud', 'grass-ne-mud-2.png'))
    TRANSITIONS[4][13][0] = Image.open(join(origin, '04_grass_mud', 'grass-cnwces-mud-1.png'))
    TRANSITIONS[4][13][1] = Image.open(join(origin, '04_grass_mud', 'grass-cnwces-mud-2.png'))
    TRANSITIONS[4][14][0] = Image.open(join(origin, '04_grass_mud', 'grass-cnecsw-mud-1.png'))
    TRANSITIONS[4][14][1] = Image.open(join(origin, '04_grass_mud', 'grass-cnecsw-mud-2.png'))
    # Dark > Grass
    #


def calc_num_from_env(x, y, matrix):
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
                raise Exception(f'This tileset: {center} has no allowed transitions towards {val}.')
        else:
            modifying_by_pos.append(center)
    if DEBUG > 1:
        print()
        print(f'col|{x=}, row|{y=}')
        print(f'{center=}')
        print(f'{values=}')
        print(f'{modifying_by_val=}')
        print(f'{modifying_by_pos=}')
    # Check only one impacting different tile around me
    if len(modifying_by_val) > 1:
        raise Exception(f'Too many modifying tilesets around center at {x} {y}: {modifying_by_val}')
    elif len(modifying_by_val) == 0:
        return center
    elif len(modifying_by_val) == 1:
        diff = modifying_by_val[0]
    # if ok
    trans = ALLOWED_TRANSITIONS[diff][center]
    # Check no sandwiches
    if modifying_by_pos[NORTH] != center and modifying_by_pos[SOUTH] != center:
        raise Exception(f'No sandwich North-South at {x},{y}')
    elif modifying_by_pos[EAST] != center and modifying_by_pos[WEST] != center:
        raise Exception(f'No sandwich East-Weast at {x},{y}')
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
            raise Exception('No discontinuities allowed except opposite corners')
    # Make a binary repr
    final = trans << 9
    if modifying_by_pos[NORTH] != center:
        final |= 0b000100000000
    if modifying_by_pos[EAST] != center:
        final |= 0b000010000000
    if modifying_by_pos[SOUTH] != center:
        final |= 0b000001000000
    if modifying_by_pos[WEST] != center:
        final |= 0b000000100000
    if modifying_by_pos[NORTHWEST] != center:
        final |= 0b000000010000
    if modifying_by_pos[NORTHEAST] != center:
        final |= 0b000000001000
    if modifying_by_pos[SOUTHEAST] != center:
        final |= 0b000000000100
    if modifying_by_pos[SOUTHWEST] != center:
        final |= 0b000000000010
    if DEBUG > 0:
        print(f'{diff_list=} {len(diff_list)=}')
        print(f'{final=:012b}')
    return final


def calc_trans_from_num(case):
    global RANDOM
    # Which tilesets in this transition?
    transition = (case & 0b111000000000) >> 9
    if transition != 0:
        # Which transition?
        borders = (case & 0b000111100000) >> 5
        corners = (case & 0b000000011110) >> 1
        #alternate = (case & 0b000000000001)
        #alternate = 0 if randint(1, 100) < 50 else 1
        alternate = randint()
        # Merge borders & corners, we are storing the corners into unused border slot
        match = {8:0b0101, 4: 0b0111, 2: 0b1010, 1: 0b1011, 10: 0b1101, 5: 0b1110}
        merged = match[corners] if borders == 0 else borders
        return Transition(transition, borders, corners, merged, alternate)
    else:
        # We are storing the tileset into merged and the variant into alternate
        return Transition(transition, 0, 0, (case & 0b11110000), (case & 0b00001111))


def produce_one_image(trans):
    img = Image.new('RGBA', (32, 32))
    img.paste(TRANSITIONS[trans.tilesets][trans.merged][trans.alternate], (0, 0))
    img.save('out.png')


def map_to_image(amap, output):
    img = Image.new('RGBA', (amap.width * 32, amap.height * 32))
    for col in range(amap.width):
        for row in range(amap.height):
            case = calc_num_from_env(col, row, amap)
            trans = calc_trans_from_num(case)
            try:
                img.paste(TRANSITIONS[trans.transition][trans.merged][trans.alternate], (col * 32, row * 32))
                if DEBUG > 0:
                    print(col, row, "outline")
                    draw = ImageDraw.Draw(img)
                    draw.rectangle((col * 32, row * 32, (col + 1) * 32, (row + 1) * 32), fill=None, outline=(0, 0, 0, 255))
            except:
                print(f'KeyError: {trans=}')
    if DEBUG > 0:
        output = output.replace('.png', '_debug.png')
    img.save(output)

if __name__ == '__main__':
    load(TRANSITIONS)

    print('Map 1')
    print()
    mymap = Map(3, 3, [ [WATER, MUD, WATER], [WATER, WATER, WATER], [WATER, WATER, WATER] ])
    mymap.info()
    map_to_image(mymap, 'out1.png')
    print()
    
    print('Map 2')
    print()
    mymap = Map(5, 5, [
        [WATER, WATER, WATER, WATER, WATER],
        [WATER, MUD,   MUD,   MUD,   WATER],
        [WATER, MUD,   GRASS, MUD,   WATER],
        [WATER, MUD,   MUD,   MUD,   WATER],
        [WATER, WATER, WATER, WATER, WATER]
    ])
    mymap.info()
    map_to_image(mymap, 'out2.png')
    print()
    
    print('Map 3')
    print()
    mymap = Map(7, 7, [
        [GRASS, MUD,   MUD,   WATER, WATER, MUD,   GRASS],
        [GRASS, MUD,   MUD,   WATER, WATER, MUD,   GRASS],
        [GRASS, MUD,   MUD,   WATER, WATER, MUD,   GRASS],
        [GRASS, MUD,   MUD,   WATER, WATER, MUD,   GRASS],
        [GRASS, MUD,   MUD,   WATER, WATER, MUD,   MUD  ],
        [GRASS, GRASS, MUD,   WATER, WATER, WATER, MUD  ],
        [GRASS, GRASS, MUD,   MUD,   WATER, WATER, MUD  ]
    ])
    mymap.info()
    map_to_image(mymap, 'out3.png')
    print()
    
    final = calc_num_from_env(1, 1, mymap)
    case = 0b010100000000 # 12 bits : mud on water at N - BORDERS : NESW CORNERS : NW NE SE SW - alternate or not
    trans = calc_trans_from_num(case)
    print(f'{trans.transition=:b}')
    if trans.transition == 2:
        print('2: mud on water (m > w)')
    print(f'{trans.borders=:b}')
    print(f'{trans.corners=:b}')
    print(f'{trans.alternate=:b}')
    
    #produce_one_image(trans)
