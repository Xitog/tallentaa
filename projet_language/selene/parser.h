#ifndef PARSER_LIB
#define PARSER_LIB

//-----------------------------------------------------------------------------
// Libraries
//-----------------------------------------------------------------------------

#include "lexer.h"

//-----------------------------------------------------------------------------
// Constants
//-----------------------------------------------------------------------------

//-----------------------------------------------------------------------------
// Types
//-----------------------------------------------------------------------------

typedef enum {
    BINARY_OPERATION,
    INTEGER_LITTERAL,
    REAL_LITTERAL,
} NodeType;

typedef struct Node {
    // TODO
    NodeType type;
    Token * content;
    struct Node * left;
    struct Node * right;
    struct Node * root;
} Node;

Node * node_create(Node * root, Token * content);
bool is_leaf(Node * n);

/*
typedef struct {
    Node * left;
    Node * right;
} AST;
*/

//-----------------------------------------------------------------------------
// Prototypes
//-----------------------------------------------------------------------------

void parse(Token * tokens, int tokens_cpt, Node * ast);
void display_ast(Node * ast);

#endif
