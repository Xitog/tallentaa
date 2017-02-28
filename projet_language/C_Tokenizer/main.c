//-----------------------------------------------------------------------------
// Libraries
//-----------------------------------------------------------------------------

#include<stdio.h>
#include<stdlib.h>
#include<errno.h>
#include<string.h>
#include <ctype.h>
#include <stdbool.h>
#include <assert.h>

//-----------------------------------------------------------------------------
// Lexer constants
//-----------------------------------------------------------------------------

const int MAX_TOKENS = 1024;
const int MAX_BUFFER = 256;

//-----------------------------------------------------------------------------
// Language definition
//-----------------------------------------------------------------------------

#define FLOAT_SEPARATOR '.'

char * KEYWORDS[] = { "if", "else", "then", "end" };
const int KEYWORDS_SIZE = 4;

char * BOOLEANS[] = { "True", "False" };
const int BOOLEANS_SIZE = 2;

char * OPERATORS_STR[] = { "and", "or", "xor", "not" };
const int OPERATORS_STR_SIZE = 4;

char SYMBOLS_OK_IN_ID[] = { '_' };
const int SYMBOLS_OK_IN_ID_SIZE = 1;

char SYMBOLS_OK_AT_THE_END_OF_ID[] = { '?', '!' };
const int SYMBOLS_OK_AT_THE_END_OF_ID_SIZE = 2;

char OPERATOR_CHARS[] = { '+', '-', '*', '/', '%', '=', '!', '>', '<' };
const int OPERATOR_CHARS_SIZE = 9;

char * OPERATORS[] = { "+", "-", "*", "/", "//", "**", "%", "=", "+=", "-=", "*=", "//=", "**=", "%=", "and", "or", "not", "xor", "==", "!=", ">", ">=", "<", "<=", ">>", "<<"};
const int OPERATORS_SIZE = 26;

char SEPARATORS[] = { '(', ')', ',', '[', ']', '{', '}' };
const int SEPARATORS_SIZE = 7;

//-----------------------------------------------------------------------------
// Tokens
//-----------------------------------------------------------------------------

// Type of tokens
typedef enum {
    // Working types
    NONE,
    NUMBER,
    // Definitive types
    INTEGER,
    FLOAT,
    IDENTIFIER,
    OPERATOR,
    SEPARATOR,
    KEYWORD, // subcase of IDENTIFIER
    BOOLEAN, // subcase of IDENTIFIER
    STRING,
    // UNUSED TYPE
    DISCARD,
    ERROR
} TokenType;

// Type to strings
char * token_str[] = {
    "None",
    "Number",
    "Integer",
    "Float",
    "Identifier",
    "Operator",
    "Separator",
    "Keyword",
    "Boolean",
    "String",
    "Discard",
    "Error"
};

bool string_is_in(char * s, char * table[], int size) {
    for(int i = 0; i < size; i++) {
        if (strcmp(s, table[i]) == 0) {
            return true;
        }
    }
    return false;
}

bool char_is_in(char c, char table[], int size) {
    for(int i = 0; i < size; i++) {
        if (c == table[i]) {
            return true;
        }
    }
    return false;
}

typedef struct {
    TokenType type;
    char * content;
    int line;
} Token;

//-----------------------------------------------------------------------------
// Reader of tokens function
//-----------------------------------------------------------------------------

// Return new pos
int read_num(char * source, long pos, Token * tokens, int * tokens_cpt, int line_cpt) {
    printf("> Reading num\n");
    // Create buffer
    char * buffer = (char *) calloc(MAX_BUFFER, sizeof(char));
    int buffer_cpt = 0;
    // Read
    int rvalue = pos;
    bool end = false;
    bool is_float = false;
    while(!end) {
        char c = source[pos];
        if (isdigit(c) || c == FLOAT_SEPARATOR) {
            buffer[buffer_cpt] = c;
            buffer_cpt += 1;
            pos++;
            if (c == '.') {
                is_float = true;
            }
        } else if (isalpha(c)) {
            printf("  Incorrect identifier starting with numbers\n");
            rvalue = -1;
            end = true;
        } else {
            // Produce token
            printf("  Producing token : %s, returning pos : %i\n", buffer, pos);
            tokens[*tokens_cpt].content = (char *) calloc(buffer_cpt, sizeof(char));
            strcpy(tokens[*tokens_cpt].content, buffer);
            tokens[*tokens_cpt].line = line_cpt;
            if (is_float) {
                tokens[*tokens_cpt].type = FLOAT;
            } else {
                tokens[*tokens_cpt].type = INTEGER;
            }
            *tokens_cpt += 1;
            rvalue = pos;
            end = true;
        }
    }
    // Destroy buffer
    free(buffer);
    return rvalue;
}

