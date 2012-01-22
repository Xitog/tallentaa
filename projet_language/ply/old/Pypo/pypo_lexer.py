import lex

# Arborix lexers

# Arithmetique Op
t_ADD    = r'\+'
t_MIN    = r'-'
t_MUL    = r'\*'
t_DIV    = r'/'
t_INTDIV = r'//'
t_POW    = r'\*\*'
t_MOD    = r'%'

# Boolean Op
t_AND    = r'and'
t_OR     = r'or'
t_NOT    = r'not'

# Affectation Op
t_AFFECT  = r'='
t_ADD_AFF = r'\+='
t_MIN_AFF = r'-='
t_MUL_AFF = r'\*='
t_DIV_AFF = r'/='
t_MOD_AFF = r'%='
t_IDV_AFF = r'//='

# Comparison Op
t_EQ = r'=='
t_NE = r'!='
t_GT = r'>'
t_GE = r'>='
t_LT = r'<'
t_LE = r'<='

# Delimiteurs
t_OPEN_PAR    = r'\('
t_CLOSING_PAR = r'\)'
t_OPEN_SB     = r'\['
t_CLOSING_SB  = r'\]'
t_SEMI        = r';'
t_COMMA       = r','

# Statement flow control
t_IF    = r'if'
t_WHILE = r'while'
t_ELSE  = r'else'
t_VAR   = r'var'
t_THEN  = r'then'
t_END   = r'end'
t_PASS  = r'pass'
t_DO    = r'do'

# keywords
keywords  = ('IF', 'WHILE', 'ELSE', 'VAR', 'THEN', 'END', 'PASS', 'AND', 'OR', 'NOT', 'TRUE', 'FALSE', 'NIL', 'DO')
symbols   = ('OPEN_PAR', 'CLOSING_PAR', 'OPEN_SB', 'CLOSING_SB', 'SEMI', 'COMMA')
operators = ('ADD', 'MIN', 'MUL', 'DIV', 'INTDIV', 'POW', 'MOD', 'AFFECT', 'ADD_AFF', 'MUL_AFF', 'MIN_AFF', 'MOD_AFF', 'DIV_AFF', 'IDV_AFF', 'EQ', 'NE', 'LE', 'LT', 'GE', 'GT')
types     = ('FLOAT', 'INT', 'STRING', 'BOOL', 'ID')
tokens    = keywords + symbols + operators + types + ('COMMENT', 'NEWLINE')

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
    #global lineno
    if t.value.upper() in keywords:
        if t.value.upper() in ('TRUE', 'FAlSE', 'NIL'):
            t.type = t.value.capitalize()
        else:
            t.type = t.value.upper()
    #t.lexer.lineno = lineno
    return t

def t_STRING(t):
    r'\".*?\"'
    t.value = t.value[1:len(t.value)-1]
    return t

def t_COMMENT(t):
    r'\# .*'
    #return t

#lineno = 0

def t_NEWLINE(t):
    r'\n'
    global lineno
    #lineno += 1
    t.lexer.lineno += 1 #lineno
    #return t

t_ignore = ' \t'

def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)

lex.lex()


# re.end() == len(s) pour les matchs !!!
# truepipo sera vrai sinon alors que on veut que
# true(FIN)

# *? non-greedy version
