#include "parser.h"

char * node_str[] = {
    "Binary",
    "Integer",
    "Float",
};

Node * node_create(Node * root, NodeType type, Token * content) {
    Node * n = (Node *) calloc(1, sizeof(Node));
    n->root = root;
    n->type = type;
    n->content = content;
    n->left = NULL;
    n->right = NULL;
    return n;
}

bool is_leaf(Node * n) {
    return (n->left == NULL && n->right == NULL);
}

void node_set_left(Node * root, Node * left) {
    assert(root->left == NULL);
    root->left = left;
}

void node_set_right(Node * root, Node * right) {
    assert(root->right == NULL);
    root->right = right;
}

void node_print_lvl(Node * root, int lvl) {
    for (int i = 0; i < lvl; i++) {
        printf("    ");
    }
    printf("%s : %s\n", root->content->content, node_str[root->type]);
    if (root->left != NULL) {
        node_print_lvl(root->left, lvl+1);
    }
    if (root->right != NULL) {
        node_print_lvl(root->right, lvl+1);
    }
}

void node_print(Node * root) {
    node_print_lvl(root, 1);
}

NodeType token_to_node_type(Token * token) {
    if (token->type == INTEGER) {
        return INTEGER_LITTERAL;
    } else if (token->type == FLOAT) {
        return FLOAT_LITTERAL;
    } else if (token->type == OPERATOR) {
        if (strcmp(token->content, "*") == 0) {
            return BINARY_OPERATION;
        }
    } else if (token->type == SEPARATOR) {
        return 0;
    } else if (token->type == STRING) {
        return 0;
    } else {
        return 0;
    }
    return 0;
}

//-----------------------------------------------------------------------------

typedef struct TokenWithPriority {
    Token * token;
    int priority;
    Node * node;
} TokenWithPriority;

typedef struct TokenListElement {
    struct TokenListElement * previous;
    struct TokenListElement * next;
    TokenWithPriority * content;
} TokenListElement;

typedef struct TokenList {
    struct TokenListElement * first;
    struct TokenListElement * last;
    int count;
} TokenList;

typedef struct Iter {
    TokenList * tl;
    TokenListElement * tle;
} Iter;

Iter * iter_create(TokenList * tl) {
    Iter * iter = (Iter *) calloc(1, sizeof(Iter));
    iter->tl = tl;
    iter->tle = tl->first;
    return iter;
}

TokenWithPriority * iter_next(Iter * iter) {
    if (iter->tle != NULL) {
        TokenWithPriority * t = iter->tle->content;
        iter->tle = iter->tle->next;
        return t;
    }
    return NULL;
}

TokenList * tokenlist_create(void) {
    TokenList * tl = (TokenList *) calloc(1, sizeof(TokenList));
    tl->first = NULL;
    tl->last = NULL;
    tl->count = 0;
    return tl;
}

TokenListElement * tokenlist_max(TokenList * tl) {
    TokenListElement * tle = tl->first;
    int max = 0;
    TokenListElement * tle_max = NULL;
    while (tle != NULL) {
        if (tle->content->priority > max && tle->content->node == NULL) {
            max = tle->content->priority;
            tle_max = tle;
        }
        tle = tle->next;
    }
    return tle_max;
}

void tokenlist_add(TokenList * tl, Token * t, int priority) {
    //printf("Adding : %s at %i for prio %i\n", t->content, tl->count, priority);
    // New Element
    TokenListElement * tle = (TokenListElement *) calloc(1, sizeof(TokenListElement *));
    tle->previous = tl->last;
    tle->next = NULL;
    // Create TokenWithPriority
    tle->content = (TokenWithPriority *) calloc(1, sizeof(TokenWithPriority *));
    tle->content->token = t;
    tle->content->priority = priority;
    tle->content->node = NULL;
    // Old last element point now to the new in next
    if (tl->last != NULL) {
        tl->last->next = tle;
    } else { // it was an empty list
        tl->first = tle;
    }
    // Last element of the list point to the new
    tl->last = tle;
    // Count
    tl->count++;
}

//-----------------------------------------------------------------------------

int priority(char * operator) {
    if (strcmp(operator, "+") == 0) {
        return 12;
    } else if (strcmp(operator, "*") == 0) {
        return 13;
    }
    assert(false);
}

