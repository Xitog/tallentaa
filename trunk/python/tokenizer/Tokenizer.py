#-----------------------------------------------------------------------
# Tokenizer
# Damien Gouteux
#-----------------------------------------------------------------------
#
# Parts :
#
# Tools
# Lexer
# Parser
# Interpreter
# Tests
# Interactive Console

debug = False
tests = False

#-----------------------------------------------------------------------
# Tools
#-----------------------------------------------------------------------

class Enum:
    def __init__(self, *tab):
        self.tab = tab
        i = 0
        for t in tab:
            setattr(self, t, t)

LexerState = Enum('start', 'float', 'integer', 'operator', 'id', 'hexa', 'bin', 'octal', 'string')
TokenType = Enum('integer', 'float', 'id', 'operator', 'separator','keyword', 'eof', 'boolean', 'string')

#-----------------------------------------------------------------------
# Lexer
#-----------------------------------------------------------------------

# Tokens

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
    return (c in [',', '+', '-', '/', '*', '%', '>', '<', '=', '!', '&', '^', '|'])

def is_sep_char(c):
    return (c in [';', '(', ')', '[', ']', '{', '}', '\n'])

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
    return (s in ['if', 'then', 'else', 'elsif', 'end', 'while', 'do', 'until', 'unless', 'break', 'next', 'return', 'fun'])

all_keywords = ['if', 'then', 'else', 'elsif', 'end', 'while', 'do', 'until', 'unless', 'break', 'next', 'return', 'fun'] + ['true', 'false']

class Token:
    def __init__(self, kind, val):
        self.kind = kind
        self.val = val
    def __str__(self):
        return 'Token: %s : %s' % (self.val, self.kind)

