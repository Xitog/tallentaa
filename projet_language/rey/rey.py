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
    
    def __init__(self, typ, val):
        self.typ = typ
        self.val = val
    
    def typ2str(self, typ):
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
    
    def __str__(self):
        return f":{self.typ2str(self.typ)}: [{self.val}]"

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
    
    def __init__(self):
        self.tokens = []
        self.line_count = 0
        Tokenizer.START_OF_OPERATOR = []
        for op in Tokenizer.OPERATORS:
            if not op[0].isalpha() and op[0] not in Tokenizer.START_OF_OPERATOR:
                Tokenizer.START_OF_OPERATOR.append(op[0])
    
    def read_num(self, line, index):
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
        print("    " + f'Creating token {t} n°{len(self.tokens)}')
        self.tokens.append(t)
        return index

    def read_id(self, line, index):
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
        else:
            t = Token(Token.ID, word)
        print("    " + f'Creating token {t} n°{len(self.tokens)}')
        self.tokens.append(t)
        return index

    def read_operator(self, line, index):
        print("    " + f'Reading operator at {index}, line {self.line_count}, starting with [{line[index]}]')
        operator = line[index]
        index += 1
        while index < len(line) and line[index] in Tokenizer.START_OF_OPERATOR:
            operator += line[index]
            index += 1
        if operator not in Tokenizer.OPERATORS:
            raise Exception("Operator unknown: " + operator + " at line " + str(self.line_count))
        t = Token(Token.OP, operator)
        print("    " + f'Creating token {t} n°{len(self.tokens)}')
        self.tokens.append(t)
        return index
    
    def read_separator(self, line, index):
        print("    " + f'Reading separator at {index}, line {self.line_count}, starting with [{line[index]}]')
        t = Token(Token.SEP, line[index])
        print("    " + f'Creating token {t} n°{len(self.tokens)}')
        self.tokens.append(t)
        return index+1
    
    def read_string(self, line, index):
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
        print("    " + f'Creating token {t} n°{len(self.tokens)}')
        return index+1
    
    def tokenize(self, source):
        self.tokens.clear()
        if os.path.isfile(source):
            source = open(source, 'r', encoding='utf8').readlines()
        else:
            source = source.split('\n')
        skip = False
        for line in source:
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
            print(line)
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
        print(f'{len(self.tokens)} tokens created.')
        return self.tokens

#-------------------------------------------------------------------------------
# Parser
#-------------------------------------------------------------------------------

class Parser:
    
    def __init__(self):
        pass
    
    def parse(self, tokens):
        pass

#-------------------------------------------------------------------------------
# Transpiler
#-------------------------------------------------------------------------------

class TranspilerPython:
    
    def __init__(self):
        pass
    
    def transpile(self, ast):
        pass

#-------------------------------------------------------------------------------
# Tests
#-------------------------------------------------------------------------------

# Test U1
print('--- Unitary Test n°1 ---')
res = Tokenizer().tokenize('5 + 6') # 5 + 6 NL
assert len(res) == 4, "[ERROR] 4 tokens should have been produced! instead:" + str(len(res))
assert type(res[0]) == Token and res[0].val == '5' and res[0].typ == Token.NUM, "[ERROR] Token 1 should be NUM, with the value of '5'"
assert type(res[1]) == Token and res[1].val == '+' and res[1].typ == Token.OP, "[ERROR] Token 2 should be OP, with the value of '+'"
print()

# Test F1
print('--- File Test n°1 ---')
Tokenizer().tokenize('woolfy.blu')
print()

print('Script has ended.')
