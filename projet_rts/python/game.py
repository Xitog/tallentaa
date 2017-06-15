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
    def __init__(self, name : str, width : int, height : int, default):
        NamedObject.__init__(self, name)
        self.width = width
        self.height = height
        self.default = default
        self.content = []
        for lin in range(0, self.height):
            self.content.append([])
            for col in range(0, self.width):
                self.content[lin].append(default)
    
    def get_at(self, x, y):
        return self.content[y][x]
    
    def set_at(self, x, y, value):
        self.content[y][x] = value


class Map(NamedObject):
    """
        This map is a standard matrix for levels.
        It can have multiple layers : multiple matrix (for units, obstacles, fog of war, etc.)
        The only method to change its content is set_layer
    """
    
    def __init__(self, name : str, width : int, height : int, layers : dict):
        """
        Create a new WorldMap
              - only square map are handled of %size
              - each map has a name %name
              - a map is divided into layers
                  %layers must be a dict of { layer_name : default_value } 
        """
        NamedObject.__init__(self, name)
        self.width = width
        self.height = height
        if len(layers) < 1:
            raise Exception("A map must have at least one layer!")
        self.layers = {}
        for layer_key in layers:
            self.layers[layer_key] = Layer(layer_key, self.width, self.height, layers[layer_key])
    
    def is_valid_at(self, x: int, y: int):
        return 0 <= x < self.width and 0 <= y < self.height
    
    def is_valid_rect(self, x: int, y: int, w: int, h: int):
        if 0 <= x < self.width and 0 <= y < self.height:
            if x + w < self.width and y + h <= self.height:
                return True
        return False
    
    def is_equal_at(self, layer: str, x: int, y: int, val):
        if layer not in self.layers:
            raise Exception("Invalid layer!")
        if not self.is_valid_at(x, y):
            raise Exception("Out of bound!")
        return self.layers[layer].get_at(x, y,) == val
    
    def is_equal_rect(self, layer: str, x: int, y: int, w: int, h: int, val):
        if layer not in self.layers:
            raise Exception("Invalid layer!")
        if not self.is_valid_rect(x, y, w, h):
            raise Exception("Out of bound!")
        for i in range(x, x+w):
            for j in range(y, y+h):
                if not self.is_equal_at(layer, i, j, val):
                    return False
        return True
    
    def get_at(self, layer: str, x: int, y: int):
        if layer not in self.layers:
            raise Exception("Invalid layer!")
        if not self.is_valid_at(x, y):
            raise Exception("Out of bound!")
        return self.layers[layer].get_at(x, y)

    def set_at(self, layer: str, x: int, y: int, val):
        if layer not in self.layers:
            raise Exception("Invalid layer!")
        if not self.is_valid_at(x, y):
            raise Exception("Out of bound!")
        self.layers[layer].set_at(x, y, val)

    def set_rect(self, layer: str, x: int, y: int, w: int, h: int, val):
        for i in range(x, x + w):
            for j in range(y, y + h):
                self.layers[layer].set_at(i, j, val) 
    
    def set_square(self, layer: str, x: int, y: int, dim: int, val):
        for i in range(x-dim, x+dim+1):
            for j in range(y-dim, y+dim+1):
                self.layers[layer].set_at(i, j, val) 
    
    def set_circle(self, layer: str, x: int, y: int, radius: int, val):
        for i in range(x - radius, x + radius):
            for j in range(y - radius, y + radius):
                if abs(x-i) <= radius or abs(y-j) <= radius:
                    self.layers[layer].set_at(i, j, val)
    
    def set_circle_from_rect(self, layer: str, x: int, y: int, w: int, h: int, radius: int, val):
        for i in range(x - radius, x + w + radius):
            for j in range(y - radius, y + h + radius):
                if min(abs(x-i), abs(x+w-i)) <= radius or min(abs(y-j), abs(y+h-i)) <= radius:
                    if self.is_valid_at(i, j):
                        self.layers[layer].set_at(i, j, val)
    
#------------------------------------------------------------------------------
# Units
#------------------------------------------------------------------------------

class IdObject():
    
    COUNTER_ID = 0
    
    def __init__(self):
        IdObject.COUNTER_ID += 1
        self.id = IdObject.COUNTER_ID

class Profile(NamedObject):
    
    def __init__(self, name: str, life: int, vision: int, width: int = 1, height: int = 1):
        NamedObject.__init__(self, name)
        self.life = life
        self.vision = vision
        self.width = width
        self.height = height

class Unit(IdObject):

    def __init__(self, player, x, y, profile, plife):
        IdObject.__init__(self)
        self.player = player
        self.map = player.game.map
        self.x = x
        self.y = y
        self.width = profile.width
        self.height = profile.height
        self.life = int(profile.life * plife)
        self.vision = profile.vision
        self.profile = profile
        self.map.set_rect("ground", self.x, self.y, self.width, self.height, self.id)
        self.map.set_circle_from_rect("fog", self.x, self.y, self.width, self.height, self.vision, 1)

class Building(Unit):

    def __init__(self, player, x, y, profile, constructed, plife):
        Unit.__init__(self, player, x, y, profile, plife)
        self.constructed = constructed

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
                write(self.view[y][x] + "  ") # invert view
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
        for x in range(0, layer.width):
            for y in range(0, layer.height):
                val = layer.get_at(x, y)
                if raw:
                    self.view[x][y] = f"{val:04d}"
                else:
                    self.view[x][y] = self.render_tile(layer, val)
    
    def render_tile(self, layer, val):
        if layer.name == "ground":
            if val == 1000:
                return ','
            elif val == 2000:
                return '_'
            elif val == 0:
                return '~'
            elif val == Tiles.COAST:
                return '_'
            elif val == Tiles.WATER:
                return '~'
            else:
                return str(val)
        elif layer.name == "fog":
            if val == 0:
                return '~'
            else:
                return ' '
        else:
            return str(val)

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
        self.target.set_rect(layer, x-1, y-1, 3, 3, val2)
        self.target.set_at(layer, x, y, val1)