class Tokenizer:
    def __init__(self):
        self.restart()
    
    def restart(self):
        self.text = ''
        self.tokens = []
        self.curr = []
        self.state = 'start'
        
    def next(self, i):        
        i+=1
        if i < len(self.text):
            c = self.text[i]
        else:
            c = '\0'
        return (i,c)
    
    def token(self, typ):
        self.tokens.append(Token(typ, ''.join(self.curr)))
        self.curr = []
        self.state = LexerState.start
    
    def parse(self, s):
        self.text = s
        
        escape = False
        i = 0
        if len(s) > 0:
            c = s[i]
        else:
            c = '\0'
        
        while not escape:
            if c == '\0': # last turn
                escape = True
            if self.state == LexerState.start:
                if is_char(c) or c == '$' or c == '@' or c == '_':
                    self.state = LexerState.id
                    #
                    self.curr.append(c)
                    i, c = self.next(i)
                elif is_digit(c):
                    self.state = LexerState.integer
                    #
                    self.curr.append(c)
                    i, c = self.next(i)
                elif c == '"':
                    self.state = LexerState.string
                    i, c = self.next(i)
                elif c == '.': # '.' can be for a float or an operator
                    state = LexerState.float
                    self.curr.append(c)
                    i, c = self.next(i)
                elif is_ops_char(c):
                    self.state = LexerState.operator
                    #
                    self.curr.append(c)
                    i, c = self.next(i)
                elif is_sep_char(c):
                    self.curr.append(c)
                    i, c = self.next(i)
                    self.token(TokenType.separator)
                elif c == '#':
                    end = False
                    while (not escape) and (not end):
                        i, c = self.next(i)
                        if c == ';' or c == '\n':
                            end = True
                elif is_silent(c):
                    i, c = self.next(i)
                elif c == '\0':
                    pass # ????
                else:
                    raise Exception('Forbidden character: [%s]' % (str(c),))
            elif self.state == LexerState.id:
                if (is_char(c) or is_digit(c) or c == '_') or (c == '@' and len(self.curr) == 1):
                    self.curr.append(c)
                    i, c = self.next(i)
                else:
                    #print '>>> [', ''.join(curr), ']', is_boolean(''.join(curr))
                    if is_keyword(''.join(self.curr)):
                        self.token(TokenType.keyword)
                    elif is_boolean(''.join(self.curr)):
                        self.token(TokenType.boolean)
                    else:
                        self.token(TokenType.id)
            elif self.state == LexerState.integer:
                if is_digit(c):
                    self.curr.append(c)
                    i, c = self.next(i)
                elif self.curr == ['0'] and (c == 'x' or c == 'X'):
                    self.state = LexerState.hexa
                    self.curr.append(c)
                    i, c = self.next(i)
                elif self.curr == ['0'] and (c == 'c' or c == 'C'):
                    self.state = LexerState.octal
                    self.curr.append(c)
                    i, c = self.next(i)
                elif self.curr == ['0'] and (c == 'b' or c == 'B'):
                    self.state = LexerState.bin
                    self.curr.append(c)
                    i, c = self.next(i)
                elif c == '.':
                    self.state = LexerState.float
                    self.curr.append(c)
                    i, c = self.next(i)
                else:
                    self.token(TokenType.integer)
            elif self.state == LexerState.float:
                if is_digit(c):
                    self.curr.append(c)
                    i, c = self.next(i)
                elif len(self.curr) == 1: # We have a lonely '.'
                    self.token(TokenType.operator)        
                else:
                    self.token(TokenType.float)
            elif self.state == LexerState.octal:
                if is_octaldigit(c):
                    self.curr.append(c)
                    i, c = self.next(i)
                elif is_hexadigit(c):
                    raise Exception("Mismatched integer")
                else:
                    self.token(TokenType.integer)
            elif self.state == LexerState.bin:
                if is_bindigit(c):
                    self.curr.append(c)
                    i, c = self.next(i)
                elif is_hexadigit(c):
                    raise Exception("Mismatched integer")
                else:
                    self.token(TokenType.integer)
            elif self.state == LexerState.hexa:
                if is_hexadigit(c):
                    self.curr.append(c)
                    i, c = self.next(i)
                elif is_char(c):
                    raise Exception("Mismatched integer")
                else:
                    self.token(TokenType.integer)
            elif self.state == LexerState.operator:
                if is_ops_char(c) and is_operator((''.join(self.curr))+c):
                    self.curr.append(c)
                    i, c = self.next(i)
                else:
                    self.token(TokenType.operator)
            elif self.state == LexerState.string:
                if c != '"' and (len(self.curr) < 2 or self.curr[len(self.curr)-1] != '\\'):
                    self.curr.append(c)
                    i, c = self.next(i)
                else:
                    i, c = self.next(i)
                    self.token(TokenType.string)
    
        self.curr = ['eof']
        self.token(TokenType.eof)
        
        return self.tokens
        
#-----------------------------------------------------------------------
# Parser (from tokens[] to Ast)
#-----------------------------------------------------------------------

