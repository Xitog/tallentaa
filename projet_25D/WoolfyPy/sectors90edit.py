# Todo :
# - Add a way to segment a wall in two
# - Add a way to merge two walls in one
# - Add a way to cancel LAST segment
# - Add a way to save and load a given map
# - Add a way to add an entity and to specify it (typ, p1, p2)
# - Add a way to scroll

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

# External library
import pygame

# Standard library
import math
import json

#-------------------------------------------------------------------------------
# Global variables & constants
#-------------------------------------------------------------------------------

# Colors
GREY       = ( 50,  50,  50)
LIGHT_GREY = (128, 128, 128)
DARK_RED   = (128,   0,   0)
RED        = (255,   0,   0)
GREEN      = (  0, 255,   0)
BLUE       = (  0,   0, 255)
YELLOW     = (255, 255,   0)
BLACK      = (  0,   0,   0)
WHITE      = (255, 255, 255)

# Configuration
BINDING = {
    pygame.K_UP     : 'up',
    pygame.K_DOWN   : 'down',
    pygame.K_LEFT   : 'left',
    pygame.K_RIGHT  : 'right',
    pygame.K_SPACE  : 'start',
    pygame.K_ESCAPE : 'cancel',
    pygame.K_s      : 'save',
    pygame.K_l      : 'load',
    pygame.K_r      : 'restart',
    pygame.K_a      : 'quit',
    }
SPEED_MOVE = 0.05

#-------------------------------------------------------------------------------
# Data model
#-------------------------------------------------------------------------------
# - A Level consists of a collection of Sector.
# - A Sector consists of a collection of Wall.
# - A Level maintains also a list of all its walls in a dict.
#   This dict use (x1, y1, x2, y2) for key, where x1 < x2 and y1 < y2 if x1 == x2
# - A Vector is a vector or a position.
#-------------------------------------------------------------------------------

def key(x1, y1, x2, y2):
    if x1 < x2:
        return (x1, y1, x2, y2)
    elif x1 > x2:
        return (x2, y2, x1, y1)
    elif y1 < y2:
        return (x1, y1, x2, y2)
    elif y1 > y2:
        return (x2, y2, x1, y1)
    else:
        print(x1, y1, x2, y2)
        raise Exception('Start point equals to end point.')
        
class Wall:

    IDW = 1
    VERTICAL = 1
    HORIZONTAL = 2
    
    def __init__(self, s1, x1, y1, x2, y2, s2=None):
        self.idw = Wall.IDW
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.s1 = s1
        self.s2 = s2
        self.maxy = max(y1, y2)
        self.miny = min(y1, y2)
        self.maxx = max(x1, x2)
        self.minx = min(x1, x2)
        if self.maxx == self.minx:
            self.typ = Wall.VERTICAL
        elif self.maxy == self.miny:
            self.typ = Wall.HORIZONTAL
        self.line = key(x1, y1, x2, y2)

    def __str__(self):
        typ = 'H' if self.typ == Wall.HORIZONTAL else 'V'
        return f"{self.x1},{self.y1} - {self.x2},{self.y2} {typ}"
        
    def to_array(self):
        if self.s2 is not None:
            return [self.x1, self.y1, self.x2, self.y2]
        else:
            return [self.x1, self.y1, self.x2, self.y2] #, self.s2]
        
    def __call__(self, f=10):
        return ((self.x1 * f, self.y1 * f), (self.x2 * f, self.y2 * f))

    def __getitem__(self, i):
        return self.line[i]

    def is_portal(self):
        return self.s2 is not None

    def collision_p(self, x, y):
        if self.typ == Wall.VERTICAL:
            return x == self.x1 and self.miny <= y <= self.maxy
        elif self.typ == Wall.HORIZONTAL:
            return y == self.y1 and self.minx <= x <= self.maxx
        #return (x == self.x1 and y == self.y1) or (x == self.x2 and y == self.y2)

    def same(self, w):
        return w.maxx == self.maxx and w.minx == self.minx and w.maxy == self.maxy and w.miny == self.miny

    def collision_w(self, w2):
        if self.typ == Wall.VERTICAL and w2.typ == Wall.VERTICAL:
            if self.x1 != w2.x1: return False
            return self.miny < w2.maxy and self.maxy > w2.miny
        elif self.typ == Wall.HORIZONTAL and w2.typ == Wall.HORIZONTAL:
            if self.y1 != w2.y1: return False
            return self.minx < w2.maxx and self.maxx > w2.minx
        else:
            return self.miny < w2.maxy and self.maxy > w2.miny and self.minx < w2.maxx and self.maxx > w2.minx


