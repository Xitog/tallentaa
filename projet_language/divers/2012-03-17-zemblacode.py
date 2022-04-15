a = "2 + 2 * 3 - 2" # marche si on enleve le -2 IL FAUT CONSTRUIRE EN RECURSIF EN PARTANT DU PLUS BAS POUR FAIRE UN ARBRE !!! STOCKABLE EN PILE...

class TokenType:
    def __init__(self, name, check):
        self.name = name
        self.check = check
    def is_a(self, value):
        if value in self.check:
            return True
    def __str__(self):
        return self.name

class Token:
    def __init__(self, value, type):
        self.value = value
        self.type = type
    def __str__(self):
        return "(%s)<%s>" % (self.value, self.type)

elements = a.split(' ')

Integer = TokenType('int', ('2','3'))
Operator = TokenType('bin_op', ('+','*','-'))

types = [Integer, Operator]
tokens = []

for e in elements:
    #print e
    # get type
    ty = None
    for t in types:
        if t.is_a(e):
            if ty == None:
                ty = t
            else:
                raise Exception("Two types are OK!")
    if ty == None:
        raise Exception("Not type found!")
    tokens.append(Token(e,ty))

for t in tokens:
    print t

prop = { '+' : 2, '-' : 2, '*' : 3 }
toks = tokens[:]
pile = []
while len(toks) > 0:
    do = None
    for i in range(0,len(toks)):
        t = toks[i]
        if t.type.name == 'bin_op':
            print "aaa: ", t
            if do is None:
                do = i
            elif prop[toks[do].value] < prop[t.value]:
                do = i
    print 'choose: ', toks[do], do
    if do-1 >= 0: pile.append(toks[do-1])
    if do+1 < len(toks): pile.append(toks[do+1])
    pile.append(toks[do])
    del toks[do-1:do+2]
    print('---tokens left---')    
    for t in toks:
        print t

def pp(pile):
    print('pile (%d):' % (len(pile),))
    i=0
    for p in pile:
        print i, '. ', p
        i+=1

pp(pile)

def send_integer(message, args):
    if message == '*':
        return args[0]*args[1]
    elif message == '+':
        return args[0]+args[1]
    elif message == '-':
        return args[0]-args[1]

# Interpreter
r = 0
counter = 0
while len(pile) > 0 and counter < len(pile):
    t = pile[counter]
    if t.type.name == 'int':
        counter += 1
    elif t.value == '*':
        r = int(pile[0].value)*int(pile[1].value)
        del pile[0:3]
        pile.insert(0, Token(r,Integer))
        counter=0
    elif t.value == '+':
        r = int(pile[0].value)+int(pile[1].value)
        del pile[0:3]
        pile.insert(0, Token(r,Integer))
        counter=0
    pp(pile)
    print '---', counter, '---'
    #raw_input()

if len(pile) == 1:
    print 'youpi'
    print pile[0]
    print(eval(a))
    if eval(a) == pile[0].value: print('Match')
    else: print('err')

"""
on = 0
state = None
pile = []
for i in range(0, len(tokens)):
    t = tokens[i]
    last = (i == len(tokens)-1)
    if i == 0:
        if t.type.name == 'int':
            if last:
                state = ['<integer>']
                pile.append(t)
            elif tokens[i+1].type.name == 'binop':
                state = ['<bin_expr']
                pile.append(t)
                pile.append(tokens[i+1])
                i += 1
            else:
                state = 'Syntax Error'
                on = i+1           
    elif state == 'bin_expr': # l'op est dans la pile
        pile.append(t)
        if not last:
            if tokens[i+1].type == 'int':
                pass
            else:
                state = 'Syntax Error'
                on = i+1
    if state == 'Syntax Error':
        break
if state == 'Syntax Error':
    print ("Syntax Error on %s" % (on,))
else:
    print state
"""

