import lex
import yacc
from n_lexer import *
from n_parser import *

import os
import sys # for sys.stdout.write

#-[Globals]--------------------------------------------------------------------

shell = True
skip_files = False
debug = False

#-[Utils]----------------------------------------------------------------------

def get_ast(string):
    ast = yacc.parse(string) #, debug=2)
    return ast

def read(filename):
    f = file(filename)
    s = f.read()
    return s

def get_tokens(String):
    tokens = lex.input(String) # la s ne plantait pas et il prenait la valeur de la main !!! quelle blague !!!
    l = []
    while 1:
        token = lex.token()
        if not token: break
        l.append(token)
    return l

def prod(level):
    s = ''
    for i in range(0,level):
        s+='  '
    return s

#-[Compute]--------------------------------------------------------------------

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
            print('Computing')
        result = compute(ast, scope)
        return result

def explore(n, level=0):
    fs = prod(level)
    if n is None:
        raise Exception('n is None')
    elif n.__class__ == Node:
        if n.typ == 'list':
            if n.par == 'sta':
                print(fs + 'list of statements:')
                for sta in n.sbg:
                    explore(sta, level+1)
            elif n.par == 'id':
                print(fs + 'list of id:')
                for i in n.sbg:
                    print(fs + '.' + i)
            elif n.par == 'expr':
                print(fs + 'list of expression:')
                for sta in n.sbg:
                    explore(sta, level+1)
            else:
                raise Exception('n.par type is unknown: %s for node of type list' % (n.par,))
        elif n.typ == 'if':
            print(fs + 'if')
        elif n.typ == 'unless':
            print(fs + 'unless')
        elif n.typ == 'affectation':
            print(fs + 'affectation')
        elif n.typ == 'while':
            print(fs + 'while')
            print(fs + '--condition')
            explore(n.par, level+1)
            print(fs + '--iteration')
            explore(n.sbg, level+1)
        elif n.typ == 'for':
            print(fs + 'for')
            explore(n.sbg, level+1)
        elif n.typ == 'value':
            print(fs + 'value = %s of registred type %s and in fact type %s' % (n.sbg, n.par, n.sbg.__class__))
        elif n.typ == 'binop':
            print(fs + 'binop [%s]' % (n.par,))
            explore(n.sbg, level+1)
            print(fs + '--[End Left][Start Right]--')
            explore(n.sbd, level+1)
        elif n.typ == 'unaop':
            print(fs + 'unaop')
        elif n.typ == 'function':
            print(fs + 'function')
        elif n.typ == 'class':
            print(fs + 'class')
        elif n.typ == 'module':
            print(fs + 'module')
        elif n.typ == 'return':
            print(fs + 'return')
            if n.par is not None: explore(n.par, level+1)  # node:expr
        elif n.typ == 'require':
            print(fs + 'require')
            print(fs + '-> %s' % (n.par,))     # string
        elif n.typ == 'include':
            print(fs + 'include')
            print(fs + '-> %s' % (n.par,))     # string (id)
        elif n.typ == 'break':
            print(fs + 'break')
        elif n.typ == 'continue':
            print(fs + 'continue')
        else:
            raise Exception('n.typ is unknown: %s' % (n.typ,))
    else:
        raise Exception('n is not a Node but %s (%s)' % (n.__class__,str(n)))

#
# Compute
# Heart of the system. Do not modify without security enabled nor guidance.
# Compute errors:
#   005 In operand is not iterable
#   004 For list is not iterable
#   002 Unless condition must be a boolean
#   001 If condition must be a boolean

# id
# op .
# op () (call op)
# op [] (index op)
# op aff
# fun def
# class def
# module def

# dans pypo v1 je faisais l'assemblage de liste dans l'interpreter. L'arbre etait tres gros !

