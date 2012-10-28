#ifndef _STACK_H
#define _STACK_H

#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

struct _StackCell {
    void * data;
    struct _StackCell * next;
};
typedef struct _StackCell StackCell;

//typedef struct {
//    void * data;
//    StackCell * next;
//} StackCell;

typedef struct {
    StackCell * head;
    int size;
} Stack;

int stack_size(Stack * s);

void push(Stack * s, void * elem, int size);

void print_int(Stack * s);

void test_stack() ;

#endif