class Parser:
    def __init__(self):
        pass
    
    def parse(self, tokens, debug=False):
        blocks = self.identify_block(tokens)
        if debug:
            for b in blocks:
                print b
        n = None
        master = None
        for b in blocks:
            if b['type'] in ['if', 'unless']:
                sel_cond = self.make_ast(tokens[b['start']+1:b['middle']])
                sel_action = self.parse(tokens[b['middle']+1:b['end']])
                n = Node(kind='if', cond=sel_cond, action=sel_action, invert=(b['type'] == 'unless'))
            elif b['type'] in ['while', 'until']:
                iter_cond = self.make_ast(tokens[b['start']+1:b['middle']])
                iter_action = self.parse(tokens[b['middle']+1:b['end']])
                n = Node(kind='while', cond=iter_cond, action=iter_action, invert=(b['type'] == 'until'))
            elif b['type'] == 'expression':
                if b['start'] > b['end']:
                    n = Node(kind='empty')
                else:
                    if debug:
                        print 'tokens'
                        i = 0
                        for tt in tokens:
                            print i, tt, tt in tokens[b['start']:b['end']+1]
                            i+=1
                        print b['start'], b['end']
                    n = self.make_ast(tokens[b['start']:b['end']+1])
            elif b['type'] in ['{', '[']: # '(', 
                if b['start'] > b['end']:
                    n = Node(kind='suite', subkind='sequence', subsubkind=b['type'], left=None, right=None)
                else:
                    r = None
                    i = b['start']
                    end_i = i
                    while i <= b['end']:
                        while tokens[end_i].val != ',' and end_i <= b['end']:
                            if debug:
                                print end_i
                            end_i += 1
                        if tokens[end_i].val in [',',']','}']: # ')',
                            n = self.make_ast(tokens[i:end_i])
                        else:
                            n = self.make_ast(tokens[i:end_i+1])
                        i = end_i + 1
                        end_i = i
                        if r is None:
                            r = Node(kind='suite', subkind='sequence', subsubkind=b['type'], left=n, right=None)
                        else:
                            r = Node(kind='suite', subkind='sequence', subsubkind=b['type'], left=n, right=r)
                    n = r
            elif b['type'] == 'empty':
                n = Node(kind='empty')
            elif b['type'] == 'break':
                n = Node(kind='break')
            elif b['type'] == 'fun':
                x = b['start']
                deb_par = 0
                end_par = 0
                while x < b['middle']:
                    if tokens[x].val == '(':
                        deb_par = x
                    elif tokens[x].val == ')':
                        end_par = x
                    x += 1
                i=0
                for tt in tokens[deb_par:end_par+1]:
                    i+=1
                if end_par > deb_par:
                    fun_param = self.make_ast(tokens[deb_par:end_par+1])
                else:
                    fun_param = Node(kind='empty')
                fun_ret = None
                fun_action = self.parse(tokens[b['middle']+1:b['end']])
                n = Node(kind='fun', name=tokens[b['start']+1].val, param=fun_param, ret=fun_ret, action=fun_action)
            if master is None:
                master = Node(kind='suite', subkind='statement', left=n, right=None)
            elif n.kind != 'empty':
                master = Node(kind='suite', subkind='statement', left=master, right=n)
        return master
    
    def identify_block(self, tokens):
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
                elif t.kind in [TokenType.id, TokenType.float, TokenType.integer, TokenType.string, TokenType.boolean] or t.val == '(' or t.val == '-':
                    block_mode = 'expression'
                    start = i
                elif t.val in ['{', '[']: #'(', 
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
            elif block_mode in ['{', '[']: # '(', (block_mode == '(' and t.val == ')')
                if t.val == block_mode:
                    level += 1
                elif (block_mode == '{' and t.val == '}') or (block_mode == '[' and t.val == ']'):
                    level -= 1
                if level == 0:
                    blocks.append({'type' : block_mode, 'start' : start+1, 'end' : i-1})
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
        
        #print 'blocks'
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
    
    def clear(self, tokens):
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

    def make_ast(self, tokens):
        ###
        if debug:
            print 'make_ast'
            i=0
            for t in tokens:
                print 'make_ast', i, t
                i+=1
        
        if len(tokens) < 1:
            raise Exception("Empty token list")
        #elif len(tokens) == 1 and tokens.kind == TokenType.eof: # only eof inside
        #    tokens[0] = Node(kind='empty')
        
        prio = {
            '->':  1, '=' :  1, '+=':  1, '-=':  1,
            ',' : 1.5, '(': 2,
            '==': 5, '!=': 5, '<' : 5, '<=': 5, '>' : 5, '>=': 5,
            '-':6, '+':6, '*':7, '/':7, '//':7, '%':7, '**':7,
            'unary_minus' : 8,
            }
        ts = {
            TokenType.id : 'id', 
            TokenType.integer : 'integer', 
            TokenType.float : 'float', 
            TokenType.boolean : 'boolean', 
            TokenType.string : 'string' }
        # Litterals and removing the last (if any)
        i = 0
        if debug:
            for t in tokens:
                print '#-#', t
        while i < len(tokens):
            t = tokens[i]
            if t.kind in ts:
                tokens[i] = Node(kind=ts[t.kind], val=t.val)
            if t.kind == TokenType.eof:
                del tokens[i]
            #if isinstance(t, Token):
            #    print '###', isinstance(t, Token), t.val, t.val == '-'
            if isinstance(t, Token) and t.val == '-':
                if i == 0 or tokens[i-1].kind in [TokenType.operator]:
                    #print 'found one'
                    t.val = 'unary_minus'
            i+=1
        while len(tokens) > 1:
            i = 0
            max = None
            level_max = 1
            level = 1
            while i < len(tokens):
                t = tokens[i]
                if isinstance(t, Token):
                    
                    if t.val == '(':
                        level *= 10
                    elif t.val == ')':
                        level /= 10
                    if t.val in prio:
                        if max is None or prio[tokens[max].val]*level_max < prio[t.val]*level:
                            max = i
                            level_max = level
                i+=1
            if not max is None and tokens[max].val == 'unary_minus':
                n = Node(kind='unaop',op=tokens[max].val, arg=tokens[max+1])
                tokens[max] = n
                del tokens[max+1]
            elif not max is None and tokens[max].val != '(':
                n = Node(kind='binop',op=tokens[max].val,arg1=tokens[max-1],arg2=tokens[max+1])
                tokens[max] = n
                if len(tokens) <= max+1:
                    raise Exception('Incorrect expr right')
                if max == 0:
                    raise Exception('Incorrect expr left')
                del tokens[max+1]
                del tokens[max-1]
            elif not max is None and tokens[max].val == '(':
                deb = max+1
                end = deb
                level = 1
                while end < len(tokens) and level > 0:
                    if isinstance(tokens[end], Token) and tokens[end].val == ')':
                        level -= 1
                    elif isinstance(tokens[end], Token) and tokens[end].val == '(':
                        level += 1
                        end += 1
                    else:
                        end += 1
                if tokens[end].val != ')':
                    raise Exception('Incorrect ()')
                else:
                    end -= 1
                if deb == end:
                    n = self.make_ast([tokens[deb]])
                    del tokens[end+1]
                    del tokens[deb-1]
                elif deb == end+1:
                    n = Node(kind='empty')
                    tokens[deb] = n
                    del tokens[deb-1]
                else:
                    if debug:
                        print '%%%%%%%', end
                    i = deb
                    sub = deb # sub start
                    n = None
                    while i <= end+1:
                        if debug:
                            print 'www', tokens[i], tokens[i] in tokens[sub:i]
                        if isinstance(tokens[i], Token) and tokens[i].val in [',',')']:
                            n = Node(kind='suite', subkind='sequence', subsubkind='(', left=self.make_ast(tokens[sub:i]), right=n)
                            sub = i+1 # DERNIER BUG. PASSER DE VIRG EN VIRG
                        i+=1
                    
                    ii = end+1
                    while ii > deb:
                        if debug:
                            print 'i delete', ii
                        del tokens[ii]
                        ii -= 1
                    tokens[deb] = n
                    del tokens[deb-1]
                
                # 'operator' 'separator' 'keyword' 'eof'
                # Call 0028 unknown op
                if max-1>=0:
                    if isinstance(tokens[max-1], Node) and tokens[max-1].kind in ['integer', 'float', 'id', 'boolean', 'string']:
                        n = Node(kind='binop', op='call', arg1=tokens[max-1],arg2=tokens[max])
                        tokens[max-1] = n
                        del tokens[max]
                
                if debug:
                    print '------------'
                    i=0
                    for tt in tokens:
                        print i, tt
                        i+=1
                    print '------------'
                
                    if len(tokens) == 1 and tokens[0].kind == 'binop':
                        print 'op=', tokens[0].op
                        if tokens[0].op == 'call':
                            print tokens[0].arg1
                            print tokens[0].arg2
                            if tokens[0].arg2.kind == 'suite':
                                print tokens[0].arg2.left
                                print tokens[0].arg2.right
            else:
                print 'ALARMA'
                for tt in tokens:
                    print tt
                raise Exception('Prio not found')
        return tokens[0]

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