def compute(n, scope):
    if n is None:
        raise Exception('n is None')
    elif n.__class__ == Node:
        if scope.flux != 'normal': # assure le fct des continue et break!
            return
        elif n.typ == 'list':
            if n.par == 'sta':
                last = None
                for sta in n.sbg:
                    last = compute(sta, scope)
                    print('sta: ' + str(last))
                return last
            elif n.par == 'id':
                for i in n.sbg:
                    print('.id : ' + i)
            elif n.par == 'expr':
                computed = []
                for expr in n.sbg:
                    computed.append(compute(expr, scope))
                return computed
            else:
                raise Exception('n.par type is unknown: %s for node of type list' % (n.par,))
        elif n.typ == 'if':
            #cmd_dump()
            cond = compute(n.par, scope)
            if cond.__class__ != bool:
                raise Exception('001 IF CONDITION MUST BE A BOOLEAN')
            if cond:
                return compute(n.sbg, scope)
            elif n.sbd is not None:
                return compute(n.sbd, scope)
            else:
                return None
        elif n.typ == 'unless':
            cond = compute(n.par, scope)
            if cond.__class__ != bool:
                raise Exception('002 UNLESS CONDITION MUST BE A BOOLEAN : %s' % (cond,))
            if not cond:
                return compute(n.sbg, scope)
            elif n.sbd is not None:
                return compute(n.sbd, scope)
            else:
                return None
        elif n.typ == 'affectation':
            droite = compute(n.sbd, scope)
            if n.par == '=':
                scope.vars[n.sbg] = droite
            elif n.par == '-=':
                scope.vars[n.sbg] -= droite
            elif n.par == '+=':
                scope.vars[n.sbg] += droite
            elif n.par == '*=':
                scope.vars[n.sbg] *= droite
            elif n.par == '/=':
                scope.vars[n.sbg] /= droite
            return scope.vars[n.sbg]
        elif n.typ == 'while':
            while compute(n.par, scope) and scope.flux == 'normal':
                compute(n.sbg, scope)
                if scope.flux == 'continue':
                    scope.flux = 'normal'
            scope.flux = 'normal'
        elif n.typ == 'for':
            scope.vars[n.sbd] = None
            liste = compute(n.par, scope)
            if not isiterable(liste):
                raise Exception("004 For list is not iterable")
            for i in r:
                scope.vars[n.sbd] = i
                compute(n.sbg, scope)
                if scope.flux == 'break': break
                elif scope.flux == 'continue': scope.flux = 'normal'
            scope.flux == 'normal'
            return None
        elif n.typ == 'value':
            if n.par != 'id':
                return n.sbg
            else:
                return scope.vars[n.sbg] # DONT WORK WITH EMBEDDED SCOPE AND '.' ???
        elif n.typ == 'binop':
            if n.par == '+':
                return compute(n.sbg, scope) + compute(n.sbd, scope)
            elif n.par == '-':
                return compute(n.sbg, scope) - compute(n.sbd, scope)
            elif n.par == '*':
                return compute(n.sbg, scope) * compute(n.sbd, scope)
            elif n.par == '/':
                result = float(compute(n.sbg, scope)) / float(compute(n.sbd, scope))
                if int(result) == result: result = int(result)
                return result
            elif n.par == '%':
                return compute(n.sbg, scope) % compute(n.sbd, scope)
            elif n.par == '**':
                return compute(n.sbg, scope) ** compute(n.sbd, scope)
            elif n.par == '//':
                return compute(n.sbg, scope) // compute(n.sbd, scope)
            elif n.par == 'and':
                return compute(n.sbg, scope) and compute(n.sbd, scope)
            elif n.par == 'or':
                return compute(n.sbg, scope) or compute(n.sbd, scope)
            elif n.par == 'not':
                return not compute(n.sbg, scope)
            elif n.par == '==':
                return compute(n.sbg, scope) == compute(n.sbd, scope)
            elif n.par == '!=':
                return compute(n.sbg, scope) != compute(n.sbd, scope)
            elif n.par == '>':
                return compute(n.sbg, scope) > compute(n.sbd, scope)
            elif n.par == '>=':
                return compute(n.sbg, scope) >= compute(n.sbd, scope)
            elif n.par == '<':
                return compute(n.sbg, scope) < compute(n.sbd, scope)
            elif n.par == '<=':
                return compute(n.sbg, scope) <= compute(n.sbd, scope)
            elif n.par == 'in':
                elem = compute(n.sbg, scope)
                liste = compute(n.sbd, scope)
                if not isiterable(liste):
                    raise Exception("005 In operand is not iterable")
                return elem in liste
            elif n.par == 'call':
                if n.sbg.sbg == 'writeln':
                    param = compute(n.sbd, scope)
                    for p in param:
                        print(p)
                elif n.sbg.sbg == 'write':
                    param = compute(n.sbd, scope)
                    for p in param:
                        sys.stdout.write(str(p))
            elif n.par == 'index':
                liste = compute(n.sbg, scope)
                index = compute(n.sbd, scope)
                if not isiterable(liste):
                    raise Exception("005 Index operand is not iterable")
                return liste[index] 
        elif n.typ == 'unaop':
            if n.par == '-':
                return -compute(n.sbg, scope)
            elif n.par == 'not':
                return not compute(n.sbg, scope)
        elif n.typ == 'function':
            print('DECL function %s' % (n.sbd,))
        elif n.typ == 'class':
            print('DECL class %s' % (n.sbd,))
            compute(n.sbg, scope)
        elif n.typ == 'module':
            print('DECL module %s' % (n.sbd,))
            compute(n.sbg, scope)
        elif n.typ == 'return':
            if n.par is not None: 
                print('return expr')
                return compute(n.par, scope)  # node:expr
            else:
                print('return empty')
        elif n.typ == 'require':
            print('require' + ' -> %s' % (n.par,))     # string
        elif n.typ == 'include':
            print('include' + ' -> %s' % (n.par,)) # id
        elif n.typ == 'break':
            scope.flux = 'break'
            return None
        elif n.typ == 'continue':
            scope.flux = 'continue'
            return None
        else:
            raise Exception('n.typ is unknown: %s' % (n.typ,))
    else:
        print('error on '+str(n))
        if n.__class__ == list:
            for elem in n:
                print(elem)
        raise Exception('n is not a Node but %s (%s)' % (n.__class__,str(n)))

