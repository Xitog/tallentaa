from rey import Tokenizer, Token, Parser, Interpreter

#-------------------------------------------------------------------------------
# Tests
#-------------------------------------------------------------------------------

results = {}

title = 'Unitary Test n°01 : Boolean false'
print('--- %s ---' % (title,))
res = Tokenizer().tokenize('false')
assert len(res) == 2, "[ERROR] 2 tokens should have been produced! instead:" + str(len(res))
assert type(res[0]) == Token and res[0].val == 'false' and res[0].typ == Token.Boolean, "[ERROR] Token 1 should be Boolean, with the value of 'false'"
assert type(res[1]) == Token and res[1].val == Tokenizer.NEWLINE and res[1].typ == Token.NewLine, "[ERROR] Token 2 should be NewLine, with the value of '\\n' instead: " + str(res[1])
ast = Parser().parse(res)
print('AST:\n', ast.to_s(), sep='', end='')
print('#======== Console ========#')
print('#-------------------------#')
res = Interpreter().do(ast)
print('#-------------------------#')
print('RES:\n    ', res, sep='')
assert res == False, "[ERROR] Result is not equal to False"
print("== OK ==")
results[title] = 'OK'
print()

title = 'Unitary Test n°02 : Boolean true'
print('--- %s ---' % (title,))
res = Tokenizer().tokenize('true')
assert len(res) == 2, "[ERROR] 2 tokens should have been produced! instead:" + str(len(res))
assert type(res[0]) == Token and res[0].val == 'true' and res[0].typ == Token.Boolean, "[ERROR] Token 1 should be Boolean, with the value of 'true'"
assert type(res[1]) == Token and res[1].val == Tokenizer.NEWLINE and res[1].typ == Token.NewLine, "[ERROR] Token 2 should be NewLine, with the value of '\\n' instead: " + str(res[1])
ast = Parser().parse(res)
print('AST:\n', ast.to_s(), sep='', end='')
print('#======== Console ========#')
print('#-------------------------#')
res = Interpreter().do(ast)
print('#-------------------------#')
print('RES:\n    ', res, sep='')
assert res == True, "[ERROR] Result is not equal to True"
print("== OK ==")
results[title] = 'OK'
print()

title = 'Unitary Test n°03 : Boolean T and F'
print('--- %s ---' % (title,))
res = Tokenizer().tokenize('true and false')
assert len(res) == 4, "[ERROR] 4 tokens should have been produced! instead:" + str(len(res))
assert type(res[0]) == Token and res[0].val == 'true' and res[0].typ == Token.Boolean, "[ERROR] Token 1 should be Boolean, with the value of 'true'"
assert type(res[1]) == Token and res[1].val == 'and' and res[1].typ == Token.Operator, "[ERROR] Token 1 should be Operator, with the value of 'and'"
assert type(res[2]) == Token and res[2].val == 'false' and res[2].typ == Token.Boolean, "[ERROR] Token 1 should be Boolean, with the value of 'false'"
assert type(res[3]) == Token and res[3].val == Tokenizer.NEWLINE and res[3].typ == Token.NewLine, "[ERROR] Token 2 should be NewLine, with the value of '\\n' instead: " + str(res[3])
ast = Parser().parse(res)
print('AST:\n', ast.to_s(), sep='', end='')
print('#======== Console ========#')
print('#-------------------------#')
res = Interpreter().do(ast)
print('#-------------------------#')
print('RES:\n    ', res, sep='')
assert res == False, "[ERROR] Result is not equal to False"
print("== OK ==")
results[title] = 'OK'
print()

title = 'Unitary Test n°04 : Boolean T or F'
print('--- %s ---' % (title,))
res = Tokenizer().tokenize('true or false')
assert len(res) == 4, "[ERROR] 4 tokens should have been produced! instead:" + str(len(res))
assert type(res[0]) == Token and res[0].val == 'true' and res[0].typ == Token.Boolean, "[ERROR] Token 1 should be Boolean, with the value of 'true'"
assert type(res[1]) == Token and res[1].val == 'or' and res[1].typ == Token.Operator, "[ERROR] Token 1 should be Operator, with the value of 'or'"
assert type(res[2]) == Token and res[2].val == 'false' and res[2].typ == Token.Boolean, "[ERROR] Token 1 should be Boolean, with the value of 'false'"
assert type(res[3]) == Token and res[3].val == Tokenizer.NEWLINE and res[3].typ == Token.NewLine, "[ERROR] Token 2 should be NewLine, with the value of '\\n' instead: " + str(res[3])
ast = Parser().parse(res)
print('AST:\n', ast.to_s(), sep='', end='')
print('#======== Console ========#')
print('#-------------------------#')
res = Interpreter().do(ast)
print('#-------------------------#')
print('RES:\n    ', res, sep='')
assert res == True, "[ERROR] Result is not equal to True"
print("== OK ==")
results[title] = 'OK'
print()

title = 'Unitary Test n°10 : Simple Addition'
print('--- %s ---' % (title,))
res = Tokenizer().tokenize('5 + 6') # 5 + 6 NL
assert len(res) == 4, "[ERROR] 4 tokens should have been produced! instead:" + str(len(res))
assert type(res[0]) == Token and res[0].val == '5' and res[0].typ == Token.Integer, "[ERROR] Token 1 should be NUM, with the value of '5'"
assert type(res[1]) == Token and res[1].val == '+' and res[1].typ == Token.Operator, "[ERROR] Token 2 should be OP, with the value of '+'"
ast = Parser().parse(res)
print('AST:\n', ast.to_s(), sep='', end='')
print('#======== Console ========#')
print('#-------------------------#')
res = Interpreter().do(ast)
print('#-------------------------#')
print('RES:\n    ', res, sep='')
assert res == 11, "[ERROR] Result is not equal to 11"
print("== OK ==")
results[title] = 'OK'
print()

