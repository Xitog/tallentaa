import os.path

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
    Discard     = TokenType('Discard') # Unused
    Error       = TokenType('Error')   # Unused
    EndOfSource = TokenType('End')     # Unused
    
    def __init__(self, typ: TokenType, val: str):
        self.typ = typ
        self.val = val
    
    def __str__(self):
        return f":{self.typ}: [{self.val}]"

class Tokenizer:

    NEWLINE = "New line"
    
    START_OF_ID = ['@', '_', '$']
    START_OF_STRING = ['"', "'"]
    END_OF_STRING = ['?', '!']
    
    SEPARATORS = [
        '(', ')', '[', ']', '{', '}',
        ',', ';',
    ]
    
    OPERATORS = [
        '+', '-', '*', '/', '%', '**', '//',
        '=', '+=', '-=', '*=', '/=', '%=', '**=', '//=',
        '==', '!=', '>', '>=', '<=', '<', '<=>',
        'and', 'or', 'not', 'xor',
        'not', 'in',
        '.', '..', '..<',
        ':', '|', '->',
        '<<', '>>'
    ]

    KEYWORDS = [
        'if', 'unless', 'then', 'elif', 'else', 'end',
        'while', 'until', 'do',
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
    
    def __init__(self):
        self.tokens = []
        self.line_count = 0
        Tokenizer.START_OF_OPERATOR = []
        for op in Tokenizer.OPERATORS:
            if not op[0].isalpha() and op[0] not in Tokenizer.START_OF_OPERATOR:
                Tokenizer.START_OF_OPERATOR.append(op[0])
        self.debug = False
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
        t = Token(Token.Integer, word)
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
            t = Token(Token.Operator, word)
        elif word in Tokenizer.KEYWORDS:
            t = Token(Token.Keyword, word)
        elif word in Tokenizer.BOOLEANS:
            t = Token(Token.Boolean, word)
        else:
            t = Token(Token.Identifier, word)
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
        t = Token(Token.Operator, operator)
        if self.debug:
            print("    " + f'Creating token {t} n°{len(self.tokens)}')
        self.tokens.append(t)
        return index
    
    def read_separator(self, line, index):
        if self.debug:
            print("    " + f'Reading separator at {index}, line {self.line_count}, starting with [{line[index]}]')
        t = Token(Token.Separator, line[index])
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
        t = Token(Token.String, word)
        if self.debug:
            print("    " + f'Creating token {t} n°{len(self.tokens)}')
        self.tokens.append(t)
        return index+1
    
    def tokenize(self, source, debug=False):
        print('[INFO] Start lexing')
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
                if char.isdigit(): # 0 1 2 3 4 5 6 7 8 9
                    index = self.read_number(line, index)
                elif char.isalpha() or char in Tokenizer.START_OF_ID: # a-z A-Z @ _
                    index = self.read_id(line, index)
                elif char.isspace(): # ' ' \n \t
                    index += 1
                elif char in Tokenizer.START_OF_STRING:
                    index = self.read_string(line, index)
                elif char in Tokenizer.START_OF_OPERATOR:
                    index = self.read_operator(line, index)
                elif char in Tokenizer.SEPARATORS:
                    index = self.read_separator(line, index)
                else:
                    raise Exception("What to do with: " + char + "?")
            self.tokens.append(Token(Token.NewLine, Tokenizer.NEWLINE))
            # Pretty print
            if not self.debug:
                print('>>>', "    " * self.line_level, line)
        if self.debug:
            print(f'{len(self.tokens)} tokens created.')
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

class Block:

    def __init__(self):
        self.actions = []

    def add(self, action):
        self.actions.append(action)

    def to_s(self, level=1):
        output = "    " * level + "Block\n"
        for elem in self.actions:
            #print(elem)
            if elem is None:
                output += 'None elem detected'
                raise Exception('ZORBA')
            else:
                output += elem.to_s(level+1)
                if output[-1] != '\n':
                    output += '\n'
        return output

class Terminal:
    
    def __init__(self, content):
        self.content = content
    
    def to_s(self, level=1):
        return "    " * level + str(self.content)
    
    def __str__(self):
         return self.to_s()

class Operation:
    
    def __init__(self, left, op, right):
        assert type(op) == Terminal and op.content.typ == Token.Operator, "Operator should be of type Token.OP"
        self.left = left
        self.right = right
        self.op = op
    
    def to_s(self, level=1):
        name = "BinOp" if self.left is not None and self.right is not None else "unaop"
        return "    " * level + f"{name} {self.left} {self.op} {self.right} \n"

    def __str__(self):
        return self.to_s()

class FunCall:

    def __init__(self, name, arg): # mono arg
        assert type(name) == Terminal and name.content.typ == Token.Identifier, "Name of a function should be an identifier"
        self.name = name
        self.arg = arg

    def to_s(self, level=1):
        typ = "FunCall"
        return "    " * level + f"{typ} {self.name} {self.arg.to_s()} \n"
    
    def __str__(self):
        return self.to_s()

class If:

    def __init__(self, cond, action, alter):
        self.cond = cond
        self.action = action
        self.alter = alter

    def to_s(self, level=1):
        start = "    " * level
        block = "    " * (level + 1)
        s = start + 'if\n' + block + 'Cond:\n' + self.cond.to_s(level + 2)
        s += block + 'Action:\n' + self.action.to_s(level + 2)
        if self.alter is not None:
            s += block + 'Else:\n' + self.alter.to_s(level + 2)
        s += start + 'end\n'
        return s

    def __str__(self):
        return 'if'

class Parser:
    
    def __init__(self):
        self.level_of_ana = 0

    def puts(self, s):
        print("    " * self.level_of_ana + s)
    
    def read_block(self, tokens, index, end_block=False):
        self.level_of_ana += 1
        self.puts('< Block >')
        block = Block()
        level = 0
        while True:
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
                raise Exception('While')
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
        while end_index < len(tokens):
            if tokens[end_index].typ == Token.NewLine or \
                tokens[end_index].typ == Token.Keyword and tokens[end_index].val == "then":
                break
            end_index += 1                
        index, cond = self.read_expr(tokens, index, end_index)
        while end_index < len(tokens):
            if tokens[end_index].typ == Token.Keyword and tokens[end_index].val in ["else", "elif", "end"]:
                break
            end_index += 1
        index, action = self.read_block(tokens, index, True)
        else_action = None
        if tokens[index - 1].typ == Token.Keyword and tokens[index - 1].val == 'else':
            index, else_action = self.read_block(tokens, index, True)
        node = If(cond, action, else_action) # action!
        self.puts('< End If @' + str(index) + '>')
        self.level_of_ana -= 1
        return index, node
    
    def read_while(self, tokens, index):
        return 99

    def read_for(self, tokens, index):
        return 99

    def read_expr(self, tokens, index, end_index):
        self.level_of_ana += 1
        self.puts('< Expr length=' + str(end_index - index) + '>')
        for i in range(index, end_index):
            if tokens[i].typ == Token.NewLine:
                 self.puts('    ' + str(i) +' -> (discarded) ' + str(tokens[i]))
            else:
                self.puts('    ' + str(i) +' -> ' + str(tokens[i]))
        length = end_index - index
        if length <= 0:
            raise Exception("Expression Error: " + str(length))
        elif length == 1:
            if tokens[index].typ in [Token.Boolean, Token.Float, Token.Integer]:
                node = Terminal(tokens[index])
                results = index + 1, node
            else:
                raise Exception("Expression Error: the expression of length 1 is not valid.")
        else:
            while tokens[index].typ == Token.NewLine:
                self.puts('    discard new line')
                index += 1
            if tokens[index + 1].typ == Token.Operator:
                self.puts('    < BinOp />')
                node = Operation(Terminal(tokens[index]), Terminal(tokens[index + 1]), Terminal(tokens[index + 2]))
                results = index + 3 + 1, node # +1 for NL :TODO: Better handling
            elif tokens[index + 1].typ == Token.Separator and tokens[index + 1].val == '(':
                self.puts('    < FunCall />')
                node = FunCall(Terminal(tokens[index]), Terminal(tokens[index + 2])) # writeln ( "Hello!" ) 0 1 2
                results = index + 4, node # +1 for ")"
            else:
                raise Exception("Non valid expression: " + str(tokens[index]))
        self.puts('< End Expr @' + str(results[0]) + '>')
        self.level_of_ana -= 1
        return results

    def parse(self, tokens):
        print('[INFO] Start parsing')
        if tokens is None:
            raise Exception("tokens is None!")
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

class Interpreter:
    
    def __init__(self):
        self.vars = {}
        
    def do_elem(self, elem, aff=False):
        if type(elem) == Operation:
            if elem.op.content.val == '+':
                return self.do_elem(elem.left) + self.do_elem(elem.right)
            elif elem.op.content.val == '-':
                return self.do_elem(elem.left) - self.do_elem(elem.right)
            elif elem.op.content.val == '*':
                return self.do_elem(elem.left) * self.do_elem(elem.right)
            elif elem.op.content.val == '/':
                return self.do_elem(elem.left) / self.do_elem(elem.right)
            elif elem.op.content.val == '%':
                return self.do_elem(elem.left) % self.do_elem(elem.right)
            elif elem.op.content.val == '**':
                return self.do_elem(elem.left) ** self.do_elem(elem.right)
            elif elem.op.content.val == '//':
                return self.do_elem(elem.left) // self.do_elem(elem.right)
            # Affectation
            elif elem.op.content.val == '=':
                val = self.do_elem(elem.right)
                self.vars[self.do_elem(elem.left, aff=True)] = val
                return val
            # Comparison
            elif elem.op.content.val == '==':
                return self.do_elem(elem.left) == self.do_elem(elem.right)
            elif elem.op.content.val == '!=':
                return self.do_elem(elem.left) != self.do_elem(elem.right)
            # Boolean
            elif elem.op.content.val == 'and':
                return self.do_elem(elem.left) and self.do_elem(elem.right)
            elif elem.op.content.val == 'or':
                return self.do_elem(elem.left) or self.do_elem(elem.right)
            else:
                raise Exception("Operator not known: " + elem.op.content.val)
        elif type(elem) == If:
            cond = self.do_elem(elem.cond)
            if cond:
                return self.do_elem(elem.action)
            elif elem.alter is not None:
                return self.do_elem(elem.alter)
            else:
                return None
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
                if aff == True:
                    return elem.content.val
                else:
                    return self.vars[elem.content.val]
            else:
                raise Exception(f"Terminal not known: {elem.content.typ}")
        elif type(elem) == FunCall:
            if elem.name.content.val == 'writeln':
                arg = self.do_elem(elem.arg)
                print(arg)
                return len(arg)
            else:
                raise Exception("Function not known: " + str(elem.name))
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

if __name__ == '__main__':
    while True:
        command = input('>>> ')
        if command == 'exit':
            break
        else:
            res = Tokenizer().tokenize(command)
            ast = Parser().parse(res)
            res = Interpreter().do(ast)
            print(res)
