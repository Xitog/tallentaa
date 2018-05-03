# Test of random dungeons

import random

VERTICAL = 'Vertical'
HORIZONTAL = 'Horizontal'

GATE = '  ' # '--'

class Room:

    IDS = 0
    
    def __init__(self, name, width, height):
        self.width = width
        self.height = height
        self.children = []
        self.divided = False
        Room.IDS += 1
        self.ids = Room.IDS
        self.sibling_gate = None
        self.name = name
        
    def divide(self, level):
        div = VERTICAL
        if self.width < self.height:
            div = HORIZONTAL
        if div == VERTICAL:
            mid = self.width // 2 #+ random.randint(-2, 2)
            left = Room('left', mid, self.height)
            self.children.append(left)
            left.sibling_gate = ((left.width - 1) // 2, (left.height - 1) // 2)
            right = Room('right', mid, self.height)
            self.children.append(right)
            right.sibling_gate = ((right.width - 1) // 2, 0)
        else: # HORIZONTAL
            mid = self.height // 2 #+ random.randint(-2, 2)
            up = Room('up', self.width, mid)
            self.children.append(up)
            up.sibling_gate = (up.width - 1, (up.height - 1) // 2)
            down = Room('down', self.width, mid)
            self.children.append(down)
            down.sibling_gate = (0, (down.height - 1) // 2)
        self.divided = div
        if level > 1:
            self.children[0].divide(level - 1)
            self.children[1].divide(level - 1)
    
    def render(self, buffer, x = 0, y = 0, level=1):
        print("    " * level + "Room " + self.name + " n ## " + "{:02}".format(self.ids) + " w- " + str(self.width) + ", h| " + str(self.height) + ' [' + str(self.divided) + '] rendered @' + str(x) + ', ' + str(y) + ' Gate: ' + str(self.sibling_gate))
        for column in range(0, self.width):
            for line in range(0, self.height):
                if column == 0 or line == 0 or column == self.width - 1 or line == self.height - 1:
                    buffer[column + x][line + y] = "{:02}".format(self.ids)
                    #if self.sibling_gate is not None and column == self.sibling_gate[1] and line == self.sibling_gate[0]:
                    #    buffer[column + x][line + y] = '  '
                    #else:
                    #    buffer[column + x][line + y] = "{:02}".format(self.ids)
                else:
                    buffer[column + x][line + y] = '  '
        if self.divided == VERTICAL:
            self.children[0].render(buffer, x, y, level + 1)
            self.children[1].render(buffer, x + self.children[1].width, y, level + 1)
        elif self.divided == HORIZONTAL:
            self.children[0].render(buffer, x, y, level + 1)
            self.children[1].render(buffer, x, y + self.children[1].height, level + 1)
        # render gates
        if self.sibling_gate is not None:
            buffer[x + self.sibling_gate[1]][y + self.sibling_gate[0]] = GATE
    
    def display(self, level = 0):
        print("    " * level + "Room " + self.name + " n ## " + "{:02}".format(self.ids) + " w- " + str(self.width) + ", h| " + str(self.height) + ' [' + str(self.divided) + ']' + ' Gate: ' + str(self.sibling_gate))
        for c in self.children:
            c.display(level + 1)

def create_matrix(width, height, default):
    tab = []
    for column in range(0, width):
        ln = []
        for line in range(0, height):
            ln.append(default)
        tab.append(ln)
    return tab

r = Room('main', width=40, height=40) # 30, 20, /2 | OK = 40, 40, / 4 | OK = 10, 10, /2 |
# OK DIV OK GATE, 20, 20, /2
# OK DIV KO!GATE, 40, 40, /4
r.divide(2) #4) # always pair !
r.display()
print()
buffer = create_matrix(r.width, r.height, '-')
r.render(buffer)
print()
for line in range(0, r.height):
    s = ''
    for column in range(0, r.width):
        s += buffer[column][line] + ' '
    print(s)

# 16h42 : premier render
# 17h18 : débuggué :-)

class Space:

    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.matrix = create_matrix(w, h, '+')

class RoomBis:

    def __init__(self, space):
        self.space = space
        self.width = random.randint(10, 20)
        self.height = random.randint(10, 20)
        print(self.width, self.height)

s = Space(40, 40)
r = RoomBis(s)

# https://stackoverflow.com/questions/134934/display-number-with-leading-zeros

#
# TEST TWO
#

class Room:

    IDS = 0
    
    def __init__(self, world, w, h, x, y):
        self.w = w
        self.h = h
        Room.IDS += 1
        self.ids = Room.IDS
        self.x = x
        self.y = y
        self.world = world
        self.render(world)

    def render(self, matrix):
        for line in range(self.x, self.x + self.w):
            for column in range(self.y, self.y + self.h):
                matrix.set(line, column, self.ids)
        
class Matrix:

    def __init__(self, w, h, default=0):
        self.matrix = []
        self.w = w
        self.h = h
        for line in range(0, self.h):
            line = []
            for column in range(0, self.w):
                line.append(default)
            self.matrix.append(line)

    def render(self):
        for line in range(0, self.h):
            s = ''
            for column in range(0, self.w):
                s +=  '{0:02d}'.format(self.matrix[line][column]) + ' '
            print(s)

    def set(self, x, y, val):
        self.matrix[y][x] = val 

world = Matrix(40, 40)
world.render()
print()
r = Room(world, 5, 5, 2, 4)
world.render()


