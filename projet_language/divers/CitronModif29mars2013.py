import inspect

INFINITY = -1

class BeamWeapon(object):

    def __init__(self, name, reload, mun):
        self.name = name
        self.reload = reload
        self.mun = mun

w = BeamWeapon("Analyzer", 20, INFINITY)
"""
class XObject:
    def __init__(self, dic):
        self.dic = dic
    def __getitem__(self, key):
        return self.dic[key]
    def __getattr__(self, what):
        if what == '__getitem__':
            return self.__getitem__
        elif what == 'dic':
            return self.dic
        print what
        if what in self.dic:
            if callable(self.dic[what]):
                return self.dic[what]()
            else:
                return self.dic[what]
        else:
            raise Exception("Field unknown %s" % (what,))
    def __setattr__(self, what, value):
        print what, value
        if what in self.dic:
            self.dic[what] = value
        else:
            raise Exception("Field unknown %s" % (what,))
    def __setitem__(self, key, value):
        if key in self.dic:
            self.dic[key] = value
        else:
            raise Exception("Field unknown %s" % (what,))

BWeapon = XObject({
        "instance" : {
            "name" : str,
            "reload": int,
            "mun" : int,
            "hello" : { "return" : str }
        },
        "name" : "BWeapon",
    })

def cls_set(cls, fun):
    fname = fun.func_name[len(cls["name"])+1:]
    #print fname
    if fname in cls["instance"]:
        if inspect.isbuiltin(fun):
            raise Exception("Cannot bind builtin function to live object")
        else:
            args = inspect.getargspec(fun)
            #print args
            cls["instance"][fname] = fun
    else:
        raise Exception("Function not declared in class definition")

def cls_new(cls, **args):
    i = XObject(cls["instance"].copy())
    i["class"] = cls["name"]
    for k in args:
        if isinstance(args[k], i[k]):
            i[k] = args[k]
        else:
            raise Exception("Wrong type : %s for %s, field <%s>" % (type(args[k]), i[k], k))
    return i

def BWeapon_hello(self):
    print "hello %s" % (self.name,)

cls_set(BWeapon, BWeapon_hello)

#ww = BWeapon.copy()
ww = cls_new(BWeapon, name="Analyzer", reload=20, mun=INFINITY)
print ww
"""

class Zembla:

    def __init__(self, dic):
        self.dic = dic
        o = object()
        #self.dic["__str__"] = self.__str__
        for s in dir(object):
            self.dic[s] = getattr(o, s)
        self.dic["new"] = self.new
    
    #def __str__(self):
    #    return str(self.dic)

    def __getattr__(self, what):
        #print what
        if what in self.dic:
            return self.dic[what]

    def __setattr__(self, what, value):
        print what
        print type(self.dic)
        raw_input
        if what in self.dic:
            self.dic[what] = value
    
    def new(self, **args):
        i = Zembla(self.dic["instance"])
        for k in args:
            if isinstance(args[k], self.dic["instance"][k]):
                i.k = args[k]
            else:
                raise Exception("Wrong type : %s for %s, field <%s>" % (type(args[k]), i[k], k))
        return i

z = Zembla({"a" : 5})
print "z =", z
print "z.a =", z.a

# "a" => 5 nouveau Ruby a : 5

BWeapon = Zembla({
        "instance" : {
            "name" : str,
            "reload": int,
            "mun" : int,
            "hello" : { "return" : str }
        },
        "name" : "BWeapon",
    })

ww = BWeapon.new(name="Analyzer", reload=20, mun=INFINITY)
print ww.name