class Army(NamedObject):

    def __init__(self, name, profiles):
        self.profiles = profiles

class Mod(NamedObject):

    def __init__(self, name, armies):
        NamedObject.__init__(self, name)
        self.armies = armies
        self.all_profiles = {}
        for arm in self.armies:
            for pro in self.armies[arm].profiles:
                if pro in self.all_profiles:
                    raise Exception(f"Duplicated Profile {pro}!")
                else:
                    self.all_profiles[pro] = self.armies[arm].profiles[pro]

    def get_profile(self, name):
        if name not in self.all_profiles:
            raise Exception(f"Unknown profile {name}!")
        else:
            return self.all_profiles[name]

class Player(NamedObject):

    def __init__(self, name, game, army, color):
        NamedObject.__init__(self, name)
        self.game = game
        self.army = army
        self.color = color
    
    def update(self):
        pass
    
class Game:

    def __init__(self, mod, mmap):
        self.mod = mod
        self.map = mmap
        self.players = {}
        self.units = []

    def update(self):
        for p in self.players:
            p.update()
        for u in self.units:
            u.update()
    
    def create_player(self, name, army, color):
        self.players[name] = Player(name, self, self.mod.armies[army], color)

    def create_unit(self, player, profile, x, y, plife=1.0):
        #a = self.players[player].army
        u = Unit(self.players[player], x, y, self.mod.all_profiles[profile], plife)
        self.units.append(u)

FutureWar = Mod("Future War", {
        "RedScum" : Army("Red Scum", {
            "barracks" : Profile("Barracks", 300, vision=3, width=2, height=3),
            "soldier" : Profile("Soldier", 50, vision=3),
            "heavy" : Profile("Heavy soldier", 80, vision=3)
        }),
        "BlueAngels": Army("Blue Angels", {
            "Defender" : Profile("Defender", 60, vision=3)
        }),
    }
)

if __name__ == "__main__":
    world = Map("The Badlands", 11, 15, {"ground" : 1000, "fog" : 0 })
    viewer = Camera(world, 20)
    viewer.render()
    mm = MapModifier(world)
    mm.set("ground", 3, 3, Tiles.WATER, Tiles.COAST)
    viewer.render()

    world.set_at("ground", 10, 1, 'x')
    world.set_at("ground", 1, 10, 'y')

    TrainingGround = Game(FutureWar, world)
    Hicks = Player("Hicks", TrainingGround, FutureWar.armies["RedScum"], "red")
    TrainingGround.players["Hicks"] = Hicks
    TrainingGround.create_player("Zoltan", "BlueAngels", "blue")
    
    plant = Building(Hicks, x=4, y=4, profile=FutureWar.get_profile("barracks"), constructed=1, plife=0.50)
    s1 = Unit(Hicks, x=9, y=9, profile=FutureWar.get_profile("soldier"), plife=0.50)
    TrainingGround.create_unit("Zoltan", "Defender", 4, 7)
    writeln(f"plant life = {plant.life}")
    viewer.render()

    from ctypes import *
    STD_OUTPUT_HANDLE = -11
    class COORD(Structure):
        pass
    COORD._fields_ = [("X", c_short), ("Y", c_short)]

    def print_at(r, c, s):
        h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        windll.kernel32.SetConsoleCursorPosition(h, COORD(c, r))
        c = s.encode("windows-1252")
        windll.kernel32.WriteConsoleA(h, c_char_p(c),  len(c), None, None)
    print_at(6, 3, "Hello") # 13h46 yes !

import time
#import server
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

m = [
    ['H', 'H', 'H', 'H', 'H'],
    ['H', 'H', 'H', 'H', 'H'],
    ['H', 'H', 'H', 'H', 'H'],
    ['H', 'H', 'H', 'H', 'H'],
    ['H', 'H', 'H', 'H', 'H'],
]

def render():
    for lin in m:
        for col in lin:
            if len(col) == 1: sys.stdout.write(" " + col + "  ")
            else: sys.stdout.write(" " + col + " ")
        sys.stdout.write("\n")

def is_trans(x, y):
    return get(x, y)[0] == 't'

def iset(x, y, v):
    if v in ['E', 'H', 'T']:
        set_square(x, y, 1, "t"+v)
        set(x, y, v)
    else:
        if get(x, y) == "E" and v == "tE":
            pass
        elif get(x, y) == "tE" and v == "tE":
            set(x, y, "E")
        elif get(x, y) in ['E', 'H', 'T']:
            set(x, y, v)

# while True:
    # render()
    # command = input('>>> ')
    # if command == 'exit':
        # break
    # elif command == 'help':
        # print('set V X Y  : set a case')
        # print('exit       : exit editor')
    # elif command.startswith('set'):
        # command = command.split(' ')
        # if len(command) != 4:
            # print('Not enough arguments')
        # if command[1] not in ['E', 'H', 'T']:
            # print('Value error')
        # arg2 = int(command[2])
        # arg3 = int(command[3])
        # if not 0 <= arg2 < 5:
            # print('Coordinate error')
        # if not 0 <= arg3 < 5:
            # print('Coordinate error')
        # iset(arg2, arg3, command[1])
