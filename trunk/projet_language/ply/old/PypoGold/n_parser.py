import lex
import yacc
from n_lexer import *

# Todo : while, id[index], id.id, (expr), not expr, - expr

# Left_sb et Left_par sont consideres comme des operateurs. C'est tres important !
# Toujours definir une precedence... sinon : shift/reduce : sans cela, 256 conflits !
# Et mes 6 erreurs dans "n_parser" etait le RETURN qui n'avait pas de precedence...

precedence = (
               ('right', 'EMPTY_RETURN'),
               ('right', 'RETURN'),
               #('left', 'NEWLINE'),
               ('nonassoc', 'INT'),
               ('nonassoc', 'FLOAT'),
               ('nonassoc', 'STRING'),
               ('nonassoc', 'ID'),
               ('right', 'AFFECT', 'ADD_AFF', 'MIN_AFF', 'MUL_AFF', 'DIV_AFF', 'DIV_INT_AFF', 'MOD_AFF', 'POW_AFF'), # 1h08 9->1 shift reduce. Je sais lire le parser.out !!!
               ('left', 'AND', 'OR'),
               ('left', 'EQ', 'NE', 'IN'),
               ('left', 'GE', 'GT', 'LE', 'LT'),
               ('left', 'ADD','MIN'),
               ('left', 'MUL','DIV', 'MOD', 'DIV_INT'),
               ('left', 'POW'),
               ('left', 'LEFT_SB'),
               ('left', 'LEFT_PAR'),
               ('left', 'DOT'),
               ('right', 'UMIN'),
               ('right', 'PAREXPR'),
               ('right', 'PARCALL'),
               ('right', 'NOT')
)

# Avec un Type, un Param, un Bras Gauche et Bras Droit, on a tout :
# Fonction          Type        Param       SBG     SBD
#--------------------------------------------------------------
# list                  list           id/expr/sta []      x
# if                    if              cond        action  sinon
# unless            unless       cond        action  sinon
# affectation      aff.            operator    var     expr
# while              while          cond        action  x
# for                 for             liste       action  id      <o>
# value             value          type        <value> x
# binop             binop          operator    op1     op2
# unaop            unaop         operator    operand x
# definition        fun/cls/mod param       action  name    <o>
# ret / req / incl  ret/req/inc expr/str/id x       x
# brk / cte         brk/cte     x           x       x

class Node(object):
    def __init__(self, typ, par=None, sbg=None, sbd=None):
        self.typ = typ
        self.par = par
        self.sbg = sbg
        self.sbd = sbd
    def __str__(self):
        return "%s(%s)[%s][%s]" % (self.typ, self.par, self.sbg, self.sbd)

#-------------------------------------------------------------------------------

def p_program(p):
    '''program : statements_suite'''
    print('> program')
    p[0] = Node(typ='list', par='sta', sbg=p[1])

def p_statements_suite(p):
    '''statements_suite : statements_suite statement_enclos
                        | statement_suite_elem'''
    if len(p) == 3:
        print('> statements suite')
        if p[2] != 'newline':
            p[1].append(p[2])
        p[0] = p[1]
    elif len(p) == 2:
        print('> statement elem')
        if p[1] != 'newline':
            p[0] = [p[1]]
        else:
            p[0] = []

def p_statement_libre(p):
    '''statement_libre : affectation
                       | expression
                       | flux
                       | interfiles'''
    print('> libre')
    p[0] = p[1]

def p_statement_clot(p):
    '''statement_clot : selection
                      | iteration
                      | modulation
                      | declaration
                      | definition'''
    print('> clot')
    p[0] = p[1]

def p_statement_libre_clot(p):
    '''statement_libre_clot : statement_libre NEWLINE'''
    print('> libre clot')
    p[0] = p[1]

def p_statement_suite_elem(p):
    '''statement_suite_elem : statement_libre_clot
                            | statement_clot'''
    print('> suite')
    p[0] = p[1]

# 20h18 : la cle est la : c un statement clos et pas un suite_elem !!!!!!!
def p_statement_suite_elem_empty(p):
    '''statement_clot : NEWLINE'''
    print('> empty')
    p[0] = 'newline'

# mettable dans un "enclos"
def p_statement_enclos(p):
    '''statement_enclos : statement_libre
                        | statement_clot'''
    print('> enclos')
    p[0] = p[1]

#-------------------------------------------------------------------------------

