# -*- coding: utf-8 -*-

# Import
import pygame
from pygame.locals import *

# Init
pygame.init()
pygame.display.set_caption('Basic PyGame')

resolution = (800,600)
flags = pygame.DOUBLEBUF
screen = pygame.display.set_mode(resolution, flags, 32)

escape = False
clock = pygame.time.Clock()

# Main loop
while not escape:
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            escape = True
    
    # Update
    
    # Draw
    screen.fill((0,0,0))
    pygame.display.flip()

    # Limit to 60 fps maximum
    clock.tick(60)

