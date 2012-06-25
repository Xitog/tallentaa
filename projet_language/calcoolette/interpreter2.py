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

TokenType = Enum('integer', 'float', 'id', 'operator', 'separator','keyword', 'eof', 'boolean', 'string', 'discard', 'warning', 'invisible')

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
"""
t = Tokenizer()
s = "2.0 * (-(2+1).abs + 2..abs) + a"
print 'solve: %s' % (s,)
o = t.parse(s)
i = 0
for e in o:
    print '%d. %s' % (i, str(e))
    i+=1
"""

class Value:
    def __init__(self, typ, val):
        self.typ = typ
        self.val = val

class Reference:
    def __init__(self, typ, nam, val, frozen_typ = False, frozen_val = False):
        self.typ = typ
        self.nam = nam
        self.val = val
        self.frozen_typ = frozen_typ
        self.frozen_val = frozen_val

class ExpressionHandler:
    def __init__(self):
        pass
    
    def fetch_next_sep(self, sep, lvl, tokens):
        i = 0
        while i < len(tokens):
            t = tokens[i]
            if t.val == sep: lvl+=1
            if sep == '(' and t.val == ')': lvl-=1
            if lvl == 0: break
            i+=1
        if lvl==0:
            return i
        else:
            raise Exception('Parenthezis not closed')
    
    def make_tree(self, tokens, context):
        expr = []        
        i = 0
        while i < len(tokens):
            t = tokens[i]
            if t.kind == TokenType.separator and t.val == '(':
                last = self.fetch_next_sep('(', 0, tokens[i:]) + i + 1
                #for j in tokens[i:last]:
                #    print 'sub from %d to %d : %s' % (i, last, str(j))
                expr.append(self.make_tree(tokens[i+1:last-1], context))
                # 
                #
                print '---'
                best = -1
                j = i+1
                while j < last-1:
                    print tokens[j]
                    if best > -1 and tokens[best].val == '+' and tokens[j] == '*':
                        best = j
                    elif best == -1 and tokens[j].val in ['+','-','/','*','**','%','.']:
                        best = j
                    j+=1
                print '---[%d]' % (best-i-1,)
                #                
                i = last
            else:
                expr.append(t)
                i+=1
        return expr
    
    def execute(self, tree, context):
        pass

#------------------------------------------------------------------------------

# unary minus ok. un peu avant.
# fun without param ok. 17h10
# 17h18 : abs (int, float) trunc, round (float) (15 : fonction ok, 18 : fonction typee)
# 17h12 : ok. It's simple, but it works.
# afaire : gestion parentheses !!!

# 11h24 : parentheses : OK OK OK pour (2+3)*2 et 2*(2+3) et aussi call(X)
# un "call" node peut etre membre d'un unprefixed_call node ou bien d'un prefixed_call.
# 12h17 : 3.add(2)... MARCHE ! Sniff... I never went so far away !

class Node:
    def __init__(self, left, right, middle):
        self.left = left
        self.right = right
        self.middle = middle

    def __str__(self):
        return "%s--%s--%s" % (self.left, self.middle, self.right)

# Fetch the operator to execute
def first_op(tokens):
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if isinstance(tok, Token):
            if tok.val == '-' and (i == 0 or tokens[i-1].kind == TokenType.operator):
                tok.val = 'unary-'
            if tok.val == '(' and i > 0 and tokens[i-1].kind != TokenType.operator:
                tok.val = 'call('
            elif tok.val == '(':
                tok.val = 'expr('
        i+=1
    i = 0
    best = -1
    best_prio = -1
    prio = { ')' : 0, '+' : 10, '-' : 10, '*' : 20, '/' : 20, '**' : 30, '%' : 30, 'call' : 35,
            '.' : 40, 'unary-' : 50, 'call(' : 51, 'expr(' : 60 }
    lvl = 1
    while i < len(tokens):
        tok = tokens[i]
        if isinstance(tok, Token) and tok.kind in [TokenType.operator, TokenType.separator]:
            if best == -1:
                best = i
                best_prio = prio[tok.val]*lvl
            else:
                if prio[tok.val]*lvl > best_prio:
                    best = i
                    best_prio = prio[tok.val]*lvl
            # () for others
            if tok.val == '(':
                lvl*=10
            elif tok.val == ')':
                lvl/=10
        elif isinstance(tok, Node) and tok.middle == 'call':
            if prio[tok.middle]*lvl > best_prio:
                best = i
                best_prio = prio[tok.middle]*lvl
        i+=1
    return best

