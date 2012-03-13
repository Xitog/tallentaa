#include "stdlib.h"
#include "stdio.h"
#include "string.h"
#include "ctype.h"

#include "zembla.h"

// TOKENIZER EN C !

// http://www.lysator.liu.se/c/ANSI-C-grammar-l.html
// http://dinosaur.compilertools.net/
// http://eli-project.sourceforge.net/EliExamples.html
// http://www.standardpascal.org/yacclex.html
// http://ashimg.tripod.com/Parser.html
// http://stackoverflow.com/questions/2467020/looking-for-a-java-grammar-in-lex-yacc-format
// http://sablecc.org/
// http://sablecc.sourceforge.net/grammars.html
// http://www.dabeaz.com/ply/
// http://www.ruby-doc.org/docs/ProgrammingRuby/

//#define INIT 1
//#define ID 2
//#define NUM 3

#define or ||
#define and &&

enum Mode { INIT, IDENTIFIER, INTEGER };
typedef enum _TokenType { ID, INT, BINOP, AFF, UNAOP, NL } TokenType;

// Ruby with type
//
// Keywords
//
// selection : if else elsif/elif unless then end
// iteration : while until for do
// 			   break return next/continue
// 			   is, and, or, xor, not
//			   var
//			   fun
//			   class
//			   import, module, include
//
// Littéral
//
// "str" ou 'str' ou """str"""
// 0xHexa (hexadécimal)
// 0b0101 (binary)
// 092 (octal)
// 0.5 .5 0. 0e+23 0e23 0e-23
// v = (a : 5, b : 25) : table
// v.a, v(:a), v("a"), v('a')
// fun(int, int -> int) add = f
// fun add(int a = 3, int b = 5 -> int)
//	 return a+b
// end
// class Personne < Animal
//   include walk
//   fun hello()
//      writeln("hello")
//   end
// end
// p = Personne.new()
// p.hello
// class List(T)
// end
//
// Identifier
//
// $global
// Constante
// @instancevar
// @@classevar
// :symbol
//
// Base type
// bool/Boolean, int/Integer, flt/float/Float, lst/List, dict/Dict, str/string/String, Duration, Date, Time
// num/Number est une classe regroupant Float & Integer. File, Dir. Exception.
//
// Base opérations
// List : <<, ==, is, (), ()=, +/concat, -, *, & (intersection), | (union), get/at, elements, clear, zip, 
// delete, delete_at, empty?, replace, first, last, random, flatten, include?, index, all_index, join/to_s, 
// length/count/size, pop, push, reverse, shift (pop first), slice, sort, uniq, insert_at
// Integer : + - * / % // ** | & << >> ^ ~ <=>, >, >=, <=, <, () -> bit x, size, to_f, to_s, to_i
// Float : + - * / % // ** <=>, >, >=, <=, <, ceil (>= int), finite?, floor (<= int), infinite?, nan?,
// round (plus proche de 0.5), to_f, to_s, to_i
// Boolean and xor or not
// Dict
// String
// Duration
// Date
// Time
// File
// Dir
// Exception
//
// Operators
//
// --General--
// Comparison == != is							3	a is b : a -> @283847 <- b
// --Integer & Float--
// Aritmethic Operator + - / * % // **			6
// Comparison Operator > >= < <= <=> (-1,0,1)	4
// Affectation Operator = += -= /= %= //= **=	7
// --Boolean--
// Binary Operator and or xor					3
// Unary  Operator not							1
// --Binary--
// Binary Operator << >>	& | ^				5
// Unary  Operator ! ~(reverse)					1
// Affectation Operator &= |= ^= <<= >>=		5
// --Others--
// Parenthesis ( )								2
// Separator NL	;								2
// Access Operator .							1
// Comment start #								1
//-----------------------------------------------
//											   41

// Symbole monocaractère	+ - / * % NL .							 6
// Symbole multicaractère 2	+= -= /= %= // ** == != > >= < <= << >>	14
// Symbole multicaractère 3 //= **=									 2
//--------------------------------------------------------------------
//																   	21
// Symbole ambiguë			+ (2) / (4) - (2) % (2) * (4)

typedef struct _Element
{
	struct _Element * next;
	int start;
	int length;
	int line;
	TokenType type;
} Element;

