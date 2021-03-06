from typing import Dict, Type
from utils import NamedObject
import sys

#-------------------------------------------------------------------------------
# LAYER
#-------------------------------------------------------------------------------
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

    def get_rect(self, x, y, w, h):
        r = []
        # print("%d %d %d %d" % (x, y, w, h))
        for lin in range(y, y+h):
            for col in range(x, x+w):
                if self.content[lin][col] != self.default:
                    r.append(self.content[lin][col])
        return r
    
    def set_at(self, x, y, value):
        self.content[y][x] = value
    
    def update(self, old, new):
        for lin in range(0, self.height):
            for col in range(0, self.width):
                if self.content[lin][col] == old:
                    self.content[lin][col] = new
    
    @staticmethod
    def from_content(name: str, width: int, height: int, content): # -> Type[Layer]:
        lay = Layer(name, width, height, 0)
        lay.content = content
        #lay.dump()
        return lay
    
    def dump(self):
        print("Layer@dump self.height = ", self.height)
        print("Layer@dump self.width = ", self.width)
        for lin in range(0, self.height):
            for col in range(0, self.width):
                try:
                    sys.stdout.write('{:2d}'.format(self.content[lin][col]) + " ")
                except IndexError as e:
                    print()
                    print("Layer@dump lin = ", lin)
                    print("Layer@dump col = ", col)
                    raise e
            sys.stdout.write("\n")
    
    def set_rect(self, x: int, y: int, w: int, h: int, val):
        for i in range(x, x + w):
            for j in range(y, y + h):
                self.set_at(i, j, val)
    
    def set_square(self, x: int, y: int, dim: int, val):
        for i in range(x-dim, x+dim+1):
            for j in range(y-dim, y+dim+1):
                self.set_at(i, j, val) 
    
    def set_circle(self, x: int, y: int, radius: int, val):
        for i in range(x - radius, x + radius):
            for j in range(y - radius, y + radius):
                if abs(x-i) <= radius or abs(y-j) <= radius:
                    self.set_at(i, j, val)
    
    def is_valid(self, x: int, y: int):
        return 0 <= x < self.width and 0 <= y < self.height
    
    # Test for each set. Longer but safer. Discard non valid xx, yy UNUSED
    def set_safe_rect(self, x: int, y: int, w: int, h: int, val):
        for i in range(x, x + w):
            for j in range(y, y + h):
                if self.is_valid(i, j):
                    self.set_at(i, j, val)
    
    def set_safe_circle(self, x: int, y: int, radius: int, val):
        for i in range(x - radius, x + radius):
            for j in range(y - radius, y + radius):
                if abs(x-i) <= radius or abs(y-j) <= radius:
                    if self.is_valid(i, j):
                        self.set_at(i, j, val)

