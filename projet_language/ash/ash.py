import os.path
import copy # only once for read_expr
import sys # for writing debug info in red for the tests
import traceback

class FallBack:
    def write(self, msg, color):
        sys.stdout.write(msg)

try:
    shell = sys.stdout.shell
except AttributeError:
    shell = FallBack()
    #raise RuntimeError("Only works in IDLE")

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
    
    BLOCK_PLUS = [ 'if', 'for', 'while', 'fun', 'sub', 'get', 'set', 'class' ]
    BLOCK_LESS = [ 'end' ]
    LINE_LESS =  [ 'elif' ]
    
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
            t = Token(Token.NewLine, line[index], self.counter)
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


class Terminal(Node):
    
    def __init__(self, content):
        Node.__init__(self, content, Node.Terminal)

    def to_s(self, level=1):
        s = "    " * level + "{Terminal} "+ f"{self.content.typ} {self.content.val} ({self.content.start} +{self.content.length})"
        return s


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


class Operation(Node):

    def __init__(self, operator : Token, left=None, right=None):
        Node.__init__(self, operator, Node.Operation, right, left)
        self.operator = self.content
        assert self.operator.is_terminal() and self.operator.content.typ == Token.Operator, "Operator should be of type Token.Operator"
    
    def to_s(self, level=1):
        name = "{Operation} Binary" if self.left is not None and self.right is not None else "Unary"
        s = "    " * level + f"{name} {self.content.content.val}\n"
        if self.right is not None:
            s += "    " * (level + 1) + "right =\n"
            s += self.right.to_s(level + 2) + "\n"
        if self.left is not None:
            s += "    " * (level + 1) + "left =\n"
            s += self.left.to_s(level + 2) + "\n"
        return s


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


