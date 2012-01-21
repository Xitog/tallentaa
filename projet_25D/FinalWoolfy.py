import pygame
from pygame.locals import *

resolution = None
screen = None
clock = None
fps = None

BLACK = (0,0,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SKYBLUE = (0, 255, 255)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)

def init(title, x, y, color=0, pfps=60):
    global resolution, screen, clock, fps
    pygame.init()
    pygame.display.set_caption('Woolfie 3D')
    resolution = (x, y)
    flags = pygame.DOUBLEBUF #| pygame.FULLSCREEN
    if color == 0:
        color = pygame.display.mode_ok(resolution)
    # 0 : not ok
    # !0: best color depth
    screen = pygame.display.set_mode(resolution, flags, color)
    clock = pygame.time.Clock()
    fps = pfps

def render():
    global clock, fps
    pygame.display.flip()
    # Limit to 60 fps maximum
    clock.tick(fps)

init('Woolfie 3D', 640, 480, 32)

play = True
while play:
    
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            play = False
    
    # Draw
    screen.fill(PURPLE)
    
    render()

