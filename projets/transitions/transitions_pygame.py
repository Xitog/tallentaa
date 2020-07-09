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

"""Transitions of tilesets with PyGame GUI"""

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

from os.path import join
import pygame
from pygame.locals import *
from transitions import Map, DEEP, WATER, MUD, DRY, GRASS, DARK, \
     ALLOWED_TRANSITIONS, ERROR, TRANSITIONS, load, make_transition, get_img

#-------------------------------------------------------------------------------
# Constants and globals
#-------------------------------------------------------------------------------

SCREEN = (640, 480)
FILL = 0

escape = False

#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------

def img(path):
    return pygame.image.load(path)

pygame.init()
pygame.display.set_caption("Test transition")
screen = pygame.display.set_mode(SCREEN, pygame.DOUBLEBUF, 32)
clock = pygame.time.Clock()
load(constructor=img)

mymap = Map('Test', 7, 7, [
        [WATER, WATER, WATER, WATER, WATER, WATER, WATER],
        [WATER, WATER, WATER, WATER, WATER, WATER, WATER],
        [WATER, WATER, WATER, WATER, WATER, WATER, WATER],
        [WATER, WATER, WATER, MUD,   WATER, WATER, WATER],
        [WATER, WATER, WATER, WATER, WATER, WATER, WATER],
        [WATER, WATER, WATER, WATER, WATER, WATER, WATER],
        [WATER, WATER, WATER, WATER, WATER, WATER, WATER]
    ])
mymap.info()
transitive_matrix = make_transition(mymap, True)
transitive = False

Cursor = 2
Cursor_Values = [DEEP, WATER, MUD, DRY, GRASS, DARK]

while not escape:
    for event in pygame.event.get():
        if event.type == QUIT:
            escape = True
        elif event.type == KEYDOWN:
            pass #print('Unicode:', event.unicode, 'Key:', event.key, 'Mod:', event.mod)
        elif event.type == KEYUP:
            if event.key == K_SPACE:
                print('pp')
            elif event.key == K_TAB:
                print('Ouput map')
                transitive = not transitive
            elif event.key == K_DOWN:
                Cursor -= 1
                if Cursor < 0:
                    Cursor = len(Cursor_Values) - 1
            elif event.key == K_UP:
                Cursor += 1
                if Cursor >= len(Cursor_Values):
                    Cursor = 0
        elif event.type == VIDEORESIZE:
            print(f'size={event.size}, width={event.w}, height={event.h}')
        elif event.type == MOUSEMOTION:
            pass #print(f'motion {event.pos} {event.rel} {event.buttons}')
        elif event.type == QUIT:
            escape = True
        elif event.type == MOUSEBUTTONDOWN:
            pass
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                cx = int(event.pos[0]/32)
                cy = int(event.pos[1]/32)
                print(f'ou: {cx} {cy}')
                if 0 <= cx < mymap.width and 0 <= cy < mymap.height:
                    mymap.set(cx, cy, Cursor_Values[Cursor])
                    transitive_matrix = make_transition(mymap, True)
        elif event.type == 1:
            #print(event.state, event.type, event.gain, event.dict)
            if event.gain == 0:
                print('Mouse out')
            elif event.gain == 1:
                print('Mouse in')
        else:
            print(f'event.type={event.type}')
    screen.fill((0,0,0))
    for col in range(mymap.width):
        for row in range(mymap.height):
            if not transitive:
                tex = TRANSITIONS[0][mymap[col][row]][0]
            else:
                trans = transitive_matrix[col][row]
                tex = get_img(trans)
            screen.blit(tex, (col * 32, row * 32))
    screen.blit(TRANSITIONS[0][Cursor_Values[Cursor]][0], (10 * 32, 10 * 32))
    mx, my = pygame.mouse.get_pos()
    pygame.draw.circle(screen, (0, 0, 255), (mx, my), 10, 1)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
