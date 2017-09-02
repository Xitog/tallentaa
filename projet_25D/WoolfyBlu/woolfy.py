# tokenize

class Token:
    
    def __init__(self, typ, val):
        self.typ = typ
        self.val = val
    
    def __str__(self):
        return f"{self.typ} [{self.val}]"

class Tokenizer:
    
    START_OF_ID = ['@', '_']
    START_OF_STRING = ['"', "'"]
    START_OF_OPERATOR = ['=', '+', '-', '*', '/', '%', '<', '>', ',', '(', ')', '.', ':', '|', '[', ']', '!']
    
    def __init__(self):
        self.tokens = []
        self.line_count = 0
    
    def read_num(self, line, index):
        print("    " + f'Reading number at {index}, line {self.line_count}, starting with [{line[index]}]')
        word = line[index]
        suspended = False
        index += 1
        while index < len(line) and (line[index].isdigit() or line[index] == '_'):
            if suspended:
                raise Exception("Twice _ in number")
            if line[index] == '_':
                suspended = True
            else:
                suspended = False
                word += line[index]
            index += 1
        t = Token("NUM", word)
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
                raise Exception("Wrong ID with ! or ? inside of it")
            if line[index] in ['!', '?']:
                terminate = True
            word += line[index]
            index += 1
        t = Token("ID", word)
        print("    " + f'Creating token {t} n°{len(self.tokens)}')
        self.tokens.append(t)
        return index

    def read_operator(self, line, index):
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
        t = Token("STR", word)
        print("    " + f'Creating token {t} n°{len(self.tokens)}')
        return index+1
    
    def tokenize(self, filepath):
        source = open(filepath, 'r', encoding='utf8').readlines()
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
                else:
                    raise Exception("What to do with: " + char + "?")
            self.tokens.append(Token("NL", "Newline"))
        print(f'{len(self.tokens)} tokens created.')

Tokenizer().tokenize('woolfy.blu')
print('Script has ended.')
