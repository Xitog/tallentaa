import pygame
import os

# 16h49 : c bon :-)

pygame.init()

GREEN = (0, 153, 0)
BROWN = (173, 112, 50)
BLUE = (0, 0, 153)

size = [400, 300]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("256 cases")

def load_w2_transitions(dirname):
    global TRANSITIONS
    TRANSITIONS.clear()
    TRANSITIONS = {
        0 : pygame.image.load(os.path.join(dirname, "0-ground.png")),
        1 : pygame.image.load(os.path.join(dirname, "001.png")),
        2 : pygame.image.load(os.path.join(dirname, "002.png")),
        4 : pygame.image.load(os.path.join(dirname, "004.png")),
        5 : pygame.image.load(os.path.join(dirname, "005.png")),
        8 : pygame.image.load(os.path.join(dirname, "008.png")),
        10 : pygame.image.load(os.path.join(dirname, "010.png")),
        19 : pygame.image.load(os.path.join(dirname, "019.png")),
        38 : pygame.image.load(os.path.join(dirname, "038.png")),
        55 : pygame.image.load(os.path.join(dirname, "055.png")),
        76 : pygame.image.load(os.path.join(dirname, "076.png")),
        110 : pygame.image.load(os.path.join(dirname, "110.png")),
        137 : pygame.image.load(os.path.join(dirname, "137.png")),
        155 : pygame.image.load(os.path.join(dirname, "155.png")),
        205 : pygame.image.load(os.path.join(dirname, "205.png")),
        'water' : pygame.image.load(os.path.join(dirname, "1-water.png")),
    }
   
def load_transitions(dirname):
    global TRANSITIONS
    TRANSITIONS = {
        0 : pygame.image.load(os.path.join(dirname, "0-ground.png")),
        1 : pygame.image.load(os.path.join(dirname, "001.png")),
        2 : pygame.image.load(os.path.join(dirname, "002.png")),
        3 : pygame.image.load(os.path.join(dirname, "003.png")),
        4 : pygame.image.load(os.path.join(dirname, "004.png")),
        5 : pygame.image.load(os.path.join(dirname, "005.png")),
        6 : pygame.image.load(os.path.join(dirname, "006.png")),
        7 : pygame.image.load(os.path.join(dirname, "007.png")),
        8 : pygame.image.load(os.path.join(dirname, "008.png")),
        9 : pygame.image.load(os.path.join(dirname, "009.png")),
        10 : pygame.image.load(os.path.join(dirname, "010.png")),
        11 : pygame.image.load(os.path.join(dirname, "011.png")),
        12 : pygame.image.load(os.path.join(dirname, "012.png")),
        13 : pygame.image.load(os.path.join(dirname, "013.png")),
        14 : pygame.image.load(os.path.join(dirname, "014.png")),
        15 : pygame.image.load(os.path.join(dirname, "015.png")),
        19 : pygame.image.load(os.path.join(dirname, "019.png")),
        23 : pygame.image.load(os.path.join(dirname, "023.png")),
        27 : pygame.image.load(os.path.join(dirname, "027.png")),
        31 : pygame.image.load(os.path.join(dirname, "031.png")),
        38 : pygame.image.load(os.path.join(dirname, "038.png")),
        39 : pygame.image.load(os.path.join(dirname, "039.png")),
        46 : pygame.image.load(os.path.join(dirname, "046.png")),
        47 : pygame.image.load(os.path.join(dirname, "047.png")), 
        55 : pygame.image.load(os.path.join(dirname, "055.png")), 
        63 : pygame.image.load(os.path.join(dirname, "063.png")), 
        76 : pygame.image.load(os.path.join(dirname, "076.png")),
        77 : pygame.image.load(os.path.join(dirname, "077.png")),
        78 : pygame.image.load(os.path.join(dirname, "078.png")),
        79 : pygame.image.load(os.path.join(dirname, "079.png")),
        95 : pygame.image.load(os.path.join(dirname, "095.png")),
        110 : pygame.image.load(os.path.join(dirname, "110.png")), # corrected from 114 -4
        111 : pygame.image.load(os.path.join(dirname, "111.png")), # corrected from 115 -4
        127 : pygame.image.load(os.path.join(dirname, "127.png")), # corrected from 133 -2-4
        137 : pygame.image.load(os.path.join(dirname, "137.png")),
        139 : pygame.image.load(os.path.join(dirname, "139.png")),
        141 : pygame.image.load(os.path.join(dirname, "141.png")),
        143 : pygame.image.load(os.path.join(dirname, "143.png")),
        155 : pygame.image.load(os.path.join(dirname, "155.png")), # corrected from 156
        159 : pygame.image.load(os.path.join(dirname, "159.png")), # corrected from 160
        175 : pygame.image.load(os.path.join(dirname, "175.png")),
        191 : pygame.image.load(os.path.join(dirname, "191.png")), # corrected from 194
        205 : pygame.image.load(os.path.join(dirname, "205.png")), # corrected from 213
        207 : pygame.image.load(os.path.join(dirname, "207.png")), # corrected from 215
        223 : pygame.image.load(os.path.join(dirname, "223.png")), # corrected from 232
        239 : pygame.image.load(os.path.join(dirname, "239.png")), # corrected from 251
        255 : pygame.image.load(os.path.join(dirname, "255.png")), # corredted from 270
        'water' : pygame.image.load(os.path.join(dirname, "1-water.png")),
    }

