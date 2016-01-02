#! /usr/bin/env python

__version__ = "$Revision: 1 $"

# http://ezide.com/games/code_examples/example.py
# http://pygame.org/docs/ref/draw.html#pygame.draw.rect

# div X and Y by 32 + math.trunc -> give the square where we are
# multiply by 32 -> give where we start to display

import pygame
import math
import sys

from pygame.locals import *
from collections import namedtuple

RED = Color(255, 0, 0)  # TODO Enum Python ?
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
GREY = Color(200, 200, 200)
BLACK = Color(0, 0, 0)
WHITE = Color(255, 255, 255)
YELLOW = Color(255, 255, 0)
SKY_BLUE = Color(0, 255, 255)
HALF_RED = Color(128, 0, 0)
HALF_BLUE = Color(0, 0, 128)
HALF_GREEN = Color(0, 128, 0)

MINIMAP_GREEN_HALF = HALF_GREEN # terre verte
MINIMAP_GREEN_LIGHT = Color(1,154,1) # terre verte claire
MINIMAP_BROWN = Color(192,96,0) # terre marron claire
MINIMAP_BROWN_DARK = Color(128,64,0) # terre marron sombre pas passable (rochers)
MINIMAP_BLUE = BLUE # eau profonde pas passable
MINIMAP_BLUE_LIGHT = Color(113,123,255) # eau claire peu profonde mais pas passable

#UnitType = namedtuple("UnitType", "size range life dom speed reload")  # or ['size', 'range', 'life', 'dom']
#BuildingType = namedtuple("BuildingType", "size range life dom speed reload type")

class Texture:
    def __init__(self, name, num, filename, minicolor, passable=True):
        self.name = name
        self.num = num
        if filename.__class__ == str:
            self.img = pygame.image.load('../../assets/tiles32x32/' + filename)
        elif filename.__class__ == pygame.Surface:
            self.img = filename
        self.mini = minicolor
        self.passable = passable

TEXTURES = {
    # Doodads
      1  : Texture('rock'  ,   1, 'rock_brown.png', MINIMAP_BROWN_DARK),
    # Real textures
    100 : Texture('grass' , 200, 'grass_two_leaves.png', MINIMAP_GREEN_LIGHT),
    200 : Texture('ground', 100, 'ground.png', MINIMAP_BROWN),
    300 : Texture('water' , 300, 'water.png', MINIMAP_BLUE_LIGHT, False),
    
    9100 : Texture('w1', 9100, 'w1.png', MINIMAP_BLUE_LIGHT, False), 
    9200 : Texture('w2', 9200, 'w2.png', MINIMAP_BLUE_LIGHT, False), 
    9300 : Texture('w3', 9300, 'w3.png', MINIMAP_BLUE_LIGHT, False),
    9400 : Texture('w4', 9400, 'w4.png', MINIMAP_BLUE_LIGHT, False), 
    9500 : Texture('w5', 9500, 'w5.png', MINIMAP_BLUE_LIGHT, False), 
    9600 : Texture('w6', 9600, 'w6.png', MINIMAP_BLUE_LIGHT, False), 
    9700 : Texture('w7', 9700, 'w7.png', MINIMAP_BLUE_LIGHT, False), 
    9800 : Texture('w8', 9800, 'w8.png', MINIMAP_BLUE_LIGHT, False), 
    8200 : Texture('x2', 8200, 'x2.png', MINIMAP_BLUE_LIGHT, False), 
    8400 : Texture('x4', 8400, 'x4.png', MINIMAP_BLUE_LIGHT, False),
    8300 : Texture('x24', 8300, 'x24.png', MINIMAP_BLUE_LIGHT, False),
    
    # Computed textures
    # 1300 : Texture('grass_water_lm', 1200, 'grass_water_ml.png', MINIMAP_BLUE_LIGHT, False),
    # minimap color depends !!!
    
    #91 : Texture('w1', 91, 'w1.png', MINIMAP_GREEN_LIGHT, False), 
    #92 : Texture('w2', 92, 'w2.png', MINIMAP_GREEN_LIGHT, False),
    #93 : Texture('w3', 93, 'w3.png', MINIMAP_GREEN_LIGHT, False),
    #94 : Texture('w4', 94, 'w4.png', MINIMAP_GREEN_LIGHT, False),
    #95 : Texture('w5', 95, 'w5.png', MINIMAP_GREEN_LIGHT, False),
    #96 : Texture('w6', 96, 'w6.png', MINIMAP_GREEN_LIGHT, False),
    #97 : Texture('w7', 97, 'w7.png', MINIMAP_GREEN_LIGHT, False),
    #98 : Texture('w8', 98, 'w8.png', MINIMAP_GREEN_LIGHT, False),
}

# Mixing Texture
for a in [9100, 9200, 9300, 9400, 9500, 9600, 9700, 9800, 8200, 8400, 8300]:
    for b in [100]:
        s = pygame.Surface((32,32))
        s.blit(TEXTURES[b].img, (0, 0))
        s.blit(TEXTURES[a].img, (0, 0))
        if a > 9000:
            n = b*10+a-9000
        else:
            n = b*10+1000+a-8000
        TEXTURES[n] = Texture(str(n), n, s, TEXTURES[a].mini, TEXTURES[a].passable)