#-----------------------------------------------------------------------
# Interpreter
#-----------------------------------------------------------------------

# Standard lib

def node2list_formal(ast):
    parcours = ast
    if isinstance(parcours, Node):
        r = []
        if parcours.kind == 'empty':
            pass
        elif parcours.kind == 'suite':
            while parcours is not None:
                if parcours.left.kind == 'id':
                    r.append(SParam(parcours.left.val)) #var,card,def
                else:
                    raise Exception('not id')
                parcours = parcours.right
        else:
            if parcours.kind == 'id':
                r.append(SParam(parcours.val))
            else:
                raise Exception('Not a suite, not empty, not id')
    else:
        raise Exception('Not a node')
    return r

def node2list(ast, scope):
    if isinstance(ast, Node):
        r = []
        parcours = ast
        if parcours.kind == 'empty':
            pass
        elif parcours.kind == 'suite':
            while parcours is not None:
                r.append(interpreter.do_node(parcours.left, scope, True))
                parcours = parcours.right
        elif parcours.kind in ['integer', 'float', 'boolean', 'string', 'id']:
            r.append(interpreter.do_node(parcours, scope, True))
        return r
    else:
        raise Exception ('node2list error: not a Node')

class SInteger(int):
    def __new__(cls, *args, **kwargs):
        return  super(SInteger, cls).__new__(cls, args[0])