def calc(worldmap, iline, icolumn):
    size = len(worldmap)
    nb = 0
    # Bord
    if iline > 0:
        if get(worldmap, iline-1, icolumn) == 1:
            nb |= 0b10011 # 19
    if iline < size-1:
        if get(worldmap, iline+1, icolumn) == 1:
            nb |= 0b1001100
    if icolumn > 0:
        if get(worldmap, iline, icolumn-1) == 1:
            nb |= 0b10001001
    if icolumn < size-1:
        if get(worldmap, iline, icolumn+1) == 1:
            nb |= 0b100110 # 38
    # Angle
    if iline > 0 and icolumn > 0:
        if get(worldmap, iline-1, icolumn-1) == 1:
            nb |= 0b0001
    if iline > 0 and icolumn < size-1:
        if get(worldmap, iline-1, icolumn+1) == 1:
            nb |= 0b0010 # 2
    if iline < size-1 and icolumn < size-1:
        if get(worldmap, iline+1, icolumn+1) == 1:
            nb |= 0b0100
    if iline < size-1 and icolumn > 0:
        if get(worldmap, iline+1, icolumn-1) == 1:
            nb |= 0b1000
    return nb

def generate_combinations(dirname="generated", value=1):
    base = GREEN
    other = BLUE
    positions = [
        [0, 0],
        [32, 0],
        [64, 0],
        [64, 32],
        [64, 64],
        [32, 64],
        [0, 64],
        [0, 32]
    ]
    # all combinations
    combi = []
    # matrix creation
    i = 0
    while i < 256:
        content = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        if i & 0b00000001: # 1
            content[0][0] = 1
        if i & 0b00000010: # 2
            content[0][1] = 1
        if i & 0b00000100: # 4
            content[0][2] = 1
        if i & 0b00001000: # 8
            content[1][2] = 1
        if i & 0b00010000: # 16
            content[2][2] = 1
        if i & 0b00100000: # 32
            content[2][1] = 1
        if i & 0b01000000: # 64
            content[2][0] = 1
        if i & 0b10000000: # 128
            content[1][0] = 1
        combi.append(content)
        i += 1
    # create raw surface
    try:
        os.chdir(dirname)
    except FileNotFoundError:
        os.mkdir(dirname)
        os.chdir(dirname)
    i = 0
    while i < 256:
        content = combi[i]
        # calc transition
        trans = calc(content, 1, 1)
        # draw
        s = pygame.Surface((96, 96))
        s.fill(base)
        if i & 0b00000001: # 1
            r = (positions[0][0], positions[0][1], 32, 32)
            pygame.draw.rect(s, other, r, 0)
        if i & 0b00000010: # 2
            r = (positions[1][0], positions[1][1], 32, 32)
            pygame.draw.rect(s, other, r, 0)
        if i & 0b00000100: # 4
            r = (positions[2][0], positions[2][1], 32, 32)
            pygame.draw.rect(s, other, r, 0)
        if i & 0b00001000: # 8
            r = (positions[3][0], positions[3][1], 32, 32)
            pygame.draw.rect(s, other, r, 0)
        if i & 0b00010000: # 16
            r = (positions[4][0], positions[4][1], 32, 32)
            pygame.draw.rect(s, other, r, 0)
        if i & 0b00100000: # 32
            r = (positions[5][0], positions[5][1], 32, 32)
            pygame.draw.rect(s, other, r, 0)
        if i & 0b01000000: # 64
            r = (positions[6][0], positions[6][1], 32, 32)
            pygame.draw.rect(s, other, r, 0)
        if i & 0b10000000: # 128
            r = (positions[7][0], positions[7][1], 32, 32)
            pygame.draw.rect(s, other, r, 0)
        # draw trans
        if trans in TRANSITIONS:
            t = myfont.render(str(trans), 0, (0, 0, 0))
            w, h = t.get_size()
            s.blit(TRANSITIONS[trans], dest=(32, 32))
            s.blit(t, dest=(48-w/2, 48-h/2)) # 15h51 : centered :-)
        else:
            t = myfont.render(str(trans), 0, (255,0,0))
            w, h = t.get_size()
            s.blit(TRANSITIONS[0], dest=(32, 32))
            s.blit(t, dest=(48-w/2, 48-h/2))
        # save picture on disk
        pygame.image.save(s, str(i) + "_" + format(i, '08b') + "_" + str(trans) + ".png")
        i+=1

