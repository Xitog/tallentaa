#! /usr/bin/env python

__version__ = "$Revision: 1 $"

# http://ezide.com/games/code_examples/example.py
# http://pygame.org/docs/ref/draw.html#pygame.draw.rect

# div X and Y by 32 + math.trunc -> give the square where we are
# multiply by 32 -> give where we start to display

import pygame
import math
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

UnitType = namedtuple("UnitType", "size range life dom")  # or ['size', 'range', 'life', 'dom']


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

    def select_zone(self, x, y, w, h):  # , player)
        x //= 32
        y //= 32
        w //= 32
        h //= 32
        ul = []
        if x == w and y == h:  # a square
            t = self.player.world.unit_map[x][y]
            if self.player.world.is_unit(x, y):
                # if t[1].player == player:
                ul.append(t[1])
        else:  # a zone
            for i in range(x, w):
                for j in range(y, h):
                    # print(i, j)
                    t = self.player.world.unit_map[i][j]
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
                    if my > self.INTERFACE_Y and self.SELECT_Y > self.INTERFACE_Y:
                        if self.mode == 'normal':
                            a = mx // 32
                            b = (my-self.INTERFACE_Y) // 32
                            if a == 0 and b == 0:
                                self.mode = 'build'
                        elif self.mode == 'build':
                            pass
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
                                    self.selected = ul
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
                            pass  # TODO Build Here. And Put in  Unit Map (-1, id) ? dans Game create_bat
                elif event.button == 3:  # Right Button
                    if self.mode == 'build':
                        self.mode = 'normal'
                    elif len(self.selected) == 1 and self.selected[0].player != self.player:
                        pass
                    else:
                        print('button right')
                        s = self.player.world.unit_map[int((mx - self.x)/32)][int((my - self.y)/32)]
                        if s == 0:  # nothing at the square clicked
                            for u in self.selected:
                                print(u, u.__class__)
                                if not self.add_mod:
                                    print('set order!')
                                    u.order(Order('go', (mx - self.x) // 32, (my - self.y) // 32))
                                    print('go at ', (mx - self.x) // 32, (my - self.y) // 32)
                                else:
                                    print('add order!')
                                    print(len(u.orders))
                                    u.add_order(Order('go', mx - self.x, my - self.y))
                                    print(len(u.orders))
                        elif s[1].player != self.player:
                            for u in self.selected:
                                if not self.add_mod:
                                    u.order(Order('attack', target=s[1]))
                                else:
                                    u.add_order(Order('attack', target=s[1]))
                elif event.button == 2:  # Middle Button
                    print('button 3')

        if self.left:
            self.x += self.scroll
        if self.right:
            self.x -= self.scroll
        if self.down:
            self.y -= self.scroll
        if self.up:
            self.y += self.scroll

        for u in self.player.world.units:
            if not u.update():
                self.player.world.units.remove(u)
                del u

        self.player.world.particles.update()
        return True

    def render(self):
        mx, my = pygame.mouse.get_pos()  # repeat from main_loop
        self.screen.fill(BLACK)

        for yy in range(0, self.player.world.size32.y):
            for xx in range(0, self.player.world.size32.x):
                r = self.player.world.world_map[xx][yy]
                if r == 1:
                    pygame.draw.rect(self.screen, RED, (xx * 32 + self.x, yy * 32 + self.y, 32, 32), 1)
                else:
                    pygame.draw.rect(self.screen, GREEN, (xx * 32 + self.x, yy * 32 + self.y, 32, 32), 1)
                u = self.player.world.unit_map[xx][yy]
                if u == 0:
                    pass
                elif u[0] == -1:
                    pygame.draw.rect(self.screen, HALF_RED, (xx * 32 + self.x, yy * 32 + self.y, 32, 32), 0)
                else:
                    pygame.draw.rect(self.screen, HALF_BLUE, (xx * 32 + self.x, yy * 32 + self.y, 32, 32), 0)
                label = self.font.render(str(xx) + ", " + str(yy), 1, (255, 255, 0))
                self.screen.blit(label, (int(xx * 32 + self.x), int(yy * 32 + self.y)))

        if self.mode == 'normal':
            if self.SELECT_R:
                r = xrect(self.SELECT_X + self.x, self.SELECT_Y + self.y, mx, my)
                pygame.draw.rect(self.screen, WHITE, r, 1)
        else:
            xx = (mx - self.x) // 32
            yy = (my - self.y) // 32
            # center the thing
            cw = self.build_size.x // 2
            ch = self.build_size.y // 2
            # test if ok
            v = self.player.world.is_empty_zone(xx-cw, yy-ch, self.build_size.x, self.build_size.y)
            if v:
                c = BLUE
            else:
                c = RED
            pygame.draw.rect(self.screen, c, ((xx-cw)*32+self.x, (yy-ch)*32+self.y, self.build_size.x*32,
                                              self.build_size.y*32), 0)

        for u in self.player.world.units:
            if u in self.selected:
                c = BLUE
                if u.player != self.player:
                    c = RED
                if len(u.orders) > 0:
                    lx = u.real_x
                    ly = u.real_y
                    for o in u.orders:
                        if o.kind == 'go':
                            pygame.draw.circle(self.screen, c, (self.x2r(o.x), self.y2r(o.y)), 5, 0)
                            pygame.draw.line(self.screen, c, (lx + self.x, ly + self.y), (self.x2r(o.x), self.y2r(o.y)),
                                             1)
                            lx = o.x
                            ly = o.y
                        elif o.kind == 'attack':
                            pygame.draw.circle(self.screen, RED, (o.target.x*32+16 + self.x, o.target.y*32+16 + self.y),
                                               5, 0)
                            pygame.draw.line(self.screen, RED, (lx + self.x, ly + self.y),
                                             (o.target.x*32+16 + self.x, o.target.y*32+16 + self.y), 1)
                            lx = o.target.x
                            ly = o.target.y
            else:
                c = u.player.color
            pygame.draw.circle(self.screen, c, (u.real_x + self.x, u.real_y + self.y), u.size, 0)

        for p in self.player.world.particles.core:
            pygame.draw.circle(self.screen, RED, (p.x + self.x, p.y + self.y), 3, 0)

        # Interface
        pygame.draw.rect(self.screen, GREY, (0, self.INTERFACE_Y, 799, 200), 0)
        pygame.draw.line(self.screen, BLUE, (0, self.INTERFACE_Y), (799, self.INTERFACE_Y), 1)
        for xx in range(0, 3):
            for yy in range(0, 3):
                pygame.draw.rect(self.screen, BLUE, (xx * 32, yy * 32 + self.INTERFACE_Y, 32, 32), 1)
        pygame.draw.line(self.screen, BLUE, (703, self.INTERFACE_Y), (703, self.INTERFACE_Y + 96), 1)
        pygame.draw.line(self.screen, BLUE, (703, self.INTERFACE_Y + 96), (799, self.INTERFACE_Y + 96), 1)

        label = self.font.render('B', 1, (0, 0, 0))
        self.screen.blit(label, (10, self.INTERFACE_Y+10))

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
        self.world_map = world_map
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
                    if self.unit_map[i][j] != 0 or self.world_map[i][j] != 0:
                        return False
            return True

    def is_empty(self, x, y):  # no unit, no blocking terrain
        # print("EMPTY UNIT : ", self.unit_map[x][y])
        # print("EMPTY WORLD : ", self.world_map[x][y])
        return self.unit_map[x][y] == 0 and self.world_map[x][y] == 0

    def is_unit(self, x, y):
        return self.unit_map[x][y] != 0

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
        self.unit_type = {"soldier": UnitType(size=10, range=100, life=100, dom=5),
                          "elite": UnitType(size=10, range=150, life=100, dom=10),
                          "big": UnitType(size=20, range=30, life=300, dom=20)}

    def create_player(self, name, player_color):
        if name in self.players:
            raise Exception("Already a player with this name")
        self.players[name] = Player(self, name, player_color)

    def create_unit(self, player_name, x, y, unit_type_name):
        p = self.get_player_by_name(player_name)
        ut = self.unit_type_by_name(unit_type_name)
        if not self.world.is_valid(x, y):
            raise Exception("False coordinates : " + x + ", " + y)
        self.world.units.append(Unit(p, x, y, ut.size, ut.range, ut.life, ut.dom))

    def get_player_by_name(self, player_name):
        if player_name not in self.players:
            raise Exception("Unknown player : " + player_name)
        return self.players[player_name]

    def unit_type_by_name(self, unit_type_name):  # TODO get_ ?
        if unit_type_name not in self.unit_type:
            raise Exception("Unknown unit type : " + unit_type_name)
        return self.unit_type[unit_type_name]


class Player:
    def __init__(self, game, name, player_color):
        self.game = game
        self.name = name
        self.world = game.world
        self.color = player_color


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


class Unit:
    def __init__(self, player, x, y, size, u_range, life, dom, reload=50):
        self.player = player
        self.real_x = x * 32 + 16
        self.real_y = y * 32 + 16
        self.x = x
        self.y = y
        self.size = size
        self.orders = []
        self.range = u_range
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

            n_x = -1
            n_y = -1
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

        print(self.x, self.y, "tr= ", self.transition, "dst= ", self.destination)
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


def configure():
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
    # print('map x :', len(my_map[0]))
    # print('map y :', len(my_map))

    g = Game('Test 1', World(my_map))
    g.create_player("Bob", YELLOW)
    g.create_player("Henry", SKY_BLUE)
    g.create_unit("Bob", 1, 1, "soldier")
    g.create_unit("Bob", 3, 3, "elite")
    g.create_unit("Henry", 12, 12, "big")

    return Camera(800, 600, 5, g.get_player_by_name("Bob"))  # x, y, scroll, player


def start():
    c = configure()
    main_loop(c)

if __name__ == '__main__':
    start()
    exit()