#! /usr/bin/env python

# v2: 45m: ajout du sol en plus des doodads. cycle. style objet. +20m ajout des entites.

#-----------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------

import pygame, sys, math, random, pickle
from pygame.locals import *
from definition import *

#-----------------------------------------------------------------------
# Global Vars
#-----------------------------------------------------------------------

# mode of edition
SELECT = 0
GROUND = 1
DOODAD = 2
ENTITY = 3
MODE_MAX = 4

ENTITY_DATA = [ '900', '904', '908', '912', '916', '920', '924', '928', '932', '936', '940', '944', '948', '952', '956', 'tour_ico', 'bat1_ico' ]
DOODAD_DATA = [ '900', 'tree1_ico', 'tree2_ico', 'tree3_ico']

ENTITY_15 = None # TOWER 15
ENTITY_16 = None


#-----------------------------------------------------------------------
# Classes
#-----------------------------------------------------------------------

# sx, sy = modifier pour dessin only!
# tx, ty = taille x,y
class Entity:
    def __init__(self, x, y, cat, sx=0, sy=0, tx=1, ty=1, vie_max=100, vie=100):
        self.angle = 1
        self.vie = vie
        self.vie_max = vie_max
        self.x = x
        self.y = y
        self.cat = cat
        self.sx = sx
        self.sy = sy
        self.tx = tx
        self.ty = ty

