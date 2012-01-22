import lex
import yacc
from pypo_lexer import *

class Node:
    def __init__(self, code, param = None, sbg = None, sbd = None, value = None):
        self.code  = code
        self.param = param
        self.sbg   = sbg
        self.sbd   = sbd
        self.value = value
    
    def __str__(self):
        if self.code in ('INT','ID','FLOAT'):
            return "(%s : val : %s)" % (self.code, self.value)
        elif self.code in ('LET'):
            return "(%s %s %s)" % (self.code, self.param, self.sbg)
        else:
            return "(%s [%s] %s else %s : val : %s)" % (self.code, self.param, self.sbg, self.sbd, self.value)

def create_while(condition, on_true, on_false):
    return Node('WHILE', condition, on_true, on_false, None)
def create_id(value):
    return Node('ID', None, None, None, value)
def create_expression_bin(type, expr1, expr2):
    return Node(type, None, expr1, expr2, None)
def create_expression_una(type, expr1):
    return Node(type, None, expr1, None, None)

precedence = (
               ('left', 'AND', 'OR'),
               ('left', 'EQ', 'NE'),
               ('left', 'GE', 'GT', 'LE', 'LT'),
               ('left', 'ADD','MIN'),
               ('left', 'MUL','DIV', 'MOD'),
               ('left', 'POW'),
               ('right','UMIN', 'NOT')
)

def p_programme(p):
    '''programme : programme statement
                 | statement
                 |'''
    if len(p) == 2:
        p[0] = Node('PROGRAM', None, p[1], None, None)
    elif len(p) == 3:
        p[0] = Node('PROGRAM', None, p[1], p[2], None)
    else:
        p[0] = Node('PROGRAM', None, None, None, None)

def p_programme_error(p):
    '''programme : error'''
    p[0] = None
    p.parser.error = 1

#----------------------------------------------------------------------------

def p_statement(p):
    ''' statement : affectation
                  | expression
                  | if_sta
                  | while_sta
                  | fct_call'''
    print("> statement")
    p[0] = p[1]

def p_command_affectation(p):
    '''affectation : ID AFFECT expression
                   | ID ADD_AFF expression
                   | ID MIN_AFF expression
                   | ID MUL_AFF expression
                   | ID DIV_AFF expression
                   | ID MOD_AFF expression
                   | ID IDV_AFF expression'''
    p[0] = Node(code=p[2], param=create_id(p[1]), sbg=p[3])
    print("> affecation")

def p_statement_if(p):
    '''if_sta : IF expression THEN programme ELSE programme END
              | IF expression THEN programme END'''
    if len(p) == 6:
        p[0] = Node('IF', p[2], p[4], None, None)
    elif len(p) == 8:
        p[0] = Node('IF', p[2], p[4], p[6], None)

def p_statement_while(p):
	'''while_sta : WHILE expression DO programme END'''
	p[0] = Node('WHILE', p[2], p[4], None, None)

def p_statement_call(p):
    '''fct_call : ID OPEN_PAR parameters CLOSING_PAR'''
    p[0] = Node(code='FUNCALL', param=create_id(p[1]), sbg=p[3], sbd=None, value=None)

def p_parameters(p):
    '''parameters : parameters COMMA expression
                  | expression'''
    print('> parameters')
    if len(p) == 4:
        p[0] = Node('PARAMS', None, p[1], p[3])
    else:
        p[0] = Node('PARAMS', None, sbg=p[1])

#----------------------------------------------------------------------------

def p_expression_int(p):
    '''expression : INT'''
    p[0] = Node(code='INT', value=p[1])

def p_expression_float(p):
    '''expression : FLOAT'''
    p[0] = Node(code='FLOAT', value=p[1])

def p_expression_id(p):
    '''expression : ID'''
    p[0] = create_id(p[1])

def p_expression_bool(p):
    '''expression : TRUE
                  | FALSE'''
    p[0] = Node('BOOL', None, None, None, p[1])

def p_expression_string(p):
    '''expression : STRING'''
    p[0] = Node('STRING', None, None, None, p[1])

def p_expression_par(p):
    '''expression : OPEN_PAR expression CLOSING_PAR'''
    p[0] = p[2]

def p_expression_bin(p):
    '''expression : expression ADD expression
                  | expression MIN expression
                  | expression DIV expression
                  | expression MUL expression
                  | expression POW expression
                  | expression MOD expression
                  | expression INTDIV expression
                  | expression AND expression
                  | expression OR expression
                  | expression EQ expression
                  | expression NE expression
                  | expression LT expression
                  | expression LE expression
                  | expression GT expression
                  | expression GE expression'''
    p[0] = create_expression_bin(p[2], p[1], p[3])
    print("> expressionbin")

def p_expression_una(p):
    '''expression : MIN expression %prec UMIN
                  | NOT expression'''
    p[0] = create_expression_una(p[1], p[2])

#----------------------------------------------------------------------------

'''def p_error(p):
    if p is not None:
        print "Syntax error in line %d" % p.lineno
    else:
        print "p is None"
        s = raw_input()
    yacc.errok()
'''

yacc.yacc()
