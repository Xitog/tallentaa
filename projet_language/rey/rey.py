import os.path
import copy # only once for read_expr

"""
    Rey
    A simple lexer / parser / interpreter / python transpiler for a small language inspired by Lua/Ruby
    - Tokenizer is working ***
    - Parser is *
    - Interpreter is *
    - Python transpiler is none
    Developed in 2017

= Working pipe

    Symbolizer/lexer/tokenizer    string   -> [tokens]
    Parser                        [tokens] -> abstract syntax tree (AST)
    Interpreter                   AST      -> result
    Python Transpiler             AST      -> python source code

= Data Model

    TokenType
        name: str
    
    Token
        name: str
        typ: TokenType
    
"""

#-------------------------------------------------------------------------------
# Tokenizer/Lexer
#-------------------------------------------------------------------------------

class TokenType:
    
    def __init__(self, name: str):
        self.name = name
    
    def __str__(self):
        return self.name
    
    def __eq__(self, obj):
        if not isinstance(obj, TokenType):
            raise Exception("Cannot compare to objet of type " + str(type(obj)))
        return self.name == obj.name


class Token:
    """
        +typ:enum the type of the token
        +val:string the actual string of the token
    """

    Integer     = TokenType('Integer')
    Float       = TokenType('Float')
    Identifier  = TokenType('Id')
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
    
    def __str__(self):
        if self.start is None or self.length is None:
            return f":{self.typ}: [{self.val}]"
        else:
            return f":{self.typ}: [{self.val}] ({self.start} +{self.length})"
    
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
        self.block_level = 0
        
    def read_number(self, line, index):
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
        t = Token(Token.Integer, word, self.counter)
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
        if debug:
            print('[INFO] Start lexing')
        self.debug = debug
        self.tokens.clear()
        self.block_level = 0
        self.counter = 0
        if os.path.isfile(source):
            source = open(source, 'r', encoding='utf8').readlines()
        else:
            if '\n' in source:
                source = source.split('\n')
                del source[-1] # delete the last element, it will be empty
                source2 = []
                for s in source:
                    source2.append(s + '\n') # add again the ending '\n' to make like readlines
                source = source2
            else:
                source = [source] # only one line
        if debug:
            print('       -------')
            print('       Source:')
            print('       -------')
            for i in range(0, len(source)):
                print(f'           {i}. ' + source[i].replace('\n', '<NEWLINE>'))
            print('       ------')
            print('       Lines:')
            print('       ------')
        skip_line = False
        for line in source:
            self.line_level = self.block_level
            self.line_count += 1
            # comments
            if skip_line or line.strip().startswith('--'):
                t = Token(Token.Comment, line[:-1], self.counter + line.index('--'))
                self.tokens.append(t)
                t = Token(Token.NewLine, "\n", self.counter + len(line) - 1)
                self.tokens.append(t)
                self.counter += len(line)
                continue
            elif line.strip().startswith('=='):
                skip_line = not skip_line
                self.counter += len(line)
                continue
            # analyze line
            if self.debug:
                print('           Analyzing line : ', line.replace('\n', '<NEWLINE>'))
                print('                of length : ', len(line))
            index = 0
            word = None
            while index < len(line):
                previous = index
                char = line[index]
                if char.isdigit(): # 0 1 2 3 4 5 6 7 8 9
                    index = self.read_number(line, index)
                elif char.isalpha() or char in Tokenizer.START_OF_ID: # a-z A-Z @ _
                    index = self.read_id(line, index)
                elif char.isspace() and char != '\n': # ' ' \t
                    index += 1
                elif char in Tokenizer.START_OF_STRING:
                    index = self.read_string(line, index)
                elif char in Tokenizer.START_OF_OPERATOR:
                    index = self.read_operator(line, index)
                elif char in Tokenizer.SEPARATORS:
                    index = self.read_separator(line, index)
                else:
                    raise Exception("What to do with: " + char + "?")
                self.counter += (index - previous)
            # Pretty print
            if self.debug:
                print('>>>', "    " * self.line_level, line)
        if self.debug:
            print(f'[INFO] {len(self.tokens)} tokens created:')
            for i in range(0, len(self.tokens)):
                print(f'{i}. {self.tokens[i]}')
        return self.tokens

