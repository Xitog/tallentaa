import math
import pygame
from pygame.locals import *

# Todo : move the gun with the mouse
# Todo : blocking walls
# Todo : 'gate' walls (overlapping sector, like Duke Nukem 3D)
# Fixme : change player's sector when he crosses a 'gate'
# Fixme : new algorithm to check if in

# Init const

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Init var

app_title = 'Zembla'
screen_width = 640
screen_height = 480
screen_resolution = (screen_width, screen_height)
screen_flags = pygame.DOUBLEBUF
color_depth = 32
repeated_delay_first = 1
repeated_delay_next = 50
app_end = False
app_fps = 60

# Init code

pygame.init()
pygame.display.set_caption(app_title)
app_screen = pygame.display.set_mode(screen_resolution, screen_flags, color_depth)
clock = pygame.time.Clock()
# Keys held down will generate multiple pygame.KEYDOWN events
# the first repeated event after DELAY milliseconds and INTERVAL ms after.
pygame.key.set_repeat(repeated_delay_first, repeated_delay_next)

# Loading resource


class Content:
    def __init__(self):
        pass

res = Content()
res.sprite_life = pygame.image.load('heart-beats-a.png').convert_alpha()
# res.sprite_life.set_colorkey((255, 0, 255))

#
# def main_loop():
#     global app_end, app_fps
#     while not app_end:
#         update()
#         render()
#         # Limit to 60 fps maximum
#         clock.tick(app_fps)
#
# def render():
#     global screen
#     screen.fill(BLACK)
#     pygame.display.flip()
#
#
# def update():
#     global app_end
#     # Handle events
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             app_end = True
#         elif event.type == KEYDOWN:
#             if event.key == K_ESCAPE:
#                 app_end = True
#             elif event.key == K_p:
#                 print("P")


class Player:
    def __init__(self, x, y, angle):
        self.a = angle
        self.pos = (x, y)
        self.gun = self.gun_pos()
        self.life = 50

    def gun_pos(self, neg=1):
        dist = 20
        x1 = int(self.pos[0] + dist * math.cos(self.a*0.0174532925) * neg)
        y1 = int(self.pos[1] + dist * math.sin(self.a*0.0174532925) * neg)
        return x1, y1

    def update(self):
        self.gun = self.gun_pos()

    def move(self, right, left, up, down):
        if left:
            self.a -= 10
        if right:
            self.a += 10
        if up:
            self.pos = self.gun_pos()
        if down:
            self.pos = self.gun_pos(-1)
        self.gun = self.gun_pos()

    def add_life(self, amount):
        self.life += amount
        print("Player life is = " + str(self.life))


class Level:
    def __init__(self, name):
        self.name = name
        self.sectors = []
        self.objects = []
        self.player = None
        self.player_sector = None

    def add_sector(self, s):
        self.sectors.append(s)

    def add_object(self, o):
        self.objects.append(o)

    def start(self, player, sector):
        self.player = player
        self.player_sector = sector

    def is_in_sector(self):
        if self.player_sector is None:
            raise Exception("Undefined Player Sector")
        if not 0 <= self.player_sector < len(self.sectors):
            raise Exception("Wrong Player Sector : " + str(self.player_sector))
        s = self.sectors[self.player_sector]
        max_x = 0
        max_y = 0
        min_x = 9999
        min_y = 9999
        for p in s:
            max_x = max(max_x, p[0])
            max_y = max(max_y, p[1])
            min_x = min(min_x, p[0])
            min_y = min(min_y, p[1])
        return min_x <= self.player.pos[0] <= max_x and min_y <= self.player.pos[1] <= max_y

    def update(self):
        for o in self.objects:
            if math.hypot(self.player.pos[0]-o.x-16, self.player.pos[1]-o.y-16) <= 32:
                o.affect(self.player)
                o.kill = True
        self.objects[:] = [o for o in self.objects if not o.kill]


class Enemy:
    def __init__(self):
        pass


class Object:
    def __init__(self, x, y, kind):
        self.x = x
        self.y = y
        self.kind = kind
        self.kill = False

    def affect(self, player):
        if self.kind == "life":
            player.add_life(10)

    def update(self):
        pass


def main_loop(screen):
    global app_end, app_fps

    player1 = Player(40, 40, 90)  # x, y, angle
    level1 = Level("Deep core")
    sector1 = [
        (10, 10),
        (200, 10),
        (200, 200),
        (10, 200)
    ]
    sector2 = [
        (150, 200),
        (150, 400),
        (250, 400),
        (200, 200)
    ]
    level1.add_sector(sector1)
    level1.add_sector(sector2)
    level1.add_object(Object(50, 50, "life"))
    level1.start(player1, 0)

    print("Starting Game...")
    print("Level is = " + level1.name)
    print("Player life is = " + str(player1.life))

    while not app_end:
        update(player1, level1)
        render(screen, player1, level1)
        # Limit to 60 fps maximum
        clock.tick(app_fps)


def render(screen, player, level):
    global res
    screen.fill(BLACK)
    # Level
    # 1-sector
    for s in level.sectors:
        if level.is_in_sector():
            pygame.draw.polygon(screen, GREEN, s, 0)
            pygame.draw.polygon(screen, RED, s, 1)
        else:
            pygame.draw.polygon(screen, RED, s, 0)
            pygame.draw.polygon(screen, GREEN, s, 1)

        #  for w in s:
        #    pygame.draw.line(screen, RED, (w[0], w[1]), (w[2], w[3]), 1)
    # 2-objects
    for o in level.objects:
        if o.kind == "life":
            screen.blit(res.sprite_life, (o.x, o.y))

    # Player
    pygame.draw.circle(screen, BLUE, player.pos, 10, 0)
    pygame.draw.line(screen, BLUE, player.pos, player.gun, 1)
    # Rest
    pygame.display.flip()


def update(player, level):
    global app_end
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            app_end = True
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                app_end = True
            if event.key == K_p:
                print("P")
            if event.key == K_RIGHT:
                player.move(True, False, False, False)
            if event.key == K_LEFT:
                player.move(False, True, False, False)
            if event.key == K_UP:
                player.move(False, False, True, False)
            if event.key == K_DOWN:
                player.move(False, False, False, True)
        elif event.type == KEYUP:
            pass
    # Process
    player.update()
    level.update()

main_loop(app_screen)
print("goodbye")
pygame.quit()
