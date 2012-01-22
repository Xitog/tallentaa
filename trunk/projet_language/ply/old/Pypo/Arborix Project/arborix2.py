import lex
import yacc

# v1 (let A 11-3) 11 33 (let B 14+4) #PIPOP DJKJDKJD
# (sans VAR, AFFECT, NEWLINE, SEMI)

# TOUJOURS TESTER SI ID N'APPARTIENT PAS KEYWORDS !!!

# Types geres
# FLOAT
# INT
# BOOL

# Operations
# Assignation var id = expr
# if : en cours. Pb avec les NEWLINE. Faire deux interpret ? Un clavier, et un fichier ?

# 00h02 : fin

#http://docs.python.org/dev/howto/regex.html
#http://www.zenspider.com/Languages/Ruby/QuickRef.html

types = ('FLOAT', 'INT', 'STRING', 'BOOL', 'ID')
symbols = ('OPEN_PAR', 'CLOSING_PAR', 'OPEN_SB', 'CLOSING_SB', 'SEMI')
litterals = ('TRUE', 'FALSE', 'NIL')
statements = ('IF', 'LET', 'WHILE', 'ELSE', 'VAR', 'THEN', 'END', 'PASS')
keywords = litterals + statements
operators = ('ADD', 'MIN', 'MUL', 'DIV', 'INTDIV', 'POW', 'MOD', 'AFFECT')

tokens = types + symbols + keywords + operators + ('COMMENT', 'NEWLINE')

t_ADD = r'\+'
t_MIN = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_INTDIV = r'//'
t_POW = r'\*\*'
t_MOD = r'%'

t_AFFECT = r'='

t_OPEN_PAR = r'\('
t_CLOSING_PAR = r'\)'
t_OPEN_SB = r'\['
t_CLOSING_SB = r'\]'
#t_SEPARATOR = r'\|'

t_SEMI    = r';'

t_IF = r'IF'
t_LET = r'LET'
t_WHILE = r'WHILE'
t_ELSE = r'ELSE'
t_VAR = r'VAR'
t_THEN = r'THEN'
t_END = r'END'
t_PASS = r'PASS'

def t_TRUE(t):
    r'True'
    t.value = True
    return t

def t_FALSE(t):
    r'False'
    t.value = False
    return t

def t_NIL(t):
    r'Nil'
    t.value = None
    return t

# Bien mettre Float avant Int !
def t_FLOAT(t):
    r'(\d*\.\d+)|(\d+\.\d*)'
    #r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][0-9a-zA-Z_]*'
    if t.value.upper() in keywords:
        t.type = t.value.upper()
    return t

def t_STRING(t):
    r'\".*?\"'               # *? non-greedy version
    t.value = t[1:len(t)-1]
    return t

# re.end() == len(s) pour les matchs !!!
# truepipo sera vrai sinon alors que on veut que
# true(FIN)

def t_COMMENT(t):
    r'\# .*'
    #return t

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t

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

def check(p):
    if p.__class__ != Node:
        Exception("FUCK")

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
        check(p[0])
    elif len(p) > 2:
        p[0] = create_program(p[1], p[2])
        check(p[0])
    else:
        p[0] = create_program(None, None)
        check(p[0])

def p_programme_error(p):
    '''programme : error'''
    p[0] = None
    p.parser.error = 1

#----------------------------------------------------------------------------------------------------------------------------------------------------

def p_statement(p):
    '''statement : command NEWLINE
                 | command SEMI'''
    p[0] = p[1]
    check(p[0])

def p_statement_error(p):
    '''statement : error NEWLINE
                 | error SEMI'''
    print("MALFORMED STATEMENT AT LINE %s" % p[1])
    p[0] = None
    p.parser.error = 1

def p_statement_blank(p):
    '''statement : NEWLINE'''
    p[0] = None

def p_command_affectation(p):
    '''command : VAR ID AFFECT expression'''
    p[0] = create_let(create_id(p[2]),p[4])
    check(p[0])

def p_statement_expression(p):
    '''statement : expression NEWLINE
                 | expression SEMI'''
    p[0] = p[1]
    check(p[0])

def p_statement_if(p):
    '''command : IF expression THEN block END'''
    p[0] = create_if(p[2], p[4], None)
    check(p[0])

def p_statement_ifelse(p):
    '''command : IF expression THEN block ELSE block END'''
    p[0] = create_if(p[2], p[4], p[6])
    check(p[0])

def p_block(p):
    '''block : block statement
             | statement
             | PASS'''
    if len(p) == 1:
        p[0] = None
    elif len(p) == 2:
        p[0] = p[1]
        check(p[0])
    elif len(p) > 2:
        p[0] = create_program(p[1], p[2])
        check(p[0])

#----------------------------------------------------------------------------------------------------------------------------------------------------

def p_expression_int(p):
    '''expression : INT'''
    p[0] = create_int(p[1])
    check(p[0])

def p_expression_float(p):
    '''expression : FLOAT'''
    p[0] = create_float(p[1])
    check(p[0])

def p_expression_id(p):
    '''expression : ID'''
    p[0] = create_id(p[1])
    check(p[0])

def p_expression_bool(p):
    '''expression : TRUE
                  | FALSE'''
    p[0] = create_bool(p[1])
    check(p[0])

def p_expression_bin(p):
    '''expression : expression ADD expression
                  | expression MIN expression
                  | expression DIV expression
                  | expression MUL expression
                  | expression POW expression
                  | expression MOD expression
                  | expression INTDIV expression'''
    p[0] = create_expression_bin(p[2], p[1], p[3])
    check(p[0])

def p_expression_una(p):
    '''expression : MIN expression %prec UMIN'''
    p[0] = create_expression_una(p[1], p[2])
    check(p[0])

#----------------------------------------------------------------------------------------------------------------------------------------------------

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
    #print n.__class__
    #print n
    #print "n.code %s" % (n.code,)
    #print "n.parameters %s" % (n.parameters,)
    
    if level != -1:
        fs = prod(level)+n.code
    else:
        fs = n.code
    if n.value is not None:
        #print "afjj"
        fs += "{%s}" % n.value
    if n.parameters is not None:
        #print "kjccbb"
        fs += "[" + explore(n.parameters,-1) + "]"
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
    if n.code == 'LET':
        vars[n.parameters.value] = compute(n.sbg)
        return vars[n.parameters.value]
    elif n.code == 'IF':
        if compute(n.parameters):
            return compute(n.sbg)
        elif n.sbd is not None:
            return compute(n.sbd)
        else:
            return None
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
    elif n.code in ('INT', 'FLOAT', 'BOOL'):
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
    print result.__class__
    print(explore(result,0))
    print("\nResult = %s" % compute(result))
    print("\nListing vars")
    for k in vars:
        print("%s:%s" % (k, vars[k]))
