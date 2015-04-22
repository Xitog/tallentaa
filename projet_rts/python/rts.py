#! /usr/bin/env python

__version__ = "$Revision: 1 $"

# http://ezide.com/games/code_examples/example.py
# http://pygame.org/docs/ref/draw.html#pygame.draw.rect

# div X and Y by 32 + math.trunc -> give the square where we are
# multiply by 32 -> give where we start to display

import pygame, sys, math
from pygame.locals import *


class Camera:
    def __init__(self, width, height, scroll, player):
        self.width = width
        self.height = height
        self.size = width, height
        self.scroll = scroll
        self.player = player
        self.x = 0
        self.y = 0
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)  # , pygame.FULLSCREEN | pygame.HWSURFACE)
        self.font = pygame.font.SysFont("monospace", 10)

    def render(self):
        mx, my = pygame.mouse.get_pos()  # repeat from main_loop
        self.screen.fill(Color(0, 0, 0, 255))

        for yy in range(0, w1.size32.y):
            for xx in range(0, w1.size32.x):
                r = my_map[xx][yy]
                if r == 1:
                    pygame.draw.rect(self.screen, Color(255, 0, 0, 128), (xx * 32 + self.x, yy * 32 + self.y, 32, 32), 1)
                else:
                    pygame.draw.rect(self.screen, Color(0, 255, 0, 128), (xx * 32 + self.x, yy * 32 + self.y, 32, 32), 1)
                u = w1.unit_map[xx][yy]
                if u == 0:
                    pass
                elif u[0] == -1:
                    pygame.draw.rect(self.screen, Color(128, 0, 0, 8), (xx * 32 + self.x, yy * 32 + self.y, 32, 32), 0)
                else:
                    pygame.draw.rect(self.screen, Color(0, 0, 128, 8), (xx * 32 + self.x, yy * 32 + self.y, 32, 32), 0)
                label = self.font.render(str(xx) + ", " + str(yy), 1, (255,255,0))
                self.screen.blit(label, (int(xx * 32 + self.x), int(yy * 32 + self.y)))

        if SELECT_R:
            r = xrect(SELECT_X + self.x, SELECT_Y + self.y, mx, my)
            pygame.draw.rect(self.screen, Color(255, 255, 255, 255), r, 1)

        for u in units:
            if u in selected:
                c = Color(0, 0, 255, 255)
                if len(u.orders) > 0:
                    lx = u.real_x
                    ly = u.real_y
                    for o in u.orders:
                        if o.kind == 'go':
                            pygame.draw.circle(self.screen, c, (x2r(o.x, self.x), y2r(o.y, self.y)), 5, 0)
                            pygame.draw.line(self.screen, c, (lx + self.x, ly + self.y), (x2r(o.x, self.x), y2r(o.y, self.y)), 1)
                            lx = o.x
                            ly = o.y
                        elif o.kind == 'attack':
                            pygame.draw.circle(self.screen, Color(255, 0, 0), (o.target.x*32+16 + self.x, o.target.y*32+16 + self.y), 5, 0)
                            pygame.draw.line(self.screen, Color(255, 0, 0), (lx + self.x, ly + self.y),
                                             (o.target.x*32+16 + self.x, o.target.y*32+16 + self.y), 1)
                            lx = o.target.x
                            ly = o.target.y
            else:
                c = u.player.color
            pygame.draw.circle(self.screen, c, (u.real_x + self.x, u.real_y + self.y), u.size, 0)

        for p in w1.particles.core:
            pygame.draw.circle(self.screen, Color(255, 0, 0), (p.x + self.x, p.y + self.y), 3, 0)

        # Interface
        pygame.draw.rect(self.screen, Color(200, 200, 200), (0, INTERFACE_Y, 799, 200), 0)
        pygame.draw.line(self.screen, Color(0, 0, 255), (0, INTERFACE_Y), (799, INTERFACE_Y), 1)
        for xx in range(0, 3):
            for yy in range(0, 3):
                pygame.draw.rect(self.screen, Color(0, 0, 255), (xx * 32, yy * 32 + INTERFACE_Y, 32, 32), 1)
        pygame.draw.line(self.screen, Color(0, 0, 255), (703, INTERFACE_Y), (703, INTERFACE_Y + 96), 1)
        pygame.draw.line(self.screen, Color(0, 0, 255), (703, INTERFACE_Y + 96), (799, INTERFACE_Y + 96), 1)

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
    def __init__(self, pos, dir, target, ttl, guided=False):
        self.x = pos[0]
        self.y = pos[1]
        self.ax = dir[0]
        self.ay = dir[1]
        self.vel = dir[2]
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
        self.world_map = world_map

    def is_empty(self, x, y):  # no unit, no blocking terrain
        # print("EMPTY UNIT : ", self.unit_map[x][y])
        # print("EMPTY WORLD : ", self.world_map[x][y])
        return self.unit_map[x][y] == 0 and self.world_map[x][y] == 0

    def is_unit_empty(self, x, y):  # no unit
        return self.unit_map[x][y] == 0

    @staticmethod
    def create_map(lines, columns, value):
        content = []
        for i in range(0, lines):
            line = []
            for j in range(0, columns):
                line.append(value)
            content.append(line)
        return content


