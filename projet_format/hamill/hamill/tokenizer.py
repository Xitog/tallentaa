# -----------------------------------------------------------
# MIT Licence (Expat License Wording)
# -----------------------------------------------------------
# Copyright © 2020, Damien Gouteux
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# For more information about the Hamill lightweight markup language see:
# https://xitog.github.io/dgx/informatique/hamill.html

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

import logging
import enum

#-------------------------------------------------------------------------------
# Globals and constants
#-------------------------------------------------------------------------------

languages = {
    'text': {
        'keywords': [],
        'booleans': [],
        'operators': [],
        'separators': [],
        'ante_identifier': [],
        'accept_unknown' : True,
        'line_comment' : None,
        'string_markers' : [],
        'number' : False
    },
    'json': {
        'keywords': ['null'],
        'booleans': ['true', 'false'],
        'operators': [],
        'separators': [],
        'ante_identifier': [],
        'accept_unknown' : True,
        'line_comment' : None,
        'string_markers' : ['"', "'"],
        'number' : True
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
                      '/=', '^=', '.', '='],
        'separators': ['{', '}', '(', ')', '[', ']', ',', ';'],
        'ante_identifier': ['def', 'class'],
        'accept_unknown' : False,
        'line_comment' : '#',
        'string_markers' : ['"', "'"],
        'number' : True
    },
    'game' : {
        'keywords': [],
        'booleans' : [],
        'operators': [':'],
        'separators' : [],
        'ante_identifier': [],
        'accept_unknown': True,
        'line_comment': None,
        'string_markers': [],
        'number' : False
    },
    'hamill' : {
        'keywords': ['var', 'const', 'include', 'require'],
        'booleans' : ['true', 'false'],
        'operators': [':'],
        'separators' : [],
        'ante_identifier': ['var', 'const'],
        'accept_unknown': True,
        'line_comment': None,
        'string_markers': [],
        'number' : True
    },
}

RECOGNIZED_LANGUAGES = list(languages.keys())

#-------------------------------------------------------------------------------
# Data model
#-------------------------------------------------------------------------------

class TokenType(enum.Enum):
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
        return f'({self.start}, {self.stop}) #{self.length} <{self.typ}> = {self.val}'

    def __repr__(self):
        return str(self)

#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------

# tokenize("123 456 abc! 'defg' True (")
def tokenize(text, lang='text'):
    if lang not in RECOGNIZED_LANGUAGES:
        logging.warning(f"Not recognized language: {lang} defaulting to 'text' for {text}") 
        lang = 'text'
    index = 0
    tokens = [] # (start, stop, len, type, val)
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
            wrong = False
            while index < len(text):
                char = text[index]
                if char.isdigit():
                    num += char
                    stop = index
                    length += 1
                    index += 1
                elif char.isalpha():
                    wrong = True
                    break
                else:
                    break
            if not wrong and languages[lang]['number']:
                tokens.append(Token(start, stop, length, TokenType.NUMBER, int(num)))
            else:
                tokens.append(Token(start, stop, length, TokenType.NORMAL, num))
        elif char in languages[lang]['string_markers']:
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
            tokens.append(Token(start, stop, length, TokenType.STRING, string[1:-1]))
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
            typ = TokenType.NORMAL
            if symbol in languages[lang]['keywords']:
                typ = TokenType.KEYWORD
            if symbol in languages[lang]['booleans']:
                typ = TokenType.BOOLEAN
            if len(tokens) > 0 and tokens[-1].val in languages[lang]['ante_identifier']:
                typ = TokenType.IDENTIFIER
            tokens.append(Token(start, stop, length, typ, symbol))
        elif char in languages[lang]['separators']:
            tokens.append(Token(index, index, 1, TokenType.SEPARATOR, char))
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
                tokens.append(Token(start, start + 2, 3, TokenType.OPERATOR,
                                    char + after + after_after))
                index += 3
            elif after is not None and \
                 char + after in languages[lang]['operators']:
                tokens.append(Token(start, start + 1, 2, TokenType.OPERATOR,
                                    char + after))
                index += 2
            elif char in languages[lang]['operators']:
                tokens.append(Token(start, start, 1, TokenType.OPERATOR, char))
                index += 1
        elif char in [' ', '\r', '\t']:
            index += 1
        elif char == '\n':
            tokens.append(Token(index, index, 1, TokenType.NEWLINE, char))
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
            tokens.append(Token(start, index - 1, length, TokenType.COMMENT, comment))
        else:
            if not languages[lang]['accept_unknown']:
                raise Exception('Char unknown: |' + char + '|')
            else:
                index += 1 # no token produced
    #for tok in tokens:
    #    print(tok)
    return tokens

if __name__ == '__main__':
    cmd = ''
    lang = 'python'
    print('Type [exit] to quit, [set <lang>] to set the language (ex: set python).')
    print(f'Lang is set to {lang}.')
    logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s')
    logging.getLogger().setLevel(logging.DEBUG)
    while cmd != 'exit':
        cmd = input('text=')
        if cmd.startswith('set '):
            lg = cmd.replace('set ', '')
            if lg in languages:
                lang = lg
                loggin.info(f'Lang set to {lang}')
            else:
                logging.warning(f'"{lg}" is not a recognized language. Choose one from {", ".join(languages.keys())}')
        elif cmd != 'exit':
            res = tokenize(cmd, lang)
            for i, r in enumerate(res):
                print(f'{i:05d} {r}')
