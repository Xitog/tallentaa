import lex
import yacc
from nnlexer import *

pdebug = False

def config(debug_parser):
    global pdebug
    pdebug = debug_parser

precedence = (
               ('right', 'EMPTY_RETURN'),
               ('right', 'RETURN'),
               ('nonassoc', 'TRUE', 'FALSE', 'INT', 'FLOAT', 'STRING', 'ID'),
               ('right', 'KEY_OP'),
               ('right', 'AFFECT', 'ADD_AFF', 'MIN_AFF', 'MUL_AFF', 'DIV_AFF', 'DIV_INT_AFF', 'MOD_AFF', 'POW_AFF'),
               ('left', 'AND', 'OR'),
               ('left', 'EQ', 'NE', 'IN'),
               ('left', 'GE', 'GT', 'LE', 'LT'),
               ('left', 'ADD','MIN', 'LSHIFT'),
               ('left', 'MUL','DIV', 'DIV_INT'),
               ('left', 'MOD','POW'),
               ('left', 'LEFT_SB', 'LEFT_CB'),
               ('left', 'LEFT_PAR'),
               ('right', 'UMIN', 'NOT'),
               ('right', 'PAREXPR'),
               ('right', 'PARCALL'),
               ('left', 'DOT'),
)

#
# SUMMARY
#
# [1] Node class
# [2] IF & UNLESS
# [3] WHILE & FOR
#

#
# [1] Node class
#

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
                if pdebug: print self.typ, self.par
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
    if pdebug: print('> program')
    p[0] = Node(typ='list', par='sta', sbg=p[1])

def p_statements_suite(p):
    '''statements_suite : statements_suite statement
                        | statement'''
    if len(p) == 3: # statements_suite
        if pdebug: print('> statements suite')
        if p[2] != 'newline': ## and p[2] is not None: ### Muy important!
            p[1].append(p[2])
        p[0] = p[1]
    elif len(p) == 2: # statement
        if pdebug: print('> statement')
        if p[1] != 'newline':
            p[0] = [p[1]]
        else:
            p[0] = []
    else:
        raise Exception("YOU SHOULDN'T BE THERE...")

def p_statement_empty(p):
    '''statement : NEWLINE'''
    p[0] = 'newline'

def p_statement(p):
    '''statement : statement_libre NEWLINE'''
    if pdebug: print('> complete')    
    p[0] = p[1]

def p_statement_libre(p):
    '''statement_libre : selection
                       | iteration
                       | flux
                       | interfiles
                       | expression
                       | affectation
                       | modulation
                       | definition
                       | declaration'''
    if pdebug: print('> libre')    
    p[0] = p[1]

#
# [2] IF & UNLESS
#

def p_selection_multi(p):
    '''selection : IF expression THEN statements_suite END
                 | IF expression THEN statements_suite ELSE statements_suite END
                 | UNLESS expression THEN statements_suite END
                 | UNLESS expression THEN statements_suite ELSE statements_suite END'''
    if len(p) == 6:
        if pdebug: print('> if multi no else')
        p[0] = Node(typ=p[1], par=p[2], sbg=Node(typ='list', par='sta', sbg=p[4]), sbd=None)
    else:
        if pdebug: print('> if multi with else')
        p[0] = Node(typ=p[1], par=p[2], sbg=Node(typ='list', par='sta', sbg=p[4]), sbd=Node(typ='list', par='sta', sbg=p[6]))

def p_selection_one(p):
    '''selection : IF expression THEN statement_libre END
                 | IF expression THEN statement_libre ELSE statement_libre END
                 | UNLESS expression THEN statement_libre END
                 | UNLESS expression THEN statement_libre ELSE statement_libre END'''
    if pdebug: print('> if simple')
    if len(p) == 6:
        p[0] = Node(typ=p[1], par=p[2], sbg=p[4], sbd=None)
    else:
        p[0] = Node(typ=p[1], par=p[2], sbg=p[4], sbd=p[6])

#
# [3] WHILE & FOR
#

