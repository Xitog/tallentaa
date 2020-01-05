"""
    Ash
    ---
    A simple lexer / parser / interpreter / python transpiler for a small language inspired by Lua/Ruby
    - Tokenizer is working ***
    - Parser is *
    - Interpreter is *
    - Python transpiler is _
    - Tests are *
    Developed in 2017

= Working pipe

    Import
    Console
    I.   Symbolizer/lexer/tokenizer [LEXER]    string   -> [tokens]
    II.  Parser                     [PARSER]   [tokens] -> abstract syntax tree (AST)
    III. Interpreter                [EXEC]     AST      -> result
    IV.  Python Transpiler          [TRANS]    AST      -> python source code
    V.   Tests                      [TESTS]
    VI.  Main                       [MAIN]

= Data Model

    TokenType
        name: str
    
    Token
        name: str
        typ: TokenType
    
"""

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

import os.path
import copy # only once for read_expr
import sys # for writing debug info in red for the tests
import traceback

#-------------------------------------------------------------------------------
# Console
#-------------------------------------------------------------------------------

class FallBack:
    def write(self, msg, color):
        sys.stdout.write(msg)


class Console:

    def __init__(self):
        try:
            # Works only in IDLE
            self.out = sys.stdout.shell
        except AttributeError:
            self.out = FallBack()
        self.outputs = []
    
    def error(self, msg):
        self.out.write('[ERROR] ' + str(msg) + '\n', 'COMMENT')

    def info(self, msg):
        self.out.write('[INFO]  ' + str(msg) + '\n', 'DEFINITION')
    
    def put(self, msg):
        self.outputs.append(msg)
        self.out.write(str(msg), 'TODO')

    def puts(self, msg):
        self.outputs.append(msg)
        self.out.write(str(msg) + '\n', 'TODO')


console = Console()

#-------------------------------------------------------------------------------
# I. Symbolizer / Tokenizer / Lexer [LEXER]
#-------------------------------------------------------------------------------

class TokenType:
    
    def __init__(self, name: str):
        self.name = name
    
    def __str__(self):
        return self.name
    
    def __eq__(self, obj):
        if not isinstance(obj, TokenType):
            raise Exception("Can only compare instances of TokenType and not instances of " + str(type(obj)))
        return self.name == obj.name


class Token:
    """
        +typ:enum the type of the token
        +val:string the actual string of the token
    """

    Integer     = TokenType('Integer')
    Float       = TokenType('Float')
    Identifier  = TokenType('Identifier')
    Operator    = TokenType('Operator')
    Separator   = TokenType('Separator')
    Keyword     = TokenType('Keyword')
    NewLine     = TokenType('New Line')
    Boolean     = TokenType('Boolean')
    String      = TokenType('String')
    Comment     = TokenType('Comment')
    Discard     = TokenType('Discard') # Unused
    Error       = TokenType('Error')   # Unused
    EndOfSource = TokenType('End')     # Unused
    
    def __init__(self, typ: TokenType, val: str, start=None):
        self.typ = typ
        self.val = val
        self.start = start
        self.length = len(val)
        self.lvl = 0
    
    def __str__(self):
        if self.start is None or self.length is None:
            return f":{self.typ}: [{self.val}]"
        else:
            return f":{self.typ}: [{self.val}] ({self.start} +{self.length})"

    def __repr__(self):
        return str(self)
    
    def to_s(self, level=1):
        return "    " * level + "{Token} " + str(self)


