from ash import Test, Assertion, Tokenizer, Token, Parser, Interpreter

#-------------------------------------------------------------------------------
# Unit tests for Rey language
#-------------------------------------------------------------------------------

tests = []

tests.append(Test('Unitary Test n°01 : Boolean false', 'false', False, 2, [
    Assertion(0, 'false', Token.Boolean),
    Assertion(1, Tokenizer.NEWLINE, Token.NewLine)
    ]))

tests.append(Test('Unitary Test n°02 : Boolean true', 'true', True, 2, [
    Assertion(0, 'true', Token.Boolean),
    Assertion(1, Tokenizer.NEWLINE, Token.NewLine)
    ]))

tests.append(Test('Unitary Test n°03 : Boolean T and F', 'true and false', False, 4, [
    Assertion(0, 'true', Token.Boolean),
    Assertion(1, 'and', Token.Operator),
    Assertion(2, 'false', Token.Boolean),
    Assertion(3, Tokenizer.NEWLINE, Token.NewLine)
    ]))

tests.append(Test('Unitary Test n°04 : Boolean T or F', 'true or false', True, 4, [
    Assertion(0, 'true', Token.Boolean),
    Assertion(1, 'or', Token.Operator),
    Assertion(2, 'false', Token.Boolean),
    Assertion(3, Tokenizer.NEWLINE, Token.NewLine)
    ]))

tests.append(Test('Unitary Test n°10 : Simple Addition', '5 + 6', 11, 4, [
    Assertion(0, '5', Token.Integer),
    Assertion(1, '+', Token.Operator),
    Assertion(2, '6', Token.Integer),
    Assertion(3, Tokenizer.NEWLINE, Token.NewLine)
    ]))

tests.append(Test('Unitary Test n°11 : Double Addition', '5 + 6 \n 2 - 1', 1, 8, [
    Assertion(0, '5', Token.Integer),
    Assertion(1, '+', Token.Operator),
    Assertion(2, '6', Token.Integer),
    Assertion(3, Tokenizer.NEWLINE, Token.NewLine),
    Assertion(4, '2', Token.Integer),
    Assertion(5, '-', Token.Operator),
    Assertion(6, '1', Token.Integer),
    Assertion(7, Tokenizer.NEWLINE, Token.NewLine)
    ]))

tests.append(Test('Unitary Test n°FUN01 : Function call, one arg, no caller', 'writeln("Hello!")', 6, 5, [
    Assertion(0, 'writeln', Token.Identifier),
    ]))

tests.append(Test('Unitary Test n°FUN02 : Function call, two args, no caller', 'writeln("Hello", "World!")', 6, 7, [
    Assertion(0, 'writeln', Token.Identifier),
    ]))

tests.append(Test('Unitary Test n°FUN03 : Function call, three args, no caller, writeln', 'writeln("Hello", "World!", 2+3)', expected=1, length=11, assertions=[
    Assertion(0, 'writeln', Token.Identifier),
    ]))

tests.append(Test('Unitary Test n°FUN04 : Function call, three args, no caller, write', 'write("Hello", "World!", 2+3, "\\n")', expected=13, length=13, assertions=[
    Assertion(0, 'writeln', Token.Identifier),
    ]))

tests.append(Test('Unitary Test n°30 : Simple If, One action', 'a = 5 \n if a == 5 then \n writeln("Hello") \n end', 5, 17, [
    Assertion(0, 'a', Token.Identifier),
    ]))

tests.append(Test('Unitary Test n°31 : Simple If, Two actions', 'a = 5 \n if a == 5 then \n writeln("Hello") \n writeln("World!") \n end', 6, 22, [
    Assertion(0, 'a', Token.Identifier),
    ]))

tests.append(Test('Unitary Test n°32 : Simple Else', 'a = 8 \n if a != 8 then \n writeln("Never!!!") \n else \n writeln("Hello") \n end', 5, 24, [
    Assertion(0, 'a', Token.Identifier),
    ]))

tests.append(Test('Unitary Test n°33 : Simple Else, Two actions', 'a = 8 \n if a != 8 then \n writeln("Never!") \n else \n writeln("Hello") \n writeln("World!") \n end', 6, 29, [
    Assertion(0, 'a', Token.Identifier),
    ]))

tests.append(Test('Unitary Test n°50 : Simple While', 'max = 5 \n count = 0 \n while count <= max do \n writeln(count) \n count += 1 \n end', 6, 25, [
    ]))

tests.append(Test('Unitary Test n°51 : Guess Game with While', 'target = (1..6).random \n guess = 0 \n count = 0 \n while target != guess do \n writeln(guess) \n guess = (1..6).random \n count += 1 \n end', 'JUST_DISPLAY', 45, [
    ])) #, no_exec = True))

##print('--- Unitary Test n°41 : Simple Elif ---')
##res = Tokenizer().tokenize('a = 5 \n if a != 5 then \n writeln("Never!") \n elif a == 5 then \n writeln("Hello!") \n end')
##assert len(res) == 28, "[ERROR] 28 tokens should have been produced! instead:" + str(len(res))
##assert type(res[0]) == Token and res[0].val == 'a' and res[0].typ == Token.Identifier, "[ERROR] Token 1 should be ID, with the value of 'a'"
##ast = Parser().parse(res)
##print('AST:\n', ast.to_s(), sep='', end='')
##print('RES:\n    ', res, sep='')
##print("== OK ==")
##print()

# .. > . (en prio)
# Range#random
# writeln

todo = [
    'Unitary Test n°FUN01 : Function call, one arg, no caller',
    'Unitary Test n°FUN02 : Function call, two args, no caller',
    'Unitary Test n°FUN03 : Function call, three args, no caller, writeln',
    'Unitary Test n°FUN04 : Function call, three args, no caller, write',
]

results = {}
restrict = False
for t in tests:
    if t.title in todo or not restrict:
        results[t.title] = t.execute()

print('--- File Test n°1 ---')
Tokenizer().tokenize('woolfy.blu')
print()

i = 0
print('+---+------------------------------------------------------------------------+-------+')
for r in sorted(results.keys()):
    i += 1
    print(f'|{i:3}| {r:70} | {results[r]:^5} |')

print('+---+------------------------------------------------------------------------+-------+')
print()
print(f'{i} tests has been passed.')
print()

print('Script has ended.')