def p_iteration_block(p):
    '''iteration : WHILE expression DO NEWLINE statements_suite END
                 | WHILE expression NEWLINE statements_suite END
                 | FOR ID IN expression DO statements_suite END
                 | FOR ID IN expression NEWLINE statements_suite END'''
    print('> iteration block')
    if p[1] == 'while':
        p[0] = Node(typ='while', par=p[2], sbg=Node(typ='list', par='sta', sbg=p[5]))
    else:
        p[0] = Node(typ='for', par=p[4], sbg=Node(typ='list', par='sta', sbg=p[6]), sbd=Node(typ='value', par='id', sbg=p[2]))

def p_iteration_one(p):
    '''iteration : WHILE expression DO NEWLINE statement_libre END
                 | WHILE expression DO statement_libre END
                 | WHILE expression NEWLINE statement_libre END'''
    print('> iteration one')
    if p[1] == 'while':
        if len(p) == 7:
            p[0] = Node(typ='while', par=p[2], sbg=p[5], sbd=None)
        elif len(p) == 6:
            p[0] = Node(typ='while', par=p[2], sbg=p[4], sbd=None)

def p_flux(p):
    '''flux        : BREAK
                   | NEXT
                   | RETURN expression
                   | RETURN %prec EMPTY_RETURN'''
    if p[1] == 'return' and len(p) == 3:
        print('> return expr')
        p[0] = Node(typ='return', par=p[2])
    else:
        print('> ' + p[1])
        p[0] = Node(typ=p[1])

def p_interfiles(p):
    '''interfiles  : REQUIRE STRING
                   | INCLUDE ID'''
    p[0] = Node(typ=p[1], par=p[2])

def p_affectation(p):
    '''affectation : ID AFFECT expression
                   | ID ADD_AFF expression
                   | ID MIN_AFF expression
                   | ID MUL_AFF expression
                   | ID DIV_AFF expression
                   | ID DIV_INT_AFF expression
                   | ID MOD_AFF expression
                   | ID POW_AFF expression'''
    print('> affectation')
    p[0] = Node(typ='affectation', par=p[2], sbg=Node(typ='value', par='id', sbg=p[1]), sbd=p[3])

# ( )
def p_expression_call(p):
    '''expression : expression LEFT_PAR expressions_suite RIGHT_PAR %prec PARCALL
                  | expression LEFT_PAR RIGHT_PAR %prec PARCALL'''
    if pdebug: print('> call')
    if len(p) == 5:
        p[0] = Node(typ='binop', par='call', sbg=p[1], sbd=Node(typ='list', par='expr', sbg=p[3])) # Node(typ='value', par='id', sbg=p[1])
    else:
        p[0] = Node(typ='binop', par='call', sbg=p[1], sbd=Node(typ='list', par='expr', sbg=[]))