title = 'Unitary Test n°11 : Double Addition'
print('--- %s ---' % (title,))
res = Tokenizer().tokenize('5 + 6 \n 2 - 1') # 5 + 6 NL
assert len(res) == 8, "[ERROR] 8 tokens should have been produced! instead:" + str(len(res))
assert type(res[4]) == Token and res[4].val == '2' and res[0].typ == Token.Integer, "[ERROR] Token 4 should be NUM, with the value of '2'"
assert type(res[5]) == Token and res[5].val == '-' and res[5].typ == Token.Operator, "[ERROR] Token 5 should be OP, with the value of '-'"
ast = Parser().parse(res)
print('AST:\n', ast.to_s(), sep='', end='')
print('#======== Console ========#')
print('#-------------------------#')
res = Interpreter().do(ast)
print('#-------------------------#')
print('RES:\n    ', res, sep='')
assert res == 1, "[ERROR] Result is not equal to 1"
print("== OK ==")
results[title] = 'OK'
print()

title = 'Unitary Test n°30 : Simple If, One action'
print('--- %s ---' % (title,))
res = Tokenizer().tokenize('a = 5 \n if a == 5 then \n writeln("Hello!") \n end')
assert len(res) == 17, "[ERROR] 17 tokens should have been produced! instead:" + str(len(res))
assert type(res[0]) == Token and res[0].val == 'a' and res[0].typ == Token.Identifier, "[ERROR] Token 1 should be ID, with the value of 'a'"
ast = Parser().parse(res)
print('AST:\n', ast.to_s(), sep='', end='')
print('#======== Console ========#')
print('#-------------------------#')
res = Interpreter().do(ast)
print('#-------------------------#')
print('RES:\n    ', res, sep='')
print("== OK ==")
results[title] = 'OK'
print()

title = 'Unitary Test n°31 : Simple If, Two actions'
print('--- %s ---' % (title,))
res = Tokenizer().tokenize('a = 5 \n if a == 5 then \n writeln("Hello!") \n writeln("World!") \n end')
assert len(res) == 22, "[ERROR] 22 tokens should have been produced! instead:" + str(len(res))
assert type(res[0]) == Token and res[0].val == 'a' and res[0].typ == Token.Identifier, "[ERROR] Token 1 should be ID, with the value of 'a'"
ast = Parser().parse(res)
print('AST:\n', ast.to_s(), sep='', end='')
print('#======== Console ========#')
print('#-------------------------#')
res = Interpreter().do(ast)
print('#-------------------------#')
print('RES:\n    ', res, sep='')
print("== OK ==")
results[title] = 'OK'
print()

print('--- Unitary Test n°32 : Simple Else ---')
res = Tokenizer().tokenize('a = 8 \n if a != 8 then \n writeln("Never!") \n else \n writeln("Hello!") \n end')
assert len(res) == 24, "[ERROR] 24 tokens should have been produced! instead:" + str(len(res))
assert type(res[0]) == Token and res[0].val == 'a' and res[0].typ == Token.Identifier, "[ERROR] Token 1 should be ID, with the value of 'a'"
ast = Parser().parse(res)
print('AST:\n', ast.to_s(), sep='', end='')
print('#======== Console ========#')
print('#-------------------------#')
res = Interpreter().do(ast)
print('#-------------------------#')
print('RES:\n    ', res, sep='')
print("== OK ==")
results[title] = 'OK'
print()

print('--- Unitary Test n°33 : Simple Else, Two actions ---')
res = Tokenizer().tokenize('a = 8 \n if a != 8 then \n writeln("Never!") \n else \n writeln("Hello!") \n writeln("World!") \n end')
assert len(res) == 29, "[ERROR] 29 tokens should have been produced! instead:" + str(len(res))
assert type(res[0]) == Token and res[0].val == 'a' and res[0].typ == Token.Identifier, "[ERROR] Token 1 should be ID, with the value of 'a'"
ast = Parser().parse(res)
print('AST:\n', ast.to_s(), sep='', end='')
print('#======== Console ========#')
print('#-------------------------#')
res = Interpreter().do(ast)
print('#-------------------------#')
print('RES:\n    ', res, sep='')
print("== OK ==")
results[title] = 'OK'
print()

##print('--- Unitary Test n°41 : Simple Elif ---')
##res = Tokenizer().tokenize('a = 5 \n if a != 5 then \n writeln("Never!") \n elif a == 5 then \n writeln("Hello!") \n end')
##assert len(res) == 28, "[ERROR] 28 tokens should have been produced! instead:" + str(len(res))
##assert type(res[0]) == Token and res[0].val == 'a' and res[0].typ == Token.Identifier, "[ERROR] Token 1 should be ID, with the value of 'a'"
##ast = Parser().parse(res)
##print('AST:\n', ast.to_s(), sep='', end='')
##print('RES:\n    ', res, sep='')
##print("== OK ==")
##print()

##print('--- Unitary Test n°5 : Simple While ---')
##res = Tokenizer().tokenize('target, guess = 1..6.random, 0 \n while target != guess do \n writeln(guess) \n guess += 1 \n end')
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
