# 15h39-42. OK

# Token

#-------------------------------------------------------------------------------

# Tools

class Enum:
    def __init__(self, *tab):
        self.tab = tab
        i = 0
        for t in tab:
            setattr(self, t, t)

LexerState = Enum('start', 'float', 'integer', 'operator', 'id', 'hexa', 'bin', 'octal', 'string')
TokenType = Enum('integer', 'float', 'id', 'operator', 'separator','keyword', 'eof', 'boolean', 'string')

#-------------------------------------------------------------------------------

# Lexer

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

def is_octaldigit(c):
    return (c in ['0', '1', '2', '3', '4', '5', '6', '7'])

def is_bindigit(c):
    return (c in ['0', '1'])

def is_ops_char(c):
    return (c in ['+', '-', '/', '*', '%', '>', '<', '=', '!', '&', '^', '|'])

def is_sep_char(c):
    return (c in [',', ';', '(', ')', '[', ']', '{', '}', '\n'])

def is_silent(c):
    return (c in [' ', '\t'])

def is_aff_operator(s): # for parsing, could be merge with the next one
    return (s in ['=', '+=', '-=', '/=', '//=', '*=', '**=', '%=', '->'])

def is_arithmetic_operator(s):
    return (s in ['+', '-', '/', '*', '//', '**', '%'])

def is_comparaison_operator(s):
    return (s in ['>', '>=', '==', '!=', '<=', '<'])

def is_bitwise_operator(s):
    return (s in ['!', '&', '^', '|'])

def is_operator(s):
    return (is_arithmetic_operator(s) or 
            is_aff_operator(s) or
            is_comparaison_operator(s) or
            is_bitwise_operator(s))

def is_boolean(s):
    return (s in ['true', 'false'])

def is_keyword(s):
    return (s in ['if', 'then', 'else', 'elsif', 'end', 'while', 'do', 'end', 'until', 'unless', 'break', 'next', 'return', 'fun'])

class Token:
    def __init__(self, kind, val):
        self.kind = kind
        self.val = val
    def __str__(self):
        return 'Token: %s : %s' % (self.val, self.kind)

s = ' '
escape = False
state = 'start'
i = 0
c = s[i]
curr = []
tokens = []

def restart():
    global s, curr, tokens, c, i, state, escape
    escape = False
    state = 'start'
    i = 0
    if len(s) > 0:
        c = s[i]
    else:
        c = '\0'
    curr = []
    tokens = []

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
    state = LexerState.start

debug = False

def tokenize():
    global s, curr, tokens, c, i, state, escape, debug
    
    while not escape:
        #print curr
        if c == '\0': # last turn
            escape = True
        if state == LexerState.start:
            if is_char(c) or c == '$' or c == '@' or c == '_':
                state = LexerState.id
                #
                curr.append(c)
                next()
            elif is_digit(c):
                state = LexerState.integer
                #
                curr.append(c)
                next()
            elif c == '"':
                state = LexerState.string
                #
                #curr.append(c)
                next()
            elif c == '.': # '.' can be for a float or an operator
                state = LexerState.float
                #
                curr.append(c)
                next()
            elif is_ops_char(c):
                state = LexerState.operator
                #
                curr.append(c)
                next()
            elif is_sep_char(c):
                curr.append(c)
                next()
                token(TokenType.separator)
            elif c == '#':
                end = False
                while (not escape) and (not end):
                    next()
                    if c == ';' or c == '\n':
                        end = True
            elif is_silent(c):
                next()
            elif c == '\0':
                pass # ????
            else:
                print 'Forbidden character: [%s]' % (str(c),)
                print c == '\0'
                print curr
        elif state == LexerState.id:
            if (is_char(c) or is_digit(c) or c == '_') or (c == '@' and len(curr) == 1):
                curr.append(c)
                next()
            else:
                #print '>>> [', ''.join(curr), ']', is_boolean(''.join(curr))
                if is_keyword(''.join(curr)):
                    token(TokenType.keyword)
                elif is_boolean(''.join(curr)):
                    token(TokenType.boolean)
                else:
                    token(TokenType.id)
        elif state == LexerState.integer:
            if is_digit(c):
                curr.append(c)
                next()
            elif curr == ['0'] and (c == 'x' or c == 'X'):
                state = LexerState.hexa
                curr.append(c)
                next()
            elif curr == ['0'] and (c == 'c' or c == 'C'):
                state = LexerState.octal
                curr.append(c)
                next()
            elif curr == ['0'] and (c == 'b' or c == 'B'):
                state = LexerState.bin
                curr.append(c)
                next()
            elif c == '.':
                state = LexerState.float
                curr.append(c)
                next()
            else:
                token(TokenType.integer)
        elif state == LexerState.float:
            if is_digit(c):
                curr.append(c)
                next()
            elif len(curr) == 1: # We have a lonely '.'
                token(TokenType.operator)        
            else:
                token(TokenType.float)
        elif state == LexerState.octal:
            if is_octaldigit(c):
                curr.append(c)
                next()
            elif is_hexadigit(c):
                raise Exception("Mismatched integer")
            else:
                token(TokenType.integer)
        elif state == LexerState.bin:
            if is_bindigit(c):
                curr.append(c)
                next()
            elif is_hexadigit(c):
                raise Exception("Mismatched integer")
            else:
                token(TokenType.integer)
        elif state == LexerState.hexa:
            if is_hexadigit(c):
                curr.append(c)
                next()
            elif is_char(c):
                raise Exception("Mismatched integer")
            else:
                token(TokenType.integer)
        elif state == LexerState.operator:
            if is_ops_char(c) and is_operator((''.join(curr))+c):
                curr.append(c)
                next()
            else:
                token(TokenType.operator)
        elif state == LexerState.string:
            if c != '"' and (len(curr) < 2 or curr[len(curr)-1] != '\\'):
                curr.append(c)
                next()
            else:
                next()
                token(TokenType.string)

    curr = ['eof']
    token(TokenType.eof)

    if debug:
        print('\nTokens\n')
    
        i=0
        for t in tokens:
            print i, '.', t
            i+=1
    
        print('\nNb: '+str(len(tokens)))