def fetch_closing(sep, tokens, i):
    lvl = 0
    pos = 0
    pos = i
    while pos < len(tokens):
        tok = tokens[pos]
        if sep == '(' and tok.val in ['call(', 'expr(']: lvl += 1
        elif sep == '(' and tok.val == ')': lvl -= 1
        if lvl == 0: break
        pos+=1
    if lvl != 0: raise Exception("Incorrect expression ()")
    return pos

def global_function(id, args):
    #print id
    #print args
    if isinstance(id, Token) and id.kind == TokenType.id and isinstance(args, Node) and args.middle == 'call':
        if id.val == 'println':
            if isinstance(args.right, Token):
                print exec_node(args.right)
                return None
    else:
        raise Exception("Bad global function call")

def instance_function(id, args):
    #print id
    #print args
    if isinstance(id, Token) and id.kind in [TokenType.integer, TokenType.float]:
        val_left = exec_node(id)
        if isinstance(args, Node) and args.middle == 'call':
            if isinstance(args.left, Token) and args.left.kind == TokenType.id:
                if args.left.val == 'add':
                    if isinstance(args.right, Token):
                        val_par = exec_node(args.right)
                        return val_left + val_par
        else:
            raise Exception("Bad instance function call")

def not_exist_or_dif(tokens, index, kind, value):
    if len(tokens) <= index: return True
    if not isinstance(tokens[index], kind): return True
    if kind == Node and tokens[index].middle != value: return True
    if kind == Token and tokens[index].kind != value: return True
    return False

# From a token list make a tree!
def make_tree(tokens):
    while len(tokens) > 1:    
        target = first_op(tokens)
        #print '>>> target=%i %s' % (target, tokens[target])
        if isinstance(tokens[target], Node):
            if tokens[target].middle == 'call':
                id = tokens[target-1]
                if isinstance(id, Token) and id.kind == TokenType.id:
                    n = Node(left=id, right=tokens[target], middle=Token(TokenType.invisible, 'unprefixed_call'))
                    del tokens[target]
                    tokens[target-1] = n
                else:
                    raise Exception("Call not understood")
            else:
                raise Exception("Error on target node")
        elif isinstance(tokens[target], Token):
            if tokens[target].val == 'unary-':        
                n = Node(left=None, right=tokens[target+1], middle=tokens[target])
                del tokens[target+1]
                tokens[target] = n
            elif tokens[target].val == 'expr(':
                fin = fetch_closing('(', tokens, target)
                sub = tokens[target+1:fin]
                make_tree(sub)
                jj = fin
                while jj > target:
                    del tokens[jj]
                    jj -= 1
                tokens[target] = sub[0]
            elif tokens[target].val == 'call(':
                fin = fetch_closing('(', tokens, target)
                sub = tokens[target+1:fin]
                make_tree(sub)
                jj = fin
                while jj > target:
                    del tokens[jj]
                    jj -= 1
                tokens[target] = Node(left=None, right=sub[0], middle='call')
            elif target > 0:
                if tokens[target].val != '.' or (tokens[target].val == '.' and not_exist_or_dif(tokens, target+2, Node, "call")):
                    n = Node(left=tokens[target-1], right=tokens[target+1], middle=tokens[target])
                    del tokens[target+1]
                    del tokens[target]
                    tokens[target-1] = n
                else:
                    # nx -> fun, call (avec par)
                    nx = tokens[target+2]
                    nx.left = tokens[target+1]
                    # n -> id, nx
                    n = Node(left=tokens[target-1], right=nx, middle=Token(TokenType.invisible, "prefixed_call"))
                    del tokens[target+2]
                    del tokens[target+1]
                    del tokens[target]
                    tokens[target-1] = n
            elif target == -1 and len(tokens) > 0:
                n = tokens[0]
        else:
            print tokens[target]
            raise Exception("Expression not understood")
        
        #for t in tokens:
        #    print t
        #print "length=%d" % (len(tokens),)
        #raw_input()
        
