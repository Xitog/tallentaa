#ifndef _LEXER_H
#define _LEXER_H

#include <stdio.h>
#include <ctype.h>

#include "List.h"
#include "Ptr.h"
#include "TokenType.h"
#include "Token.h"

// States of our state machine.
typedef enum { START = 0, SYMBOL = 1, INTEGER = 2, FLOAT = 3, OPERATOR = 4, COMMENT = 5, STRING_QQ = 6, STRING_Q = 7 } State;

List * lex(char * cmd);

#endif
