from rey import Tokenizer, Token, Parser, Interpreter

#-------------------------------------------------------------------------------
# Unit tests for Rey language
#-------------------------------------------------------------------------------

results = {}

class Assertion:
    def __init__(self, nb, typ, val):
        self.nb = nb
        self.typ = typ
        self.val = val

def test(title, command, expected, length=None, assertions=None, no_exec=False):
    global results
    print('--- %s ---' % (title,))
    res = Tokenizer().tokenize(command)
    if length is not None:
        assert len(res) == length, f"[ERROR] {length} tokens should have been producted! Instead: {str(len(res))}"
    if assertions is not None and type(assertions) == dict:
        for val in assertions:
            if type(val) != Assertion:
                raise Exception("Only Assertion instance can be handled here.")
            assert type(res[val.nb]) == Token and res[val.nb].val == val.val and res[val.nb].typ == val.typ, f"[ERROR] Token {val.nb} should be {val.typ} with the falue of '{val.val}'. Instead: {res[val.nb]}"
    ast = Parser().parse(res)
    print('AST:\n', ast.to_s(), sep='', end='')
    if not no_exec:
        print('#======== Console ========#')
        print('#-------------------------#')
        res = Interpreter().do(ast)
        print('#-------------------------#')
        print('RES:\n    ', res, sep='')
        assert res == expected, "[ERROR] Result is not equal to " + str(expected) + " instead: " + str(res)
    else:
        print('Execution skipped')
    print("== OK ==")
    results[title] = 'OK'
    print()

test('Unitary Test n°01 : Boolean false', 'false', False, 2, [
    Assertion(0, 'false', Token.Boolean),
    Assertion(1, Tokenizer.NEWLINE, Token.NewLine)
    ])

test('Unitary Test n°02 : Boolean true', 'true', True, 2, [
    Assertion(0, 'true', Token.Boolean),
    Assertion(1, Tokenizer.NEWLINE, Token.NewLine)
    ])

test('Unitary Test n°03 : Boolean T and F', 'true and false', False, 4, [
    Assertion(0, 'true', Token.Boolean),
    Assertion(1, 'and', Token.Operator),
    Assertion(2, 'false', Token.Boolean),
    Assertion(3, Tokenizer.NEWLINE, Token.NewLine)
    ])

test('Unitary Test n°04 : Boolean T or F', 'true or false', True, 4, [
    Assertion(0, 'true', Token.Boolean),
    Assertion(1, 'or', Token.Operator),
    Assertion(2, 'false', Token.Boolean),
    Assertion(3, Tokenizer.NEWLINE, Token.NewLine)
    ])

test('Unitary Test n°10 : Simple Addition', '5 + 6', 11, 4, [
    Assertion(0, '5', Token.Integer),
    Assertion(1, '+', Token.Operator),
    Assertion(2, '6', Token.Integer),
    Assertion(3, Tokenizer.NEWLINE, Token.NewLine)
    ])

test('Unitary Test n°11 : Double Addition', '5 + 6 \n 2 - 1', 1, 8, [
    Assertion(0, '5', Token.Integer),
    Assertion(1, '+', Token.Operator),
    Assertion(2, '6', Token.Integer),
    Assertion(3, Tokenizer.NEWLINE, Token.NewLine),
    Assertion(4, '2', Token.Integer),
    Assertion(5, '-', Token.Operator),
    Assertion(6, '1', Token.Integer),
    Assertion(7, Tokenizer.NEWLINE, Token.NewLine)
    ])

test('Unitary Test n°30 : Simple If, One action', 'a = 5 \n if a == 5 then \n writeln("Hello") \n end', 5, 17, [
    Assertion(0, 'a', Token.Identifier),
    ])

test('Unitary Test n°31 : Simple If, Two actions', 'a = 5 \n if a == 5 then \n writeln("Hello") \n writeln("World!") \n end', 6, 22, [
    Assertion(0, 'a', Token.Identifier),
    ])

test('Unitary Test n°32 : Simple Else', 'a = 8 \n if a != 8 then \n writeln("Never!!!") \n else \n writeln("Hello") \n end', 5, 24, [
    Assertion(0, 'a', Token.Identifier),
    ])

test('Unitary Test n°33 : Simple Else, Two actions', 'a = 8 \n if a != 8 then \n writeln("Never!") \n else \n writeln("Hello") \n writeln("World!") \n end', 6, 29, [
    Assertion(0, 'a', Token.Identifier),
    ])

test('Unitary Test n°50 : Simple While', 'max = 5 \n count = 0 \n while count <= max do \n writeln(count) \n count += 1 \n end', 6, 25, [
    ])

test('Unitary Test n°51 : Guess Game with While', 'target = 1..6.random \n guess = 0 \n count = 0 \n while target != guess do \n writeln(guess) \n guess = 1..6.random \n count += 1 \n end', 6, 41, [
    ], no_exec = True)

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

print('--- File Test n°1 ---')
Tokenizer().tokenize('woolfy.blu')
print()

i = 0
print('+---+--------------------------------------------------------------+-------+')
for r in sorted(results.keys()):
    i += 1
    print(f'|{i:3}| {r:60} | {results[r]:^5} |')

print('+---+--------------------------------------------------------------+-------+')
print()
print(f'{i} tests has been passed.')
print()

print('Script has ended.')
