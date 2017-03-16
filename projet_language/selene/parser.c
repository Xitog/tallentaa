#include "parser.h"

Node * node_create(Node * root, Token * content) {
    Node * n = (Node *) calloc(1, sizeof(Node));
    n->root = root;
    n->content = content;
    n->left = NULL;
    n->right = NULL;
    return n;
}

bool is_leaf(Node * n) {
    return (n->left == NULL && n->right == NULL);
}

const int MAX_STACK = 128;

typedef struct {
    int * token;
    int * priority;
    Node * nodes;
    int head;
} Stack;

Stack * stack_create(void) {
    Stack * s = (Stack *) calloc(1, sizeof(Stack));
    s->token = (int *) calloc(MAX_STACK, sizeof(int));
    s->priority = (int *) calloc(MAX_STACK, sizeof(int));
    s->nodes = (Node *) calloc(MAX_STACK, sizeof(Node));
    s->head = 0;
    return s;
}

void stack_add(Stack * s, int token, int priority) {
    s->token[s->head] = token;
    s->priority[s->head] = priority;
    (s->head)++;
}

int stack_size(Stack * s) {
    return s->head;
}

int stack_max(Stack * s) {
    int max = -1;
    int token = -1;
    for(int i = 0; i < s->head; i++) {
        if (s->priority[i] > max) {
            max = s->priority[i];
            token = i;
        }
    }
    assert(token != -1 && max != -1);
    return token;
}

void stack_disable(Stack * s, int i) {
    assert(i >= 0);
    assert(i < s->head);
    s->priority[i] = 0; // the token will never be picked up by the get max algorithm
}

void stack_print_at(Stack * s, Token * tokens, int i, char * level) {
    printf("%s%i. %s : prio = %i\n", level, s->token[i], tokens[s->token[i]].content, s->priority[i]);
}

void stack_print(Stack * s, Token * tokens, char * level) {
    for(int i = 0; i < s->head; i++) {
        stack_print_at(s,  tokens, i, level);
    }
}

int priority(char * operator) {
    if (strcmp(operator, "+") == 0) {
        return 12;
    } else if (strcmp(operator, "*") == 0) {
        return 13;
    }
    assert(false);
}

void parse(Token * tokens, int tokens_cpt, Node * ast) {
    printf("Parsing %i tokens\n\n", tokens_cpt);
    // on va dire qu'on a directement une expression
    // On calcule les priorités
    Stack * s = stack_create();
    for(int i = 0; i < tokens_cpt; i++) {
        //printf("%i. %s [%s]\n", i, tokens[i].content, token_str[tokens[i].type]);
        if (tokens[i].type == OPERATOR) {
            //printf("We have an operator! : %s\n", tokens[i].content);
            stack_add(s, i, priority(tokens[i].content));
        }
    }
    printf("Operators detected:\n");
    stack_print(s, tokens,  "  ");
    // Get max algorithm : On sélectionne la plus forte
    printf("Ordered operators: \n");
    for(int i = 0; i < stack_size(s); i++) {
        int token_max = stack_max(s);
        stack_print_at(s, tokens, token_max, "  ");
        stack_disable(s, token_max);
    }
    
}

void display_ast(Node * ast) {
    // TODO
}
