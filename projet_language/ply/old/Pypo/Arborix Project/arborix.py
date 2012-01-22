import lex
import yacc

# v1 (let A 11-3) 11 33 (let B 14+4) #PIPOP DJKJDKJD

# TOUJOURS TESTER SI ID N'APPARTIENT PAS KEYWORDS !!!

types = ('FLOAT', 'INT', 'STRING', 'BOOL', 'ID')
symbols = ('OPEN_PAR', 'CLOSING_PAR', 'OPEN_SB', 'CLOSING_SB')
statements = ('IF', 'LET', 'WHILE', 'ELSE')
operators = ('ADD', 'MIN', 'MUL', 'DIV', 'INTDIV', 'POW', 'MOD')

tokens = types + symbols + statements + operators + ('COMMENT',)

t_ADD = r'\+'
t_MIN = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_INTDIV = r'//'
t_POW = r'\*\*'
t_MOD = r'%'

t_OPEN_PAR = r'\('
t_CLOSING_PAR = r'\)'
t_OPEN_SB = r'\['
t_CLOSING_SB = r'\]'
#t_SEPARATOR = r'\|'

t_IF = r'IF'
t_LET = r'LET'
t_WHILE = r'WHILE'
t_ELSE = r'ELSE'

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_FLOAT(t):
    r'\d+.\d*'
    t.value = float(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][0-9a-zA-Z_]*'
    if t.value.upper() in statements:
        t.type = t.value.upper()
    return t

def t_STRING(t):
    r'\".*?\"'               # *? non-greedy version
    t.value = t[1:len(t)-1]
    return t

def t_BOOL(t):
    r'(true)|(false)'       # re.end() == len(s) pour les matchs !!!
    if t == 'true':         # truepipo sera vrai sinon alors que on veut que
        t.value = true      # true(FIN)
    else:
        t.value = false
    return t

def t_COMMENT(t):
    r'\# .*'
    #return t

t_ignore = ' \t'

def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)

lex.lex()

if __name__ == '__main__':
    import sys
    s = raw_input('>>> ')
    s += "\n"
    lex.input(s)

while 1:
    tok = lex.token()
    if not tok: break
    print "line %d:%s(%s)"%(tok.lineno, tok.type, tok.value)

class Node:
    def __init__(self, code, parameters = None, sbg = None, sbd = None, value = None):
        self.code = code
        self.parameters = parameters
        self.sbg = sbg
        self.sbd = sbd
        self.value = value
    
    def __str__(self):
        if self.code in ('INT','ID','FLOAT'):
            return "(%s : val : %s)" % (self.code, self.value)
        elif self.code in ('LET'):
            return "(%s %s %s)" % (self.code, self.parameters, self.sbg)
        else:
            return "(%s [%s] %s else %s : val : %s)" % (self.code, self.parameters, self.sbg, self.sbd, self.value)

def create_program(sbg, sbd):
    return Node('PROGRAM', None, sbg, sbd, None)

def create_while(condition, on_true, on_false):
    return Node('WHILE', condition, on_true, on_false, None)
def create_if(condition, on_true, on_false):
    return Node('IF', condition, on_true, on_false, None)
def create_let(ids, expr):
    return Node('LET', ids, expr, None, None)

def create_int(value):
    return Node('INT', None, None, None, value)
def create_float(value):
    return Node('FLOAT', None, None, None, value)
def create_bool(value):
    return Node('BOOL', None, None, None, value)
def create_string(value):
    return Node('STRING', None, None, None, value)
def create_id(value):
    return Node('ID', None, None, None, value)

def create_expression_bin(type, expr1, expr2):
    return Node(type, None, expr1, expr2, None)
def create_expression_una(type, expr1):
    return Node(type, None, expr1, None, None)

# (if [pipo == 4] ... | ...)

#def p_programme_while_complex(p):
#    '''programme : OPEN_PAR WHILE OPEN_SB expression CLOSING_SB programme ELSE programme CLOSING_PAR'''
#    p[0] = create_while(p[4], p[6], p[7])

#def p_programme_while_simple(p):
#    '''programme : OPEN_PAR WHILE OPEN_SB expression CLOSING_SB programme CLOSING_PAR'''
#    p[0] = create_while(p[4], p[6], None)

#def p_programme_if_complex(p):
#    '''programme : OPEN_PAR IF OPEN_SB expression CLOSING_SB programme ELSE programme CLOSING_PAR'''
#    p[0] = create_if(p[4], p[6], p[7])

#def p_programme_if_simple(p):
#    '''programme : OPEN_PAR IF OPEN_SB expression CLOSING_SB programme CLOSING_PAR'''
#    p[0] = create_if(p[4], p[6], None)

precedence = (
               ('left', 'ADD','MIN'),
               ('left', 'MUL','DIV'),
               ('left', 'POW'),
               ('right','UMIN')
)

def p_programme(p):
    '''programme : programme statement
                 | statement
                 |'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) > 2:
        p[0] = create_program(p[1], p[2])
    else:
        p[0] = create_program(None, None)

def p_programme_error(p):
    '''programme : error'''
    p[0] = None
    p.parser.error = 1

def p_statement_let_simple(p):
    '''statement : OPEN_PAR LET ID expression CLOSING_PAR'''
    p[0] = create_let(create_id(p[3]), p[4])

def p_expression_int(p):
    '''expression : INT'''
    p[0] = create_int(p[1])

def p_expression_float(p):
    '''expression : FLOAT'''
    p[0] = create_float(p[1])

def p_expression_id(p):
    '''expression : ID'''

def p_expression_bin(p):
    '''expression : expression ADD expression
                  | expression MIN expression
                  | expression DIV expression
                  | expression MUL expression
                  | expression POW expression
                  | expression MOD expression
                  | expression INTDIV expression'''
    p[0] = create_expression_bin(p[2], p[1], p[3])

def p_expression_una(p):
    '''expression : MIN expression %prec UMIN'''
    p[0] = create_expression_una(p[1], p[2])
    
def p_error(p):
    if p is not None:
        print "Syntax error in line %d" % p.lineno
    else:
        print "p is None"
        s = raw_input()
    yacc.errok()

yacc.yacc()

def prod(level):
    s = ''
    for i in range(0,level):
        s+='\t'
    return s

def explore(n, level):
    if level != -1:
        fs = prod(level)+n.code
    else:
        fs = n.code
    if n.value is not None:
        fs += "{%s}" % n.value
    if n.parameters is not None:
        fs += "[" + explore(n.parameters,-1) + "]"
    if n.sbg is not None:
        fs += "\n"
        fs += explore(n.sbg, level+1)
    if n.sbd is not None:
        fs += "\n"
        fs += explore(n.sbd, level+1)
    return fs

vars = {}
def compute(n):
    if n.code == 'LET':
        vars[n.parameters.value] = compute(n.sbg)
        return vars[n.parameters.value]
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
    elif n.code in ('INT', 'FLOAT'):
        return n.value
    elif n.code == 'PROGRAM':
        if n.sbd is not None:
            compute(n.sbg)
            return compute(n.sbd)
        elif n.sbg is not None:
            return compute(n.sbg)
        else:
            return None

if __name__ =="__main__":
    result = yacc.parse(s) #, debug=2)
    #print '>>>', result
    print(explore(result,0))
    print("\nResult = %s" % compute(result))
    print("\nListing vars")
    for k in vars:
        print("%s:%s" % (k, vars[k]))