#-------------------------------------------------------------------------------

# Parser
# tokens -> AST

print('\nParser\n')

def xxparse(tokens):
    #print '--- big xxparse---'
    
    blocks = xparse(tokens)
    #
    if len(blocks) == 0:
        print '********* ERROR *********'
        for t in tokens:
            print t
        print 'Nothing found'
    #
    n = None
    master = None
    for b in blocks:
        if b['type'] in ['if', 'unless']:
            sel_cond = make_ast(tokens[b['start']+1:b['middle']])
            sel_action = xxparse(tokens[b['middle']+1:b['end']])
            n = Node(kind='if', cond=sel_cond, action=sel_action, invert=(b['type'] == 'unless'))
        elif b['type'] in ['while', 'until']:
            iter_cond = make_ast(tokens[b['start']+1:b['middle']])
            iter_action = xxparse(tokens[b['middle']+1:b['end']])
            n = Node(kind='while', cond=iter_cond, action=iter_action, invert=(b['type'] == 'until'))
        elif b['type'] == 'expression':
            n = make_ast(tokens[b['start']:b['end']+1])
        elif b['type'] in ['{', '(', '[']:
            if b['start'] == b['end']:
                n = Node(kind='suite', subkind='sequence', left=None, right=None)
            else:
                r = None
                i = b['start']
                end_i = i
                while i <= b['end']:
                    while tokens[end_i].val != ',' and end_i <= b['end']:
                        end_i += 1
                    n = make_ast(tokens[i:end_i]) # ERROR HUMANUM EST
                    i+=1
                    end_i = i
                    if r is None:
                        r = Node(kind='suite', subkind='sequence', left=n, right=None)
                    else:
                        r = Node(kind='suite', subkind='sequence', left=r, right=n)
                n = r
        elif b['type'] == 'empty':
            n = Node(kind='empty')
        elif b['type'] == 'break':
            n = Node(kind='break')
        elif b['type'] == 'fun':
            fun_param = [] #TODO
            fun_ret = None
            fun_action = xxparse(tokens[b['middle']+1:b['end']])
            n = Node(kind='fun', name=tokens[b['start']+1].val, param=fun_param, ret=fun_ret, action=fun_action)
        if master is None:
            master = Node(kind='suite', subkind='statement', left=n, right=None)
        elif n.kind != 'empty':
            master = Node(kind='suite', subkind='statement', left=master, right=n)
    return master