class Sector:

    IDS = 1
    
    def __init__(self):
        self.ids = Sector.IDS
        Sector.IDS += 1
        self.walls = []


class Level:

    IDL = 1

    def __init__(self, name, sectors=None):
        self.idl = Level.IDL
        Level.IDL += 1
        self.name = name
        self.sectors = []
        self.walls = {}
        if sectors is not None:
            for s in sectors:
                sec = Sector()
                for w in s:
                    sec.walls.append(self.reg(sec, *w))
                self.sectors.append(sec) 

    def exists(self, wp):
        return wp.line in self.walls
    
    def collision(self, wp):
        override = False
        collided = False
        for kw, w in self.walls.items():
            if w.same(wp):
                override = True
                break
            if w.collision_w(wp):
                collided = True
        #print(override, collided)
        return collided if not override else False
    
    def reg(self, sector, x1, y1, x2, y2):
        k = key(x1, y1, x2, y2)
        if k not in self.walls:
            self.walls[k] = Wall(sector.ids, x1, y1, x2, y2)
        else:
            self.walls[k].s2 = sector
        return self.walls[k]
    
    def to_json(self):
        out = { 'name' : self.name, 'sectors' : []}
        for sec in lvl.sectors:
            out['sectors'].append([])
            for w in sec.walls:
                out['sectors'][-1].append(w.to_array())
        return out


class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, v):
        return Vector(self.x + v.x, self.y + v.y)

    def __str__(self):
        return f"{self.x}:{self.y}"

    def __call__(self):
        return (int(self.x*10), int(self.y*10))

#-------------------------------------------------------------------------------

lvl = None

def restart():
    global lvl
    lvl = Level('The abandonned base',
        ( # sectors
            ( # sector 0
                ( 1,  4, 10,  4),
                (10,  4, 10,  9),
                (10,  9,  5,  9),
                ( 1,  9,  1,  4),
                ( 1,  9,  5,  9)
            ),
            ( # sector 1
                ( 5,  9, 10,  9),
                ( 5,  9,  5, 20),
                ( 5, 20, 10, 20),
                (10, 20, 10,  9)
            ),
         )
    )


#-------------------------------------------------------------------------------
# UI
#-------------------------------------------------------------------------------

def draw_grid(screen, rx, ry, f):
    for x in range(0, 100): # verti
        if x != rx:
            pygame.draw.line(screen, GREY, (x * f, 0), (x * f, 480), 1)
        else:
            pygame.draw.line(screen, LIGHT_GREY, (x * f, 0), (x * f, 480), 1)
    for y in range(0, 100): # hori
        if y != ry:
            pygame.draw.line(screen, GREY, (0, y * f), (640, y * f), 1)
        else:
            pygame.draw.line(screen, LIGHT_GREY, (0, y * f), (640, y * f), 1)


def draw_wall(screen, wall, rx, ry, f=10):
    if wall.is_portal():
        pygame.draw.line(screen, DARK_RED, *wall())
    else:
        if wall.collision_p(rx, ry):
            pygame.draw.line(screen, BLUE, *wall())
        else:
            pygame.draw.line(screen, WHITE, *wall())
    pygame.draw.rect(screen, RED, (wall[0] * f - 2, wall[1] * f - 2, 5, 5), 1)
    pygame.draw.rect(screen, RED, (wall[2] * f - 2, wall[3] * f - 2, 5, 5), 1)


def draw_level(screen, level, rx, ry, f=10):
    for sec in level.sectors:
        for wall in sec.walls:
            draw_wall(screen, wall, rx, ry, f)

#-------------------------------------------------------------------------------
# Main function
#-------------------------------------------------------------------------------

