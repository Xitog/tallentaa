import weyland

rex = weyland.Rex('aaa')
res = rex.match('aaa')
print(res)

print('\nTest lexer')
text = 'if A then 5 end'
print(f'Lex : |{text}| ({len(text)})')
lex = weyland.Lexer(weyland.LANGUAGES['ash']['tokens'])
tokens = lex.lex(text)
for i, t in enumerate(tokens):
    print(i, t)

print('\nRunning regex main()')
weyland.regex.main()

print('\nRunning lexer main()')
weyland.lexer.main()