// Return new pos
int read_id(char * source, long pos, Token * tokens, int * tokens_cpt, int line_cpt) {
    printf("> Reading id\n");
    // Create buffer
    char * buffer = (char *) calloc(MAX_BUFFER, sizeof(char));
    int buffer_cpt = 0;
    // Read
    int rvalue = pos;
    bool end = false;
    while(!end) {
        char c = source[pos];
        if (isalnum(c) || char_is_in(c, SYMBOLS_OK_IN_ID, SYMBOLS_OK_IN_ID_SIZE)) {
            buffer[buffer_cpt] = c;
            buffer_cpt += 1;
            pos++;
        } else {
            // Produce token
            printf("  Producing token : %s, returning pos : %i\n", buffer, pos);
            tokens[*tokens_cpt].content = (char *) calloc(buffer_cpt, sizeof(char));
            strcpy(tokens[*tokens_cpt].content, buffer);
            tokens[*tokens_cpt].line = line_cpt;
            if (string_is_in(tokens[*tokens_cpt].content, KEYWORDS, KEYWORDS_SIZE)) {
                tokens[*tokens_cpt].type = KEYWORD;
            } else if (string_is_in(tokens[*tokens_cpt].content, BOOLEANS, BOOLEANS_SIZE)) {
                tokens[*tokens_cpt].type = BOOLEAN;
            } else if (string_is_in(tokens[*tokens_cpt].content, OPERATORS_STR, OPERATORS_STR_SIZE)) {
                tokens[*tokens_cpt].type = OPERATOR;
            } else {
                tokens[*tokens_cpt].type = IDENTIFIER;
            }
            *tokens_cpt += 1;
            rvalue = pos;
            end = true;
        }
    }
    // Destroy buffer
    free(buffer);
    return rvalue;
}

// Return new pos
int read_operator(char * source, long pos, Token * tokens, int * tokens_cpt, int line_cpt) {
    printf("> Reading operator\n");
    // Create buffer
    char * buffer = (char *) calloc(MAX_BUFFER, sizeof(char));
    int buffer_cpt = 0;
    // Read
    int rvalue = pos;
    bool end = false;
    while(!end) {
        char c = source[pos];
        if (char_is_in(c, OPERATOR_CHARS, OPERATOR_CHARS_SIZE)) {
            buffer[buffer_cpt] = c;
            buffer_cpt += 1;
            pos++;
        } else {
            // Produce token
            printf("  Producing token : %s, returning pos : %i\n", buffer, pos);
            tokens[*tokens_cpt].content = (char *) calloc(buffer_cpt, sizeof(char));
            strcpy(tokens[*tokens_cpt].content, buffer);
            tokens[*tokens_cpt].line = line_cpt;
            if (string_is_in(tokens[*tokens_cpt].content, OPERATORS, OPERATORS_SIZE)) {
                tokens[*tokens_cpt].type = OPERATOR;
            } else {
                return -1; // No delete, should stop the program right away of memory leak
            }
            *tokens_cpt += 1;
            rvalue = pos;
            end = true;
        }
    }
    // Destroy buffer
    free(buffer);
    return rvalue;
}

//-----------------------------------------------------------------------------
// Lexer : String -> [Tokens]
//-----------------------------------------------------------------------------

void create_token_from_string(char * content, int line_cpt, TokenType ttype, Token * tokens, int * tokens_cpt) {
    printf("    Producing token for %s of type %s at line %i\n", content, token_str[ttype], line_cpt);
    tokens[*tokens_cpt].content = (char *) calloc(strlen(content)+1, sizeof(char));
    strcpy(tokens[*tokens_cpt].content, content);
    tokens[*tokens_cpt].line = line_cpt;
    tokens[*tokens_cpt].type = ttype;
    *tokens_cpt += 1;
}

