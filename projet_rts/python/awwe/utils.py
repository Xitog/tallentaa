#------------------------------------------------------------------------------
# NAMEDOBJECT
#------------------------------------------------------------------------------
class NamedObject:
    def __init__(self, name):
        self.name = name
    
    def get_name(self):
        return self.name

#------------------------------------------------------------------------------
# IDOBJECT
#------------------------------------------------------------------------------
class IdObject():
    
    COUNTER_ID = 0
    
    def __init__(self):
        IdObject.COUNTER_ID += 1
        self.id = IdObject.COUNTER_ID

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