def xparse(tokens):
    #print '---xparse---'
    block_mode = 'start'
    level = 0
    start = 0
    middle = -1
    blocks = []
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if block_mode == 'start':
            if t.val in ['if', 'while', 'until', 'unless', 'fun']:
                block_mode = t.val
                level = 1
                start = i
            elif t.val in ['break']:
                block_mode = t.val
                start = i
            elif t.kind in [TokenType.id, TokenType.float, TokenType.integer, TokenType.string, TokenType.boolean]:
                block_mode = 'expression'
                start = i
            elif t.val in ['{', '(', '[']:
                block_mode = t.val
                level = 1
                start = i
            elif t.kind == TokenType.eof:
                blocks.append({'type' : 'empty', 'start' : i, 'end' : i})
                break
        elif block_mode in ['if', 'while', 'until', 'unless']:
            if t.val in ['if', 'while', 'until', 'unless']:
                level += 1
            elif middle == -1 and block_mode in ['if', 'unless'] and (t.val == 'then' or t.val == '\n'):
                middle = i
            elif middle == -1 and block_mode in ['while', 'until'] and (t.val == 'do' or t.val == '\n'):
                middle = i
            elif t.val == 'end':
                level -= 1
            if level == 0:
                blocks.append({'type' : block_mode, 'start' : start, 'end' : i, 'middle' : middle})
                block_mode = 'start'
                middle = -1
        elif block_mode == 'fun':
            if t.val in ['if', 'while', 'until', 'unless']:
                level += 1
            elif middle == -1 and (t.val == 'do' or t.val == '\n'):
                middle = i
            elif t.val == 'end':
                level -= 1
            if level == 0:
                blocks.append({'type' : block_mode, 'start' : start, 'end' : i, 'middle' : middle})
                block_mode = 'start'
                middle = -1
        elif block_mode in ['{', '(', '[']:
            if t.val == block_mode:
                level += 1
            elif (block_mode == '{' and t.val == '}') or (block_mode == '(' and t.val == ')') or (block_mode == '[' and t.val == ']'):
                level -= 1
            if level == 0:
                blocks.append({'type' : block_mode, 'start' : start+1, 'end' : i})
                block_mode = 'start'
        
        if block_mode == 'expression':
            if t.kind == TokenType.eof or t.val == ';' or t.val == '\n' or i == len(tokens)-1:
                if i == len(tokens)-1: # and len(tokens) == 1:
                    blocks.append({'type' : block_mode, 'start' : start, 'end' : i})
                else:
                    blocks.append({'type' : block_mode, 'start' : start, 'end' : i-1})
                block_mode = 'start'
        elif block_mode == 'break':
            if t.val in [';', '\n'] or i == len(tokens)-1:
                blocks.append({'type' : block_mode, 'start' : start, 'end' : i})
                block_mode = 'start'
        
        i+=1
    #i=0
    #for b in blocks:
    #    i = 0
    #    for t in tokens:
    #        print '\t', i, t
    #        i += 1
    #    if 'middle' in b:
    #        print b['type'], b['start'], b['middle'], b['end']
    #    else:
    #        print b['type'], b['start'], b['end']
    return blocks

class Node:
    def __init__(self, **kw):
        self.rem = kw # on ne devrait prendre que les cles !
        for k in kw:
            setattr(self, k, kw[k])
    def info(self):
        for k in self.rem:
            print '\t', k, '=>', getattr(self, k) #self.rem[k]
    def __str__(self):
        return 'node(%s)' % (self.kind,)

#

def clear():
    global tokens
    i = 0
    while i < len(tokens)-1:
        actual = tokens[i].val
        next = tokens[i+1].val
        
        if actual == 'then' and next == '\n':
            del tokens[i+1]
        elif actual == '\n' and next == '\n':
            del tokens[i+1]
        elif actual == ';' and next == ';':
            del tokens[i+1]
        elif actual == ';' and next == '\n':
            del tokens[i+1]
        elif actual == '\n' and next == ';':
            del tokens[i+1]
        elif actual == 'end' and next == '\n':
            del tokens[i+1]
        elif actual == 'end' and next == ';':
            del tokens[i+1]
        elif actual == '\n' and next == 'end':
            del tokens[i]
        elif actual == ';' and next == 'end':
            del tokens[i]
        else:
            i += 1
    
    if  len(tokens) == 2: # eof + whatever
        if tokens[0].val in ['\n', ';']:
            del tokens[0]
    
    #for t in tokens:
    #    print 'cleared: ', t

