#include<stdio.h>
#include<stdlib.h>
#include<errno.h>
#include<string.h>
#include <ctype.h>
#include <stdbool.h>
#include <assert.h>

#define MAX_TOKENS 1024
#define MAX_BUFFER 256

#define FLOAT_SEPARATOR '.'

#define KEYWORDS { "if", "else", "then", "end" }
#define KEYWORDS_SIZE 4

#define SYMBOLS_OK_IN_ID { '_' }
#define SYMBOLS_OK_IN_ID_SIZE 1

#define SYMBOLS_OK_AT_THE_END_OF_ID { '?', '!' } // TODO but only for fun!

#define OPERATORS { "+", "-", "*", "/", "//", "**", "%", "=", "+=", "-=", "*=", "//=", "**=", "%=", "and", "or", "not", "xor", "==", "!=", ">", ">=", "<", "<=", ">>", "<<"}
#define OPERATORS_SIZE 26

#define SEPARATORS { '(', ')', ',', '[', ']', '{', '}' }
#define SEPARATORS_SIZE 7

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

char * keywords[] = KEYWORDS;

bool is_keyword(char * str) {
    for(int i = 0; i < KEYWORDS_SIZE; i++) {
        if (strcmp(str, keywords[i]) == 0) {
            return true;
        }
    }
    return false;
}

char symbols_ok_in_id[] = SYMBOLS_OK_IN_ID;

bool is_ok_in_id(char c) {
    for(int i = 0; i < SYMBOLS_OK_IN_ID_SIZE; i++) {
        if (c == symbols_ok_in_id[i]) {
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

// Return new pos
int read_num(char * source, long pos, Token * tokens, int * tokens_cpt, int line_cpt) {
    printf(">Reading num\n");
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
    printf(">Reading id\n");
    // Create buffer
    char * buffer = (char *) calloc(MAX_BUFFER, sizeof(char));
    int buffer_cpt = 0;
    // Read
    int rvalue = pos;
    bool end = false;
    while(!end) {
        char c = source[pos];
        if (isalnum(c) || is_ok_in_id(c)) {
            buffer[buffer_cpt] = c;
            buffer_cpt += 1;
            pos++;
        } else {
            // Produce token
            printf("  Producing token : %s, returning pos : %i\n", buffer, pos);
            tokens[*tokens_cpt].content = (char *) calloc(buffer_cpt, sizeof(char));
            strcpy(tokens[*tokens_cpt].content, buffer);
            tokens[*tokens_cpt].line = line_cpt;
            if (is_keyword(tokens[*tokens_cpt].content)) {
                tokens[*tokens_cpt].type = KEYWORD;
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
            printf("  Producing token new line\n");
            pos++;
        } else if (c == '\r') {
            printf(">Reading ms-dos new line (carriage return) \\r at %i.\n", pos);
            if (pos + 1 < size) {
                if (source[pos + 1] == '\n') {
                    printf("  Producing token new line\n");
                    line_cpt++;
                    pos += 2;
                    continue;
                }
            }
            printf("Malformed end of line, found carriage return (\\r) but missing line feed (\\n).\n");
            exit(EXIT_FAILURE);
        } else if (isalpha(c) || is_ok_in_id(c)) {
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
        } else {
            printf("Unknown char : %x\n", c);
            exit(EXIT_FAILURE);
        }
    }
}

void display_tokens(Token * tokens, int tokens_cpt) {
    printf("[INFO] Tokens produced : %i\n", tokens_cpt);
    int i = 0;
    while (i < tokens_cpt) {
        printf("%i : [%s] %s\n", i+1, token_str[tokens[i].type], tokens[i].content);
        i += 1;
    }
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
    if (argc < 2) {
        printf("[ERROR] Usage : tokenizer.exe filename\n");
        return 1;
    }
    printf("[INFO] opening(%s)\n", argv[1]);
    
    //-----------------------------------------------------
    // Get size of the file
    //-----------------------------------------------------
    FILE * f = fopen(argv[1], "rb");
    fseek(f, 0, SEEK_END);
    long size = ftell(f);
    if (size == -1) {
        printf("[ERROR] Unable to read size of the file %s\n", argv[1]);
    }
    printf("[INFO] Size of the file is : %i\n", size);
    fclose(f);
    
    //-----------------------------------------------------
    // Create a buffer for the entire file and fill it
    //-----------------------------------------------------
    char * source = (char *) calloc(size+1, sizeof(char));
    f = fopen(argv[1], "rb");
    if (f == NULL) {
        fprintf(stderr, "[ERROR] %s : %s\n", argv[1], strerror(errno));
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
    
    //-----------------------------------------------------
    // Tests
    //-----------------------------------------------------
    
    // Simple integer
    char * test1 = "123456";
    memset(tokens, MAX_TOKENS, sizeof(Token));
    tokens_cpt = 0;
    tokenize(test1, 6, tokens, &tokens_cpt);
    display_tokens(tokens, tokens_cpt);
    assert ( tokens_cpt == 1);
    assert ( tokens[0].type == INTEGER);
    
    // Two integers
    char * test2 = "123456 294857";
    memset(tokens, MAX_TOKENS, sizeof(Token));
    tokens_cpt = 0;
    tokenize(test2, 13, tokens, &tokens_cpt);
    display_tokens(tokens, tokens_cpt);
    assert ( tokens_cpt == 2);
    assert ( tokens[0].type == INTEGER);
    assert ( tokens[1].type == INTEGER);
    assert ( strcmp(tokens[0].content, "123456") == 0);
    assert ( strcmp(tokens[1].content, "294857") == 0);
    
    // A float
    char * test3 = "1.34";
    memset(tokens, MAX_TOKENS, sizeof(Token));
    tokens_cpt = 0;
    tokenize(test3, 4, tokens, &tokens_cpt);
    display_tokens(tokens, tokens_cpt);
    assert ( tokens_cpt == 1);
    assert ( tokens[0].type == FLOAT);
    assert ( strcmp(tokens[0].content, "1.34") == 0);

    // An identifier
    char * test4 = "hello";
    memset(tokens, MAX_TOKENS, sizeof(Token));
    tokens_cpt = 0;
    tokenize(test4, 5, tokens, &tokens_cpt);
    display_tokens(tokens, tokens_cpt);
    assert ( tokens_cpt == 1);
    assert ( tokens[0].type == IDENTIFIER);
    assert ( strcmp(tokens[0].content, "hello") == 0);

    // A keyword
    char * test5 = "then";
    memset(tokens, MAX_TOKENS, sizeof(Token));
    tokens_cpt = 0;
    tokenize(test5, 4, tokens, &tokens_cpt);
    display_tokens(tokens, tokens_cpt);
    assert ( tokens_cpt == 1);
    assert ( tokens[0].type == KEYWORD);
    assert ( strcmp(tokens[0].content, "then") == 0);

    // An identifier starting by '_'
    char * test6 = "_then";
    memset(tokens, MAX_TOKENS, sizeof(Token));
    tokens_cpt = 0;
    tokenize(test6, 5, tokens, &tokens_cpt);
    display_tokens(tokens, tokens_cpt);
    assert ( tokens_cpt == 1);
    assert ( tokens[0].type == IDENTIFIER);
    assert ( strcmp(tokens[0].content, "_then") == 0);

    return 0;
    //exit(EXIT_SUCCESS);
    
}
