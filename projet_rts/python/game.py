__author__ = 'dgx'


class NamedObject:
    def __init__(self, name):
        self.name = name
    
    def get_name(self):
        return self.name


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



class Layer(NamedObject):
    """
        A layer of a map.
    """
    def __init__(self, name : str, width : int, height : int, default_value):
        NamedObject.__init__(self, name)
        self.w = width
        self.h = height
        self.default_value = default_value
        self.content = []
        for lin in range(0, self.w):
            self.content.append([])
            for col in range(0, self.h):
                self.content[lin].append(default_value)
    
    def get_at(self, lin, col):
        return self.content[lin][col]
    
    def set_at(self, lin, col, value):
        self.content[lin][col] = value


class Map(NamedObject):
    """
        This map is a standard matrix for levels.
        It can have multiple layers : multiple matrix (for units, obstacles, fog of war, etc.)
        The only method to change its content is set_layer
    """
    
    def __init__(self, name : str, size : Pair, layers : dict):
        """
        Create a new WorldMap
              - only square map are handled of %size
              - each map has a name %name
              - a map is divided into layers
                  %layers must be a dict of { layer_name : default_value } 
        """
        NamedObject.__init__(self, name)
        self.name = name
        self.size = size
        if len(layers) < 1:
            raise Exception("A map must have at least one layer!")
        self.layers = {}
        for layer_key in layers:
            self.layers[layer_key] = Layer(layer_key, self.size.x, self.size.y, layers[layer_key])
    
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
        return self.layers[layer].get_at(x, y,) == val
    
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
    
    def get_at(self, layer: str, x: int, y: int):
        if layer not in self.layers:
            raise Exception("Invalid layer!")
        if not self.is_valid(x, y):
            raise Exception("Out of bound!")
        return self.layers[layer].get_at(x, y)

    def set_at(self, layer: str, x: int, y: int, val):
        if layer not in self.layers:
            raise Exception("Invalid layer!")
        if not self.is_valid(x, y):
            raise Exception("Out of bound!")
        self.layers[layer].set_at(x, y, val)

    def put_object(self, layer, obj):
        """Put on object on the map."""
        for i in range(obj.x, obj.x + obj.w):
            for j in range(obj.y, obj.y + obj.h):
                self.layers[layer].set_at(i, j, obj.id) 

    def radius(self, layer, obj, val):
        for i in range(obj.x1, obj.x2):
            for j in range(obj.y1, obj.y2):
                self.layers[layer].set_at(i, j, val)
    
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
# Units
#------------------------------------------------------------------------------

class IdObject():
    
    COUNTER_ID = 0
    
    def __init__(self):
        IdObject.COUNTER_ID += 1
        self.id = IdObject.COUNTER_ID

class Shadow():

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

class Building(IdObject):

    def __init__(self, x, y, w, h, max_life, vision):
        IdObject.__init__(self)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.wmap = None
        self.constructed = 0
        self.life = max_life
        self.max_life = max_life
        self.vision = vision
        self.shadow = Shadow(x- vision, y - vision, x + w + vision, y + h + vision)

    def create(self, wmap, constructed, plife):
        self.wmap = wmap
        self.constructed = constructed
        self.life = int(self.max_life * plife)
        self.wmap.put_object("ground", self)
        self.wmap.radius("fog", self.shadow, 1)

#------------------------------------------------------------------------------
# Basic Textual Representation (BTR)
#------------------------------------------------------------------------------

import sys

def write(s):
    sys.stdout.write(str(s))

def writeln(s):
    sys.stdout.write(str(s) + "\n")

def newline():
    sys.stdout.write("\n")

class Camera:
    
    def __init__(self, world: Map, size):
        self.world = world
        self.size = size
        self.view = []
        for x in range(0, self.size):
            self.view.append([])
            for y in range(0, self.size):
                self.view[x].append(".")
    
    def render(self, raw=False):
        self.render_map(raw)
        write(" ")
        for y in range(0, self.size):
            write(f" {y:02d}")
        newline()
        for x in range(0, self.size):
            write(f"{x:02d} ")
            for y in range(0, self.size):
                write(self.view[x][y] + "  ")
            newline()
        
    def render_map(self, raw=False):
        """Output the map on the console."""
        print(f"== Map {self.world.name}")
        #for layer_key in self.world.layers:
        #    self.render_layer(self.world.layers[layer_key], raw)
        self.render_layer(self.world.layers["ground"], raw)
        
    def render_layer(self, layer: Layer, raw=False):
        """Output a layer of the map on the console."""
        print(f"-- Layer {layer.get_name()}")
        for lin in range(0, layer.w):
            for col in range(0, layer.h):
                val = layer.get_at(lin, col)
                if raw:
                    self.view[col][lin] = f"{val:04d}"
                else:
                    self.view[col][lin] = self.render_tile(layer, val)
    
    def render_tile(self, layer, val):
        if layer.name == "ground":
            if val == 1000:
                return ','
            elif val == 2000:
                return '_'
            elif val == 0:
                return '~'
            else:
                return '?'
        elif layer.name == "fog":
            if val == 0:
                return '~'
            else:
                return ' '
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
                        self.target.set_at(layer, lin, col, val2.value)
                    else:
                        self.target.set_at(layer, x, y, val1.value)

if __name__ == "__main__":
    world = Map("The Badlands", Pair(10, 15), {"ground" : 1000, "fog" : 0 })
    viewer = Camera(world, 20)
    viewer.render()
    mm = MapModifier(world)
    mm.set("ground", 3, 3, Tiles.WATER, Tiles.COAST)
    viewer.render()

    plant = Building(x=4, y=4, w=2, h=3, max_life=220, vision=4)
    plant.create(world, 1, 0.50)
    writeln(f"plant life = {plant.life}")
    viewer.render()

import time
import server
import threading
import queue

g_queue = queue.Queue()

#g_server = server.Server("localhost", 2222, g_queue)

def start_server():
    g_server.start()
    
#g_server_thread = threading.Thread(target=start_server)
#g_server_thread.start()

def update():
    print("Update")
    if not g_queue.empty():
        while not g_queue.empty():
            val = g_queue.get_nowait()
            print("I got a value in the queue = ", val)

def render():
    pass #print("Affichage")

def main_loop():
    try:
        start = time.time()
        interval = 6
        done = False
        fps = 0
        last_sec = 0
        refresh = False
        while not done:
            elapsed = time.time() - start
            if refresh:
                last_sec = int(elapsed)
                refresh = False
            #print(elapsed)
            if elapsed >= interval:
                update()
                start = time.time()
                # fps count
                refresh = True
            render()
            # fps count
            if last_sec != int(elapsed): # one second has passed
                last_sec = int(elapsed)
                print("FPS = ", fps) # 300 avec un simple print, 1 500 000 sinon !
                fps = 0
            else:
                fps += 1
    except KeyboardInterrupt:
        pass
