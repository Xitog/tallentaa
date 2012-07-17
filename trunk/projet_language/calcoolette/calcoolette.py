#-----------------------------------------------------------------------
# Base
#-----------------------------------------------------------------------

class SymbolType:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name

Integer     = SymbolType('Integer')
Float       = SymbolType('Float')
Id          = SymbolType('Id')
Operator    = SymbolType('Operator')
Separator   = SymbolType('Separator')
Keyword     = SymbolType('Keyword')
EOF         = SymbolType('EOF')
Boolean     = SymbolType('Boolean')
String      = SymbolType('String')
Discard     = SymbolType('Discard')
Error       = SymbolType('Error')
Structure   = SymbolType('Structure')

class Symbol:
    def __init__(self, kind, val, left=None, right=None):
        self.val = val
        self.kind = kind
        self.left = left
        self.right = right
    def __str__(self):
        if self.left is None and self.right is None:
            return "%s:%s" % (self.val, self.kind)
        else:
            return "%s--%s:%s--%s" % (self.left, self.val, self.kind, self.right)
    def terminal(self):
        return self.left is None and self.right is None

class SymbolList:
    def __init__(self, tokens=[]):
        self.core = tokens
    
    def clear(self):
        i = len(self.core)-1
        while i >= 0:
            del self.core[i]
            i-=1
    
    def __call__(self, index):
        return self.core[index]
    
    def __getitem__(self, index):
        return self.core[index]
    
    def __setitem__(self, index, val):
        self.core[index] = val
        return val
    
    def __delitem__(self, index):
        del self.core[index]
    
    def add(self, tok):
        self.core.append(tok)
    
    def to_a(self):
        return self.core
    
    def from_a(self, tokens):
        self.core = tokens
    
    def include(self, val):
        i = 0
        for t in self.core:
            if t.val == val:
                return i
            i+=1
        return False
    
    def split(self, val):
        index = self.include(val)
        right = []
        left = []
        i = 0
        for t in self.core:
            if i < index:
                right.append(t)
            elif i > index:
                left.append(t)
            i+=1
        return right, left
    
    def __len__(self):
        return len(self.core)

#-----------------------------------------------------------------------
# Lexical analysis
#-----------------------------------------------------------------------

symbols = [
    
    ('".*"', String),
    ("'.*'", String),
    
    ('0(b|B)[0-1]*' , Integer),
    ('0(x|X)[0-9A-Fa-f]*' , Integer),
    ('0(c|C)[0-7]*' , Integer),
    
    ('[0-9]*\.[0-9]+' , Float),
    ('[0-9]+\.[0-9]*' , Float),
    ('\.[0-9]+' , Float),
    
    ('\[' , Separator),
    ('\]' , Separator),
    ('\{' , Separator),
    ('\}' , Separator),
    ('\n' , Separator),
    (',' , Separator),
    
    ('=' , Operator),
    ('\+=' , Operator),
    ('-=' , Operator),
    ('/=' , Operator),
    ('//=' , Operator),
    ('\*=' , Operator),
    ('\*\*=' , Operator),
    ('%=' , Operator),
    ('->' , Operator),
    
    #('!' , Operator),
    #('&' , Operator),
    #('\^' , Operator), 
    #('\|' , Operator),
    
    ('[a-zA-Z_][a-zA-Z0-9_]*(\?|!)?', Id),
]

digits = ['0','1','2','3','4','5','6','7','8','9']
alphas = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
          'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '_']
ops = ['+', '-', '*', '/', '**', '%', '.', '<', '>', '!', '=']
white = [' ', '\n', '\t']
operators = ['+', '-', '*', '/', '**', '%', '.', '<', '<<', '<=', '>', '>>', '>=', '!=', '==', '<=>', '=']
separators = ['(', ')', ';', ',']
id_booleans = ['true', 'True', 'False', 'false']
id_operators = ['and', 'xor', 'or']
id_keywords = ['class', 'fun', 'return', 'next', 'break', 'unless', 'until', 'do', 'while', 'end', 'elsif', 'else', 'then', 'if', 'module']
spe = ['$', '?']

