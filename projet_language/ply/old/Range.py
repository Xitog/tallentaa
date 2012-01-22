from Object import *

import random

def itr_init(self, rng):
    self['range'] = rng
    self['index'] = rng['start']

def itr_next(self):
    if self['index'] > self['range']['end']:
        return None
    self['index'] = int_add(self['index'], 1)

def itr_has_next(self):
    return self['index'] != self['range']['end']

def itr_to_s(self):
    return "Iterator(%s)" % (int_to_s(self['index']),)

ins_itr = {'to_s' : itr_to_s, 'init' : itr_init, 'next?' : itr_has_next, 'next': itr_next }
cls_itr = cls.copy()
cls_itr.update ( { 'name' : 'Iterator', 'super' : 'Object', 'instance_members' : ins_itr } )

#
#
#

def rng_init(self, start, end):
    self['start'] = start
    self['end'] = end

def rng_to_s(self):
    return "Range(%s,%s)" % (int_to_s(self['start']), int_to_s(self['end']))

def rng_random(self):
    return random.randint(self['start']['native'], self['end']['native'])

def rng_iterate(self):
    return make_new(cls_iterator, self)

ins_rng = {'to_s' : rng_to_s, 'init' : rng_init, 'random' : rng_random, 'iterate' : rng_iterate }
cls_rng = cls.copy()
cls_rng.update ( { 'name' : 'Range', 'super' : 'Object', 'instance_members' : ins_rng } )

import datetime
class PLP_DATE(object):
    
    def __init__(self, x, y):
        self.code = datetime.today()

class PLP_RANGE(object):
    
    def __init__(self, x, y):
        self.core = xrange(x, y)
    
    def random(self):
        return random.randint(self.core[0], self.core[len(self.core)-1]+1)

    def __repr__(self):
        return "Range(%d,%d)" % (self.core[0], self.core[len(self.core)-1]+1)
