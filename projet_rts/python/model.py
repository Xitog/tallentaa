
class Position:

    level = None
    
    @staticmethod
    def set_level(self, level):
        Position.level = level
    
    def __init__(self, x, y, w=1, h=1):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

class Unit:

    ID = 0
    
    def __init__(self, kind, pos, life=100.0, shield=100.0):
        self.kind = kind
        self.pos = pos
        Unit.ID += 1
        self.id = Unit.ID
        self.orders = []
    
    def __str__(self):
        return f"{self.kind} #{self.id} @{self.pos}"

class Group:

    maximum = None
    
    def __init__(self):
        self.units = []

    def append(self, unit):
        if maximum is None or len(self.units) < maximum:
            self.units.append(unit)

class Player:

    def __init__(self, name, side):
        self.name = name
        self.side = side
        self.units = []
        self.groups = []

class Game:

    def __init__(self, level):
        self.players = []
        self.level = level
        Position.set_level(level)

class Doodad:

    def __init__(self, pos, kind):
        self.pos = pos
        self.kind = kind

class Map:

    def __init__(self, name, width, height):
        self.name = name
        self.content = [[]]
        self.triggers = []
        self.doodads = []
        self.width = width
        self.height = height

class Trigger:

    def __init__(self):
        self.conditions = []
        self.actions = []

class Action:

    def __init__(self, kind, **parameters):
        self.kind = kind
        self.parameters = parameters

class UnitType:

    def __init__(self):
        self.vision = 0
        self.armor = 0
        self.life = 0
        self.range = 0
        self.dommage = 0
        self.name = ''
        self.shield = 0
        self.regen = 0
        self.reshield = 0
        self.reload = 0
        self.weapon_kind = 0
        self.movable = False
        self.speed = 0
        self.orders = []
        self.builder = False
        self.constructor = False
        self.shadow = False
