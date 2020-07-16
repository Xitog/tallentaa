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

    def __init__(self, lang, discards=None, debug=False):
        self.debug = debug
        self.lang = lang
        self.defs = []
        self.discards = [] if discards is None else discards
        for typ, values in lang.tokens.items():
            for val in values:
                self.defs.append(TokenDef(typ, val, self.debug))
        if self.debug:
            self.info()

    def ignore(self, typ):
        if isinstance(typ, str):
            self.discards.append(typ)
        elif isinstance(typ, list):
            for t in typ:
                self.ignore(t)
        else:
            raise Exception(f"Unknown type to ignore: {typ} of {type(typ)}")

    def clear_ignored(self):
        self.discards = []
    
    def info(self):
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

    def check(self, string, typs, vals):
        print(f'Text: {string}')
        tokens = self.lex(string)
        if len(tokens) != len(vals):
            print(f'ERROR        Wrong length of tokens expected: len(typs)')
            return False
        print(f'Tokens: {len(tokens)}')
        for i, t in enumerate(tokens):
            if t.typ == typs[i] and t.val == vals[i]:
                print(f'OK  {i:5d}. {t.typ:10s} |{t.val:s}|')
            else:
                print(f'ERROR   {i:5d}. {t.typ:10s} |{t.val:s}|')
                print(f'EXPECTED {typs[i]:10s} |{vals[i]:s}|')
                return False

    def to_html(self, text=None, tokens=None, raws=None):
        if text is None and tokens is None:
            raise LexingException("Nothing send to html")
        elif text is not None and tokens is not None:
            raise LexingException("Send to html text OR tokens, not both!")
        if text is not None:
            tokens = self.lex(text)
        raws = [] if raws is None else raws
        output = ''
        for tok in tokens:
            if tok.typ in raws:
                output += tok.val
            else:
                output += f'<span class="{self.lang}.{tok.typ}">{tok.val}</span>'
        return output

    def lex(self, text):
        if self.debug:
            print(f'Texte = |{text}|')
        index = 0
        res = [ None ] * len(self.defs)
        start = 0
        complete = []
        prev_complete = []
        tokens = []
        while index <= len(text):
            # Get Regex matching the current word
            if self.debug:
                print(f'-- {index:5d} ----------------------------')
            if index < len(text):
                for idf in range(len(self.defs)):
                    if res[idf] is None or res[idf] != Rex.Result.NO:
                        res[idf] = self.defs[idf].regex.match(text[start:index + 1])
                        if self.debug:
                            print(f'{idf:5d} {self.defs[idf].typ:10s} {str(self.defs[idf].regex):20s} {res[idf].value:20s} |{text[start:index + 1]}|')
                partial = list(filter(lambda elem: res[elem] == Rex.Result.PARTIAL, range(len(res))))
                complete = list(filter(lambda elem: res[elem] == Rex.Result.COMPLETE, range(len(res))))
            else:
                partial = []
                complete = []
            # We got too far: deciding the correct matching regex
            if (len(partial) == 0 and len(complete) == 0):
                count = len(prev_complete)
                end = index - 1 if index <= len(text) else index
                if count == 0:
                    raise LexingException(f'\nLang:[{self.lang.name}]\nSource:\n|{text}|\nError:\nNo matching token for |{text[start:index + 1]}| in:\n{self.defs}')
                elif count == 1:
                    tokens.append(Token(self.defs[prev_complete[0]].typ, text[start:end + 1], start, end))
                    if self.debug:
                        print(f'Token {tokens[-1]}')
                elif count > 1:
                    specific = list(filter(lambda elem: self.defs[elem].regex.is_specific(), prev_complete))
                    if len(specific) == 1:
                        chosen = specific[0]
                    else:
                        min_length = None
                        for s in prev_complete:
                            if min_length is None or len(self.defs[s].regex) < min_length:
                                min_length = s
                        corresponding = list(filter(lambda elem: len(self.defs[elem].regex) == min_length, prev_complete))
                        if len(corresponding) > 1:
                            raise LexingEception(f'Multiple matching regex of same length: {corresponding}')
                        else:
                            chosen = min_length
                    tokens.append(Token(self.defs[chosen].typ, text[start:end + 1], start, end))
                    if self.debug:
                        print(f'Token {tokens[-1]}')
                if index == len(text):
                    break
                else:
                    start = index
                    res = [ None ] * len(self.defs)
            else:
                index += 1
            prev_complete = copy(complete) # must be enhanced
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

