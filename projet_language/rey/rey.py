import os.path

#-------------------------------------------------------------------------------
# Tokenizer/Lexer
#-------------------------------------------------------------------------------

class Token:
    
    NUM = 0
    ID = 1
    STR = 2
    NL = 3
    OP = 4
    SEP = 5
    KW = 6
    
    def __init__(self, typ, val):
        self.typ = typ
        self.val = val
    
    @classmethod
    def typ2str(cls, typ):
        if typ == Token.NUM:
            return "Number"
        elif typ == Token.ID:
            return "Identifier"
        elif typ == Token.STR:
            return "String"
        elif typ == Token.NL:
            return "New line"
        elif typ == Token.OP:
            return "Operator"
        elif typ == Token.SEP:
            return "Separator"
        elif typ == Token.KW:
            return "Keyword"
    
    def __str__(self):
        return f":{Token.typ2str(self.typ)}: [{self.val}]"

class Tokenizer:
    
    START_OF_ID = ['@', '_']
    START_OF_STRING = ['"', "'"]
    
    SEPARATORS = [
        '(', ')', '[', ']', '{', '}',
        ',', ';',
    ]
    
    OPERATORS = [
        '+', '-', '*', '/', '%', '**', '//',
        '=', '+=', '-=', '*=', '/=', '%=', '**=', '//=',
        '==', '!=', '>', '>=', '<=', '<',
        'and', 'or', 'not', 'xor',
        'not', 'in',
        '.', '..', '..<',
        ':', '|', '->'
    ]

    KEYWORDS = [
        'if', 'then', 'elif', 'else', 'end',
        'while', 'do',
        'for', 'in',
        'break', 'next',
        'new',
        'fun', 'sub', 'get', 'set',
        'return',
        'class',
    ]

    BLOCK_PLUS = [ 'if', 'for', 'while', 'fun', 'sub', 'get', 'set', 'class' ]
    BLOCK_LESS = [ 'end' ]
    LINE_LESS =  [ 'elif' ]
    
    def __init__(self):
        self.tokens = []
        self.line_count = 0
        Tokenizer.START_OF_OPERATOR = []
        for op in Tokenizer.OPERATORS:
            if not op[0].isalpha() and op[0] not in Tokenizer.START_OF_OPERATOR:
                Tokenizer.START_OF_OPERATOR.append(op[0])
        self.debug = False
        self.block_level = 0
        
    def read_num(self, line, index):
        if self.debug:
            print("    " + f'Reading number at {index}, line {self.line_count}, starting with [{line[index]}]')
        word = line[index]
        suspended = False
        index += 1
        while index < len(line) and (line[index].isdigit() or line[index] == '_'):
            if suspended:
                raise Exception("Twice _ following in number at line " + str(self.line_count))
            if line[index] == '_':
                suspended = True
            else:
                suspended = False
                word += line[index]
            index += 1
        t = Token(Token.NUM, word)
        if self.debug:
            print("    " + f'Creating token {t} n°{len(self.tokens)}')
        self.tokens.append(t)
        return index

    def read_id(self, line, index):
        if self.debug:
            print("    " + f'Reading id at {index}, line {self.line_count}, starting with [{line[index]}]')
        word = line[index]
        terminate = False
        index += 1
        while index < len(line) and (line[index].isalnum() or line[index] in ['_', '!', '?']):
            if terminate:
                raise Exception("Wrong ID with ! or ? inside of it at line " + str(self.line_count))
            if line[index] in ['!', '?']:
                terminate = True
            word += line[index]
            index += 1
        if word in Tokenizer.OPERATORS:
            t = Token(Token.OP, word)
        elif word in Tokenizer.KEYWORDS:
            t = Token(Token.KW, word)
        else:
            t = Token(Token.ID, word)
        if self.debug:
            print("    " + f'Creating token {t} n°{len(self.tokens)}')
        self.tokens.append(t)
        # Handling of block level only for display!
        if t.val in Tokenizer.BLOCK_PLUS:
            self.block_level += 1
        elif t.val in Tokenizer.BLOCK_LESS:
            self.block_level -= 1
            self.line_level -= 1
        elif t.val in Tokenizer.LINE_LESS:
            self.line_level -= 1
        return index

    def read_operator(self, line, index):
        if self.debug:
            print("    " + f'Reading operator at {index}, line {self.line_count}, starting with [{line[index]}]')
        operator = line[index]
        index += 1
        while index < len(line) and line[index] in Tokenizer.START_OF_OPERATOR:
            operator += line[index]
            index += 1
        if operator not in Tokenizer.OPERATORS:
            raise Exception("Operator unknown: " + operator + " at line " + str(self.line_count))
        t = Token(Token.OP, operator)
        if self.debug:
            print("    " + f'Creating token {t} n°{len(self.tokens)}')
        self.tokens.append(t)
        return index
    
    def read_separator(self, line, index):
        if self.debug:
            print("    " + f'Reading separator at {index}, line {self.line_count}, starting with [{line[index]}]')
        t = Token(Token.SEP, line[index])
        if self.debug:
            print("    " + f'Creating token {t} n°{len(self.tokens)}')
        self.tokens.append(t)
        return index+1
    
    def read_string(self, line, index):
        if self.debug:
            print("    " + f'Reading string at {index}, line {self.line_count}, starting with [{line[index]}]')
        terminator = line[index]
        index += 1
        escaped = False
        word = ''
        while index < len(line) and ((not escaped) and line[index] != terminator):
            if line[index] == '\\' and not escaped:
                escaped = True
            else:
                escaped = False
            word += line[index]
            index += 1
        if index >= len(line):
            raise Exception("Terminator char not found for string!")
        t = Token(Token.STR, word)
        if self.debug:
            print("    " + f'Creating token {t} n°{len(self.tokens)}')
        self.tokens.append(t)
        return index+1
    
    def tokenize(self, source, debug=False):
        self.debug = debug
        self.tokens.clear()
        self.block_level = 0
        if os.path.isfile(source):
            source = open(source, 'r', encoding='utf8').readlines()
        else:
            source = source.split('\n')
        skip = False
        for line in source:
            self.line_level = self.block_level
            self.line_count += 1
            line = line.strip()
            if len(line) >= 2:
                if line.startswith('--'):
                    continue
                elif line.startswith('=='):
                    skip = not skip
                    continue
                elif skip:
                    continue
            elif len(line) == 1:
                if line[0] == '\n':
                    continue
            elif not line:
                continue
            # analyze line
            if self.debug:
                print('>>>', line)
            index = 0
            word = None
            while index < len(line):
                char = line[index]
                if char.isdigit():
                    index = self.read_num(line, index)
                elif char.isalpha() or char in Tokenizer.START_OF_ID:
                    index = self.read_id(line, index)
                elif char.isspace():
                    index += 1
                elif char in Tokenizer.START_OF_STRING:
                    index = self.read_string(line, index)
                elif char in Tokenizer.START_OF_OPERATOR:
                    index = self.read_operator(line, index)
                elif char in Tokenizer.SEPARATORS:
                    index = self.read_separator(line, index)
                else:
                    raise Exception("What to do with: " + char + "?")
            self.tokens.append(Token(Token.NL, "Newline"))
            # Pretty print
            if not self.debug:
                print('>>>', "    " * self.line_level, line)
        if self.debug:
            print(f'{len(self.tokens)} tokens created.')
        return self.tokens

