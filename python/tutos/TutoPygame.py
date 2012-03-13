import pygame
from pygame.locals import *

pygame.init()

pygame.display.set_caption('Woolfie 3D')

resolution = (800,600)
flags = pygame.DOUBLEBUF

print(pygame.display.mode_ok(resolution))
# 0 : not ok
# !0: best color depth

screen = pygame.display.set_mode(resolution,flags,32)

sprite1 = pygame.image.load('flower.png').convert()
sprite1.set_colorkey((255,0,255))

clock = pygame.time.Clock()

escape = False

while not escape:
    clock.tick(60) # Limit to 60 fps maximum
    screen.blit(sprite1, (100, 100))
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            escape = True
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            escape = True
