from __future__ import division

import sys    # getsizeof, stdout.write
import math   # factorial

# Il faut un meilleur systeme que ajouter a la main pour chaque fonction
# les tests du nb de parametre et l'affichage dans functions !
# De plus functions retourne une liste, ce qui n'est pas gerer !

class BaseLib:
    
    def send(self, target, msg, par, scope):
        if target is None:
            if msg in ['println', 'writeln']:
                print par
                return None
            elif msg in ['print', 'write']:
                sys.stdout.write(str(par))
                return None
            elif msg == 'read':
                return raw_input(par)
            else:
                raise Exception("Global function not known: %s" % (msg,))
        else:
            if isinstance(target, int) and not isinstance(target, bool):
                return self.send_int(target, msg, par, scope)
            elif isinstance(target, float):
                return self.send_flt(target, msg, par, scope)
            elif isinstance(target, bool):
                return self.send_boo(target, msg, par, scope)
            elif isinstance(target, str): 
                return self.send_str(target, msg, par, scope)
    
    def send_object(self, target, msg, par, scope):
        # check
        if msg in ['type', 'class']:
            if len(par) != 0: raise Exception('%s function take 0 parameter, %d given' % (msg, len(par)))
        # do
        if msg == 'type' or msg == 'class':
            return target.__class__
    
    def send_int(self, target, msg, par, scope):
        # common
        if msg in ['type', 'class']:
            return self.send_object(target, msg, par, scope)
        # check
        if msg in ['add', 'sub', 'div', 'mul', 'pow', 'mod', 'lshift', 'rshift', 'and', 'or', 'xor','cmp', 'intdiv']:
            if len(par) != 1: raise Exception('%s function take 1 parameter, %d given' % (msg, len(par)))
        elif msg in ['abs', 'inv', 'invbin', 'to_s', 'to_f', 'to_i', 'size', 'factorial', 'functions']:
            if len(par) != 0: raise Exception('%s function take 0 parameter, %d given' % (msg, len(par)))
        elif msg in ['between?']:
            if len(par) != 2: raise Exception('%s function take 2 parameters, %d given' % (msg, len(par)))
        # do
        if msg == 'add':
            return target + par[0]
        elif msg == 'sub':
            return target - par[0]
        elif msg == 'div':
            return target / par[0]
        elif msg == 'intdiv':
            return target // par[0]
        elif msg == 'mul':
            return target * par[0]
        elif msg == 'pow':
            return target ** par[0]
        elif msg == 'mod':
            return target % par[0]
        elif msg == 'abs':
            return abs(target)
        elif msg == 'inv':
            return -target
        elif msg == 'lshift':
            return target << par[0]
        elif msg == 'rshift':
            return target >> par[0]
        elif msg == 'and':
            return target & par[0]
        elif msg == 'or':
            return target | par[0]
        elif msg == 'xor':
            return target ^ par[0]
        elif msg == 'invbin':
            return ~target
        elif msg == 'cmp':
            if target > par[0]: return 1
            elif target < par[0]: return -1
            else: return 0
        elif msg == 'to_s':
            return str(target)
        elif msg == 'to_f':
            return float(target)
        elif msg == 'to_i':
            return target
        elif msg == 'size':
            return sys.getsizeof(target)
        elif msg == 'between?':
            return target >= par[1] and target <= par[0]
        elif msg == 'factorial':
            return math.factorial(target)
        elif msg == 'functions':
            r = ['type', 'class', 'add', 'sub', 'div', 'intdiv', 'mul', 'pow', 'mod', 'abs', 'inv', 'lshift', 'rshift', 'and', 'or', 'xor', 'invbin', 'cmp', 'to_s', 'to_f', 'to_i', 'size', 'between?', 'factorial', 'functions' ]
            r.sort()
            return r 
        else:
            raise Exception("Function %s not known for integer" % (msg,))
    
    def send_flt(self, target, msg, par, scope):
        # common
        if msg in ['type', 'class']:
            return self.send_object(target, msg, par, scope)
        # check
        if msg in ['add', 'sub', 'div', 'mul', 'pow', 'mod']:
            if len(par) != 1: raise Exception('%s function take 1 parameter, %d given' % (msg, len(par)))
        elif msg in ['abs', 'inv', 'round', 'trunc', 'floor', 'to_i', 'ceil']:
            if len(par) != 0: raise Exception('%s function take 0 parameter, %d given' % (msg, len(par)))
        # do
        if msg == 'add':
            return target + par[0]
        elif msg == 'sub':
            return target - par[0]
        elif msg == 'div':
            return target / par[0]
        elif msg == 'mul':
            return target * par[0]
        elif msg == 'pow':
            return target ** par[0]
        elif msg == 'mod':
            return target % par[0]
        elif msg == 'abs':
            return abs(target)
        elif msg == 'inv':
            return -target
        elif msg == 'round':
            return int(round(target))
        elif msg == 'trunc' or msg == 'floor' or 'to_i':
            return int(target)
        elif msg == 'ceil':
            return int(target)+1
        else:
            raise Exception("Function %s not known for float" % (msg,))

    def send_str(self, target, msg, par, scope):
        # common
        if msg in ['type', 'class']:
            return self.send_object(target, msg, par, scope)
    
    def send_boo(self, target, msg, par, scope):
        # common
        if msg in ['type', 'class']:
            return self.send_object(target, msg, par, scope)
        # check
        if msg in ['and', 'or', 'xor', 'inv', 'to_i']:
            if len(par) != 1: raise Exception('%s function take 1 parameter, %d given' % (msg, len(par)))
        # do
        if msg == 'and':
            return target and par[0]
        elif msg == 'or':
            return target or par[0]
        elif msg == 'xor':
            return (target or par[0]) and not (target and par[0])
        elif msg == 'inv':
            return target == False
        elif msg == 'to_i':
            if target: return 1
            else: return 0
