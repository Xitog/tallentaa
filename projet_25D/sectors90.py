#-----------------------------------------------------------
# Imports
#-----------------------------------------------------------

import math
import pygame
from pygame.locals import *

#-----------------------------------------------------------
# Constants
#-----------------------------------------------------------

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)

TITLE         = '2.5D Engine'
SCREEN_WIDTH  = 320
SCREEN_HEIGHT = 200
COLOR_DEPTH   = 32
FLAGS         = 0

#-----------------------------------------------------------
# Init code
#-----------------------------------------------------------

pygame.init()
pygame.display.set_caption(TITLE)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FLAGS, COLOR_DEPTH)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)

#-----------------------------------------------------------
# Resources
#-----------------------------------------------------------

greendot = pygame.image.load('green_dot.png').convert_alpha()
# res.sprite_life.set_colorkey((255, 0, 255))

text_surface = font.render('Hello', False, (255, 255, 255))
text_rect = text_surface.get_rect()
print('Text rect:', text_rect, 'center =', text_rect.center)
print('Screen rect:', screen.get_rect(), 'center =', screen.get_rect().center)
text_rect.center = screen.get_rect().center
print(text_rect)

level = {
    'name' : 'The Deep',
    'sectors': {
        1: {
            'walls': [
                [10, 10, 100, 10, 0],
                [10, 10, 10, 100, 0],
                [10, 100, 100, 100, 0],
                [100, 100, 100, 50, 0],
                [100, 50, 100, 10, 2]
            ]
        },
        2: {
            'walls': [
                [100, 50, 100, 10, 1],
                [100, 50, 130, 50, 0],
                [100, 10, 130, 10, 0],
                [130, 50, 130, 10, 3]
            ]
        },
        3 : {
            'walls' : [
                [130, 50, 130, 10, 2],
                [130, 10, 160, 10, 0],
                [160, 10, 160, 60, 0],
                [130, 50, 130, 60, 0],
                [130, 60, 160, 60, 4]
            ]
        },
        4 : {
            'walls' : [
                [130, 60, 160, 60, 3],
                [130, 60, 130, 90, 0],
                [130, 90, 160, 90, 0],
                [160, 90, 160, 60, 5]
            ]
        },
        5 : {
            'walls' : [
                [160, 90, 160, 60, 4],
                [160, 60, 180, 60, 0],
                [160, 90, 180, 90, 0],
                [180, 90, 180, 120, 0],
                [180, 60, 180, 30, 0],
                [180, 30, 260, 30, 0],
                [180, 120, 260, 120, 6],
                [260, 30, 260, 120, 0]
            ]
        },
        6 : {
            'walls' : [
                [180, 120, 260, 120, 5],
                [260, 120, 260, 170, 0],
                [260, 170, 100, 170, 0],
                [100, 170, 100, 100, 0],
                [100, 100, 100, 110, 0],
                [100, 110, 150, 110, 0],
                [150, 110, 150, 120, 0],
                [150, 120, 180, 120, 0]
            ]
        },
        7 : {
            'walls' : [
                [210, 90, 230, 90, 0],
                [210, 60, 230, 60, 0],
                [210, 90, 210, 60, 0],
                [230, 90, 230, 60, 0]
            ]
        },
        8 : {
            'walls' : [
                [130, 140, 240, 140, 6],
                [130, 150, 240, 150, 6],
                [130, 150, 130, 140, 6],
                [240, 150, 240, 140, 6],
            ]
        }
    },
    'objects' : [
        [50, 50, 'life']
    ],
    'start' : [30, 50, 90, 1] # x, y, a, sector
}

#-----------------------------------------------------------
# Functions
#-----------------------------------------------------------

def get_rect(sector):
    min_x = 2000
    min_y = 2000
    max_x = 0
    max_y = 0
    for w in sector['walls']:
        if w[0] < min_x: min_x = w[0]
        if w[1] < min_y: min_y = w[1]
        if w[2] < min_x: min_x = w[2]
        if w[3] < min_y: min_y = w[3]
        if w[0] > max_x: max_x = w[0]
        if w[1] > max_y: max_y = w[1]
        if w[2] > max_x: max_x = w[2]
        if w[3] > max_y: max_y = w[3]
    return min_x, min_y, max_x - min_x, max_y - min_y