void create_token_from_char(char content, int line_cpt, TokenType ttype, Token * tokens, int * tokens_cpt) {
    char buffer[2] = "\0"; // <=> { '\0', '\0' };
    buffer[0] = content;
    create_token_from_string(buffer, line_cpt, ttype, tokens, tokens_cpt);
}

void tokenize(char * source, long size, Token * tokens, int * tokens_cpt) {
    long pos = 0;
    int line_cpt = 1;
    while (pos < size) {
        char c = source[pos];
        printf("I read : %x (%c) at %i\n", c, c, pos);
        if (isdigit(c)) {
            pos = read_num(source, pos, tokens, tokens_cpt, line_cpt);
            if (pos == -1) {
                printf("Something bad happened during reading read_num.\n");
                exit(EXIT_FAILURE);
            }
        } else if (c == '\n') { // does not handle macos new line \n\r
            printf(">Reading linux new line (line feed) \\n at %i.\n", pos);
            //printf("  Producing token new line\n");
            create_token_from_char('\n', line_cpt, SEPARATOR, tokens, tokens_cpt);
            pos++;
        } else if (c == '\r') {
            printf(">Reading ms-dos new line (carriage return) \\r at %i.\n", pos);
            if (pos + 1 < size) {
                if (source[pos + 1] == '\n') {
                    printf("  Producing token new line\n");
                    create_token_from_char('\n', line_cpt, SEPARATOR, tokens, tokens_cpt);
                    line_cpt++;
                    pos += 2;
                    continue;
                }
            }
            printf("Malformed end of line, found carriage return (\\r) but missing line feed (\\n).\n");
            exit(EXIT_FAILURE);
        } else if (isalpha(c) || char_is_in(c, SYMBOLS_OK_IN_ID, SYMBOLS_OK_IN_ID_SIZE)) {
            pos = read_id(source, pos, tokens, tokens_cpt, line_cpt);
            if (pos == -1) {
                printf("Something bad happened during reading read_id.\n");
                exit(EXIT_FAILURE);
            }
        } else if (c == ' ') {
            printf(">Reading and discarding space at position %i, advancing at %i.\n", pos, pos+1);
            pos++; // Discard blank
        } else if (c == '\0') {
            printf(">End of source.\n");
            break;
        } else if (char_is_in(c, OPERATOR_CHARS, OPERATOR_CHARS_SIZE)) {
            pos = read_operator(source, pos, tokens, tokens_cpt, line_cpt);
            if (pos == -1) {
                printf("Something bad happened during reading_operator.\n");
                exit(EXIT_FAILURE);
            }
        } else if (char_is_in(c, SEPARATORS, SEPARATORS_SIZE)) {
            create_token_from_char(c, line_cpt, SEPARATOR, tokens, tokens_cpt);
            pos++;
        } else {
            printf("Unknown char : %x\n", c);
            exit(EXIT_FAILURE);
        }
    }
}

//-----------------------------------------------------------------------------
// Utils
//-----------------------------------------------------------------------------

void display_tokens(Token * tokens, int tokens_cpt) {
    printf("[INFO] Tokens produced : %i\n", tokens_cpt);
    int i = 0;
    while (i < tokens_cpt) {
        printf("%i : [%s] %s\n", i+1, token_str[tokens[i].type], tokens[i].content);
        i += 1;
    }
}