class Symbolizer:
    
    def __init__(self):
        pass
        self.symbols = []
    
    def parse(self, input):
        self.symbols = []
        START = 0
        mode = START
        i = 0
        while i < len(input):
            #print '> char at : ', input[i]
            #print '> index   : ', i
            #raw_input()
            if input[i] in digits: i=self.parse_num(input, i)
            elif input[i] in alphas: i=self.parse_id(input, i)
            elif input[i] in ops: i=self.parse_op(input, i)
            elif input[i] in white: i+=1
            elif input[i] in separators:
                self.symbols.append(Symbol(Separator, input[i]))
                i+=1
            else: raise Exception("Char incorrect %s at %s" % (input[i], i))
        self.symbols.append(Symbol(EOF, 'eof'))
        return SymbolList(self.symbols)
    
    def parse_num(self, input, i):
        global digits, alphas
        #print '> parse num'
        float = False
        num = input[i]
        i+=1
        cont = True
        while i < len(input) and cont:
            #print '> ', i
            if input[i] in digits:
                #print 'go on num'
                num += input[i]
                i+=1
            elif input[i] == '.' and not float and i+1 < len(input) and input[i+1] in digits:
                float = True
                num += input[i]
                i+=1
            elif input[i] == '.' and not float and i+1 < len(input) and input[i+1] == '.':
                float = True
                num += input[i]
                i+=1
                cont = False
            elif input[i] in alphas:
                raise Exception("Incorrect Id starting with numbers")
            else:
                #print 'end num'
                cont = False
        if not float:
            self.symbols.append(Symbol(Integer, num))
        else:
            self.symbols.append(Symbol(Float, num))
        return i
    
    def parse_id(self, input, i):
        global alphas, digits
        #print '> parse id'
        id = input[i]
        i+=1
        cont = True
        while i < len(input) and cont:
            #print '> ', i
            if input[i] in alphas or input[i] in digits:
                id+=input[i]
                i+=1
            # si i == $ ou ? et que c le dernier ou que i+1 != digits et i+1 != alphas alors
            elif input[i] in spe and (i == len(input)-1 or (not input[i+1] in digits and not input[i+1] in alphas)):
                id+=input[i]
                i+=1
            else:
                cont = False
        if id in id_booleans:
            self.symbols.append(Symbol(Boolean, id))
        elif id in id_operators:
            if len(self.symbols) > 1 and i > 0 and self.symbols[-1].val == '.':
                self.symbols.append(Symbol(Id, id))
            else:
                self.symbols.append(Symbol(Operator, id))
        elif id in id_keywords:
            self.symbols.append(Symbol(Keyword, Id))
        else:
            self.symbols.append(Symbol(Id, id))
        return i
    
    def parse_op(self, input, i):
        global ops, operators
        #print '> parse op'
        op = input[i]
        i+=1
        cont = True
        while op != '-' and i < len(input) and cont:
            #print '>', i
            if input[i] in ops and input[i] != '-':
                op += input[i]
                i+=1
            else:
                cont = False
        if not op in operators:
            raise Exception("Not known operator : %s" % (op,))
        self.symbols.append(Symbol(Operator, op))
        return i

"""
s = "2 + 3 - 4.to_f + (true) or False xor True ** 2.3 + 0.3.to_i / 0.to_f / 0..to_f +- 3"
y = Symbolizer()
l = y.parse(s)
i = 0
for e in l:
    print i, '. ', l[i]
    i+=1
"""

#exit() 16h28 : ancien symbolizer rempl car bug.

#-----------------------------------------------------------------------
# Syntaxic analysis (Expression)
#-----------------------------------------------------------------------

