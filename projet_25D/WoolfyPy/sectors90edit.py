# Todo :
# - Add a way to segment a wall in two
# - Add a way to merge two walls in one
# - Add a way to cancel LAST segment
# - Add a way to save and load a given map
# - Add a way to add an entity and to specify it (typ, p1, p2)
# - Add a way to scroll
# - Add a way to have gates
# - add a way to move gun with the mouse

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

# External library
import pygame

# Standard library
import random
import math
import json
import sys

#-------------------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------------------

# Pygame
TITLE         = '2.5D Engine'
SCREEN_WIDTH  = 640
SCREEN_HEIGHT = 400
COLOR_DEPTH   = 32
FLAGS         = 0

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

#-------------------------------------------------------------------------------
# Global variables
#-------------------------------------------------------------------------------

# Configuration
BINDING = {
    pygame.K_w      : 'forward',
    pygame.K_s      : 'backward',
    pygame.K_a      : 'strafe_left',
    pygame.K_d      : 'strafe_right',
    pygame.K_q      : 'turn_left',
    pygame.K_e      : 'turn_right',
    
    pygame.K_UP     : 'forward',
    pygame.K_DOWN   : 'backward',
    pygame.K_LEFT   : 'strafe_left',
    pygame.K_RIGHT  : 'strafe_right',
    
    pygame.K_SPACE  : 'start',
    pygame.K_ESCAPE : 'cancel',
    pygame.K_F5     : 'save',
    pygame.K_F9     : 'load',
    pygame.K_r      : 'restart',
    pygame.K_F12    : 'quit',
    pygame.K_TAB    : 'show_map',
    pygame.K_x      : 'segment',
    pygame.K_i      : 'info',
}
SPEED_MOVE = 0.05

#-------------------------------------------------------------------------------
# Tools
#-------------------------------------------------------------------------------

def error(msg):
    sys.stderr.write(msg + '\n')

#-------------------------------------------------------------------------------
# Data model
#-------------------------------------------------------------------------------
# - A Level consists of a collection of Sector.
# - A Sector consists of a collection of Wall.
# - A Level maintains also a list of all its walls in a dict.
#   This dict use (x1, y1, x2, y2) for key, where x1 < x2 and y1 < y2 if x1 == x2
# - A Vector is a vector or a position.
#-------------------------------------------------------------------------------

# key for wall
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
        self.key = key(x1, y1, x2, y2)

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
        return self.key[i]

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
    
    def __init__(self, level, ids):
        self.level = level
        self.ids = int(ids)
        self.wall_keys = []


class Level:

    IDL = 1

    def __init__(self, name):
        self.idl = Level.IDL
        Level.IDL += 1
        self.name = name
        self.sectors = {}
        self.walls = {}
        self.monsters = {}
        self.start = {}
    
    def exists(self, wp):
        return wp.key in self.walls
    
    def collision(self, wp):
        override = False
        collided = False
        for kw, w in self.walls.items():
            if w.same(wp):
                override = True
                break
            if w.collision_w(wp):
                collided = True
        return collided if not override else False

    def add_sector(self, sector_id):
        s = Sector(self, sector_id)
        self.sectors[s.ids] = s
        return s
    
    def add_wall(self, sector, x1, y1, x2, y2):
        k = key(x1, y1, x2, y2)
        if k not in self.walls:
            self.walls[k] = Wall(sector, x1, y1, x2, y2)
        else:
            self.walls[k].s2 = sector
        sector.wall_keys.append(k)

    def add_monster(self, x, y, a, s, kind):
        self.monsters[len(self.monsters)] = Monster(x, y, a, s, kind)

    def set_start(self, start_data):
        self.start = start_data
    
    @staticmethod
    def from_json(data):
        lvl = Level(data['name'])
        for ks, s in data['sectors'].items():
            sec = lvl.add_sector(ks)
            for wall_data in s['walls']:
                lvl.add_wall(sec, *wall_data)
        for i, m in enumerate(data['monsters']):
            lvl.add_monster(m['x'], m['y'], m['a'], m['s'], m['kind'])
        lvl.set_start(data['start'])
        return lvl
    
    def to_json(self):
        out = { 'name' : self.name, 'sectors' : {}, 'monsters' : [], 'start' : self.start}
        for sec in self.sectors.values():
            out['sectors'][sec.ids] = {'walls' : []}
            for w in sec.wall_keys:
                wall = self.walls[w]
                out['sectors'][sec.ids]['walls'].append(wall.to_array())
        for km, m in self.monsters.items():
            out['monsters'].append(m.to_json())
        return out


