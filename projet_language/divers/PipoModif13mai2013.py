
def err2tex(error):
    return error.get('message').value

def make_error(value):
    e = Compound('Core.Error')
    e.set('message', Value('Core.String', value))
    return e

class Value(object):
    def __init__(self, kind='Core.Nihil', value='Core.nil'):
        self.kind = kind
        self.value = value

class Compound(Value):
    def __init__(self, kind):
        Value.__init__(self, kind, {})
    
    def set(self, name, value):
        self.value[name] = value
    
    def get(self, name):
        if name in self.value:
            return self.value[name]
        else:
            return make_error('AttributeError: ' + self.kind + ' object has no attribute ' + name)

a = Compound('Person')
a.set('Age', Value('Core.Integer', 25))

#clsPerson = Compound('Person')

#clsClass = Compound('Class')
#clsClass.set('instance_fields', Compound
 
#clsObject = Compound('Object')
#clsObject.set('class', 

class Emulation(object):
    def __init__(self):
        self.fields = {}
    def set(self, name, value):
        self.fields[name] = value
    def get(self, name):
        if name in self.fields:
            return self.fields[name]
        else:
            e = Emulation()
            e.set('message', 'AttributeError: ' + self.kind + ' object has no attribute ' + name)
            return e

class Native(object):
    def __init__(self, kind, value):
        Emulation.__init__(self)
        self.kind = kind
        self.value = value

bob = Emulation()
bob.set('age', Native('int', 25))
bob.set('name', Native('str', 'Bob Gore'))

i = Native('int', 3)

print('I am ' + bob.get('name').value + ' and I have ' + str(bob.get('age').value) + ' years')

nil = Native('nihil', 'nil')

Class = Emulation()
Class.set('class', Class) # loop

Person = Emulation()
Person.set('instance_fields', Native('dict', {}))
Person.get('instance_fields').value['age'] = 'int'
Person.get('instance_fields').value['name'] = 'string'
Person.set('class', Class)

def new(cls):
    obj = Emulation()
    obj.set('class', cls)
    for k in cls.get('instance_fields').value:
        obj.set(k, nil)
    return obj

Bob = new(Person)

print('I am ' + Bob.get('name').value)

Integer = Emulation()
Integer.set('class', Class)
Integer.set('instance_fields', Native('dict', {}))
Integer.get('instance_fields').value['add'] = 'int'

# Idee du 12 mai
# Et si seulement les methodes etaient publiques ?
# tous les datas seraient privees ?
# Et pas de nil !!!

class Param:
    def __init__(self, _name, _type, _default=None, _hasDefault=False):
        self._name = _name
        self._type = _type
        self._default = _default
        self._hasDefault = _hasDefault
        
class Function:
    def __init__(self, _name, _type, _code, _args={}):
        self._name = _name
        self._args = _args
        self._type = _type
        self._code = _code
    
    def call(self, *args):
        print(self._name + ' has been called with : ')
        for k in args: #self._args:
            print('\t' + str(k)) #print(k + ':' + self._args[k]._type + ' = ' + args[k])
        print('\tCode = ' + self._code)

class Class:
    def __init__(self, _name, _super = None):
        self._name = _name
        self._super = _super
        self._methods = {}
        self._class_methods = {}
        self._class_attr = {}

    def new(self, *args):
        o = Object(self)
        if 'init' in self._methods:
            self._methods['init'].call(*args)
        return o

class Object:
    def __init__(self, _class):
        self._class = _class
    def call(self, name, *args):
        self._class._methods[name].call(*args)

init   = Function('init', 'void', '@name = name ; @age = age', {'name':Param('name', 'string'), 'age':Param('age', 'int')})
setAge = Function('age=', 'int', '@age = age', {'age':Param('age', 'int')})
getAge = Function('age', 'string', 'return @age')

Person = Class('Person')
Person._methods['init'] = init
Person._methods['age='] = setAge
Person._methods['age'] = getAge

Bob = Person.new('Bob', 25)
Bob.call('age=', 30)

# http://docs.python.org/2/glossary.html#term-parameter