class Tokenizer:

    NEWLINE = "New line"
    
    START_OF_ID = ['@', '_', '$']
    START_OF_STRING = ['"', "'"]
    END_OF_STRING = ['?', '!']
    
    SEPARATORS = [
        '(', ')', '[', ']', '{', '}',
        '\n',
    ]
    
    OPERATORS = [
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

    KEYWORDS = [
        'if', 'then', 'else', 'elif', 'end', # 'unless'
        'while', 'repeat', 'until', 'do',
        'for', 'in',
        'break', 'next',
        'new',
        'fun', 'sub', 'get', 'set',
        'return',
        'class'
    ]

    BOOLEANS = [
        'true',
        'false'
    ]
    
    def __init__(self, debug = False):
        self.tokens = []
        self.line_count = 0
        Tokenizer.START_OF_OPERATOR = []
        for op in Tokenizer.OPERATORS:
            if not op[0].isalpha() and op[0] not in Tokenizer.START_OF_OPERATOR:
                Tokenizer.START_OF_OPERATOR.append(op[0])
        self.debug = debug
        
    def read_number(self, line, index):
        if self.debug:
            print("    " + f'Reading number at {index}, line {self.line_count}, starting with [{line[index]}]')
        word = line[index]
        suspended = False
        index += 1
        is_float = False
        while index < len(line) and (line[index].isdigit() or line[index] == '_' or line[index] == '.'):
            if line[index] == '_' and suspended:
                raise Exception("Twice _ following in number at line " + str(self.line_count))
            if line[index] == '_':
                suspended = True
            elif line[index] == '.':
                if is_float:
                    raise Exception("Twice . in a number")
                else:
                    # 1..2 => range op
                    if index + 1 < len(line) and line[index + 1] == '.':
                        break
                    else:
                        is_float = True
                        word += '.'
            else:
                suspended = False
                word += line[index]
            index += 1
        if not is_float:
            t = Token(Token.Integer, word, self.counter)
        else:
            t = Token(Token.Float, word, self.counter)
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
            t = Token(Token.Operator, word, self.counter)
        elif word in Tokenizer.KEYWORDS:
            t = Token(Token.Keyword, word, self.counter)
        elif word in Tokenizer.BOOLEANS:
            t = Token(Token.Boolean, word, self.counter)
        else:
            t = Token(Token.Identifier, word, self.counter)
        if self.debug:
            print("    " + f'Creating token {t} n°{len(self.tokens)}, returning index {index}')
        self.tokens.append(t)
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
        t = Token(Token.Operator, operator, self.counter)
        if self.debug:
            print("    " + f'Creating token {t} n°{len(self.tokens)}')
        self.tokens.append(t)
        return index
    
    def read_separator(self, line, index):
        if self.debug:
            print("    " + f'Reading separator at {index}, line {self.line_count}, starting with [{line[index]}]')
        if line[index] == '\n':
            t = Token(Token.NewLine, 'NEWLINE', self.counter) #line[index], self.counter)
        else:
            t = Token(Token.Separator, line[index], self.counter)
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
        while index < len(line) and (escaped or line[index] != terminator):
            if line[index] == '\\' and not escaped:
                escaped = True
            else:
                escaped = False
            word += line[index]
            index += 1
        if index >= len(line):
            raise Exception("Terminator char not found for string!")
        if word == '\\n':
            word = '\n'
        t = Token(Token.String, word, self.counter)
        if self.debug:
            print("    " + f'Creating token {t} n°{len(self.tokens)}')
        self.tokens.append(t)
        return index+1
    
    def tokenize(self, source, debug=False):
        if debug: print('[INFO] Start lexing')
        self.debug = debug
        self.tokens.clear()
        self.counter = 0
        if os.path.isfile(source):
            source = open(source, 'r', encoding='utf8').read()
        index = 0
        word = None
        self.line_position = 0
        self.line_count = 1
        skip_line = False
        while index < len(source):
            char = source[index]
            self.line_position += 1
            if char == '-' and index + 1 < len(source) and source[index + 1] == '-':
                skip_line = True
            if skip_line and char == '\n':
                skip_line = False
                self.line_count += 1
                self.line_position = 0
            elif skip_line:
                index += 1
            else:
                if char.isdigit(): # 0 1 2 3 4 5 6 7 8 9
                    index = self.read_number(source, index)
                elif char.isalpha() or char in Tokenizer.START_OF_ID: # a-z A-Z @ _
                    index = self.read_id(source, index)
                elif char.isspace() and char != '\n': # ' ' \t
                    index += 1
                elif char in Tokenizer.START_OF_STRING:
                    index = self.read_string(source, index)
                elif char in Tokenizer.START_OF_OPERATOR:
                    index = self.read_operator(source, index)
                elif char in Tokenizer.SEPARATORS:
                    index = self.read_separator(source, index)
                else:
                    raise Exception("[TOKENS] What to do with: " + char + " at line " + str(self.line_count) + " pos " + str(self.line_position))
        if self.debug:
            print(f'[INFO] {len(self.tokens)} tokens created:')
            for i in range(0, len(self.tokens)):
                print(f'{i}. {self.tokens[i]}')
        return self.tokens

#-------------------------------------------------------------------------------
# II. Parser (Syntaxic analysis) [PARSER]
#-------------------------------------------------------------------------------

# Model

class AST:

    def __init__(self):
        self.root = None

    def __str__(self):
        return self.root.to_s()

    def to_s(self, level=1):
        return self.root.to_s()

    def to_html_list(self, s, level, n):
        s += '  ' * level + '<li>' + n.get_name() + '\n'
        level += 1
        if hasattr(n, 'get_children'):
            lst = 'ol' if type(n) == Block else 'ul'
            s += '  ' * level + f'<{lst}>\n'
            inner = ''
            for c in n.get_children():
                inner = self.to_html_list(inner, level + 1, c)
            s += inner
            s += '  ' * level + f'</{lst}>\n'
        level -= 1
        s += '  ' * level + '</li>\n'
        return s
    
    def to_html(self):
        s = '    <ul>\n'
        s = self.to_html_list(s, 3, self.root)
        s += '    </ul>\n'
        return s


class Node:

    Terminal = "Terminal" # content is Token, right and left None
    Operation = "Operation" # content is Token.Operator, right and left are operands
    
    def __init__(self, content : Token, typ=None, right=None, left=None):
        if typ is None:
            if right is None and left is None:
                self.typ = Node.Terminal
            else:
                raise Exception("[ERROR] Cannot guess Node type")
        self.typ = typ
        self.content = content
        self.right = right
        self.left = left
        self.lvl = content.lvl
    
    def to_s(self, level=1):
        s = "    " * level + "{Terminal}\n"
        s += self.content.to_s(level + 1)
        return s
    
    def __str__(self):
         return self.to_s()

    def is_terminal(self):
        return self.right is None and self.left is None

    def get_name(self):
        return '{' + self.typ + '}'

    def get_children(self):
        if self.left is not None:
            yield self.left
        if self.right is not None:
            yield self.right


class Terminal(Node):
    
    def __init__(self, content):
        Node.__init__(self, content, Node.Terminal)

    def to_s(self, level=1):
        s = "    " * level + self.get_name()
        return s

    def get_name(self):
        return "{Terminal} "+ f"{self.content.typ} {self.content.val} ({self.content.start} +{self.content.length})"


class Block(Node):

    def __init__(self):
        self.actions = []

    def add(self, action):
        self.actions.append(action)

    def to_s(self, level=1):
        output = "    " * level + "{Block}\n"
        for elem in self.actions:
            if elem is None:
                raise Exception('None element in Block detected')
            output += elem.to_s(level+1)
            if output[-1] != '\n':
                output += '\n'
        return output
    
    def is_terminal(self):
        return len(self.actions) == 0

    def get_name(self):
        return '{Block}'
    
    def get_children(self):
        for elem in self.actions:
            yield elem


class Operation(Node):

    def __init__(self, operator : Token, left=None, right=None):
        Node.__init__(self, operator, Node.Operation, right, left)
        self.operator = self.content
        assert self.operator.is_terminal() and self.operator.content.typ == Token.Operator, "Operator should be of type Token.Operator and is " + self.operator.content.typ
    
    def to_s(self, level=1):
        name = self.get_name()
        s = "    " * level + f"{name}\n" # {self.content.content.val}
        if self.right is not None:
            s += "    " * (level + 1) + "right =\n"
            s += self.right.to_s(level + 2) + "\n"
        if self.left is not None:
            s += "    " * (level + 1) + "left =\n"
            s += self.left.to_s(level + 2) + "\n"
        return s

    def get_name(self):
        n = "{Operation} Binary" if self.left is not None and self.right is not None else "Unary"
        n += ' ' + self.content.content.val
        return n


class FunCall(Node):

    def __init__(self, name, arg): # mono arg
        assert type(name) == Terminal and name.content.typ == Token.Identifier, "Name of a function should be an identifier"
        self.name = name
        self.arg = arg

    def to_s(self, level=1):
        typ = "{Function Call}"
        return "    " * level + f"{typ} {self.name} {self.arg.to_s()} \n"
    
    def is_terminal(self):
        return True


class Statement(Node):

    def __init__(self, cond, action, alter=None, loop=False, on_false=False):
        self.cond = cond
        self.action = action
        self.alter = alter
        self.loop = loop
        self.on_false = on_false

    def get_name(self):
        if not self.on_false and not self.loop:
            return '{Statement} if'
        elif not self.on_false and self.loop:
            return '{Statement} while'
        elif self.on_false and not self.loop:
            return '{Statement} unless'
        elif self.on_false and self.loop:
            return '{Statement} until'
        else:
            raise Exception('Statement is not in a valid state')
    
    def to_s(self, level=1):
        start = "    " * level
        block = "    " * (level + 1)
        s = start + self.get_name() + '\n' + block + 'Cond:\n' + self.cond.to_s(level + 2)
        s += block + 'Action:\n' + self.action.to_s(level + 2)
        if self.alter is not None:
            s += block + 'Else:\n' + self.alter.to_s(level + 2)
        s += start + 'end\n'
        return s

    def __str__(self):
        return self.get_name()

    def get_children(self):
        yield self.cond
        yield self.action
        if self.alter is not None:
            yield self.alter


class Parser:
    
    PRIORITIES = { 
        '=' : 1, '+=' : 1, '-=' : 1, '*=' : 1, '/=' : 1, '//=' : 1, '**=' : 1, '%=' : 1,
        ',' : 2,
        'and' : 5, 'or' : 5, 'xor' : 5, 
        '>' : 8, '<' : 8, '>=' : 8, '<=' : 8, '==' : 8, '!=' : 8, '<=>' : 8, 
        '<<': 9, '>>' : 9, '..' : 9, '..<' : 9,
        '+' : 10, '-' : 10,
        '*' : 20, '/' : 20, '//' : 20,
        '**' : 30, '%' : 30,
        'call' : 35,
        'call(' : 40,
        '.' : 50,
        'not' : 51,
        'unary-' : 52,
        'expr(' : 60,
    }
    
    def __init__(self, debug = False):
        self.level_of_ana = 0
        self.debug = debug
        self.debug_expression = False # expression are too verbose, we must try to segregate
    
    def set_debug(self):
        self.debug = not self.debug

    def parse(self, tokens):
        if self.debug:
            print('[INFO] Start parsing')
        if tokens is None:
            raise Exception("tokens is None!")
        # clean tokens
        cleaned = [tok for tok in tokens if tok.typ not in [Token.Comment]] # Token.NewLine, 
        tokens = cleaned
        index = 0
        ast = AST()
        ast.root = self.read_block(tokens, 0)[1] # index is discared
        return ast
    
    def get_end(self, tokens, index):
        level = 0
        for t in range(index + 1, len(tokens)):
            tok = tokens[t]
            if tok.typ == Token.Keyword and tok.val in ['if', 'while', 'for']:
                level += 1
            elif tok.typ == Token.Keyword and tok.val == 'end' and level == 0:
                return t
            elif tok.typ == Token.Keyword and tok.val == 'end' and level > 0:
                level -= 1
        # should have an "end" keyword at the end
        raise Exception("[ERROR] Parser: malformed expression")

    def get_else(self, tokens, index, end):
        level = 0
        t = index + 1
        for t in range(index + 1, end):
            tok = tokens[t]
            if tok.typ == Token.Keyword and tok.val in ['if', 'while', 'for']:
                level += 1
            elif tok.typ == Token.Keyword and tok.val in ['else', 'elif'] and level == 0:
                return t
            elif tok.typ == Token.Keyword and tok.val == 'end' and level > 0:
                level -= 1
        return None
    
    def read_block(self, tokens, index, max_index=None):
        if max_index is None: max_index = len(tokens)
        #print('    ' * self.level_of_ana, 'read_block from', index, 'to', max_index)
        block = Block()
        while index < max_index:
            tok = tokens[index]
            if tok.typ == Token.Keyword and tok.val == 'if':
                end = self.get_end(tokens, index)
                els = self.get_else(tokens, index, end)
                index, node = self.read_if(tokens, index + 1, els, end)
                block.add(node)
            elif tok.typ == Token.Keyword and tok.val in ['while', 'for']:
                end = self.get_end(tokens, index)
                if tok.val == 'while':
                    index, node = self.read_while(tokens, index + 1, end)
                else:
                    index, node = self.read_for(tokens, index + 1, end)
                block.add(node)
            elif tok.typ == Token.NewLine: # discard not meaningfull newline
                index += 1
            else:
                end = self.get_keyword_or_nl(tokens, index, max_index, ['else', 'end'])
                index, node = self.read_expr(tokens, index, end)
                block.add(node)
        return index, block

    def get_keyword_or_nl(self, tokens, index, max_index, keywords):
        if type(keywords) == str:
            keywords = [keywords]
        for t in range(index, max_index):
            if tokens[t].typ == Token.NewLine or (tokens[t].typ == Token.Keyword and tokens[t].val in keywords):
                return t
    
    def read_if(self, tokens, index, else_index, end_index):
        self.level_of_ana += 1
        #print('    ' * self.level_of_ana, 'read_if from', index, tokens[index], 'to', end_index)
        #for t in range(index, end_index):
        #    print('    ' * self.level_of_ana, ' -', tokens[t])
        # read condition
        cond = None
        t = self.get_keyword_or_nl(tokens, index, end_index, 'then')
        index, cond = self.read_expr(tokens, index, t)
        # read action
        action = None
        end = else_index if else_index is not None else end_index
        _, action = self.read_block(tokens, index, end)
        # read else action
        else_action = None
        if else_index is not None:
            if tokens[else_index].val == 'else':
                _, else_action = self.read_block(tokens, else_index + 1, end_index)
            else: # elif
                elif_else = self.get_else(tokens, else_index + 1, end_index)
                _, else_action = self.read_if(tokens, else_index + 1, elif_else, end_index)
        node = Statement(cond, action, else_action)
        self.level_of_ana -= 1
        return end_index + 1, node
    
    def read_while(self, tokens, index, end_index):
        # read condition
        cond = None
        t = self.get_keyword_or_nl(tokens, index, end_index, 'do')
        index, cond = self.read_expr(tokens, index, t)        
        # read action
        action = None
        _, action = self.read_block(tokens, index, end_index)
        node = Statement(cond, action, loop=True)
        return end_index + 1, node
    
    def read_for(self, tokens, index, end_index):
        return 99
    
    def read_expr(self, tokens, index, end_index):
        #self.debug_expression = True
        if end_index is None: end_index = len(tokens)
        self.level_of_ana += 1
        # Sorting operators
        working_list = copy.deepcopy(tokens[index:end_index + 1])
        sorted_operators = []
        prio_values = []
        lvl = 1
        index = 0
        after_aug = False
        if self.debug_expression:
            print('================================')
            print('Building initial list')
            print('================================')
        while index < len(working_list):
            if after_aug:
                after_aug = False
                lvl *= 100
            token = working_list[index]
            token.lvl = lvl
            if self.debug_expression:
                print(f"    working_list {str(index)}. {token} lvl={token.lvl}")
            if token.typ in [Token.Operator, Token.Separator]:
                # Handling of ( )
                if token.val == '(':
                    if index >= 1 and working_list[index - 1].typ != Token.Operator: # not the first and not after an Operator
                        token.val = 'call('
                        token.typ = Token.Operator
                        after_aug = True
                    else:
                        lvl *= 100
                        del working_list[index]
                        continue
                elif token.val == ')':
                    lvl /= 100
                    del working_list[index]
                    continue
                # Handling of Operators
                if token.typ == Token.Operator:
                    if len(sorted_operators) == 0:
                        if self.debug_expression:
                            print('        => adding the first operator')
                        sorted_operators.append(index)
                        prio_values.append(Parser.PRIORITIES[token.val] * lvl)
                    else:
                        if self.debug_expression:
                            print('        => adding another operator')
                        computed_prio = Parser.PRIORITIES[token.val] * lvl
                        ok = False
                        for i in range(0, len(sorted_operators)):
                            if prio_values[i] < computed_prio:
                                sorted_operators.insert(i, index)
                                prio_values.insert(i, computed_prio)
                                ok = True
                                break
                        if not ok:
                            sorted_operators.append(index)
                            prio_values.append(computed_prio)
            index += 1
        # remove ending newline(s)
        while working_list[-1].typ == Token.NewLine:
            working_list.pop()
        if len(sorted_operators) == 0 and len(working_list) > 1:
            raise Exception("[ERROR] Incorrect expression len(sorted_operators) == 0")
        # Resolving operators
        length = len(working_list)
        if length <= 0:
            raise Exception("[ERROR] Parser: Empty expression of length = " + str(length))
        elif length == 1:
            if working_list[0].typ in [Token.Boolean, Token.Float, Token.Integer, Token.Identifier, Token.String]:
                node = Terminal(working_list[0])
                results = end_index + 1, node
            else:
                #for t in range(index, end_index):
                #    print(t, tokens[t])
                raise Exception("[ERROR] Parser: Expression of length 1 is not valid we have: " + str(working_list[0]))
        else:
            modifier = 0
            counter = 0 # only for debug
            length_at_start = len(sorted_operators) # only for debug
            while len(sorted_operators) > 0:
                # Debug Display
                counter += 1
                if self.debug_expression:
                    print('================================')
                    print('=', counter, '/', length_at_start)
                    print('================================')
                    print('--------------------')
                    print('Initial working list')
                    print('--------------------')
                    for index, token in enumerate(working_list):
                        print(f"    working_list {index}. {token.__class__.__name__} {token} lvl={token.lvl}")
                    print('----------------')
                    print('Sorted Operators')
                    print('----------------')
                    for so in range(0, len(sorted_operators)):
                        idx = sorted_operators[so]
                        obj = working_list[sorted_operators[so] + modifier]
                        print(f'    {so}. index={idx} type={obj.__class__.__name__} str={obj} modifier={modifier}')
                    print('-------------------')
                    print('Starting to resolve')
                    print('-------------------')
                # End of Debug Display
                operator_index = sorted_operators[0] + modifier
                if self.debug_expression:
                    print('    Resolving 0. in sorted_operators: ' + str(working_list[operator_index]))
                # Left parameter, None for Unary Operator
                op = working_list[operator_index]
                if (type(op) == Token and op.val == 'not') or (type(op) == Operation and op.operator.content.val == 'not'):
                    left = None
                elif ((type(op) == Token and op.val == '-') or (type(op) == Operation and op.operator.content.val == '-')) and operator_index - 1 < 0:
                    left = None
                else:
                    left = working_list[operator_index - 1]
                    if not isinstance(left, Node):
                        left = Terminal(left)
                # Right parameter
                right = None
                # We must have a parameter and its priority/lvl must be superior : ( "abc" ) abc is lvl = 100 vs () "abc" abc is lvl = 1
                if (type(op) == Token and op.val == 'call(') or (type(op) == Operation and op.operator.content.val == 'call('):
                    if len(working_list) > operator_index + 1 and working_list[operator_index + 1].lvl > working_list[operator_index].lvl:
                        right = working_list[operator_index + 1]
                # We must have always a right parameter (there is no unary op with left operand)
                else:
                    if len(working_list) > operator_index + 1:
                        right = working_list[operator_index + 1]
                if right is not None and not isinstance(right, Node):
                    right = Terminal(right)
                op = Terminal(working_list[operator_index])
                node = Operation(
                    op,
                    left,
                    right
                )
                # update working list
                if left is not None and right is not None:
                    del working_list[operator_index + 1] # right
                    del working_list[operator_index] # op
                    del working_list[operator_index - 1] # left
                    working_list.insert(operator_index - 1, node)
                elif left is None and right is not None:
                    del working_list[operator_index + 1] # right
                    del working_list[operator_index] # op
                    working_list.insert(operator_index, node)
                elif left is not None and right is None: # call( without arg
                    del working_list[operator_index] # op
                    del working_list[operator_index - 1] # left
                    working_list.insert(operator_index - 1, node)
                else: # left is None and right is None
                    del working_list[operator_index]
                    working_list.insert(operator_index, node)
                # update sorted operators
                if self.debug_expression:
                    print(f'    Updating working list, operator_index={operator_index}, left={left}, right={right}')
                    print('---------------------')
                    print('Modified working list')
                    print('---------------------')
                    for index, token in enumerate(working_list):
                        print(f"    working_list {index}. {token.__class__.__name__} {token} lvl={token.lvl}")
                    print('    Updating sorted operators')
                    print('    < Before')
                del sorted_operators[0]
                for so in range(0, len(sorted_operators)):
                    if sorted_operators[so] > operator_index:
                        if right is not None: # f()
                            sorted_operators[so] -= 2
                        else:
                            sorted_operators[so] -= 1
                if self.debug_expression:
                    print('    > After')
                    print('       ', sorted_operators)
            results = end_index + 1, node
        self.level_of_ana -= 1
        return results

#-------------------------------------------------------------------------------
# III. Interpreter [EXEC]
#-------------------------------------------------------------------------------

# III.A Basic Library

GLOBAL_DEBUG = False

def writeln(arg):
    if isinstance(arg, list):
        res = 0
        for i, a in enumerate(arg):
            res += write(a, i == 0)
        print()
        return res + 1 # for the newline
    else:
        msg = str(arg)
        prompt = '          ' if GLOBAL_DEBUG else ''
        console.puts(prompt + msg)
        return len(msg) + 1 # for the newline

def write(arg, first=True):
    if isinstance(arg, list):
        res = 0
        for i, a in enumerate(arg):
            res += write(a, i == 0)
        return res
    else:
        msg = str(arg)
        prompt = '          ' if first and GLOBAL_DEBUG else ''
        console.put(prompt + msg)
        return len(msg)

def readint(arg=None):
    if isinstance(arg, str) or arg is None:
        if arg is not None:
            res = input(arg)
        else:
            res = input()
        i = int(res)
        return i
    else:
        raise Exception('readint arg should be a string or None and is ' + str(type(arg)))

def readstr(arg=None):
    if isinstance(arg, str) or arg is None:
        if arg is not None:
            res = input(arg)
        else:
            res = input()
        return res
    else:
        raise Exception('readstr arg should be a string or None' + str(type(arg)))
    
# III.B Engine

class AshObject:

    def __init__(self, cls=None, val=None):
        self.val = val
        self.cls = cls
        self.attributes = {}
        if self.cls is not None and hasattr(self.cls, 'instance_methods'):
            self.methods = self.cls.instance_methods

    def send(self, msg, *params):
        res = self.methods[msg](self, *params)
        return res

    def get_method(self, name):
        return self.methods[name]
    
    def __gt__(self, o):
        if self.val is not None and type(o) == AshObject and o.val is not None:
            return self.val > o.val
        else:
            raise Exception("Unable to compare to: " + str(o))
    
    def __repr__(self):
        if self.val is not None:
            return f'{self.val} : {self.cls.name}'
        else:
            return '{AshObject}'


class AshClass(AshObject):

    def __init__(self, name):
        super().__init__(cls=self)
        self.name = name
        self.instance_attributes = {}
        self.instance_methods = {}

def int_flt(op, res, v1, v2):
    if v1.cls not in [AshInteger, AshFloat] or v2.cls not in [AshInteger, AshFloat]:
        raise Exception(f'[ERROR] Interpreter: v1 and v2 must be Integer or Float, not {v1.cls} and {v2.cls}')
    if op not in ['/', '//']:
        if v1.cls == v2.cls:
            return v1.cls
        else:
            return AshFloat
    elif op == '/':
        return AshFloat
    elif op == '//':
        return AshInteger
    else:
        raise Exception(f'[ERROR] Interpreter: Operator {op} not known')
    
AshInteger = AshClass('Integer')

def ari_add(a1, a2):
    val = a1.val + a2.val
    return AshObject(int_flt('+', val, a1, a2), val=val)
def ari_sub(a1, a2):
    val=a1.val - a2.val
    return AshObject(int_flt('-', val, a1, a2), val=val)
def ari_mul(a1, a2):
    val=a1.val * a2.val
    return AshObject(int_flt('*', val, a1, a2), val=val)
def ari_div(a1, a2):
    val=a1.val / a2.val
    return AshObject(int_flt('/', val, a1, a2), val=val)
def ari_divint(a1, a2):
    val=a1.val // a2.val
    return AshObject(int_flt('//', val, a1, a2), val=val)
def ari_mod(a1, a2):
    val=a1.val % a2.val
    return AshObject(int_flt('%', val, a1, a2), val=val)
def ari_pow(a1, a2):
    val=a1.val ** a2.val
    return AshObject(int_flt('**', val, a1, a2), val=val)
def ari_lshift(a1, a2):
    val=a1.val << a2.val
    return AshObject(int_flt('<<', val, a1, a2), val=val)
def ari_rshift(a1, a2):
    val=a1.val >> a2.val
    return AshObject(int_flt('>>', val, a1, a2), val=val)
def ari_unary_minus(a1):
    return AshObject(a1.cls, val=-a1.val)

def ari_cmp_eq(a1, a2):
    return AshObject(AshBoolean, val=a1.val == a2.val)
def ari_cmp_le(a1, a2):
    return AshObject(AshBoolean, val=a1.val <= a2.val)
def ari_cmp_lt(a1, a2):
    return AshObject(AshBoolean, val=a1.val < a2.val)
def ari_cmp_ge(a1, a2):
    return AshObject(AshBoolean, val=a1.val >= a2.val)
def ari_cmp_gt(a1, a2):
    return AshObject(AshBoolean, val=a1.val > a2.val)
def ari_cmp_dif(a1, a2):
    return AshObject(AshBoolean, val=a1.val != a2.val)

AshInteger.instance_methods['+'] = ari_add
AshInteger.instance_methods['-'] = ari_sub
AshInteger.instance_methods['*'] = ari_mul
AshInteger.instance_methods['/'] = ari_div
AshInteger.instance_methods['//'] = ari_divint
AshInteger.instance_methods['%'] = ari_mod
AshInteger.instance_methods['**'] = ari_pow
AshInteger.instance_methods['<<'] = ari_lshift
AshInteger.instance_methods['>>'] = ari_rshift
AshInteger.instance_methods['=='] = ari_cmp_eq
AshInteger.instance_methods['<'] = ari_cmp_lt
AshInteger.instance_methods['<='] = ari_cmp_le
AshInteger.instance_methods['>='] = ari_cmp_ge
AshInteger.instance_methods['>'] = ari_cmp_gt
AshInteger.instance_methods['!='] = ari_cmp_dif
AshInteger.instance_methods['unary-'] = ari_unary_minus

def boo_and(b1, b2):
    return AshObject(AshBoolean, val=b1.val and b2.val)
def boo_or(b1, b2):
    return AshObject(AshBoolean, val=b1.val or b2.val)
def boo_not(b):
    return AshObject(AshBoolean, val=not b.val)

AshBoolean = AshClass('Boolean')

AshBoolean.instance_methods['and'] = boo_and
AshBoolean.instance_methods['or'] = boo_or
AshBoolean.instance_methods['not'] = boo_not

AshFloat = AshClass('Float')

AshFloat.instance_methods['+'] = ari_add
AshFloat.instance_methods['-'] = ari_sub
AshFloat.instance_methods['*'] = ari_mul
AshFloat.instance_methods['/'] = ari_div
AshFloat.instance_methods['//'] = ari_divint
AshFloat.instance_methods['%'] = ari_mod
AshFloat.instance_methods['**'] = ari_pow
AshFloat.instance_methods['<<'] = ari_lshift
AshFloat.instance_methods['>>'] = ari_rshift
AshFloat.instance_methods['=='] = ari_cmp_eq
AshFloat.instance_methods['<'] = ari_cmp_lt
AshFloat.instance_methods['<='] = ari_cmp_le
AshFloat.instance_methods['>='] = ari_cmp_ge
AshFloat.instance_methods['>'] = ari_cmp_gt
AshFloat.instance_methods['!='] = ari_cmp_dif

AshString = AshClass('String')

AshModule = AshClass('Module')

AshModuleSDL = AshObject(cls=AshModule)

global tk_root
global tk_screen

def SDL_init(self):
    from tkinter import Tk, Label, Canvas
    global tk_root, tk_screen
    tk_root = Tk()
    tk_root.title('Init')
    tk_root.geometry("645x485")
    #w = Label(root, text="Hello")
    tk_screen = Canvas(tk_root, width=640, height=480, background='#000000')
    tk_screen.create_text(30, 30, text="Hello", fill='#FF0000')
    tk_screen.pack()
    tk_root.wm_attributes("-topmost", 1)
    #root.focus_force()

def SDL_run(self):
    global tk_root
    tk_root.mainloop()

def SDL_text(self, args):
    global tk_screen
    x = args[0]
    y = args[1]
    t = args[2]
    tk_screen.create_text(x, y, text=t, fill='#FF0000')

AshModuleSDL.methods['init'] = SDL_init
AshModuleSDL.methods['run'] = SDL_run
AshModuleSDL.methods['text'] = SDL_text

class Interpreter:
    
    def __init__(self, debug=False):
        self.vars = {}
        self.vars['writeln'] = writeln
        self.vars['write'] = write
        self.vars['readint'] = readint
        self.vars['readstr'] = readstr
        self.vars['sdl'] = AshModuleSDL
        self.debug = debug

    #def set_debug(self):
    #    self.debug = not self.debug
    
    def do_elem(self, elem, affectation=False, Scope=None):
        if self.debug:
            if type(elem) == Terminal:
                print(type(elem), '::', elem)
            else:
                print(type(elem), '::\n', elem)
        if type(elem) == Operation:
            op = elem.operator.content.val
            # Arithmetic
            if op in ['+', '-', '*', '/', '//', '%', '**', '<<', '>>']:
                if elem.left is None:
                    return self.do_elem(elem.right).send('unary-')
                else:
                    return self.do_elem(elem.left).send(op, self.do_elem(elem.right))
            # Comparison
            elif op in ['==', '<=', '<', '>=', '>', '!=']:
                return self.do_elem(elem.left).send(op, self.do_elem(elem.right))
            elif op in ['+=', '-=', '*=', '/=', '//=', '%=', '**=']:
                ids = self.do_elem(elem.left, affectation=True)
                val = self.do_elem(elem.right)
                true_op = op[:-1]
                self.vars[ids] = self.vars[ids].send(true_op, val)
                return self.vars[ids]
            # Affectation
            elif elem.operator.content.val == '=':
                val = self.do_elem(elem.right)
                ids = self.do_elem(elem.left, affectation=True)
                self.vars[ids] = val
                if self.debug: print('[EXEC] =', val, 'to', ids)
                return self.vars[ids]
            # Boolean
            elif op in ['and', 'or']:
                return self.do_elem(elem.left).send(op, self.do_elem(elem.right))
            # Not
            elif op == 'not':
                return self.do_elem(elem.right).send(op)
            # Function Call
            elif elem.operator.content.val == 'call(':
                a = self.do_elem(elem.left)
                return self.do_elem(elem.left).__call__(self.do_elem(elem.right))
            # Range create
            elif elem.operator.content.val == '..':
                a = self.do_elem(elem.left)
                b = self.do_elem(elem.right)
                return range(a, b)
            # Call
            elif elem.operator.content.val == '.':
                obj = self.do_elem(elem.left)
                msg = elem.right.content.val
                return obj.get_method(msg)
                # NOT USED BELOW
                #if isinstance(elem.right, Operation) and elem.right.operator.content.val == 'call(':
                #    # TODO: PARAMETERS ARE NOT HANDLED
                #    msg = elem.right.left.content.val
                #else:
                #    raise Exception("don't known what to do with <" + type(elem.right).__name__ + '>' + str(elem.right))
                ##b = self.do_elem(elem.right, scope={random})
                #if hasattr(obj, msg):
                #    fun = getattr(obj, msg)
                #    if callable(fun):
                #        return fun()
                #    else:
                #        raise Exception("not callable :" + msg)
                #elif b == 'random' and type(a) == range: # TODO: do not work
                #    # TODO: HERE SHOULD BE THE BASE LIBRARY
                #    import random
                #    return random.sample(a, 1)[0]
                #else:
                #    raise Exception("not implemented yet")
            # Concat expression
            elif elem.operator.content.val == ',':
                args = []
                args.append(self.do_elem(elem.left))
                right = self.do_elem(elem.right)
                if isinstance(right, list):
                    args.extend(right)
                else:
                    args.extend([right])
                return args
            else:
                raise Exception("Operator not known: " + elem.operator.content.val)
        elif type(elem) == Statement:
            cond = self.do_elem(elem.cond)
            executed = 0
            result = False
            if self.debug: print('[EXEC] Statement cond=', cond, 'executed=', executed)
            while cond.val and (executed == 0 or elem.loop):
                result = self.do_elem(elem.action)
                executed += 1
                if elem.loop:
                    cond = self.do_elem(elem.cond)
                if self.debug: print('[EXEC] Looping cond=', cond, 'executed=', executed, 'loop=', elem.loop)
            if executed == 0 and elem.alter is not None:
                return self.do_elem(elem.alter)
            else:
                return result
        elif type(elem) == Terminal:
            if elem.content.typ == Token.Integer:
                return AshObject(AshInteger, val=int(elem.content.val))
            elif elem.content.typ == Token.Float:
                return AshObject(AshFloat, val=float(elem.content.val))
            elif elem.content.typ == Token.Boolean:
                return AshObject(AshBoolean, val=elem.content.val == "true")
            elif elem.content.typ == Token.String:
                return elem.content.val
            elif elem.content.typ == Token.Identifier:
                if affectation == True:
                    return elem.content.val
                else:
                    if elem.content.val not in self.vars:
                        raise Exception(f"[ERROR] Interpreter: Identifier not know: {elem.content.val}")
                    return self.vars[elem.content.val]
            else:
                raise Exception(f"Terminal not known:\nelem.content.typ = {elem.content.typ} and type(elem) = {type(elem)}")
        #elif type(elem) == FunCall:
        #    if elem.name.content.val == 'writeln':
        #        arg = self.do_elem(elem.arg)
        #        print(arg)
        #        return len(str(arg))
        #    else:
        #        raise Exception("Function not known: " + str(elem.name))
        elif elem is None:
            return None
        elif type(elem) == Block:
            res = None
            for el in elem.actions:
                res = self.do_elem(el)
            return res
        else:
            raise Exception(f"Elem not known {elem}")

    def do(self, data):
        parser = Parser()
        res = Tokenizer().tokenize(data)
        ast = parser.parse(res)
        res = self.do_ast(ast)
    
    def do_ast(self, ast):
        last = None
        for elem in ast.root.actions:
            last = self.do_elem(elem)
        return last #18h59 8/9

#-------------------------------------------------------------------------------
# IV. Transpiler [TRANS]
#-------------------------------------------------------------------------------

class TranspilerPython:
    
    def __init__(self):
        pass
    
    def transpile(self, ast, filename):
        s = self.do_elem(ast)
        print(s)
        f = open(filename, mode='w', encoding='utf8')
        f.write(s)
        f.close()

    def do_elem(self, elem, affectation=False, Scope=None):
        if type(elem) == Operation:
            op = elem.operator.content.val
            # Arithmetic
            if op in ['+', '-', '*', '/', '//', '%', '**', '<<', '>>']:
                if elem.left is None:
                    return self.do_elem(elem.right).send('unary-')
                else:
                    return self.do_elem(elem.left).send(op, self.do_elem(elem.right))
            # Comparison
            elif op in ['==', '<=', '<', '>=', '>', '!=']:
                return self.do_elem(elem.left).send(op, self.do_elem(elem.right))
            elif op in ['+=', '-=', '*=', '/=', '//=', '%=', '**=']:
                ids = self.do_elem(elem.left, affectation=True)
                val = self.do_elem(elem.right)
                true_op = op[:-1]
                self.vars[ids] = self.vars[ids].send(true_op, val)
                return self.vars[ids]
            # Affectation
            elif elem.operator.content.val == '=':
                val = self.do_elem(elem.right)
                ids = self.do_elem(elem.left, affectation=True)
                self.vars[ids] = val
                if self.debug: print('[EXEC] =', val, 'to', ids)
                return self.vars[ids]
            # Boolean
            elif op in ['and', 'or']:
                return self.do_elem(elem.left).send(op, self.do_elem(elem.right))
            # Not
            elif op == 'not':
                return self.do_elem(elem.right).send(op)
            # Function Call
            elif elem.operator.content.val == 'call(':
                a = self.do_elem(elem.left)
                return self.do_elem(elem.left).__call__(self.do_elem(elem.right))
            # Range create
            elif elem.operator.content.val == '..':
                a = self.do_elem(elem.left)
                b = self.do_elem(elem.right)
                return range(a, b)
            # Call
            elif elem.operator.content.val == '.':
                #if self.debug:
                #    print(elem)
                obj = self.do_elem(elem.left)
                if isinstance(elem.right, Operation) and elem.right.operator.content.val == 'call(':
                    # TODO: PARAMETERS ARE NOT HANDLED
                    msg = elem.right.left.content.val
                else:
                    raise Exception("don't known what to do with" + str(type(elem.right)))
                #b = self.do_elem(elem.right, scope={random})
                if hasattr(obj, msg):
                    fun = getattr(obj, msg)
                    if callable(fun):
                        return fun()
                    else:
                        raise Exception("not callable :" + msg)
                elif b == 'random' and type(a) == range:
                    # TODO: HERE SHOULD BE THE BASE LIBRARY
                    import random
                    return random.sample(a, 1)[0]
                else:
                    raise Exception("not implemented yet")
            # Concat expression
            elif elem.operator.content.val == ',':
                args = []
                args.append(self.do_elem(elem.left))
                right = self.do_elem(elem.right)
                if isinstance(right, list):
                    args.extend(right)
                else:
                    args.extend([right])
                return args
            else:
                raise Exception("Operator not known: " + elem.operator.content.val)
        elif type(elem) == Statement:
            cond = self.do_elem(elem.cond)
            executed = 0
            result = False
            if self.debug: print('[EXEC] Statement cond=', cond, 'executed=', executed)
            while cond.val and (executed == 0 or elem.loop):
                result = self.do_elem(elem.action)
                executed += 1
                if elem.loop:
                    cond = self.do_elem(elem.cond)
                if self.debug: print('[EXEC] Looping cond=', cond, 'executed=', executed, 'loop=', elem.loop)
            if executed == 0 and elem.alter is not None:
                return self.do_elem(elem.alter)
            else:
                return result
        elif type(elem) == Terminal:
            if elem.content.typ == Token.Integer:
                return f'AshObject(AshInteger, val={elem.content.val})'
            elif elem.content.typ == Token.Float:
                return f'AshObject(AshFloat, val={elem.content.val})'
            elif elem.content.typ == Token.Boolean:
                return f'AshObject(AshBoolean, val={elem.content.val == "true"})'
            elif elem.content.typ == Token.String:
                return elem.content.val
            elif elem.content.typ == Token.Identifier:
                if affectation == True:
                    return elem.content.val
                else:
                    if elem.content.val not in self.vars:
                        raise Exception(f"[ERROR] Interpreter: Identifier not know: {elem.content.val}")
                    return self.vars[elem.content.val]
            else:
                raise Exception(f"Terminal not known:\nelem.content.typ = {elem.content.typ} and type(elem) = {type(elem)}")
        #elif type(elem) == FunCall:
        #    if elem.name.content.val == 'writeln':
        #        arg = self.do_elem(elem.arg)
        #        print(arg)
        #        return len(str(arg))
        #    else:
        #        raise Exception("Function not known: " + str(elem.name))
        elif elem is None:
            return None
        elif type(elem) == Block:
            res = ''
            for el in elem.actions:
                res += self.do_elem(el) + '\n'
                print(res)
            return res
        else:
            raise Exception(f"Elem not known {type(elem).__name__}")

#-------------------------------------------------------------------------------
# V. Test framework [TESTS]
#-------------------------------------------------------------------------------

#class Assertion:
#    def __init__(self, nb, typ, val):
#        self.nb = nb
#        self.typ = typ
#        self.val = val

#class Test:
#
#    def __init__(self, title, command, expected, length=None, assertions=None, no_exec=False):
#        self.title = title
#        self.command = command
#        self.expected = expected
#        self.length = length
#        self.assertions = assertions
#        self.no_exec = no_exec
#    
#    def execute(self):
#        print(f'--- {self.title} ---')
#        res = Tokenizer().tokenize(self.command)
#        for itoken in range(0, len(res)):
#            print(itoken, '. ', res[itoken], sep='')
#        if self.length is not None:
#            assert len(res) == self.length, f"[ERROR] {self.length} tokens should have been producted! Instead: {str(len(res))}"
#        if self.assertions is not None and type(self.assertions) == dict:
#            for val in self.assertions:
#                if type(val) != Assertion:
#                    raise Exception("Only Assertion instance can be handled here.")
#                assert type(res[val.nb]) == Token and res[val.nb].val == val.val and res[val.nb].typ == val.typ, f"[ERROR] Token {val.nb} should be {val.typ} with the falue of '{val.val}'. Instead: {res[val.nb]}"
#        ast = Parser().parse(res)
#        print('AST:\n', ast.to_s(), sep='', end='')
#       if not self.no_exec:
#            print('#======== Console ========#')
#            print('#-------------------------#')
#            res = Interpreter().do(ast)
#            print('#-------------------------#')
#            print('RES:\n    ', res, sep='')
#            if self.expected != 'JUST_DISPLAY':
#                assert res == self.expected, "[ERROR] Result is not equal to " + str(self.expected) + " instead: " + str(res)
#        else:
#            print('Execution skipped')
#        print("== OK ==")
#        print()
#        return 'OK'

def read_tests(filepath):
    global GLOBAL_DEBUG
    GLOBAL_DEBUG = True
    print('-------------------------------')
    type2python = {
        'Boolean' : bool,
        'Integer' : int,
        'String' : str
    }
    res2python = {
        'false' : False,
        'true' : True
    }
    f = open(filepath, mode='r')
    lines = f.readlines()
    f.close()
    nb_tests = {
        'skipped' : 0,
        'success' : 0,
        'failed'  : 0,
        'total'   : 0,
    }
    for i, line in enumerate(lines, start=1):
        if i < 3: continue # headers
        try:
            data    = line.split('\t')
            idt     = data[0]
            status  = data[1]
            py      = data[2]
            lua     = data[3]
            title   = data[4]
            content = data[5]
            content_exec = content.replace('\\n', '\n')
            resval  = data[6]
            restyp  = data[7]
            try:
                numtok  = int(data[8].rstrip())
            except ValueError:
                numtok = None
            asserts  = data[9:]
            if len(asserts) > 0:
                asserts[-1] = asserts[-1].rstrip()
        except (ValueError, IndexError) as e:
            print(f'[TEST]    {nb_tests["total"]+1:03} Skipping line {i:05d} {e}')
            nb_tests['skipped'] += 1
            nb_tests['total']   += 1
            continue
        if status == 'Do':
            print(f'[TEST]    {nb_tests["total"]+1:03} {title} : {content}')
            try:
                # Tokenizing
                res = Tokenizer(False).tokenize(content_exec)
                if numtok is not None and len(res) != numtok:
                    shell.write(f'[FAILED]  Wrong number of tokens, expecting {numtok} got {len(res)}\n', 'COMMENT')
                    nb_tests['failed'] += 1
                    nb_tests['total']  += 1
                    continue
                for assertcheck in asserts:
                    data = assertcheck.split('::')
                    if len(data) == 4:
                        what = data[0]
                        where = data[1]
                        typ = data[2]
                        val = data[3]
                        if what == 'Tokens':
                            where = int(where)
                            if res[where].typ.name != typ:
                                shell.write(f'[FAILED]  Wrong type of token, expecting {typ} got {res[where].typ}\n', 'COMMENT')
                                nb_tests['failed'] += 1
                                nb_tests['total']  += 1
                                continue
                            else:
                                if res[where].val != val: # all value are strings
                                    shell.write(f'[FAILED]  Wrong value of token, expecting {val} got {res[where].val}\n', 'COMMENT')
                                    nb_tests['failed'] += 1
                                    nb_tests['total']  += 1
                                    continue
                                else:
                                    shell.write(f'[ASSERT]  Assert ok for token {where} of type {typ} of val {val}\n', 'STRING')
                # Parsing & Interpreting
                ast = parser.parse(res)
                res = interpreter.do_ast(ast)
                ok = False
                if restyp in type2python:
                    if type(res) == type2python[restyp]:
                        if restyp == 'Boolean':
                            if res == res2python[resval]:
                                ok = True
                        elif restyp == 'Integer':
                            if res == int(resval):
                                ok = True
                        elif restyp == 'String':
                            if "'" + res + "'" == resval:
                                ok = True
                if ok:
                     shell.write(f'[SUCCESS] Expected {resval} of type {restyp} and got: {res} of type {type(res)}\n', 'STRING')
                     nb_tests['success'] += 1
                     nb_tests['total']   += 1
                else:
                    shell.write(f'[FAILED]  Expected {resval} of type {restyp} and got: {res} of type {type(res)}\n', 'COMMENT')
                    nb_tests['failed'] += 1
                    nb_tests['total']  += 1
            except Exception as e:
                shell.write(f'[FAILED]  Exception: {e}\n', 'COMMENT')
                traceback.print_exception(*sys.exc_info())
                nb_tests['failed'] += 1
                nb_tests['total']  += 1
    print('-------------------------------')
    if nb_tests["success"] + nb_tests["failed"] + nb_tests["skipped"] != nb_tests['total']:
        raise Exception("[ERROR] Total of tests not equal to total of tests failed/skipped/success")
    shell.write(f'Nb test success:   {nb_tests["success"]:05d} ({round(nb_tests["success"]/nb_tests["total"]*100):3d}%)\n', 'STRING')
    if nb_tests["failed"] == 0:
        shell.write(f'Nb test failed:    {nb_tests["failed"]:05d} ({round(nb_tests["failed"]/nb_tests["total"]*100):3d}%)\n', 'STRING')
    else:
        shell.write(f'Nb test failed:    {nb_tests["failed"]:05d} ({round(nb_tests["failed"]/nb_tests["total"]*100):3d}%)\n', 'COMMENT')
    shell.write(f'Nb test skipped:   {nb_tests["skipped"]:05d} ({round(nb_tests["skipped"]/nb_tests["total"]*100):3d}%)\n', 'KEYWORD')
    print('-------------------------------')
    print(f'Total test passed: {nb_tests["total"]:05d}')
    print('-------------------------------')
    GLOBAL_DEBUG = False

#-------------------------------------------------------------------------------
# VI. Main [MAIN]
#-------------------------------------------------------------------------------

def read(filepath):
    f = open(filepath, mode='r', encoding='utf8')
    c = f.read()
    f.close()
    return c

def run(command, interpreter, output=None):
    global console
    tokenizer = Tokenizer()
    parser = Parser()
    console.outputs = []

    tokens = []
    ast = None
    res = None
    try:
        tokens = tokenizer.tokenize(command)
        ast = parser.parse(tokens)
        res = interpreter.do_ast(ast)
        console.puts('= ' + str(res))
    except Exception as e:
        console.error(e)
        traceback.print_exc(file=sys.stdout)
    
    if debug:
        filename = output if output is not None else 'last.html'
        f = open(filename, mode='w', encoding='utf8')
        f.write('<html>\n  <body>\n')
        f.write('    <h2>Command</h2>\n      <pre>\n')
        f.write(command)
        f.write('    </pre>\n')
        f.write('    <h2>Tokens</h2>\n      <table border="1">\n')
        for i, t in enumerate(tokens):
            f.write(f'      <tr><td>{i}</td><td>{t.typ.name}</td><td>{t.val}</td></tr>\n')
        f.write('    </table>\n')
        f.write('    <h2>Abstract syntax tree</h2>\n')
        if ast is not None:
            f.write(ast.to_html())
        else:
            f.write('    <p>No AST defined.</p>\n')
        f.write('    <h2>Outputs</h2>\n      <table border="1">\n')
        for t in console.outputs:
            f.write('      <tr><td>' + str(t) + '</td></tr>\n')
        f.write('    </table>\n')
        f.write('    <h2>Result</h2>\n')
        f.write('    <h1>' + str(res) + '</h1>\n')
        f.write('  </body>\n</html>')
        f.close()
                
if __name__ == '__main__':
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        f = open(filepath, mode='r')
        data = f.read()
        f.close()
        interpreter = Interpreter().do(data)
    else:
        debug = True
        interpreter = Interpreter()
        while True:
            command = input('ash> ')
            if command == 'exit':
                break
            elif command == 'help':
                print('Ash language v0.1 2017-2019')
                print('help      : this help')
                print('tests     : run multiple tests')
                print('reset     : reset interpreter')
                print('debug     : set/unset debug. You can specify true or false')
                print('locals    : get local variable')
                print('exec <f>  : execute a file')
                print('trans <f> : transpile a file')
                print('exit      : exit this shell')
            elif command.startswith('debug'):
                args = command.split(' ')
                if len(args) < 2:
                    debug = not debug
                    console.info('Debug set to ' + str(debug))
                else:
                    debug = True if args[1] == 'true' else False
            elif command == 'locals':
                for k in sorted(interpreter.vars):
                    print(f"{k:10}", interpreter.vars[k])
            elif command.startswith('trans'):
                args = command.split(' ')
                args = command.split(' ')
                if len(args) < 2:
                    console.error('You must indicate a file to process.')
                else:
                    arg = args[1]
                    if not arg.endswith('.ash'):
                            arg += '.ash'
                    if not os.path.isfile(arg):
                        console.error('File ' + arg + ' does not exist')
                    else:
                        c = read(arg)
                        tokenizer = Tokenizer()
                        parser = Parser()
                        console.outputs = []
                        tokens = tokenizer.tokenize(c)
                        ast = parser.parse(tokens)
                        TranspilerPython().transpile(ast.root, 'last.py') 
            elif command.startswith('exec') or command == 'tests':
                if command == 'tests': # hack
                    command = 'exec tests'
                args = command.split(' ')
                if len(args) < 2:
                    console.error('You must indicate a file to process.')
                else:
                    arg = args[1]
                    if os.path.isdir(arg):
                        files = os.listdir(arg)
                        cpt = 0
                        max_file = 0
                        for f in files:
                            if f.endswith('.ash'):
                                max_file += 1
                        for f in files:
                            if f.endswith('.ash'):
                                cpt += 1
                                console.info(f'Executing {f} ({cpt}/{max_file})')
                                filename = os.path.join(arg, f)
                                html_output = os.path.join(arg, 'html', f)
                                c = read(filename)
                                run(c, interpreter, html_output[:-4] + '.html')
                    else:
                        if not arg.endswith('.ash'):
                            arg += '.ash'
                        if not os.path.isfile(arg):
                            console.error('File ' + arg + ' does not exist')
                        else:
                            c = read(arg)
                            run(c, interpreter)
            elif command == 'reset':
                interpreter = Interpreter()
            elif command == 'tests':
                read_tests('./tests/tests.txt')      
            else:
                try:
                    run(command, interpreter)
                except Exception as e:
                    console.error(f'Exception: {e}')
                    traceback.print_exception(*sys.exc_info())
