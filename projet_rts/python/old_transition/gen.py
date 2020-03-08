import pygame
import os

pygame.init()

GREEN = (0, 153, 0)
BROWN = (173, 112, 50)
BLUE = (0, 0, 153)

size = [400, 300]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("256 cases")

positions = [
        [0, 0],
        [32, 0],
        [64, 0],
        [0, 32],
        #[32, 32],
        [64, 32],
        [0, 64],
        [32, 64],
        [64, 64]
    ]

def generate_combinations(dirname):
    base = GREEN
    transition = BLUE
    try:
        os.chdir(dirname)
    except FileNotFoundError:
        os.mkdir(dirname)
        os.chdir(dirname)
    i = 0
    while i < 256:
        s = pygame.Surface((96, 96))
        s.fill(base)
        if i & 0b00000001:
            r = (positions[0][0], positions[0][1], 32, 32)
            pygame.draw.rect(s, transition, r, 0)
        if i & 0b00000010:
            r = (positions[1][0], positions[1][1], 32, 32)
            pygame.draw.rect(s, transition, r, 0)
        if i & 0b00000100:
            r = (positions[2][0], positions[2][1], 32, 32)
            pygame.draw.rect(s, transition, r, 0)
        if i & 0b00001000:
            r = (positions[3][0], positions[3][1], 32, 32)
            pygame.draw.rect(s, transition, r, 0)
        if i & 0b00010000:
            r = (positions[4][0], positions[4][1], 32, 32)
            pygame.draw.rect(s, transition, r, 0)
        if i & 0b00100000:
            r = (positions[5][0], positions[5][1], 32, 32)
            pygame.draw.rect(s, transition, r, 0)
        if i & 0b01000000:
            r = (positions[6][0], positions[6][1], 32, 32)
            pygame.draw.rect(s, transition, r, 0)
        if i & 0b10000000:
            r = (positions[7][0], positions[7][1], 32, 32)
            pygame.draw.rect(s, transition, r, 0)
        #if i & 0b10000000:
        #    r = (positions[8][0], positions[8][1], 32, 32)
        #    pygame.draw.rect(s, GREEN, r, 0)
        try:
            pygame.image.save(s, str(i) + ".png")
        except Exception as e:
            print(e.__class__, " : ", e)
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

def generate_map(size):
    random.seed()
    content = []
    s = pygame.Surface((size * 32, size * 32))
    for iline in range(size):
        line = []
        for icolumn in range(size):
            val = random.choice([0, 1])
            line.append(val)
            if val == 0:
                color = GREEN
            elif val == 1:
                color = BLUE
            pygame.draw.rect(s, color, (iline*32, icolumn*32, 32, 32), 0)
        content.append(line)
    name = "map_" + str(time.time())
    pygame.image.save(s, name  + ".png")
    return content, size, name

myfont = pygame.font.SysFont("monospace", 12)

def get(worldmap, line, column):
    return worldmap[line][column]

def transitive_map(worldmap, size, name):
    errors = []
    transitions = {
        0 : pygame.image.load("0-ground.png"),
        1 : pygame.image.load("001.png"),
        2 : pygame.image.load("002.png"),
        3 : pygame.image.load("003.png"),
        4 : pygame.image.load("004.png"),
        5 : pygame.image.load("005.png"),
        6 : pygame.image.load("006.png"),
        7 : pygame.image.load("007.png"),
        8 : pygame.image.load("008.png"),
        9 : pygame.image.load("009.png"),
        10 : pygame.image.load("010.png"),
        11 : pygame.image.load("011.png"),
        12 : pygame.image.load("012.png"),
        13 : pygame.image.load("013.png"),
        14 : pygame.image.load("014.png"),
        15 : pygame.image.load("015.png"),
        19 : pygame.image.load("019.png"),
        23 : pygame.image.load("023.png"),
        27 : pygame.image.load("027.png"),
        31 : pygame.image.load("031.png"),
        38 : pygame.image.load("038.png"),
        39 : pygame.image.load("039.png"),
        46 : pygame.image.load("046.png"),
        47 : pygame.image.load("047.png"),
        57 : pygame.image.load("057.png"),
        65 : pygame.image.load("065.png"),
        76 : pygame.image.load("076.png"),
        77 : pygame.image.load("077.png"),
        78 : pygame.image.load("078.png"),
        79 : pygame.image.load("079.png"),
        95 : pygame.image.load("095.png"),
        114 : pygame.image.load("114.png"),
        115 : pygame.image.load("115.png"),
        133 : pygame.image.load("133.png"),
        137 : pygame.image.load("137.png"),
        139 : pygame.image.load("139.png"),
        141 : pygame.image.load("141.png"),
        143 : pygame.image.load("143.png"),
        156 : pygame.image.load("156.png"),
        160 : pygame.image.load("160.png"),
        175 : pygame.image.load("175.png"),
        194 : pygame.image.load("194.png"),
        213 : pygame.image.load("213.png"),
        215 : pygame.image.load("215.png"),
        232 : pygame.image.load("232.png"),
        251 : pygame.image.load("251.png"),
        270 : pygame.image.load("270.png"),
    }
    water = pygame.image.load("1-water.png")
    s = pygame.Surface((size * 32, size * 32))
    for iline in range(size):
        for icolumn in range(size):
            val = worldmap[iline][icolumn]
            if val == 1: # water, don't do anything
                t = myfont.render("1", 0, (0,0,0))
                s.blit(water, dest=(icolumn*32, iline*32))
                s.blit(t, dest=(icolumn*32+5, iline*32+5))
                continue
            nb = 0
            if iline > 0:
                if get(worldmap, iline-1, icolumn) == 1:
                    nb |= 0b10011
            if iline < size-1:
                if get(worldmap, iline+1, icolumn) == 1:
                    nb |= 0b1001100
            if icolumn > 0:
                if get(worldmap, iline, icolumn-1) == 1:
                    nb |= 0b10001001
            if icolumn < size-1:
                if get(worldmap, iline, icolumn+1) == 1:
                    nb |= 0b100110
            if iline > 0 and icolumn > 0:
                if get(worldmap, iline-1, icolumn-1) == 1:
                    nb |= 0b0001
            if iline > 0 and icolumn < size-1:
                if get(worldmap, iline-1, icolumn+1) == 1:
                    nb |= 0b0010
            if iline < size-1 and icolumn < size-1:
                if get(worldmap, iline+1, icolumn+1) == 1:
                    nb |= 0b0100
            if iline < size-1 and icolumn > 0:
                if get(worldmap, iline+1, icolumn-1) == 1:
                    nb |= 0b1000
            if nb in transitions:
                t = myfont.render(str(nb), 0, (0, 0, 0))
                s.blit(transitions[nb], dest=(icolumn*32, iline*32))
                s.blit(t, dest=(icolumn*32+5, iline*32+5))
            else:
                t = myfont.render(str(nb), 0, (255,0,0))
                s.blit(transitions[0], dest=(icolumn*32, iline*32))
                s.blit(t, dest=(icolumn*32+5, iline*32+5))
            if nb not in transitions:
                if nb not in errors:
                    print(nb)
                    errors.append(nb)
    pygame.image.save(s, name + "_transitive"  + ".png")

#cut("sea-to-grass2.png")
#generate_combinations("generated")
m = [
    [0, 0, 0],
    [1, 0, 0],
    [1, 0, 1],
]
#transitive_map(m, 3, "pipo")
transitive_map(*generate_map(32))

pygame.quit()