# Fetch the operator to execute
def first_op(symbols):
    # highlighting differences
    i = 0
    while i < len(symbols):
        symb = symbols[i]
        if symb.terminal:
            if symb.val == '-' and (i == 0 or symbols[i-1].kind == Operator):
                symb.val = 'unary-'
            if symb.val == '(' and i > 0 and symbols[i-1].kind != Operator:
                symb.val = 'call('
            elif symb.val == '(':
                symb.val = 'expr('
        i+=1
    # fetching the highest priority
    i = 0
    best = -1
    best_prio = -1
    prio = { ')' : 0, ',' : 1, 'and' : 5, 'or' : 5, 'xor' : 5, '<=>' : 8, '<<': 9, '>>' : 9, '+' : 10, '-' : 10, 
             '*' : 20, '/' : 20, '**' : 30, '%' : 30, 'call' : 35, '.' : 40, 
             'unary-' : 50, 'call(' : 51, 'expr(' : 60 }
    lvl = 1
    while i < len(symbols):
        symb = symbols[i]
        if symb.terminal() and symb.kind in [Operator, Separator]:
            if best == -1:
                best = i
                best_prio = prio[symb.val]*lvl
            else:
                if prio[symb.val]*lvl > best_prio:
                    best = i
                    best_prio = prio[symb.val]*lvl
            # () for others
            if symb.val in ['call(', 'expr(']:
                lvl*=10
            elif symb.val == ')':
                lvl/=10
        elif symb.val == 'call(': # not terminal
            if prio[symb.val]*lvl > best_prio:
                best = i
                best_prio = prio[symb.val]*lvl
        i+=1
    
    if best == -1: raise Exception("Incorrect expression")
    return best

def fetch_closing(sep, symbols, i):
    lvl = 0
    pos = 0
    pos = i
    while pos < len(symbols):
        symb = symbols[pos]
        if sep == '(' and symb.val in ['call(', 'expr(']: lvl += 1
        elif sep == '(' and symb.val == ')': lvl -= 1
        if lvl == 0: break
        pos+=1
    if lvl != 0: raise Exception("Incorrect expression ()")
    return pos

def not_exist_or_dif(symbols, index, terminal, value):
    if len(symbols) <= index: return True
    if symbols[index].terminal() != terminal: return True
    if symbols[index].val != value: return True
    return False

# From a token list make a tree!
def make_tree(symbols, debug=False):
    while len(symbols) > 1:    
        target = first_op(symbols)
        if debug:
            print '>>> target=%i %s' % (target, symbols[target])
        if not symbols[target].terminal():
            if symbols[target].val == 'call(':
                id = symbols[target-1]
                if id.terminal() and id.kind == Id:
                    n = Symbol(left=id, right=symbols[target], val='unprefixed_call', kind=Structure)
                    del symbols[target]
                    symbols[target-1] = n
                else:
                    raise Exception("Call not understood")
            else:
                raise Exception("Error on target node")
        elif symbols[target].terminal():
            if symbols[target].val == 'unary-':        
                n = Symbol(left=None, right=symbols[target+1], val='unary-', kind=Operator)
                del symbols[target+1]
                symbols[target] = n
            elif symbols[target].val == 'expr(':
                fin = fetch_closing('(', symbols, target)
                sub = symbols[target+1:fin]
                make_tree(sub)
                jj = fin
                while jj > target:
                    del symbols[jj]
                    jj -= 1
                symbols[target] = sub[0]
            elif symbols[target].val == 'call(':
                fin = fetch_closing('(', symbols, target)
                sub = symbols[target+1:fin]
                make_tree(sub)
                jj = fin
                while jj > target:
                    del symbols[jj]
                    jj -= 1
                symbols[target] = Symbol(left=None, right=sub[0], val='call(', kind=Structure)
            elif symbols[target].val == ',':
                n = Symbol(left=symbols[target-1], right=symbols[target+1], val='suite', kind=Structure)
                del symbols[target+1]
                del symbols[target]
                symbols[target-1] = n
            elif target > 0:
                if symbols[target].val != '.' or (symbols[target].val == '.' and not_exist_or_dif(symbols, target+2, False, "call")):
                    n = Symbol(left=symbols[target-1], right=symbols[target+1], val=symbols[target].val, kind=symbols[target].kind)
                    del symbols[target+1]
                    del symbols[target]
                    symbols[target-1] = n
                #else:
                #    raise Exception("AAAAAAAAAAAAAAAAA")
                #    # nx -> fun, call (avec par)
                #    nx = symbols[target+2]
                #    nx.left = symbols[target+1]
                #    # n -> id, nx
                #    n = Symbol(left=symbols[target-1], right=nx, val="prefixed_call", kind=Structure)
                #    del symbols[target+2]
                #    del symbols[target+1]
                #    del symbols[target]
                #    symbols[target-1] = n
            elif target == -1 and len(symbols) > 0:
                n = symbols[0]
        else:
            print symbols[target]
            raise Exception("Expression not understood")
        
        if debug:
            ii=0
            for t in symbols:
                print ii, '. ', t
                ii+=1
            print "length=%d" % (len(symbols),)
            raw_input()