# if                    if              cond        action  sinon
# unless            unless        cond        action  sinon
# affectation      aff.            operator    var     expr
# while              while          cond        action  x
# for                 for             liste       action  id      <o>
# unaop            unaop         operator    operand x
# definition        fun/cls/mod param       action  name    <o>

#-[Shell Commands]-------------------------------------------------------------

def cmd_dump():
    if len(Root.vars) > 0:
        print("Listing vars : %i" % len(Root.vars))
        for k in Root.vars:
            print("%s:%s:%s" % (k, Root.vars[k].__class__, Root.vars[k]))
    else:
        print("No vars in current scope")

def cmd_exit():
    pass

def cmd_tokens():
    global String
    if String == '':
        print('Last string is empty')
    elif String in commands:
        print('Last string is a command')
    else:
        tokens = get_tokens(String)
        for tok in tokens:
            print(tok)

def cmd_help():
    print('This is an interpreter for Pypo. Have fun!')
    print('Commands:')
    print('exit\texit this interpreter')
    print('dump\tdump all variables in current scope')
    print('tokens\tprint the last tokens entered')
    print('help\tthis help')

commands = { 'exit' : cmd_exit, 'dump' : cmd_dump, 'tokens' : cmd_tokens, 'help' : cmd_help }

#-[Execution]------------------------------------------------------------------

class Scope:
    def __init__(self, typ):
        self.vars = {}
        self.type = typ
        self.flux = 'normal'

Root = Scope('root')
Root.vars['_'] = None
String = ''

#-[Main Function]--------------------------------------------------------------

if os.path.exists('./essai.rb') and not skip_files:
    print('> Tests Directory Found')
    #files = os.listdir('./tests')
    files = ['while.rb'] #['not.rb'] #['essai.rb', 'modules.rb', 'call.rb', 'if.rb', 'if_if.rb', 'if_else.rb', 'unless_else.rb', 'if_else_if.rb','if_essai.rb']
    compute_string("aaa = 22\n", Root)
    cmd_dump()
    raw_input('Press Enter to go')
    for fname in files:
        print('--Filename ' + fname + '-----------------------------------------')
        #f = file('./tests/' + fname)
        f = file(fname)
        content = f.read()
        print('--Content')
        content += "\n"
        print(content)
        print('--Tokens')
        tokens = get_tokens(content)
        for t in tokens:
            print(t)
        print('--Eval')
        print compute_string(content, Root)
        raw_input('Press Enter for next file')

if __name__ == '__main__':
    if shell:
        s = ''
        while s != 'exit':
            String = s
            s = raw_input('>>> ')
            #print(String)
            #print(s)
            if s in commands:
                commands[s]()
            else:
                ###
                s += "\n"
                if debug:
                    print s
                    for t in get_tokens(s):
                        print(t)
                ###
                result = compute_string(s, Root)
                Root.vars['_'] = result
                print result
    else:
        files = ('essai.pypo',)
        String = read(files[0])
        compute_string(String)
        dump()