class Window:
    
    def __init__(self, x, y, w, h, background_color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.background_color = background_color
    
    def collide(self, x, y):
        return x >= self.x and x <= self.x + self.w and y >= self.y and y <= self.y + self.h
    
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
            self.editor.apply = False
            x,y = event.pos
            #print x,y
            #print (x-100)/35
            #print (y-500)/35 
            # 14*35 = 490 et 19*35=665
            i = (x-200)/35 + 14*((y-500)/35)
            if self.editor.mode == GROUND and i < len(TEXTURES) and i >= 0:
                self.editor.ground_content = i
            elif self.editor.mode == ENTITY and i < len(ENTITY_DATA) and i >= 0:
                self.editor.entity_content = i
            elif self.editor.mode == DOODAD and i < len(DOODAD_DATA) and i >= 0:
                self.editor.doodad_content = i
            if x <= 97:
                b = (y-self.editor.MAX_Y*32)/32
                if b == 0: self.editor.mode = SELECT
                elif b == 1: self.editor.mode = GROUND
                elif b == 2: self.editor.mode = DOODAD
            elif x > 97 and x <= 96*2:
                b = (y-self.editor.MAX_Y*32)/32
                if b == 0: self.editor.mode = ENTITY
                print b
    
    def draw(self, surf):
        global ENTITY_15, ENTITY_16 # TOWER 15
        
        pygame.draw.rect(surf, (0,0,0), (self.x, self.y, self.w, self.h), 0)
        pygame.draw.rect(surf, (0,162,232), (self.x, self.y, self.w, self.h), 1)
        
        # Les lignes du bas et de separation avec les boutons du menu
        pygame.draw.line(surf, (0, 162, 232), (0,self.editor.MAX_Y*32+97), (self.editor.MAX_X*32,self.editor.MAX_Y*32+97), 1)
        pygame.draw.line(surf, (0, 162, 232), (96*2+1,self.editor.MAX_Y*32), (96*2+1,(self.editor.MAX_Y+3)*32), 1)
        pygame.draw.line(surf, (0, 162, 232), ((self.editor.MAX_X-3)*32-1,self.editor.MAX_Y*32), ((self.editor.MAX_X-3)*32-1,(self.editor.MAX_Y+3)*32), 1)

        if self.editor.mode == SELECT:
            pass
        elif self.editor.mode == GROUND:
            for i in range(0, len(TEXTURES)):
                surf.blit(TEXTURES[i].content_ico, (200+(i*35%490),500+(35*((i*35)/490))))
            #for i in range(0, len(GROUND_DATA)):
            #    surf.blit(GROUND_DATA[i], (200+(i*35%490),500+(35*((i*35)/490))))
            pygame.draw.rect(surf, (255, 255, 0), (200+(self.editor.ground_content*35%490)-2,500+(35*((self.editor.ground_content*35)/490))-2,32+2,32+2), 2)
        elif self.editor.mode == DOODAD:
            for i in range(0, len(DOODAD_DATA)):
                surf.blit(DOODAD_DATA[i], (200+(i*35%490),500+(35*((i*35)/490))))
            pygame.draw.rect(surf, (255, 255, 0), (200+(self.editor.doodad_content*35%490)-2,500+(35*((self.editor.doodad_content*35)/490))-2,32+2,32+2), 2)
            # La croix pour "pas de doodad"
            pygame.draw.line(surf, (255, 0, 255), (201,501), (231,531), 1)
            pygame.draw.line(surf, (255, 0, 255), (231,501), (201,531), 1)
        elif self.editor.mode == ENTITY:
            for i in range(0, len(ENTITY_DATA)):
                surf.blit(ENTITY_DATA[i], (200+(i*35%490),500+(35*((i*35)/490))))
            pygame.draw.rect(surf, (255, 255, 0), (200+(self.editor.entity_content*35%490)-2,500+(35*((self.editor.entity_content*35)/490))-2,32+2,32+2), 2)
            # La croix pour "pas d'entity"
            pygame.draw.line(surf, (255, 0, 255), (201,501), (231,531), 1)
            pygame.draw.line(surf, (255, 0, 255), (231,501), (201,531), 1)
        
        #surf.blit(self.editor.font.render("select", True, (255, 255, 255)), (10, self.editor.MAX_Y*32+5))
        
        if self.editor.mode == SELECT: surf.blit(self.editor.button_select_on, (1, self.editor.MAX_Y*32+1))
        else: surf.blit(self.editor.button_select, (1, self.editor.MAX_Y*32+1))
        if self.editor.mode == GROUND: surf.blit(self.editor.button_ground_on, (1, (self.editor.MAX_Y+1)*32+1))
        else: surf.blit(self.editor.button_ground, (1, (self.editor.MAX_Y+1)*32+1))
        if self.editor.mode == DOODAD: surf.blit(self.editor.button_doodad_on, (1, (self.editor.MAX_Y+2)*32+1))        
        else: surf.blit(self.editor.button_doodad, (1, (self.editor.MAX_Y+2)*32+1))        
        if self.editor.mode == ENTITY: surf.blit(self.editor.button_entity_on, (1+96, (self.editor.MAX_Y+0)*32+1))
        else: surf.blit(self.editor.button_entity, (1+96, (self.editor.MAX_Y+0)*32+1))

        # minimap
        x = (self.editor.MAX_X-3)*32
        y = (self.editor.MAX_Y)*32
        for yy in range(0, self.editor.MAP_Y):
            for xx in range(0, self.editor.MAP_X):
                g = self.editor.ground[yy][xx]
                if g == 100:
                    pygame.draw.rect(surf, (255,255,255), (xx*3+x, yy*3+y+1, 3, 3), 0)
                else:
                    pygame.draw.rect(surf, (255,0,0), (xx*3+x, yy*3+y+1, 3, 3), 0)
        
class MapView(Window):
    
    def __init__(self, editor, x, y, w, h, background_color):
        Window.__init__(self, x, y, w, h, background_color)
        self.editor = editor
    
    def on_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                self.editor.apply = True
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.editor.apply = False
            if self.editor.mode == SELECT:
                mx, my = pygame.mouse.get_pos()
                mx32 = mx / 32 + self.editor.X
                my32 = my / 32 + self.editor.Y
                print 'line=', my32, 'column=', mx32, 'scrollX=', self.editor.X, 'scrollY=', self.editor.Y
                #elif event.button == 3:
                #    if mx32 > 0 and mx32 < self.MAP_X and my32 > 0 and my32 < self.MAP_Y: print self.doodad[my32][mx32]
    
    def draw(self, surf):
        surf.fill(Color(0, 0, 0, 255))
        for yy in range(0, self.editor.MAX_Y+3):
            for xx in range(0, self.editor.MAX_X+1):
                if xx+self.editor.X < self.editor.MAP_X and yy+self.editor.Y < self.editor.MAP_Y:
                    # GROUND
                    g = self.editor.ground[yy+self.editor.Y][xx+self.editor.X]
                    surf.blit(GROUND_DATA[g], (xx*32, yy*32))
                    # DOODAD
                    r = self.editor.doodad[yy+self.editor.Y][xx+self.editor.X]
                    if r > 0:
                        pygame.draw.rect(surf, Color(255, 0, 0, 128), (xx*32, yy*32, 32, 32), 1)
                        surf.blit(self.editor.content_img[r], (xx*32+self.editor.content[r][1],yy*32+self.editor.content[r][2]))
                    #for d in self.editor.doodadx:
                    #    surf.blit(self.editor.content_img[d[0]], ((d[1]-self.editor.X)*32+self.editor.content[d[0]][1],(d[2]-self.editor.Y)*32+self.editor.content[d[0]][2]))
                    #else:
                    #    pygame.draw.rect(surf, Color(0, 255, 0, 128), (xx*32, yy*32, 32, 32), 1)
                    # ENTITY
                    e = self.editor.entity[yy+self.editor.Y][xx+self.editor.X]
                    if e != 0 and e is not None: #surf.blit(ENTITY_DATA[e], (xx*32, yy*32))
                        if e.cat < 15: surf.blit(ENTITY_DATA[e.cat], ((e.x-self.editor.X)*32, (e.y-self.editor.Y)*32))
                        elif e.cat == 15: surf.blit(ENTITY_15, ((e.x-self.editor.X-e.sx)*32, (e.y-self.editor.Y-e.sy)*32)) # TOWER 15
                        elif e.cat == 16: surf.blit(ENTITY_16, ((e.x-self.editor.X-e.sx)*32, (e.y-self.editor.Y-e.sy)*32))
        # mouse
        mx, my = pygame.mouse.get_pos()
        #mx32 = mx / 32 + self.X
        #my32 = my / 32 + self.Y
        if self.editor.mode == GROUND:
            pygame.draw.rect(surf, (0, 0, 255), ((mx/32)*32, (my/32)*32, TEXTURES[self.editor.ground_content].size_x*32, TEXTURES[self.editor.ground_content].size_y*32), 1)

class Editor:
    
    def load(self):
        # loading of ground data
        for i in range(0, len(GROUND_DEF)):
            GROUND_DATA[GROUND_DEF[i]] = pygame.image.load(DIRECTORY+str(GROUND_DEF[i])+EXTENSION).convert()
            GROUND_DATA[GROUND_DEF[i]].set_colorkey((255,0,255))
        
        # icon creation for texture
        for i in range(0, len(TEXTURES)):
            if TEXTURES[i].ico is None:
                TEXTURES[i].content_ico = GROUND_DATA[TEXTURES[i].tex[0][0]]
            else:
                TEXTURES[i].content_ico = pygame.image.load(DIRECTORY+TEXTURES[i].ico+EXTENSION).convert()
    
    def __init__(self):
        global ENTITY_15, ENTITY_16 # TOWER 15
        
        pygame.init()
        self.size = self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode(self.size)

        self.MAP_X = 32
        self.MAP_Y = 32
        self.MAX_X = 25
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
                self.ground[yy].append(100)
                self.doodad[yy].append(0)
                self.entity[yy].append(0)
                sys.stdout.write(str(self.doodad[yy][xx]))
        print
        self.doodad[4][4] = 1
        self.doodad[31][31] = 1
        self.doodad[3][2] = 1
        self.entity[7][7] = Entity(7, 7, 1) #1
        
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
        self.entity_content = 1
        
        self.mode = GROUND
        
        self.content_img = []
        for c in self.content:
            i =  pygame.image.load(c[0]+'.png').convert()
            i.set_colorkey((255,0,255))
            self.content_img.append(i)
        
        for i in range(0, len(ENTITY_DATA)):
            ENTITY_DATA[i] = pygame.image.load('./media/'+ENTITY_DATA[i]+'.png').convert()
            ENTITY_DATA[i].set_colorkey((255,0,255))
        
        for i in range(0, len(DOODAD_DATA)):
            DOODAD_DATA[i] = pygame.image.load('./media/'+DOODAD_DATA[i]+'.png').convert()
            DOODAD_DATA[i].set_colorkey((255,0,255))
        
        self.load()
        
        ENTITY_15 = pygame.image.load('./media/tour.png').convert() # TOWER 15
        ENTITY_15.set_colorkey((255,0,255))
        ENTITY_16 = pygame.image.load('./media/bat1.png').convert() # TOWER 15
        ENTITY_16.set_colorkey((255,0,255))
        
        self.button_select = pygame.image.load('./media/gui/button_select.png').convert()
        self.button_ground = pygame.image.load('./media/gui/button_ground.png').convert()
        self.button_doodad = pygame.image.load('./media/gui/button_doodad.png').convert()
        self.button_entity = pygame.image.load('./media/gui/button_entity.png').convert()
        self.button_select_on = pygame.image.load('./media/gui/button_select_on.png').convert()
        self.button_ground_on = pygame.image.load('./media/gui/button_ground_on.png').convert()
        self.button_doodad_on = pygame.image.load('./media/gui/button_doodad_on.png').convert()
        self.button_entity_on = pygame.image.load('./media/gui/button_entity_on.png').convert()
        
        print 'bas : scrolling vers le bas'
        print 'haut : scrolling vers le haut'
        print 'droit : scrolling vers la droite'
        print 'gauche : scrolling vers la gauche'
        print 'espace : changement de motif'
        print 'm (,) : changement de mode (sol / motif)'
        print 'bouton gauche : application motif'
        print 'bouton droit : information'
        print 's : save ground map'
        print 'l : load ground map'
        
        for i in range(0, random.randint(1, 10)):
            self.build()

        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 32)
        
        self.menu = Menu(self, 0, 32*self.MAX_Y, 32*self.MAX_X, 32*4, (255, 0, 0))
        self.view = MapView(self, 0, 0, 32*self.MAX_X, 32*self.MAX_Y, (0, 0, 255))
    
    def build(self):
        # ia pour "faire des salles"
        size_x = random.randint(3,10)
        size_y = random.randint(3,10)
        x = random.randint(0, self.MAP_X-size_x-1)
        y = random.randint(0, self.MAP_Y-size_y-1)
        for yy in range(x, x+size_x):
            for xx in range(y, y+size_y):
                self.ground[yy][xx] = 105
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
                if self.menu.collide(mx, my):
                    self.menu.on_event(event)
                elif self.view.collide(mx, my):
                    self.view.on_event(event)
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
                        self.doodad_content = (self.doodad_content + 1) % len(DOODAD_DATA)
                    elif self.mode == GROUND:
                        self.ground_content = (self.ground_content + 1) % len(GROUND_DATA)
                    elif self.mode == ENTITY:
                        self.entity_content = (self.entity_content + 1) % len(ENTITY_DATA)
                elif event.key == K_m:
                    self.mode = (self.mode + 1) % MODE_MAX
                    print self.mode
                elif event.key == K_l:
                    f = file('out.svg', 'r')
                    self.ground = pickle.load(f)
                elif event.key == K_s:
                    f = file('out.svg', 'w')
                    pickle.dump(self.ground, f)
        
        #---------------------------------------------------------------
        # Update
        if self.left or mx < 5:
            if self.X > 0: 
                self.X -= 1
            print self.X, self.Y
        if self.right or mx > 800-5:
            if self.X < self.MAP_X-self.MAX_X: 
                self.X += 1
            print self.X, self.Y
        if self.down or my > 600-5:
            if self.Y < self.MAP_Y-self.MAX_Y: 
                self.Y += 1
            print self.X, self.Y
        if self.up or my < 5:
            if self.Y > 0: 
                self.Y -= 1
            print self.X, self.Y
        #if left or right or down or up: print X, Y
        if self.apply:
            if self.mode == DOODAD:
                if mx32 >= 0 and mx32 < self.MAP_X and my32 >= 0 and my32 < self.MAP_Y: self.doodad[my32][mx32] = self.doodad_content
                #self.doodadx.append((self.doodad_content, mx32, my32))
            elif self.mode == GROUND:
                if mx32 >= 0 and mx32 < self.MAP_X and my32 >= 0 and my32 < self.MAP_Y: #self.ground[my32][mx32] = self.ground_content
                    for v in range(my32, my32+TEXTURES[self.ground_content].size_y):
                        for w in range(mx32, mx32+TEXTURES[self.ground_content].size_x):
                            if TEXTURES[self.ground_content].tex[v-my32][w-mx32] != 0:
                                self.ground[v][w] = TEXTURES[self.ground_content].tex[v-my32][w-mx32]
            elif self.mode == ENTITY:
                if mx32 >= 0 and mx32 < self.MAP_X and my32 >= 0 and my32 < self.MAP_Y: #self.entity[my32][mx32] = self.entity_content
                    u = self.entity[my32][mx32]
                    if u != 0 and u is not None: del u
                    if self.entity_content < 15:
                        self.entity[my32][mx32] = Entity(mx32, my32, self.entity_content)
                    elif self.entity_content == 15:
                        self.entity[my32][mx32] = Entity(mx32, my32, self.entity_content,1,3) # TOWER 15
                    elif self.entity_content == 16:
                        self.entity[my32][mx32] = Entity(mx32, my32, self.entity_content,1,1)
    
    def draw(self):
        self.view.draw(self.screen)
        self.menu.draw(self.screen)
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)

Editor().run()