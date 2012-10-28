#include "TokenType.h"
#include "Ptr.h"
#include <string.h>
#include <stdio.h> // Only for debug

int TokenType_count = 0;

const int NB_TOKENS = 44;

TokenType TokenType_create(char * name, char * str, int priority)
{
    TokenType_count += 1;
    
    TokenType tt;
    string_copy(&tt.name, name);
	string_copy(&tt.str, str);
    tt.code = TokenType_count;
    tt.priority = priority;
    return tt;
}

char * TokenType_to_s(TokenType * self)
{
    return self->name;
}

bool TokenType_eq(TokenType * self, TokenType * p)
{
    return (self->code == p->code);
}

bool TokenType_is(TokenType * self, char * str)
{
	return (strcmp(self->str, str)==0);
}

TokenType TokenType_get(char * str)
{
	for (int i = 0; i < NB_TOKENS; i++)
	{
        //printf("%p\n", TOKENS[i]);
        //printf("Get: %s vs %s\n", TOKENS[i]->str, str);
		if (TokenType_is(TOKENS[i], str))
			return *(TOKENS[i]);
	}
}

void TokenType_init()
{
    /* Literals */    
    ID    = TokenType_create("id", "$", 1);
    INT   = TokenType_create("int", "$", 10);
    FLT   = TokenType_create("flt", "$", 1);
    OP    = TokenType_create("op", "$", 999);
    STR   = TokenType_create("str", "$", 1);
    TRUE  = TokenType_create("true", "true", 10);
    FALSE = TokenType_create("false", "false", 10);
    NIL   = TokenType_create("nil", "nil", 1);
    /* Keyword */
    IF    = TokenType_create("if", "if", 1);
    THEN  = TokenType_create("then", "then", 1);
    ELSE  = TokenType_create("else", "else", 1);
    END   = TokenType_create("end", "else", 1);
    WHILE = TokenType_create("while", "else", 1);
    DO    = TokenType_create("do", "do", 1);
    FOR   = TokenType_create("for", "for", 1);
    UNTIL = TokenType_create("until", "until", 1);
    UNLESS= TokenType_create("unless", "unless", 1);
    RETURN= TokenType_create("return", "return", 1);
    BREAK = TokenType_create("break", "break", 1);
    NEXT  = TokenType_create("next", "next", 1);
    REDO  = TokenType_create("redo", "redo", 1);
    REPEAT= TokenType_create("repeat", "repeat", 1);
    BEGIN = TokenType_create("begin", "begin", 1);
    ELSIF = TokenType_create("elsif", "elsif", 1);
    /* Boolean operator and or not xor */
    AND   = TokenType_create("and", "and", 2);
    OR    = TokenType_create("or", "or", 2);
    NOT   = TokenType_create("not", "not", 3);
    XOR   = TokenType_create("xor", "xor", 2);
    /* Comparison operator <= < > >= == != <=> */
    LE    = TokenType_create("le", "<=", 5);
    LT    = TokenType_create("lt", "<", 5);
    GT    = TokenType_create("gt", ">", 5);
    GE    = TokenType_create("ge", ">=", 5);
    EQ    = TokenType_create("eq", "==", 5);
    NE    = TokenType_create("ne", "!=", 5);
    CMP   = TokenType_create("cmp", "<=>", 5);
    /* Arithmetic operator + - * / // % ** */
    ADD   = TokenType_create("add", "+", 7);
    SUB   = TokenType_create("sub", "-", 7);
    MUL   = TokenType_create("mul", "*", 8);
    DIV   = TokenType_create("div", "/", 8);
    INTDIV= TokenType_create("intdiv", "//", 8);
    MOD   = TokenType_create("mod", "%", 8);
    POW   = TokenType_create("pow", "**", 9);
    /* Other operator */
    IN    = TokenType_create("in", "in", 1);
    /* Separator */
    LPAR  = TokenType_create("left par", "(", 1);
    RPAR  = TokenType_create("right par", ")", 1);
    LBRA  = TokenType_create("left bracket", "{", 1);
    RBRA  = TokenType_create("right bracket", "}", 1);
    LSQB  = TokenType_create("left square bracket", "[", 1);
    RSQB  = TokenType_create("right square bracket", "]", 1);
    COMMA = TokenType_create("comma", ",", 1);
    DOT   = TokenType_create("dot", ".", 1);
    SEMICOLON =  TokenType_create("semicolon", ";", 1);
    COLON = TokenType_create("colon", ":", 1);
    NEWLINE   = TokenType_create("newline", "\n", 1);
    /* Affectation operator = += -= *= /= //= %= **= */
    AFF   = TokenType_create("aff", "=", 4);
    AFFADD= TokenType_create("add & aff", "+=", 4);
    AFFSUB= TokenType_create("sub & aff", "-=", 4);
    AFFMUL= TokenType_create("mul & aff", "*=", 4);
    AFFDIV= TokenType_create("div & aff", "/=", 4);
    AFFINTDIV = TokenType_create("intdiv & aff", "//=", 4);
    AFFMOD= TokenType_create("mod & aff", "%=", 4);
    AFFPOW= TokenType_create("pow & aff", "**=", 4);
    /* Binary operator */
    LEFT  = TokenType_create("left shift", "<<", 6);
    RIGHT = TokenType_create("right shift", ">>", 6);
    /* Definition of data */
    CLASS = TokenType_create("class", "class", 1);
    FUN   = TokenType_create("fun", "fun", 1);
    MODULE= TokenType_create("module", "module", 1);
    SELF  = TokenType_create("self", "self", 1);
    SUPER = TokenType_create("super", "super", 1);
    CALLER= TokenType_create("caller", "caller", 1);
	
	TOKENS = (TokenType **) malloc(sizeof(TokenType *) * NB_TOKENS);
	TOKENS[0] = &AND;
	TOKENS[1] = &OR;
	TOKENS[2] = &XOR;
	TOKENS[3] = &NOT;
	TOKENS[4] = &LE;
	TOKENS[5] = &LT;
	TOKENS[6] = &GE;
	TOKENS[7] = &GT;
	TOKENS[8] = &EQ;
	TOKENS[9] = &NE;
	TOKENS[10] = &CMP;
	TOKENS[11] = &ADD;
	TOKENS[12] = &SUB;
	TOKENS[13] = &MUL;
	TOKENS[14] = &DIV;
	TOKENS[15] = &INTDIV;
	TOKENS[16] = &MOD;
	TOKENS[17] = &POW;
	TOKENS[18] = &AFF;
	TOKENS[19] = &AFFADD;
	TOKENS[20] = &AFFSUB;
	TOKENS[21] = &AFFMUL;
	TOKENS[22] = &AFFDIV;
	TOKENS[23] = &AFFINTDIV;
	TOKENS[24] = &AFFMOD;
	TOKENS[25] = &AFFPOW;
	TOKENS[26] = &IF;
	TOKENS[27] = &THEN;
	TOKENS[28] = &ELSE;
	TOKENS[29] = &END;
	TOKENS[30] = &WHILE;
	TOKENS[31] = &DO;
	TOKENS[32] = &FOR;
	TOKENS[33] = &UNTIL;
	TOKENS[34] = &UNLESS;
	TOKENS[35] = &RETURN;
	TOKENS[36] = &BREAK;
	TOKENS[37] = &NEXT;
	TOKENS[38] = &REDO;
	TOKENS[39] = &REPEAT;
	TOKENS[40] = &BEGIN;
	TOKENS[41] = &ELSIF;
    TOKENS[42] = &TRUE;
    TOKENS[43] = &FALSE;
}

bool isComparisonOperator(TokenType * t)
{
    if (TokenType_eq(t, &LE) ||
        TokenType_eq(t, &LT) ||
        TokenType_eq(t, &GE) ||
        TokenType_eq(t, &GT) ||
        TokenType_eq(t, &EQ) ||
        TokenType_eq(t, &NE) ||
        TokenType_eq(t, &CMP) )
    {
        return true;
    }
    return false;
}

bool isArithmeticOperator(TokenType * t)
{
    if (TokenType_eq(t, &ADD)    ||
		TokenType_eq(t, &MUL)    ||
        TokenType_eq(t, &INTDIV) ||
        TokenType_eq(t, &SUB)    ||
        TokenType_eq(t, &MOD)    ||
        TokenType_eq(t, &POW) )
        return true;
    return false;
}

bool isBooleanOperator(TokenType * t)
{
    if (TokenType_eq(t, &AND) ||
        TokenType_eq(t, &OR)  ||
        TokenType_eq(t, &XOR) ||
        TokenType_eq(t, &NOT)  )
        return true;
    return false;
}

bool isBinaryOperator(TokenType * t)
{
    return (isComparisonOperator(t) || isArithmeticOperator(t) || isBooleanOperator(t));
}
