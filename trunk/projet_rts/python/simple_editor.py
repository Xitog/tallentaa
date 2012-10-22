#! /usr/bin/env python

# v2: 45m: ajout du sol en plus des doodads. cycle. style objet. +20m ajout des entites.

#-----------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------

import pygame, sys, math, random, pickle, zipfile, os
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
LAYER2 = 4
MODE_MAX = 5

ENTITY_15 = None # TOWER 15
ENTITY_16 = None

#-----------------------------------------------------------------------
# Classes
#-----------------------------------------------------------------------

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
        self.Y_ELEMENTS = 485
        
    def on_event(self, event):
        if event.type == MOUSEBUTTONUP:
            self.editor.apply = False
            x,y = event.pos
            # 14*35 = 490 et 19*35=665
            if x > 200:
                i = (x-200)/35 + 14*((y-self.Y_ELEMENTS)/35)
                if self.editor.mode == GROUND and i < len(TEXTURES) and i >= 0:
                    self.editor.ground_content = i
                elif self.editor.mode == ENTITY and i < len(ENTITIES) and i >= 0:
                    self.editor.entity_content = i
                elif self.editor.mode == DOODAD and i < len(DOODADS) and i >= 0:
                    self.editor.doodad_content = i
                elif self.editor.mode == LAYER2 and i < len(LAYER2_DATA) and i >= 0:
                    self.editor.layer2_content = i
            elif x <= 97:
                b = (y-self.editor.MAX_Y*32)/32
                if b == 0: self.editor.mode = SELECT
                elif b == 1: self.editor.mode = GROUND
                elif b == 2: self.editor.mode = DOODAD
            elif x > 97 and x <= 96*2:
                b = (y-self.editor.MAX_Y*32)/32
                if b == 0: self.editor.mode = ENTITY
                elif b == 1: self.editor.mode = LAYER2
    
    def draw(self, surf):
        
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
                surf.blit(TEXTURES[i].content_ico, (200+(i*35%490),self.Y_ELEMENTS+(35*((i*35)/490))))
            #for i in range(0, len(GROUND_DATA)):
            #    surf.blit(GROUND_DATA[i], (200+(i*35%490),500+(35*((i*35)/490))))
            pygame.draw.rect(surf, (255, 255, 0), (200+(self.editor.ground_content*35%490)-2,self.Y_ELEMENTS+(35*((self.editor.ground_content*35)/490))-2,32+2,32+2), 2)
        elif self.editor.mode == DOODAD:
            for i in range(0, len(DOODADS)):
                surf.blit(DOODADS[i].ico, (200+(i*35%490),self.Y_ELEMENTS+(35*((i*35)/490))))
            pygame.draw.rect(surf, (255, 255, 0), (200+(self.editor.doodad_content*35%490)-2,self.Y_ELEMENTS+(35*((self.editor.doodad_content*35)/490))-2,32+2,32+2), 2)
            # La croix pour "pas de doodad"
            pygame.draw.line(surf, (255, 0, 255), (201,self.Y_ELEMENTS+1), (231,self.Y_ELEMENTS+31), 1)
            pygame.draw.line(surf, (255, 0, 255), (231,self.Y_ELEMENTS+1), (201,self.Y_ELEMENTS+31), 1)
        elif self.editor.mode == ENTITY:
            for i in range(0, len(ENTITIES)):
                surf.blit(ENTITIES[i].ico, (200+(i*35%490),self.Y_ELEMENTS+(35*((i*35)/490))))
            pygame.draw.rect(surf, (255, 255, 0), (200+(self.editor.entity_content*35%490)-2,self.Y_ELEMENTS+(35*((self.editor.entity_content*35)/490))-2,32+2,32+2), 2)
            # La croix pour "pas d'entity"
            pygame.draw.line(surf, (255, 0, 255), (201,self.Y_ELEMENTS+1), (231,self.Y_ELEMENTS+31), 1)
            pygame.draw.line(surf, (255, 0, 255), (231,self.Y_ELEMENTS+1), (201,self.Y_ELEMENTS+31), 1)
        elif self.editor.mode == LAYER2:
            i = 0
            for k in LAYER2_DATA:
                surf.blit(LAYER2_DATA[k].tex, (200+(i*35%490),self.Y_ELEMENTS+(35*((i*35)/490))))
                i+=1
            pygame.draw.rect(surf, (255, 255, 0), (200+(self.editor.layer2_content*35%490)-2,self.Y_ELEMENTS+(35*((self.editor.layer2_content*35)/490))-2,32+2,32+2), 2)
            # La croix pour "pas d'entity"
            pygame.draw.line(surf, (255, 0, 255), (201,self.Y_ELEMENTS+1), (231,self.Y_ELEMENTS+31), 1)
            pygame.draw.line(surf, (255, 0, 255), (231,self.Y_ELEMENTS+1), (201,self.Y_ELEMENTS+31), 1)
        
        #surf.blit(self.editor.font.render("select", True, (255, 255, 255)), (10, self.editor.MAX_Y*32+5))
        
        if self.editor.mode == SELECT: surf.blit(self.editor.button_select_on, (1, self.editor.MAX_Y*32+1))
        else: surf.blit(self.editor.button_select, (1, self.editor.MAX_Y*32+1))
        if self.editor.mode == GROUND: surf.blit(self.editor.button_ground_on, (1, (self.editor.MAX_Y+1)*32+1))
        else: surf.blit(self.editor.button_ground, (1, (self.editor.MAX_Y+1)*32+1))
        if self.editor.mode == DOODAD: surf.blit(self.editor.button_doodad_on, (1, (self.editor.MAX_Y+2)*32+1))        
        else: surf.blit(self.editor.button_doodad, (1, (self.editor.MAX_Y+2)*32+1))        
        if self.editor.mode == ENTITY: surf.blit(self.editor.button_entity_on, (1+96, (self.editor.MAX_Y+0)*32+1))
        else: surf.blit(self.editor.button_entity, (1+96, (self.editor.MAX_Y+0)*32+1))
        if self.editor.mode == LAYER2: surf.blit(self.editor.button_layer2_on, (1+96, (self.editor.MAX_Y+1)*32+1))
        else: surf.blit(self.editor.button_layer2, (1+96, (self.editor.MAX_Y+1)*32+1))

        # minimap
        x = (self.editor.MAX_X-3)*32
        y = (self.editor.MAX_Y)*32
        for yy in range(0, self.editor.MAP_Y):
            for xx in range(0, self.editor.MAP_X):
                #g = self.editor.map.blocks[yy][xx] #self.editor.ground[yy][xx]
                #r = self.editor.map.doodad[yy][xx]
                #if g == 0 and r == 0: #100:
                if not self.editor.map.is_blocked(xx, yy):
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
                print 'line=', my32, 'column=', mx32, 'scrollX=', self.editor.X, 'scrollY=', self.editor.Y, 'doodad=', self.editor.map.doodad[my32][mx32]
                if self.editor.map.doodad[my32][mx32] != 0:
                    self.editor.selected = self.editor.map.doodad[my32][mx32]
                #elif event.button == 3:
                #    if mx32 > 0 and mx32 < self.MAP_X and my32 > 0 and my32 < self.MAP_Y: print self.doodad[my32][mx32]
    
    def draw(self, surf):
        #surf.fill(Color(0, 0, 0, 255))
        #
        # Surface principale
        #
        for yy in range(0, self.editor.MAX_Y+3):
            for xx in range(0, self.editor.MAX_X+1):
                if xx+self.editor.X < self.editor.MAP_X and yy+self.editor.Y < self.editor.MAP_Y:
                    # GROUND
                    g = self.editor.map.ground[yy+self.editor.Y][xx+self.editor.X]
                    layer1 = g % 1000
                    layer2 = (g / 1000)*1000
                    surf.blit(GROUND_DATA[layer1], (xx*32, yy*32))
                    if layer2 != 0: surf.blit(LAYER2_DATA[layer2].tex, (xx*32, yy*32))
                    # DOODAD & ENTITY
                    r = self.editor.map.doodad[yy+self.editor.Y][xx+self.editor.X]
                    if r != 0 and r is not None:
                        surf.blit(r.obj.tex, ((r.x-self.editor.X)*32+r.obj.dev_x,(r.y-self.editor.Y)*32+r.obj.dev_y))
                        if self.editor.selected == r:
                            pygame.draw.rect(surf, (0, 255, 0), ((r.x-self.editor.X)*32,(r.y-self.editor.Y)*32, r.obj.size_x*32, r.obj.size_y*32), 1)
        
        #
        # Curseur de la souris
        #
        mx, my = pygame.mouse.get_pos()
        mx32 = mx / 32 + self.editor.X
        my32 = my / 32 + self.editor.Y
        if self.editor.mode == GROUND:
            # on dessine un rectangle bleu de la taille de la texture.
            pygame.draw.rect(surf, (0, 0, 255), ((mx/32)*32, (my/32)*32, TEXTURES[self.editor.ground_content].size_x*32, TEXTURES[self.editor.ground_content].size_y*32), 1)
        elif self.editor.mode in [ENTITY, DOODAD]:
            if self.editor.mode == ENTITY: obj = ENTITIES[self.editor.entity_content]
            elif self.editor.mode == DOODAD: obj = DOODADS[self.editor.doodad_content]
            # on verifie si il n'y a rien dans [blocks] pour la taille de l'objet (doodad ou entity).
            # si oui, le rectangle du curseur est bleu, rouge sinon.
            there_is_something = False
            for v in range(my32, my32+obj.size_y):
                for w in range(mx32, mx32+obj.size_x):
                    if v >= self.editor.MAP_Y or w >= self.editor.MAP_X or self.editor.map.blocks[v][w] == 1 or self.editor.map.doodad[v][w] != 0:
                        there_is_something = True
            if there_is_something:
                pygame.draw.rect(surf, (255, 0, 0), ((mx/32)*32, (my/32)*32, obj.size_x*32, obj.size_y*32), 1)
            else:
                pygame.draw.rect(surf, (0, 0, 255), ((mx/32)*32, (my/32)*32, obj.size_x*32, obj.size_y*32), 1)
        elif self.editor.mode == LAYER2:
            pygame.draw.rect(surf, (0, 0, 255), ((mx/32)*32, (my/32)*32, 32, 32), 1)

