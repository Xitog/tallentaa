import pygame
import math

from pygame.locals import *

BLACK = (0,0,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SKYBLUE = (0, 255, 255)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
GREY = (128, 128, 128)
LIGHT_GREY = (192, 192, 192)
ULTRA_LIGHT_GREY = (224, 224, 224)

class Renderer:

    def __init__(self, title, x, y, color=0, pfps=60):
        pygame.init()
        pygame.display.set_caption('Woolfie 3D')
        self.resolution = (x, y)
        flags = pygame.DOUBLEBUF #| pygame.FULLSCREEN
        if color == 0:
            color = pygame.display.mode_ok(resolution)
        if color == 0:
            raise Exception("Error : can't find a suitable color depth for " + str(resolution) + " mode")
        self.screen = pygame.display.set_mode(self.resolution, flags, color)
        self.clock = pygame.time.Clock()
        self.fps = pfps

    def get_main_screen(self):
        return self.screen
    
    def dot(self, x, y, color):
        pygame.draw.line(self.screen, color, (x, y), (x, y), 1)
    
    def line(self, x1, y1, x2, y2, color):
        pygame.draw.line(self.screen, color, (x1, y1), (x2, y2), 1)
    
    def render(self):
        pygame.display.flip()
        # Limit to 60 fps maximum
        self.clock.tick(self.fps)

class InputHandler:
    
    def __init__(self):
        self.bindings = {}
        self.bindings[KEYDOWN] = {}
        self.bindings[KEYUP] = {}
    
    def set(self, event, type, function):
        self.bindings[type][event] = function
    
    def input(self, obj):
        app_end = False
        for event in pygame.event.get():
            if event.type == QUIT:
                app_end = True
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    app_end = True
            else:
                if event.type in self.bindings:
                    if event.key in self.bindings[event.type]:
                        self.bindings[event.type][event.key](obj)
                    else:
                        print("Key not binded:", event.key, "for event.type=", event.type)
                else:
                    pass #print("Event type not binded:", event.type) #, "for event.key=", event.key)
        return app_end

class Player:

    def __init__(self, x, y, a):
        self.x = x
        self.y = y
        self.a = a
        self.mod_a = 0 # 360
        self.prev_a = self.a
        self.ia = None
        
    def update(self):
        self.a += self.mod_a
        if self.ia is not None:
            self.ia(self)
        #if self.prev_a != self.a:
        #    print("previous a:", self.prev_a, "new a:", self.a)
        #    self.prev_a = self.a
        
    def right(self):
        self.mod_a = 10.0
    
    def left(self):
        self.mod_a = -10.0

    def stop(self):
        self.mod_a = 0.0
     
    def set_ia(self, fun):
        self.ia = fun

class Level:

    def __init__(self):
        self.walls = {}
        self.nb = 0
    
    def add_wall(self, w):
        self.nb += 1
        self.walls[self.nb] = w
    
def test(obj):
    print("P")

WITDH = 640
HEIGHT = 480
    
rd = Renderer('Woolfie 3D', WITDH, HEIGHT, 32)
ih = InputHandler()
ih.set(K_p, KEYDOWN, test)
ih.set(K_RIGHT, KEYDOWN, Player.right)
ih.set(K_LEFT, KEYDOWN, Player.left)
ih.set(K_RIGHT, KEYUP, Player.stop)
ih.set(K_LEFT, KEYUP, Player.stop)

player = Player(100, 100, 0)
#player.set_ia(Player.right)
level = Level()
level.add_wall([160, 50, 160, 150]) # gauche
level.add_wall([160, 150, 10, 150]) # bas
level.add_wall([10, 150, 10, 50])   # droite
level.add_wall([10, 50, 160, 50])   # haut

viewport = []
for i in range(0, WITDH):
    viewport.append((999999999, None, 0, 0, 0))

DEG2RAD = math.pi / 180 # 0.0174532925

# Returns 1 if the lines intersect, otherwise 0. In addition, if the lines 
# intersect the intersection point may be stored in the floats i_x and i_y.
def get_line_intersection(p0_x, p0_y, p1_x, p1_y, p2_x, p2_y, p3_x, p3_y):
    i_x = 0.0
    i_y = 0.0
    # Vectors
    s1_x = p1_x - p0_x
    s1_y = p1_y - p0_y
    s2_x = p3_x - p2_x
    s2_y = p3_y - p2_y

    s = (-s1_y * (p0_x - p2_x) + s1_x * (p0_y - p2_y)) / ((-s2_x * s1_y + s1_x * s2_y) + 0.0000000000000001)
    t = ( s2_x * (p0_y - p2_y) - s2_y * (p0_x - p2_x)) / ((-s2_x * s1_y + s1_x * s2_y) + 0.0000000000000001)

    if s >= 0 and s <= 1 and t >= 0 and t <= 1:
        # Collision detected
        i_x = p0_x + (t * s1_x)
        i_y = p0_y + (t * s1_y)
        return (True, i_x, i_y)

    return (False, 0, 0) # No collision

def get_dist(x1, y1, x2, y2):
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx * dx + dy * dy)
  
app_end = False
while not app_end:
    # 1. Handle events
    app_end = ih.input(player)
    # 2. Update sim
    player.update()
    # 3. Draw screen
    rd.get_main_screen().fill(ULTRA_LIGHT_GREY)
    rd.dot(player.x, player.y, RED)
    # 3.1 Level walls
    for wk in level.walls:
        w = level.walls[wk]
        rd.line(w[0], w[1], w[2], w[3], BLUE)
    # 3.2 Raycasting
    start = player.a - 45.0
    end = player.a + 45.0
    # print("Angle from", start, "to", end)
    nb = 0
    ii = start
    step = 90.0/640.0
    while nb < WITDH:
        dist = 300
        x1 = int(player.x + dist * math.cos(ii*DEG2RAD))
        y1 = int(player.y + dist * math.sin(ii*DEG2RAD))
        # rd.line(player.x, player.y, x1, y1, RED)
        viewport[nb] = (999999999, None, x1, y1, ii) # on met le viewport courant à nul
        for wk in level.walls:
            w = level.walls[wk]
            r = get_line_intersection(player.x, player.y, x1, y1, w[0], w[1], w[2], w[3])
            if r[0]: # intersection
                d = get_dist(player.x, player.y, r[1], r[2])
                #if viewport[nb][0] > d:
                viewport[nb] = (int(d), wk, int(r[1]), int(r[2]), ii) # la distance, le mur en cause, le x et y de l'intersection et l'angle (debug)
        # 2D draw
        if viewport[nb][0] != 999999999: # intersection
            rd.line(player.x, player.y, viewport[nb][2], viewport[nb][3], GREEN)
        else:
            rd.line(player.x, player.y, x1, y1, RED)
        ii += step
        nb += 1
    # 2.5D Test
    nb = 0
    while nb < WITDH:
        if viewport[nb][0] != 999999999:
            d = viewport[nb][1]
            line_height = HEIGHT / d
            rd.line(nb, HEIGHT/2-line_height, nb, HEIGHT/2+line_height, GREEN)
        else:
            pass
        nb += 1
    # Final render
    rd.render()

#print(viewport)
f = open("debug_viewport.txt", "w")
nb = 0
for v in viewport:
    f.write(str(nb) + " -" + str(v) + "\n")
    nb += 1
f.close()

print("goodbye")
pygame.quit()