#

def sub(subjects):
    mod = 0
    start = subjects[0]
    i = 0
    while i < len(subjects):
        t = subjects[i]
        if isinstance(t, Node):
            i+=1
            continue
        if start.val == '(':
            if t.val == '(':
                mod += 1
            elif t.val == ')':
                mod -= 1
                if mod == 0:
                    break
        elif start.val == '{':
            if t.val == '{':
                mod += 1
            elif t.val == '}':
                mod -= 1
                if mod == 0:
                    break
        elif start.val == '[':
            if t.val == '[':
                mod += 1
            elif t.val == ']':
                mod -= 1
                if mod == 0:
                    break
        elif start.val in ['while', 'for', 'class', 'fun', 'module', 'until', 'if']:
            #print '>>', t.val
            #print '>>', mod
            if t.val in ['while', 'for', 'class', 'fun', 'module', 'until', 'if']:
                mod += 1
            elif t.val == 'end':
                mod -= 1
                if mod == 0:
                    break
        i+=1
    r = subjects[1: i]
    return r
#

def make_ast(tokens):
    if len(tokens) < 1:
        raise Exception("Empty token list")
    #elif len(tokens) == 1 and tokens.kind == TokenType.eof: # only eof inside
    #    tokens[0] = Node(kind='empty')
    
    prio = {
        '->':  10, '=' :  10, '+=':  10, '-=':  10,
        '==': 80, '!=': 81, '<' : 82, '<=': 81, '>' : 83, '>=': 84,
        '-':101, '+':101, '*':102, '/':102, '//':102, '%':103, '**':103,
        }
    ts = {
        TokenType.id : 'id', 
        TokenType.integer : 'integer', 
        TokenType.float : 'float', 
        TokenType.boolean : 'boolean', 
        TokenType.string : 'string' }
    # Litterals and removing the last (if any)
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t.kind in ts:
            tokens[i] = Node(kind=ts[t.kind], val=t.val)
        if t.kind == TokenType.eof:
            del tokens[i]
        i+=1
    # Operators GROS BUG J AI { { !!!
    #i = 0
    #for t in tokens:
    #    print i, t
    #    i+=1
    while len(tokens) > 1:
        i = 0
        max = None
        while i < len(tokens):
            t = tokens[i]
            if isinstance(t, Token) and t.val in prio:
                if max is None or prio[tokens[max].val] < prio[t.val]:
                    max = i
            i+=1
        if not max is None and tokens[max].val != '{':
            n = Node(kind='binop',op=tokens[max].val,arg1=tokens[max-1],arg2=tokens[max+1])
            tokens[max] = n
            if len(tokens) <= max+1:
                raise Exception('Incorrect expr right')
            if max == 0:
                raise Exception('Incorrect expr left')
            del tokens[max+1]
            del tokens[max-1]
        #elif not max is None and tokens[max].val == '{': # laid. a revoir.
        #    l = sub(tokens[max:])
        #    n = Node(kind='hash',val={}) #TODO
        #    tokens[max] = n
        #    del tokens[max+1+len(l)]
        else:
            for t in tokens:
                print '%%%', t
            raise Exception('Prio not found')
    return tokens[0]
#

#-------------------------------------------------------------------------------

# Interpreter

class XINT(int):
    def __init__(self, val):
        int.__init__(self, val)

class ZINT(int):
    def __new__(cls, *args, **kwargs):
        return  super(ZINT, cls).__new__(cls, args[0])

class XFUN(object):
    def __init__(self, name, par, ret, ast):
        self.name = name
        self.par = par
        self.ret = ret
        self.ast = ast
    def xcall(self, interpreter, scope, *par_lst, **par_dic):
        xscope = scope.copy()
        # la faire le mix des param dans xscope
        interpreter.do_node(self.ast, xscope, True)