class Camera:
    def __init__(self, width, height, scroll, player):
        self.width = width
        self.height = height
        self.size = width, height
        self.scroll = scroll
        self.player = player
        self.auto_scroll_zone = 10
        self.game = player.game
        self.x = 0
        self.y = 0
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)  # , pygame.FULLSCREEN | pygame.HWSURFACE)
        self.font = pygame.font.SysFont("monospace", 10)
        self.SELECT_X = 0
        self.SELECT_Y = 0
        self.SELECT_R = False
        self.INTERFACE_Y = 480
        self.selected = []
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.add_mod = False
        self.mode = 'normal'  # or build
        self.build_size = Pair(3, 3)
        self.not_enough_ress = 0
    
    def select_zone(self, x, y, w, h):  # , player)
        x //= 32
        y //= 32
        w //= 32
        h //= 32
        ul = []
        if x == w and y == h:  # a square
            t = self.player.world.unit_map[y][x]
            if self.player.world.is_unit(x, y):
                # if t[1].player == player:
                ul.append(t[1])
        else:  # a zone
            for i in range(x, w):
                for j in range(y, h):
                    # print(i, j)
                    t = self.player.world.unit_map[j][i]
                    if self.player.world.is_unit(i, j):
                        # if t[1].player == player:
                        ul.append(t[1])
        # DEBUG
        for u in ul:
            print(u)
        return ul

    def x2r(self, x):
        return x * 32 + self.x + 16

    def y2r(self, y):
        return y * 32 + self.y + 16

    def update(self):
        self.player.game.update() # here
        
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
                elif event.key == K_DOWN:
                    self.down = True
                elif event.key == K_UP:
                    self.up = True
                elif event.key == K_LEFT:
                    self.left = True
                elif event.key == K_RIGHT:
                    self.right = True
                elif event.key == K_LSHIFT:
                    print('add_mod!')
                    self.add_mod = True
            elif event.type == KEYUP:
                if event.key == K_DOWN:
                    self.down = False
                elif event.key == K_UP:
                    self. up = False
                elif event.key == K_LEFT:
                    self.left = False
                elif event.key == K_RIGHT:
                    self.right = False
                elif event.key == K_LSHIFT:
                    self.add_mod = False
                    print('stop add mod!')
                elif event.key == K_SPACE:
                    self.scroll += 1
                elif event.key == K_b:
                    if self.mode == 'normal':
                        self.mode = 'build'
                    else:
                        self.mode = 'normal'
                    print(self.mode)
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not self.SELECT_R:
                        self.SELECT_R = True
                        self.SELECT_X = mx - self.x
                        self.SELECT_Y = my - self.y
            elif event.type == MOUSEBUTTONUP:
                self.SELECT_R = False
                if event.button == 1:  # Left Button
                    if my > self.INTERFACE_Y and self.SELECT_Y > self.INTERFACE_Y: # Interface click
                        #if self.mode == 'normal':
                        # CLICK FOR A BUILDING
                        a = mx // 32
                        b = (my-self.INTERFACE_Y) // 32
                        # print(a,b)
                        nb = a + b * 3
                        if nb >= 0 and nb < len(self.player.game.all_building_types_ordered):
                            btn = self.player.game.all_building_types_ordered[nb]
                            bt = self.player.game.all_building_types[btn]
                            self.mode = 'build'
                            self.build_type = btn
                            self.build_size = Pair(bt.grid_w, bt.grid_h)
                            
                        #if a == 0 and b == 0: # 100 000 000
                        #    self.mode = 'build'
                        #    self.build_type = 'solar'
                        #    self.build_size = Pair(2, 1)
                        #elif a == 1 and b == 0: # 010 000 000
                        #    self.mode = 'build'
                        #    self.build_type = 'mine'
                        #    self.build_size = Pair(2, 2)
                        #elif a == 2 and b == 0: # 001 000 000
                        #    self.mode = 'build'
                        #    self.build_type = 'radar'
                        #    self.build_size = Pair(1, 1)
                        #elif a == 0 and b == 1: # 000 100 000
                        #    self.mode = 'build'
                        #    self.build_type = 'barracks'
                        #    self.build_size = Pair(2, 3)
                        #elif a == 1 and b == 1: # 000 010 000
                        #    self.mode = 'build'
                        #    self.build_type = 'factory'
                        #    self.build_size = Pair(2, 3)
                        #elif a == 2 and b == 1: # 000 001 000
                        #    self.mode = 'build'
                        #    self.build_type = 'laboratory'
                        #    self.build_size = Pair(2, 2)
                        #elif self.mode == 'build':
                        #    pass
                    elif self.mode == 'normal':
                        deb_x = min(self.SELECT_X, mx - self.x)
                        fin_x = max(self.SELECT_X, mx - self.x)
                        deb_y = min(self.SELECT_Y, my - self.y)
                        fin_y = max(self.SELECT_Y, my - self.y)
                        ul = self.select_zone(deb_x, deb_y, fin_x, fin_y)
                        if not self.add_mod:
                            self.selected = []
                        if len(ul) > 1:
                            for u in ul:
                                if u.player == self.player:
                                    if u not in self.selected:
                                        self.selected.append(u)
                        elif len(ul) == 1:
                            if ul[0].player == self.player:
                                self.selected.append(ul[0])
                            else:
                                if not self.add_mod:
                                    self.selected = ul # on peut selectionner une et une seule unite ennemie
                    elif self.mode == 'build':
                        # repeated code in render
                        xx = (mx - self.x) // 32
                        yy = (my - self.y) // 32
                        # center the thing
                        cw = self.build_size.x // 2
                        ch = self.build_size.y // 2
                        # test if ok
                        v = self.player.world.is_empty_zone(xx-cw, yy-ch, self.build_size.x, self.build_size.y)
                        if v:
                            # Final Building Here
                            bt = self.player.game.all_building_types[self.build_type]
                            if self.player.min >= bt.cost[0] and self.player.sol >= bt.cost[1]:
                                self.player.min -= bt.cost[0]
                                self.player.sol -= bt.cost[1]
                                self.player.game.create_building(self.player.name, xx-cw, yy-ch, self.build_type)
                            else:
                                self.not_enough_ress = 10
                        if not self.add_mod: # multiple construction orders
                            self.mode = 'normal'
                elif event.button == 3:  # Right Button
                    if self.mode == 'build':
                        self.mode = 'normal'
                    elif len(self.selected) == 1 and self.selected[0].player != self.player:
                        pass
                    else:
                        print('button right')
                        s = self.player.world.unit_map[int((my - self.y)/32)][int((mx - self.x)/32)]
                        if s == 0:  # nothing at the square clicked
                            # faut-il faire un for u in self.selected?
                            self.game.order_move(self.selected, (mx - self.x) // 32, (my - self.y) // 32, self.add_mod)
                            #for u in self.selected:
                            #    print(u, u.__class__)
                            #    if not self.add_mod:
                            #        #print('set order!')
                            #        u.order(Order('go', (mx - self.x) // 32, (my - self.y) // 32))
                            #        #print('go at ', (mx - self.x) // 32, (my - self.y) // 32)
                            #    else:
                            #        #print('add order!')
                            #        #print(len(u.orders))
                            #        u.add_order(Order('go', (mx - self.x) // 32, (my - self.y) // 32))
                            #        #print(len(u.orders))
                        elif s[1].player != self.player:
                            for u in self.selected:
                                if not self.add_mod:
                                    u.order(Order('attack', target=s[1]))
                                else:
                                    u.add_order(Order('attack', target=s[1]))
                elif event.button == 2:  # Middle Button
                    print('button 3')

        # Scroll on border with the mouse
        if self.left or mx < self.auto_scroll_zone:
            self.x += self.scroll
        if self.right or mx > self.width - self.auto_scroll_zone:
            self.x -= self.scroll
        if self.down or my > self.height - self.auto_scroll_zone:
            self.y -= self.scroll
        if self.up or my < self.auto_scroll_zone:
            self.y += self.scroll

        self.player.world.particles.update()
        return True

    def render(self):
        mx, my = pygame.mouse.get_pos()  # repeat from main_loop
        self.screen.fill(BLACK)

        # Sol
        for yy in range(0, self.player.world.size32.y):
            for xx in range(0, self.player.world.size32.x):
                t = self.player.world.world_map[yy][xx]
                d = self.player.world.passable_map[yy][xx]
                self.screen.blit(TEXTURES[t].img, (xx * 32 + self.x, yy * 32 + self.y, xx * 32 + self.x + 32, yy * 32 + self.y))
                if d != 0 and d != 99:
                    self.screen.blit(TEXTURES[d].img, (xx * 32 + self.x, yy * 32 + self.y, xx * 32 + self.x + 32, yy * 32 + self.y))
                
                u = self.player.world.unit_map[yy][xx]
                if u == 0:
                    pass # Empty
                elif u[0] == -1: # en mouvement, carreau reserve
                    pygame.draw.rect(self.screen, HALF_RED, (xx * 32 + self.x +1, yy * 32 + self.y +1, 32-1, 32-1), 0)
                elif u[1] == 1: # en position
                    pygame.draw.rect(self.screen, HALF_BLUE, (xx * 32 + self.x +1, yy * 32 + self.y +1, 32-1, 32-1), 0)
                elif u[1] == 2:
                    pass # Building
        
                # DEBUG
                label = self.font.render("%(v)04d" % {"v" : self.player.world.debug_map[yy][xx]}, 1, (255, 0, 0))
                self.screen.blit(label, (xx * 32 + self.x, yy * 32 + self.y))
                
        # Cursor
        if self.mode == 'normal':
            if self.SELECT_R:
                r = xrect(self.SELECT_X + self.x, self.SELECT_Y + self.y, mx, my)
                pygame.draw.rect(self.screen, WHITE, r, 1)
        elif self.mode == 'build':
            xx = (mx - self.x) // 32
            yy = (my - self.y) // 32
            # center the thing
            cw = self.build_size.x // 2
            ch = self.build_size.y // 2
            # test if ok
            v = self.player.world.is_empty_zone(xx-cw, yy-ch, self.build_size.x, self.build_size.y)
            if v:
                c = GREEN
            else:
                c = RED
            pygame.draw.rect(self.screen, c, ((xx-cw)*32+self.x, (yy-ch)*32+self.y, self.build_size.x*32,
                                              self.build_size.y*32), 0)

        # Unit
        for u in self.player.world.units:
            if type(u).__name__ == 'Building':
                for ix in range(u.grid_x, u.grid_x+u.type.grid_w):
                    for iy in range(u.grid_y, u.grid_y+u.type.grid_h):
                        #print(ix, iy, ix * 32 + self.x, iy * 32 + self.y)
                        pygame.draw.rect(self.screen, u.player.color, (ix * 32 + self.x, iy * 32 + self.y, 32, 32), 0)
                        if u in self.selected: # and u.grid_x == ix and u.grid_y == iy:
                            pygame.draw.rect(self.screen, GREEN, (u.grid_x * 32 + self.x, u.grid_y * 32 + self.y, u.type.grid_w * 32, u.type.grid_h * 32), 2)
            else:
                if u in self.selected:
                    if len(u.orders) > 0:
                        lx = u.real_x + self.x
                        ly = u.real_y + self.y
                        for o in u.orders:
                            if o.kind == 'go': # x2r => return x * 32 + self.x + 16
                                pygame.draw.circle(self.screen, GREEN, (self.x2r(o.x), self.y2r(o.y)), 5, 0)
                                pygame.draw.line(self.screen, GREEN, (lx, ly), (self.x2r(o.x), self.y2r(o.y)), 1)
                                lx = self.x2r(o.x)
                                ly = self.y2r(o.y)
                            elif o.kind == 'attack':
                                #pygame.draw.circle(self.screen, RED, (o.target.x*32+16 + self.x, o.target.y*32+16 + self.y), 5, 0)
                                pygame.draw.line(self.screen, RED, (lx, ly), (self.x2r(o.target.x), self.y2r(o.target.y)), 1)
                                lx = self.x2r(o.target.x)
                                ly = self.y2r(o.target.y)
                    pygame.draw.circle(self.screen, u.player.color, (u.real_x + self.x, u.real_y + self.y), u.size, 0)
                    if u.player == self.player:
                        pygame.draw.circle(self.screen, GREEN, (u.real_x + self.x, u.real_y + self.y), u.size+3, 2)
                    else:
                        pygame.draw.circle(self.screen, RED, (u.real_x + self.x, u.real_y + self.y), u.size+3, 2)
                else:
                    pygame.draw.circle(self.screen, u.player.color, (u.real_x + self.x, u.real_y + self.y), u.size, 0)
        
        for p in self.player.world.particles.core:
            pygame.draw.circle(self.screen, RED, (p.x + self.x, p.y + self.y), 3, 0)

        # Interface
        pygame.draw.rect(self.screen, GREY, (0, self.INTERFACE_Y, 799, 200), 0) # fond
        pygame.draw.line(self.screen, BLUE, (0, self.INTERFACE_Y), (799, self.INTERFACE_Y), 1)
        for xx in range(0, 3):
            for yy in range(0, 3):
                pygame.draw.rect(self.screen, BLUE, (xx * 32, yy * 32 + self.INTERFACE_Y, 32, 32), 1)
        pygame.draw.line(self.screen, BLUE, (703, self.INTERFACE_Y), (703, self.INTERFACE_Y + 96), 1)
        pygame.draw.line(self.screen, BLUE, (703, self.INTERFACE_Y + 96), (799, self.INTERFACE_Y + 96), 1)

        # Build menu
        
        xs = 8
        ys = self.INTERFACE_Y + 8
        for btn in self.player.game.all_building_types_ordered:
            bt = self.player.game.all_building_types[btn]
            label = self.font.render(bt.name[0:3], 1, (255, 255, 0))
            self.screen.blit(label, (xs, ys))
            xs += 32
            if xs > 72:
                xs = 8
                ys += 32
            
        #label = self.font.render('Min', 1, (0, 0, 0))
        #self.screen.blit(label, (8, self.INTERFACE_Y+8))
        #label = self.font.render('Sol', 1, (0, 0, 0))
        #self.screen.blit(label, (40, self.INTERFACE_Y+8))
        #label = self.font.render('Rad', 1, (0, 0, 0))
        #self.screen.blit(label, (72, self.INTERFACE_Y+8))
        
        #label = self.font.render('Cas', 1, (0, 0, 0))
        #self.screen.blit(label, (8, self.INTERFACE_Y+40))
        #label = self.font.render('Fac', 1, (0, 0, 0))
        #self.screen.blit(label, (40, self.INTERFACE_Y+40))
        #label = self.font.render('Lab', 1, (0, 0, 0))
        #self.screen.blit(label, (72, self.INTERFACE_Y+40))
        
        # Metal (min) & Energie (sol)
        min = int(self.player.min)
        sol = int(self.player.sol)
        if self.not_enough_ress > 0:
            label = self.font.render("M : %(min)04d E : %(sol)04d NOT ENOUGH RESSOURCES!" % {"min" : min, "sol" : sol}, 1, (255, 0, 0))
            self.not_enough_ress -= 1
        else:
            label = self.font.render("M : %(min)04d E : %(sol)04d" % {"min" : min, "sol" : sol}, 1, (255, 255, 0))
        self.screen.blit(label, (5, self.INTERFACE_Y+104))
        
        # Minimap
        for yy in range(0, self.player.world.size32.y):
            for xx in range(0, self.player.world.size32.x):
                t = self.player.world.world_map[yy][xx]
                d = self.player.world.passable_map[yy][xx]
                if d != 0 and d != 99:
                    pygame.draw.rect(self.screen, TEXTURES[d].mini, (xx * 3 + 22 * 32, yy * 3 + self.INTERFACE_Y +1, 3, 3), 0)
                else:
                    pygame.draw.rect(self.screen, TEXTURES[t].mini, (xx * 3 + 22 * 32, yy * 3 + self.INTERFACE_Y +1, 3, 3), 0)
                u = self.player.world.unit_map[yy][xx]
                if u != 0:
                    if u[0] == 1 or u[0] == 2:
                        pygame.draw.rect(self.screen, u[1].player.color, (xx * 3 + 22 * 32, yy * 3 + self.INTERFACE_Y +1, 3, 3), 0)
        # fin Interface

        pygame.display.flip()


class Particles:
    def __init__(self):
        self.core = []

    def add(self, p):
        self.core.append(p)

    def update(self):
        i = 0
        while i < len(self.core):
            ttl = self.core[i].update()
            if ttl <= 0:
                del self.core[i]
                print(ttl, len(self.core))
            else:
                i += 1
                print(ttl, len(self.core))


class Particle:
    def __init__(self, pos, p_dir, target, ttl, guided=False):
        self.x = pos[0]
        self.y = pos[1]
        self.ax = p_dir[0]
        self.ay = p_dir[1]
        self.vel = p_dir[2]
        self.tx = target[0]
        self.ty = target[1]
        self.ttl = ttl
        self.guided = guided

    def update(self):
        if self.ttl == 0:
            return 0
        if not self.guided:
            self.x += self.vel * self.ax
            self.y += self.vel * self.ay
        else:
            pass
        # print self.x > self.tx and self.y > self.ty
        if self.x > self.tx and self.y > self.ty:
            self.ttl = 0
        else:
            self.ttl -= 1
        return self.ttl


# unit_map can be : 0 : void, (1, u) : unit u is here, (-1, u) : unit u is moving here
class World:
    def __init__(self, world_map):
        self.particles = Particles()
        if len(world_map) == 0:
            raise Exception("Empty map detected")
        self.size32 = Pair(len(world_map[0]), len(world_map))
        self.unit_map = World.create_map(self.size32.x, self.size32.y, 0)
        self.world_map = World.create_map(self.size32.x, self.size32.y, 0)
        self.passable_map = World.create_map(self.size32.x, self.size32.y, 0)
        self.debug_map = World.create_map(self.size32.x, self.size32.y, 0)
        # separate [128] => 100 (in world map) + 28 (in passable_map or 99 if texture not passable by default (and no doodad can be put on it))
        for yy in range(0, self.size32.y):
            for xx in range(0, self.size32.x):
                r = world_map[yy][xx]
                self.world_map[yy][xx] = (r // 100) * 100
        
        for yy in range(0, self.size32.y):
            for xx in range(0, self.size32.x):
                r = world_map[yy][xx] # 101, 228, 312
                self.passable_map[yy][xx] = r % 100
                r = self.world_map[yy][xx] # 100, 200, 300
                if not TEXTURES[r].passable:
                    self.passable_map[yy][xx] = 99
        
        # Computation of passage from tex to tex
        world_map2 = World.create_map(self.size32.x, self.size32.y, 0)
        for yy in range(0, self.size32.y):
            for xx in range(0, self.size32.x):
                r = self.world_map[yy][xx]
                
                # On travaille ne base 3
                b1 = 1
                b2 = 3
                b3 = 9
                b4 = 27
                b5 = 81
                b6 = 243
                b7 = 729
                b8 = 2187
                sum = 0
                
                # On commence en haut à gauche, puis on tourne dans le sens horaire
                # 1 = différent 0 = égal 2 = bord
                # ligne du haut
                if yy > 1 and xx > 1:
                    if self.world_map[yy-1][xx-1] != r:
                        sum += 1 * b1 # sinon 0*b1 donc rien
                else:
                    sum += 2 * b1
                if xx > 1:
                    if self.world_map[yy][xx-1] != r:
                        sum += 1 * b2
                else:
                    sum += 2 * b2
                if yy < self.size32.y - 1 and xx > 1:
                    if self.world_map[yy+1][xx-1] != r:
                        sum += 1 * b3
                else:
                    sum += 2 * b3
                # ligne du milieu, gauche
                if yy < self.size32.y - 1:
                    if self.world_map[yy+1][xx] != r:
                        sum += 1 * b4
                else:
                    sum += 2 * b4
                # ligne du bas, en partant de la gauche
                if yy < self.size32.y - 1 and xx < self.size32.x - 1:
                    if self.world_map[yy+1][xx+1] != r:
                        sum += 1 * b5
                else:
                    sum += 2 * b5
                if xx < self.size32.x - 1:
                    if self.world_map[yy][xx+1] != r:
                        sum += 1 * b6
                else:
                    sum += 2 * b6
                if yy > 1 and xx < self.size32.x - 1:
                    if self.world_map[yy-1][xx+1] != r:
                        sum += 1 * b7
                else:
                    sum += 2 * b7
                # ligne du milieu, droit
                if yy > 1:
                    if self.world_map[yy-1][xx] != r:
                        sum += 1 * b8
                else:
                    sum += 2 * b8
                
                self.debug_map[yy][xx] = sum
                
                world_map2[yy][xx] = self.world_map[yy][xx]
                if r == 300:
                    # coin
                    if sum == 2929 or sum == 2200 or sum == 2191: # coin haut gauche
                        world_map2[yy][xx] = 1100
                    elif sum == 3241: # coin haut droit
                        world_map2[yy][xx] = 1300
                    elif sum == 1089 or sum == 1080 or sum == 351: # coin bas droit
                        world_map2[yy][xx] = 1500
                    elif sum == 121: # coin bas gauche
                        world_map2[yy][xx] = 1700
                    # milieu
                    elif sum == 2917: #2920: # milieu haut
                        world_map2[yy][xx] = 1200
                    elif sum == 1053 or sum == 324: #3240: # milieu droit
                        world_map2[yy][xx] = 1400
                        #print('modified! at', yy, xx, 'to', world_map2[yy][xx])
                    elif sum == 117: #120: # milieu bas
                        world_map2[yy][xx] = 1600
                    elif sum == 13 or sum == 4: #2200: # milieu gauche
                        world_map2[yy][xx] = 1800
                    # les coins bizarres, entre deux diag /
                    elif sum == 1:
                        world_map2[yy][xx] = 2200
                    elif sum == 81:
                        world_map2[yy][xx] = 2400
                    elif sum == 82:
                        world_map2[yy][xx] = 2300
                    else:
                        print(sum)
                
                # if xx < self.size32.x - 1:
                    # r_middle_right = world_map[xx+1][yy]
                    # if r_middle_right != r:
                        # if r_middle_right == 300:
                            ## self.world_map[xx][yy] = 1300
                            # self.passable_map[xx][yy] = 98
                # if xx > 1:
                    # r_middle_left = world_map[xx-1][yy]
                    # if r_middle_left != r:
                        # if r_middle_left == 300:
                            # self.passable_map[xx][yy] = 94
                # if yy > 1:
                    # r_top_center = world_map[xx][yy-1]
                    # if r_top_center != r:
                        # if r_top_center == 300:
                            # self.passable_map[xx][yy] = 96 # why?
                # if yy < self.size32.y - 1:
                    # r_bottom_center = world_map[xx][yy+1]
                    # if r_bottom_center != r:
                        # if r_bottom_center == 300:
                            # self.passable_map[xx][yy] = 92 #why?
        
        self.world_map = world_map2
        self.units = []
    
    def is_valid(self, x, y):
        return 0 <= x < self.size32.x and 0 <= y < self.size32.y

    def is_valid_zone(self, x, y, w, h):
        if 0 <= x < self.size32.x and 0 <= y < self.size32.y:
            if x + w < self.size32.x and y + h <= self.size32.y:
                return True
        return False
    
    def is_empty_zone(self, x, y, w, h):
        if not self.is_valid_zone(x, y, w, h):
            return False
        else:
            for i in range(x, x+w):
                for j in range(y, y+h):
                    if self.passable_map[j][i] != 0 and self.unit_map[j][i] != 0:
                        return False
            return True
    
    def is_empty(self, x, y):  # no unit, no blocking terrain
        return self.passable_map[y][x] == 0 and self.unit_map[y][x] == 0
    
    def is_unit(self, x, y):
        return self.unit_map[y][x] != 0

    @staticmethod
    def create_map(lines, columns, value):
        content = []
        for i in range(0, lines):
            line = []
            for j in range(0, columns):
                line.append(value)
            content.append(line)
        return content


class Game:
    def __init__(self, name, world):
        self.name = name
        self.world = world
        self.players = {}
        self.unit_type = {"soldier": UnitType("Soldier", size=10, range=100, life=100, dom=5, speed=8, reload=50),
                          "elite": UnitType("Elite", size=10, range=150, life=100, dom=10, speed=8, reload=50),
                          "big": UnitType("Big", size=20, range=30, life=300, dom=20, speed=8, reload=50)}
        # self.building_type = {"mine": BuildingType(size=(2,2), range=20, life=300, dom=0, speed=0, reload=0, type=1)}
        self.all_building_types = {"mine" : BuildingType("Mine", 2, 2, 100, (0,50)),
                                   "solar" : BuildingType("Solar", 1, 2, 80, (0, 50)),
                                   "radar" : BuildingType("Radar", 1, 1, 80, (50, 200)),
                                   "barracks" : BuildingType("Barracks", 3, 2, 300, (50, 100)),
                                   "factory" : BuildingType("Factory", 3, 2, 500, (200, 200)),
                                   "laboratory" : BuildingType("Laboratory", 2, 2, 250, (100, 400)),
                                  }
        self.all_building_types_ordered = ["solar", "mine", "radar", "barracks", "factory", "laboratory"]
        
    def create_player(self, name, player_color, *ress):
        print("creating player")
        if name in self.players:
            raise Exception("Already a player with this name")
        self.players[name] = Player(self, name, player_color, ress)

    def create_unit(self, player_name, x, y, unit_type_name):
        sys.stdout.write("creating unit")
        p = self.get_player_by_name(player_name)
        ut = self.get_unit_type_by_name(unit_type_name)
        if not self.world.is_valid(x, y) or not self.world.is_empty(x,y):
            raise Exception("False or not empty coordinates : " + str(x) + ", " + str(y) + " p = " + str(self.world.passable_map[y][x]))
        u = Unit(ut, p, x, y)
        self.world.units.append(u)
        p.units.append(u)
        sys.stdout.write(' :: unit #' + str(u.id) + ' created\n')
        return u.id
        
    def create_building(self, player_name, x, y, building_type_name):
        sys.stdout.write("creating building")
        p = self.get_player_by_name(player_name)
        bt = self.get_building_type_by_name(building_type_name)
        if not self.world.is_valid_zone(x, y, bt.grid_w, bt.grid_h) or not self.world.is_empty_zone(x, y, bt.grid_w, bt.grid_h):
            raise Exception("False or not empty coordinates : " + str(x) + ", " + str(y))
        b = Building(p, bt, x, y)
        self.world.units.append(b) 
        p.buildings.append(b)
        sys.stdout.write(' :: building #' + str(b.id) + ' created\n')
        return b.id
        
    def order_move(self, units, x : int, y : int, add : bool):
        sys.stdout.write('Move ')
        for u in units:
            sys.stdout.write(str(u) + ' ')
            if add:
                sys.stdout.write('(delayed) ')
                u.add_order(Order('go', x, y))
            else:
                u.order(Order('go', x, y))
        sys.stdout.write('to ' + str(x) + ', ' + str(y) + '\n')
    
    def get_player_by_name(self, player_name):
        if player_name not in self.players:
            raise Exception("Unknown player : " + player_name)
        return self.players[player_name]

    def get_unit_type_by_name(self, unit_type_name):
        if unit_type_name not in self.unit_type:
            raise Exception("Unknown unit type : " + unit_type_name)
        return self.unit_type[unit_type_name]
        
    def get_building_type_by_name(self, building_type_name):
        if building_type_name not in self.all_building_types:
            raise Exception("Unknown building type : " + building_type_name)
        return self.all_building_types[building_type_name]

    #def get_units_by_id(self, ids):
    #    units = []
    #    cpt = 0
    #    for u in self.world.units:
    #        if u.uid in ids:
    #            units.append(u)
    #            cpt += 1
    #    if cpt != len(ids):
    #        raise Exception("ID of unit unknown detected !!!")
    #    return units
    
    def update(self):
        for key, value in self.players.items():
            value.update()


class Player:
    def __init__(self, game, name, player_color, ress):
        self.game = game
        self.name = name
        self.world = game.world
        self.color = player_color
        self.units = []
        self.buildings = []
        self.min = ress[0]
        self.sol = ress[1]
    
    def update(self):
            # Update for all units?
        for u in self.units:
            if not u.update():
                self.player.world.units.remove(u)
                print("deleting unit")
                del u
        for b in self.buildings:
            b.update()


class Order:
    def __init__(self, kind=None, x=0, y=0, target=None):
        self.x = x
        self.y = y
        self.target = target
        self.kind = kind


class Pair:
    def __init__(self, x, y, rep=1):
        if rep != 1 and rep != 32:
            raise Exception("rep must be 32 or 1")
        self.x = x
        self.y = y
        self.rep = rep

    def set(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if other is None:
            return False
        if self.rep != other.rep:
            x = other.x * 32
            y = other.y * 32
        else:
            x = other.x
            y = other.y
        return isinstance(other, self.__class__) and self.x == x and self.y == y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "[" + str(self.x) + ", " + str(self.y) + "]"


class BuildLoad:

    def __init__(self):
        pass


class WeaponType:

    def __init__(self, name : str, range : int, reload : int):
        self.name = name
        self.range = range
        self.reload = reload


class BuildingType:

    def __init__(self, name : str, grid_h : int, grid_w : int, life : int, cost : int, build_load : BuildLoad = None, weapon_type : WeaponType = None):
        self.name = name
        self.grid_h = grid_h
        self.grid_w = grid_w
        self.life = life
        self.cost = cost
        self.build_load = build_load
        self.weapon_type = weapon_type


class GameObject:
 
    seed = 0
    
    def __init__(self):
        self.id = GameObject.seed + 1
        GameObject.seed = self.id


class Building(GameObject):

    def __init__(self, player : Player, type : BuildingType, grid_x : int, grid_y : int):
        GameObject.__init__(self)
        self.player = player
        self.type = type
        self.grid_x = grid_x
        self.grid_y = grid_y
        
        self.orders = []
        for i in range(grid_x, grid_x + type.grid_w):
            for j in range(grid_y, grid_y + type.grid_h):
                self.player.world.unit_map[j][i] = (2, self) # STILL, BUILDING
    
    def __str__(self):
        return str(id(self)) + ' (' + self.type.name + ')'
    
    def update(self):
        if self.type.name == "Mine":
            self.player.min += 0.2
            if self.player.min > 9999:
                self.player.min = 9999
        elif self.type.name == "Solar":
            self.player.sol += 0.2
            if self.player.sol > 9999:
                self.player.sol = 9999
        return True # Very Important
    
    def order(self, o):
        self.orders = [o]

    def add_order(self, o):
        self.orders.append(o)


class UnitType:

    def __init__(self, name, size, range, life, dom, speed, reload):
        self.name = name
        self.size = size
        self.range = range
        self.life = life
        self.dom = dom
        self.speed = speed
        self.reload = reload


class Unit(GameObject):
    
    def __init__(self, type, player, x, y):
        GameObject.__init__(self)
        self.type = type
        self.player = player
        self.real_x = x * 32 + 16
        self.real_y = y * 32 + 16
        self.x = x
        self.y = y
        self.size = type.size
        self.range = type.range
        self.life = type.life
        self.dom = type.dom
        self.reload = type.reload
        
        self.orders = []
        self.cpt = 0
        self.cpt_move = 0
        self.speed_move = 1
        self.speed_step = type.speed  # must be 1 or a multiple of 2 - 2 before
        self.old_x = x
        self.old_y = y

        # Transitional movement system (TMS)
        self.transition = None
        self.destination = None
        self.previous32 = None

    def __str__(self):
        return 'Unit #' + str(self.id) + ' (' + self.type.name + ')'
        #return str(id(self)) + ' (' + self.uname + ')'

    def update(self):
        self.player.world.unit_map[self.y][self.x] = 0
        # print 'update ', len(self.orders)
        if self.life <= 0:
            return False

        if len(self.orders) > 0:
            o = self.orders[0]
            if o.kind == 'go':
                r = self.go(o.x, o.y)
                if r:
                    del self.orders[0]
            elif o.kind == 'attack':
                # print o.kind, o.target, o.target.x, o.target.y
                if math.sqrt((self.x - o.target.x) ** 2 + (self.y - o.target.y) ** 2) > self.range or (
                        self.x - 16) % 32 != 0 or (self.y - 16) % 32 != 0:
                    self.go(o.target.x, o.target.y)
                elif self.cpt <= 0:
                    self.player.world.particles.add(
                        Particle([self.x, self.y], [1, 1, 4], [o.target.x, o.target.y], self.range + 10, False))
                    o.target.life -= self.dom
                    self.cpt = self.reload
                    if o.target.life <= 0:
                        del self.orders[0]
                else:
                    self.cpt -= 1
        self.player.world.unit_map[self.y][self.x] = (1, self) # CODE: STILL, UNIT
        return True

    def order(self, o : Order):
        self.orders = [o]

    def add_order(self, o):
        self.orders.append(o)

    def go(self, x : int, y : int):

        if self.cpt_move > 0:
            self.cpt_move -= 1
            return False
        else:
            self.cpt_move = self.speed_move

        if self.destination is None:
            # 32 en 32
            from_x = self.x
            from_y = self.y
            to_x = x
            to_y = y

            # print 'destination x,y = ', x,y
            # print 'destination/32 x,y = ', to_x32, to_y32

            n_x = -1
            n_y = -1
            going_x = 0
            going_y = 0
            if to_x > from_x:
                n_x = from_x + 1
                going_x = 1
            elif to_x < from_x:
                n_x = from_x - 1
                going_x = -1
            elif to_x == from_x:
                n_x = from_x
            if to_y > from_y:
                n_y = from_y + 1
                going_y = 1
            elif to_y < from_y:
                n_y = from_y - 1
                going_y = -1
            elif to_y == from_y:
                n_y = from_y

            if not self.player.world.is_empty(n_x, n_y):
                print("blocked!")
                if going_x == 1 and going_y == 1:
                    test = (from_x, n_y, n_x, from_y)
                elif going_x == 1 and going_y == 0:
                    test = (n_x, n_y + 1, n_x, n_y - 1)
                elif going_x == 1 and going_y == -1:
                    test = (from_x, n_y, n_x, from_y)
                elif going_x == 0 and going_y == 1:
                    test = (from_x - 1, n_y, from_x + 1, n_y)
                elif going_x == 0 and going_y == 0:
                    pass  # not a move
                elif going_x == 0 and going_y == -1:
                    test = (from_x - 1, n_y, from_x + 1, n_y)
                elif going_x == -1 and going_y == 1:
                    test = (from_x, n_y, n_x, from_y)
                elif going_x == -1 and going_y == 0:
                    test = (n_x, n_y + 1, n_x, n_y - 1)
                elif going_x == -1 and going_y == -1:
                    test = (from_x, n_y, n_x, from_y)

                if self.player.world.is_empty(test[0], test[1]):
                    print("trying : " + str(test[0]) + ", " + str(test[1]))
                    n_x = test[0]
                    n_y = test[1]
                elif self.player.world.is_empty(test[2], test[3]):
                    print("trying : " + str(test[2]) + ", " + str(test[3]))
                    n_x = test[2]
                    n_y = test[3]
                if n_x == self.old_x and n_y == self.old_y:
                    return True  # no loop !

            if self.player.world.is_empty(n_x, n_y):
                self.destination = Pair(n_x * 32 + 16, n_y * 32 + 16)
                self.player.world.unit_map[n_y][n_x] = (-1, self) # CODE: IN MOVEMENT

        if self.destination is not None and self.transition is None:
            self.transition = Pair(self.x * 32 + 16, self.y * 32 + 16)

        if self.transition != self.destination:
            if self.transition.x < self.destination.x:
                self.transition.x += self.speed_step
            elif self.transition.x > self.destination.x:
                self.transition.x -= self.speed_step
            if self.transition.y < self.destination.y:
                self.transition.y += self.speed_step
            elif self.transition.y > self.destination.y:
                self.transition.y -= self.speed_step

        if self.transition is not None:
            self.real_x = self.transition.x
            self.real_y = self.transition.y
        else:
            self.real_x = self.x * 32 + 16
            self.real_y = self.y * 32 + 16

        if self.destination == self.transition and self.destination is not None:
            self.old_x = self.x
            self.old_y = self.y
            self.x = int((self.destination.x - 16) / 32)
            self.y = int((self.destination.y - 16) / 32)
            self.destination = None
            self.transition = None

        print(self.x, self.y, "tr= ", self.transition, "dst= ", self.destination) # Add details on pathfinding (verbose)
        return self.x == x and self.y == y


# -----------------------------------------------------------------------------
# Tools


def xrect(x1, y1, x2, y2):
    tx = abs(x1 - x2)
    ty = abs(y1 - y2)
    if x1 > x2:
        rx = x2
    else:
        rx = x1
    if y1 > y2:
        ry = y2
    else:
        ry = y1
    return Rect(rx, ry, tx, ty)


def main_loop(camera):
    while 1:

        r = camera.update()
        camera.render()
        if not r:
            break

        pygame.time.Clock().tick(30)
    print("Metal = " + str(camera.player.min))
    print("Energy = " + str(camera.player.sol))

def configure():
    # 1 rock 0 ground 2 grass 3 water 
    my_map = [
        [101, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 101, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 200, 200, 200, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 300, 300, 300, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 300, 300, 300, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 300, 300, 300, 100, 100, 100, 100, 100],
        [100, 100, 100, 200, 200, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 200, 200, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 101, 101, 101, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 100, 100, 100, 100, 300, 300, 300, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 300, 300, 300, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 300, 300, 300, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 101, 100, 100, 100, 100, 100, 100, 100, 100, 100, 300, 300, 300, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 300, 300, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 300, 300, 300, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 300, 300, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 300, 300, 300, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 101, 101, 101, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 101, 100, 101, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 101, 101, 101, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 300, 300, 100, 100, 100, 300, 300, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 100, 100, 100, 100, 300, 300, 100, 100, 100, 100, 100, 300, 300, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
    ]
    # print('map x :', len(my_map[0]))
    # print('map y :', len(my_map))

    g = Game('Test 1', World(my_map))
    g.create_player("Bob", YELLOW, 100, 100)
    g.create_player("Henry", SKY_BLUE, 0, 0)
    g.create_unit("Bob", 1, 1, "soldier")
    g.create_unit("Bob", 3, 3, "elite")
    
    g.create_unit("Henry", 12, 12, "big")
    g.create_unit("Henry", 18, 14, "soldier")
    
    g.create_building("Bob", 5, 5, "mine")
    
    return Camera(800, 600, 5, g.get_player_by_name("Bob"))  # x, y, scroll, player


def start():
    c = configure()
    main_loop(c)

if __name__ == '__main__': 
    import sys
    _maj, _min = sys.version_info[:2]
    print('Starting on Python ' + str(_maj) + "." + str(_min) + " with pygame " + pygame.version.ver)
    start()
    exit()