#-------------------------------------------------------------------------------
# Parser
#-------------------------------------------------------------------------------

# Model

class AST:

    def __init__(self):
        self.root = Block()

    def __str__(self):
        return self.root.to_s()

class Block:

    def __init__(self):
        self.actions = []

    def add(self, action):
        self.actions.append(action)

    def to_s(self, level=0):
        output = "block\n"
        for elem in self.actions:
            output += elem.to_s(level+1)
        return output

class Terminal:
    
    def __init__(self, content):
        self.content = content
    
    def to_s(self, level=0):
        return str(self.content)
    
    def __str__(self):
        return self.to_s()

class Operation:
    
    def __init__(self, left, op, right):
        assert type(op) == Terminal and op.content.typ == Token.OP, "Operator should be of type Token.OP"
        self.left = left
        self.right = right
        self.op = op
    
    def to_s(self, level=0):
        name = "binop" if self.left is not None and self.right is not None else "unaop"
        return "    " * level + f"{name} {self.left} {self.op} {self.right} \n"

class If:

    def __init__(self, cond, action, alter):
        self.cond = cond
        self.action = action
        self.alter = alter

    def to_s(self, level=0):
        if self.alter is not None:
            return "    " * level + f"if {self.cond} then \n" + self.action.to_s(level+1) + "    " * level + "end \n"

class Parser:
    
    def __init__(self):
        pass
    
    def read_if(self, tokens, index):
        return 99

    def read_while(self, tokens, index):
        return 99

    def read_for(self, tokens, index):
        return 99

    def read_expr(self, tokens, index):
        if len(tokens) <= index:
            raise Exception("Unfinished expression")
        elif len(tokens) > index + 1:
            if tokens[index + 1].typ == Token.OP:
                node = Operation(Terminal(tokens[index]), Terminal(tokens[index + 1]), Terminal(tokens[index + 2]))
                return index + 3 + 1, node # +1 for NL :TODO: Better handling
            else:
                return 99, None #raise Exception("Non valid expression: " + str(tokens[index]))
    
    def parse(self, tokens):
        if tokens is None:
            raise Exception("tokens is None!")
        index = 0
        ast = AST()
        while index < len(tokens):
            if tokens[index].typ == Token.KW:
                if tokens[index].val == 'if':
                    index = self.read_if(tokens, index)
            elif tokens[index].typ in [Token.NUM, Token.ID]:
                index, n = self.read_expr(tokens, index)
                ast.root.add(n)
            else:
                raise Exception("What to do? tokens = " + str(tokens[index]))
        return ast