class Interpreter:

    def __init__(self, scope=[]):
        self.scope = scope
        self.MASTER_LOOP_EXIT = False

    def do_string(self, s2, stack=[], scope={}):
        global s
        s = s2
        restart()
        tokenize()
        clear()
        # Test
        master = xxparse(tokens)
        r = self.do_node(master, scope, True)
        #self.process_python(n)
        self.process_vm(master, stack)
        return r
    
    def process_vm(self, n, start):
        if not isinstance(n, Node):
            raise Exception('Not a node but %s' % (str(n.__class__),))
        if n.kind == 'suite' and n.subkind == 'statement':
            self.process_vm(n.left, start)
            if not n.right is None:
                self.process_vm(n.right, start)
        elif n.kind == 'suite' and n.subkind == 'sequence':
            start.append('SEQ START')
            if not n.left is None:
                self.process_vm(n.left, start)
                if not n.right is None:
                    self.process_vm(n.right, start)
            start.append('SEQ END')
        elif n.kind == 'suite':
            print n.subkind
            exit(1)
        elif n.kind == 'binop':
            dop = {'+' : 'ADD', '*' : 'MUL', '-' : 'SUB', '/' : 'DIV', '//' : 'INTDIV', '**' : 'POW', '%' : 'MOD', '<' : 'LT', '>' : 'GT', '>=' : 'GE', '<=' : 'LE', '!=' : 'NE', '==' : 'EQ', '=' : 'AFF', '+=' : 'AFF_ADD', '-=' : 'AFF_SUB', '->' : 'CONST' }
            self.process_vm(n.arg1, start)
            self.process_vm(n.arg2, start)
            start.append(dop[n.op])
        elif n.kind == 'integer':
            start.append('INTEGER ' + n.val)
        elif n.kind == 'float':
            start.append('FLOAT ' + n.val)
        elif n.kind == 'boolean':
            start.append('BOOLEAN ' + n.val)
        elif n.kind == 'hash':
            for e in n.val:
                start.append('KEY ' + e)
                start.append('VAL ' + n.val[e])
            start.append('HASH ' + str(len(n.val)))
        elif n.kind == 'string':
            start.append('STRING ' + n.val)
        elif n.kind == 'id':
            start.append('ID ' + n.val)
        elif n.kind == 'if':
            self.process_vm(n.cond, start)
            minis = []
            minis.append('JUMP XXX')
            self.process_vm(n.action, minis)
            if n.invert:
                minis[0] = 'JUMP_ON_TRUE ' + str(len(minis))
            else:
                minis[0] = 'JUMP_ON_FALSE ' + str(len(minis))
            minis.append('REM ENDIF')
            for elem in minis:
                start.append(elem)
        elif n.kind == 'while':
            lbl = len(start)
            self.process_vm(n.cond, start)
            minis = []
            minis.append('JUMP XXX')
            self.process_vm(n.action, minis)
            minis.append('JUMP ' + str(lbl))
            if n.invert:
                minis[0] = 'JUMP_ON_TRUE ' + str(len(minis))
            else:
                minis[0] = 'JUMP_ON_FALSE ' + str(len(minis))
            minis.append('REM ENDWHILE')
            for elem in minis:
                start.append(elem)
        #elif n.kind == 'seq': # => suite
        #    if n.subkind == 'sta':
        #        self.process_vm(n.left, start)
        #        self.process_vm(n.right, start)
        #    else:
        #        raise Exception("ZEMBLA !") #TODO
        elif n.kind == 'break':
            start.append('JUMP_BRK') #TODO
        elif n.kind == 'fun':
            start.append('FUN %s' % (n.name,)) # on inclut le JMP dans le FUN.
            self.process_vm(n.action, start)
            start.append('REM END FUN %s' % (n.name,))
        elif n.kind == 'empty':
            pass
        else:
            raise Exception('Node type not handled %s' % (n.kind,))
        pass
        # LOAD_STACK X
        # LOAD_STACK Y
        # ADD
        # STORE A
        
    def process_python(self, n):
        if not isinstance(n, Node):
            raise Exception('Not a node but %s' % (str(n.__class__),))
        if n.kind == 'suite' and n.subkind == 'statement':
            pass
        elif n.kind == 'binop':
            return self.process_python(n.arg1) + ' ' + n.op + ' '+self.process_python(n.arg2)
        elif n.kind == 'integer':
            return n.val
        elif n.kind == 'float':
            return n.val
        elif n.kind == 'boolean':
            if n.val == 'true':
                return 'True'
            else:
                return 'False'
        #elif n.kind == 'hash':
        #    s = '{'
        #    for e in n.val:
        #        s += self.process_python(n.val[e])
        #        s += ','
        #    s += '}'
        #    return s
        else:
            raise Exception('Node type not handled %s' % (n.kind,))
    
    def binop_num(self, a, b, op):
        if isinstance(b, int) or isinstance(b, float):
            if op == '+':
                return a + b
            elif op == '*':
                return a * b
            elif op == '/':
                f = float(a) / float(b)
                if a.__class__ == int and b.__class__ == int and f == int(f):
                    return int(f)
                else:
                    return f
            elif op == '//':
                return int(a / b)
            elif op == '**':
                return a ** b
            elif op == '-':
                return a - b
            elif op == '%':
                return a % b
            else:
                raise Exception('Unknown operator %s for %s with par %s' % (op, a.__class__, b.__class__))
        else:
            raise Exception('Incorrect operand %s for %s with operator %s' % (a.__class__, b.__class__, op))
    
    def binop_str(self, a, b, op):
        if isinstance(b, basestring):
            if op == '+':
                return a + b
            elif op == '-':
                return a.replace(b, '')
            else:
                raise Exception('Unknown operator %s for %s with par %s' % (op, a.__class__, b.__class__))
        elif isinstance(b, int):
            if op == '*':
                return a * b
            else:
                raise Exception('Unknown operator %s for %s with par %s' % (op, a.__class__, b.__class__))        
        else:
            raise Exception('Incorrect operand %s for %s with operator %s' % (a.__class__, b.__class__, op))
    
    def do_node(self, n, scope={}, lonely=False):
        if not isinstance(n, Node):
            raise Exception('Not a node but %s' % (str(n.__class__),))
        if n.kind == 'suite' and n.subkind == 'statement':
            r = self.do_node(n.left, scope, True)
            if not n.right is None:
                r = self.do_node(n.right, scope, True)
            return r
        if n.kind == 'suite' and n.subkind == 'sequence':
            if not n.left is None:
                r = [self.do_node(n.left, scope, True)]
                if not n.right is None:
                    r.append(self.do_node(n.right, scope, True))
            else:
                r = []
            return r
        elif n.kind == 'binop':
            a = self.do_node(n.arg1, scope)
            b = self.do_node(n.arg2, scope)
            if isinstance(a, str) and n.arg1.kind == 'id':
                ida = a
                if a in scope:
                    a = scope[a]
                else:
                    a = None
            if isinstance(b, str) and n.arg2.kind == 'id':
                idb = b
                if b in scope:
                    b = scope[b]
                else:
                    b = None
            if is_arithmetic_operator(n.op):
                if (a.__class__ in [int, float]):
                    return self.binop_num(a, b, n.op)
                elif isinstance(a, basestring):
                    return self.binop_str(a, b, n.op)
                else:
                    raise Exception('Incorrect class %s for operator %s' % (a.__class__, n.op))
            elif n.op == '<':
                return a < b
            elif n.op == '<=':
                return a <= b
            elif n.op == '>':
                return a > b
            elif n.op == '>=':
                return a >= b
            elif n.op == '==':
                return a == b
            elif n.op == '!=':
                return a != b
            elif n.op == '=':
                if ida in scope:
                    if hasattr(scope[ida], 'frozen') and scope[ida].frozen:
                        raise Exception("Can't assign constants %s" % (ida,))
                    elif scope[ida].__class__ != b.__class__:
                        raise Exception("Can't change type for %s (%s -> %s)" % (ida, scope[ida].__class__, b.__class__))
                #if isinstance(b, int):
                scope[ida] = b #XINT(b)
                return scope[ida]
            elif n.op == '+=':
                scope[ida] = scope[ida] + b
                return scope[ida]
            elif n.op == '-=':
                scope[ida] = scope[ida] - b
                return scope[ida]
            elif n.op == '->':
                if isinstance(b, int):
                    scope[ida] = ZINT(b)
                scope[ida].frozen = True
                return scope[ida]
            else:
                raise Exception('error unknown op : %s' % (n.op,))
        elif n.kind == 'integer':
            if len(n.val) >= 3:
                if n.val[0:2] == '0x' or n.val[0:2] == '0X':
                    r = int(n.val, 16)
                elif n.val[0:2] == '0b' or n.val[0:2] == '0B':
                    r = int(n.val, 2)
                elif n.val[0:2] == '0c' or n.val[0:2] == '0C':
                    r = int(n.val[2:], 8)
                else:
                    r = int(n.val)
            else:
                r = int(n.val)
            return r
        elif n.kind == 'float':
            return float(n.val)
        elif n.kind == 'boolean':
            return (n.val == 'true')
        elif n.kind == 'hash':
            h = {}
            for e in n.val:
                h[e] = self.do_node(n.val[e])
            return h
        elif n.kind == 'string':
            return n.val
        elif n.kind == 'id':
            if not lonely:
                return n.val
            else:
                if n.val in scope:
                    return scope[n.val]
                else:
                    raise Exception('Var %s not defined' % (n.val,))
        elif n.kind == 'if':
            cond = self.do_node(n.cond, scope, True)
            r = None
            #print 'b', scope['b']
            #print 'cond', cond
            #print 'n.invert', n.invert
            if (cond and (not n.invert)) or ((not cond) and n.invert):
                r = self.do_node(n.action, scope, True)
            return r
        elif n.kind == 'while':
            max_repeat = 1000
            iteration = 0
            cond = self.do_node(n.cond, scope, True)
            r = None
            while ((cond and (not n.invert)) or ((not cond) and n.invert)) and not self.MASTER_LOOP_EXIT:
                if iteration >= max_repeat:
                    r = '<<max iteration>>'
                    break
                else:
                    iteration+=1
                r = self.do_node(n.action, scope, True)
                cond = self.do_node(n.cond, scope, True)
            if self.MASTER_LOOP_EXIT:
                self.MASTER_LOOP_EXIT = False
            return r
        #elif n.kind == 'seq':
        #    if n.subkind == 'sta':
        #        self.do_node(n.left)
        #        return self.do_node(n.right)
        #    else:
        #        exit(1) # TODO
        elif n.kind == 'break':
            self.MASTER_LOOP_EXIT = True
        elif n.kind == 'fun':
            scope[n.name] = XFUN(n.name, n.param, n.ret, n.action)
        elif n.kind == 'empty':
            return None
        else:
            raise Exception('Node type not handled %s' % (n.kind,))

