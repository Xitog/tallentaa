
# creuser des portes entre feuilles
# creuser des portes entre parents des feuilles

import sys
import pygame
from datetime import datetime

import random
import dg_random

# Wall Thickness

d100 = dg_random.Dice(1, 100)

SMALL_wall_thickness = dg_random.Table(d100)
SMALL_wall_thickness.register(dg_random.Interval(1, 100), 1)

BIG_wall_thickness = dg_random.Table(d100)
BIG_wall_thickness.register(dg_random.Interval(1, 80), 1)
BIG_wall_thickness.register(dg_random.Interval(81, 100), 2)

VERY_BIG_wall_thickness = dg_random.Table(d100)
VERY_BIG_wall_thickness.register(dg_random.Interval(1, 40), 1)
VERY_BIG_wall_thickness.register(dg_random.Interval(41, 80), 2)
VERY_BIG_wall_thickness.register(dg_random.Interval(81, 100), 3)

class Division:

    VERTICAL = 'V'
    HORIZONTAL = 'H'
    UNITED = 'U'

    LETTERS =  ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    LETTER_COUNT = -1

    MINIMUM = 3
    SMALL = 4
    BIG = 5
    VERY_BIG = 7

    MINIMUM_TO_DIVIDE = (MINIMUM+1)*2

    WALL_THICKNESS = {
        SMALL : SMALL_wall_thickness,
        BIG : BIG_wall_thickness,
        VERY_BIG : VERY_BIG_wall_thickness
    }
    
    def __init__(self, level, x, y, width, height, div='U', val=-1):
        # level
        self.level = level
        # letter
        Division.LETTER_COUNT += 1
        self.letter = Division.LETTERS[Division.LETTER_COUNT]
        # size
        self.x = x
        self.y = y
        if width < Division.MINIMUM:
            raise Exception('Wrong width: ' + str(width))
        self.width = width
        if height < Division.MINIMUM:
            raise Exception('Wrong height:' + str(height))
        self.height = height
        if width > Division.VERY_BIG and height > Division.VERY_BIG:
            self.size = Division.VERY_BIG
        elif width > Division.BIG and height > Division.BIG:
            self.size = Division.BIG
        else:
            self.size = Division.SMALL
        # wall thickness
        self.wall = Division.WALL_THICKNESS[self.size].roll()[0]
        # sub rooms
        self.sub_one = None
        self.sub_two = None
        # division
        if div not in [Division.VERTICAL, Division.HORIZONTAL, Division.UNITED]:
            raise Exception('Div unknown.')
        self.div = div
        if div == Division.VERTICAL:
            if val < x or val >= x + width:
                raise Exception('Invalid x divider')
        elif div == Division.HORIZONTAL:
            if val < y or val >= y + height:
                raise Exception('Invalid y divider')
        elif div == Division.UNITED:
            if val != -1:
                raise Exception('Invalid val for united')
        # connections
        self.connections = []
        
    def is_leaf(self):
        return self.sub_one is None and self.sub_two is None

    def in_wall(self, lin, col):
        for c in self.connections:
            #print(c[0], c[1], lin, col)
            if lin == c[1] and col == c[0]:
                return False
        return self.y <= lin < self.y + self.wall or self.y + self.height - self.wall <= lin <= self.y + self.height - 1 or self.x <= col < self.x + self.wall or self.x + self.width - self.wall <= col <= self.x + self.width - 1

    def info(self, level=0):
        if self.is_leaf():
            leaf_or_div = "LEAF"
        else:
            if self.div == Division.UNITED:
                leaf_or_div = "United"
            elif self.div == Division.VERTICAL:
                leaf_or_div = f"/ Vertical ({self.val})"
            elif self.div == Division.HORIZONTAL:
                leaf_or_div = f"/ Horizontal ({self.val})"
        print(" " * level * 4, f"x[{self.x}, {self.x + self.width-1}] ({self.width}) y[{self.y}, {self.y + self.height-1}] ({self.height}) {self.letter} {leaf_or_div} ||{self.wall}")
        for c in self.connections:
            print(" " * level * 4, "connection:", c[0], c[1])
        if self.sub_one is not None:
            self.sub_one.info(level + 1)
        if self.sub_two is not None:
            self.sub_two.info(level + 1)
    
    def display(self):
        for lin in range(0, self.height):
            for col in range(0, self.width):
                sys.stdout.write(self.letter)
            print()
        if self.sub_one is not None:
            self.sub_one.display()
        if self.sub_two is not None:
            self.sub_two.display()

    # x indique une colonne !
    # y indique une ligne !
    # x, y = col, lin
    # pour les boucles, on fait for y in lin, puis for x in col et après on peut utiliser x, y
    # car on parcourt l'ensemble des valeurs en premier de la boucle la plus interne !!!
    # level_max starts at 1 (and not 0)
    def divide(self, level_max):
        print(" " * (self.level - 1) * 4, f'Dividing at level {self.level}')
        # Choosing the division
        # we roll a dice, if result > 50, Vertical, else if <= 50 Horizontal
        # but if we can't dividing according to this result, we try to divide the other way
        per = d100.roll()
        if per > 50:
            if self.width > Division.MINIMUM_TO_DIVIDE:
                self.div = Division.VERTICAL
            elif self.height > Division.MINIMUM_TO_DIVIDE:
                self.div = Division.HORIZONTAL
            else:
                return
        else:
            if self.height > Division.MINIMUM_TO_DIVIDE:
                self.div = Division.HORIZONTAL
            elif self.width > Division.MINIMUM_TO_DIVIDE:
                self.div = Division.VERTICAL
            else:
                return
        # Dividing
        if self.div == Division.VERTICAL:
            if self.width > 9:
                quart = int(self.width / 4)
            else:
                quart = 1
            chance = random.randint(-quart, quart)
            print(" " * (self.level-1) * 4, 'VERTICAL', 'width=', self.width, 'quart=', quart, 'chance=', chance)
            self.val = int(self.width / 2) + chance
            print(" " * (self.level-1) * 4, f'X: {self.x} < {self.x + self.val} < {self.x+self.width-1}')
            self.sub_one = Division(self.level + 1, self.x, self.y, self.val, self.height)
            self.sub_two = Division(self.level + 1, self.x + self.val, self.y, self.width - self.val, self.height)
            if self.level == level_max:
                # connect the two sub room
                min_conn = self.sub_one.y + self.sub_one.wall
                max_conn = self.sub_one.y + self.height - self.sub_one.wall - 1
                connection = random.randint(min_conn, max_conn)
                for i in range(0, self.sub_one.wall):
                    self.sub_one.connections.append((self.sub_one.x + self.sub_one.width - 1 - i, connection)) # ex: x=5, wid=3, wal=1 x[5, 6, 7]<- perce
                for i in range(0, self.sub_two.wall):
                    self.sub_two.connections.append((i + self.sub_two.x, connection)) # ex: x=5, wid=3, wal=1 perce->x[5, 6, 7]
        elif self.div == Division.HORIZONTAL:
            if self.height > 9:
                quart = int(self.height / 4)
            else:
                quart = 1
            chance = random.randint(-quart, quart)
            print(" " * (self.level-1) * 4, 'HORIZONTAL', 'height=', self.height, 'quart=', quart, 'chance=', chance)
            self.val = int(self.height / 2) + chance
            print(" " * (self.level-1) * 4, f'Y: {self.y} < {self.y + self.val} < {self.y+self.height-1}')
            self.sub_one = Division(self.level + 1, self.x, self.y, self.width, self.val)
            self.sub_two = Division(self.level + 1, self.x, self.y + self.val, self.width, self.height - self.val)
            if self.level == level_max:
                # connect the two sub room
                # Ex 1 : x[11, 17] (7) y[14, 29] (16) i LEAF ||2 : 11 12 13 14 15 16 17
                # Ex 2 : x[0, 2] (3) ||1 : 0 1 2
                min_conn = self.sub_one.x + self.sub_one.wall # 13 | 1
                max_conn = self.sub_one.x + self.width - self.sub_one.wall - 1 # 15
                connection = random.randint(min_conn, max_conn)
                for i in range(0, self.sub_one.wall):
                    self.sub_one.connections.append((connection, self.sub_one.y + self.sub_one.height - 1 - i))
                for i in range(0, self.sub_two.wall):
                    self.sub_two.connections.append((connection, i + self.sub_two.y))
        if self.level < level_max:
            self.sub_one.divide(level_max)
            self.sub_two.divide(level_max)
        
        
