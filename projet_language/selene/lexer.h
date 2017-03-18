#ifndef LEXER_LIB
#define LEXER_LIB

//-----------------------------------------------------------------------------
// Libraries
//-----------------------------------------------------------------------------

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>
#include <assert.h>

//-----------------------------------------------------------------------------
// Constants
//-----------------------------------------------------------------------------

extern const int MAX_TOKENS;
extern const int MAX_BUFFER;

//-----------------------------------------------------------------------------
// Constants of language definition
//-----------------------------------------------------------------------------

#define FLOAT_SEPARATOR '.'

extern char * KEYWORDS[];
extern const int KEYWORDS_SIZE;

extern char * BOOLEANS[];
extern const int BOOLEANS_SIZE;

extern char * OPERATORS_STR[];
extern const int OPERATORS_STR_SIZE;

extern char SYMBOLS_OK_IN_ID[];
extern const int SYMBOLS_OK_IN_ID_SIZE;

extern char SYMBOLS_OK_AT_THE_END_OF_ID[];
extern const int SYMBOLS_OK_AT_THE_END_OF_ID_SIZE;

extern char OPERATOR_CHARS[];
extern const int OPERATOR_CHARS_SIZE;

extern char * OPERATORS[];
extern const int OPERATORS_SIZE;

extern char SEPARATORS[];
extern const int SEPARATORS_SIZE;

extern char STRING_DELIMITERS[];
extern const int STRING_DELIMITERS_SIZE;

//-----------------------------------------------------------------------------
// Types
//-----------------------------------------------------------------------------

// Type of tokens warning! change the disposition of token_str if you modify something here
typedef enum {
    // Working types
    NONE,
    NUMBER,
    // Definitive types
    INTEGER,
    FLOAT,
    IDENTIFIER,
        KEYWORD, // subcase of IDENTIFIER identified by read_id
        BOOLEAN, // subcase of IDENTIFIER identified by read_id
    OPERATOR,    // some operator can be identified by read_id
    SEPARATOR,
    STRING,
    // UNUSED TYPE
    DISCARD,
    ERROR
} TokenType;

// Type to strings
extern char * token_str[];

typedef struct {
    TokenType type;
    char * content;
    int line;
} Token;

//-----------------------------------------------------------------------------
// Prototypes
//-----------------------------------------------------------------------------

void tokenize(char * source, long size, Token * tokens, int * tokens_cpt);
void display_tokens(Token * tokens, int tokens_cpt);
int handle_file(char * filename);
void tests_lexer(void);
int test_expression1(Token * tokens);
int test_expression2(Token * tokens);

#endif