#intr = Interpreter()

#try:
    #try:
        #r = None
        #r = intr.do_node(n)
    #except Exception: #as e: # ne marche pas !!!!!!!
        #print "ALARMA"
    #else: # si pas d'exception leve
        #pass
        #r = None
        #print 'done'
#finally: #NE MARCHE PAS ???? !!!!!! http://docs.python.org/tutorial/errors.html
    #pass #print 'f'
    #    pass BROKEN PYTHON ???? 2.3.5 sur ce mac !!! 2.5 pour unifier


#-------------------------------------------------------------------------------

import sys
import traceback

class Test:
    def __init__(self, test, waited):
        self.test_str = test
        self.waited = waited
        self.computed = None
    
    @classmethod
    def setup(cls, intpr):
        Test.intpr = intpr
        Test.ERROR = (None, 99)
    
    def test(self, stack=[], scope={}):
        try:
            self.computed = Test.intpr.do_string(self.test_str, stack, scope)
        except Exception as e:
            if self.waited == Test.ERROR:
                self.computed = Test.ERROR
            else:
                traceback.print_exc(file=sys.stdout)
                raise e
                
    
    def is_ok(self):
        return self.computed == self.waited
    
    def __str__(self):
        if self.computed == self.waited:
            if self.waited != Test.ERROR:
                return "[ok] for '%s' we got %s" % (self.test_str.replace('\n', 'NL'), self.computed)
            else:
                return "[ok] for '%s' as failed as intended" % (self.test_str.replace('\n', 'NL'),)
        else:
            return "[!!] for '%s' we got %s instead of %s" % (self.test_str.replace('\n', 'NL'), self.computed, self.waited)

