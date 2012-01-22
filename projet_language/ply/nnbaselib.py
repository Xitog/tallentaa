import sys
import math
import types
import inspect

baselib_debug = False

def fatal(num, message):
    print 
    print '>>> Something went wrong, sorry :-('
    print '>>>', '['+str(num)+']', message
    print '>>> End of Session'
    raise Exception("Z")
    exit(num)

from Range import *

# V002
def cls(a):
    return a.__class__

class Symbol:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return ":"+self.name

class Scope:
    def __init__(self, father=None):
        self.content = {}
        self.father = father
    
    def set(self, s, value):
        if cls(s) != Symbol:
            raise Exception("Not symbol")
        self.content[s.name] = value

    def get(self, s):
        if cls(s) != Symbol:
            raise Exception("Not symbol")
        if s.name in self.content:
            return self.content[s.name]
        elif self.father is not None:
            r = self.father.get(s)
        else:
            raise Exception("Not known symbol <%s> in <%s>" % (s.name, str(self.content))) # le dernier scope levera l'exception

    def copy(self):
        s = Scope()
        s.content = self.content.copy()
        return s

def is_symbol(obj):
    return obj.__class__ == Symbol

#unused
def is_in(obj, scp):
    return obj in scp.content

def display(obj):
    if obj.__class__ == list:
        for elem in obj:
            sys.stdout.write(str(elem))
    else:
        sys.stdout.write(str(obj))
    print

def get_io(prompt=None):
    return raw_input(prompt)

def end(msg=None):
    exit(msg)

def stoi(lst):
    return int(*lst)

def kernel_dir():
    global Kernel
    return Kernel.content

Kernel = Scope()
Kernel.set(Symbol('println'), display)
Kernel.set(Symbol('print'), sys.stdout.write)
Kernel.set(Symbol('Range'), PLP_RANGE)
Kernel.set(Symbol('ask'), get_io)
Kernel.set(Symbol('exit'), end)
Kernel.set(Symbol('Date'), PLP_DATE)
Kernel.set(Symbol('Time'), PLP_TIME)
Kernel.set(Symbol('int'), int)
Kernel.set(Symbol('object'), object)
Kernel.set(Symbol('dir'), kernel_dir)

# a.i attention cela change le scope courant !!! On passe a scope = a.scope + father (celui qu'on manip now) et symbol i.

def xbase_eval(token, scope):
    r = base_eval(token, scope)
    if baselib_debug: print 'xbase Typ=', token.typ, 'Par=', token.par, 'Sbg=', token.sbg, 'Res=', r, 'CRes=', r.__class__
    return r

imported = {}
current = None

def register(name, fun):
    global current
    current[name] = fun

class Fun(object):
    def __init__(self, fname, formals, ast):
        self.name = fname
        self.ast = ast
        self.formals = formals
    def eval(self, scope, par):
        i = 0
        while i < len(self.formals):
            if not isinstance(par[i], scope.get(Symbol(self.formals[i][1]))):
                fatal("013", "Wrong parameter type")
            scope.set(Symbol(self.formals[i][0]), par[i])
            i+=1
        return base_eval(self.ast, scope)
    def arity(self):
        return len(self.formals)