class Dungeon:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root = Division(1, 0, 0, width, height)
    
    def create(self, level_max):
        self.root.divide(level_max)
        
    def display(self):
        self.root.display()

class Renderer:

    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 32)
        
    def render(self, dungeon):
        self.s = pygame.Surface((dungeon.width * 32, dungeon.height * 32))
        self.render_division(dungeon.root)
        pygame.image.save(self.s, "result" + str(datetime.now()).replace(':','_').split('.')[0] + ".png")
    
    def render_division(self, division, render_conn = False):
        if division.is_leaf():
            letter = self.font.render(division.letter, False, pygame.Color(255, 0, 0))
            letterConn = self.font.render(division.letter, False, pygame.Color(0, 255, 255))
            for lin in range(division.y, division.y + division.height): # range is not inclusive of the max
                for col in range(division.x, division.x + division.width):
                    if division.in_wall(lin, col):
                        self.s.blit(letter, (col*32, lin*32))
            if render_conn:
                for c in division.connections:
                    self.s.blit(letterConn, (c[0]*32, c[1]*32))
        else:
            if division.sub_one is not None:
                self.render_division(division.sub_one)
            if division.sub_two is not None:
                self.render_division(division.sub_two)

d = Dungeon(30, 30)
d.create(3)
#d.display()
d.root.info()
Renderer().render(d)

