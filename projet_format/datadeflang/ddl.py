definition = """
class Position
    attr x : real
    attr y : real
    attr w : int   -- width
    attr h : int   -- height
    map : Map
end

class Map
    name : str
    width : int
    height : int
end

class Unit
    pos : Position
    player : Player
end

class Player
    units : Unit -- should be a list
end

class Game {
    players : Player -- should be a list
}

"""


class Model:

    def __init__(self, name):
        self.name = name
        self.classes = {}

    def __repr__(self):
        s = 'model ' + self.name + '\n\n'
        for _, cls in self.classes.items():
            s += repr(cls) + '\n'
        s += 'end\n'
        return s


class Class:
    
    def __init__(self, name):
        self.name = name
        self.attributes = {}

    def __repr__(self):
        s = 'class ' + self.name + '\n'
        for _, attr in self.attributes.items():
            s += '    ' + repr(attr) + '\n'
        s += 'end\n'
        return s


class Attribute:
    
    def __init__(self, name, kind):
        self.name = name
        self.kind = kind

    def __repr__(self):
        return 'attr ' + self.name + ' : ' + self.kind


class Generator:

    def __init__(self):
        pass


class C_Generator(Generator):

    def __init__(self, mapping):
        self.types = mapping

    def generate(self, elem):
        s = None
        if type(elem) == Model:
            c_name = elem.name.upper() + '_H'
            s = '#IFNDEF ' + c_name + '\n'
            s += '#DEFINE ' + c_name + '\n\n'
            for _, cls in elem.classes.items():
                s += self.generate(cls) + '\n'
            s += '#ENDIF'
        elif type(elem) == Class:
            s = 'typedef struct {\n'
            for _, attr in elem.attributes.items():
                s += self.generate(attr)
            s += '} ' + elem.name + ';\n'
        elif type(elem) == Attribute:
            if elem.kind in self.types:
                kind = self.types[elem.kind]
            else:
                kind = elem.kind
            s = '    ' + kind + ' ' + elem.name + ';\n'
        else:
            raise Exception(str(type(elem)) + ' ' + str(elem))
        return s


model = Model('RTS')
current_cls = None
lines = definition.split('\n')
nb_line = 0
for line in lines:
    nb_line += 1
    line = line.split('--')[0].strip()
    elements = line.split(' ')
    if elements[0] == 'class':
        if len(elements) != 2:
            if len(elements) != 3 or elements[2] != '{':
                print('[ERROR]', nb_line, ':', line)
                raise Exception('Syntax is : class <CLASSNAME>')
        current_cls = Class(elements[1])
        model.classes[current_cls.name] = current_cls
    elif elements[0] == 'attr':
        if len(elements) != 4:
            print('[ERROR]', nb_line, ':', line)
            raise Exception('Syntax is : attr <ATTRNAME> : <ATTRTYPE>')
        current_cls.attributes[elements[1]] = Attribute(elements[1], elements[3])
    elif elements[0] in ('end', '}'):
        current_cls = None
    elif elements[0] in '{':
        continue
    elif len(elements) == 1 and elements[0] == '': # empty lines
        continue
    else:
        if len(elements) != 3:
            print('[ERROR]', nb_line, ':', line)
            raise Exception('Syntax is : <ATTRNAME> : <ATTRTYPE>')
        current_cls.attributes[elements[0]] = Attribute(elements[0], elements[2])

print(repr(model))

genc = C_Generator({'int': 'int', 'real': 'double', 'str' : 'char *'})
s = genc.generate(model)
print(s)