class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, v):
        return Vector(self.x + v.x, self.y + v.y)

    def __sub__(self, v):
        return Vector(self.x - v.x, self.y - v.y)
    
    def __mul__(self, i):
        return Vector(self.x * i, self.y * i)
    
    def __str__(self):
        return f"{round(self.x,2)}:{round(self.y,2)}"

    def __call__(self):
        return (int(self.x*10), int(self.y*10))


class Monster:

    def __init__(self, x, y, a, s, kind):
        self.x = x
        self.y = y
        self.a = a
        self.s = s
        self.kind = kind

    def to_json(self):
        return { 'x' : self.x, 'y' : self.y, 'a' : self.a, 's' : self.s, 'kind' : self.kind }


class Player:

    MAX_LIFE = 100
    
    def __init__(self, x, y, life=100.0):
        self.life = Player.MAX_LIFE * life // 100
        self.ang = 0
        self.move_speed = 0.02
        self.turn_speed = 0.10
        self.pos = Vector(x, y)
        self.dir = self.update_dir()
        print(self.pos)
        print(self.dir)
    
    def update_dir(self, neg=1):
        dist = 1
        dir_x = dist * math.cos(self.ang * 0.0174532925) * neg
        dir_y = dist * math.sin(self.ang * 0.0174532925) * neg
        return Vector(dir_x, dir_y)

    def forward(self, dt):
        self.pos += self.dir * self.move_speed * dt
        self.dir = self.update_dir()
    
    def backward(self, dt):
        self.pos -= self.dir * self.move_speed * dt
        self.dir = self.update_dir()

    def turn_left(self, dt):
        self.ang -= self.turn_speed * dt
        self.dir = self.update_dir()

    def turn_right(self, dt):
        self.ang += self.turn_speed * dt
        self.dir = self.update_dir()

    def strafe_left(self, dt):
        strafe_ang = self.ang - 90
        strafe_vec_x = math.cos(strafe_ang * 0.0174532925)
        strafe_vec_y = math.sin(strafe_ang * 0.0174532925)
        strafe_vec = Vector(strafe_vec_x, strafe_vec_y)
        self.pos += strafe_vec * self.move_speed * dt
    
    def strafe_right(self, dt):
        strafe_ang = self.ang + 90
        strafe_vec_x = math.cos(strafe_ang * 0.0174532925)
        strafe_vec_y = math.sin(strafe_ang * 0.0174532925)
        strafe_vec = Vector(strafe_vec_x, strafe_vec_y)
        self.pos += strafe_vec * self.move_speed * dt
    
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
    for wall in level.walls.values():
            draw_wall(screen, wall, rx, ry, f)

#-------------------------------------------------------------------------------
# Main function
#-------------------------------------------------------------------------------