#-------------------------------------------------------------------------------
# Parser (Syntaxic analysis)
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
        name = "{Operation} Binary Operation" if self.left is not None and self.right is not None else "Unary Operation"
        s = "    " * level + f"{name} ({self.content.content.val})\n"
        if self.right is not None:
            s += "    " * (level + 2) + ".right =\n"
            s += self.right.to_s(level + 3) + "\n"
        if self.left is not None:
            s += "    " * (level + 2) + ".left =\n"
            s += self.left.to_s(level + 3) + "\n"
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
        if self.debug:
            print('read block', tokens[index].val)
        guard = True if max_index is None else False
        while guard or index < max_index:
            print('.', index, max_index)
            # Test to terminate
            if index >= len(tokens):
                self.puts('    Terminating stream of tokens')
                if end_block: # should have an "end" keyword at the end
                    raise Exception("[ERROR] malformed expression")
                break
            if tokens[index].typ == Token.Keyword and tokens[index].val == 'end' and level == 0:
                self.puts('||| Keyword End found')
                index += 1
                break
            if tokens[index].typ == Token.Keyword and tokens[index].val == 'else' and level == 0:
                self.puts('||| Keyword Else found')
                index += 1
                break
            # Parsing
            self.puts('    read_block:' + str(tokens[index]))
            if tokens[index].typ == Token.Keyword and tokens[index].val in ['if', 'unless']:
                level +=1
                #self.puts('||| :: If/unless')
                index, node = self.read_if(tokens, index + 1)
                block.add(node)
            elif tokens[index].typ == Token.Keyword and tokens[index].val in ['while', 'until']:
                level += 1
                #self.puts('||| :: While/until')
                index, node = self.read_while(tokens, index + 1)
                block.add(node)
            elif tokens[index].typ == Token.Keyword and tokens[index].val == 'end':
                level -= 1
                self.puts('||| :: End')
                index += 1
            elif tokens[index].typ == Token.NewLine:
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
            if tokens[index - 1].typ == Token.Keyword and tokens[index - 1].val == 'else':
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
            self.puts("    working_list " + str(index) + '. ' + str(token) + " lvl=" + str(lvl))
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
                        self.puts('    adding the first operator')
                        sorted_operators.append(index)
                        prio_values.append(Parser.PRIORITIES[token.val] * lvl)
                    else:
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
            raise Exception("[ERROR] Empty expression of length = " + str(length))
        elif length == 1:
            if working_list[0].typ in [Token.Boolean, Token.Float, Token.Integer, Token.Identifier]:
                node = Terminal(working_list[0])
                results = end_index + 1, node
            else:
                raise Exception("[ERROR] Expression of length 1 is not valid we have: " + str(working_list[0]))
        else:
            modifier = 0
            while len(sorted_operators) > 0:
                # Debug Display
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
                self.puts(f'    Resolving 0. in sorted_operators is : {operator_index} referencing token : {working_list[operator_index]}')
                left = working_list[operator_index - 1]
                if not isinstance(left, Node):
                    left = Terminal(left)
                right = working_list[operator_index + 1]
                if not isinstance(right, Node):
                    right = Terminal(right)
                op = Terminal(working_list[operator_index])
                self.puts('    < BinOp />')
                node = Operation(
                    op,
                    left,
                    right
                )
                # update working list
                del working_list[operator_index - 1]
                del working_list[operator_index - 1]
                del working_list[operator_index - 1]
                working_list.insert(operator_index - 1, node)
                # update sorted operators
                del sorted_operators[0]
                for so in range(0, len(sorted_operators)):
                    if sorted_operators[so] > operator_index:
                        sorted_operators[so] -= 2
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
        cleaned = [tok for tok in tokens if tok.typ not in [Token.NewLine, Token.Comment]]
        tokens = cleaned
        index = 0
        ast = AST()
        ast.root = self.read_block(tokens, 0)[1] # index is discared
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

def writeln(arg):
    if isinstance(arg, list):
        res = None
        for i in arg:
            res = writeln(i)
        return res
    else:
        print(arg)
        return len(str(arg))

def write(arg):
    if isinstance(arg, list):
        res = 0
        for i in arg:
            res += write(i)
        return res
    else:
        print(arg, end='')
        return len(str(arg))

class Interpreter:
    
    def __init__(self):
        self.vars = {}
        self.vars['writeln'] = writeln
        self.vars['write'] = write
    
    def do_elem(self, elem, affectation=False, Scope=None):
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
                return self.do_elem(elem.left) == self.do_elem(elem.right)
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
                a = self.do_elem(elem.left)
                #b = self.do_elem(elem.right, scope={random})
                b = elem.right.content.val
                if b == 'random' and type(a) == range:
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
            while cond and (executed == 0 or elem.loop):
                result = self.do_elem(elem.action)
                executed += 1
                if elem.loop:
                    cond = self.do_elem(elem.cond)
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
                        raise Exception(f"Identifier not know: {elem.content.val}")
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
    
    def do(self, ast):
        last = None
        for elem in ast.root.actions:
            last = self.do_elem(elem)
        return last #18h59 8/9

Tests = {
        "2 + 5" : 7,
        "'abc' * 2" : "abcabc",
        "a = true" : True,
        "if a == true then write('hello') end" : 5
    }
if __name__ == '__main__':
    interpreter = Interpreter()
    parser = Parser(False)
    while True:
        command = input('>>> ')
        if command == 'exit':
            break
        elif command == 'help':
            print('Rey language')
            print('help    : this help')
            print('tests   : run multiple tests')
            print('reset   : reset interpreter')
            print('debug.x : set/unset debug. x can be parser')
            print('exit    : exit this shell')
        elif command == 'debug.parser':
            parser.set_debug()
        elif command == 'reset':
            interpreter = Interpreter()
        elif command == 'tests':
            for tst in Tests:
                print('--', tst, '--------------------------')
                try:
                    res = Tokenizer(False).tokenize(tst)
                    ast = parser.parse(res)
                    res = interpreter.do(ast)
                    print('   RES =', res)
                    if res == Tests[tst]:
                        print('-- [SUCCESS] --------------------')
                    else:
                        print('-- [FAILED] ---------------------')
                        print('-- Expected :', Tests[tst])
                except Exception as e:
                    print('-- [FAILED] ---------------------')
                    print('-- Error :', e)
        else:
            #try:
                res = Tokenizer(False).tokenize(command)
                ast = parser.parse(res)
                res = interpreter.do(ast)
                print(res)
            #except Exception as e:
            #    print(e)