Node * parse(Token * tokens, int tokens_cpt) {
    printf("Parsing %i tokens\n\n", tokens_cpt);
    // Dans cette nouvelle liste :
    // - on supprime les "(" et les ")" qui influent juste sur lemode
    // - on stocke TOUS les tokens
    // - on stocke les tokens AVEC une priorité
    // - on stocke les tokens AVEC le noeud auxquels ils appartiennent
    TokenList * tl = tokenlist_create();
    int mode = 1;
    for(int i = 0; i < tokens_cpt; i++) {
        if (tokens[i].type == INTEGER) {
            tokenlist_add(tl, &tokens[i], 0); 
        } else if (tokens[i].type == OPERATOR) {
            //printf("adding token : [%s, prio=%i mode=%i]\n", tokens[i].content, priority(tokens[i].content), mode);
            tokenlist_add(tl, &tokens[i], priority(tokens[i].content) * mode); 
        } else if (tokens[i].type == SEPARATOR) {
            if (strcmp(tokens[i].content, "(") == 0) {
                //printf("( found! old mode = %i new mode = %i\n", mode, mode * 100);
                mode = mode * 100;
            } else if (strcmp(tokens[i].content, ")") == 0) {
                //printf(") found! old mode = %i new mode = %i\n", mode, mode / 100);
                mode = mode / 100;
            } else if (strcmp(tokens[i].content, "\n") == 0) {
                // What do we do with the \n ?
            } else {
                printf("token=%s\n", tokens[i].content);
                assert(false);
            }
        } else {
            assert(false);
        }
    }
    // Display
    Iter * iter = iter_create(tl);
    TokenWithPriority * twp = iter_next(iter);
    int i = 0;
    while (twp != NULL) {
        printf("  %i. content = %s type = %s priority = %i\n", i, twp->token->content, token_str[twp->token->type], twp->priority);
        i++;
        twp = iter_next(iter);
    }
    // Resolution the priorities
    printf("\n");
    TokenListElement * tle = tokenlist_max(tl);
    Node * node = NULL;
    while (tle != NULL) {
        twp = tle->content;
        printf("  Dealing with max = %s priority %i\n", twp->token->content, twp->priority);
        Node * left = NULL;
        Node * right = NULL;
        NodeType type = token_to_node_type(twp->token);
        if (type == BINARY_OPERATION) {
            node = node_create(NULL, type, twp->token);
            twp->node = node;
            if (tle->previous != NULL) {
                if (tle->previous->content->node != NULL) {
                    printf("    Adding node to the left!\n");
                    node_set_left(node, tle->previous->content->node);
                } else {
                    printf("    Adding NEW node to the left!\n");
                    left = node_create(node, token_to_node_type(tle->previous->content->token), tle->previous->content->token);
                    node_set_left(node, left);
                    tle->previous->content->node = node;
                }
            }
            if (tle->next != NULL) {
                if (tle->next->content->node != NULL) {
                    printf("    Adding node to the right!\n");
                    node_set_right(node, tle->next->content->node);
                } else {
                    printf("    Adding NEW node to the right!\n");
                    right = node_create(node, token_to_node_type(tle->next->content->token), tle->next->content->token);
                    node_set_right(node, right);
                    tle->previous->content->node = node;
                }
            }
        }
        tle = tokenlist_max(tl);
    }

    //printf("Operators detected in stack:\n");
    //printf("Ordered operators: \n");

    return node;
}

void display_ast(Node * ast) {
    printf("\n  AST :\n");
    node_print(ast);
}

void tests_parser(void) {

    /*
    // A simple Hello World
    char * test1 = "writeln(\"Hello world!\")";
    printf("\nTest 1 : %s\n", test1);
    memset(tokens, MAX_TOKENS, sizeof(Token));
    tokens_cpt = 0;
    tokenize(test1, strlen(test1), tokens, &tokens_cpt);
    display_tokens(tokens, tokens_cpt);
    */

    printf("\n====== START OF PARSER TESTS ======\n");

    // Here should be test of the parser only (checking each member of the AST produced).

    printf("\n====== END OF PARSER TESTS ======\n");
    
}
