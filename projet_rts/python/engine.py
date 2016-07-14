import pygame
from pygame.locals import *
from enum import Enum


class Colors(Enum):

    RED = Color(255, 0, 0)
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
    LIGHT_BLUE = Color(0, 128, 255)
    DARK_BLUE = Color(0, 64, 128)
    MINI_MAP_GREEN_DARK = (0, 64, 0)
    MINI_MAP_GREEN_HALF = HALF_GREEN  # terre verte
    MINI_MAP_GREEN_LIGHT = Color(1, 154, 1)  # terre verte claire
    MINI_MAP_BROWN = Color(192, 96, 0)  # terre marron claire
    MINI_MAP_BROWN_DARK = Color(128, 64, 0)  # terre marron sombre pas passable (rochers)
    MINI_MAP_BLUE = BLUE  # eau profonde pas passable
    MINI_MAP_BLUE_LIGHT = Color(113, 123, 255)  # eau claire peu profonde mais pas passable
    MINI_MAP_FOG = Color(32, 32, 32, 128)
    MINI_MAP_BLACK = Color(0, 0, 0, 255)


class Texture:

    def __init__(self, name, num, filename, minicolor, passable=True, mod_x=0, mod_y=0):
        self.name = name
        self.num = num
        if filename.__class__ == str:
            try:
                self.img = pygame.image.load('..\\..\\assets\\tiles32x32\\' + filename).convert_alpha()
            except pygame.error:
                try:
                    self.img = pygame.image.load('..\\..\\assets\\tiles64x32\\' + filename).convert_alpha()
                except pygame.error:
                    self.img = pygame.image.load('..\\..\\assets\\buildings\\' + filename).convert_alpha()
        elif filename.__class__ == pygame.Surface:
            self.img = filename
        self.mini = minicolor
        self.passable = passable
        self.mod_x = mod_x
        self.mod_y = mod_y


class Engine:

    QUIT = pygame.QUIT

    class EventTypes:
        KEY_UP = pygame.locals.KEYUP
        KEY_DOWN = pygame.locals.KEYDOWN
        MOUSE_BUTTON_DOWN = pygame.locals.MOUSEBUTTONDOWN
        MOUSE_BUTTON_UP = pygame.locals.MOUSEBUTTONUP

    class Keys:
        MOUSE_LEFT = 1
        MOUSE_RIGHT = 3
        MOUSE_MIDDLE = 2
        DOWN = pygame.locals.K_DOWN
        UP = pygame.locals.K_UP
        LEFT = pygame.locals.K_LEFT
        RIGHT = pygame.locals.K_RIGHT
        LSHIFT = pygame.locals.K_LSHIFT
        ESCAPE = pygame.locals.K_ESCAPE
        SPACE = pygame.locals.K_SPACE
        TAB = pygame.locals.K_TAB
        RETURN = pygame.locals.K_RETURN
        B = pygame.locals.K_b

    def __init__(self, width, height):
        pygame.init()
        self.size = width, height
        self.screen = pygame.display.set_mode(self.size, pygame.DOUBLEBUF, 32)  # , pygame.FULLSCREEN | pygame.HWSURFACE)
        self.render_orders = []
        self.fonts = {10: pygame.font.SysFont("monospace", 10), 12: pygame.font.SysFont("monospace", 12), 18: pygame.font.SysFont("monospace", 18)}
        self.textures = {}

    def stop(self):
        pygame.quit()

    def text(self, x, y, text, color, z, center=False, size=10):
        label = self.fonts[size].render(text, 1, color.value)
        if center:
            self.tex(x - label.get_width()/2, y - label.get_height()/2, label, z)
        else:
            self.tex(x, y, label, z)

    def tex(self, x, y, tex, z):
        self.render_orders.append((0, x, y, tex, None, None, None, z))

    def rect(self, x, y, w, h, col, thick, z):
        self.render_orders.append((1, x, y, w, h, col, thick, z))

    def circle(self, x, y, r, col, thick, z):
        self.render_orders.append((2, x, y, r, None, col, thick, z))

    def line(self, x1, y1, x2, y2, col, thick, z):
        self.render_orders.append((3, x1, y1, x2, y2, col, thick, z))

    def fill(self, col):
        self.render_orders.append((4, col, None, None, None, None, None, -1))

    def render(self):
        self.render_orders.sort(key=lambda elem: elem[7])
        for o in self.render_orders:
            if o[0] == 0:
                self.screen.blit(o[3], (o[1], o[2]))
            elif o[0] == 1:
                pygame.draw.rect(self.screen, o[5].value, (o[1], o[2], o[3], o[4]), o[6])
            elif o[0] == 2:
                pygame.draw.circle(self.screen, o[5].value, (o[1], o[2]), o[3], o[6])
            elif o[0] == 3:
                pygame.draw.line(self.screen, o[5].value, (o[1], o[2]), (o[3], o[4]), o[6])
            elif o[0] == 4:
                self.screen.fill(o[1].value)
        pygame.display.flip()
        self.render_orders.clear()

    def get_mouse_pos(self):
        return pygame.mouse.get_pos()

    def get_events(self):
        return pygame.event.get()

