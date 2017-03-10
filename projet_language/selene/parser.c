#include "parser.h"

const int MAX_STACK = 128;

typedef struct {
    int * token;
    int * priority;
    int head;
} Stack;

Stack * stack_create(void) {
    Stack * s = (Stack *) calloc(1, sizeof(Stack));
    s->token = (int *) calloc(MAX_STACK, sizeof(int));
    s->priority = (int *) calloc(MAX_STACK, sizeof(int));
    s->head = 0;
    return s;
}

void stack_add(Stack * s, int token, int priority) {
    s->token[s->head] = token;
    s->priority[s->head] = priority;
    (s->head)++;
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

void stack_print_at(Stack * s, Token * tokens, int i) {
    printf("%i. %s : prio = %i\n", s->token[i], tokens[s->token[i]].content, s->priority[i]);
}

void stack_print(Stack * s, Token * tokens) {
    for(int i = 0; i < s->head; i++) {
        stack_print_at(s,  tokens, i);
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

void parse(Token * tokens, int tokens_cpt, AST * ast) {
    printf("\n\nParsing %i tokens\n", tokens_cpt);
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
    stack_print(s, tokens);
    // On sélectionne la plus forte
    printf("Max : ");
    int token_max = stack_max(s);
    stack_print_at(s, tokens, token_max);
}

void display_ast(AST * tokens) {
    // TODO
}