def cut(filename):
    original = pygame.image.load(os.path.join("tests", filename))
    i = 0
    w, h = original.get_size()
    nb = 0
    while i < w:
        j = 0
        while j < h:
            s = pygame.Surface((32, 32))
            s.fill(BLUE)
            s.blit(original, dest=(0, 0), area=(i, j, 32, 32))
            pygame.image.save(s, "cut_" + str(nb) + ".png")
            j += 32
            nb += 1
        i += 32

import random
import time

def create_matrix(size, val):
    content = []
    for iline in range(size):
        line = []
        for icolumn in range(size):
            line.append(val)
        content.append(line)
    return content

class WorldMap:
    def __init__(self, name, size, content):
        self.name = name
        self.size = size
        self.content = content
        self.trans = create_matrix(size, 0)
    
    def set_map(self, lin, col, val):
        if val not in [0, 1]:
            Exception("[ERROR] Val out of range!")
        self.content[lin][col] = val

def generate_map(size, name=None):
    if name is None:
        name = "map_" + str(time.time())
    random.seed()
    content = []
    for iline in range(size):
        line = []
        for icolumn in range(size):
            #val = random.choice([0, 1])
            dice = random.randint(1, 6)
            val = 1 if dice > 4 else 0 # 5, 6 = water
            line.append(val)
            if val == 0:
                color = GREEN
            elif val == 1:
                color = BLUE
        content.append(line)
    worldmap = WorldMap(name, size, content)
    return worldmap

def draw_raw_map(worldmap):
    size = worldmap.size
    colors = [GREEN, BLUE]
    surf = pygame.Surface((size * 32, size * 32))
    for iline in range(size):
        for icolumn in range(size):
            val = worldmap.content[iline][icolumn]
            if val not in [0, 1]:
                print("[ERROR] val = ", val)
                exit()
            pygame.draw.rect(surf, colors[val], (icolumn*32, iline*32, 32, 32), 0)
    return surf

def surface_save(surf, dirname, filename):
    old = os.getcwd()
    try:
        os.chdir(dirname)
    except FileNotFoundError:
        os.mkdir(dirname)
        os.chdir(dirname)
    pygame.image.save(surf, filename  + ".png")
    os.chdir(old)

myfont = pygame.font.SysFont("monospace", 12)

def get(worldmap, line, column):
    return worldmap[line][column]

def calc_transitive(worldmap):
    for iline in range(worldmap.size):
        for icolumn in range(worldmap.size):
            val = worldmap.content[iline][icolumn]
            if val == 1:
                worldmap.trans[iline][icolumn] = 1
                continue
            nb = calc(worldmap.content, iline, icolumn)
            worldmap.trans[iline][icolumn] = nb