# +, -, *, /, %, //, and, or, ==, !=, <, <=, >, >=, in : Binary operator
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
                  | expression IN expression
                  | expression DOT expression
                  | expression LSHIFT expression'''
    if pdebug: print('> binop')
    p[0] = Node(typ='binop', par=p[2], sbg=p[1], sbd=p[3])

# +, - : Unary operator expression

def p_expression_una(p):
    '''expression : MIN expression %prec UMIN
                  | NOT expression'''
    p[0] = Node(typ='unaop', par=p[1], sbg=p[2])

### {} : dict / hash

def p_expression_curly(p):
    '''expression  : LEFT_CB expressions_key_suite RIGHT_CB
                   | LEFT_CB RIGHT_CB'''
    if len(p) == 4:
        p[0] = Node(typ='list', par='dict', sbg=p[2])
    elif len(p) == 3:
        p[0] = Node(typ='list', par='dict', sbg={})

def p_expressions_key_suite(p):
    '''expressions_key_suite : expressions_key_suite COMMA expression_key
                             | expression_key'''
    if len(p) == 4:
        print('> expr key suite')
        p[1].update(p[3])
        p[0] = p[1]
    elif len(p) == 2:
        print('> expr key final of suite')
        p[0] = p[1]

def p_expression_key(p):
    '''expression_key : ID KEY_OP expression'''
    p[0] = {p[1] : p[3]}

### [] : list

def p_expression_square(p):
    '''expression  : LEFT_SB expressions_suite RIGHT_SB
                   | LEFT_SB RIGHT_SB'''
    if pdebug: print('> expression with ( )')
    if len(p) == 4:
        p[0] = Node(typ='list', par='expr', sbg=p[2])
    elif len(p) == 3:
        p[0] = Node(typ='list', par='expr', sbg=[])

def p_expressions_suite(p):
    '''expressions_suite : expressions_suite COMMA expression
                         | expression'''
    if len(p) == 4:
        if pdebug: print('> expr suite')
        p[1].append(p[3])
        p[0] = p[1]
    elif len(p) == 2:
        if pdebug: print('> expr final of suite')
        p[0] = [p[1]]

def p_expression_par(p):
    '''expression  : LEFT_PAR expression RIGHT_PAR %prec PAREXPR'''
    if pdebug: print('> expression par')
    p[0] = p[2]

def p_expression_int(p):
    '''expression : INT'''
    if pdebug: print('> int')
    p[0] = Node(typ='value', par='int', sbg=int(p[1]))

def p_expression_id(p):
    '''expression : ID'''
    if pdebug: print('> id')
    p[0] = Node(typ='value', par='id', sbg=p[1])

def p_expression_flt(p):
    '''expression  : FLOAT'''
    if pdebug: print('> float')
    p[0] = Node(typ='value', par='flt', sbg=float(p[1]))

def p_expression_true(p):
    '''expression  : TRUE'''
    if pdebug: print('> true')
    p[0] = Node(typ='value', par='bool', sbg=True)

def p_expression_false(p):
    '''expression  : FALSE'''
    if pdebug: print('> false')
    p[0] = Node(typ='value', par='bool', sbg=False)

def p_expression_nil(p):
    '''expression : NIL'''
    p[0] = Node(typ='value', par='nil', sbg=None)

def p_expression_str(p):
    '''expression  : STRING'''
    print('> string')
    p[0] = Node(typ='value', par='str', sbg=p[1])

def p_modulation(p):
    '''modulation  : MODULE ID statements_suite END'''
    p[0] = Node(typ='module', par=None, sbg=Node(typ='list', par='sta', sbg=p[3]), sbd=p[2])

def p_definition(p):
    '''definition  : DEF ID LEFT_PAR parameters RIGHT_PAR statements_suite END
                   | DEF ID LEFT_PAR RIGHT_PAR statements_suite END'''
    if len(p) == 8:
        p[0] = Node(typ='function', par=Node(typ='list', par='id', sbg=p[4]), sbg=Node(typ='list', par='sta', sbg=p[6]), sbd=p[2])
    elif len(p) == 7:
        p[0] = Node(typ='function', par=None, sbg=Node(typ='list', par='sta', sbg=p[5]), sbd=p[2])

def p_parameters(p):
    '''parameters  : parameters COMMA parameter
                   | parameter'''
    if len(p) == 4:
        print('> param suite')
        p[1].append(p[3])
        p[0] = p[1]
    elif len(p) == 2:
        print('> param final')
        p[0] = [p[1]]

def p_parameter(p):
    '''parameter   : ID ID
                   | ID'''
    if len(p) == 3:
        p[0] = (p[1],p[2])
    elif len(p) == 2:
        p[0] = (p[1],'object')

def p_declaration(p):
    '''declaration : CLASS ID LT ID statements_suite END
                   | CLASS ID statements_suite END'''
    if len(p) == 7:
        p[0] = Node(typ='class', par=p[4], sbg=Node(typ='list', par='sta', sbg=p[5]), sbd=p[2])
    else:
        p[0] = Node(typ='class', par=None, sbg=Node(typ='list', par='sta', sbg=p[3]), sbd=p[2])

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
