# 16h54 : correction du bug 2..abs et 2.abs.

import re           # for Lexer

#-----------------------------------------------------------------------
# Tools
#-----------------------------------------------------------------------

class Enum:
    def __init__(self, *tab):
        self.tab = tab
        i = 0
        for t in tab:
            setattr(self, t, t)

TokenType = Enum('integer', 'float', 'id', 'operator', 'separator','keyword', 'eof', 'boolean', 'string', 'discard', 'warning')

#-----------------------------------------------------------------------
# Lexer
#-----------------------------------------------------------------------

tokens = [
    
    ('".*"', TokenType.string),
    ("'.*'", TokenType.string),
    
    ('0(b|B)[0-1]*' , TokenType.integer),
    ('0(x|X)[0-9A-Fa-f]*' , TokenType.integer),
    ('0(c|C)[0-7]*' , TokenType.integer),
    ('[0-9]+', TokenType.integer),     #[0-9]+(?![a-zA-Z_])
    
    ('[0-9]*\.[0-9]+' , TokenType.float),
    ('[0-9]+\.[0-9]*' , TokenType.float),
    ('\.[0-9]+' , TokenType.float),

    ('[0-9]+\.[a-zA-Z]+', TokenType.warning),
    
    (';' , TokenType.separator),
    ('\(' , TokenType.separator),
    ('\)' , TokenType.separator),
    ('\[' , TokenType.separator),
    ('\]' , TokenType.separator),
    ('\{' , TokenType.separator),
    ('\}' , TokenType.separator),
    ('\n' , TokenType.separator),
    (',' , TokenType.separator),
    
    ('=' , TokenType.operator),
    ('\+=' , TokenType.operator),
    ('-=' , TokenType.operator),
    ('/=' , TokenType.operator),
    ('//=' , TokenType.operator),
    ('\*=' , TokenType.operator),
    ('\*\*=' , TokenType.operator),
    ('%=' , TokenType.operator),
    ('->' , TokenType.operator),
    
    ('\+' , TokenType.operator),
    ('-' , TokenType.operator),
    ('/' , TokenType.operator),
    ('\*' , TokenType.operator),
    ('//' , TokenType.operator),
    ('\*\*' , TokenType.operator),
    ('%' , TokenType.operator),
    
    ('>' , TokenType.operator),
    ('>=' , TokenType.operator),
    ('==' , TokenType.operator),
    ('!=' , TokenType.operator),
    ('<=' , TokenType.operator),
    ('<' , TokenType.operator),
    
    ('!' , TokenType.operator),
    ('&' , TokenType.operator),
    ('\^' , TokenType.operator), 
    ('\|' , TokenType.operator),
    
    ('\.' , TokenType.operator),
    
    ('true' , TokenType.boolean),
    ('false' , TokenType.boolean),
    
    ('if' , TokenType.keyword),
    ('then' , TokenType.keyword),
    ('else' , TokenType.keyword),
    ('elsif' , TokenType.keyword),
    ('end' , TokenType.keyword),
    ('while' , TokenType.keyword),
    ('do' , TokenType.keyword),
    ('until' , TokenType.keyword),
    ('unless' , TokenType.keyword),
    ('break' , TokenType.keyword),
    ('next' , TokenType.keyword),
    ('return' , TokenType.keyword),
    ('fun' , TokenType.keyword),
    ('class' , TokenType.keyword),

    (' ', TokenType.discard),
    ('\t', TokenType.discard),
    ('\n', TokenType.discard),
    
    ('[a-zA-Z_][a-zA-Z0-9_]*(\?|!)?', TokenType.id),
]

class Token:
    def __init__(self, kind, val):
        self.kind = kind
        self.val = val
    
    def __str__(self):
        return 'Token(%s, %s)' % (self.val, self.kind)

class Tokenizer:
    def __init__(self):
        global tokens
        self.tokens = tokens
    
    def parse(self, input):
        input += '\0'
        output = []
        current = ''
        previous = None
        i = 0
        while i < len(input):
            current += input[i]
            found = False
            #print '-------------------------------------[', current, '] (', len(current), ')' 
            for tok in self.tokens:
                #print tok[0]
                r = re.match(tok[0], current)
                if r is not None and r.end() == len(current):
                    #print 'found!', tok[1]
                    previous = tok[1]
                    found = True
                    break
            if not found:
                if previous is not None:
                    if previous != TokenType.discard:
                        if previous != TokenType.warning:
                            output.append(Token(previous, current[:len(current)-1]))
                        else:
                            num,name = current[:len(current)-1].split('.')
                            output.append(Token(TokenType.integer, num))
                            output.append(Token(TokenType.operator, '.'))
                            output.append(Token(TokenType.id, name))
                    current = ''
                    previous = None
                    i-=1
                else:
                    pass # not enough caracter to decide
            else:
                pass # we found at least one matching tokens
            i+=1
        output.append(Token(TokenType.eof, 'eof'))
        return output

t = Tokenizer()
s = "2.0 * (-3.abs + 2..abs)"
print 'solve: %s' % (s,)
o = t.parse(s)
for e in o:
    print e

