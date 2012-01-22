import sys
sys.dont_write_bytecode = True

import lex 
import yacc 
from nnlexer import * 
from nnparser import * 
from nnbaselib import * 
 
shell = True
debug = True 
config(False)
 
def cmd_exit(): 
    print('Goodbye.') 

def cmd_vars():
    pass

def unit(s, result, root=Scope()): 
    if s[len(s)-1] != "\n": 
        s += "\n" 
    r = compute_string(s, root)
    if r.__class__ == Ref:
        r = r.get()
    if r == result and r.__class__ == result.__class__: 
        print "Test OK %s >> %s" % (s.rstrip("\n"),r) 
    else: 
        print "Test ERR %s >> %s(%s) instead of %s(%s)" % (s.rstrip("\n"), r, r.__class__, result, result.__class__) 
    return r == result and r.__class__ == result.__class__ 
 
commands = { 'exit' : cmd_exit} 

Root = Kernel

import sys 
 
def mwrite(*liste): 
    for i in liste: 
        sys.stdout.write(str(i)) 
 
def disp(s): 
    mwrite('[',s, '] l->', len(s), "\n") 
    for t in get_tokens(s): 
        print(t) 
 
def get_tokens(string): 
    tokens = lex.input(string) 
    l = [] 
    while 1: 
        token = lex.token() 
        if not token: break 
        l.append(token) 
    return l 
 
def get_ast(string): 
    ast = yacc.parse(string) 
    return ast 
 
def compute_string(string, scope): 
    global debug 
    ast = get_ast(string) 
    if ast is None: 
        print 'ERROR : Ast could not be generated.' 
    else: 
        if debug: 
            print('Ast built') 
            print('Exploring') 
            explore(ast)
            print
            print
            return base_eval(ast, scope)

def make_space(nb):
    s = ""
    for i in range(0, nb):
        s += " "
    return s

def explore(ast, space=0, nb=""):
    if ast.__class__ != Node:
        print nb, make_space(space), "PB we have a ", ast.__class__, ' with value ', ast
        #raise Exception("Wrong type! %s" % repr(ast.__class__))
    
    if space == 0:
        print "=== Printing AST ==="
        print
        print "Harsh view :", ast
        print
    
    if ast.par.__class__ == Node:
        print nb, make_space(space), "Type =", ast.typ
        print nb, make_space(space), "With Par ="
        explore(ast.par, space+2, nb)
        print nb, make_space(space), "End Par."
    elif ast.typ == 'list':
        if ast.par == 'dict':
            print nb, make_space(space), "Dict %s" % (ast.sbg,)
        elif ast.par == 'id':
            print nb, make_space(space), "List of id:"
            for elem in (ast.sbg):
                print nb, make_space(space), elem
        else:
            print nb, make_space(space), "List"
            i = 0
            for statement in ast.sbg:
                explore(statement, space+2, nb+str(i+1)+". ")
                i += 1
    elif ast.par is not None:
        print nb, make_space(space), "Type =", ast.typ
        print nb, make_space(space), "Par =", ast.par
    else:
        print nb, make_space(space), "Type =", ast.typ
        print nb, make_space(space), "No Par."
    
    if ast.sbg.__class__ == Node:
        print nb, make_space(space), "Left :"
        explore(ast.sbg, space+2, nb)
    elif ast.sbg is None:
        print nb, make_space(space), "Left is None"
    else:
        print nb, make_space(space), "Left Raw Content:", ast.sbg, ast.sbg.__class__
    if ast.sbd.__class__ == Node:
        print nb, make_space(space), "Right :"
        explore(ast.sbd, space+2, nb)
    elif ast.sbd is None:
        print nb, make_space(space), "Right is None"
    else:
        print nb, make_space(space), "Right Raw Content :", ast.sbd, ast.sbd.__class__
    
    if space == 0:
        print "=== End display ==="
 
def good(s): 
    if_level = 0 
    last = '' 
    for t in get_tokens(s): 
        if t.type == 'IF': 
            if_level += 1 
            last = 'IF' 
        elif t.type == 'END': 
            if last == 'IF': 
                if_level -= 1 
    return if_level 
 
test_root = {} 
test_suite = ( 
    ('2+3', 5), 
    ('2', 2), 
    ('(2+2)*3', 12), 
    ('3*(2+2)', 12), 
    ('3*2+2', 8), 
    ('(3+2)*(2*2)', 20), 
    ('(3)', 3), 
    # Float 
    ('(3.0)', 3.0), 
    ('5/2', 2), 
    ('5/2.0', 2.5), 
    ('5.0/2', 2.5), 
    ('5.0//2.0', 2), 
    ('5%2', 1), 
    ('5%2*3', 3), 
    ('5*3%2', 5), 
    ('b=4', 4),
    ('a = 3', 3), 
    ('a+=0', 3), 
    ('a*=2', 6), 
    ('a/=2', 3), 
    ('a%=2', 1),
    ('a-=1', 0),
    ('b', 4),
    # Boolean
    ('a = true', True),
    ('true == true', True),
    ('true == false', False),
    ('false == false', True),
    ('not true', False),
    ('not false', True),
    ('a', True),
    ('not a', False),
    ('true and true', True),
    ('true and false', False),
    ('false and true', False),
    ('false or true', True),
    ('true or false', True),
    ('true and true and false', False),
    ('false or false or true', True),
    ('false and false or true', True),
    ('false and (false or true)', False),
    # Selection (if)
    ('if true then 3 end', 3),
    ('if false then 3 else 5 end', 5),
    ('if a then 42 end', 42),
    ('if not a then 22 else 42 end', 42)
)

ESCAPE_TEST = True

if not ESCAPE_TEST:
    raw_input('Press enter to launch tests')
    cpt = 0 
    for t in test_suite:
        print '---------------------------------------------'
        r = unit(t[0], t[1], test_root) 
        if r: cpt+=1 
    print '---------------------------------------------'
    print "Test OK : %d / %d = %d" % (cpt, len(test_suite), float(cpt)/len(test_suite)*100.0) 

ESCAPE_SHELL = False

if __name__ == '__main__' and not ESCAPE_SHELL:
    last_result = Symbol('_')
    
    if shell: 
        s = '' 
        while s != 'exit': 
            String = s 
            s = raw_input('> ') 
            if s in commands: 
                commands[s]() 
            else: 
                s += "\n" 
                if debug: disp(s) 
                while good(s) != 0: 
                    s2 = raw_input('. ')                     
                    s += s2 
                    s += "\n" 
                    if debug: disp(s)
                try: # else: (no exception) finally: (always)
                    result = compute_string(s, Root) 
                except Exception as e:
                    print e
                    result = None
                if isinstance(result, Symbol): # 'forced execution'
                    result = Root.get(result)
                Root.set(last_result, result)
                print result 
    else: 
        files = ('essai.pypo',) 
        String = read(files[0]) 
        compute_string(String) 
        dump() 

ESCAPE_FILE = True

if not ESCAPE_FILE:
    raw_input("Check Parser")

    #f = file('first.plp')
    f = file('second.plp')
    s = f.read()
    compute_string(s, Root)
    print
    print "Fin."
    print
    #dump()