int handle_file(char * filename) {
    printf("[INFO] opening(%s)\n", filename);
    
    //-----------------------------------------------------
    // Get size of the file
    //-----------------------------------------------------
    FILE * f = fopen(filename, "rb");
    fseek(f, 0, SEEK_END);
    long size = ftell(f);
    if (size == -1) {
        printf("[ERROR] Unable to read size of the file %s\n", filename);
        return 1;
    }
    printf("[INFO] Size of the file is : %i\n", size);
    fclose(f);
    
    //-----------------------------------------------------
    // Create a buffer for the entire file and fill it
    //-----------------------------------------------------
    char * source = (char *) calloc(size+1, sizeof(char));
    f = fopen(filename, "rb");
    if (f == NULL) {
        fprintf(stderr, "[ERROR] %s : %s\n", filename, strerror(errno));
        return 2;
    }
    long pos = 0;
    int c = 0;
    while (c != EOF) {
        c = fgetc(f);
        source[pos] = c;
        pos+=1;
    }
    fclose(f);
    source[pos] = '\0';
    printf("Source :\n%s\n", source);
    
    //-----------------------------------------------------
    // Check the buffer
    //-----------------------------------------------------
    pos = 0;
    while (pos < size) {
        printf("char in hex : %x (%c) at : %i\n", source[pos], source[pos], pos);
        pos++;
    }

    //-----------------------------------------------------
    // Read the buffer and create tokens
    //-----------------------------------------------------
    Token tokens[MAX_TOKENS];
    int tokens_cpt = 0;
    tokenize(source, size, tokens, &tokens_cpt);
    
    //-----------------------------------------------------
    // Display the token
    //-----------------------------------------------------
    display_tokens(tokens, tokens_cpt);

    return 0;
}