def intersect(seg1, seg2):
    ab_seg1 = ab(seg1)
    seg1_min_x = min(seg1[0], seg1[2])
    seg1_max_x = max(seg1[0], seg1[2])
    seg1_min_y = min(seg1[1], seg1[3])
    seg1_max_y = max(seg1[1], seg1[3])
    seg2_min_x = min(seg2[0], seg2[2])
    seg2_max_x = max(seg2[0], seg2[2])
    seg2_min_y = min(seg2[1], seg2[3])
    seg2_max_y = max(seg2[1], seg2[3])
    if ab_seg1[0] is None: # horizontal
        if seg2[0] == seg2[2]: # vertical
            if seg1_min_x <= seg2[0] <= seg1_max_x:
                if seg2_min_y <= seg1_min_y <= seg2_max_y: # 221211
                    #print('vertical', seg2[0], 'minxs1', seg1_min_x, 'maxxs1', seg1_max_x, 'minys1', seg1_min_y, 'maxys1', seg1_max_y, seg2_min_y, seg2_max_y)
                    print('crossed')
                    return True
                elif seg2_min_y <= seg1_max_y <= seg2_max_y:  # 112122
                    print('crossed')
                    return True
                elif seg1_min_y <= seg2_min_y and seg1_max_y >= seg2_max_y:  # 11222211
                    print('crossed')
                    return True
        elif seg2[1] == seg2[3]: # horizontal
            if seg2[1] == seg1[1]: # same line fixée par Y, décrite par X
                if seg2_min_x <= seg1_min_x <= seg2_max_x: # 221211
                    print('crossed')
                    return True
                elif seg2_min_x <= seg1_max_x <= seg2_max_x:  # 112122
                    print('crossed')
                    return True
                elif seg1_min_x <= seg2_min_x and seg1_max_x >= seg2_max_x:  # 11222211
                    print('crossed')
                    return True
        else:
            raise Exception("Wall not angular are not handled")
    elif ab_seg1[1] is None: # vertical
        if seg2[0] == seg2[2]: # vertical
            if seg2[0] == seg1[0]: # same colonne fixée par X, décrite par Y
                if seg2_min_y <= seg1_min_y <= seg2_max_y: # 221211
                    print('crossed')
                    return True
                elif seg2_min_y <= seg1_max_y <= seg2_max_y:  # 112122
                    print('crossed')
                    return True
                elif seg1_min_y <= seg2_min_y and seg1_max_y >= seg2_max_y:  # 11222211
                    print('crossed')
                    return True
        elif seg2[1] == seg2[3]: # horizontal
            if seg1_min_y <= seg2[1] <= seg1_max_y:
                if seg2_min_x <= seg1_min_x <= seg2_max_x: # 221211
                    print('crossed')
                    return True
                elif seg2_min_x <= seg1_max_x <= seg2_max_x:  # 112122
                    print('crossed')
                    return True
                elif seg1_min_x <= seg2_min_x and seg1_max_x >= seg2_max_x:  # 11222211
                    print('crossed')
                    return True
        else:
            raise Exception("Wall not angular are not handled")
    else:
        print(move_left, move_right, move_down, move_up, seg1, ab_seg1)
        if seg2[0] == seg2[2]: # vertical
            raise Exception("A") # True
        elif seg2[1] == seg2[3]: # horizontal
            raise Exception("A") # True
        else:
            raise Exception("Wall not angular are not handled")
    return False


def ab(quad):
    if quad[0] == quad[2]: # vertical x1=x2
        return quad[0], None
    elif quad[1] == quad[3]: # horizontal y1=y2
        return None, quad[1]
    else:
        a = (quad[1] - quad[3]) / (quad[0] - quad[2])
        b = quad[1] - a * quad[0]
    return a, b

#-----------------------------------------------------------
# Data Model
#-----------------------------------------------------------

class Entity:

    def __init__(self, kind, x, y):
        self.kind = kind
        self.x = x
        self.y = y
        self.remove = False

    def activate(self, player):
        if self.kind == 'life':
            player.mod_life(10)
            self.remove = True
    
    def update(self):
        pass


class Player(Entity):

    def __init__(self, x, y, a, s):
        super().__init__('player', x, y)
        self.a = a
        self.sector = s
        self.life = 100
        self.speed = 0.2
        self.dir = self.update_dir()

    def update_dir(self, neg=1):
        dist = 20
        dir_x = int(self.x + dist * math.cos(self.a*0.0174532925) * neg)
        dir_y = int(self.y + dist * math.sin(self.a*0.0174532925) * neg)
        return dir_x, dir_y
    
    def update(self):
        self.dir = self.update_dir()
    
    def mod_life(self, amount):
        self.life = min(max(0, self.life + amount), 999)
        print(f"Player life set to {self.life:3d}")

#-----------------------------------------------------------
# Variables
#-----------------------------------------------------------

start         = level['start']
player        = Player(start[0], start[1], start[2], start[3])
app_end       = False
player_x_old  = player.x
player_y_old  = player.y
move_left     = False
move_right    = False
move_up       = False
move_down     = False
turn_left     = False
turn_right    = False
forward       = False
backward      = False
mod           = 'MAP'
entities      = [player, Entity('life', 20, 20)]

