#include <stdlib.h>
#include <stdio.h>

#define NONE 0

struct _Cell {
	struct _Cell * next;
	void * value;
	short type;
};

typedef struct _Cell Cell;

Cell * list_create(void);

void go(void);
