#! /usr/bin/env python

__version__ = "$Revision: 1 $"

# http://ezide.com/games/code_examples/example.py
# http://pygame.org/docs/ref/draw.html#pygame.draw.rect

# div X and Y by 32 + math.trunc -> give the square where we are
# multiply by 32 -> give where we start to display

import pygame, sys, math
from pygame.locals import *


class Camera:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.size = width, height
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)


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
            self.x += self.vel*self.ax
            self.y += self.vel*self.ay
        else:
            pass
        # print self.x > self.tx and self.y > self.ty
        if self.x > self.tx and self.y > self.ty:
            self.ttl = 0
        else:
            self.ttl -= 1
        return self.ttl


class World:

    def __init__(self):
        self.particles = Particles()
        self.unit_map = World.create_map(32, 32, 0)

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


class Unit:

    def __init__(self, player, x, y, size, range, life, dom, reload=50):
        self.player = player
        self.real_x = x*32+16
        self.real_y = y*32+16
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
        self.speed_move = 20

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
                if math.sqrt((self.x-o.target.x)**2 + (self.y-o.target.y)**2) > self.range or (self.x-16) % 32 != 0 or (self.y-16) % 32 != 0:
                    self.go(o.target.x, o.target.y)
                elif self.cpt <= 0:
                    world.particles.add(Particle([self.x,self.y], [1, 1, 4], [o.target.x, o.target.y], self.range+10, False))
                    o.target.life -= self.dom
                    self.cpt = self.reload
                    if o.target.life <= 0:
                        del self.orders[0]
                else:
                    self.cpt -= 1
        self.player.world.unit_map[self.x][self.y] = self
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

        # 32 en 32
        from_x = self.x
        from_y = self.y
        to_x = x
        to_y = y

        # print 'destination x,y = ', x,y
        # print 'destination/32 x,y = ', to_x32, to_y32

        if to_x > from_x:
            n_x = from_x+1
        elif to_x < from_x:
            n_x = from_x - 1
        elif to_x == from_x:
            n_x = from_x
        if to_y > from_y:
            n_y = from_y+1
        elif to_y < from_y:
            n_y = from_y - 1
        elif to_y == from_y:
            n_y = from_y

        if self.player.world.unit_map[n_x][n_y] == 0:
            self.x = n_x
            self.y = n_y
            self.real_x = n_x * 32 + 16
            self.real_y = n_y * 32 + 16

        # nx = self.x
        # ny = self.y

        # print 'go', x, y, 'from', self.x, self.y
        # if x > self.x:
        #     nx += 1
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
        return self.x == x and self.y == y

w1 = World()
j1 = Player(w1, Color(255, 255, 0))
j2 = Player(w1, Color(0, 255, 255))

units = [Unit(j1, 1, 1, size=10, range=100, life=100, dom=5),
         Unit(j1, 3, 3, size=10, range=150, life=100, dom=10),
         Unit(j2, 12, 12, size=20, range=30, life=300, dom=20)]

camera = Camera(800, 600)

# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Tools


def xrect(x1, y1, x2, y2):
    tx = abs(x1-x2)
    ty = abs(y1-y2)
    if x1 > x2:
        rx = x2
    else:
        rx = x1
    if y1 > y2:
        ry = y2
    else:
        ry = y1
    return Rect(rx, ry, tx, ty)


def select(x, y):
    global w1
    x = math.trunc(x/32)
    y = math.trunc(y/32)
    if w1.unit_map[x][y] != 0:
        return w1.unit_map[x][y]
    else:
        return False
    # global units
    # for u in units:
    #    if u.real_x-u.size <= x <= u.real_x + u.size and u.real_y-u.size <= y <= u.real_y+u.size:
    #        return u
    # return False


def select_zone(x, y, w, h):
    x = math.trunc(x/32)
    y = math.trunc(y/32)
    w = math.trunc(w/32)
    h = math.trunc(h/32)
    # print(x, y, w, h)
    ul = []
    if x == w and y == h:  # a square
        if w1.unit_map[x][y] != 0:
            ul.append(w1.unit_map[x][y])
    else:  # a zone
        for i in range(x, w):
            for j in range(y, h):
                print(i,j)
                if w1.unit_map[i][j] != 0:
                    ul.append(w1.unit_map[i][j])
    return ul


def x2r(x, X):
    return x*32+X+16


def y2r(y, Y):
    return y*32+Y+16

# -----------------------------------------------------------------------------
# Current setting

