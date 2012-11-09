# Advanced BIB

def missing(*par):
    raise Exception('AttributeError')

class XObject:
    def __init__(self, xclass=None):
        self.core = {}
        self.core['class'] = xclass
        self.core['missing'] = XFunction(missing)
    def set(self, name, value):
        self.core[name] = value
    def send(self, msg, *par):
        if msg in self.core:
            if self.core[msg].__class__ == XFunction:
                return self.core[msg].do(self, *par)
            else:
                return self.core[msg]
        else:
            return self.core['missing'].do(self, *par)

class XClass(XObject):
    def __init__(self, xsuper=None):
        XObject.__init__(self, None)
        self.instance = {}
        self.xsuper = xsuper
    def set_instance(self, name, value):
        self.instance[name] = value
    def new(self):
        xo = XObject(self)
        if super is not None:
            self.inherit(xo)
        xo.core.update(self.instance)
        return xo
    def inherit(self, obj):
        if self.xsuper is not None:
            self.xsuper.inherit(obj)
        obj.core.update(self.instance)

class XFunction:
    def __init__(self, code):
        self.code = code
    def do(self, Xself, *par):
        return self.code(Xself, *par)

def test(self, a, b):
    print a+b

# class root
r = XClass()
r.set('name', 'Class')
r.set('class', r) # THIS IS THE KEY. Class.class => pointe sur elle-meme

def cls_type(self):
    return self.core['class']
r.set_instance('type', XFunction(cls_type))
r.set('type', XFunction(cls_type))

# class
#xc = XClass(r)
#xc.set('name', 'Personne')

# object & attribute
#xo = XObject(xc)
#xo.set('age', 25)
#print xo.send('age')

# object & class
#print xo.send('class').send('name')
#print xo.send('class').send('class').send('name')
#print xo.send('class').send('class').send('class').send('name')

# unbound fun
#xf = XFunction(test)
#xf.do(None, 2,3)

# bound fun
#xo.set('add', xf)
#xo.send('add', 2, 3)

# method not found
# xo.send('blob')


#-----------------------------------------------------------------------
# Integer
#-----------------------------------------------------------------------

def make_int(v):
  i = Integer.new()
  i.set('value', v)
  return i

def int_abs(self):
    return make_int(abs(self.send('value')))
def int_add(self, p):
    return make_int(self.send('value') + p.send('value'))
def int_sub(self, p):
    return make_int(self.send('value') - p.send('value'))
def int_mul(self, p):
    return make_int(self.send('value') * p.send('value'))
def int_div(self, p):
    return make_int(self.send('value') / p.send('value'))
def int_neg(self):
    return make_int(-self.send('value'))

Integer = XClass(r)
Integer.set('name', 'Integer')
Integer.set('class', r)
Integer.set('type', XFunction(cls_type))
Integer.set_instance('value', 0)
Integer.set_instance('abs', XFunction(int_abs))
Integer.set_instance('add', XFunction(int_add))
Integer.set_instance('sub', XFunction(int_sub))
Integer.set_instance('mul', XFunction(int_mul))
Integer.set_instance('div', XFunction(int_div))
Integer.set_instance('neg', XFunction(int_neg))

#i = Integer.new()
#i.set('value', -5)
#print i.send('abs')
#j = make_int(3)
#print j.send('add', i)

#k = Integer.new()
#print k.send('type').send('name')
#print k.send('type').send('type').send('name')
#print k.send('type').send('type').send('type').send('name')

