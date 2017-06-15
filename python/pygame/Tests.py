import pygame
import time
import math

# https://www.pygame.org/docs/ref/draw.html angles are in radians
# pygame light or dark a surface
# game.py rts.py

def update():
    pass

def render(screen):
    screen.fill((66, 66, 66))
    pygame.draw.circle(screen, (255, 0, 0), (45, 45), 10, 0)
    pygame.draw.rect(screen, (0, 255, 0), (10, 10, 20, 20), 0)
    pygame.draw.arc(screen, (0, 255, 255), (60, 60, 45, 45), 0, math.pi/2, 1)
    pygame.draw.rect(screen, (255, 0, 0), (100, 100, 150, 150), 0)
    screen.blit(black_circle, (100, 100)) #, None, pygame.BLEND_ADD)
    screen.blit(white_circle, (250-64, 250-64)) #, None, pygame.BLEND_ADD)
    pygame.display.flip()

pygame.init()
pygame.display.set_caption("Test")
screen = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF, 32)
start = time.time()
escape = False
update_interval = 6

black_circle = pygame.Surface((64, 64))
black_circle.set_alpha(200, pygame.RLEACCEL)
black_circle.fill((32, 32, 32, 128))
white_circle = pygame.Surface((64, 64))
white_circle.set_alpha(200, pygame.RLEACCEL)
white_circle.fill((255, 255, 255, 128))

while not escape:
    elapsed = time.time() - start
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            escape = True
    if elapsed >= update_interval:
        update()
        start = time.time()
    render(screen)

pygame.quit()
