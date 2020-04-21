RECOGNIZED_LANGUAGES = ['text', 'python', 'json']

languages = {
    'text': {
        'keywords': [],
        'booleans': [],
        'operators': [],
        'separators': [],
        'ante_identifier': [],
        'accept_unknown' : True,
        'line_comment' : None
    },
    'json': {
        'keywords': ['null'],
        'booleans': ['true', 'false'],
        'operators': [],
        'separators': [],
        'ante_identifier': [],
        'accept_unknown' : True,
        'line_comment' : None
    },
    'python': {
        'keywords': ['await', 'else', 'import', 'pass', 'break', 'except', 'in',
                     'raise', 'class', 'finally', 'is', 'return', 'and', 'for',
                     'continue', 'lambda', 'try', 'as', 'def', 'from', 'while',
                     'nonlocal', 'assert', 'del', 'global', 'not', 'with', 'if',
                     'async', 'elif', 'or', 'yield'],
        'booleans': ['True', 'False'],
        'operators': ['+', '/', '//', '&', '^', '~', '|', '**', '<<', '%', '*',
                      '-', '>>', ':', '<', '<=', '==', '!=', '>=', '>', '+=',
                      '&=', '//=', '<<=', '%=', '*=', '|=', '**=', '>>=', '-=',
                      '/=', '^=', '.'],
        'separators': ['{', '}', '(', ')', '[', ']', ',', ';'],
        'ante_identifier': ['def', 'class'],
        'accept_unknown' : False,
        'line_comment' : '#'
    }
}

class Token:

    def __init__(self, start, stop, length, typ, val):
        self.start = start
        self.stop = stop
        self.length = length
        self.typ = typ
        self.val = val
        if self.length != self.stop - self.start + 1:
            raise Exception(f"Length is not correct: {self.length} start={self.start} stop={self.stop}")

    def __str__(self):
        return f'({self.start}-{self.stop} #{self.length} <{self.typ}> = {self.val})'

    def __repr__(self):
        return str(self)

# tokenize("123 456 abc! 'defg' True (")
def tokenize(text, lang='text'):
    if lang not in RECOGNIZED_LANGUAGES:
        warn("Not recognized language:", str(lang), "defaulting to text") 
        lang = 'text'
    index = 0
    tokens = [] # (start, stop, len, type, val)
    NORMAL = 'normal'
    KEYWORD = 'keyword'
    STRING = 'string'
    NUMBER = 'number'
    IDENTIFIER = 'identifier'
    OPERATOR = 'operator'
    BOOLEAN = 'boolean'
    NEWLINE = 'newline'
    SEPARATOR = 'separator'
    SPECIAL = 'special'
    COMMENT = 'comment'
    operator_elements = []
    for op in languages[lang]['operators']:
        for ope in op:
            if ope not in operator_elements:
                operator_elements.append(ope)
    while index < len(text):
        # current, after, prev
        char = text[index]
        if index < len(text) - 1:
            after = text[index + 1]
        else:
            after = None
        if index > 0:
            prev = text[index -1 ]
        else:
            prev = None
        # tokenize
        if char.isdigit():
            start = index
            num = ''
            length = 0
            while index < len(text):
                char = text[index]
                if char.isdigit():
                    num += char
                    stop = index
                    length += 1
                    index += 1
                else:
                    break
            tokens.append(Token(start, stop, length, NUMBER, int(num)))
        elif char == '"' or char == "'":
            start = index
            ender = char
            length = 0
            string = ''
            while index < len(text):
                char = text[index]
                string += char
                stop = index
                length += 1
                index += 1
                if char == ender:
                    if length == 1: # first
                        continue
                    else:
                        break
            tokens.append(Token(start, stop, length, STRING, string[1:-1]))
        elif char.isalpha():
            start = index
            symbol = ''
            length = 0
            while index < len(text):
                if index < len(text) - 1:
                    after = text[index + 1]
                else:
                    after = None
                char = text[index]
                if char.isalpha() or char.isdigit() or char == '_' or (char in ['!', '?'] and (after is None or (not after.isalpha() and not after.isdigit()))):
                    symbol += char
                    stop = index
                    length += 1
                    index += 1
                else:
                    break
            typ = NORMAL
            if symbol in languages[lang]['keywords']:
                typ = KEYWORD
            if symbol in languages[lang]['booleans']:
                typ = BOOLEAN
            if len(tokens) > 0 and tokens[-1].val in languages[lang]['ante_identifier']:
                typ = IDENTIFIER
            tokens.append(Token(start, stop, length, typ, symbol))
        elif char in languages[lang]['separators']:
            tokens.append(Token(index, index, 1, SEPARATOR, char))
            index += 1
        elif char in operator_elements:
            start = index
            operator = ''
            length = 0
            if index < len(text) - 1:
                after = text[index + 1]
            else:
                after = None
            if index < len(text) - 2:
                after_after = text[index + 2]
            else:
                after_after = None
            if after is not None and after_after is not None and \
               char + after + after_after in languages[lang]['operators']:
                tokens.append(Token(start, start + 2, 3, OPERATOR,
                                    char + after + after_after))
                index += 3
            elif after is not None and \
                 char + after in languages[lang]['operators']:
                tokens.append(Token(start, start + 1, 2, OPERATOR,
                                    char + after))
                index += 2
            elif char in languages[lang]['operators']:
                tokens.append(Token(start, start, 1, OPERATOR, char))
                index += 1
        elif char in [' ', '\r', '\t']:
            index += 1
        elif char == '\n':
            tokens.append(Token(index, index, 1, NEWLINE, char))
            index += 1
        elif languages[lang]['line_comment'] is not None and \
             (len(languages[lang]['line_comment']) == 1 and char == languages[lang]['line_comment']):
            start = index
            comment = ''
            length = 0
            while index < len(text) and text[index] != '\n':
                comment += text[index]
                index += 1
                length += 1
            tokens.append(Token(start, index - 1, length, COMMENT, comment))
        else:
            if not languages[lang]['accept_unknown']:
                raise Exception('Char unknown: |' + char + '|')
            else:
                index += 1 # no token produced
    #for tok in tokens:
    #    print(tok)
    return tokens