def p_selection_one(p):
    '''selection   : IF expression THEN statement_enclos END
                   | IF expression THEN statement_enclos ELSE statement_enclos END
                   | UNLESS expression THEN statement_enclos END
                   | UNLESS expression THEN statement_enclos ELSE statement_enclos END'''
    print('> if one sta')
    if len(p) == 8:
        sinon = p[6]
    else:
        sinon = None
    p[0] = Node(typ=p[1], par=p[2], sbg=p[4], sbd=sinon)

def p_selection_block(p):
    '''selection : IF expression THEN NEWLINE statements_suite END
                 | IF expression THEN NEWLINE statements_suite ELSE statements_suite END
                 | UNLESS expression THEN NEWLINE statements_suite END
                 | UNLESS expression THEN NEWLINE statements_suite ELSE statements_suite END'''
    print('> if block')
    if len(p) == 9:
        sinon = Node(typ='list', par='sta', sbg=p[7])
    else:
        sinon = None
    p[0] = Node(typ=p[1], par=p[2], sbg=Node(typ='list', par='sta', sbg=p[5]), sbd=sinon)

def p_selection_with_elif_suite(p):
    '''selection : IF expression THEN NEWLINE statements_suite elif_suite END
                 | IF expression THEN NEWLINE statements_suite elif_suite ELSE statements_suite END'''
    print('> if block with elif')
    if len(p) == 8: # no else
        sinon_fin = None
    else:
        sinon_fin = Node(typ='list', par='sta', sbg=p[8])
    elifs = p[6]
    sinon = elifs[0]
    i = 1
    parcours = sinon
    while i < len(elifs):
        parcours.sbd = elifs[i]
        parcours = parcours.sbd
        i+=1
    parcours.sbd = sinon_fin
    p[0] = Node(typ=p[1], par=p[2], sbg=Node(typ='list', par='sta', sbg=p[5]), sbd=sinon)

def p_selection_elif_suite(p):
    '''elif_suite : elif_suite ELSIF expression THEN NEWLINE statements_suite
                  | ELSIF expression THEN NEWLINE statements_suite'''
    if len(p) == 7:
        print('> elifs suite')
        p[1].append(Node(typ='if', par=p[3], sbg=Node(typ='list', par='sta', sbg=p[6])))
        p[0] = p[1]
    elif len(p) == 6:
        print('> elif elem')
        p[0] = [Node(typ='if', par=p[2], sbg=Node(typ='list', par='sta', sbg=p[5]))]

#------------------------------------------------------------------------------

def p_iteration_block(p):
    '''iteration : WHILE expression DO NEWLINE statements_suite END'''
    print('> iteration')
    if p[1] == 'while':
        p[0] = Node(typ='while', par=p[2], sbg=Node(typ='list', par='sta', sbg=p[5]))

#def p_iteration(p):
#    '''iteration   : WHILE expression DO statements END
#                   | WHILE expression NEWLINE statements END
#                   | FOR ID IN expression DO statements END
#                   | FOR ID IN expression NEWLINE statements END'''
#    print('> iteration')
#    if p[1] == 'while':
#        p[0] = Node(typ='while', par=p[2], sbg=Node(typ='list', par='sta', sbg=p[4]))
#    else:
#        p[0] = Node(typ='for', par=p[4], sbg=Node(typ='list', par='sta', sbg=p[6]), sbd=p[2])
#    if p[0] is None: raise Exception('ZEMBLA')

# | IF expression THEN NEWLINE statements elifs ELSE statements END
#def p_selection_statements(p):
#    '''selection  : IF expression THEN NEWLINE statements END
#                  | IF expression THEN NEWLINE statements ELSE statements END
#                  | UNLESS expression THEN NEWLINE statements END
#                  | UNLESS expression THEN NEWLINE statements ELSE statements END'''
#    print('> selection statements')
#    if len(p) == 9:
#        sinon = Node(typ='list', par='sta', sbg=p[7])
#    elif len(p) == 10:
#        xp = p[6].sbd
#        while xp != None:
#            old = xp
#            xp = xp.sbd
#        old.sbd = Node(typ='list', par='sta', sbg=p[8])
#        sinon = p[6]
#    else:
#        sinon = None
#    p[0] = Node(typ=p[1], par=p[2], sbg=Node(typ='list', par='sta', sbg=p[5]), sbd=sinon)

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
    p[0] = Node(typ='affectation', par=p[2], sbg=p[1], sbd=p[3])

# classic binary operators

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

# special operators

# Call operator

def p_expression_call(p):
    '''expression : ID LEFT_PAR values RIGHT_PAR %prec PARCALL'''
    print('> call')
    p[0] = Node(typ='binop', par='call', sbg=Node(typ='value', par='id', sbg=p[1]), sbd=Node(typ='list', par='expr', sbg=p[3]))

# Access operator

