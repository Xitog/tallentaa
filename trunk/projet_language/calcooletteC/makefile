easy.exe : easy.o List.o Stack.o Parser.o Lexer.o Ptr.o TokenType.o Token.o
	gcc -o easy.exe easy.o List.o Stack.o Ptr.o Parser.o Lexer.o TokenType.o Token.o -std=c99

Parser.o : Parser.c Parser.h
	gcc -c Parser.c -std=c99

Lexer.o : Lexer.c Lexer.h
	gcc -c Lexer.c -std=c99

List.o : List.c List.h
	gcc -c List.c -std=c99

Stack.o : Stack.c Stack.h
	gcc -c Stack.c -std=c99

Ptr.o : Ptr.c Ptr.h
	gcc -c Ptr.c -std=c99

Token.o : Token.c Token.h TokenType.h
	gcc -c Token.c -std=c99

TokenType.o : TokenType.c TokenType.h
	gcc -c TokenType.c -std=c99

easy.o : easy.c Ptr.h Stack.c List.c
	gcc -c easy.c -std=c99

clean :
	rm *.o