class Map:
    def __init__(self, MAP_X, MAP_Y):
        self.ground = []
        self.doodad = []
        self.blocks = []
        self.MAP_X = MAP_X
        self.MAP_Y = MAP_Y
        for yy in range(0, self.MAP_Y):
            self.ground.append([])
            self.doodad.append([])
            self.blocks.append([])
            for xx in range(0, self.MAP_X):
                self.ground[yy].append(100)
                self.doodad[yy].append(0)
                self.blocks[yy].append(0)
        #        sys.stdout.write(str(self.doodad[yy][xx]))
        #print
    
    def set(self, ref, x, y, layer):
        layer1 = self.ground[y][x] % 1000
        layer2 = (self.ground[y][x] / 1000) * 1000
        if layer == 1:
            layer1 = ref
        else:
            layer2 = ref
        self.ground[y][x] = layer1 + layer2
    
    def is_blocked(self, x, y):
        if self.blocks[y][x] != 0 or self.doodad[y][x] != 0 or self.ground[y][x] >= 1000 : return True
        else: return False
    
    def save(self, name):
        ground_map = file(name+"_ground.map", 'w')
        blocks_map = file(name+"_blocks.map", 'w')
        doodad_map = file(name+"_doodad.map", 'w')
        u = []
        for yy in range(0, self.MAP_Y):
            for xx in range(0, self.MAP_X):
                ground_map.write(str(self.ground[yy][xx])+"\n")
                blocks_map.write(str(self.blocks[yy][xx])+"\n")
                if self.doodad[yy][xx] != 0 and not self.doodad[yy][xx] in u:
                    u.append(self.doodad[yy][xx])
        for i in u:
            if i.obj.__class__ == Doodad:
                doodad_map.write('d,'+i.obj.name_ico+','+str(i.x)+","+str(i.y)+"\n")
            elif i.obj.__class__ == Entity:
                doodad_map.write('e,'+i.obj.name_ico+','+str(i.x)+","+str(i.y)+"\n")
        # zip into one file
        ground_map.close()
        blocks_map.close()
        doodad_map.close()
        save = zipfile.ZipFile(name+'.zip', mode='w')
        save.write(name+"_ground.map")
        save.write(name+"_blocks.map")
        save.write(name+"_doodad.map")
        save.close()
        os.remove(name+"_ground.map")
        os.remove(name+"_blocks.map")
        os.remove(name+"_doodad.map")
        
    def load(self, name):
        load = zipfile.ZipFile(name+'.zip')
        ground_map = load.open(name+"_ground.map")
        #ground_map = file(name+"_ground.map", 'r')
        ground_content = ground_map.readlines()
        blocks_map = load.open(name+"_blocks.map")
        #blocks_map = file(name+"_blocks.map", 'r')
        blocks_content = blocks_map.readlines()
        doodad_map = load.open(name+"_doodad.map")
        #doodad_map = file(name+"_doodad.map", 'r')
        doodad_content = doodad_map.readlines()
        for yy in range(0, self.MAP_Y):
            for xx in range(0, self.MAP_X):
                self.ground[yy][xx] = int(ground_content[yy*self.MAP_Y+xx])
                self.blocks[yy][xx] = int(blocks_content[yy*self.MAP_Y+xx])
                self.doodad[yy][xx] = 0
        for d in doodad_content:
            parts = d.split(',')
            if parts[0] == 'd':
                for doo in DOODADS:
                    if doo.name_ico == parts[1]:
                        #print 'load at x=', int(parts[2]), 'y=', int(parts[3])
                        u = Use(doo, int(parts[2]), int(parts[3]))
                        for v in range(int(parts[2]), int(parts[2])+doo.size_y):
                            for w in range(int(parts[3]), int(parts[3])+doo.size_x):
                                self.doodad[w][v] = u
                                #print 'written', u, 'at v=', v, 'w=', w
                        break
            elif parts[1] == 'e':
                for ent in ENTITIES:
                    if ent.name_ico == parts[1]:
                        u = Use(ent, int(parts[2]), int(parts[3]))
                        for v in range(int(parts[2]), int(parts[2])+ent.size_y):
                            for w in range(int(parts[3]), int(parts[3])+ent.size_x):
                                self.doodad[w][v] = u
                        break

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
        
        # loading doodads icons
        for i in range(0, len(DOODADS)):
            DOODADS[i].ico = pygame.image.load('./media/doodads/'+DOODADS[i].name_ico+'.png').convert()
            DOODADS[i].ico.set_colorkey((255,0,255))
            if DOODADS[i].name_tex is None:
                DOODADS[i].tex = DOODADS[i].ico
            else:
                DOODADS[i].tex = pygame.image.load('./media/doodads/'+DOODADS[i].name_tex+'.png').convert()
                DOODADS[i].tex.set_colorkey((255,0,255))
        
        # loading entities
        for i in range(0, len(ENTITIES)):
            ENTITIES[i].ico = pygame.image.load('./media/entities/'+ENTITIES[i].name_ico+'.png').convert()
            ENTITIES[i].ico.set_colorkey((255,0,255))
            if ENTITIES[i].name_tex is None:
                ENTITIES[i].tex = ENTITIES[i].ico
            else:
                ENTITIES[i].tex = pygame.image.load('./media/entities/'+ENTITIES[i].name_tex+'.png').convert()
                ENTITIES[i].tex.set_colorkey((255,0,255))
        
        # layer2
        for k in LAYER2_DATA:
            LAYER2_DATA[k].tex = pygame.image.load('./media/layer2/'+LAYER2_DATA[k].name+'.png').convert()
            LAYER2_DATA[k].tex.set_colorkey((255,0,255))
        
    def __init__(self):
        
        pygame.init()
        self.size = self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode(self.size)

        self.MAP_X = 32
        self.MAP_Y = 32
        self.MAX_X = 25
        self.MAX_Y = 15
        self.X = 0
        self.Y = 0
        
        self.map = Map(self.MAP_X, self.MAP_Y)
        
        #self.doodad[4][4] = 1
        #self.doodad[31][31] = 1
        #self.doodad[3][2] = 1
        #self.entity[7][7] = Entity(7, 7, 1) #1
        
        self.down = False
        self.up = False
        self.left = False
        self.right = False

        self.apply = False
        self.ground_content = 1
        self.doodad_content = 1
        self.entity_content = 1
        self.layer2_content = 0
        
        self.mode = GROUND
        
        self.load()
        
        self.button_select = pygame.image.load('./media/gui/button_select.png').convert()
        self.button_ground = pygame.image.load('./media/gui/button_ground.png').convert()
        self.button_doodad = pygame.image.load('./media/gui/button_doodad.png').convert()
        self.button_entity = pygame.image.load('./media/gui/button_entity.png').convert()
        self.button_layer2 = pygame.image.load('./media/gui/button_layer2.png').convert()
        self.button_select_on = pygame.image.load('./media/gui/button_select_on.png').convert()
        self.button_ground_on = pygame.image.load('./media/gui/button_ground_on.png').convert()
        self.button_doodad_on = pygame.image.load('./media/gui/button_doodad_on.png').convert()
        self.button_entity_on = pygame.image.load('./media/gui/button_entity_on.png').convert()
        self.button_layer2_on = pygame.image.load('./media/gui/button_layer2_on.png').convert()
        
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
        print 'backspace : delete selected doodad'
        
        # salle aleatoire
        #for i in range(0, random.randint(1, 10)):
        #    self.build()

        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 32)
        
        self.menu = Menu(self, 0, 32*self.MAX_Y, 32*self.MAX_X, 32*4, (255, 0, 0))
        self.view = MapView(self, 0, 0, 32*self.MAX_X, 32*self.MAX_Y, (0, 0, 255))
        
        self.selected = None
        
    def build(self):
        # ia pour "faire des salles"
        size_x = random.randint(3,10)
        size_y = random.randint(3,10)
        x = random.randint(0, self.MAP_X-size_x-1)
        y = random.randint(0, self.MAP_Y-size_y-1)
        for yy in range(x, x+size_x):
            for xx in range(y, y+size_y):
                self.map.ground[yy][xx] = 105
                self.map.blocks[yy][xx] = 1
        print 'creating a room of ', size_x, 'by', size_y, 'at', x, ',', y
    
    def run(self):
        while 1:
            self.update()
            self.draw()
    
    # IO et UPDATE
    def update(self):
        #
        # Get IO
        #
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
                    #f = file('out.svg', 'r')
                    #self.map = pickle.load(f)
                    self.map.load('out')
                elif event.key == K_s:
                    #f = file('out.svg', 'w')
                    #pickle.dump(self.map, f)
                    self.map.save('out')
                elif event.key == K_BACKSPACE:
                    if self.selected is not None:
                        for v in range(self.selected.y, self.selected.y+self.selected.obj.size_y):
                            for w in range(self.selected.x, self.selected.x+self.selected.obj.size_x):
                                self.map.doodad[v][w] = 0
                        del self.selected
                        self.selected = None
        #
        # Scrolling
        #
        if self.left or mx < 5:
            if self.X > 0: 
                self.X -= 1
            #print self.X, self.Y
        if self.right or mx > 800-5:
            if self.X < self.MAP_X-self.MAX_X: 
                self.X += 1
            #print self.X, self.Y
        if self.down or my > 600-5:
            if self.Y < self.MAP_Y-self.MAX_Y: 
                self.Y += 1
            #print self.X, self.Y
        if self.up or my < 5:
            if self.Y > 0: 
                self.Y -= 1
            #print self.X, self.Y
        #
        # Application du curseur
        #
        if self.apply:
            if self.mode == GROUND:
                if mx32 >= 0 and mx32 < self.MAP_X and my32 >= 0 and my32 < self.MAP_Y: #self.ground[my32][mx32] = self.ground_content
                    for v in range(my32, my32+TEXTURES[self.ground_content].size_y):
                        for w in range(mx32, mx32+TEXTURES[self.ground_content].size_x):
                            if TEXTURES[self.ground_content].tex[v-my32][w-mx32] != 0:
                                #self.map.ground[v][w] = TEXTURES[self.ground_content].tex[v-my32][w-mx32]
                                self.map.set(TEXTURES[self.ground_content].tex[v-my32][w-mx32], w, v, 1)
                                self.map.blocks[v][w] = TEXTURES[self.ground_content].passable[v-my32][w-mx32]
            elif self.mode in [DOODAD, ENTITY]:
                if mx32 >= 0 and mx32 < self.MAP_X and my32 >= 0 and my32 < self.MAP_Y:
                    # on empeche de mettre des entities la ou [blocks] est a 1 et si il y a deja un doodad ou une entities
                    if self.mode == ENTITY: obj = ENTITIES[self.entity_content]
                    elif self.mode == DOODAD: obj = DOODADS[self.doodad_content]
                    there_is_something = False
                    for v in range(my32, my32+obj.size_y):
                        for w in range(mx32, mx32+obj.size_x):
                            if v >= self.MAP_Y or w >= self.MAP_X or self.map.blocks[v][w] == 1 or self.map.doodad[v][w] != 0:
                                there_is_something = True
                    if not there_is_something:
                        u = Use(obj, mx32, my32)
                        for v in range(my32, my32+obj.size_y):
                            for w in range(mx32, mx32+obj.size_x):
                                self.map.doodad[v][w] = u
            elif self.mode == LAYER2:
                self.map.set(LAYER2_DATA.keys()[self.layer2_content], mx32, my32, 2)
                #layer1 = self.map.ground[my32][mx32] % 1000
                #self.map.ground[my32][mx32] = layer1 + LAYER2_DATA.keys()[self.layer2_content]
    
    def draw(self):
        self.view.draw(self.screen)
        self.menu.draw(self.screen)
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)

Editor().run()
