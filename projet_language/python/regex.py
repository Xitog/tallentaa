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
#-------------------------------------------------------------------------------
# Language:
#   Special chars for classes:
#       @ = alpha
#       # = digit
#       $ = alpha + digit + _
#   Special chars for repeatability/optionality:
#       * repeat (0, n)
#       + repeat (1, n)
#       ? repeat (0, 1)
#   Escape for special chars and \:
#       \
#   Choice:
#       [xy] => x or y
#       In choice, no repeat, no option, and no sub expression like [(xa)y]

"""Regex: a alternative way to define regex"""

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

from enum import Enum
from collections import namedtuple
import sys

#-------------------------------------------------------------------------------
# Types
#-------------------------------------------------------------------------------

Test = namedtuple('Test', ['regex', 'length', 'candidate', 'expected'])

#-------------------------------------------------------------------------------
# Classes
#-------------------------------------------------------------------------------

class Console:

    def __init__(self):
        try:
            self.puts = sys.stdout.shell.write
        except AttributeError:
            self.puts = None
    
    def write(self, msg, color, end='\n'):
        if self.puts is not None:
            self.puts(msg + end, color)
        else:
            print(msg)


class Element:
    """This class represents a element of a regex."""
    
    def __init__(self, core, option=False, repeat=False, special=False):
        self.option = option
        self.repeat = repeat
        self.special = special
        self.core = core

    def __str__(self):
        return f'{self.core} *={str(self.repeat):5s} ?={str(self.option):5s} !={str(self.special):5s}'

    def __repr__(self):
        return f'|{self.core}|'

    def is_optionnal(self):
        return self.option

    def is_repeatable(self):
        return self.repeat

    def is_choice(self):
        return isinstance(self.core, list)

    def is_included(self, other): # only to check #?#
        if self.is_choice():
            for sub_elem in self.core:
                res = sub_elem.is_included(other)
                if res:
                    return res
            return False
        elif other.is_choice():
            for sub_elem in other.core:
                res = self.is_included(sub_elem)
                if res:
                    return res
            return False
        elif self.special:
            if self.core == '#':
                return other.core == '#' or other.core.isdigit()
            elif self.core == '@':
                return other.core == '@' or other.core.isalpha()
            elif self.core == '$':
                return other.core in ['$', '_'] or other.core.isalnum()
        else:
            return self.core == other.core

    def check(self, candidate):
        if self.is_choice():
            res = False
            for sub_elem in self.core:
                res = sub_elem.check(candidate)
                if res:
                    break
        elif self.special:
            if self.core == '#':   # \d
                res = candidate.isdigit()
            elif self.core == '@': # \a
                res = candidate.isalpha()
            elif self.core == '$': # \w
                res = (candidate.isalnum() or candidate == '_') 
            else:
                raise Exception(f'Unknown special char {self.elements[index].elem}')
        else:
            res = (candidate == self.core)
        return res


