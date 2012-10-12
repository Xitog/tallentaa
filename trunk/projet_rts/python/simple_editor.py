#! /usr/bin/env python

# v2: 45m: ajout du sol en plus des doodads. cycle. style objet. +20m ajout des entites.

#-----------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------

import pygame, sys, math, random
from pygame.locals import *

#-----------------------------------------------------------------------
# Global Vars
#-----------------------------------------------------------------------

# mode of edition
SELECT = 0
GROUND = 1
DOODAD = 2
ENTITY = 3
MODE_MAX = 4

#-----------------------------------------------------------------------
# Classes
#-----------------------------------------------------------------------

class Entity:
    def __init__(self, vie_max=100, vie=100):
        self.angle = 1
        self.vie = vie
        self.vie_max = vie_max

class Window:
    
    def __init__(self, x, y, w, h, background_color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.background_color = background_color
    
    def on_event(self, event):
        print event
    
    def draw(self, surf):
        pygame.draw.rect(surf, self.background_color, (self.x, self.y, self.w, self.h), 0)

class Menu(Window):
    
    def __init__(self, editor, x, y, w, h, background_color):
        Window.__init__(self, x, y, w, h, background_color)
        self.editor = editor
    
    def on_event(self, event):
        if event.type == MOUSEBUTTONUP:
            x,y = event.pos
            #print x,y
            #print (x-100)/35
            #print (y-500)/35
            print (x-100)/35 + 19*((y-500)/35)
    
    def draw(self, surf):
        pygame.draw.rect(surf, self.background_color, (self.x, self.y, self.w, self.h), 1)
        
        surf.blit(self.editor.content_img[self.editor.doodad_content], (500, 450))
        if self.editor.ground_content == 0:
            pygame.draw.rect(surf, (0, 0, 255), (400, 500, 32, 32), 0)
        elif self.editor.ground_content == 1:
            pygame.draw.rect(surf, (255, 0, 0), (400, 500, 32, 32), 0)
        pygame.draw.circle(surf, (255, 255, 0), (300+16, 500+16), 16, 0)
        
        if self.editor.mode == GROUND:
            pygame.draw.rect(surf, (255, 255, 0), (390, 490, 128, 128), 1)
            pygame.draw.rect(surf, (255, 255, 0), (8, 500, 80, 25), 1)
            for i in range(0, 22):
                pygame.draw.rect(surf, (i*10, i*10, i*10), (100+(i*35%665),500+(35*((i*35)/665)),32,32), 0)
        elif self.editor.mode == DOODAD:
            pygame.draw.rect(surf, (255, 255, 0), (500, 490, 128, 128), 1)
            pygame.draw.rect(surf, (255, 255, 0), (8, 525, 80, 25), 1)
        elif self.editor.mode == ENTITY:
            pygame.draw.rect(surf, (255, 255, 0), (290, 490, 128, 128), 1)
            pygame.draw.rect(surf, (255, 255, 0), (8, 550, 80, 25), 1)
        
        surf.blit(self.editor.font.render("bonjour", True, (255,255,255)), (10,0))
        surf.blit(self.editor.font.render("ground", True, (255, 255, 255)), (10, 500))
        surf.blit(self.editor.font.render("doodad", True, (255, 255, 255)), (10, 525))
        surf.blit(self.editor.font.render("entity", True, (255, 255, 255)), (10, 550))

class MapView(Window):
    
    def __init__(self, editor, x, y, w, h, background_color):
        Window.__init__(self, x, y, w, h, background_color)
        self.editor = editor
    
    def on_event(self, event):
        pass
    
    def draw(self, surf):
        surf.fill(Color(0, 0, 0, 255))
        for yy in range(0, self.editor.MAX_Y):
            for xx in range(0, self.editor.MAX_X):
                # GROUND
                g = self.editor.ground[yy+self.editor.Y][xx+self.editor.X]
                if g == 0:
                    pygame.draw.rect(surf, (0, 0, 255), (xx*32, yy*32, 32, 32), 0)
                elif g == 1:
                    pygame.draw.rect(surf, (255, 0, 0), (xx*32, yy*32, 32, 32), 0)
                # DOODAD
                r = self.editor.doodad[yy+self.editor.Y][xx+self.editor.X]
                if r > 0:
                    pygame.draw.rect(surf, Color(255, 0, 0, 128), (xx*32, yy*32, 32, 32), 1)
                    surf.blit(self.editor.content_img[r], (xx*32+self.editor.content[r][1],yy*32+self.editor.content[r][2]))
                else:
                    pygame.draw.rect(surf, Color(0, 255, 0, 128), (xx*32, yy*32, 32, 32), 1)
                # ENTITY
                e = self.editor.entity[yy+self.editor.Y][xx+self.editor.X]
                if e != 0:
                    pygame.draw.circle(surf, (255, 255, 0), (xx*32+16, yy*32+16), 16, 0)
        

class Editor:
    
    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode(self.size)

        self.MAP_X = 32
        self.MAP_Y = 32
        self.MAX_X = 24
        self.MAX_Y = 15
        self.X = 0
        self.Y = 0

        self.ground = []
        self.doodad = []
        self.entity = []
        for yy in range(0, self.MAP_Y):
            self.ground.append([])
            self.doodad.append([])
            self.entity.append([])
            for xx in range(0, self.MAP_X):
                self.ground[yy].append(0)
                self.doodad[yy].append(0)
                self.entity[yy].append(0)
                sys.stdout.write(str(self.doodad[yy][xx]))
        print
        self.doodad[4][4] = 1
        self.doodad[31][31] = 1
        self.doodad[3][2] = 1
        self.entity[7][7] = Entity()
        
        self.down = False
        self.up = False
        self.left = False
        self.right = False

        self.apply = False
        self.content = [
            ('none', 0, 0),
            ('tree1', -48, -4*32),
            ('tree2', -48, -4*32),
            ('tree3', -48, -4*32),
        ]
        self.ground_content = 1
        self.doodad_content = 1
        self.MAX_GROUND_CONTENT = 2
        self.MAX_DOODAD_CONTENT = 4
        
        self.mode = GROUND
        
        self.content_img = []
        for c in self.content:
            i =  pygame.image.load(c[0]+'.png').convert()
            i.set_colorkey((255,0,255))
            self.content_img.append(i)
        
        print 'bas : scrolling vers le bas'
        print 'haut : scrolling vers le haut'
        print 'droit : scrolling vers la droite'
        print 'gauche : scrolling vers la gauche'
        print 'espace : changement de motif'
        print 'm (,) : changement de mode (sol / motif)'
        print 'bouton gauche : application motif'
        print 'bouton droit : information'
        
        for i in range(0, random.randint(1, 10)):
            self.build()

        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 32)
        
        self.menu = Menu(self, 0, 32*self.MAX_Y, 32*self.MAX_X, 100, (255, 0, 0))
        self.view = MapView(self, 0, 0, 32*self.MAX_X, 32*self.MAX_Y, (0, 0, 255))
    
    def build(self):
        # ia pour "faire des salles"
        size_x = random.randint(3,10)
        size_y = random.randint(3,10)
        x = random.randint(0, self.MAP_X-size_x-1)
        y = random.randint(0, self.MAP_Y-size_y-1)
        for yy in range(x, x+size_x):
            for xx in range(y, y+size_y):
                self.ground[yy][xx] = 1
        print 'creating a room of ', size_x, 'by', size_y, 'at', x, ',', y
    
    def run(self):
        while 1:
            self.update()
            self.draw()
    
    def update(self):
        #---------------------------------------------------------------
        # IO
        mx, my = pygame.mouse.get_pos()
        mx32 = mx / 32 + self.X
        my32 = my / 32 + self.Y
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: exit()
            elif event.type in [MOUSEBUTTONDOWN, MOUSEBUTTONUP]:
                if mx >= self.menu.x and mx <= self.menu.x + self.menu.w and my >= self.menu.y and my <= self.menu.y + self.menu.h:
                    self.menu.on_event(event)
                else:
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.apply = True
                    elif event.type == MOUSEBUTTONUP:
                        if event.button == 1:
                            self.apply = False
                            if self.mode == SELECT:
                                print 'select'
                        elif event.button == 3:
                            print 'line=', my32, 'column=', mx32, self.Y, self.X
                            if mx32 > 0 and mx32 < self.MAP_X and my32 > 0 and my32 < self.MAP_Y: print self.doodad[my32][mx32]
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
                elif event.key == K_DOWN: self.down = True
                elif event.key == K_UP: self.up = True
                elif event.key == K_LEFT: self.left= True
                elif event.key == K_RIGHT: self.right = True
            elif event.type == KEYUP:
                if event.key == K_DOWN: self.down = False
                elif event.key == K_UP: self.up = False
                elif event.key == K_LEFT: self.left = False
                elif event.key == K_RIGHT: self.right = False
                elif event.key == K_SPACE:
                    if self.mode == DOODAD:
                        self.doodad_content = (self.doodad_content + 1) % self.MAX_DOODAD_CONTENT
                    elif self.mode == GROUND:
                        self.ground_content = (self.ground_content + 1) % self.MAX_GROUND_CONTENT
                elif event.key == K_m:
                    self.mode = (self.mode + 1) % MODE_MAX
                    print self.mode
        
        #---------------------------------------------------------------
        # Update
        if self.left:
            if self.X > 0: 
                self.X -= 1
            print self.X, self.Y
        if self.right:
            if self.X < self.MAP_X-self.MAX_X: 
                self.X += 1
            print self.X, self.Y
        if self.down:
            if self.Y < self.MAP_Y-self.MAX_Y: 
                self.Y += 1
            print self.X, self.Y
        if self.up:
            if self.Y > 0: 
                self.Y -= 1
            print self.X, self.Y
        #if left or right or down or up: print X, Y
        if self.apply:
            if self.mode == DOODAD:
                if mx32 >= 0 and mx32 < self.MAP_X and my32 >= 0 and my32 < self.MAP_Y: self.doodad[my32][mx32] = self.doodad_content
                print 'apply=', self.doodad_content
            elif self.mode == GROUND:
                if mx32 >= 0 and mx32 < self.MAP_X and my32 >= 0 and my32 < self.MAP_Y: self.ground[my32][mx32] = self.ground_content
            elif self.mode == ENTITY:
                if mx32 >= 0 and mx32 < self.MAP_X and my32 >= 0 and my32 < self.MAP_Y: self.entity[my32][mx32] = Entity()
            
    def draw(self):
        self.view.draw(self.screen)
        self.menu.draw(self.screen)
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)

Editor().run()
