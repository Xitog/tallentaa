#include "Stack.h"

Stack new_stack() {
    Stack s;
    s.size = 0;
    s.head = NULL;
    return s;
}

int stack_size(Stack * s) {
    return (s->size);
}

void push(Stack * s, void * elem, int size)
{
    StackCell * parcours = s->head;
    StackCell * old = NULL;
    while (parcours != NULL)
    {
        old = parcours;
        parcours = parcours->next;
    }
    if (old == NULL) // Empty
    {
        s->head = (StackCell *) malloc(sizeof(StackCell));
        s->size+=1;
        s->head->next = NULL;
        s->head->data = malloc(size);
        memcpy( s->head->data, elem, size); 
    }
    else // At least one
    {
        old->next = (StackCell *) malloc(sizeof(StackCell));
        s->size+=1;
        old->next->next = NULL;
        old->next->data = malloc(size);
        memcpy( old->next->data, elem, size);
    }
}

void print_int(Stack * s)
{
    StackCell * parcours = s->head;
    for (int i = 0; i < s->size; i++)
    {
        printf("data: %d next: %p\n", *((int *)parcours->data), parcours->next);
        parcours = parcours->next;
    }
}

void test_stack() {
    Stack s = new_stack();
    printf("%d\n", stack_size(&s));
    int a1 = 1;
    int a2 = 2;
    int a3 = 3;
    push(&s, &a1, sizeof(int));
    push(&s, &a2, sizeof(int));
    push(&s, &a3, sizeof(int));
    print_int(&s);
}