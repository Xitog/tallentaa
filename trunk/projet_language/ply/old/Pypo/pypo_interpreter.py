import lex
import yacc
from pypo_lexer import *
from pypo_parser import *

# 001 IF CONDITION MUST BE A BOOLEAN
# 002 VARIABLE DOESN'T EXIST

#k ID affectation_operator expression
#k expression binary_operator expression
#k unary_operator expression
#k expression (bool, string, float, int, id)
#k ( expressiion )
#t if condition then statements else statements end   # 15hxx OK
#t print( expression ) # 16h03 a present il va falloir faire une pile !11 Juillet
#k while condition do statements end 16h34 Le 13 Juillet
#t break
#t continue

from_disk = True

def error(error_code, error_msg):
    print("%d : %s" % (error_code, error_msg))
    exit()

import sys

def compute_file(fn, debug=False):
    f = file(fn)
    s = f.read()
    compute_string(s, debug)

def compute_string(s, debug=False):
    lex.input(s)
    
    if debug:
        while 1:
            tok = lex.token()
            if not tok: break
            if tok.type != 'NEWLINE':
                print "line %d:%s(%s)"%(tok.lineno, tok.type, tok.value)
            else:
                print("line %d:%s(\\n)"%(tok.lineno, tok.type))
    
    result = yacc.parse(s) #, debug=2)
    print result.__class__
    print(explore(result,0))
    print("------------------ End Explore ------------------")
    r = compute(result)
    print("\nResult = %s of type %s" % (r, r.__class__))
    print("\nListing vars")
    for k in vars:
        print("%s:%s:%s" % (k, vars[k].__class__, vars[k]))
    return r

#print("s last: %s" % (s[len(s)-1],))
#s += "\n"

def prod(level):
    s = ''
    for i in range(0,level):
        s+='\t'
    return s

def explore(n, level):
    if n is None:
        print "n is None"
    #print n.__class__
    #print n
    #print "n.code %s" % (n.code,)
    #print "n.parameters %s" % (n.parameters,)
    
    if level != -1:
        fs = prod(level)+n.code
    else:
        print(">>> %s" % (n,))
        fs = n.code
    if n.value is not None:
        #print "afjj"
        fs += "{%s}" % n.value
    if n.param is not None:
        #print "kjccbb"
        fs += "[" + explore(n.param,-1) + "]"
    if n.sbg is not None:
        #print "kfjfkjk'"
        fs += "\n"
        fs += explore(n.sbg, level+1)
    if n.sbd is not None:
        #print "bdjfdjfhj"
        fs += "\n"
        fs += explore(n.sbd, level+1)
    return fs

class Variable(object):
    def __init__(name, sta_type, value):
        self.name = name
        self.sta_type = sta_type
        self.value = value

vars = {}
def compute(n):
    if n.code == '=':
        vars[n.param.value] = compute(n.sbg)
        return vars[n.param.value]
    elif n.code == '+=':
        vars[n.param.value] += compute(n.sbg)
    elif n.code == '-=':
        vars[n.param.value] -= compute(n.sbg)
    elif n.code == '*=':
        vars[n.param.value] *= compute(n.sbg)
    elif n.code == '/=':
        vars[n.param.value] /= compute(n.sbg)
    elif n.code == '//=':
        vars[n.param.value] //= compute(n.sbg)
    elif n.code == '%=':
        vars[n.param.value] %= compute(n.sbg)
        return vars[n.param.value]
    elif n.code == 'IF':
        r = compute(n.param)
        if r.__class__ != bool:
            error(1, 'IF CONDITION MUST BE A BOOLEAN')
        if r:
        #if compute(n.param):
            return compute(n.sbg)
        elif n.sbd is not None:
            return compute(n.sbd)
        else:
            return None
    elif n.code == 'WHILE':
        while compute(n.param):
        	compute(n.sbg)
    elif n.code == '+':
        return compute(n.sbg) + compute(n.sbd)
    elif n.code == '-':
        if n.sbd is not None:
            return compute(n.sbg) - compute(n.sbd)
        else:
            return -compute(n.sbg)
    elif n.code == '/':
        return compute(n.sbg) / compute(n.sbd)
    elif n.code == '*':
        return compute(n.sbg) * compute(n.sbd)
    elif n.code == '%':
        return compute(n.sbg) % compute(n.sbd)
    elif n.code == '**':
        return compute(n.sbg) ** compute(n.sbd)
    elif n.code == '//':
        return compute(n.sbg) // compute(n.sbd)
    elif n.code in ('INT', 'FLOAT', 'BOOL', 'STRING'):
        return n.value
    elif n.code == 'and':
        return compute(n.sbg) and compute(n.sbd)
    elif n.code == 'or':
        return compute(n.sbg) or compute(n.sbd)
    elif n.code == 'not':
        return not compute(n.sbg)
    elif n.code == '==':
        return compute(n.sbg) == compute(n.sbd)
    elif n.code == '!=':
        return compute(n.sbg) != compute(n.sbd)
    elif n.code == '>':
    	return compute(n.sbg) > compute(n.sbd)
    elif n.code == '>=':
    	return compute(n.sbg) >= compute(n.sbd)
    elif n.code == '<':
    	return compute(n.sbg) < compute(n.sbd)
    elif n.code == '<=':
    	return compute(n.sbg) <= compute(n.sbd)
    elif n.code == 'ID':
        if not n.value in vars:
            error(2, "VARIABLE DOESN'T EXIST")
        return vars[n.value]
    elif n.code == 'FUNCALL':
        if n.param.value == 'print':
            print(compute(n.sbg))
    elif n.code == 'PARAMS':
        return compute(n.sbg) # IL VA FALLOIR UNE PILE POUR EMPILER LES RES DES COMPUTESs
    elif n.code == 'PROGRAM':
        if n.sbd is not None:
            compute(n.sbg)
            return compute(n.sbd)
        elif n.sbg is not None:
            return compute(n.sbg)
        else:
            return None
    else:
        raise Exception("CODE UNKNOWN")

if __name__ == '__main__':
    if not from_disk:
        s = raw_input('>>> ')
        compute_string(s, True)
    else:
        files = ('tests/pypo_essai.txt', 
                 'tests/pypo_essai_error.txt')
        #compute_file(files[1], True)
    print "TEST"
    tests = (("a = 3"    , 3), 
             ('b = "abc"', 'abc')
            )
    for test in tests:
        if compute_string(test[0]) == test[1]:
            print("OK")
        else:
            print("NO")
