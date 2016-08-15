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


class Map:
    """
        This map is a standard matrix for levels.
        It can have multiple layers : multiple matrix (for units, obstacles, fog of war, etc.)
        The only method to change its content is set_layer
    """
    def __init__(self, size: Pair, layers: int=1):
        self.size = size
        if layers < 1:
            raise Exception("A map must have at least one layer!")
        self.layers = [None] * layers
        self.layer_if_empty = [None] * layers

    def set_layer(self, layer: int=0, base: int=0, content: list=None, empty_test=None):
        if layer < 0 or layer >= len(self.layers):
            raise Exception("Layer level incorrect")
        if content is not None:
            self.layers[layer] = content
        else:
            self.layers[layer] = Map.create_map(self.size.x, self.size.y, base)
        if empty_test is not None:
            self.layer_if_empty[layer] = empty_test
        else:
            def basic_empty(val):
                return val == base
            self.layer_if_empty[layer] = basic_empty

    def is_valid(self, x: int, y: int):
        return 0 <= x < self.size.x and 0 <= y < self.size.y

    def is_valid_zone(self, x: int, y: int, w: int, h: int):
        if 0 <= x < self.size.x and 0 <= y < self.size.y:
            if x + w < self.size.x and y + h <= self.size.y:
                return True
        return False

    def is_empty_zone(self, x: int, y: int, w: int, h: int, layer: int=0):
        if not self.is_valid_zone(x, y, w, h):
            return False
        else:
            for i in range(x, x+w):
                for j in range(y, y+h):
                    if not self.is_empty(i, j, layer):
                        return False
            return True

    def is_empty(self, x: int, y: int, layer: int=0):
        if not self.is_valid(x, y):
            return False
        else:
            return self.layer_if_empty[layer](self.get(x, y, layer))

    def get(self, x: int, y: int, layer: int=0):
        if not self.is_valid(x, y):
            return False
        else:
            return self.layers[layer][y][x]

    def set(self, x: int, y: int, val, layer: int=0):
        if not self.is_valid(x, y):
            return False
        else:
            self.layers[layer][y][x] = val
            return True

    @staticmethod
    def create_map(lines, columns, value):
        content = []
        for i in range(0, lines):
            line = []
            for j in range(0, columns):
                line.append(value)
            content.append(line)
        return content