#def p_expression_access(p):
#    '''expression  : expression DOT expression'''
#    p[0] = Node(typ='binop', par='access', sbg=p[1], sbd=p[3])

# Index operator

#def p_expression_index(p):
#    '''expression  : expression LEFT_SB expression RIGHT_SB'''
#    p[0] = Node(typ='binop', par='index', sbg=p[1], sbd=p[3])

# Unary operator expression

def p_expression_una(p):
    '''expression : MIN expression %prec UMIN
                  | NOT expression'''
    p[0] = Node(typ='unaop', par=p[1], sbg=p[2])

# Parenthesis

def p_expression_par(p):
    '''expression  : LEFT_PAR expression RIGHT_PAR %prec PAREXPR'''
    print('> expression par')
    p[0] = p[2]

# litterals

def p_expression_id(p):
    '''expression : ID'''
    print('> id')
    p[0] = Node(typ='value', par='id', sbg=p[1])

def p_expression_int(p):
    '''expression : INT'''
    print('> int')
    p[0] = Node(typ='value', par='int', sbg=int(p[1]))

def p_expression_flt(p):
    '''expression  : FLOAT'''
    print('> float')
    p[0] = Node(typ='value', par='flt', sbg=float(p[1]))

def p_expression_str(p):
    '''expression  : STRING'''
    print('> string')
    p[0] = Node(typ='value', par='str', sbg=p[1])

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

def p_expression_lists(p):
    '''expression  : LEFT_SB values RIGHT_SB
                   | LEFT_SB RIGHT_SB
                   | LEFT_BR keys RIGHT_BR
                   | LEFT_BR RIGHT_BR'''
    if len(p) == 3:
        if p[1] == '[':
            p[0] = Node(typ='value', par='list', sbg=[])
        else:
            p[0] = Node(typ='value', par='dict', sbg={})
    elif len(p) == 4:
        if p[1] == '[':
            f = 'list'
        else:
            f = 'dict'
        p[0] = Node(typ='value', par=f, sbg=p[2])

def p_values_list(p):
    '''values      : values COMMA expression
                   | expression'''    
    if len(p) == 4:
        p[0] = p[1] + [p[3]]  # append two lists
    else:
        p[0] = [p[1]]       # create a list

def p_keys_list(p):
    '''keys        : keys COMMA expression KEY_OP expression
                   | expression KEY_OP expression'''
    if len(p) == 6:
        p[0] = p[1] + {p[3] : p[5]}  # append two lists
    else:
        p[0] = {p[1] : p[3]}       # create a list

#--[Flux]--

def p_flux(p):
    '''flux        : BREAK
                   | CONTINUE
                   | RETURN expression
                   | RETURN %prec EMPTY_RETURN'''
    if p[1] == 'return' and len(p) == 3:
        print('> return expr')
        p[0] = Node(typ='return', par=p[2])
    else:
        print('> ' + p[1])
        p[0] = Node(typ=p[1])

#--[Modulation--]

def p_modulation(p):
    '''modulation  : MODULE ID statements_suite END'''
    p[0] = Node(typ='module', par=None, sbg=Node(typ='list', par='sta', sbg=p[3]), sbd=p[2])

#--[Interfiles]--

def p_interfiles(p):
    '''interfiles  : REQUIRE STRING
                   | INCLUDE ID'''
    p[0] = Node(typ=p[1], par=p[2])

#--[Function definition]--

def p_definition(p):
    '''definition  : DEF ID LEFT_PAR parameters RIGHT_PAR statements_suite END
                   | DEF ID LEFT_PAR RIGHT_PAR statements_suite END'''
    if len(p) == 8:
        p[0] = Node(typ='function', par=Node(typ='list', par='id', sbg=p[4]), sbg=Node(typ='list', par='sta', sbg=p[6]), sbd=p[2])
    elif len(p) == 7:
        p[0] = Node(typ='function', par=None, sbg=Node(typ='list', par='sta', sbg=p[5]), sbd=p[2])

def p_parameters(p):
    '''parameters  : parameters COMMA ID
                   | ID'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]  # append two lists
    else:
        p[0] = [p[1]]       # create a list

#--[Class declaration]--

def p_declaration(p):
    '''declaration : CLASS ID LT ID statements_suite END
                   | CLASS ID statements_suite END'''
    if len(p) == 7:
        p[0] = Node(typ='class', par=p[4], sbg=Node(typ='list', par='sta', sbg=p[5]), sbd=p[2])
    else:
        p[0] = Node(typ='class', par=None, sbg=Node(typ='list', par='sta', sbg=p[3]), sbd=p[2])

#-------------------------------------------------------------------------------

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
