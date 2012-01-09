import lex
import yacc
from simple_lexer import *

precedence = (
               ('left', 'AND', 'OR'),
               ('left', 'EQ', 'NE', 'IN'),
               ('left', 'GE', 'GT', 'LE', 'LT'),
               ('left', 'ADD','MIN'),
               ('left', 'MUL','DIV', 'MOD', 'DIV_INT'),
               ('left', 'POW'),
               ('left', 'LEFT_SB'),
               ('left', 'LEFT_PAR'),
)

class Node(object):
    
    def __init__(self, typ, par=None, sbg=None, sbd=None):
        self.typ = typ
        self.par = par
        self.sbg = sbg
        self.sbd = sbd
    
    def __str__(self):
        par = pretty_list(self.par)
        sbg = pretty_list(self.sbg)
        sbd = pretty_list(self.sbd)
        if self.sbd is None:
                print self.typ, self.par
                if self.typ == 'value':
                    return "(%s)" % (self.sbg)
                elif self.typ == 'if':
                    return "(if[%s]? %s | %s)" % (par, sbg, sbd)
                elif self.typ == 'list':
                    return "(%s)" % sbg
                else:
                    return "(n:%s,p:%s,<-:%s)" % (self.typ, par, sbg)
        else:
            if self.typ == 'binop':
                return "(%s, %s, %s)" % (par, sbg, sbd)
            return "(n:%s,p:%s,<-:%s,->:%s)" % (self.typ, par, sbg, sbd)

def pretty_list(o):
    if isinstance(o, list):
        s = '['
        i = 0
        for e in o:
            s += str(e)
            if i != len(o)-1:
                s += ', '
            i+=1
        s += ']'
        return s
    else:
        return str(o)


def p_program(p):
    '''program : statements_suite'''
    print('> program')
    p[0] = Node(typ='list', par='sta', sbg=p[1])

def p_statements_suite(p):
    '''statements_suite : statements_suite statement
                        | statement'''
    if len(p) == 3: # statements_suite
        print('> statements suite')
        if p[2] != 'newline':
            p[1].append(p[2])
        p[0] = p[1]
    elif len(p) == 2: # statement
        print('> statement')
        if p[1] != 'newline':
            p[0] = [p[1]]
        else:
            p[0] = []

def p_statement_empty(p):
    '''statement : NEWLINE'''
    p[0] = 'newline'

def p_statement(p):
    '''statement : statement_libre NEWLINE'''
    print('> complete')    
    p[0] = p[1]

def p_statement_libre(p):
    '''statement_libre : selection
                       | expression'''
    print('> libre')    
    p[0] = p[1]

def p_selection_multi(p):
    '''selection : IF expression THEN statements_suite END'''
    p[0] = Node(typ=p[1], par=p[2], sbg=p[4], sbd=None)

def p_selection_one(p):
    '''selection : IF expression THEN statement_libre END'''
    p[0] = Node(typ=p[1], par=p[2], sbg=p[4], sbd=None)

def p_expression_binop(p):
    '''expression : expression ADD expression
                  | expression MIN expression
                  | expression DIV expression
                  | expression MUL expression
                  | expression POW expression
                  | expression MOD expression
                  | expression DIV_INT expression
                  | expression AND expression
                  | expression OR expression
                  | expression EQ expression
                  | expression NE expression
                  | expression LT expression
                  | expression LE expression
                  | expression GT expression
                  | expression GE expression
                  | expression IN expression'''
    print('> binop')
    p[0] = Node(typ='binop', par=p[2], sbg=p[1], sbd=p[3])

def p_expression_int(p):
    '''expression : INT'''
    print('> int')
    p[0] = Node(typ='value', par='int', sbg=int(p[1]))

def p_expression_id(p):
    '''expression : ID'''
    print('> id')
    p[0] = Node(typ='value', par='id', sbg=p[1])

def p_expression_flt(p):
    '''expression  : FLOAT'''
    print('> float')
    p[0] = Node(typ='value', par='flt', sbg=float(p[1]))

def p_expression_true(p):
    '''expression  : TRUE'''
    print('> true')
    p[0] = Node(typ='value', par='bool', sbg=True)

def p_expression_false(p):
    '''expression  : FALSE'''
    print('> false')
    p[0] = Node(typ='value', par='bool', sbg=False)

def p_expression_nil(p):
    '''expression : NIL'''
    p[0] = Node(typ='value', par='nil', sbg=None)

def p_error(p):
    if p is not None:
        print "Syntax error in line %d" % p.lineno
        print(p)
        import sys
        sys.exit(1)
    else:
        print 'p is None. No rule matching.'
    #yacc.errok()
    return None

yacc.yacc()

def cmd_exit():
    pass

shell = True
debug = True
commands = { 'exit' : cmd_exit}
Root = {}

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

import sys

def mwrite(*liste):
    for i in liste:
        sys.stdout.write(str(i))

def disp(s):
    mwrite('[',s, '] l->', len(s), "\n")
    for t in get_tokens(s):
        print(t)

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
                #Root.vars['_'] = result
                #print result
    else:
        files = ('essai.pypo',)
        String = read(files[0])
        compute_string(String)
        dump()

