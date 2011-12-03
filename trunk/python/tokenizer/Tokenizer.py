# 15h39-42. OK

s = "a = 5; b = 2; c = a * -b+1; writeln(c) #pipo; 11+1 .4 2.3.alpha 5..alpha"

def is_lower_char(c):
    return (c in ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'])

def is_upper_char(c):
    return (c in ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'])   

def is_char(c):
    return (is_lower_char(c) or is_upper_char(c))

def is_digit(c):
    return (c in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])

def is_hexadigit(c):
    return (is_digit(c) or (c in ['A', 'B', 'C', 'D', 'E', 'F']))

def is_ops_char(c):
    return (c in ['+', '-', '/', '*', '%', '>', '<', '=', '!', '&', '^', '|'])

def is_sep_char(c):
    return (c in [';', '(', ')', '[', ']', '{', '}', '\n'])

def is_silent(c):
    return (c in [' ', '\t'])

def is_operator(s):
    return (s in ['+', '-', '/', '*', '//', '**', '%', '>', '>=', '==', '!=', '<=', '<', '!', '&', '^', '|', '=', '+=', '-=', '/=', '//=', '*=', '**=', '%='])

def is_keyword(s):
    return (s in ['if', 'then', 'else', 'elsif', 'end', 'while', 'do', 'end', 'until', 'unless', 'break', 'next', 'return'])

escape = False
state = 'start'
i = 0
c = s[i]
curr = []
tokens = []

class Token:
    def __init__(self, kind, val):
        self.kind = kind
        self.val = val
    def __str__(self):
        return 'Token: %s : %s' % (self.val, self.kind)

def next():
    global s, i, c, escape
    i+=1
    if i < len(s):
        c = s[i]
    else:
        c = '\0'

def token(t):
    global curr, state
    #print 'Token!', ''.join(curr), 'of type', t
    tokens.append(Token(t, ''.join(curr)))
    curr = []
    state = 'start'

while not escape:
    if c == '\0': # last turn
        escape = True
    if state == 'start':
        if is_char(c) or c == '$' or c == '@' or c == '_':
            state = 'id'
            #
            curr.append(c)
            next()
        elif is_digit(c):
            state = 'integer'
            #
            curr.append(c)
            next()
        elif c == '.': # '.' can be for a float or an operator
            state = 'float'
            #
            curr.append(c)
            next()
        elif is_ops_char(c):
            state = 'operator'
            #
            curr.append(c)
            next()
        elif is_sep_char(c):
            curr.append(c)
            next()
            token('separator')
        elif c == '#':
            end = False
            while (not escape) and (not end):
                next()
                if c == ';' or c == '\n':
                    end = True
        elif is_silent(c):
            next()
        else:
            print 'Forbidden character: ', c
    elif state == 'id':
        if (is_char(c) or is_digit(c) or c == '_') or (c == '@' and len(curr) == 1):
            curr.append(c)
            next()
        else:
            if is_keyword(''.join(c)):
                token('keyword')
            else:
                token('id')
    elif state == 'integer':
        if is_digit(c):
            curr.append(c)
            next()
        elif c == '.':
            state = 'float'
            curr.append(c)
            next()
        else:
            token('integer')
    elif state == 'float':
        if is_digit(c):
            curr.append(c)
            next()
        elif len(curr) == 1: # We have a lonely '.'
            token('operator')        
        else:
            token('float')
    elif state == 'operator':
        if is_ops_char(c) and is_operator((''.join(curr))+c):
            curr.append(c)
            next()
        else:
            token('operator')

for t in tokens:
    print t