#-----------------------------------------------------------------------
# Syntaxic analysis (Instruction)
#-----------------------------------------------------------------------

def make_aff(symbols):
    sub = symbols.core[2:]
    make_tree(sub)
    nx = sub[0]
    n = Symbol(left=symbols(0), right=nx, val='aff', kind=Structure)
    symbols.clear()
    symbols.add(n)

def parse(symbols): 
    if symbols.include(';'):
        two_part = symbols.split(';')
        parse(two_part[0])
        parse(two_part[1])
        n = Symbol(val=suite, kind=Structure, left=two_part[0][0], right=two_part[1][0])
        symbols.clear()
        symbols.add(n)
    elif not_exist_or_dif(symbols, 1, True, '='):
        make_tree(symbols)
    else:
        make_aff(symbols)

#-----------------------------------------------------------------------
# Interpreter
#-----------------------------------------------------------------------

import math
root_scope = {'PI' : math.pi, 'Pi' : math.pi, '_' : None }

import baselib
bb = baselib.BaseLib()

def global_function(id, args, scope):
    if id.terminal() and id.kind == Id and not args.terminal() and args.val == 'call(':
        name = id.val
        if args.right.terminal():
            if args.right.kind in [Integer, Float, String]:
                par = exec_node(args.right)
            elif args.right.kind == Id:
                par = scope[args.right.val]
            else:
                raise Exception("Bad param for global function call")
        else:
            raise Exception("Bad global function call")
        return bb.send(None, name, par, scope)

def instance_function(target, name, args, scope):
    if target.__class__ in [int, float, str, bool]:
        pass
    elif target.terminal() and target.kind in [Integer, Float, String, Boolean]:
        target = exec_node(target)
    elif target.terminal() and target.kind == Id:
        target = scope[target.val]
    else:
        raise Exception("Bad target for instance function call: %s" % (target,))
    
    if name.terminal() and name.kind == Id:
        name = name.val
    else:
        raise Exception("Bad name for instance function call: %s" % (name,))
    
    if args is None:
        par = []
    elif args.right.__class__ in [int, float, str, bool]:
        par = [args.right]
    elif args.right.terminal():
        par = [exec_node(args.right, scope)]
    elif args.right.val == 'suite':
        a = args.right
        par = []
        while not a.terminal():
            par.append(exec_node(a.right))
            a = a.left
        par.append(exec_node(a))
    else:
        raise Exception("Bad par for instance function call: %s" % (args.right,))
    r = bb.send(target, name, par, scope)
    return r

