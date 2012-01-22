import lex
import yacc
from arb_lexer import *

#k ID affectation_operator expression
#k expression binary_operator expression
#k unary_operator expression
#k expression (bool, string, float, int, id)
#k ( expressiion )
#t if condition then statements else statements end   # 15hxx OK
#t print( expression ) # 16h03 à présent, il va falloir faire une pile !
#t while condition do statements end
#t break
#t continue

from_disk = True

if __name__ == '__main__':
    import sys
    if not from_disk:
        s = raw_input('>>> ')
    else:
        f = file('essai.txt')
        s = f.read()
        print("s last: %s" % (s[len(s)-1],))
    #s += "\n"
    lex.input(s)

while 1:
    tok = lex.token()
    if not tok: break
    if tok.type != 'NEWLINE':
        print "line %d:%s(%s)"%(tok.lineno, tok.type, tok.value)
    else:
        print("line %d:%s(\\n)"%(tok.lineno, tok.type))

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
def create_aff(afftype, ids, expr):
    return Node(afftype, ids, expr, None, None)

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
    if p is None or p.__class__ != Node:
        Exception("FUCK")

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
        p[0] = create_program(p[1],None)
    elif len(p) == 3:
        p[0] = create_program(p[1],p[2])
    else:
        p[0] = create_program(None, None)
    check(p[0])

def p_programme_error(p):
    '''programme : error'''
    p[0] = None
    p.parser.error = 1

#----------------------------------------------------------------------------------------------------------------------------------------------------

def p_statement(p):
    ''' statement : affectation
                  | expression
                  | if_sta
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
    p[0] = create_aff(p[2], create_id(p[1]), p[3])
    print("> affecation")
    check(p[0])

def p_statement_if(p):
    '''if_sta : IF expression THEN programme ELSE programme END
              | IF expression THEN programme END'''
    if len(p) == 6:
        p[0] = create_if(p[2], p[4], None)
    elif len(p) == 8:
        p[0] = create_if(p[2], p[4], p[6])
    check(p[0])

def p_statement_call(p):
    '''fct_call : ID OPEN_PAR parameters CLOSING_PAR'''
    p[0] = Node(code='FUNCALL', parameters=create_id(p[1]), sbg=p[3], sbd=None, value=None)

def p_parameters(p):
    '''parameters : parameters COMMA expression
                  | expression'''
    print('> parameters')
    if len(p) == 4:
        p[0] = Node('PARAMS', None, p[1], p[3])
    else:
        p[0] = Node('PARAMS', None, sbg=p[1])

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

def p_expression_string(p):
    '''expression : STRING'''
    p[0] = Node('STRING', None, None, None, p[1])
    check(p[0])

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
    check(p[0])

def p_expression_una(p):
    '''expression : MIN expression %prec UMIN
                  | NOT expression'''
    p[0] = create_expression_una(p[1], p[2])
    check(p[0])

#----------------------------------------------------------------------------------------------------------------------------------------------------

'''def p_error(p):
    if p is not None:
        print "Syntax error in line %d" % p.lineno
    else:
        print "p is None"
        s = raw_input()
    yacc.errok()
'''

yacc.yacc()

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
    if n.code == '=':
        vars[n.parameters.value] = compute(n.sbg)
        return vars[n.parameters.value]
    elif n.code == '+=':
        vars[n.parameters.value] += compute(n.sbg)
    elif n.code == '-=':
        vars[n.parameters.value] -= compute(n.sbg)
    elif n.code == '*=':
        vars[n.parameters.value] *= compute(n.sbg)
    elif n.code == '/=':
        vars[n.parameters.value] /= compute(n.sbg)
    elif n.code == '//=':
        vars[n.parameters.value] //= compute(n.sbg)
    elif n.code == '%=':
        vars[n.parameters.value] %= compute(n.sbg)
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
    elif n.code == 'ID':
        return vars[n.value]
    elif n.code == 'FUNCALL':
        if n.parameters.value == 'print':
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

if __name__ =="__main__":
    result = yacc.parse(s) #, debug=2)
    #print '>>>', result
    print result.__class__
    print(explore(result,0))
    print("------------------ End Explore ------------------")
    print("\nResult = %s" % compute(result))
    print("\nListing vars")
    for k in vars:
        print("%s:%s:%s" % (k, vars[k].__class__, vars[k]))