int main(int argc, char * argv[]) {
    //-----------------------------------------------------
    // Test args
    //-----------------------------------------------------
    printf("Tokenizer v0.1\n");
    int i = 0;
    while (i < argc) {
        printf("[INFO] Arg %i : %s\n", i, argv[i]);
        i += 1;
    }
    if (argc == 2) {
        //printf("[ERROR] Usage : tokenizer.exe filename\n");
        //return 1;
        printf("[INFO] File : %s\n", argv[1]);
        handle_file(argv[1]);
    }
    
    //-----------------------------------------------------
    // Tests
    //-----------------------------------------------------
    
    printf("[INFO] Tests\n");
    Token tokens[MAX_TOKENS];
    int tokens_cpt = 0;
    
    // Simple integer
    char * test1 = "123456";
    printf("\nTest 1 : %s\n", test1);
    memset(tokens, MAX_TOKENS, sizeof(Token));
    tokens_cpt = 0;
    tokenize(test1, strlen(test1), tokens, &tokens_cpt);
    display_tokens(tokens, tokens_cpt);
    assert ( tokens_cpt == 1);
    assert ( tokens[0].type == INTEGER);
    
    // Two integers
    char * test2 = "123456 294857";
    printf("\nTest 2 : %s\n", test2);
    memset(tokens, MAX_TOKENS, sizeof(Token));
    tokens_cpt = 0;
    tokenize(test2, strlen(test2), tokens, &tokens_cpt);
    display_tokens(tokens, tokens_cpt);
    assert ( tokens_cpt == 2);
    assert ( tokens[0].type == INTEGER);
    assert ( tokens[1].type == INTEGER);
    assert ( strcmp(tokens[0].content, "123456") == 0);
    assert ( strcmp(tokens[1].content, "294857") == 0);
    
    // A float
    char * test3 = "1.34";
    printf("\nTest 3 : %s\n", test3);
    memset(tokens, MAX_TOKENS, sizeof(Token));
    tokens_cpt = 0;
    tokenize(test3, strlen(test3), tokens, &tokens_cpt);
    display_tokens(tokens, tokens_cpt);
    assert ( tokens_cpt == 1);
    assert ( tokens[0].type == FLOAT);
    assert ( strcmp(tokens[0].content, "1.34") == 0);

    // An identifier
    char * test4 = "hello";
    printf("\nTest 4 : %s\n", test4);
    memset(tokens, MAX_TOKENS, sizeof(Token));
    tokens_cpt = 0;
    tokenize(test4, strlen(test4), tokens, &tokens_cpt);
    display_tokens(tokens, tokens_cpt);
    assert ( tokens_cpt == 1);
    assert ( tokens[0].type == IDENTIFIER);
    assert ( strcmp(tokens[0].content, "hello") == 0);

    // A keyword
    char * test5 = "then";
    printf("\nTest 5 : %s\n", test5);
    memset(tokens, MAX_TOKENS, sizeof(Token));
    tokens_cpt = 0;
    tokenize(test5, strlen(test5), tokens, &tokens_cpt);
    display_tokens(tokens, tokens_cpt);
    assert ( tokens_cpt == 1);
    assert ( tokens[0].type == KEYWORD);
    assert ( strcmp(tokens[0].content, "then") == 0);

    // An identifier starting by '_'
    char * test6 = "_then";
    printf("\nTest 6 : %s\n", test6);
    memset(tokens, MAX_TOKENS, sizeof(Token));
    tokens_cpt = 0;
    tokenize(test6, strlen(test6), tokens, &tokens_cpt);
    display_tokens(tokens, tokens_cpt);
    assert ( tokens_cpt == 1);
    assert ( tokens[0].type == IDENTIFIER);
    assert ( strcmp(tokens[0].content, "_then") == 0);
    
    // A simple operation
    char * test7 = "2.3 + 4";
    printf("\nTest 7 : %s\n", test7);
    memset(tokens, MAX_TOKENS, sizeof(Token));
    tokens_cpt = 0;
    tokenize(test7, strlen(test7), tokens, &tokens_cpt);
    display_tokens(tokens, tokens_cpt);
    assert ( tokens_cpt == 3);
    assert ( tokens[0].type == FLOAT);
    assert ( strcmp(tokens[0].content, "2.3") == 0);
    assert ( tokens[1].type == OPERATOR);
    assert ( strcmp(tokens[1].content, "+") == 0);
    assert ( tokens[2].type == INTEGER);
    assert ( strcmp(tokens[2].content, "4") == 0);

    // A boolean
    char * test8 = "True";
    printf("\nTest 8 : %s\n", test8);
    memset(tokens, MAX_TOKENS, sizeof(Token));
    tokens_cpt = 0;
    tokenize(test8, strlen(test8), tokens, &tokens_cpt);
    display_tokens(tokens, tokens_cpt);
    assert ( tokens_cpt == 1);
    assert ( tokens[0].type == BOOLEAN);
    assert ( strcmp(tokens[0].content, "True") == 0);

    // A simple operation between boolean
    char * test9 = "True and False";
    printf("\nTest 9 : %s\n", test9);
    memset(tokens, MAX_TOKENS, sizeof(Token));
    tokens_cpt = 0;
    tokenize(test9, strlen(test9), tokens, &tokens_cpt);
    display_tokens(tokens, tokens_cpt);
    assert ( tokens_cpt == 3);
    assert ( tokens[0].type == BOOLEAN);
    assert ( strcmp(tokens[0].content, "True") == 0);
    assert ( tokens[1].type == OPERATOR);
    assert ( strcmp(tokens[1].content, "and") == 0);
    assert ( tokens[2].type == BOOLEAN);
    assert ( strcmp(tokens[2].content, "False") == 0);

    // A simple operation with parenthesis
    char * test10 = "4 * (2 + 3)\n";
    printf("\nTest 10 : %s\n", test10);
    memset(tokens, MAX_TOKENS, sizeof(Token));
    tokens_cpt = 0;
    tokenize(test10, strlen(test10), tokens, &tokens_cpt);
    display_tokens(tokens, tokens_cpt);
    assert ( tokens_cpt == 8);
    assert ( tokens[0].type == INTEGER);
    assert ( strcmp(tokens[0].content, "4") == 0);
    assert ( tokens[1].type == OPERATOR);
    assert ( strcmp(tokens[1].content, "*") == 0);
    assert ( tokens[2].type == SEPARATOR);
    assert ( strcmp(tokens[2].content, "(") == 0);
    assert ( tokens[3].type == INTEGER);
    assert ( strcmp(tokens[3].content, "2") == 0);
    assert ( tokens[4].type == OPERATOR);
    assert ( strcmp(tokens[4].content, "+") == 0);
    assert ( tokens[5].type == INTEGER);
    assert ( strcmp(tokens[5].content, "3") == 0);
    assert ( tokens[6].type == SEPARATOR);
    assert ( strcmp(tokens[6].content, ")") == 0);

    return 0;
    //exit(EXIT_SUCCESS);
    
}
