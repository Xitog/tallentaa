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
# Import
#-------------------------------------------------------------------------------

import weyland

#-------------------------------------------------------------------------------
# Function
#-------------------------------------------------------------------------------

def display(tokens):
   print(f'Tokens: {len(tokens)}')
   for i, t in enumerate(tokens):
        print(f'    {i:5d}. {t.typ:10s} ({t.first:3d},{t.last:3d}) |{t.val:s}|')

#-------------------------------------------------------------------------------
# Tests of Regex
#-------------------------------------------------------------------------------
 
rex = weyland.Rex('aaa')
res = rex.match('aaa')
print(res)

#-------------------------------------------------------------------------------
# Tests for the Ash language
#-------------------------------------------------------------------------------

print('\nTest lexer')
text = 'if A then 5 end'
print(f'Lexing: |{text}| ({len(text)})')
lex = weyland.Lexer(weyland.LANGUAGES['ash'])
tokens = lex.lex(text)
display(tokens)

#-------------------------------------------------------------------------------
# Tests for the BNF language
#-------------------------------------------------------------------------------

print('\nTest "abc" "def" with bnf language')
lex = weyland.Lexer(weyland.LANGUAGES['bnf'])
tokens = lex.lex('"abc" "def"')
display(tokens)

print('\nTest [ (A B) C ] D with bnf language')
lex = weyland.Lexer(weyland.LANGUAGES['bnf'])
tokens = lex.lex("[ (A B) C ] D")
display(tokens)

#-------------------------------------------------------------------------------
# Tests for the python language
#-------------------------------------------------------------------------------

print('\nTests of python language')
lex = weyland.Lexer(weyland.LANGUAGES['python'], debug=False)
lex.check("Test 1999",
          ['identifier', 'blank', 'number'],
          ['Test'  , ' '    , '1999'])

#-------------------------------------------------------------------------------
# Tests for the game language
#-------------------------------------------------------------------------------

print('\nTests of game language')
lex = weyland.Lexer(weyland.LANGUAGES['game'], debug=False)
lex.info()

lex.check("Test 1999",
          ['normal', 'blank', 'number'],
          ['Test'  , ' '    , '1999'])

lex.check("3D 3 D3",
          ['normal', 'blank', 'number', 'blank', 'normal'],
          ['3D'    , ' '    , '3'     , ' '    , 'D3'])

lex.check("Baldur's Gate",
          ['normal'  , 'blank', 'normal'],
          ["Baldur's", ' '    , 'Gate'])

lex.check("FarCry: Blood Dragon",
          ['normal', 'operator', 'blank', 'normal', 'blank', 'normal'],
          ['FarCry', ':'       , ' '    , 'Blood' , ' '    , 'Dragon'])

print('Ignore blank')
lex.ignore('blank')
lex.check("Je suis un jeu",
          ['normal', 'normal', 'normal', 'normal'],
          ['Je'    , 'suis'  , 'un'    , 'jeu'])
lex.clear_ignored()

output = lex.to_html(text='Test 1999')
print(output)
assert(output == '<span class="game.normal">Test</span><span class="game.blank"> </span><span class="game.number">1999</span>')

output = lex.to_html(text='Test 1999', raws=['blank'])
print(output)
assert(output == '<span class="game.normal">Test</span> <span class="game.number">1999</span>')

#lex.ignore([1, 'a'])

#-------------------------------------------------------------------------------
# Breaking it: we must trace ALL the completes before (complete + overload)
#-------------------------------------------------------------------------------

funk = weyland.Language('funk', {
            'aaab': ['aaab'],
            'aa': ['aa'],
            'ac': ['ac'],
      })
lex = weyland.Lexer(funk, debug=True)
lex.info()
lex.check("aaac",
          ['aa', 'ac'],
          ['aa', 'ac'])

exit()

#-------------------------------------------------------------------------------
# Main functions of Regex and Lexer
#-------------------------------------------------------------------------------

print('\nRunning regex main()')
weyland.regex.main()

print('\nRunning lexer main()')
weyland.lexer.main()