def base_eval(token, scope): 
    global imported, current
    if token.typ == 'list': 
        if token.par == 'sta': 
            r = None 
            for sta in token.sbg: 
                r = xbase_eval(sta, scope) 
            return r
        elif token.par == 'expr':
            l = []
            for e in token.sbg:
                l.append(xbase_eval(e, scope))
            return l
        elif token.par == 'dict':
            d = {}
            for e in token.sbg:
                d.update({e: xbase_eval(token.sbg[e], scope)})
            return d 
        else: 
            raise Exception('Par list not handled') 
    elif token.typ == 'value': 
        if token.par == 'int': 
            return int(token.sbg) 
        elif token.par == 'flt': 
            return float(token.sbg) 
        elif token.par == 'id':
            return Symbol(token.sbg)
        elif token.par == 'str':
            return token.sbg
        elif token.par == 'bool':
            return token.sbg
        else:
            raise Exception('Value type unknown') 
    elif token.typ == 'affectation': 
        if token.par == '=':
            left = xbase_eval(token.sbg, scope)
            right = xbase_eval(token.sbd, scope)
            if isinstance(right, Symbol):
                right = scope.get(right)
            scope.set(left, right)
            return left
        else:
            var = xbase_eval(token.sbg, scope)
            val = xbase_eval(token.sbd, scope)
            value_linked_to_var = scope.get(var)
            v = base_obj(scope.get(var), token.par.rstrip('='), scope, val)
            scope.set(var, v)
            return var
    elif token.typ == 'binop':
        left = xbase_eval(token.sbg, scope) 
        right = xbase_eval(token.sbd, scope) 
        return base_obj(left, token.par, scope, right)
    elif token.typ == 'unaop':
        left = xbase_eval(token.sbg, scope)
        if is_symbol(left):
            left = scope.get(left)
        if isinstance(left, bool):
            return not left
        elif isinstance(left, int) or isinstance(left, float):
            return -left
        else:
            fatal("00x", "NotImplemented")
    elif token.typ == 'if':
        cond = xbase_eval(token.par, scope)
        r = None        
        if cond:
            r = xbase_eval(token.sbg, scope)
        elif token.sbd is not None:
            r = xbase_eval(token.sbd, scope)
        return r
    elif token.typ == 'while':
        cond = xbase_eval(token.par, scope)
        r = None
        while cond:
            r = xbase_eval(token.sbg, scope)
            cond = xbase_eval(token.par, scope)
        return r
    elif token.typ == 'for':
        print "lst = ", token.par
        print "var = ", token.sbd
        lst = xbase_eval(token.par, scope)
        var = xbase_eval(token.sbd, scope)
        i = 0
        while i < len(lst):
            scope.set(var, lst[i])
            r = xbase_eval(token.sbg, scope)
            i += 1
        return r
    elif token.typ == 'function':
        f = Fun(fname=token.sbd, formals=token.par.sbg, ast=token.sbg)
        scope.set(Symbol(token.sbd), f)
        return f
    elif token.typ == 'require':
        filename = token.par
        import os
        if os.path.exists(filename):
            if os.path.isfile(filename):
                f = file(filename)
                module_name = filename.rstrip('.py')
                # Register module
                imported[module_name] = {}
                current = imported[module_name] # for register
                # On supprime tous les trucs globaux
                # On peut apres donner des locaux
                #exec f.read() in {'__builtins__' : None}, {'core' : imported, 'dir' : dir, 'register' : register, 'module' : module_name}
                exec f.read() in {}, {'core' : imported, 'register' : register, 'module' : module_name}
                #print imported
                #raw_input()
        else:
            fatal(001, 'Required file <%s> not found' % (filename,))
    elif token.typ == 'include':
        name = token.par
        if name in imported:
            dic = imported[name]     # ex : first
            for elem in dic:         # ex : first['hello'] donc hello
                s = Symbol(elem)
                scope.set(s, dic[elem])
    elif token.typ == 'return':
        return xbase_eval(token.par, scope) # ret vide aussi
    else:
        raise Exception('Token Type not handled %s' % (token.typ,)) 

# Translate cmp(x,y) or x.__cmp__(y) result into a boolean
def translate_cmp(r, op):
    if op in ['==', '<=', '>='] and r == 0:
        return True
    elif op in ['!=', '<'] and r == -1:
        return True
    elif op in ['!=', '>'] and r == 1:
        return True
    return False

def resolve_extended(obj, field):
    if field == 'len':
        return obj.__len__()
    elif field == 'contains?':
        return obj.__contains__
    elif field == 'to_i':
        return int(obj)
    elif field == 'sin':
        return math.sin(obj)
    elif field == 'to_s':
        return obj.__str__()
    else:
        exit(field)

def base_obj(rec, op, scope, par):
    
    # Desymbolisation du receveur
    if is_symbol(rec):
        symbol_name = rec
        rec = scope.get(rec)
    else:
        symbol_name = None
    
    # Scope elargit avec rec
    #scope = scope.copy()
    #listing = dir(rec)
    #for elem in listing:
    #    scope.set(Symbol(elem), getattr(rec, elem))
    
    # Mise en forme et desymbolisation des parametres
    correspondance = { '+' : '__add__', '-' : '__sub__', '*' : '__mul__', '/' : '__div__', '**' : '__pow__', '%' : '__mod__', '//' : '__truediv__', '<<' : 'append', 'and' : '__and__', 'or' : '__or__', 'xor' : '__xor__' }
    
    if op == 'call' or op in [ '==', '<=', '>=', '>', '<', '!=' ] or op in correspondance: # CALL
        if hasattr(par, '__iter__'):
            args = []
            for elem in par:
                if is_symbol(elem):
                    args.append(scope.get(elem))
                else:
                    args.append(elem)
        else:
            if is_symbol(par):
                args = [scope.get(par)]
            else:
                args = [par]
    
    # Appel
    if op == 'call':
        if callable(rec):
            if type(rec) == types.TypeType:
                return rec(*args) # Constructor
            else:
                return rec.__call__(*args)
        elif hasattr(rec, '__getitem__'):
            return rec[args[0]]
        elif rec.__class__ == Fun:
            return rec.eval(scope, args)
        else:
            fatal("010", "Object <%s> is not callable" % (rec,))
    elif op in [ '==', '<=', '>=', '>', '<', '!=' ]:
        if hasattr(rec, '__cmp__'):
            r = rec.__cmp__(*args)
            return translate_cmp(r, op)
        else:
            fatal("011", "Object <%s> cannot be compared" % (rec,))
    elif op in correspondance:
        if hasattr(rec, correspondance[op]):
            return getattr(rec, correspondance[op])(*args)
        else:
            fatal("012", "Object <%s> is not arithmetic" % (rec,))
    elif op == '.':
        field = par.name
        if isinstance(rec, dict) and field in rec:
            return rec[field]
        elif field in dir(rec):
            attr = getattr(rec, field)
            if callable(attr):
                return attr.__call__()
            else:
                return attr
        else: #field not found
            return resolve_extended(rec, field)
    else:
        print op
        fatal("011", "Operation <%s> not handled" % (op,))
    
    exit("Rev op=%s cls=%s" % (op,rec.__class__))