class SParam:
    
    def __init__(self, name, typ='var', card='1', default=None):
        self.name = name
        self.typ = typ
        self.card = card
        self.default = None

class SFunction:
    
    def __init__(self, name, formals, rettype, code):
        self.name = name
        self.formals = formals
        self.rettype = rettype
        self.code = code
    
    def __str__(self):
        return '%s/%d' % (self.name, len(self.formals))

    def do(self, interpreter, scope, reals):
        fun_scope = scope.copy()
        if len(reals) != len(self.formals):
            raise Exception('Wrong number of parameters: %i / %i' % (len(reals), len(self.formals)))
        parameters = {}
        i = 0
        for p in self.formals:
            parameters[p.name] = reals[i]
            i+=1
        if isinstance(self.code, Node):
            fun_scope.update(parameters)
            #for s in fun_scope:
            #   print s
            return interpreter.do_node(self.code, fun_scope, True)
        else:
            return self.code(fun_scope, parameters)  

global_scope = {}

def base_println(scope, par):
    global global_scope
    i = 0
    for e in par:
        sys.stdout.write(str(par[e]))
        i += len(str(par[e]))
    sys.stdout.write("\n")
    #i+=1
    return i

def base_print(scope, par):
    global global_scope
    i = 0
    for e in par:
        sys.stdout.write(str(par[e]))
        i += len(str(par[e]))
    return i

global_scope['println'] = SFunction('println', [SParam('a',card='*')], 'int', base_println)
global_scope['print'] = SFunction('print', [SParam('a',card='*')], 'int', base_print)

