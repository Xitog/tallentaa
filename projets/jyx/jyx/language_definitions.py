import sys
sys.path.append('../../projet_language/rey')
from rey import LangageDefinition

#-----------------------------------------------------------
# C
#-----------------------------------------------------------

C = LangageDefinition()
C.NEWLINE = "New line"   
C.START_OF_ID = ['_']
C.START_OF_STRING = ['"', "'"]
C.END_OF_STRING = []
C.SEPARATORS = [
    '(', ')', '[', ']', '{', '}',
    '\n',
]
C.OPERATORS = [
    '+', '-', '*', '/', '%', '++', '--',
    '=', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>=',
    '==', '!=', '>', '>=', '<=', '<',
    'and', 'or', 'not',
    'not',
    '~', '&', '|', '^', '<<', '>>'
    '.', '->',
    '?', ':',
    '::',
    ',', ';'
]
C.KEYWORDS = [
    'auto', 'break', 'case', 'char', 'const', 'continue', 'default',
    'do', 'double', 'else', 'enum', 'extern', 'float', 'for', 'goto',
    'if', 'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof',
    'static', 'struct', 'switch', 'typedef', 'union', 'unsigned', 'void',
    'volatile', 'while', 'bool',
]
C.BOOLEANS = [
    'true',
    'false'
]

#-----------------------------------------------------------
# LUA
#-----------------------------------------------------------

#-----------------------------------------------------------
# REY
#-----------------------------------------------------------

REY = LangageDefinition()
REY.NEWLINE = "New line"   
REY.START_OF_ID = ['@', '_', '$']
REY.START_OF_STRING = ['"', "'"]
REY.END_OF_STRING = ['?', '!']
REY.SEPARATORS = [
    '(', ')', '[', ']', '{', '}',
    '\n',
] 
REY.OPERATORS = [
    '+', '-', '*', '/', '%', '**', '//',
    '=', '+=', '-=', '*=', '/=', '%=', '**=', '//=',
    '==', '!=', '>', '>=', '<=', '<', '<=>',
    'and', 'or', 'not', 'xor',
    'not', 'in',
    '.', '..', '..<',
    ':', '|', '->',
    '<<', '>>',
    ',', ';' # concat : , for expression, ; for statement
]
REY.KEYWORDS = [
    'if', 'unless', 'then', 'elif', 'else', 'end',
    'while', 'until', 'do',
    'for', 'in',
    'break', 'next',
    'new',
    'fun', 'sub', 'get', 'set',
    'return',
    'class'
]
REY.BOOLEANS = [
    'true',
    'false'
]
REY.BLOCK_PLUS = [ 'if', 'for', 'while', 'fun', 'sub', 'get', 'set', 'class' ]
REY.BLOCK_LESS = [ 'end' ]
REY.LINE_LESS =  [ 'elif' ]
