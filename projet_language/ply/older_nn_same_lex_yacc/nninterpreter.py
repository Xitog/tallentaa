import lex 
import yacc 
from nnlexer import * 
from nnparser import * 
from nnbaselib import * 
 
shell = True 
debug = True 
 
def cmd_exit(): 
    pass 
 
def unit(s, result, root={}): 
    if s[len(s)-1] != "\n": 
        s += "\n" 
    r = compute_string(s, root) 
    if r == result and r.__class__ == result.__class__: 
        print "Test OK %s >> %s" % (s.rstrip("\n"),r) 
    else: 
        print "Test ERR %s >> %s instead of %s" % (s.rstrip("\n"), r, result) 
    return r == result and r.__class__ == result.__class__ 
 
commands = { 'exit' : cmd_exit} 
 
Root = {} 
 
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
            return base_eval(ast, scope) 
 
def explore(ast): 
    print ast 
 
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
    ('a = 3', 3), 
    ('a+=0', 3), 
    ('a*=2', 6), 
    ('a/=2', 3), 
    ('a%=2', 1), 
) 
 
cpt = 0 
for t in test_suite: 
    r = unit(t[0], t[1], test_root) 
    if r: cpt+=1 
print "Test OK : %d / %d = %f" % (cpt, len(test_suite), cpt/len(test_suite)*100.0) 
 
if __name__ == '__main__': 
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
                result = compute_string(s, Root) 
                Root['_'] = result 
                #Root.vars['_'] = result 
                print result 
    else: 
        files = ('essai.pypo',) 
        String = read(files[0]) 
        compute_string(String) 
        dump() 
 