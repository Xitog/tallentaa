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
    FLOAT_LITTERAL,
    STRING_LITTERAL,
    IDENTIFIER_LITTERAL,
    ARRAY_LITTERAL,
    TABLE_LITTERAL,
    CONDITION,
    REPETITION,
    AFFECTATION,
    FUNCTION,
    CLASSE,
    FIELD,
    KEYVALUE,
    PARAMETER,
    NODEERROR,
} NodeType;

// Type to strings
extern char * node_str[];

typedef struct Node {
    // TODO
    NodeType type;
    Token * content;
    struct Node * left;
    struct Node * right;
    struct Node * root;
} Node;

Node * node_create(Node * root, NodeType type, Token * content);
bool is_leaf(Node * n);
void node_set_left(Node * root, Node * left);
void node_set_right(Node * root, Node * right);
NodeType token_type_to_node_type(Token token);

/*
typedef struct {
    Node * left;
    Node * right;
} AST;
*/

//-----------------------------------------------------------------------------
// Prototypes
//-----------------------------------------------------------------------------

Node * parse(Token * tokens, int tokens_cpt);
void display_ast(Node * ast);
void tests_parser(void);

#endif
