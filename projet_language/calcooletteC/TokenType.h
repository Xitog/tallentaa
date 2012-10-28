#ifndef _TOKEN_TYPE_H
#define _TOKEN_TYPE_H

#include <stdbool.h>

typedef struct 
{
    char * name;
	char * str;
    int code;
    int priority;
} TokenType;

TokenType ** TOKENS;

/* Literals */    
TokenType ID;
TokenType INT;
TokenType FLT;
TokenType OP;
TokenType STR;
TokenType TRUE;
TokenType FALSE;
TokenType NIL;
/* Keyword */
TokenType IF;
TokenType THEN;
TokenType ELSE;
TokenType END;
TokenType WHILE;
TokenType DO;
TokenType FOR;
TokenType UNTIL;
TokenType UNLESS;
TokenType RETURN;
TokenType BREAK;
TokenType NEXT;
TokenType REDO;
TokenType REPEAT;
TokenType BEGIN;
TokenType ELSIF;
/* Boolean operator and or not xor */
TokenType AND;
TokenType OR;
TokenType NOT;
TokenType XOR;
/* Comparison operator <= < > >= == != <=> */
TokenType LE;
TokenType LT;
TokenType GT;
TokenType GE;
TokenType EQ;
TokenType NE;
TokenType CMP;
/* Arithmetic operator + - * / // % ** */
TokenType ADD;
TokenType SUB;
TokenType MUL;
TokenType DIV;
TokenType INTDIV;
TokenType MOD;
TokenType POW;
/* Other operator */
TokenType IN;
/* Separator */
TokenType LPAR;
TokenType RPAR;
TokenType LBRA;
TokenType RBRA;
TokenType LSQB;
TokenType RSQB;
TokenType COMMA;
TokenType DOT;
TokenType SEMICOLON;
TokenType COLON;
TokenType NEWLINE;
/* Affectation operator = += -= *= /= //= %= **= */
TokenType AFF;
TokenType AFFADD;
TokenType AFFSUB;
TokenType AFFMUL;
TokenType AFFDIV;
TokenType AFFINTDIV;
TokenType AFFMOD;
TokenType AFFPOW;
/* Binary operator */
TokenType LEFT;
TokenType RIGHT;
/* Definition of data */
TokenType CLASS;
TokenType FUN;
TokenType MODULE;
TokenType SELF;
TokenType SUPER;
TokenType CALLER;

// Class Method
void 		TokenType_init			();
TokenType 	TokenType_get			(char * str);
TokenType 	TokenType_create		(char * name, char * str, int priority);
// Instance Method
char * 		TokenType_to_s			(TokenType * self);
bool 		TokenType_eq			(TokenType * self, TokenType * p);
bool 		TokenType_is			(TokenType * self, char * str);
bool        isComparisonOperator    (TokenType * t);
bool        isArithmeticOperator    (TokenType * t);
bool        isBooleanOperator       (TokenType * t);
bool        isBinaryOperator        (TokenType * t);

#endif
