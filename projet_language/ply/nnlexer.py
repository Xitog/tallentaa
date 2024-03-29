import lex 
 
# Arithmetique Op 
t_ADD     = r'\+' 
t_MIN     = r'-' 
t_MUL     = r'\*' 
t_DIV     = r'/' 
t_DIV_INT = r'//' 
t_POW     = r'\*\*' 
t_MOD     = r'%' 
t_LSHIFT  = r'<<'

# Boolean Op 
t_AND     = r'and' 
t_OR      = r'or' 
t_NOT     = r'not' 
 
# Affectation Op 
t_AFFECT  = r'=' 
t_ADD_AFF = r'\+=' 
t_MIN_AFF = r'-=' 
t_MUL_AFF = r'\*=' 
t_DIV_AFF = r'/=' 
t_MOD_AFF = r'%=' 
t_DIV_INT_AFF = r'//=' 
t_POW_AFF = r'\*\*=' 
 
# Comparison Op 
t_EQ = r'==' 
t_NE = r'!=' 
t_GT = r'>' 
t_GE = r'>=' 
t_LT = r'<' 
t_LE = r'<=' 
 
# Special Op 
t_KEY_OP = r'=>' 
 
# Delimiteurs 
t_LEFT_PAR    = r'\(' 
t_RIGHT_PAR   = r'\)' 
t_LEFT_SB     = r'\[' 
t_RIGHT_SB    = r'\]' 
t_LEFT_CB     = r'{' 
t_RIGHT_CB    = r'}' 
t_SEMI        = r';' 
t_COMMA       = r',' 
t_DOT         = r'\.' 
 
# Statement flow control 
t_IF      = r'if' 
t_WHILE   = r'while' 
t_ELSE    = r'else' 
#t_VAR     = r'var' 
t_THEN    = r'then' 
t_END     = r'end' 
#t_PASS    = r'pass' 
t_DO      = r'do' 
t_BREAK   = r'break' 
t_FOR     = r'for' 
t_IN      = r'in' 
t_UNLESS  = r'unless' 
t_DEF     = r'def' 
t_REQUIRE = r'require' 
t_INCLUDE = r'include' 
t_NEXT    = r'next' 
t_MODULE  = r'module' 
t_RETURN  = r'return' 
t_CLASS   = r'class' 
t_TRUE    = r'true' 
t_FALSE   = r'false' 
t_NIL     = r'nil' 
t_ELSIF   = r'elsif' 
 
# keywords 
keywords  = ('IF', 'WHILE', 'ELSE', 'THEN', 'END', 'AND', 'OR', 'NOT', 'TRUE', 'FALSE', 'NIL', 'DO', 'BREAK', 'FOR', 'IN', 'UNLESS', 'DEF', 'REQUIRE', 'INCLUDE','NEXT','MODULE','RETURN','CLASS', 'ELSIF') # 'VAR' 
symbols   = ('LEFT_PAR', 'RIGHT_PAR', 'LEFT_SB', 'RIGHT_SB', 'LEFT_CB', 'RIGHT_CB', 'SEMI', 'COMMA', 'DOT') 
operators = ('ADD', 'MIN', 'MUL', 'DIV', 'DIV_INT', 'POW', 'MOD', 'AFFECT', 'ADD_AFF', 'MUL_AFF', 'MIN_AFF', 'MOD_AFF', 'DIV_AFF', 'DIV_INT_AFF', 'EQ', 'NE', 'LE', 'LT', 'GE', 'GT', 'KEY_OP','POW_AFF','LSHIFT') 
types     = ('FLOAT', 'INT', 'STRING', 'ID') 
tokens    = keywords + symbols + operators + types + ('COMMENT', 'NEWLINE') 
 
def t_ID(t): 
    r'[a-zA-Z_][0-9a-zA-Z_]*(\?|\!)?' 
    #global lineno 
    if t.value.upper() in keywords: 
        t.type = t.value.upper() 
    return t 
 
# Bien mettre Float avant Int ! 
def t_FLOAT(t): 
    r'(\d*\.\d+)|(\d+\.\d*)' 
    #r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))' 
    t.value = float(t.value) 
    return t 
 
def t_INT(t): 
    r'\d+|0x[0-9a-fA-F]+|0b[0-1]+' 
    t.value = int(t.value) 
    return t 
 
def t_STRING(t): 
    r"""(\'\'\'.*?\'\'\')|(\".*?\")|(\'.*?\')""" 
    if len(t.value) >= 6 and t.value[0:3] == "'''" and t.value[len(t.value)-3:len(t.value)] == "'''": 
        t.value = t.value[3:len(t.value)-3] 
    else: 
        t.value = t.value[1:len(t.value)-1] 
    return t 
 
def t_COMMENT(t): 
    r'\#.*' 
    #return t 

lineno = 0 
 
def t_NEWLINE(t): 
    r'\n' 
    global lineno 
    lineno += 1 
    t.lexer.lineno += 1 #lineno 
    return t 
 
t_ignore = ' \t' 
 
def t_error(t): 
    print("Illegal character %s" % t.value[0]) 
    t.lexer.skip(1) 
 
lex.lex() 
 
 
# re.end() == len(s) pour les matchs !!! 
# truepipo sera vrai sinon alors que on veut que 
# true(FIN) 
 
# *? non-greedy version
