#ifndef PARSER_H
#define PARSER_H

#include <stdio.h>
#include "Ptr.h"
#include "TokenType.h"
#include "Token.h"
#include "List.h"

struct _Node {
    Class * class;
    void * sbg;
    void * sbd;
    void * par;
    void * opt;
};
typedef struct _Node Node;

struct _max
{
    Token * max;
    int prio;
    int index;
};
typedef struct _max Max;

Max Max_init();
Max get_max(List * list);

Node Node_init();

void make_int(List * list, Max * max);
void make_bool(List * list, Max * max);
void make_binop(List * list, Max * max);
void List_print_tokens(List * list);

Object * parse(List * tokens);

#endif