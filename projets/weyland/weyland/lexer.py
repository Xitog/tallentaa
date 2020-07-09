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
# For more information about my projects see:
# https://xitog.github.io/dgx (in French)

"""Lexer: a simple lexer"""

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

from weyland.regex import Rex
from copy import copy
from collections import namedtuple
from weyland.languages import LANGUAGES, Language

#-------------------------------------------------------------------------------
# Types
#-------------------------------------------------------------------------------

Test = namedtuple('Test', ['text', 'language', 'nb'])

#-------------------------------------------------------------------------------
# Classes
#-------------------------------------------------------------------------------

class TokenDef:
    
    def __init__(self, typ, pattern, debug=False):
        self.typ = typ
        self.regex = Rex(pattern, debug=False)
    
    def __str__(self):
        return f"TokenDef {self.typ}"

    def __repr__(self):
        return f"{self.typ} {self.regex}"


class Token:

    def __init__(self, typ, val, first, last):
        self.typ = typ
        self.val = val
        self.first = first
        self.last = last
        self.length = self.last - self.first + 1
    
    def __str__(self):
        return f"{self.typ} |{self.val}| ({self.first}, {self.last}) #{self.length}"

    def __repr__(self):
        return str(self)

    def __len__(self):
        return self.length


class LexingException(Exception):
    pass


class Lexer:

    def __init__(self, lang, debug=False):
        self.debug = debug
        self.lang = lang
        self.defs = []
        for typ, values in lang.tokens.items():
            for val in values:
                self.defs.append(TokenDef(typ, val, self.debug))
        if self.debug:
            print('----------------------------------------')
            print('Language')
            print('----------------------------------------')
            print('Types :', len(self.lang.tokens))
            for d in self.lang.tokens:
                print('   ', d)
            print('----------------------------------------')
            print('Token definitions :', len(self.defs))
            for tokdef in self.defs:
                print('   ', repr(tokdef))
            print('----------------------------------------')

    def lex(self, text):
        if self.debug:
            print(f'Texte = |{text}|')
        index = 0
        res = [ None ] * len(self.defs)
        word = ''
        complete = []
        prev_complete = []
        tokens = []
        while index < len(text):
            if self.debug:
                print(f'- {index} -------------------------')
            char = text[index]
            after = text[index + 1] if index + 1 < len(text) else None
            word += char
            for idf in range(len(self.defs)):
                if res[idf] is not None and res[idf] == Rex.Result.NO:
                    if self.debug:
                        print(f'{idf:5d} {self.defs[idf].typ:10s} {str(self.defs[idf].regex):20s} SKIPPED              {word}')
                    continue
                res[idf] = self.defs[idf].regex.match(word)
                if self.debug:
                    print(f'{idf:5d} {self.defs[idf].typ:10s} {str(self.defs[idf].regex):20s} {res[idf].value:20s} {word}')
            partial = list(filter(lambda elem: res[elem] == Rex.Result.PARTIAL, range(len(res))))
            complete = list(filter(lambda elem: res[elem] == Rex.Result.COMPLETE, range(len(res))))
            if self.debug:
                print(f'This turn: {len(partial)} partials and {len(complete)} complete')
            if len(partial) == 0 and len(complete) == 0:
                specifics = list(filter(lambda elem: self.defs[elem].regex.is_specific(), prev_complete))
                if len(prev_complete) == 0:
                    raise LexingException(f'\nLang:[{self.lang.name}]\nSource:\n{text}\nError:\nNo matching token for |{word}| in:\n{self.defs}')
                elif len(prev_complete) > 1 and len(specifics) != 1:
                    msg = ''
                    for p in prev_complete:
                        msg += ' ' + str(self.defs[p])
                    msg += ' specifics = ' + str(specifics)
                    raise LexingException(f'[{self.lang.name}] Multiple matching tokens:' + msg)
                else:
                    if len(prev_complete) > 1:
                        chosen = specifics[0]
                    else:
                        chosen = prev_complete[0]
                    tokens.append(Token(self.defs[chosen].typ, word[:-1], index - len(word) + 1, index - 1))
                    if self.debug:
                        print(f'Token {tokens[-1]}')
                    word = ''
                    index -= 1
                    res = [ None ] * len(self.defs)
            prev_complete = copy(complete)
            index += 1
        # Last token
        specifics = list(filter(lambda elem: self.defs[elem].regex.is_specific(), prev_complete))
        if len(prev_complete) > 1 and len(specifics) != 1:
            msg = ''
            for p in prev_complete:
                msg += ' ' + str(self.defs[p])
            raise LexingException('Multiple matching tokens:' + msg)
        elif len(prev_complete) >= 1 and len(specifics) <= 1:
            if len(prev_complete) > 1:
                chosen = specifics[0]
            else:
                chosen = prev_complete[0]
            tokens.append(Token(self.defs[chosen].typ, word[:-1], index - len(word), index - 1))
            if self.debug:
                print(f'Token {tokens[-1]}')
        if self.debug:
            print('----------------------------------------')
            print('Tokens :', len(tokens))
            print('----------------------------------------')
            for i, tok in enumerate(tokens):
                print('   ', i, tok)
            if len(tokens) > 0:
                print('----------------------------------------')
        return tokens


#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------

def main(debug=False):
    simple_one = {
        'A': ['aaa'],
        'B': ['bbb'],
        'SPACE': [' '],
    }
    test_one = {
        'KEYWORD' : ['bonjour', 'bon'],
        'IDENTIFIER' : ['[@_]$*'],
        'SPECIFIC_INTEGER' : ['08789'],
        'ALL_INTEGER' : ['#+'],
        'OPERATOR' : ['\+', '\+='],
        'NEWLINE' : ['\n'],
        'WRONGINT' : [r'#+$+'], #
        'SPACE': [' '],
    }
    tests = [
        Test(text = 'aaa bbb', language = Language('simple_one', simple_one, {}), nb = 3),
        Test(text = '08789 bonjour', language = Language('test_one', test_one, {}), nb = 3),
        Test(text = '2 22 abc 2a2 a+b', language = Language('test_one', test_one, {}), nb = 11),
        Test(text = 'bonjour 08789 b2974 0b01111 breaka break', language = LANGUAGES['ash'], nb = 11),
        Test(text = 'bonjour bon bonjour 08789 22 abc + += a+b \n c _d 2a2 #a', language = LANGUAGES['ash'], nb = 30)
    ]
    for tst in tests:
        lexer = Lexer(tst.language, debug=debug)
        tokens = lexer.lex(tst.text)
        print()
        print(f'{tst.text} => {tokens} ({len(tokens)})')
        for i, t in enumerate(tokens):
            print(i, t.typ, t.val)
        if len(tokens) != tst.nb:
            print(f'ERROR: Wrong number of tokens, expected: {tst.nb}')
        else:
            print(f'OK')

if __name__ == '__main__':
    main(debug=False)