def exec_node(n):
    if isinstance(n, Node):
        if n.middle.kind == TokenType.operator:
            if n.middle.val == '+':
                return exec_node(n.left) + exec_node(n.right)
            elif n.middle.val == '-':
                return exec_node(n.left) - exec_node(n.right)
            elif n.middle.val == '*':
                return exec_node(n.left) * exec_node(n.right)
            elif n.middle.val == '/':
                return exec_node(n.left) / exec_node(n.right)
            elif n.middle.val == '%':
                return exec_node(n.left) % exec_node(n.right)
            elif n.middle.val == '**':
                return exec_node(n.left) ** exec_node(n.right)
            elif n.middle.val == 'unary-':
                return -exec_node(n.right)
            elif n.middle.val == '.':
                if n.right.val == 'abs':
                    value = exec_node(n.left)
                    if isinstance(value, int) or isinstance(value, float):
                        return abs(value)
                    else:
                        raise Exception("Wrong type for function abs")
                elif n.right.val == 'round':
                    value = exec_node(n.left)
                    if isinstance(value, float):
                        return round(value)
                    else:
                        raise Exception("Wrong type for function round")
                elif n.right.val == 'trunc':
                    value = exec_node(n.left)
                    if isinstance(value, float):
                        return float(int(value))
                    else:
                        raise Exception("Wrong type for function trunc")
            else:
                raise Exception("Operator not understood")
        elif n.middle.kind == TokenType.invisible:
            if n.middle.val == 'unprefixed_call':
                return global_function(n.left, n.right)
            elif n.middle.val == 'prefixed_call':
                return instance_function(n.left, n.right)
        else:
            print n.left
            print n.middle
            print n.right
            raise Exception("Node type not understood")
    elif isinstance(n, Token):
        if n.kind == TokenType.integer:
            return int(n.val)
        elif n.kind == TokenType.float:
            return float(n.val)
        else:
            raise Exception("TokenType not understood")
    else:
        print n.__class__
        print n
        raise Exception("Node not known")

def test(s):
    #print '--------------------------------------'
    #print s
    #print '---'
    t = Tokenizer()
    o = t.parse(s)
    i = 0
    #for e in o:
    #    print '%d. %s' % (i, str(e))
    #    i+=1
    del o[-1] # del eof
    #print '>>> %i %s' % (first_op(o), o[first_op(o)])
    make_tree(o)
    print "for: %s \t res = %s" % (s, str(exec_node(o[0])))

test("2+3")         # 5
test("2**3")        # 8
test("8%2")         # 0
test("2+3*2")       # 8
test("-2+3")        # 1
test("-3")          # -3
test("5+-4")        # 1
test("-7.abs")      # 7
test("-8..abs")     # 8.0
test("8.5.round")   # 9.0
test("8.4.round")   # 8.0
test("6.5.trunc")   # 6.0
test("1..trunc")    # 1.0 
test("2 * ( 3 + 1)")  # 8
test("(3 + 1) * 2")   # 8
test("println(4)")    #
test("3.add(2)")    # 

"""
val_abs = Value('fun', abs)
val_1   = Value('int', 1)
ref_abs = Reference('fun', 'abs', val_abs)
ref_a   = Reference('int', 'a', val_1)
scope = { 'abs' : ref_abs, 'a' : ref_a }

ett = ExpressionHandler()
tree = ett.make_tree(o, scope)

def mksp(lvl):
    return "    " * lvl

def display (t,lvl=-1):
    if isinstance(t, list):
        for e in t:
            display(e,lvl+1)
    else:
        print "%s%s" % (mksp(lvl), str(t))

display(tree)

out = ett.execute(tree, scope)
"""