#s = "a = 5; b = 2; c = a * -b+1; writeln(c) #pipo; 11+1 .4 2.3.alpha 5..alpha"

Test.setup(Interpreter())

suite = []
suite.append(Test("4 + 5", 9))
suite.append(Test("4 + 5 + 1", 10))
suite.append(Test("4 + 3 + 2", 9))
suite.append(Test("4 * 2 + 2", 10))
suite.append(Test("4 + 2 * 2", 8))
suite.append(Test("5 / 2", 2.5))
suite.append(Test("5 // 2", 2))
suite.append(Test("5 ** 2", 25))
suite.append(Test("10 + 2 / 2", 11))
suite.append(Test("10 % 5", 0))
suite.append(Test("11 % 5", 1))
suite.append(Test("11 % 5 + 1", 2))
suite.append(Test("1 + 11 % 5", 2))
suite.append(Test("2.0 + 1.3", 3.3))
suite.append(Test("2 < 3", True))
suite.append(Test("2 + 1 == 3", True))
suite.append(Test("2 < 3 == 3 < 5", True))
suite.append(Test("true", True))
suite.append(Test("5", 5))
suite.append(Test("true + 1", Test.ERROR))
suite.append(Test("1 / 0", Test.ERROR))
suite.append(Test('"savior" / 5', Test.ERROR))
suite.append(Test("{}", {}))
suite.append(Test("0xA == 10", True))
suite.append(Test("0b10 == 2", True))
suite.append(Test("0c10 == 8", True))
suite.append(Test("0XA == 10", True))
suite.append(Test("0B10 == 2", True))
suite.append(Test("0C10 == 8", True))
suite.append(Test('"savior"', "savior"))
suite.append(Test("a = 5", 5))
suite.append(Test("a", 5))
suite.append(Test("a + 5", 10))
suite.append(Test("a", 5))
suite.append(Test("b = a + 5", 10))
suite.append(Test("b", 10))
suite.append(Test('"hel"+"lo"', "hello"))
suite.append(Test('"hello" - "ll"', "heo"))
suite.append(Test('"helloll" - "ll"', "heo"))
suite.append(Test('"a" * 3', "aaa"))
suite.append(Test('"a" / 3', Test.ERROR))
suite.append(Test("if b == 10 then 42 end", 42))
suite.append(Test("if b != 10 then 42 end", None))
suite.append(Test("unless b == 10 then 42 end", None))
suite.append(Test("unless b != 10 then 42 end", 42))
suite.append(Test("42 ; 23", 23))
suite.append(Test("if b == 10 then 42 ; 23 end", 23))
suite.append(Test("until b > 12 do b = b + 1 end", 13))
suite.append(Test("while b > 10 do b = b - 1 end", 10))
suite.append(Test("until b > 12 do b += 1 end", 13))
suite.append(Test("while b > 10 do b -= 1 end", 10))
suite.append(Test("const -> 0", 0))
suite.append(Test("const = 22", Test.ERROR))
suite.append(Test("a = 2.2", Test.ERROR))
suite.append(Test("", None))
suite.append(Test(" ", None))
suite.append(Test("          \t", None))
suite.append(Test("\n", None))
suite.append(Test("\n;;\t\n", None))
suite.append(Test("if b == 10 then\n 42\n 23\n end\n", 23))
suite.append(Test("if b == 10 then if a == 5 then 5 end end", 5)) #13h05 : marche !
suite.append(Test("while b < 100 do b += 1 ; if b == 20 then break end end", None))
suite.append(Test("b", 20))
st = """
    while b < 100
        b += 1
        if b == 30
            break
        end
    end
"""
suite.append(Test(st, None)) # 14h53
suite.append(Test("b", 30))
st = """
    fun hello
        "hello"
    end
"""
suite.append(Test(st, None))
suite.append(Test("[1,2,3]", [1,2,3]))