class Interpreter:

    def __init__(self, scope=[]):
        self.scope = scope
        self.MASTER_LOOP_EXIT = False

    def do_string(self, s, stack=[], scope={}):
        t = Tokenizer()
        tokens = t.parse(s)
        p = Parser()
        p.clear(tokens)
        master = p.parse(tokens)
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
        elif n.kind == 'unaop':
            self.process_vm(n.arg, start)
            start.append('INVERT')
        elif n.kind == 'binop':
            dop = {'+' : 'ADD', '*' : 'MUL', '-' : 'SUB', '/' : 'DIV', '//' : 'INTDIV', '**' : 'POW', '%' : 'MOD', '<' : 'LT', '>' : 'GT', '>=' : 'GE', '<=' : 'LE', '!=' : 'NE', '==' : 'EQ', '=' : 'AFF', '+=' : 'AFF_ADD', '-=' : 'AFF_SUB', '->' : 'CONST', 'call' : 'CALL' }
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
            if n.subsubkind in ['[','(']:
                r = []
                while n is not None:
                    if n.left is not None: # empty list
                        r.append(self.do_node(n.left, scope, True))
                    n = n.right
                r.reverse()
                return r
            elif n.subsubkind in ['{']:
                r = {}
                return r # 23h33 yeah en qwerty 69/69
        elif n.kind == 'unaop':
            a = self.do_node(n.arg, scope)
            if isinstance(a, str) and n.arg.kind == 'id':
                ida = a #unused
                a = scope[a]
            if isinstance(a, int) or isinstance(a, float):
                return -a
            else:
                raise Exception('Invalid type for unary minus : %s' % (a.__class__,))
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
                    scope[ida] = SInteger(b)
                scope[ida].frozen = True
                return scope[ida]
            elif n.op == 'call':
                #if n.arg1.kind == 'id' and n.arg1.val == 'println':
                #    print self.do_node(n.arg2)
                if n.arg1.kind == 'id' and n.arg1.val in scope:
                    identifier = n.arg1.val
                    if isinstance(scope[identifier], SFunction):
                        par = node2list(n.arg2, scope)
                        return scope[identifier].do(self, scope, par)
                    else:
                        raise Exception('not callable')
                else:
                    print 'ERROR', n.arg1.kind, n.arg1.kind == 'id'
                    print 'ERROR', n.arg1.val, n.arg1.val in scope
                    raise Exception('function call not handled')
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
        elif n.kind == 'break':
            self.MASTER_LOOP_EXIT = True
        elif n.kind == 'fun':
            l_parameters = node2list_formal(n.param)
            new_fun = SFunction(n.name, l_parameters, n.ret, n.action)
            scope[n.name] = new_fun
            return new_fun
        elif n.kind == 'empty':
            return None
        else:
            raise Exception('Node type not handled %s' % (n.kind,))

#-----------------------------------------------------------------------
# Tests
#-----------------------------------------------------------------------

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

interpreter = Interpreter()
Test.setup(interpreter)

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
    hello()
"""
suite.append(Test(st, 'hello'))
suite.append(Test("[1,2,3]", [1,2,3]))
#suite.append(Test("(1, 2, 3)", [1,2,3]))
suite.append(Test("(1)", 1)) #0054
suite.append(Test("(1+2)", 3))
suite.append(Test("println(23)", 2)) #0031
suite.append(Test("1 + (3)", 4)) #0036
suite.append(Test("2 * 4 + 5", 13))
suite.append(Test("5 + 4 * 2", 13))
suite.append(Test("2 * (4 + 5)", 18))
suite.append(Test("(5 + 4) * 2", 18)) #0108 PUREE level_max et test pour savoir avant max-1>=0
suite.append(Test("(5 * (5 + 2))", 35)) #0112 PREMIERE FAUTE D ENTREE SUR OUBLI DE PAR !!!
suite.append(Test("(2+3)*(1+1)", 10))
suite.append(Test('println("hello")', 5))
suite.append(Test('hello()', "hello")) # appel d'une fonction !!!
st = """
    fun add(i, j)
        i + j
    end
    println(add)