def draw_transitive_map(worldmap, debug=False):
    errors = []
    water = TRANSITIONS['water']
    surf = pygame.Surface((worldmap.size * 32, worldmap.size * 32))
    for iline in range(worldmap.size):
        for icolumn in range(worldmap.size):
            val = worldmap.content[iline][icolumn]
            if val == 1: # water, don't do anything
                t = myfont.render("1", 0, (0,0,0))
                surf.blit(water, dest=(icolumn*32, iline*32))
                if debug:
                    surf.blit(t, dest=(icolumn*32+5, iline*32+5))
                continue
            nb = worldmap.trans[iline][icolumn]
            if debug:
                if nb in TRANSITIONS:
                    t = myfont.render(str(nb), 0, (0, 0, 0))
                    surf.blit(TRANSITIONS[nb], dest=(icolumn*32, iline*32))
                    surf.blit(t, dest=(icolumn*32+5, iline*32+5))
                else:
                    t = myfont.render(str(nb), 0, (255,0,0))
                    surf.blit(TRANSITIONS[0], dest=(icolumn*32, iline*32))
                    surf.blit(t, dest=(icolumn*32+5, iline*32+5))
                if nb not in TRANSITIONS:
                    if nb not in errors:
                        print(nb)
                        errors.append(nb)
            else:
                surf.blit(TRANSITIONS[nb], dest=(icolumn*32, iline*32))
    return surf

def transform_map_w2(worldmap):
    restart = False
    for iline in range(worldmap.size):
        for icolumn in range(worldmap.size):
            val = worldmap.content[iline][icolumn]
            if val == 1:
                continue
            trans = worldmap.trans[iline][icolumn]
            if trans in TRANSITIONS:
                continue
            else:
                if trans in [3]:
                    worldmap.trans[iline][icolumn] = 19
                elif trans in [6]:
                    worldmap.trans[iline][icolumn] = 38
                elif trans in [7, 23, 39]:
                    worldmap.trans[iline][icolumn] = 55
                elif trans in [9]:
                    worldmap.trans[iline][icolumn] = 137
                elif trans in [11, 27, 139]:
                    worldmap.trans[iline][icolumn] = 155
                elif trans in [12]:
                    worldmap.trans[iline][icolumn] = 76
                elif trans in [13, 77, 141]:
                    worldmap.trans[iline][icolumn] = 205
                elif trans in [14, 46, 78]:
                    worldmap.trans[iline][icolumn] = 110
                elif trans in [15, 31, 47, 63, 79, 95, 111, 127, 143, 159, 175, 191, 207, 223, 239, 255]:
                    worldmap.trans[iline][icolumn] = 1
                    worldmap.set_map(iline, icolumn, 1)
                #restart = True
    #if restart:
    #    transform_map_w2(worldmap)
    return worldmap

def invert_map(worldmap):
    for iline in range(worldmap.size):
        for icolumn in range(worldmap.size):
            val = worldmap.content[iline][icolumn]
            if val == 1:
                worldmap.content[iline][icolumn] = 0
            else:
                worldmap.content[iline][icolumn] = 1
    worldmap.trans = worldmap.content
    return worldmap

TRANSITIONS = {}
load_transitions("transitions_no_border")
#load_transitions("transitions_black_border")

#cut("sea-to-grass2.png")
#generate_combinations()
#m = [
#    [0, 0, 0],
#    [1, 0, 0],
#    [1, 0, 1],
#]
#transitive_map(m, 3, "pipo")
#draw_transitive_map(*generate_map(32), "results")

FIXED = False

if FIXED:
    content = [
        [0, 1, 0],
        [1, 0, 0],
        [0, 1, 0]
    ]
    worldmap = WorldMap("fixed_155", 3, content)
else:
    # 1 generate
    worldmap = generate_map(32)
surf_raw = draw_raw_map(worldmap)
surface_save(surf_raw, "results", worldmap.name + "_raw")
# 2 calc transtive
calc_transitive(worldmap)
surf_trans = draw_transitive_map(worldmap, True)
surface_save(surf_trans, "results", worldmap.name + "_transitive")

# 3 transform
load_w2_transitions("w2_filtered")
transform_map_w2(worldmap)
surf_raw = draw_raw_map(worldmap)
surface_save(surf_raw, "results", worldmap.name + "_raw_transformed")
surf_trans = draw_transitive_map(worldmap, True)
surface_save(surf_trans, "results", worldmap.name + "_transitive_transformed")

# Inversion
invert_map(worldmap)
worldmap.trans = create_matrix(worldmap.size, 0) # 20h25 c bon. ct ça !
surf_raw = draw_raw_map(worldmap)
surface_save(surf_raw, "results", worldmap.name + "_raw_transformed_inv")

calc_transitive(worldmap)
transform_map_w2(worldmap)
surf_trans = draw_transitive_map(worldmap, True)
surface_save(surf_trans, "results", worldmap.name + "_transitive_transformed_inv")

pygame.quit()