class App:

    def __init__(self, title, w, h, flags, colors):
        self.title = title
        self.w = w
        self.h = h
        self.flags = flags
        self.colors = colors
        self.lvl = None
        self.player = None
        print('Level editor for sector based 2.5 FPS')
        print('(q)uit F9 load F5 save (r)estart (space)start (esc)cancel (i)nfo (s)egment')
    
    
    def run(self):
        self.init_pygame()
        self.restart()
        cam = Vector(0.5, 0.8)
        print(self.player.pos + cam)
        stop = False
        actions = {
            'forward'       : False,
            'backward'      : False,
            'turn_right'    : False,
            'turn_left'     : False,
            'strafe_right'  : False,
            'strafe_left'   : False,
            'start'         : False,
            'cancel'        : False,
            'save'          : False,
            'load'          : False,
            'restart'       : False,
            'quit'          : False,
            'show_map'      : False,
            'segment'       : False,
            'info'          : False,
            }
        factor = 10
        # Game loop
        print("Starting Game...")
        print("Level is = " + self.lvl.name)
        print("Player life is = " + str(self.player.life))
        amorce = False
        state = 'free'
        turn = 0
        while not stop:
            turn += 1
            # Input
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    stop = True
                elif e.type == pygame.KEYDOWN:
                    if e.key in BINDING:
                        actions[BINDING[e.key]] = True
                    else:
                        print(f"{event.key:4d}", event.unicode)
                elif e.type == pygame.KEYUP:
                    if e.key in BINDING:
                        actions[BINDING[e.key]] = False
            mx, my = pygame.mouse.get_pos()
            rx = round(mx / factor)
            ry = round(my / factor)
            # Update
            if actions['forward']:      self.player.forward(dt)
            if actions['backward']:     self.player.backward(dt)
            if actions['turn_right']:   self.player.turn_right(dt)
            if actions['turn_left']:    self.player.turn_left(dt)
            if actions['strafe_right']: self.player.strafe_right(dt)
            if actions['strafe_left']:  self.player.strafe_left(dt)
            if actions['quit'] and not amorce:
                amorce = 'quit'
            elif not actions['quit'] and amorce == 'quit':
                amorce = False
                stop = True
            if actions['restart'] and not amorce:
                amorce = 'restart'
            elif not actions['restart'] and amorce == 'restart':
                amorce = False
                self.restart()
                print('restarted.')
            if actions['load'] and not amorce:
                amorce = 'load'
            elif not actions['load'] and amorce == 'load':
                amorce = False
                try:
                    f = open('out.map', mode='r', encoding='utf8')
                    data = json.load(f)
                    self.lvl = Level.from_json(data)
                    print(self.lvl.name, 'loaded.')
                except FileNotFoundError:
                    error('Error while loading out.map')
            if actions['save'] and not amorce:
                amorce = 'save'
            elif not actions['save'] and amorce == 'save':
                f = open('out.map', mode='w', encoding='utf8')
                amorce = False
                data = self.lvl.to_json()
                json.dump(data, f, indent=4)
                f.close()
                print(self.lvl.name, 'saved.')
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
                    sec = Sector(self.lvl, len(self.lvl.sectors))
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
                            if not self.lvl.exists(w) and self.lvl.collision(w):
                                ok = False
                                break
                        if ok:
                            sec = self.lvl.add_sector(len(self.lvl.sectors) + 1)
                            for w in draw_building:
                                self.lvl.add_wall(sec, *w.key)
                        else:
                            print("Invalid Sector")
                    draw_start_x = draw_end_x
                    draw_start_y = draw_end_y
            if actions['show_map'] and not amorce:
                amorce = 'show_map'
            elif not actions['show_map'] and amorce == 'show_map':
                amorce = False
                print("SHOW") # change
            if actions['segment'] and not amorce:
                amorce = 'segment'
            elif not actions['segment'] and amorce == 'segment':
                amorce = False
                selected = []
                for kw, wall in self.lvl.walls.items():
                    if wall.collision_p(rx, ry):
                        selected.append(wall)
                if len(selected) == 1 and not selected[0].is_portal():
                    wall = selected[0]
                    del self.lvl.walls[wall.key]
                    wall.s1.wall_keys.remove(wall.key)
                    if wall.typ == Wall.VERTICAL:
                        self.lvl.add_wall(wall.s1, wall.x1, wall.y1, wall.x2, ry)
                        self.lvl.add_wall(wall.s1, wall.x1, ry, wall.x2, wall.y2)
                    elif wall.typ == Wall.HORIZONTAL:
                        self.lvl.add_wall(wall.s1, wall.x1, wall.y1, rx, wall.y2)
                        self.lvl.add_wall(wall.s1, rx, wall.y1, wall.x2, wall.y2)
            if actions['info'] and not amorce:
                amorce = 'info'
            elif not actions['info'] and amorce == 'info':
                amorce = False
                print('=== Walls ===')
                for w in self.lvl.walls:
                    print(f"{str(w):15} {str(self.lvl.walls[w])}")
                print('=== Sectors ===')
                for s in self.lvl.sectors:
                    print(s)
                    for kw in self.lvl.sectors[s].wall_keys:
                        print('   ', kw)
            # Draw
            self.screen.fill(BLACK)
            draw_grid(self.screen, rx, ry, 10)
            draw_level(self.screen, self.lvl, rx, ry)
            # Draw : Player
            #pygame.draw.circle(self.screen, BLUE, self.player.pos(), 5, 2)
            pygame.draw.rect(self.screen, BLUE, (self.player.pos.x * factor - 2, self.player.pos.y * factor - 2, 5, 5))
            pygame.draw.line(self.screen, BLUE, self.player.pos(), (self.player.pos + self.player.dir)(), 1)
            # Draw : Sector under construction
            if state == 'draw':
                pygame.draw.line(self.screen, WHITE, (draw_start_x * 10, draw_start_y * 10), (mx, my), 1)
                for w in draw_building:
                    draw_wall(self.screen, w, rx, ry, 10)
            pygame.draw.circle(self.screen, GREEN, (mx, my), 5, 2)
            s = self.font.render(self.lvl.name, False, YELLOW, None)
            self.screen.blit(s, (620 - s.get_width(), 450))
            s = self.font.render(f"{mx//10:03d}, {my//10:03d}", False, YELLOW, None)
            self.screen.blit(s, (0, 450))
            pygame.display.update()
            # Setting framerate by limiting it to 30 fps
            dt = self.clock.tick_busy_loop(30)  # more accurate
            #print(f'Elapsed: {dt} milliseconds')
        print("Goodbye")
        pygame.quit()

    
    def init_pygame(self):
        pygame.init()
        pygame.display.set_caption(self.title)
        self.screen = pygame.display.set_mode((self.w, self.h), self.flags, self.colors)
        pygame.mouse.set_visible(False)
        self.font = pygame.font.SysFont('Arial', 18, False, False)
        self.clock = pygame.time.Clock()
    

    def restart(self):
        self.lvl = Level.from_json(
            {
                "name" : "The abandonned base",
                "sectors" : {
                    "1" : {
                        "walls" : [
                            [ 1,  4, 10,  4],
                            [10,  4, 10,  9],
                            [10,  9,  5,  9],
                            [ 1,  9,  1,  4],
                            [ 1,  9,  5,  9]
                        ]
                    },
                    "2" : {
                        "walls" : [
                            [ 5,  9, 10,  9],
                            [ 5,  9,  5, 20],
                            [ 5, 20, 10, 20],
                            [10, 20, 10,  9]
                        ]
                    }
                },
                "monsters" : [
                    {
                        "x" : 120, "y" : 120, "a" : 90, "s" : 6,  "kind" : "Monster"
                    },
                    {
                        "x" : 250, "y" : 70, "a" : 90, "s" : 5, "kind" : "Monster"
                    }
                ],
                "start" :
                {
                    "x" : 3, "y" : 5, "a" : 90, "s" : 0, "life" : 100.0
                }
            }       
        )
        self.player = Player(self.lvl.start['x'], self.lvl.start['y'], self.lvl.start['life'])


if __name__ == '__main__':
    App(TITLE, SCREEN_WIDTH, SCREEN_HEIGHT, FLAGS, COLOR_DEPTH).run()