class Parser:
    
    PRIORITIES = { 
        '=' : 1, '+=' : 1, '-=' : 1,
        ',' : 2,
        'and' : 5, 'or' : 5, 'xor' : 5, 
        '>' : 8, '<' : 8, '>=' : 8, '<=' : 8, '==' : 8, '!=' : 8, '<=>' : 8, 
        '<<': 9, '>>' : 9, '..' : 9, '..<' : 9,
        '+' : 10, '-' : 10,
        '*' : 20, '/' : 20, '//' : 20,
        '**' : 30, '%' : 30,
        'call' : 35,
        '.' : 40,
        'unary-' : 50,
        'call(' : 51,
        'expr(' : 60,
    }
    
    def __init__(self, debug = False):
        self.level_of_ana = 0
        self.debug = debug
        self.debug_expression = False # expression are too verbose, we must try to segregate
    
    def set_debug(self):
        self.debug = not self.debug
    
    def puts(self, s):
        if self.debug:
            print("    " * self.level_of_ana + s)
    
    def read_block(self, tokens, index, end_block=False, max_index=None):
        self.level_of_ana += 1
        self.puts('< Block >')
        block = Block()
        level = 0
        while (max_index is None or (max_index is not None and index < max_index)) and index < len(tokens):
            if index >= len(tokens):
                raise Exception("[ERROR] Parser: impossible to read a token at " + str(index))
            tok = tokens[index]
            #print('.', index, max_index)
            # Test to terminate
            if index >= len(tokens):
                self.puts('    Terminating stream of tokens')
                if end_block: # should have an "end" keyword at the end
                    raise Exception("[ERROR] Parser: malformed expression")
                break
            if tok.typ == Token.Keyword and tok.val == 'end' and level == 0:
                self.puts('||| Keyword End found')
                index += 1
                break
            if tok.typ == Token.Keyword and tok.val == 'else' and level == 0:
                self.puts('||| Keyword Else found')
                index += 1
                break
            # Parsing
            self.puts('    read_block decides on: ' + str(tok))
            if tok.typ == Token.Keyword and tok.val in ['if', 'unless']:
                level +=1
                #self.puts('||| :: If/unless')
                index, node = self.read_if(tokens, index + 1)
                block.add(node)
            elif tok.typ == Token.Keyword and tok.val in ['while', 'until']:
                level += 1
                #self.puts('||| :: While/until')
                index, node = self.read_while(tokens, index + 1)
                block.add(node)
            elif tok.typ == Token.Keyword and tok.val == 'end':
                level -= 1
                self.puts('||| :: End')
                index += 1
            elif tok.typ == Token.NewLine:
                self.puts('||| :: Newline (discarded)')
                index += 1
            else:
                #self.puts('||| :: Expression')
                end_index = index
                while end_index < len(tokens):
                    #print('pipo', end_index, '/', len(tokens), tokens[end_index])
                    if tokens[end_index].typ == Token.NewLine:
                        break
                    end_index += 1
                index, node = self.read_expr(tokens, index, end_index)
                if node is None:
                    raise Exception("[ERROR] read_expr has returned a None node")
                block.add(node)
        self.puts('< End Block @' + str(index) + ' >')
        self.level_of_ana -= 1
        return index, block
    
    def read_if(self, tokens, index):
        self.level_of_ana += 1
        self.puts('< If >')
        if len(tokens) <= index:
            raise Exception("Unfinished If")
        end_index = index
        # read condition
        while end_index < len(tokens):
            if tokens[end_index].typ == Token.NewLine or \
                tokens[end_index].typ == Token.Keyword and tokens[end_index].val == "then":
                break
            end_index += 1
        index, cond = self.read_expr(tokens, index, end_index)
        # read action
        while end_index < len(tokens):
            if tokens[end_index].typ == Token.Keyword and tokens[end_index].val in ["else", "elif", "end"]:
                break
            end_index += 1
        index, action = self.read_block(tokens, index, True, end_index) # end_index added for one line if
        # read else action
        else_action = None
        if index < len(tokens):
            if tokens[index].typ == Token.Keyword and tokens[index].val == 'else':
                index, else_action = self.read_block(tokens, index, True)
        node = Statement(cond, action, else_action)
        self.puts('< End If @' + str(index) + '>')
        self.level_of_ana -= 1
        return index, node
    
    def read_while(self, tokens, index):
        self.level_of_ana += 1
        self.puts('< While >')
        if len(tokens) <= index:
            raise Exception("Unfinished While")
        end_index = index
        while end_index < len(tokens):
            if tokens[end_index].typ == Token.NewLine or \
                tokens[end_index].typ == Token.Keyword and tokens[end_index].val == "do":
                break
            end_index += 1
        index, cond = self.read_expr(tokens, index, end_index)
        while end_index < len(tokens):
            if tokens[end_index].typ == Token.Keyword and tokens[end_index].val == "end":
                break
            end_index += 1
        index, action = self.read_block(tokens, index, True)
        node = Statement(cond, action, loop=True)
        self.puts('< End If @' + str(index) + '>')
        self.level_of_ana -= 1
        return index, node
    
    def read_for(self, tokens, index):
        return 99
    
    def read_expr(self, tokens, index, end_index):
        # sorting operators
        working_list = copy.deepcopy(tokens[index:end_index])
        sorted_operators = []
        prio_values = []
        lvl = 1
        index = 0
        after_aug = False
        while index < len(working_list):
            if after_aug:
                after_aug = False
                lvl *= 100
            token = working_list[index]
            token.lvl = lvl
            if self.debug_expression:
                self.puts(f"    working_list {str(index)}. {token} lvl={token.lvl}")
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
                            self.puts('    adding the first operator')
                        sorted_operators.append(index)
                        prio_values.append(Parser.PRIORITIES[token.val] * lvl)
                    else:
                        if self.debug_expression:
                            self.puts('    adding another operator')
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
        if len(sorted_operators) == 0 and len(working_list) > 1:
            raise Exception("[ERROR] Incorrect expression len(sorted_operators) == 0")
        # Resolving operators
        length = len(working_list)
        self.level_of_ana += 1
        self.puts(f'< Expr length={length}>')
        if length <= 0:
            raise Exception("[ERROR] Parser: Empty expression of length = " + str(length))
        elif length == 1:
            if working_list[0].typ in [Token.Boolean, Token.Float, Token.Integer, Token.Identifier, Token.String]:
                node = Terminal(working_list[0])
                results = end_index + 1, node
            else:
                raise Exception("[ERROR] Parser: Expression of length 1 is not valid we have: " + str(working_list[0]))
        else:
            modifier = 0
            while len(sorted_operators) > 0:
                # Debug Display
                if self.debug_expression:
                    self.puts('====================')
                    self.puts('    Sorted Operators')
                    for so in range(0, len(sorted_operators)):
                        self.puts('        ' + str(so) + '. ' + str(sorted_operators[so]) + ' -> ' + str(working_list[sorted_operators[so] + modifier]) + ' modifier = ' + str(modifier))
                    self.puts('    Starting to resolve')
                    self.puts('    Working copy (start):')
                    for j in range(0, len(working_list)):
                        self.puts('        ' + str(j) + '. ' + str(working_list[j]))
                # End of Debug Display
                operator_index = sorted_operators[0] + modifier
                if self.debug_expression:
                    self.puts(f'    Resolving 0. in sorted_operators is : {operator_index} referencing token : {working_list[operator_index]}')
                left = working_list[operator_index - 1]
                if not isinstance(left, Node):
                    left = Terminal(left)
                # Right parameter
                right = None
                #print('len working list =', len(working_list))
                #print('ope index =', operator_index)
                #if len(working_list) > operator_index + 1:
                #    print('ope lvl =', working_list[operator_index + 1].lvl)
                #    print('param lvl =', working_list[operator_index].lvl)
                # We must have a parameter and its priority/lvl must be superior : ( "abc" ) abc is lvl = 100 vs () "abc" abc is lvl = 1
                if working_list[operator_index].val == 'call(':
                    if len(working_list) > operator_index + 1 and working_list[operator_index + 1].lvl > working_list[operator_index].lvl:
                        right = working_list[operator_index + 1]
                # We must have a parameter (? and for unary op ?)
                else:
                    if len(working_list) > operator_index + 1:
                        right = working_list[operator_index + 1]
                if right is not None and not isinstance(right, Node):
                    right = Terminal(right)
                op = Terminal(working_list[operator_index])
                self.puts('    < BinOp />')
                #print('debug OPERATOR>', type(op.typ), op.typ, op.content)
                #print('debug> LEFT', type(left), left, 'END')
                #print('debug> RIGHT', type(right), right, 'END')
                node = Operation(
                    op,
                    left,
                    right
                )
                # update working list
                #print('Updating working list')
                #print('< Before')
                #print(operator_index)
                #for i, e in enumerate(working_list):
                #    print(i, type(e), e)
                del working_list[operator_index - 1]
                del working_list[operator_index - 1]
                if right is not None: # f()
                    del working_list[operator_index - 1]
                working_list.insert(operator_index - 1, node)
                #print('> After')
                #for i, e in enumerate(working_list):
                #    print(i, type(e), e)
                # update sorted operators
                #print('Updating sorted operators')
                #print('< Before')
                #print(sorted_operators)
                del sorted_operators[0]
                for so in range(0, len(sorted_operators)):
                    if sorted_operators[so] > operator_index:
                        if right is not None: # f()
                            sorted_operators[so] -= 2
                        else:
                            sorted_operators[so] -= 1
                #print('> After')
                #print(sorted_operators)
            results = end_index + 1, node
        
        #    elif tokens[index + 1].typ == Token.Separator and tokens[index + 1].val == '(':
        #        self.puts('    < FunCall />')
        #        node = FunCall(Terminal(tokens[index]), Terminal(tokens[index + 2])) # writeln ( "Hello!" ) 0 1 2
        #        results = index + 4, node # +1 for ")"
        #    else:
        #        raise Exception("Non valid expression: " + str(tokens[index]))
        self.puts('< End Expr @' + str(results[0]) + '>')
        self.level_of_ana -= 1
        return results
    
    def sort_operators(self, tokens):
        """Sort the operator by priority"""

    
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
        shell.write(prompt + msg + '\n', "TODO")
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
        shell.write(prompt + msg, "TODO")
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