def test():
    global lvl
    print('Level editor for sector based 2.5 FPS')
    print('(q)uit (l)oad (s)ave (space)start (esc)cancel')
    pos = Vector(1.5, 3.2)
    cam = Vector(0.5, 0.8)
    print(pos + cam)
    restart()
    # init
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Vectors")
    pygame.mouse.set_visible(False)
    font = pygame.font.SysFont('Arial', 18, False, False)
    stop = False
    actions = {
        'down'   : False,
        'up'     : False,
        'right'  : False,
        'left'   : False,
        'start'  : False,
        'cancel' : False,
        'save'   : False,
        'load'   : False,
        'restart': False,
        'quit'   : False,
        }
    factor = 10
    # game loop
    amorce = False
    state = 'free'
    while not stop:
        # input
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                stop = True
            elif e.type == pygame.KEYDOWN:
                if e.key in BINDING:
                    actions[BINDING[e.key]] = True
            elif e.type == pygame.KEYUP:
                if e.key in BINDING:
                    actions[BINDING[e.key]] = False
        mx, my = pygame.mouse.get_pos()
        rx = round(mx / factor)
        ry = round(my / factor)
        # update
        if actions['down']:
            pos.y += SPEED_MOVE
        if actions['up']:
            pos.y -= SPEED_MOVE
        if actions['right']:
            pos.x += SPEED_MOVE
        if actions['left']:
            pos.x -= SPEED_MOVE
        if actions['quit'] and not amorce:
            amorce = 'quit'
        elif not actions['quit'] and amorce == 'quit':
            amorce = False
            stop = True
        if actions['restart'] and not amorce:
            amorce = 'restart'
        elif not actions['restart'] and amorce == 'restart':
            amorce = False
            restart()
            print('restarted.')
        if actions['load'] and not amorce:
            amorce = 'load'
        elif not actions['load'] and amorce == 'load':
            f = open('out.map', mode='r', encoding='utf8')
            #content = f.read()
            #f.close()
            data = json.load(f)
            lvl = Level(data['name'], data['sectors'])
            amorce = False
            print(lvl.name, 'loaded.')
        if actions['save'] and not amorce:
            amorce = 'save'
        elif not actions['save'] and amorce == 'save':
            f = open('out.map', mode='w', encoding='utf8')
            amorce = False
            #json.dump(lvl, f, default=to_json)#,indent=4)
            f.write('{\n    "name": "'+ lvl.name + '",\n    "sectors": [\n')
            for i, sec in enumerate(lvl.sectors):
                f.write('        [\n')
                for j, wall in enumerate(sec.walls):
                    if j == len(sec.walls) - 1:
                        f.write(f'            [{wall.x1}, {wall.y1}, {wall.x2}, {wall.y2}]\n')
                    else:
                        f.write(f'            [{wall.x1}, {wall.y1}, {wall.x2}, {wall.y2}],\n')
                if i == len(lvl.sectors) - 1:
                    f.write('        ]\n')
                else:
                    f.write('        ],\n')
            f.write('    ]\n}')
            f.close()
            print(lvl.name, 'saved.')
        if actions['cancel'] and not amorce:
            amorce = 'cancel'
        elif not actions['cancel'] and amorce == 'cancel':
            amorce = False
            if state == 'draw':
                state = 'free'
        if actions['start'] and not amorce:
            amorce = 'start'
        elif not actions['start'] and amorce == 'start':
            amorce = False
            if state == 'free':
                print('free -> draw')
                state = 'draw'
                sec = Sector()
                draw_building = []
                draw_start_x = rx
                draw_start_y = ry
            elif state == 'draw':
                draw_end_x = rx
                draw_end_y = ry
                draw_diff_x = abs(draw_start_x - draw_end_x)
                draw_diff_y = abs(draw_start_y - draw_end_y)
                if draw_diff_x < draw_diff_y:
                    draw_end_x = draw_start_x
                else:
                    draw_end_y = draw_start_y
                draw_building.append(Wall(sec, draw_start_x, draw_start_y, draw_end_x, draw_end_y))
                if len(draw_building) > 1 and draw_building[0].collision_p(draw_end_x, draw_end_y):
                    print('draw -> free')
                    state = 'free'
                    ok = True
                    for w in draw_building:
                        if not lvl.exists(w) and lvl.collision(w):
                            ok = False
                            break
                    if ok:
                        for w in draw_building:
                            sec.walls.append(lvl.reg(sec, *w.line))
                        lvl.sectors.append(sec)
                    else:
                        print("Invalid Sector")
                draw_start_x = draw_end_x
                draw_start_y = draw_end_y
        # draw
        screen.fill(BLACK)
        draw_grid(screen, rx, ry, 10)
        draw_level(screen, lvl, rx, ry)
        pygame.draw.circle(screen, BLUE, pos(), 5, 2)
        if state == 'draw':
            pygame.draw.line(screen, WHITE, (draw_start_x * 10, draw_start_y * 10), (mx, my), 1)
            for w in draw_building:
                draw_wall(screen, w, rx, ry, 10)
        pygame.draw.circle(screen, GREEN, (mx, my), 5, 2)
        s = font.render(lvl.name, False, YELLOW, None)
        screen.blit(s, (620 - s.get_width(), 450))
        s = font.render(f"{mx//10:03d}, {my//10:03d}", False, YELLOW, None)
        screen.blit(s, (0, 450))
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    test()
