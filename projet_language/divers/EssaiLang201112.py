class Boolean:
    def __init__(self, value):
        self.value = value
    def _and(self, p):
        if p.__class__ != Boolean: raise Exception("PARAMETER TYPE ERROR: %s" % (p.__class__,))
        return Boolean(self.value and p.value)
    def _or(self, p):
        if p.__class__ != Boolean: raise Exception("PARAMETER TYPE ERROR: %s" % (p.__class__,))
        return Boolean(self.value or p.value)
    def _not(self):
        return Boolean(not self.value)
    def _xor(self):
        if p.__class__ != Boolean: raise Exception("PARAMETER TYPE ERROR: %s" % (p.__class__,))
        return Boolean( (self.value or p.value) and (self.value != p.value) )
    def __str__(self):
        if self.value:
            return 'true'
        else:
            return 'false'

class Numeric:
    def __init__(self, value):
        self.value = value
    def add(self, p):
        if p.__class__ == Numeric:
            return Numeric(self.value + p.value)
        else:
            raise Exception("PARAMETER TYPE ERROR: %s" % (p.__class__,))
    def sub(self, p):
        if p.__class__ == Numeric:
            return Numeric(self.value - p.value)
        else:
            raise Exception("PARAMETER TYPE ERROR: %s" % (p.__class__,))
    def mul(self, p):
        if p.__class__ == Numeric:
            return Numeric(self.value * p.value)
        else:
            raise Exception("PARAMETER TYPE ERROR: %s" % (p.__class__,))
    def div(self, p):
        if p.__class__ == Numeric:
            if p.value == 0: raise Exception("DIV BY ZERO ERROR")
            return Numeric(self.value / p.value)
        else:
            raise Exception("PARAMETER TYPE ERROR: %s" % (p.__class__,))
    def mod(self, p):
        if p.__class__ == Numeric:
            return Numeric(self.value % p.value)
        else:
            raise Exception("PARAMETER TYPE ERROR: %s" % (p.__class__,))
    def pow(self, p):
        if p.__class__ == Numeric:
            return Numeric(self.value ** p.value)
        else:
            raise Exception("PARAMETER TYPE ERROR: %s" % (p.__class__,))
    def abs(self):
        return Numeric(abs(self.value))
    def __str__(self):
        return str(self.value)
    def is_float(self):
        return Boolean(int(self.value) != self.value)
    def is_int(self):
        return Boolean(int(self.value) == self.value)
    def to_s(self):
        return String(str(self.value))
    # bug detected
    def between(self, xmin, xmax):
        return Boolean(self.value >= xmin.value and self.value <= xmax.value)
    def send(self, msg, pars):
        if msg == '+':
            return self.add(pars)
        elif msg == '*':
            return self.mul(pars)
        elif msg == 'between':
            return self.between(*pars)
        elif msg == 'abs':
            return self.abs()

class String:
    def __init__(self, value):
        self.value = value
    def count(self):
        return Numeric(len(self.value))
    def length(self):
        return self.count()
    def size(self):
        return self.count()
    def get(self, index):
        if index >= len(self.value): raise Exception("INDEX OUT OF RANGE: %s" % (index,))
        if index < -len(self.value): raise Exception("INDEX OUT OF RANGE: %s" % (index,))
        return String(self.value[index])
    def __str__(self):
        return self.value

class List:
    def __init__(self, cls=None):
        self.value = []
        self.cls = cls
    def append(self, element):
        if self.cls is not None and self.cls != element.__class__: raise Exception("WRONG TYPE: %s for %s" % (element.__class__, self.cls))
        self.value.append(element)
    def get(self, index):
        if index >= len(self.value): raise Exception("INDEX OUT OF RANGE: %s" % (index,))
        if index < -len(self.value): raise Exception("INDEX OUT OF RANGE: %s" % (index,))
        return self.value[index]
    def count(self):
        return Numeric(len(self.value))
    def length(self):
        return self.count()
    def size(self):
        return self.size()

# un nom, un type, une valeur par defaut
class Triplet:
    def __init__(self, name, typ, default=None):
        self.name = name
        self.typ = typ
        self.default = default

# enregistrement compose de triplet
class Struct:
    def __init__(self, name):
        self.name = name
        self.fields = {}
    def add_field(self, name, typ, default=None):
        self.fields[name] = Triplet(name, typ, default)
        
# une valeur d'un type struct avec des valeurs correspondant aux fields de la Struct
class StructValue:
    def __init__(self, struct):
        self.struct = struct
        self.values = {}
        for k in self.struct.fields:
            self.values[k] = self.struct.fields[k].default
    def set_value(self, name, value):
        if value.__class__ != self.struct.fields[name].typ: raise Exception("WRONG TYPE: %s for %s" % (value.__class__, self.struct.fields[name].typ))
        else: self.values[name] = value
    def get_value(self, name):
        if name in self.values:
            return self.values[name]
        else: raise Exception("ATTRIBUTE ERROR: %s" % (name,))

n1 = Numeric(5)
n2 = Numeric(3)
n3 = n1.add(n2)
print n3
print Numeric(2).add(Numeric(3))
print n3.is_int()
print n3.is_float()

s1 = String("hello")
print s1.get(0)
print s1.get(1)
print s1.get(2)
print s1.get(3)
print s1.get(4)
print s1.get(-1)
print s1.get(-2)
print s1.get(-3)
print s1.get(-4)
print s1.get(-5)

print n3.to_s().size().add(Numeric(9)).to_s()

l1 = List(Numeric)
l1.append(Numeric(5))
l1.append(Numeric(3))
print l1.get(1)

Personne = Struct('Personne')
Personne.add_field('age', Numeric, 0)
Personne.add_field('nom', String)
p1 = StructValue(Personne)
p1.set_value('age', Numeric(25))
print p1.get_value('nom')
print p1.get_value('age')

class Node:
    def __init__(self, typ=None, left=None, right=None, middle=None, par=None):
        self.typ = typ        
        self.left = left
        self.right = right
        self.middle = middle
        self.par = par

# (25 + 17) * 2 = 84
operand1 = Node(typ='value', left=Numeric(25))
operand2 = Node(typ='value', left=Numeric(17))
operationPlus = Node(typ='call', left=operand1, middle='+', right=operand2)
operand3 = Node(typ='value', left=Numeric(2))
operationMul = Node(typ='call', left=operationPlus, middle='*', right=operand3) 

# 25.between(20, 30)
operand = Node(typ='value', left=Numeric(25))
par1 = Node(typ='value', left=Numeric(20))
par2 = Node(typ='value', left=Numeric(30))
parlist = Node(typ='list', left=par1, right=par2, par='par')
operationBetween = Node(typ='call', left=operand, middle='between', right=parlist)

# -33.abs = 33
operand = Node(typ='value', left=Numeric(-33))
operationAbs = Node(typ='call', left=operand, middle='abs')

class Interpreter:
    def __init__(self):
        pass
    def execute(self, node):
        if node.typ == 'value':
            return node.left
        elif node.typ == 'call':
            if node.right is not None:
                return self.execute(node.left).send(node.middle, self.execute(node.right))
            else:
                return self.execute(node.left).send(node.middle, None)
        elif node.typ == 'list':
            return [self.execute(node.left), self.execute(node.right)]

i = Interpreter()
print i.execute(operationMul)
print i.execute(operationBetween)
print i.execute(operationAbs)