class Player:
    def __init__(self, world, player_color):
        self.world = world
        self.color = player_color


class Order:
    def __init__(self, kind=None, x=0, y=0, target=None):
        self.x = x  # (x/32*32)+16
        self.y = y  # (y/32*32)+16
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


class Unit:
    def __init__(self, player, x, y, size, range, life, dom, reload=50):
        self.player = player
        self.real_x = x * 32 + 16
        self.real_y = y * 32 + 16
        self.x = x
        self.y = y
        self.size = size
        self.orders = []
        self.range = range
        self.life = life
        self.dom = dom
        self.reload = reload
        self.cpt = 0
        self.cpt_move = 0
        self.speed_move = 1
        self.speed_step = 2  # must be 1 or a multiple of 2

        # Transitional movement system (TMS)
        self.transition = None
        self.destination = None
        self.previous32 = None

    def __str__(self):
        return str(id(self))

    def update(self):
        self.player.world.unit_map[self.x][self.y] = 0
        # print 'update ', len(self.orders)
        if self.life <= 0:
            return False

        if len(self.orders) > 0:
            o = self.orders[0]
            if o.kind == 'go':
                r = self.go(o.x, o.y)
                if r: del self.orders[0]
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
        self.player.world.unit_map[self.x][self.y] = (1, self)
        return True

    def order(self, o):
        self.orders = [o]

    def add_order(self, o):
        self.orders.append(o)

    def go(self, x, y):

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

            if to_x > from_x:
                n_x = from_x + 1
            elif to_x < from_x:
                n_x = from_x - 1
            elif to_x == from_x:
                n_x = from_x
            if to_y > from_y:
                n_y = from_y + 1
            elif to_y < from_y:
                n_y = from_y - 1
            elif to_y == from_y:
                n_y = from_y

            if self.player.world.is_empty(n_x, n_y):
                self.destination = Pair(n_x * 32 + 16, n_y * 32 + 16)
                self.player.world.unit_map[n_x][n_y] = (-1, self)

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
            self.x = int((self.destination.x - 16) / 32)
            self.y = int((self.destination.y - 16) / 32)
            self.destination = None
            self.transition = None

        # nx = self.x
        # ny = self.y

        # print 'go', x, y, 'from', self.x, self.y
        # if x > self.x:
        # nx += 1
        # elif x < self.x:
        #     nx -= 1
        # if y > self.y:
        #     ny += 1
        # elif y < self.y:
        #     ny -= 1
        #
        # Collision
        # coll = False
        # for u in units:
        #     if u == self: continue
        #     distance = math.sqrt((u.x-nx)**2 + (u.y-ny)**2)
        #     if distance < self.size + u.size:
        #         coll = True
        #         break
        # if not coll:
        #     self.x = nx
        #     self.y = ny

        print(self.x, self.y, "tr= ", self.transition, "dst= ", self.destination)
        return self.x == x and self.y == y

my_map = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

print('map x :', len(my_map[0]))
print('map y :', len(my_map))
# print(">>> ", str(my_map[10][8]))

w1 = World(my_map)
j1 = Player(w1, Color(255, 255, 0))
j2 = Player(w1, Color(0, 255, 255))

units = [Unit(j1, 1, 1, size=10, range=100, life=100, dom=5),
         Unit(j1, 3, 3, size=10, range=150, life=100, dom=10),
         Unit(j2, 12, 12, size=20, range=30, life=300, dom=20)]

camera = Camera(800, 600, 5, j1)  # x, y, scroll, player

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


def select_zone(x, y, w, h, player):
    x = math.trunc(x / 32)
    y = math.trunc(y / 32)
    w = math.trunc(w / 32)
    h = math.trunc(h / 32)
    # print(x, y, w, h)
    ul = []
    if x == w and y == h:  # a square
        t = w1.unit_map[x][y]
        if not w1.is_unit_empty(x, y):
            if t[1].player == player:
                ul.append(t[1])
    else:  # a zone
        for i in range(x, w):
            for j in range(y, h):
                # print(i, j)
                t = w1.unit_map[i][j]
                if not w1.is_unit_empty(i, j):
                    # print(">>>> ", t, " i= ", i, " j= ", j, " empty? ",  w1.is_empty(i, j), " content = ", w1.unit_map[i][j])
                    if t[1].player == player:
                        ul.append(t[1])
    # DEBUG
    for u in ul:
        print(u)
    return ul


