#ifndef _TOKEN_H
#define _TOKEN_H

#include "Ptr.h"
#include "TokenType.h"

typedef struct {
	Class * class;
    char * str;
    TokenType type;
} Token;

#endif
