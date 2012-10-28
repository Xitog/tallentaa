#include <stdlib.h>     // EXIT_SUCCESS
#include <string.h>     // str...
#include <stdio.h>      // printf
#include <ctype.h>      // isalpha
#include <stdbool.h>    // boolean
#include <math.h>       // pow              http://www.cplusplus.com/reference/clibrary/cmath/pow/

#include "List.h"
#include "Stack.h"
#include "Ptr.h"
#include "TokenType.h"
#include "Token.h"
#include "Lexer.h"
#include "Parser.h"

// a = 97 z = 122 A = 65 Z = 90

/*
 * Checklist for basic types
 * Declare it in (Ptr.c)
 * Object_init
 * c_xxx (Ptr.c)
 * atom_to_x (Ptr.c)
 * make_xxx (Parser.c)
 * remplacement du token correspondant (littéral) par sa valeur dans parse (Parser.c)
 * exec_node (easy.c)
 *
 */

void Object_init()
{
	TOKEN = Class_create("Token", sizeof(Token));
	NODE = Class_create("Node", sizeof(Node));
	
	Integer = Class_create("Integer", sizeof(long));
	Float = Class_create("Float", sizeof(double));
	Boolean = Class_create("Boolean", sizeof(bool));
	String = Class_create("String", sizeof(char *));
	Symbol = Class_create("Symbol", sizeof(char *));
	Id = Class_create("Id", sizeof(char *));
}

//-----------------------------------------------------------------------------
// Interpreter
//-----------------------------------------------------------------------------

Object * exec_node(Object * obj)
{
	if (is_a(obj, Integer))
	{
		return obj;
	}
    else if (is_a(obj, Boolean))
    {
        return obj;
    }
	else if (is_a(obj, NODE))
	{
		printf("It's a node\n");
		Node * node = (Node *) obj;
		Token * par = (Token *) node->par;
        printf("|-- %s\n", obj->class->name);
		if (isArithmeticOperator(&par->type))
		{
            printf("It's an arithmetic op!\n");
			Object * self = exec_node(node->sbg);
			printf("self OK\n");
			Object * operand = exec_node(node->sbd);
			printf("operand OK\n");
			if (is_a(self, Integer))
			{
				printf("It's self=integer!\n");
				Atom * a_self = (Atom *) self;
				Atom * a_operand = (Atom *) operand;
				Atom * r = (Atom *) malloc(sizeof(Atom));
				r->class = Integer;
				r->value = malloc(sizeof(long *));
				long rr = -1;
				if (TokenType_eq(&par->type, &ADD))
					rr = atom_to_i(a_self) + atom_to_i(a_operand);
				else if (TokenType_eq(&par->type, &MUL))
					rr = atom_to_i(a_self) * atom_to_i(a_operand);
                else if (TokenType_eq(&par->type, &INTDIV))
                    rr = atom_to_i(a_self) / atom_to_i(a_operand);
                else if (TokenType_eq(&par->type, &SUB))
                    rr = atom_to_i(a_self) - atom_to_i(a_operand);
                else if (TokenType_eq(&par->type, &MOD))
                    rr = atom_to_i(a_self) % atom_to_i(a_operand);
                else if (TokenType_eq(&par->type, &POW))
                    rr = (long) pow(atom_to_i(a_self),atom_to_i(a_operand));
				memcpy(r->value, &rr, sizeof(long));
				printf("%p\n", r->value);
				return (Object *) r;
			}
        }
        else if (isBooleanOperator(&par->type))
        {
            printf("It's an boolean op!\n");
            Object * self = exec_node(node->sbg);
			printf("self OK\n");
			Object * operand = exec_node(node->sbd);
			printf("operand OK\n");
            if (is_a(self, Boolean))
            {
                printf("It's self=boolean!\n");
                Atom * a_self = (Atom *) self;
				Atom * a_operand = (Atom *) operand;
				Atom * r = (Atom *) malloc(sizeof(Atom));
				r->class = Boolean;
				r->value = malloc(sizeof(bool *));
                bool rr = false;
                if (TokenType_eq(&par->type, &AND))
                    rr = atom_to_b(a_self) && atom_to_b(a_operand);
                else if (TokenType_eq(&par->type, &OR))
                    rr = atom_to_b(a_self) || atom_to_b(a_operand);
                else if (TokenType_eq(&par->type, &XOR))
                    rr = (atom_to_b(a_self) || atom_to_b(a_operand)) && (!atom_to_b(a_self) || !atom_to_b(a_operand));
                memcpy(r->value, &rr, sizeof(bool));
                printf("%p\n", r->value);
                return (Object *) r;
            }
		}
	}
	else
	{
		printf("ERROR! corrupted list\n");
		exit(-1);
	}
}

// POLYMORPHISME Required
// 21h20
int main(int argc, char * argv[])
{
	Object_init();
	TokenType_init();
	
	// Lexer
    //char * cmd = "alpha + beta * 2 AZ3***aa>=<=b<=>%if ()[]{}.;: \" sweet homme \" true nil //=//****=<<>> \"o'reilly\" '\"' \n # aaaa + bbbb";
    printf("\n---[Lexing... \n");
    
	//char * cmd = "2 + 2 * 3";
    //char * cmd = "2 * 4 // 2 ** 2";
    //char * cmd = "true";
    //char * cmd = "true and false";
    //char * cmd = "true or false";
    //char * cmd = "true xor false";
    //char * cmd = "true xor true";
    char * cmd = "false xor false";
    
	List * tokens = lex(cmd);
	List_print_tokens(tokens);
    
	// Parser
	printf("\n---[Parsing... \n");
	Object * ast = parse(tokens);
	
	// Interpreter
	printf("\n---[Executing... \n");
	Object * o = exec_node(ast);
	if (is_a(o, Integer))
	{
		printf("Youpi!\n");
		long rr = atom_to_i((Atom *)o);
		printf(">>> %d <<<\n", rr);
	}
    else if (is_a(o, Boolean))
    {
        printf("Youpi too!\n");
        bool rr = atom_to_b((Atom *)o);
        if (rr)
            printf(">>> true <<<\n");
        else
            printf(">>> false <<<\n");
    }
    
    return EXIT_SUCCESS;
}

// 23h30 : PARSER EN C.

// 22h54 : IL FAIT LA PRIORITE ET GERE ADD ET MUL