def exec_node(symbol, scope={}, debug=False):
    if debug: print 'Enter ExecNode: val=', symbol.val, "kind=", symbol.kind
    if not symbol.terminal():
        #print 'IsNode'
        if symbol.kind == Operator:
            if symbol.val == '+':
                return instance_function(exec_node(symbol.left, scope), Symbol(Id, 'add'), Symbol(Structure, 'call(', right=exec_node(symbol.right)), scope)
            elif symbol.val == '-':
                return instance_function(exec_node(symbol.left, scope), Symbol(Id, 'sub'), Symbol(Structure, 'call(', right=exec_node(symbol.right)), scope)
            elif symbol.val == '*':
                return instance_function(exec_node(symbol.left, scope), Symbol(Id, 'mul'), Symbol(Structure, 'call(', right=exec_node(symbol.right)), scope)
            elif symbol.val == '/':
                return instance_function(exec_node(symbol.left, scope), Symbol(Id, 'div'), Symbol(Structure, 'call(', right=exec_node(symbol.right)), scope)
            elif symbol.val == '%':
                return instance_function(exec_node(symbol.left, scope), Symbol(Id, 'mod'), Symbol(Structure, 'call(', right=exec_node(symbol.right)), scope)
            elif symbol.val == '**':
                return instance_function(exec_node(symbol.left, scope), Symbol(Id, 'pow'), Symbol(Structure, 'call(', right=exec_node(symbol.right)), scope)
            elif symbol.val == 'unary-':
                return instance_function(exec_node(symbol.right, scope), Symbol(Id, 'inv'), None, scope)
            elif symbol.val in ['and', 'or', 'xor']:
                return instance_function(exec_node(symbol.left, scope), Symbol(Id, symbol.val), Symbol(Structure, 'call(', right=exec_node(symbol.right)), scope)
            elif symbol.val == '.':
                if symbol.right.val != 'unprefixed_call':
                    target = exec_node(symbol.left, scope)
                    return instance_function(target, symbol.right, None, scope)
                elif symbol.right.val == 'unprefixed_call':
                    call = symbol.right
                    return instance_function(symbol.left, call.left, call.right, scope)
                else:
                    raise Exception("What to do with this symbol ? : %s" % (symbol.right.val))
            elif symbol.val == '<<':
                return instance_function(exec_node(symbol.left, scope), Symbol(Id, 'lshift'), Symbol(Structure, 'call(', right=exec_node(symbol.right)), scope)
            elif symbol.val == '>>':
                return instance_function(exec_node(symbol.left, scope), Symbol(Id, 'rshift'), Symbol(Structure, 'call(', right=exec_node(symbol.right)), scope)
            elif symbol.val == '<=>':
                return instance_function(exec_node(symbol.left, scope), Symbol(Id, 'cmp'), Symbol(Structure, 'call(', right=exec_node(symbol.right)), scope)
            else:
                raise Exception("Operator not understood")
        elif symbol.kind == Structure:
            if symbol.val == 'unprefixed_call':
                return global_function(symbol.left, symbol.right, scope)
            #elif symbol.val == 'prefixed_call':
            #    return instance_function(symbol.left, symbol.right, scope)
            elif symbol.val == 'aff':
                if symbol.left.val in scope and symbol.left.val[0].isupper():
                    raise Exception("Constant reference can't be changed")
                value = exec_node(symbol.right, scope)
                if symbol.left.val[-1] == '?' and not isinstance(value, bool):
                    raise Exception("?-ending id must reference boolean value")
                scope[symbol.left.val] = value
                return scope[symbol.left.val]
            elif symbol.val == 'suite':
                exec_node(symbol.left, scope)
                return exec_node(symbol.right, scope)
            else:
                raise Exception("Invisible Node type not understood")
        else:
            print symbol.left
            print symbol.middle
            print symbol.right
            raise Exception("Node type not understood")
    elif symbol.terminal():
        if symbol.kind == Integer:
            if len(symbol.val) > 1 and symbol.val[1] == 'x':
                return int(symbol.val, 16)
            elif len(symbol.val) > 1 and symbol.val[1] == 'b':
                return int(symbol.val, 2)
            elif len(symbol.val) > 1 and symbol.val[1] == 'c':
                return int("0" + symbol.val[2:], 8)
            else:
                return int(symbol.val)
        elif symbol.kind == Float:
            return float(symbol.val)
        elif symbol.kind == Id:
            return scope[symbol.val]
        elif symbol.kind == String:
            return symbol.val[1:len(n.val)-1]
        elif symbol.kind == Boolean:
            return symbol.val in ['true', 'True']
        else:
            print symbol
            raise Exception("TokenType not understood")
    else:
        print symbol.__class__
        print symbol
        raise Exception("Node not known")