"""
suite.append(Test(st, 5))
suite.append(Test('add(2,3)', 5)) #2h32. Vendredi (matin) 6 Janvier 2012. Enfin. Oui... Oui... Oui... Depuis 00h00...
suite.append(Test('2 * add(2,3)', 10)) # 2h32 aussi.
suite.append(Test('add(2,3)+add(3,2)', 10)) # 2h36 (sans rien faire)
suite.append(Test('add(1+1, 2+1)', 5)) # 2h37 (un petit bug)
suite.append(Test('-3', -3))
suite.append(Test('-(3+2)', -5))
suite.append(Test('-(3+2)*4', -20))

scope = global_scope.copy()
stack = []

def all_tests():
    global suite, scope, stack
    good = 0
    for elem in suite:
        elem.test(stack, scope)
        print elem
        if elem.is_ok():
            good+=1
    
    print
    print '-- Stack'
    print
    
    i = 0
    for s in stack:
        #print i, '.', s
        i += 1
    
    print
    print "%s / %s" % (str(good), str(len(suite)))
    print

if tests:
    all_tests()

#-----------------------------------------------------------------------
# Interactive Console
#-----------------------------------------------------------------------

import sys
import os

# Console On
console = True

# Commands
def com_keywords():
    global all_keywords
    print len(all_keywords), 'keywords:'
    all_keywords.sort()
    for k in all_keywords:
        print '\t', k

def com_help(*args):
    global commands
    if len(args)<=1:
        print len(commands), 'commands:'
        keys = commands.keys()
        keys.sort()
        for k in keys:
            print '\t', k
    elif args[1] == 'if':
        print 'Syntax: if <condition> then <actions> end'
        print 'Execute <actions> if <condition> is true.'
        print 'See also: unless'
        print 'Alternative: do can be replaced by a new line.'
    elif args[1] == 'unless':
        print 'Syntax: unless <condition> then <actions> end'
        print 'Execute <actions> if <conditions> is false.'
        print 'unless = if not'
        print 'See also: if'
        print 'Alternative: do can be replaced by a new line.'
    elif args[1] == 'fun':
        print 'Syntax: fun <name> (<parameter list>) do <actions> end'
        print 'Store <actions> in order be called later under the name <name>.'
        print 'Alternative: do can be replaced by a new line.'
    else:
        print 'no help for', args[1]

def com_tests():
    all_tests()

def com_clear():
    os.system('cls')

def com_exit():
    pass

def com_tokens():
    global previous
    t = Tokenizer()
    tokens = t.parse(previous)
    i = 0
    for t in tokens:
        print "%i. %s" % (i, str(t))
        i+=1

def com_blocks():
    global previous
    t = Tokenizer()
    tokens = t.parse(previous)
    p = Parser()
    p.clear(tokens)
    p.parse(tokens, True)
    
command = ''
previous = ''
commands = { 'keywords' : com_keywords, 'help' : com_help, 'exit' : com_exit, 'tests' : com_tests, 'clear' : com_clear, 'tokens' : com_tokens, 'blocks' : com_blocks}

def clos(command):
    t = Tokenizer()
    tokens = t.parse(command)
    if tokens[0].val == 'help': return True
    cdeb = 0
    cend = 0
    for t in tokens:
        if t.val in ['if','unless','while','until','fun']:
            cdeb+=1
        elif t.val == 'end':
            cend+=1
    return cdeb == cend
    
if console:
    ver = sys.version_info
    print '+- Welcome to Pypo 0.1 on Python %i.%i' % (ver[0], ver[1])
    print '+- Enter code or type help for more information.'
    while command != 'exit':
        command = raw_input('>>> ') # +->
        while not clos(command):
            command += '\n' + raw_input('... ')
        if not(command in commands) and not(command.split(' ')[0] in commands):
            #try:
                r = interpreter.do_string(command, stack, scope)
                print r
                scope['_'] = r
            #except Exception as e:
            #    print e
            #finally:
                previous = command
        elif command in commands:
            commands[command]()
        elif command.split(' ')[0] in commands:
            commands[command.split(' ')[0]](*command.split(' '))

print '+- Goodbye!'
print
