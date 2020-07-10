import weyland

def display(tokens):
   for i, t in enumerate(tokens):
        print(i, t)
 
rex = weyland.Rex('aaa')
res = rex.match('aaa')
print(res)

print('\nTest lexer')
text = 'if A then 5 end'
print(f'Lex : |{text}| ({len(text)})')
lex = weyland.Lexer(weyland.LANGUAGES['ash'])
tokens = lex.lex(text)
display(tokens)

print('\nTest "abc" "def" with bnf language')
lex = weyland.Lexer(weyland.LANGUAGES['bnf'])
tokens = lex.lex('"abc" "def"')
display(tokens)

print('\nTest [ (A B) C ] D with bnf language')
lex = weyland.Lexer(weyland.LANGUAGES['bnf'])
tokens = lex.lex("[ (A B) C ] D")
display(tokens)

print('\nTest 1999 with game language')
lex = weyland.Lexer(weyland.LANGUAGES['game'], True)
tokens = lex.lex("1999")
display(tokens)

exit()

print('\nRunning regex main()')
weyland.regex.main()

print('\nRunning lexer main()')
weyland.lexer.main()
