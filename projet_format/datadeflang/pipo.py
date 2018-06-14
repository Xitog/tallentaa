definition = """
class Position
    attr x : real
    attr y : real
    attr w : int   -- width
    attr h : int   -- height
end"""


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
        if type(elem) == Class:
            s = 'typedef struct {\n'
            for _, attr in elem.attributes.items():
                s += self.generate(attr)
            s += '} ' + elem.name + ';\n'
        elif type(elem) == Attribute:
            kind = self.types[elem.kind]
            s = '    ' + kind + ' ' + elem.name + ';\n'
        else:
            raise Exception(str(type(elem)) + ' ' + str(elem))
        return s


cls = None
lines = definition.split('\n')
for line in lines:
    line = line.split('--')[0].strip()
    elements = line.split(' ')
    if elements[0] == 'class':
        if len(elements) != 2:
            raise Exception('Syntax is : class <CLASSNAME>')
        cls = Class(elements[1])
    elif elements[0] == 'attr':
        if len(elements) != 4:
            raise Exception('Syntax is : attr <ATTRNAME> : <ATTRTYPE>')
        cls.attributes[elements[1]] = Attribute(elements[1], elements[3])

print(repr(cls))

genc = C_Generator({'int': 'int', 'real': 'double'})
s = genc.generate(cls)
print(s)