#-----------------------------------------------------------------------
# Tests
#-----------------------------------------------------------------------

"""
t = Symbolizer()
#s = "2.0 * (-(2+1).abs + 2..abs) + a"
s = "(2 + 3) * 4"
s = "3.add(2)"
print 'solve: %s' % (s,)
o = t.parse(s)
i = 0
for e in o:
    print '%d. %s' % (i, str(e))
    i+=1
del o[-1] # eof
print o[first_op(o)], first_op(o)

make_tree(o, True)
r = exec_node(o[0], {}, True)
print r

exit()
"""

def test(s, debug=True, mode = 'exec'):
    global root_scope
    t = Symbolizer()
    o = t.parse(s)
    if debug or mode == 'symbols':
        i = 0
        for e in o:
            print '%d. %s' % (i, str(e))
            i+=1
    if mode == 'symbols':
        return o
    del o[-1] # del eof
    #print '>>> %i %s' % (first_op(o), o[first_op(o)])
    parse(o)
    r = exec_node(o[0], root_scope)
    root_scope['_'] = r
    if debug:
        print "result of parse: ", o[0]
        print "for: %s \t res = %s" % (s, str(r))
    #else:
    #    print r
    return r

def run_tests():
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
    test("println(4)")    # None >> 4
    test("3.add(2)")    # 5 
    test("a = 3")       # 3
    test("a")           # 3
    test("a + 2")       # 5
    test("a = 2 + 4")   # 6
    test("a")           # 6
    test("a.add(1)")    # 7

class Interpreter:
    def __init__(self):
        pass
    
    def do_string(self, text):
        return test(text, False, 'exec')

if __name__ == '__main__':
    command = ''
    loop = True
    debug = False
    mode = 'exec'
    prod = True
    print 'Welcome to Pypo 0.1'
    while loop:
        command = raw_input('>>> ')
        if command in ['exit', 'debug', '', 'symbols', 'exec', 'dump', 'prod', 'test']:
            if command == 'exit' or command == '':
                loop = False
            elif command == 'debug':
                debug = not debug
            elif command == 'symbols':
                mode = 'symbols'
                print 'mode changed to symbols only'
            elif command == 'exec':
                mode = 'exec'
                print 'mode changed to full execution'
            elif command == 'dump':
                for e in root_scope:
                    print e
            elif command == 'prod':
                prod = not prod
                if prod: print 'production mode on'
                else: print 'beware: dev mode on'
            elif command == 'test':
                run_tests()
        else:
            if prod:
                try:
                    print test(command, debug, mode)
                except Exception as e:
                    print e
            else:
                print test(command, debug, mode)

    a = Symbol(Id, "a")
    b = Symbol(Operator, "=")
    c = Symbol(Integer, "5")
    l = [a, b, c]

    a = Symbol(Integer, "3")
    b = Symbol(Separator, ";")
    c = Symbol(Integer, "5")

#tl = TokenList([a,b,c])
#print tl[0]

#raw_input()

#print exists_token([a,b,c], ';')
#split_on([a,b,c], ';')

#parse(l)
#print exec_node(l[0])


#exit()
