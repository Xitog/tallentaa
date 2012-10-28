#ifndef _PTR_H
#define _PTR_H

#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

void string_copy(char ** dest, char * from);
void clone(void ** dest, void * src, int size);
char * substr(int start, int end, char * from);

struct _Class
{
	char * name;
	unsigned int size;
};
typedef struct _Class Class;

struct _Object
{
	Class * class;
};
typedef struct _Object Object;

typedef struct {
	Class * class;
	void * value;
} Atom;

// Class declarations
// For Lexer
Class * TOKEN;
Class * NODE;
// For Parser
Class * Integer;
Class * Float;
Class * Boolean;
Class * String;
Class * Symbol;
Class * Id;

// Class Class
Class * 	Class_create	(char * name, unsigned size);

// Class Object
bool 		eq				(Object * o1, Object * o2);
bool 		is_a			(Object * o, Class * c);

// Class Atom < Object
long 		atom_to_i		(Atom * a);
bool        atom_to_b       (Atom * a);

Atom * c_int(long l);
Atom * c_flt(double d);
Atom * c_bool(bool d);
Atom * c_string(char * c);

#endif
