from Object import *

import math

def int_init(self, value):
    if value.__class__ == list:
        self['native'] = value[0]
    else:
        self['native'] = value

def int_to_s(self):
    return str(self['native'])

def int_sin(self):
    return math.sin(self['native'])

def int_add(self, value):
    return make_new(cls_int, self['native'] + value[0])

def int_min(self, value):
    return make_new(cls_int, self['native'] - value[0])

def int_intdiv(self, value):
    return make_new(cls_int, self['native'] / int(value[0]))

ins_int = {'sin' : int_sin, 'to_s' : int_to_s, 'init' : int_init, 'add' : int_add }
cls_int = cls.copy()
cls_int.update ( { 'name' : 'Integer', 'super' : 'Object', 'instance_members' : ins_int } )
