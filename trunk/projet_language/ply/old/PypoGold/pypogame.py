# http://www.pygame.org/docs/tut/chimp/ChimpLineByLine.html

import pygame
from pygame.locals import *

glb_initialized = False
glb_background = None       # Type = Surface
glb_screen = None
glb_clock = None
glb_stop = False

def pypo_init(parameters):
    if parameters[0].__class__ is not str or parameters[1].__class__ is not int or parameters[2].__class__ is not int: raise Exception("Wrong type")
    if len(parameters) == 4 and parameters[3].__class__ is not bool: raise Exception("Wrong type")
    # check on color
    if len(parameters) > 5: raise Exception("Too much parameters")
    return init(*parameters)

def init(title, x, y, mouse=False, color=(255,255,255)):
    global glb_background, glb_screen, glb_clock
    pygame.init()
    glb_screen = pygame.display.set_mode((x, y))
    pygame.display.set_caption(title)
    if not mouse:
        pygame.mouse.set_visible(0)
    # Init background
    glb_background = pygame.Surface(glb_screen.get_size())
    glb_background = glb_background.convert()
    glb_background.fill(color)
    # Init clock
    glb_clock = pygame.time.Clock()
    print glb_screen.__class__
    return None

p = ["Mouse trap", 640, 480, True]
pypo_init(p)

while not glb_stop:
    #glb_clock.tick(60) # Max 60 fps
    glb_screen.blit(glb_background, (0, 0))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == QUIT:
            glb_stop = True
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            glb_stop = True

