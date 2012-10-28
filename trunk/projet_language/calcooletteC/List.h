#ifndef _LIST_H
#define _LIST_H

#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

struct _cell {
    void * data;
    struct _cell * next;
    struct _cell * prev;
};
typedef struct _cell Cell;

struct _list {
    Cell * head;
    Cell * back;
    int size;
};
typedef struct _list List;

List *		List_create		();
void 		List_add		(List * list, void * elem, int size);
void 		List_remove		(List * list, int index);
void 		List_replace	(List * list, int index, void * elem, int size);
int 		List_count		(List * list);
bool 		List_empty		(List * list);
void * 		List_get		(List * list, int index);
void 		List_test		();

#endif
