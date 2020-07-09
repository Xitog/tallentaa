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

"""This file provides languages definition"""

#-------------------------------------------------------------------------------
# Globals and constants
#-------------------------------------------------------------------------------

class Language:

    def __init__(self, name, tokens, specials):
        self.name = name
        self.tokens = tokens
        self.specials = specials

LANGUAGES = {
    'text': Language('text', {
            'normal': ['.*'],
            'identifier': [],
            'integer': [],
            'boolean': [],
            'nil': [],
            'keyword': [],
            'operator': [],
            'separator': [],
            'wrong_int': [],
            'blank': [' +'],
            'newline' : ['\n'],
            'line_comment' : [],
        },
        # Special
        {
            'ante_identifier': [],
            'accept_unknown' : True,
            'string_markers' : [],
            'number' : False
        }
    ),
    'json': Language('json', {
            'identifier' : ['[@_]$*'],
            'integer' : ['#+'],
            'boolean': ['true', 'false'],
            'nil': [],
            'keyword': ['null'],
            'operator': [],
            'separator': ['{', '}', '(', ')', r'\[', ']', ',', ':', '"', "'", "\."],
            'wrong_int' : ['#+$+'],
            'blank': [' +'],
            'newline' : ['\n'],
            'line_comment' : [],
        },
        # Special
        {
            'ante_identifier': [],
            'accept_unknown' : True,
            'string_markers' : ['"', "'"],
            'number' : True
        }
    ),
    'ash': Language('ash', {
            # Old
            'AFFECTATION' : ['='],
            'COMBINED_AFFECTATION' : [r'\+=', '-=', r'\*=', '/=', '//=', r'\*\*=', '%='],
            'TYPE' : [':', '->'],
            'FAST' : ['=>'],
            'LABEL' : ['::'],
            'UNARY_OPERATOR' : ['-', 'not', r'\#', '~'],
            # New
            'identifier' : [r'[@_]$*'],
            'integer' : [r'#+'],
            'boolean' : ['false', 'true'],
            'nil': ['nil'],
            'keyword' : ['if', 'then', 'else', 'end', 'while', 'do', 'for',
                 'break', 'next', 'return',
                 'var', 'fun', 'sub', 'get', 'set', 'class',
                 'import', 'from', 'as',
                 'try', 'catch', 'finally', 'raise'],
            'binary_operator' : ['and', 'or', # boolean
                  'in', # belongs to
                  r'\+', '-', r'\*', '/', '//', r'\*\*', '%', # mathematical
                  '&', '|', '~', '>>', '<<', # bitwise
                  '<', '<=', '>', '>=', '==', '!=', # comparison
                  '\.'], # call
            'separator': ['{', '}', '(', ')', r'\[', ']', ',', ';', '"', "'"],
            'wrong_int' : ['#+$+'],
            'blanks': [' +'],
            'newline' : ['\n'],
            'line_comment': ['--'],
        },
        # Special
        {
            'ante_identifier': ['def', 'class'],
            'accept_unknown' : False,
            'string_markers' : ['"', "'"],
            'number' : True
        }
    ),
    'python': Language('python', {
            'identifier' : ['[@_]$*'],
            'integer' : ['#+'],
            'boolean' : ['True', 'False'],
            'nil': ['None'],
            'keyword' : ['await', 'else', 'import', 'pass', 'break', 'except', 'in',
                     'raise', 'class', 'finally', 'is', 'return', 'and', 'for',
                     'continue', 'lambda', 'try', 'as', 'def', 'from', 'while',
                     'nonlocal', 'assert', 'del', 'global', 'not', 'with', 'if',
                     'async', 'elif', 'or', 'yield'],
            'operator': [r'\+', '/', '//', '&', '^', '~', '|', r'\*\*', '<<', '%', r'\*',
                      '-', '>>', ':', '<', '<=', '==', '!=', '>=', '>', r'\+=',
                      '&=', '//=', '<<=', '%=', '\*=', '|=', r'\*\*=', '>>=', '-=',
                      '/=', '^=', '\.', '='],
            'separator': ['{', '}', '(', ')', r'\[', ']', ',', ';'],
            'wrong_int' : ['#+$+'],
            'blank': [' +'],
            'newline' : ['\n'],
            'line_comment': ['\#[. ]+\n'],
            'string': ['"."', "'.'"],
        },
        # Special
        {
            'ante_identifier': ['def', 'class'],
            'accept_unknown' : False,
            'string_markers' : ['"', "'"],
            'number' : True
        }
    ),
    'hamill' : Language('hamill', {
            'identifier' : ['[@_]$*'],
            'integer' : ['#+'],
            'boolean' : ['true', 'false'],
            'nil': [],
            'keyword': ['var', 'const', 'include', 'require', 'css', 'html'],
            'operator': [':'],
            'separator' : ['{', '}', '\#', '.'],
            'wrong_int' : ['#+$+'],
            'blank': [' +'],
            'newline' : ['\n'],
            'line_comment': ['§§'],
        },
        # Special
        {
            'ante_identifier': ['var', 'const'],
            'accept_unknown': True,
            'string_markers': [],
            'number' : True
        }
    ),
}

RECOGNIZED_LANGUAGES = list(LANGUAGES.keys())