class Interpreter:
    
    def __init__(self, debug=False):
        self.vars = {}
        self.vars['writeln'] = writeln
        self.vars['write'] = write
        self.vars['readint'] = readint
        self.vars['readstr'] = readstr
        self.debug = debug

    def set_debug(self):
        self.debug = not self.debug
    
    def do_elem(self, elem, affectation=False, Scope=None):
        if self.debug:
            if type(elem) == Terminal:
                print(type(elem), '::', elem)
            else:
                print(type(elem), '::\n', elem)
        if type(elem) == Operation:
            #print('do operation', elem)
            if elem.operator.content.val == '+':
                return self.do_elem(elem.left) + self.do_elem(elem.right)
            elif elem.operator.content.val == '-':
                return self.do_elem(elem.left) - self.do_elem(elem.right)
            elif elem.operator.content.val == '*':
                return self.do_elem(elem.left) * self.do_elem(elem.right)
            elif elem.operator.content.val == '/':
                return self.do_elem(elem.left) / self.do_elem(elem.right)
            elif elem.operator.content.val == '%':
                return self.do_elem(elem.left) % self.do_elem(elem.right)
            elif elem.operator.content.val == '**':
                return self.do_elem(elem.left) ** self.do_elem(elem.right)
            elif elem.operator.content.val == '//':
                return self.do_elem(elem.left) // self.do_elem(elem.right)
            # Affectation
            elif elem.operator.content.val == '=':
                val = self.do_elem(elem.right)
                ids = self.do_elem(elem.left, affectation=True)
                self.vars[ids] = val
                if self.debug: print('[EXEC] =', val, 'to', ids)
                return self.vars[ids]
            elif elem.operator.content.val == '+=':
                val = self.do_elem(elem.right)
                ids = self.do_elem(elem.left, affectation=True)
                self.vars[ids] += val
                return self.vars[ids]
            elif elem.operator.content.val == '-=':
                val = self.do_elem(elem.right)
                ids = self.do_elem(elem.left, affectation=True)
                self.vars[ids] -= val
                return self.vars[ids]
            # Comparison
            elif elem.operator.content.val == '==':
                r = self.do_elem(elem.left) == self.do_elem(elem.right)
                if self.debug: print('[EXEC] == ', r)
                return r
            elif elem.operator.content.val == '!=':
                return self.do_elem(elem.left) != self.do_elem(elem.right)
            elif elem.operator.content.val == '<':
                return self.do_elem(elem.left) < self.do_elem(elem.right)
            elif elem.operator.content.val == '<=':
                return self.do_elem(elem.left) <= self.do_elem(elem.right)
            elif elem.operator.content.val == '>=':
                return self.do_elem(elem.left) >= self.do_elem(elem.right)
            elif elem.operator.content.val == '>':
                return self.do_elem(elem.left) > self.do_elem(elem.right)
            # Boolean
            elif elem.operator.content.val == 'and':
                return self.do_elem(elem.left) and self.do_elem(elem.right)
            elif elem.operator.content.val == 'or':
                return self.do_elem(elem.left) or self.do_elem(elem.right)
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
            while cond and (executed == 0 or elem.loop):
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
                return int(elem.content.val)
            elif elem.content.typ == Token.Float:
                return float(elem.content.val)
            elif elem.content.typ == Token.Boolean:
                return elem.content.val == "true"
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
    
    def transpile(self, ast):
        pass

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

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        f = open(filepath, mode='r')
        data = f.read()
        f.close()
        interpreter = Interpreter().do(data)
    else:        
        interpreter = Interpreter()
        parser = Parser(False)
        debug = False
        while True:
            command = input('>>> ')
            if command == 'exit':
                break
            elif command == 'help':
                print('Rey language v0.1 2017-2019')
                print('help    : this help')
                print('tests   : run multiple tests')
                print('reset   : reset interpreter')
                print('debug.x : set/unset debug. x can be parser, interpreter')
                print('locals  : get local variable')
                print('exit    : exit this shell')
            elif command == 'debug':
                debug = not debug
                print('Debug set to', debug)
            elif command == 'debug.parser':
                parser.set_debug()
            elif command == 'debug.interpreter':
                interpreter.set_debug()
            elif command == 'locals':
                for k in sorted(interpreter.vars):
                    print(f"{k:10}", interpreter.vars[k])
            elif command == 'reset':
                interpreter = Interpreter()
            elif command == 'tests':
                read_tests('./tests/tests.txt')      
            else:
                try:
                    res = Tokenizer(False).tokenize(command)
                    ast = parser.parse(res)
                    if debug:
                        print('AST\n', ast)
                    res = interpreter.do_ast(ast)
                    print(res)
                except Exception as e:
                    shell.write(f'[ERROR] Exception: {e}\n', 'COMMENT')
                    traceback.print_exception(*sys.exc_info())