print("Starting Game...")
print("Level is = " + level['name'])
print("Player life is = " + str(player.life))

while not app_end:
    # Drawing picture
    screen.fill(BLACK)
    if mod == 'GAME':
        for i in range(SCREEN_WIDTH):
            pygame.draw.line(screen, GREEN, (i, 50), (i, 150))
        pygame.draw.line(screen, RED, (140, 0), (140, 200))
        screen.blit(greendot, (30, 30))
        screen.blit(text_surface, text_rect)
    elif mod == 'MAP':
        pygame.draw.rect(screen, (50, 50, 50), get_rect(level['sectors'][player.sector]))
        for sector_key, sector in level['sectors'].items():
            for w in sector['walls']:
                color = WHITE if w[4] == 0 else RED
                pygame.draw.line(screen, color, (w[0], w[1]), (w[2], w[3]))
                pygame.draw.rect(screen, GREEN,
                                 (w[0] - 2, w[1] - 2, 5, 5), 1)
                pygame.draw.rect(screen, (0, 255, 0),
                                 (w[2] - 2, w[3] - 2, 5, 5), 1)
            for e in entities:
                if e.kind == 'life':
                    screen.blit(greendot, (e.x - 16, e.y - 16))
        pygame.draw.line(screen, RED, (player_x_old, player_y_old),
                         (player.x, player.y))
        pygame.draw.rect(screen, BLUE, (player.x - 2, player.y - 2, 5, 5))
        pygame.draw.line(screen, BLUE, (player.x, player.y), player.dir, 1)
    pygame.display.flip()
    # Setting framerate by limiting it to 30 fps
    # dt = clock.tick(30)
    dt = clock.tick_busy_loop(30)  # more accurate
    #print(f'Elapsed: {dt} milliseconds')
    # Handling events
    for event in pygame.event.get():
        if event.type == QUIT:
            app_end = True
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:   app_end    = True
            elif event.key == K_DOWN:   move_down  = True
            elif event.key == K_UP:     move_up    = True
            elif event.key == K_LEFT:   move_left  = True
            elif event.key == K_RIGHT:  move_right = True
            elif event.key == K_a:      turn_left  = True
            elif event.key == K_d:      turn_right = True
            elif event.key == K_w:      forward    = True
            elif event.key == K_s:      backward   = True
            else:
                print(f"{event.key:4d}", event.unicode)
        elif event.type == KEYUP:
            if event.key == K_ESCAPE:   app_end    = False
            elif event.key == K_DOWN:   move_down  = False
            elif event.key == K_UP:     move_up    = False
            elif event.key == K_LEFT:   move_left  = False
            elif event.key == K_RIGHT:  move_right = False
            elif event.key == K_a:      turn_left  = False
            elif event.key == K_d:      turn_right = False
            elif event.key == K_w:      forward    = False
            elif event.key == K_s:      backward   = False
            elif event.key == K_TAB:
                mod = 'GAME' if mod == 'MAP' else 'MAP'
    # Updating
    player_x_old = player.x
    player_y_old = player.y
    if move_down:  player.y += player.speed * dt
    if move_up:    player.y -= player.speed * dt
    if move_left:  player.x -= player.speed * dt
    if move_right: player.x += player.speed * dt
    if turn_left:  player.a -= player.speed * dt
    if turn_right: player.a += player.speed * dt
    if forward:    player.x, player.y = player.update_dir()
    if backward:   player.x, player.y = player.update_dir(-1)
    if player.x != player_x_old and player.y != player_y_old:
        player.x = player_x_old
    for e in entities:
        dist = math.sqrt((player.x-e.x)*(player.x-e.x) + (player.y-e.y)*(player.y-e.y))
        #print(dist)
        if dist < 10:
            e.activate(player)
        else:
            e.update()
    entities[:] = [o for o in entities if not o.remove]
    # Check wall
    old_sectors = []
    while True:
        old_sectors.append(player.sector)
        for w in level['sectors'][player.sector]['walls']:
            if intersect([player_x_old, player_y_old, player.x, player.y], w):
                if w[4] == 0:
                    player.x = player_x_old
                    player.y = player_y_old
                    break
                elif w[4] not in old_sectors:
                    player.sector = w[4]
                    print('changing sector', w[4])
                    break
        if player.sector in old_sectors:
            break
    player.dir = player.update_dir()

print("Goodbye")
pygame.quit()

# Portes
# Move gun with the mouse

# secteur 7 : le joueur passe car on ne check que son secteur !

# Fusion de topdown dedans
# TopDown datait du 15 août 2015 
# Transformé en orienté objet le 6 février 2016