#-------------------------------------------------------------------------------
# Transpiler
#-------------------------------------------------------------------------------

class TranspilerPython:
    
    def __init__(self):
        pass
    
    def transpile(self, ast):
        pass

#-------------------------------------------------------------------------------
# Interpreter
#-------------------------------------------------------------------------------

class Interpreter:
    
    def __init__(self):
        pass
        
    def do_elem(self, elem):
        if type(elem) == Operation:
            if elem.op.content.val == '+':
                return self.do_elem(elem.left) + self.do_elem(elem.right)
            elif elem.op.content == '-':
                return self.do_elem(elem.left) - self.do_elem(elem.right)
            else:
                raise Exception("Operator not known: " + elem.op.content.val)
        elif type(elem) == Terminal:
            if elem.content.typ == Token.NUM:
                return int(elem.content.val)
            else:
                raise Exception("Terminal not known:" + Token.typ2str(elem.content.typ))
        else:
            raise Exception("Elem not known")
    
    def do(self, ast):
        last = None
        for elem in ast.root.actions:
            last = self.do_elem(elem)
        return last #18h59 8/9

#-------------------------------------------------------------------------------
# Tests
#-------------------------------------------------------------------------------

print('--- Unitary Test n°1 : Simple Addition ---')
res = Tokenizer().tokenize('5 + 6') # 5 + 6 NL
assert len(res) == 4, "[ERROR] 4 tokens should have been produced! instead:" + str(len(res))
assert type(res[0]) == Token and res[0].val == '5' and res[0].typ == Token.NUM, "[ERROR] Token 1 should be NUM, with the value of '5'"
assert type(res[1]) == Token and res[1].val == '+' and res[1].typ == Token.OP, "[ERROR] Token 2 should be OP, with the value of '+'"
ast = Parser().parse(res)
print(ast)
print(Interpreter().do(ast))
print()

print('--- Unitary Test n°2 : Double Addition ---')
res = Tokenizer().tokenize('5 + 6 \n 2 - 1') # 5 + 6 NL
assert len(res) == 8, "[ERROR] 8 tokens should have been produced! instead:" + str(len(res))
assert type(res[4]) == Token and res[4].val == '2' and res[0].typ == Token.NUM, "[ERROR] Token 4 should be NUM, with the value of '2'"
assert type(res[5]) == Token and res[5].val == '-' and res[5].typ == Token.OP, "[ERROR] Token 5 should be OP, with the value of '-'"
ast = Parser().parse(res)
print(ast)
print()

print('--- Unitary Test n°3 : Simple If ---')
res = Tokenizer().tokenize('a = 5 \n if a == 5 then \n writeln("Hello!") \n end')
assert len(res) == 17, "[ERROR] 17 tokens should have been produced! instead:" + str(len(res))
assert type(res[0]) == Token and res[0].val == 'a' and res[0].typ == Token.ID, "[ERROR] Token 1 should be ID, with the value of 'a'"
ast = Parser().parse(res)
print()

print('--- Unitary Test n°4 : Simple Elif ---')
res = Tokenizer().tokenize('a = 5 \n if a != 5 then \n writeln("Never!") \n elif a == 5 then \n writeln("Hello!") \n end')
assert len(res) == 28, "[ERROR] 28 tokens should have been produced! instead:" + str(len(res))
assert type(res[0]) == Token and res[0].val == 'a' and res[0].typ == Token.ID, "[ERROR] Token 1 should be ID, with the value of 'a'"
ast = Parser().parse(res)
print()

print('--- Unitary Test n°5 : Simple Else ---')
res = Tokenizer().tokenize('a = 8 \n if a != 8 then \n writeln("Never!") \n else \n writeln("Hello!") \n end')
assert len(res) == 24, "[ERROR] 24 tokens should have been produced! instead:" + str(len(res))
assert type(res[0]) == Token and res[0].val == 'a' and res[0].typ == Token.ID, "[ERROR] Token 1 should be ID, with the value of 'a'"
ast = Parser().parse(res)
print()

print('--- Unitary Test n°5 : Simple While ---')
res = Tokenizer().tokenize('target, guess = 1..6.random, 0 \n while target != guess do \n writeln(guess) \n guess += 1 \n end')
ast = Parser().parse(res)
print()

# .. > . (en prio)
# Range#random
# writeln

print('--- File Test n°1 ---')
Tokenizer().tokenize('woolfy.blu')
print()

print('Script has ended.')