void add(Element ** list, int start, int length, TokenType t)
{
	if (*list == NULL)
	{
		*list = malloc(sizeof(Element));
		(*list)->next = NULL;
		(*list)->start = start;
		(*list)->length = length;
		(*list)->type = t;
	}
	else
	{
		add(&((*list)->next), start, length, t);
	}
}

void print(char * s, Element * list)
{
	if (list == NULL)
	{
		printf("\n");
	}
	else
	{
		char word[50];
		strncpy(word, &s[list->start], list->length);
		word[list->length] = '\0';
		printf("Token : %s of type ", word);
		switch (list->type) 
		{
			case ID:
				printf("ID\n");
				break;
			case INT:
				printf("INT\n");
				break;
			case BINOP:
				printf("BINARY OPERATOR\n");
				break;
			case AFF:
				printf("AFFECTATION OPERATOR\n");
				break;
			case UNAOP:
				printf("UNARY OPERATOR\n");
				break;
			case NL:
				printf("NEWLINE\n");
				break;
		}
		print(s, list->next);
	}
}

char next(char * s, int actual)
{
	if (actual >= strlen(s))
	{
		return 0;
	}
	else
	{
		return s[actual+1];
	}
}

int main (int argc, char * argv[]) 
{
	printf("hello world\n");
	printf("Enter a string:\n");
	char s[100] = "azerty + 12345 += 2 %=";
	//scanf("%30[0-9a-zA-Z ]s", s);
	printf("Entered: %s length: (%d)\n", s, strlen(s));

	Element * tokens = NULL;

	char word[50];
	int start = 0;
	int state = INIT;
	for (int i = 0; i < strlen(s);)
	{
		char n = next(s, i);
		if (state == INIT)
		{
			if (s[i] == '\n')
			{
				printf("Token : Newline\n");
				add(&tokens, i, 1, NL);
				i++;
			}
			else if (s[i] == ' ' || s[i] == '\t')
			{
				i++;
			}
			else if (s[i] == '+' or s[i] == '-' or s[i] == '*' or s[i] == '/' or s[i] == '%' or
				s[i] == '>' or s[i] == '<' or s[i] == '=' or s[i] == '!')
			{
				if (n != '=' and n != '*' and n != '/')
				{
					printf("Token : Operator %c\n", s[i]);
					add(&tokens, i, 1, BINOP);
					i++;
				}
				else if (n == '=')
				{
					printf("Token : AffOperator %c%c\n", s[i], n);
					add(&tokens, i, 2, AFF);
					i+=2;
				}
				//else
				//{
				//	printf("ERROR : UNKNOWN OPERATOR %c%c\n", s[i], n)
				//	exit(1);
				//}
			}
			else if (isalpha(s[i]))
			{
				start = i; //start = &s[i];
				strncpy(word, &s[start], i-start+1);
				word[i-start+1] = '\0';
				printf("%s,", word);
				i++;
				state = IDENTIFIER;
			}
			else if (isdigit(s[i]))
			{
				start = i; //start = &s[i];
				strncpy(word, &s[start], i-start+1);
				word[i-start+1] = '\0';
				printf("%s,", word);
				i++;
				state = INTEGER;
			}
			else
			{
				printf("Error : Unknown character %c", s[i]);
				break;
			}
		}
		else if (state == IDENTIFIER)
		{
			if (isalnum(s[i]))
			{
				strncpy(word, &s[start], i-start+1);
				word[i-start+1] = '\0';
				printf("%s,", word);
				i++;
			}
			else
			{
				printf("\nToken : Identifier %s\n", word);
				add(&tokens, start, i-start, ID);
				state = INIT;
			}
		}
		else if (state == INTEGER)
		{
			if (isdigit(s[i]))
			{
				strncpy(word, &s[start], i-start+1);
				word[i-start+1] = '\0';
				printf("%s,", word);
				i++;
			}
			else
			{
				printf("\nToken : Number %s\n", word);
				add(&tokens, start, i-start, INT);
				state = INIT;
			}
		}
	}
	printf("\n");
	// Traitement de fin
	if (state == IDENTIFIER)
	{
		printf("Token : Identifier %s\n", word);
		add(&tokens, start, strlen(s)-start+1, ID);
	}
	else if (state == INTEGER)
	{
		printf("\nToken : Number %s\n", word);
		add(&tokens, start, strlen(s)-start+1, INT);
	}
	printf("--------\n");
	print(s, tokens);


	// ZEMBLA VIRTUAL MACHINE

	go();

	return 0;
}