#-------------------------------------------------------------------------------
# MAP
#-------------------------------------------------------------------------------
class Map(NamedObject):
    """
        This map is a standard matrix for levels.
        It can have multiple layers : multiple matrix (for units, obstacles, fog of war, etc.)
        The only method to change its content is set_layer
    """
    
    def __init__(self, name : str, width : int, height : int, layers : Dict[str, Type[Layer]]):
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
    
    def add_layer(self, layername, default):
        self.layers[layername] = Layer(layername, self.width, self.height, default)
    
    def is_valid_at(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height
    
    def is_valid_rect(self, x: int, y: int, w: int, h: int) -> bool:
        if 0 <= x < self.width and 0 <= y < self.height:
            if x + w < self.width and y + h <= self.height:
                return True
        return False
    
    def is_equal_at(self, layer: str, x: int, y: int, val) -> bool:
        if layer not in self.layers:
            raise Exception("Invalid layer!")
        if not self.is_valid_at(x, y):
            raise Exception("Out of bound!")
        return self.layers[layer].get_at(x, y,) == val
    
    def is_equal_rect(self, layer: str, x: int, y: int, w: int, h: int, val) -> bool:
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

    def get_rect(self, layer: str, x: int, y: int, w: int, h: int):
        if layer not in self.layers:
            raise Exception("Invalid layer!")
        if not self.is_valid_rect(x, y, w, h):
            raise Exception("Out of bound! %d %d %d %d" % (x, y, w, h))
        return self.layers[layer].get_rect(x, y, w, h)

    def set_at(self, layer: str, x: int, y: int, val):
        if layer not in self.layers:
            raise Exception("Invalid layer!")
        if not self.is_valid_at(x, y):
            raise Exception("Out of bound!")
        self.layers[layer].set_at(x, y, val)

    def set_rect(self, layer: str, x: int, y: int, w: int, h: int, val):
        if self.is_valid_rect(x, y, w, h):
            self.layers[layer].set_rect(x, y, w, h, val)
    
    def set_square(self, layer: str, x: int, y: int, dim: int, val):
        if self.is_valid_rect(x, y, dim, dim):
            self.layers[layer].set_square(x, y, dim, val)
    
    def set_circle(self, layer: str, x: int, y: int, radius: int, val):
        if self.is_valid_rect(x-radius, y-radius, radius * 2, radius * 2):
            self.layers[layer].set_circle(x, y, radius, val)
    
    def set_circle_from_rect(self, layer: str, x: int, y: int, w: int, h: int, radius: int, val):
        for i in range(x - radius, x + w + radius):
            for j in range(y - radius, y + h + radius):
                if min(abs(x-i), abs(x+w-i)) <= radius or min(abs(y-j), abs(y+h-i)) <= radius:
                    if self.is_valid_at(i, j):
                        self.layers[layer].set_at(i, j, val)

    @staticmethod
    def from_csv(mapname: str, layername: str, filename: str, sep: str=";"):
        f = open(filename, "r")
        lines = f.readlines()
        height = len(lines)
        width = None
        nbcell = 0
        xlines = []
        for lin in lines:
            lin = lin.rstrip()
            xcol = []
            columns = lin.split(sep)
            if width is None:
                width = len(columns)
            elif width != len(columns):
                Exception("Incoherent csv")
            for j in columns:
                keys = {"0" : 0, "1" : 1, "2" : 2, "10" : 10, "20" : 20, "30" : 30, "31" : 30, "32" : 30, "33" : 30, "3A": 30, "40" : 40, "4A" : 40, "50" : 50, "60" : 60}
                if j in keys:
                    xcol.append(keys[j])
                else:
                    raise Exception("Wrong value: [" +  str(j) +"]")
                nbcell += 1
            #print(len(xcol))
            xlines.append(xcol)
        m = Map(mapname, width, height, {"ground" : 0})
        m.layers[layername] = Layer.from_content(layername, width, height, xlines)
        #print("width = ", width)
        #print("height = ", height)
        #print("cells = ", nbcell)
        return m

#-------------------------------------------------------------------------------
# MAPTESTS
#-------------------------------------------------------------------------------
class MapTests:

    def __init__(self):
        self.test_layer1()
        self.test_layer2()
    
    def test_layer1(self):
        """
            Cover:
                Layer#__init__
                Layer#get_at
                Layer#set_at
                Layer#dump
        """
        print("\nTest 1 ===============================================")
        layer = Layer("test1", 5, 5, 0)
        print("[TEST] Layer(\"test1\", 5, 5, 0)", layer is not None)
        print("[ACTI] layer.dump()")
        layer.dump()
        print("[TEST] layer.get_at(4, 4) should be equal to 0", layer.get_at(4, 4) == 0)
        print("[TEST] layer.get_at(0, 3) should be equal to 0", layer.get_at(0, 3) == 0)
        print("[TEST] layer.set_at(0, 3, 22)", layer.set_at(0, 3, 22) == None)
        print("[ACTI] layer.dump()")
        layer.dump()
        print("[TEST] layer.get_at(0, 3) should be equal to 22", layer.get_at(0, 3) == 22)
        
    def test_layer2(self):
        """
            Cover:
                Layer.from_content
                Layer#get_at
                Layer#dump
                Layer#update
        """
        print("\nTest 2 ===============================================")
        print("[ACTI] Layer.from_content(\"test2\", 4, 4, [[0, 0, 0, 0], [1, 11, 1, 1], [2, 2, 22, 2], [1, 3, 3 ,33]])")
        layer = Layer.from_content("test2", 4, 4, [[0, 0, 0, 0], [1, 11, 1, 1], [2, 2, 22, 2], [1, 3, 3 ,33]])
        print("[ACTI] layer.dump()")
        layer.dump()
        print("[ACTI] layer.update(1, 44)")
        layer.update(1, 44)
        print("[TEST] layer.get_at(0, 3) should be equal to 44", layer.get_at(0, 3) == 44)
        print("[ACTI] layer.dump()")
        layer.dump()

if __name__ == '__main__':
    MapTests()