def x2r(x, X):
    return x * 32 + camera.x + 16


def y2r(y, Y):
    return y * 32 + camera.y + 16

SELECT_X = 0
SELECT_Y = 0
SELECT_R = False
INTERFACE_Y = 480
selected = []


def main_loop():
    global SELECT_R, SELECT_X, SELECT_Y, INTERFACE_Y, selected

    # -----------------------------------------------------------------------------
    # Selection

    add_mod = False

    left = False
    right = False
    up = False
    down = False

    while 1:

        mx, my = pygame.mouse.get_pos()
        mx32 = math.trunc((mx - camera.x) / 32)
        my32 = math.trunc((my - camera.y) / 32)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
                elif event.key == K_DOWN:
                    down = True
                elif event.key == K_UP:
                    up = True
                elif event.key == K_LEFT:
                    left = True
                elif event.key == K_RIGHT:
                    right = True
                elif event.key == K_LSHIFT:
                    print('add_mod!')
                    add_mod = True
            elif event.type == KEYUP:
                if event.key == K_DOWN:
                    down = False
                elif event.key == K_UP:
                    up = False
                elif event.key == K_LEFT:
                    left = False
                elif event.key == K_RIGHT:
                    right = False
                elif event.key == K_LSHIFT:
                    add_mod = False
                    print('stop add mod!')
                elif event.key == K_SPACE:
                    camera.scroll += 1
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not SELECT_R:
                        SELECT_R = True
                        SELECT_X = mx - camera.x
                        SELECT_Y = my - camera.y
            elif event.type == MOUSEBUTTONUP:
                SELECT_R = False
                if event.button == 1:  # Left
                    if mx32 in range(0, w1.size32.x) and my32 in range(0, w1.size32.y):
                        pass
                        # print('map=', my_map[mx32][my32])
                    # print(SELECT_X, SELECT_Y, mx - camera.x, my - camera.y)
                    deb_x = min(SELECT_X, mx - camera.x)
                    fin_x = max(SELECT_X, mx - camera.x)
                    deb_y = min(SELECT_Y, my - camera.y)
                    fin_y = max(SELECT_Y, my - camera.y)
                    ul = select_zone(deb_x, deb_y, fin_x, fin_y, camera.player)
                    if ul:
                        if add_mod:
                            # print('add unit to selection', u, ' (', u.life, ') at [', my_map[mx32][my32], ']')
                            selected += ul  # selected.append(u)
                        else:
                            # print('select unit ', u, ' (', u.life, ') at [', my_map[mx32][my32], ']')
                            selected = ul  # selected = [u]
                    else:
                        selected = []
                elif event.button == 3:  # Right
                    print('button right')
                    #s = select_zone(mx - camera.x, my - camera.y, mx - camera.x, my - camera.y, camera.player)  # list of 1 max
                    s = w1.unit_map[int((mx - camera.x)/32)][int((my - camera.y)/32)]
                    if s == 0: # nothing at the square clicked
                        for u in selected:
                            print(u, u.__class__)
                            if not add_mod:
                                print('set order!')
                                u.order(Order('go', math.trunc((mx - camera.x) / 32), math.trunc((my - camera.y) / 32)))
                                print('go order at ', math.trunc((mx - camera.x) / 32), math.trunc((my - camera.y) / 32))
                            else:
                                print('add order!')
                                print(len(u.orders))
                                u.add_order(Order('go', mx - camera.x, my - camera.y))
                                print(len(u.orders))
                    elif s[1].player != camera.player:
                        for u in selected:
                            if not add_mod:
                                u.order(Order('attack', target=s[1]))
                            else:
                                u.add_order(Order('attack', target=s[1]))
                elif event.button == 2:
                    print('button 3')

                    # -----------------------------------------------------------------------------
                    # Update

        if left: camera.x += camera.scroll
        if right:
            camera.x -= camera.scroll
        if down:
            camera.y -= camera.scroll
        if up:
            camera.y += camera.scroll

        for u in units:
            if not u.update():
                units.remove(u)
                del u

        w1.particles.update()

        # -----------------------------------------------------------------------------
        # Render

        camera.render()

        pygame.time.Clock().tick(30)


if __name__ == '__main__':
    main_loop()