class Rex:
    """ This class handles the core of the Regex
        It compiles from a pattern (a simple string)
    """

    MODIFIERS = ['?', '+', '*']
    CLASSES = ['#', '@', '$'] # \d \a \w
    
    def __init__(self, pattern, debug=False):
        self.pattern = pattern
        self.debug = debug
        self.elements = []
        self.compile()

    def __str__(self):
        return f"Regex |{self.pattern}| ({len(self)})"

    def __repr__(self):
        return f"Regex |{self.pattern}|"
    
    def compile(self, start=0, limit=None):
        index = start
        if limit is None:
            limit = len(self.pattern)
        while index < limit:
            c = self.pattern[index]
            if c == '[': # choice
                sub_index = index + 1
                c = self.pattern[sub_index]
                while c != ']' and sub_index < limit:
                    if c == '[': # no choice allowed in choice
                        raise Exception("No choice in choice")
                    elif c == '\\':
                        sub_index += 2
                    elif c in Rex.MODIFIERS:
                        raise Exception("No modifiers ? + * in choice")
                    else:
                        sub_index += 1
                    c = self.pattern[sub_index]
                if c != ']':
                    raise Exception("Uncomplete choice: opening [ has not matching closing ]")
                old = self.elements
                self.elements = []
                self.compile(start=index + 1, limit=sub_index)
                if len(self.elements) < 2:
                    raise Exception("Choice with one or zero element: not a choice")
                sub_elems = self.elements
                self.elements = old
                self.elements.append(Element(sub_elems))
                index = sub_index + 1
            elif c in Rex.MODIFIERS:
                if index == 0:
                    raise Exception(c + " without something to repeat. Did you miss to escape?")
                if c == '?':
                    self.elements[-1].repeat = False
                    self.elements[-1].option = True
                elif c == '+':
                    self.elements[-1].repeat = True
                    self.elements[-1].option = False
                elif c == '*':
                    self.elements[-1].repeat = True
                    self.elements[-1].option = True
                index += 1
            elif c == '\\':
                if index + 1 >= len(self.pattern):
                    raise Exception("A regex cannot finish with an escaped char")
                cnext = self.pattern[index + 1]
                if cnext not in Rex.MODIFIERS + Rex.CLASSES + ['\\']:
                    raise Exception("Unable to escape char: " + cnext)
                self.elements.append(Element(cnext))
                index += 2
            elif c in Rex.CLASSES:
                self.elements.append(Element(c, special=True))
                index += 1
            else:
                self.elements.append(Element(c))
                index += 1
        # Check
        for index, elem in enumerate(self.elements):
            if index < len(self) - 1:
                print(index, elem, self.elements[index + 1], elem.is_included(self.elements[index+1]))
                if elem.is_included(self.elements[index+1]) and elem.is_optionnal():
                    raise Exception("An optionnal element can't be followed by the same non optionnal element.") # x?x forbidden, how to match this?

    def check_at(self, candidate, index):
        if index >= len(self.elements):
            raise Exception('Index out of range of Rex')
        return self.elements[index].check(candidate)

    def __len__(self):
        return len(self.elements)

    def info(self, starter=''):
        index = 0
        print(f'{starter}{self}')
        max_length = 0
        for i, e in enumerate(self.elements):
            print(f'{starter}{i} {e}')

    class Result(Enum):
        NO = 'no'                                 # the regex doesn't match content
        PARTIAL = 'partial'                       # the regex is only matched partially
        COMPLETE = 'complete'                     # the regex is matched
        COMPLETE_OVERLOAD = 'complete & overload' # the regex is matched and there is more
        PARTIAL_OVERLOAD = 'partial & overload'   # the regex is only matched partially and there is more
    
    class ResultX:
        
        def __init__(self, matched):
            self.matched = matched
    
    def match(self, candidate):
        matched = [0] * len(self.elements)
        index_candidate = 0
        index_regex = 0
        final = Rex.Result.NO
        previous = False
        while index_candidate < len(candidate) and index_regex < len(self):
            elem = self.elements[index_regex]
            res = self.check_at(candidate[index_candidate], index_regex)
            if self.debug:
                print(f'    iter {index_candidate=} {index_regex=} {candidate[index_candidate]} vs {elem} => {res}')
            if res:
                matched[index_regex] += 1
                if not elem.is_repeatable():
                    index_regex += 1
                index_candidate += 1
            else:
                if elem.is_optionnal() or (elem.is_repeatable() and matched[index_regex] > 0): # ?/* or (+ and nb > 0)
                    index_regex += 1 # test next
                else:
                    break
        # Get last none empty
        if self.debug:
            print(f'\n    Iter   Element                        Num   Matched')
        res = True
        count = 0
        for i, c in enumerate(matched):
            count += matched[i]
            if self.debug:
                cnd = candidate[i:i+matched[i]]
                print(f'    {i:05d}. {str(self.elements[i]):30s} {matched[i]:05d} {str(cnd):8s}')
            if c == 0 and not self.elements[i].is_optionnal():
                res = False
        if self.debug:
            print(f'    Unmatched: {candidate[count:]} ({len(candidate[count:])})')
            print()
        if res == False:
            if count == len(candidate):
                final = Rex.Result.PARTIAL
            elif count > 0:
                final = Rex.Result.PARTIAL_OVERLOAD
            else:
                final = Rex.Result.NO
        else:
            if count == len(candidate):
                final = Rex.Result.COMPLETE
            else:
                final = Rex.Result.COMPLETE_OVERLOAD
        return final

#-------------------------------------------------
# Tests
#-------------------------------------------------

NO = Rex.Result.NO
PARTIAL = Rex.Result.PARTIAL
COMPLETE = Rex.Result.COMPLETE
COMPLETE_OVERLOAD = Rex.Result.COMPLETE_OVERLOAD
PARTIAL_OVERLOAD = Rex.Result.PARTIAL_OVERLOAD

