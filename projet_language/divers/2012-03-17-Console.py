# -*- coding: utf-8 -*-

# Import
import pygame
from pygame.locals import *

import sys

# Init
pygame.init()

pygame.display.set_caption('Woolfie 3D')

resolution = (800,600)
flags = pygame.DOUBLEBUF

print(pygame.display.mode_ok(resolution))
# 0 : not ok
# !0: best color depth

screen = pygame.display.set_mode(resolution,flags,32)

#sprite1 = pygame.image.load('flower.png').convert()
#sprite1.set_colorkey((255,0,255))

clock = pygame.time.Clock()

escape = False

area = [[1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,1,1,1,0,1,0,1,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1]]

position = [212,212]    # position vector (point)
direction = [1,0]       # direction vector
camera = [0, 0.66]      # camera plane (orthogonal to direction vector) 2 * atan(0.66/1.0)=66

modx = 0.0
mody = 0.0

letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',u'é',u'è',u'ê',u'à',u'â',u'ç',u'ô',u'î',u'ù',u'û']
majs = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
numbers = ['1','2','3','4','5','6','7','8','9','0']
others = [' ', '=', '<', '>', '!', '.', ',', ';', ':', '!', '?', '(', ')', '{', '}', '[', ']', '-', '_', '+', '*', '/', '*', '"', "'", '&', '#', '|', '$'] 
authorized_char = letters + others + numbers + majs
lines = []
lines_pos = (10,10)
font_size = 28
current = 0
lines.append('')

ff = pygame.font.SysFont(pygame.font.get_default_font(), font_size)

def reboot():
    global lines, current
    lines = []
    current = 0
    lines.append('')

def interpret():
    global lines
    if len(lines) == 2:
        words = lines[0].split(' ')
        if words[0] == 'say':
            print(words[1])
            reboot()

#delete = False
# initial delay before first repetition, delay between repetition
pygame.key.set_repeat(50,50)

MAX = 30
repeat = MAX

# Main loop
while not escape:
    
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            escape = True
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            escape = True
        elif event.type == KEYDOWN and event.key == K_LEFT:
            modx = -1
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            modx = 1
        elif event.type == KEYDOWN and event.key == K_UP:
            mody = -1
        elif event.type == KEYDOWN and event.key == K_DOWN:
            mody = 1
        elif event.type == KEYDOWN:
            if event.unicode in authorized_char:
                sys.stdout.write(event.unicode)
                sys.stdout.flush()
                lines[current] += event.unicode
            elif event.key == K_RETURN:
                lines.append('')
                current += 1
                interpret()
            elif event.key == K_BACKSPACE:
                #delete = True
                if len(lines[current]) == 0 and current > 0:
                    del lines[current] #lines.remove(lines[current])
                    current -= 1
                else:
                    lines[current] = lines[current][0:len(lines[current])-1]
        elif event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                modx = 0
            elif event.key == K_DOWN or event.key == K_UP:
                mody = 0
            #elif event.key == K_BACKSPACE:
            #    delete = False
    
    #if delete:
    #    if len(lines[current]) and current > 0 == 0:
    #        lines.remove(lines[current])
    #        current -= 1
    #    else:
    #        lines[current] = lines[current][0:len(lines[current])-1]
    
    # Update
    position[0] += modx
    position[1] += mody
    
    # Draw
    screen.fill((0,0,0))
    
    #screen.blit(sprite1, (100, 100))
    
    for i in range(0, len(area)):
        line = area[i]
        for j in range(0, len(line)):
            #print(len(area))
            #print(len(line))
            #print(i,j,line[j])
            #raw_input()
            #exit()
            rx = j * 10 + 200
            ry = i * 10 + 200
            if line[j] == 1:
                color = (0,255,0)
            else:
                color = (255,255,255)
            pygame.draw.rect(screen, color, (rx,ry,10,10), 0)
    
    screen.set_at((int(position[0]), int(position[1])), (255,0,0))
    
    for i in range(0, len(lines)):
        x = lines_pos[0]
        y = lines_pos[1] + i * font_size
        screen.blit(ff.render(lines[i], True, (255,0,255), (0,0,0)), (x,y))
        last_x = lines_pos[0] + ff.size(lines[i])[0]
        last_y = y
    
    if repeat >= 5 and repeat < MAX:
        pygame.draw.rect(screen, (255,0,255), (last_x, last_y, 3, font_size), 0)
        repeat += 1
    elif repeat == MAX:
        repeat = 0
    else:
        repeat += 1
    
    screen.blit(ff.render('len     = ' + str(len(lines)), True, (255,0,255), (255,255,255)), (300,10))
    screen.blit(ff.render('current = ' + str(current), True, (255,0,255), (255,255,255)), (300,40))
    screen.blit(ff.render('repeat = ' + str(repeat), True, (255,0,255), (255,255,255)), (300,70))
    
    pygame.display.flip()
    
    # Limit to 60 fps maximum
    clock.tick(60) 
