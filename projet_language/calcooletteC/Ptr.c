#include "Ptr.h"

void string_copy(char ** dest, char * from)
{
	unsigned int total_length = strlen(from) + 1;
	*dest = (char *) malloc(sizeof(char) * total_length);
	memcpy(*dest, from, total_length);
}

void clone(void ** dest, void * src, int size)
{
    *dest = malloc(size);
    memcpy(*dest, src, size);
}

// GEN
char * substr(int start, int end, char * from)
{
	int length = end - start + 1; // +1 pour comptage
    char * str = (char *) malloc(length+1); // +1 car on mettra nous-même le \0
    strncpy(str, from+start, length);
    str[length] = '\0'; // Ne pas oublier !!!
    return str;
}

bool eq(Object * o1, Object * o2)
{
	if (o1->class == o2->class)
	{
		return (memcmp(o1, o2, o1->class->size)==0);
	}
	return false;
}

Class * Class_create(char * name, unsigned size)
{
	Class * cls = (Class *) malloc(sizeof(Class));
	string_copy(&cls->name, "Token");
	cls->size = size;
	return cls;
}

bool is_a(Object * o, Class * c)
{
	return (o->class == c);
}

long atom_to_i(Atom * a)
{
	//long i = *((long *)(a->value));
	long * i = (long *) malloc(sizeof(long));
	//printf("====> %p\n", a->value);
	memcpy(i, a->value, sizeof(long));
    int ri = *i;
    free(i);
	return ri;
}

bool atom_to_b(Atom * a)
{
    bool * b = (bool *) malloc(sizeof(bool));
    memcpy(b, a->value, sizeof(bool));
    bool rb = *b;
    free(b);
    return rb;
}

Atom * c_int(long i)
{
	Atom * a = (Atom *) malloc(sizeof(Atom));
	a->class = Integer;
	a->value = malloc(sizeof(long));
	memcpy(a->value, &i, sizeof(long));
	return a;
}

Atom * c_flt(double d)
{
	Atom * a = (Atom *) malloc(sizeof(Atom));
	a->class = Float;
	a->value = malloc(sizeof(double));
	memcpy(a->value, &d, sizeof(double));
	return a;
}

Atom * c_bool(bool b)
{
	Atom * a = (Atom *) malloc(sizeof(Atom));
	a->class = Boolean;
	a->value = malloc(sizeof(bool));
	memcpy(a->value, &b, sizeof(bool));
	return a;
}

Atom * c_string(char * c)
{
	Atom * a = (Atom *) malloc(sizeof(Atom));
	a->class = String;
	string_copy((char **)&a->value, c);
	return a;
}

/*

void details(char * c)
{
    printf(">>> Details on %s (%d)\n", c, sizeof(c));
    for (int i = 0; i < strlen(c); i++)
        printf(">>> %2d : %c (%d)\n", i, c[i], (int)c[i]);
}

bool eq(Ptr p1, Ptr p2)
{
    if (p1.code != p2.code || p1.size != p2.size)
    {
        //printf("CODE %d != CODE %d or SIZE %d != SIZE %d\n", p1.code, p2.code, p1.size, p2.size);
        return false;
    }
    else
        //printf("VAL = %d VAL = %d\n", *((int *)p1.thing), *((int *)p2.thing));
        return (memcmp(p1.thing, p2.thing, p1.size) == 0);
}

Ptr ref(void * thing, int size, int code)
{
    Ptr p;
    p.code = code;
    p.thing = malloc(size);
    p.size = size;
    memcpy(p.thing, thing, size);
    return p;
}

Token * retrieve_token(Ptr p)
{
    if (p.code != CTOKEN)
        return NULL;
    return (Token *) p.thing;
}

// TYPE = Organisation + Taille !!!
void testPtr()
{
    int i = 5;
    int j = 5;
    char c = 'a';
    
    Ptr ptr_i = ref(&i, sizeof(int), CINT);
    Ptr ptr_j = ref(&j, sizeof(int), CINT);
    Ptr ptr_c = ref(&c, sizeof(char), CCHAR);
    
    if (eq(ptr_i, ptr_j))
    {
        printf("hello!\n");
    }
    else
        printf("failed\n");
    
    
}

*/

void pipo(int i)
{
}

