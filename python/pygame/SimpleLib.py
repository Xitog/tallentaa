# Une bibliotheque simple.
# Gere la profondeur (axe z)
#

# incorpore :
# - pygame_framework.py du 27/10/2012

# Import
import pygame
from pygame.locals import *

import math # is_in for Circle

# Moyen d'ameliorer les surfaces PyGame en les dotant de plus de methode (enrobage de celle-ci)
class Canvas:
    def __init__(self, pygame_surf):
        self.core = pygame_surf
    
    def circle(self, x, y, radius, color, thickness=0):
        pygame.draw.circle(self.core, color, (x, y), radius, thickness)
    
    def rectangle(self, x, y, width, height, color, thickness=0):
        pygame.draw.rect(self.core, color, (x, y, width, height), thickness)

# La base : un update et draw sur une surface (en fait un Canvas)
class GraphicItem:
    def update(self):
        pass
    
    def draw(self, surface):
        pass
    
    def is_in(self, x, y):
        return False
    
    def on_event(self, event):
        pass

# Un container du DP Composite
class Container(GraphicItem):
    def __init__(self):
        self.content = []
    
    def update(self):
        for e in self.content:
            e[0].update()
        
    def draw(self, surface):
        for e in self.content:
            e[0].draw(surface)
    
    def add(self, gi, z):
        couple = (gi, z)
        inserted = False
        for i in range(0, len(self.content)):
            if self.content[i][1] > z:
                self.content.insert(i, couple)
                inserted = True
        if not inserted:
            self.content.append(couple)

# Un container special qui est en fait l'ecran et l'application a la fois.
class Application(Container):
    
    def __init__(self, title, width, height):
        self.title = title
        self.size = width, height
        
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)
        
        self.clock = pygame.time.Clock()
        self.fixed_fps = 60
        
        self.canvas = Canvas(self.screen)
        Container.__init__(self)
    
    def get_io(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            elif event.type == pygame.MOUSEBUTTONUP:
                for e in self.content:
                    if e[0].is_in(event.pos[0], event.pos[1]):
                        e[0].on_event(event)
    
    def run(self):
        while 1:
            self.clock.tick(self.fixed_fps)
            self.update()
            self.draw(self.canvas)
            pygame.display.flip()
            self.get_io()
    
class Square(GraphicItem):
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
    
    def is_in(self, x, y):
        return x >= self.x and x <= self.x + self.width and y >= self.y and y <= self.y + self.height
    
    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.color = (0, 0, 120)
    
    def update(self):
        self.color = ((self.color[0]+1)%255, self.color[1], self.color[2])
    
    def draw(self, surface):
        surface.rectangle(self.x, self.y, self.width, self.height, self.color, 0)

# Un exemple de graphical item : un cercle
class Circle(GraphicItem):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
    
    def draw(self, surface):
        surface.circle(self.x, self.y, self.radius, self.color, 0)
    
    def is_in(self, x, y):
        return math.sqrt((self.x-x)**2+(self.y-y)**2) <= self.radius
    
    def on_event(self, event):
        self.color = (128, 128, 128)

s = Application("SimpleLib", 640, 400)
s.add(Circle(30, 30, 20, (255, 0, 0)), 10)
s.add(Circle(30, 30, 10, (0, 0, 255)), 11)
s.add(Square(40, 40, 60, 30, (120, 0, 0)), 8)
s.run()