scope = {}
stack = []
good = 0
for elem in suite:
    #print elem.__class__
    elem.test(stack, scope)
    #print elem.__class__
    print elem
    #print elem.__class__
    if elem.is_ok():
        good+=1

print
print '-- Stack'
print

i = 0
for s in stack:
    print i, '.', s
    i += 1

print
print "%s / %s" % (str(good), str(len(suite)))

print
print 'Goodbye'

#LineType = Enum('Unknown', 'Empty', 'Expression', 'Affectation')

#def execute(sta):
#    tol = type_of_line(sta)
#    print '[', tol, ']',
#    for t in sta:
#        print t.val,
#    print
#    if tol == LineType.Affectation:
#        n = Node(kind='Expr', val=sta[2:])
#        return Node(kind='Aff', target=sta[0].val, expr=n)
#
#def type_of_line(statement):
#    if len(statement) == 0:
#        return LineType.Empty
#    elif statement[0].kind == 'id':
#        if len(statement) == 1:
#            return LineType.Expression
#        elif is_aff_operator(statement[1].val):
#            return LineType.Affectation
#    return LineType.Unknown
#
#i = 0
#todo = []
#while tokens[i].kind != 'EOF' and i < len(tokens):
#    if not tokens[i].val in [';', '\n']:
#        todo.append(tokens[i])
#    else:
#        r = execute(todo)
#        if r is not None: r.info()
#        todo = []
#    i+=1