my_map = [
    [1, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [0, 0, 1, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [0, 0, 0, 0, 0, 0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [0, 0, 0, 0, 0, 0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [0, 0, 0, 0, 0, 0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [1, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [0, 0, 1, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [0, 0, 0, 0, 0, 0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [0, 0, 0, 0, 0, 0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [0, 0, 0, 0, 0, 0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [0, 0, 0, 0, 0, 0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [0, 0, 0, 0, 0, 0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
    [0, 0, 0, 0, 0, 0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
]

print('mapX :', len(my_map[0]))
print('mapY :', len(my_map))


def main_loop():

    MAP_X = 32  # need ?
    MAP_Y = 32  # need ?

    SIDE_PLAYER = j1  # need ?

    # -----------------------------------------------------------------------------
    # Scrolling

    X = 0
    Y = 0

    SCROLL_MOD = 5

    # -----------------------------------------------------------------------------
    # Selection

    SELECT_X = 0
    SELECT_Y = 0
    SELECT_R = False

    add_mod = False

    selected = []

    left = False
    right = False
    up = False
    down = False

    INTERFACE_Y = 480

    while 1:

        mx, my = pygame.mouse.get_pos()
        mx32 = math.trunc((mx-X) / 32)
        my32 = math.trunc((my-Y) / 32)

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
                    SCROLL_MOD += 1
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not SELECT_R:
                        SELECT_R = True
                        SELECT_X = mx-X
                        SELECT_Y = my-Y
            elif event.type == MOUSEBUTTONUP:
                SELECT_R = False
                if event.button == 1:  # Left
                    if mx32 in range(0, MAP_X) and my32 in range(0, MAP_Y):
                        pass
                        # print('map=', my_map[mx32][my32])
                    print(SELECT_X, SELECT_Y, mx-X, my-Y)
                    deb_x = min(SELECT_X, mx-X)
                    fin_x = max(SELECT_X, mx-X)
                    deb_y = min(SELECT_Y, my-Y)
                    fin_y = max(SELECT_Y, my-Y)
                    ul = select_zone(deb_x, deb_y, fin_x, fin_y)
                    # if select(mx-X, my-Y):
                    if ul:
                        # u = select(mx-X, my-Y)
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
                    s = select(mx-X, my-Y)
                    if not s:
                        for u in selected:
                            if not add_mod:
                                print('set order!')
                                u.order(Order('go', math.trunc((mx-X)/32), math.trunc((my-Y)/32)))
                                print('go order at ', math.trunc((mx-X)/32), math.trunc((my-Y)/32))
                            else:
                                print('add order!')
                                print(len(u.orders))
                                u.add_order(Order('go', mx-X, my-Y))
                                print(len(u.orders))
                    elif s.side != SIDE_PLAYER:
                        for u in selected:
                            if not add_mod:
                                u.order(Order('attack', target=s))
                            else:
                                u.add_order(Order('attack', target=s))
                elif event.button == 2:
                    print('button 3')

    # -----------------------------------------------------------------------------
    # Update

        if left:
            X += SCROLL_MOD
        if right:
            X -= SCROLL_MOD
        if down:
            Y -= SCROLL_MOD
        if up:
            Y += SCROLL_MOD

        for u in units:
            if not u.update():
                units.remove(u)
                del u

        # for p in world.particles.core:
        #     p.update()
        w1.particles.update()

    # -----------------------------------------------------------------------------
    # Render

        # print X, Y

        camera.screen.fill(Color(0, 0, 0, 255))

        for yy in range(0, MAP_Y):
            for xx in range(0, MAP_X):
                # sys.stdout.write(str(my_map[yy][xx]))
                r = my_map[yy][xx]
                if r == 1:
                    pygame.draw.rect(camera.screen, Color(255, 0, 0, 128), (xx*32+X, yy*32+Y, 32, 32), 1)
                else:
                    pygame.draw.rect(camera.screen, Color(0, 255, 0, 128), (xx*32+X, yy*32+Y, 32, 32), 1)

        if SELECT_R:
            r = xrect(SELECT_X+X, SELECT_Y+Y, mx, my)
            pygame.draw.rect(camera.screen, Color(255, 255, 255, 255), r, 1)

        for u in units:
            if u in selected:
                c = Color(0, 0, 255, 255)
                if len(u.orders) > 0:
                    lx = x2r(u.x, X)
                    ly = y2r(u.y, Y)
                    for o in u.orders:
                        if o.kind == 'go':
                            pygame.draw.circle(camera.screen, c, (x2r(o.x, X), y2r(o.y, Y)), 5, 0)
                            pygame.draw.line(camera.screen, c, (lx+X, ly+Y), (x2r(o.x, X), y2r(o.y, Y)), 1)
                            lx = o.x
                            ly = o.y
                        elif o.kind == 'attack':
                            pygame.draw.circle(camera.screen, Color(255, 0, 0), (o.target.x+X, o.target.y+Y), 5, 0)
                            pygame.draw.line(camera.screen, Color(255, 0, 0), (lx+X, ly+Y), (o.target.x+X, o.target.y+Y), 1)
                            lx = o.target.x
                            ly = o.target.y
            else:
                c = u.player.color
            pygame.draw.circle(camera.screen, c, (u.real_x+X, u.real_y+Y), u.size, 0)

        for p in w1.particles.core:
            pygame.draw.circle(camera.screen, Color(255, 0, 0), (p.x+X, p.y+Y), 3, 0)

        # Interface
        pygame.draw.rect(camera.screen, Color(200, 200, 200), (0, INTERFACE_Y, 799, 200), 0)
        pygame.draw.line(camera.screen, Color(0, 0, 255), (0, INTERFACE_Y), (799, INTERFACE_Y), 1)
        for xx in range(0, 3):
            for yy in range(0, 3):
                pygame.draw.rect(camera.screen, Color(0, 0, 255), (xx*32, yy*32+INTERFACE_Y, 32, 32), 1)
        pygame.draw.line(camera.screen, Color(0, 0, 255), (703, INTERFACE_Y), (703, INTERFACE_Y+96), 1)
        pygame.draw.line(camera.screen, Color(0, 0, 255), (703, INTERFACE_Y+96), (799, INTERFACE_Y+96), 1)

        # fin Interface

        # screen.blit(ball, ballrect)
        pygame.display.flip()

        pygame.time.Clock().tick(30)


if __name__ == '__main__':
    main_loop()
