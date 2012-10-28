//-----------------------------------------------------------------------------
// Title: Parser.c
// Author: Damien Gouteux
// Creation: 1 Nov 2011
// Synopsis: The parser component. Track the most prioritary token and convert it into a Node.
//-----------------------------------------------------------------------------

#include "Parser.h"

Max Max_init()
{
    Max max;
    max.max = NULL;
    max.prio = 0;
    max.index = -1;
    return max;
}

Max get_max(List * list)
{
    Max max = Max_init();
    Cell * parcours = list->head;
    int i = 0;
    while (parcours != NULL)
    {
		Object * obj = (Object *) parcours->data;
		if (is_a(obj, TOKEN))
		{
			Token * target = (Token *) parcours->data;
			if ( target->type.priority > max.prio )
			{
				max.prio = target->type.priority;
				max.max = target;
				max.index = i;
			}
		}
		parcours = parcours -> next;
        i++;
    }
    return max;
}

// self const : pas * | de class : pas de self
Node Node_init()
{
    Node n;
    n.class = NODE;
    n.sbg = NULL;
    n.sbd = NULL;
    n.par = NULL;
    n.opt = NULL;
    return n;
}

void make_int(List * list, Max * max)
{
	Token * t = List_get(list, max->index);
	Atom * a = c_int(atoi(t->str));
	List_replace(list, max->index, a, sizeof(Atom));
}

void make_bool(List * list, Max * max)
{
	Token * t = List_get(list, max->index);
	Atom * a;
    if (TokenType_eq(&max->max->type, &TRUE))
        a = c_bool(true);
    else
        a = c_bool(false);
	List_replace(list, max->index, a, sizeof(Atom));
}

void make_binop(List * list, Max * max)
{
    int before = max->index - 1;
    int after = max->index + 1;
    
    Node n = Node_init();
    clone(&n.sbg, List_get(list, before), sizeof(Token));       // OP1
    clone(&n.sbd, List_get(list, after), sizeof(Token));        // OP2
    clone(&n.par, List_get(list, max->index), sizeof(Token));   // OPERATOR
    //printf("ENDING CLONES\n");
    
    List_replace(list, max->index, &n, sizeof(Node));
    //printf("REPLACE END\n");
    List_remove(list, max->index+1);
    //printf("REMOVE RIGHT END\n");
    List_remove(list, max->index-1);
    //printf("REMOVE LEFT END\n");
}

void List_print_tokens(List * list)
{
    Cell * parcours = list->head;
    for(int i = 0; i < list->size; i++)
    {
        Token * t = (Token *)parcours->data;
        printf("%d. Token operator (len = %d) (type = %s): [%s]\n", i, strlen(t->str), TokenType_to_s(&t->type), t->str);
        parcours = parcours -> next;
    }
}

Object * parse(List * tokens)
{
    Max max;
    if (tokens->size == 1)
    {
        max.max = (Token *) tokens->head->data;
        max.prio = (max.max->type).priority;
        max.index = 0;
        printf("str du token cible : %s\n", max.max->str);
        
        if (TokenType_eq(&max.max->type, &INT))
        {
            printf("> int\n");
            make_int(tokens, &max);
        }
        else if (TokenType_eq(&max.max->type, &TRUE) || TokenType_eq(&max.max->type, &FALSE))
        {
            printf("> bool\n");
            make_bool(tokens, &max);
        }
        else
        {
            printf("ERROR! I don't know this type: %s\n", max.max->type.name);
        }
    }
    else
    {
        while (tokens->size > 1)
        {
            // Search le token de priority max
            max = get_max(tokens);
            //printf("index : %d prio : %d\n", max.index, max.prio);
		
            // On va créer son noeud
            if (isBinaryOperator(&max.max->type))
            {
                printf("> binop\n");
                make_binop(tokens, &max);
            }
            else if (TokenType_eq(&max.max->type, &INT))
            {
                printf("> int\n");
                make_int(tokens, &max);
            }
            else if (TokenType_eq(&max.max->type, &TRUE) || TokenType_eq(&max.max->type, &FALSE))
            {
                printf("> bool\n");
                make_bool(tokens, &max);
            }
            else
            {
                printf("ERROR! I don't know this type: %s\n", max.max->type.name);
            }
            //printf("Size = %d \n", tokens->size);
        }
    }
	
	return tokens->head->data;
}