test_library = {
    100: Test("abc", 3, "zor", NO),
    101: Test("abc", 3, "ab", PARTIAL),
    102: Test("abc", 3, "abc", COMPLETE),
    103: Test("abc", 3, "abcd", COMPLETE_OVERLOAD),

    110: Test("@", 1, "a", COMPLETE),
    111: Test("@", 1, "5", NO),
    112: Test("@", 1, "ab", COMPLETE_OVERLOAD),

    150: Test("a@+", 2, "a5", PARTIAL_OVERLOAD),
    151: Test("a@+", 2, "a", PARTIAL),
    152: Test("a@+", 2, "ab", COMPLETE),
    153: Test("a@+", 2, "abc", COMPLETE),

    154: Test("a@*", 2, "a5", COMPLETE_OVERLOAD),
    155: Test("a@*", 2, "a", COMPLETE),
    156: Test("a@*", 2, "ab", COMPLETE),
    157: Test("a@*", 2, "abc", COMPLETE),

    200: Test("#", 1, "a", NO),
    201: Test("#", 1, "1", COMPLETE),
    202: Test("#", 1, "15", COMPLETE_OVERLOAD),

    220: Test("##", 2, "aa", NO),
    221: Test("##", 2, "a5", NO),
    222: Test("##", 2, "1", PARTIAL),
    223: Test("##", 2, "1a", PARTIAL_OVERLOAD),
    224: Test("##", 2, "15", COMPLETE),
    225: Test("##", 2, "158", COMPLETE_OVERLOAD),
    
    230: Test("##?", 2, "a", NO),
    231: Test("##?", 2, "1", COMPLETE),
    232: Test("##?", 2, "15", COMPLETE),
    233: Test("##?", 2, "158", COMPLETE_OVERLOAD),

    240: Test("##+", 2, "a", NO),
    241: Test("##+", 2, "ab", NO),
    242: Test("##+", 2, "1", PARTIAL),
    243: Test("##+", 2, "1a", PARTIAL_OVERLOAD),
    244: Test("##+", 2, "15", COMPLETE),
    245: Test("##+", 2, "158", COMPLETE),

    500: Test("a\?", 2, "b", NO),
    501: Test("a\?", 2, "a", PARTIAL),
    502: Test("a\?", 2, "a?", COMPLETE),
    503: Test("a\?", 2, "ab", PARTIAL_OVERLOAD),
    504: Test("a\?", 2, "a?b", COMPLETE_OVERLOAD),

    510: Test("a\\\\", 2, "b", NO),
    511: Test("a\\\\", 2, "a", PARTIAL),
    512: Test("a\\\\", 2, "a\\", COMPLETE),
    513: Test("a\\\\", 2, "ab", PARTIAL_OVERLOAD),
    514: Test("a\\\\", 2, "a\\b", COMPLETE_OVERLOAD),

    1000: Test("[ab]", 1, "c", NO),
    1001: Test("[ab]", 1, "a", COMPLETE),
    1002: Test("[ab]", 1, "b", COMPLETE),

    5000: Test(r"[@_]$*[\?!]?", 3, "_a15", COMPLETE),
    5001: Test(r"[@_]$*[\?!]?", 3, "4a", NO),
    5002: Test(r"[@_]$*[\?!]?", 3, "_isalpha?", COMPLETE),

    9000: Test("#?#", None, None, None),
    9001: Test("#?1", None, None, None),
    
    #100: Test(r"[@_]\w*", 2, 1, "_a15", COMPLETE),
    #327: Test(r"\d\d?\d", 3, 2, "123", COMPLETE), # pb
}

tests = test_library.keys() # [327]

DEBUG = False #True

#-------------------------------------------------
# Running the tests if we are main
#-------------------------------------------------

if __name__ == '__main__':
    console = Console()
    previous = None
    for test_index in tests:
        t = test_library[test_index]
        if previous != t.regex:
            print('-----------------------')
            regex = None
            msg = None
            try:
                regex = Rex(t.regex, DEBUG)
            except Exception as e:
                msg = e
            end = '\n' if DEBUG else ''
            if t.length is None:
                if regex is None:
                    console.write(f'= Building of {t.regex} failed as expected: {msg}', color='STRING')
                else:
                    console.write(f"= Building of {t.regex} didn't fail as expected", color='COMMENT')
                continue
            elif len(regex) != t.length:
                console.write(f'= Building {regex} expected ({t.length}) -> KO{end}', color='COMMENT', end=end)
                continue
            console.write(f'= Building {regex} expected ({t.length}) -> OK{end}', color='KEYWORD', end=end)
            if DEBUG:
                regex.info(starter='    ')
        console.write(f'{end}= Matching {t.candidate} vs {regex}{end}', color='KEYWORD')
        res = regex.match(t.candidate)
        res_str = 'ERROR' if res != t.expected else 'OK   '
        color = 'COMMENT' if res != t.expected else 'STRING'
        console.write(f'    {res_str} comparing |{t.candidate}| to regex, expected {t.expected.value} and found {res.value}', color)
        previous = t.regex
