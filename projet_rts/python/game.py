__author__ = 'dgx'


class Pair:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return "[" + str(self.x) + ", " + str(self.y) + "]"

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)



class Layer:
    """
        A layer of a map.
    """
    def __init__(self, width : int, height : int, val):
        self.w = width
        self.h = height
        self.content = []
        for lin in range(0, self.w):
            line = []
            for col in range(0, self.h):
                line.append(val)
            self.content.append(line)

    def get(self, x, y):
        return self.content[y][x]

    def set(self, x, y, val):
        self.content[y][x] = val


class Map:
    """
        This map is a standard matrix for levels.
        It can have multiple layers : multiple matrix (for units, obstacles, fog of war, etc.)
        The only method to change its content is set_layer
    """
    def __init__(self, name : str, size : Pair, layers : dict):
        self.name = name
        self.size = size
        if len(layers) < 1:
            raise Exception("A map must have at least one layer!")
        self.layers = {}
        for key in layers:
            self.layers[key] = Layer(self.size.x, self.size.y, layers[key])
    
    def is_valid(self, x: int, y: int):
        return 0 <= x < self.size.x and 0 <= y < self.size.y
    
    def is_valid_zone(self, x: int, y: int, w: int, h: int):
        if 0 <= x < self.size.x and 0 <= y < self.size.y:
            if x + w < self.size.x and y + h <= self.size.y:
                return True
        return False
    
    def is_equal(self, layer: str, x: int, y: int, val):
        if layer not in self.layers:
            raise Exception("Invalid layer!")
        if not self.is_valid(x, y):
            raise Exception("Out of bound!")
        return self.layers[layer].get(x, y,) == val
    
    def is_equal_zone(self, layer: str, x: int, y: int, w: int, h: int, val):
        if layer not in self.layers:
            raise Exception("Invalid layer!")
        if not self.is_valid_zone(x, y, w, h):
            raise Exception("Out of bound!")
        for i in range(x, x+w):
            for j in range(y, y+h):
                if not self.is_equal(layer, i, j, val):
                    return False
        return True
    
    def get(self, layer: str, x: int, y: int):
        if layer not in self.layers:
            raise Exception("Invalid layer!")
        if not self.is_valid(x, y):
            raise Exception("Out of bound!")
        return self.layers[layer].get(x, y)

    def set(self, layer: str, x: int, y: int, val):
        if layer not in self.layers:
            raise Exception("Invalid layer!")
        if not self.is_valid(x, y):
            raise Exception("Out of bound!")
        self.layers[layer].set(x, y, val)
    
    @staticmethod
    def create_map(lines, columns, value):
        content = []
        for i in range(0, lines):
            line = []
            for j in range(0, columns):
                line.append(value)
            content.append(line)
        return content


#------------------------------------------------------------------------------
# Basic Textual Representation (BTR)
#------------------------------------------------------------------------------

import sys

class View:
    
    def __init__(self, world: Map):
        self.world = world
    
    def render(self, raw=False):
        self.render_map(raw)
    
    def render_map(self, raw=False):
        print(f"-- Map {self.world.name}")
        for layer in self.world.layers:
            print(f"-- Layer {layer}")
            self.render_layer(self.world.layers[layer], raw)
    
    def render_layer(self, layer: Layer, raw=False):
        for lin in range(0, layer.w):
            sys.stdout.write(f"{lin:02d}. ") # 11h32 formatted string rules!
            for col in range(0, layer.h):
                if raw:
                    sys.stdout.write(f"{self.layer[lin][col]:04d} ")
                else:
                    sys.stdout.write(self.render_tile(layer, lin, col))
            sys.stdout.write("\n")
    
    def render_tile(self, layer, lin, col):
        val = layer.content[lin][col]
        if val == 1000:
            return ','
        elif val == 2000:
            return '_'
        elif val == 0:
            return '~'
        else:
            return '?'

#------------------------------------------------------------------------------
# Tests
#------------------------------------------------------------------------------

import enum

class Tiles(enum.Enum):
    WATER = 0
    GRASS = 1000
    COAST = 2000

class MapModifier:

    def __init__(self, target):
        self.target = target

    def set(self, layer, x, y, val1, val2):
        for lin in range(y-1, y+2):
            for col in range(x-1, x+2):
                if self.target.is_valid(x, y):
                    if lin != y or col != x:
                        self.target.set(layer, lin, col, val2.value)
                    else:
                        self.target.set(layer, x, y, val1.value)

world = Map("Badlands", Pair(6, 6), {"base" : 1000 })
viewer = View(world)
viewer.render()
mm = MapModifier(world)
mm.set("base", 3, 3, Tiles.WATER, Tiles.COAST)
viewer.render()

