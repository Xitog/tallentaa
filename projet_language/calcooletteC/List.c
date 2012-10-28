#include "List.h"

List * List_create()
{
    List * l = (List *) malloc(sizeof(List));
    l->head = NULL;
    l->back = NULL;
    l->size = 0;
    return l;
}

void List_add(List * list, void * elem, int size)
{
    if (list->head == NULL)
    {
        list->head = (Cell *) malloc(sizeof(Cell));
        list->head->next = NULL;
        list->head->prev = NULL;
        //
        list->head->data = (void *) malloc(size);
        memcpy(list->head->data, elem, size);
        // list->head->data = elem;
        list->back = list->head;
    }
    else
    {
        list->back->next = (Cell *) malloc(sizeof(Cell));
        list->back->next->next = NULL;
        list->back->next->prev = list->back;
        //
        list->back->next->data = (void *) malloc(size);
        memcpy(list->back->next->data, elem, size);
        //list->back->next->data = elem;
        list->back = list->back->next;
    }
    list->size+=1;
    printf("head: %p back: %p\n", list->head, list->back);
}

void List_remove(List * list, int index)
{
    Cell * parcours = list->head;
    int i = 0;
    for(i = 0; i < list->size; i++)
    {
        if (i == index)
        {
            break;
        }
        parcours = parcours -> next;
    }
    if (i == index)
    {
        if (i != 0 && i != list->size-1)
        {
            //printf("ICI %d\n", i);
            parcours->next->prev = parcours->prev;
            parcours->prev->next = parcours->next;
            free(parcours);
            list->size-=1;
        }
        else if (i == 0)
        {
            //printf("LA\n");
            if (list->head->next == NULL)
            {
                free(list->head);
                list->head = NULL;
                list->back = NULL;
                list->size--;
            }
            else
            {
                parcours = list->head;
                list->head = list->head->next;
                list->head->prev = NULL;
                free(parcours);
                list->size--;
            }
        }
        else if (i == list->size-1) // i != 0 il y a un prev !
        {
            //printf("ENCORE\n");
            parcours = list->back;
            //printf("... %p\n", list->back->prev);
            list->back = list->back->prev;
            free(parcours);
            list->size--;
        }
    }
}

void List_replace(List * list, int index, void * elem, int size)
{
    Cell * parcours = list->head;
    int i = 0;
    for(i = 0; i < list->size && parcours != NULL; i++)
    {
        if (i == index)
            break;
        parcours = parcours -> next;
    }
    if (i == index)
    {
        free(parcours->data);
        parcours->data = malloc(size);
        memcpy(parcours->data, elem, size);
    }
}

int List_count(List * list)
{
    return (list->size);
}

bool List_empty(List * list)
{
    return (list->size == 0);
}

// Faire un List_get_cell private ?

void * List_get(List * list, int index)
{
    Cell * parcours = list->head;
    int i = 0;
    for(i = 0; i < list->size; i++)
    {
        if (i == index)
        {
            break;
        }
        parcours = parcours -> next;
    }
    if (i == index)
    {
        return parcours->data;
    }
    return NULL;
}

void List_test()
{
    int i1 = 1;
    int i2 = 2;
    int i3 = 3;
    List * list = List_create();
    List_add(list, &i1, sizeof(int));
    List_add(list, &i2, sizeof(int));
    List_add(list, &i3, sizeof(int));
    for (int i = 0; i < list->size; i++)
    {
        printf("%d : %d\n", i, *((int *)List_get(list, i)));
    }
    List_remove(list, 1);
    for (int i = 0; i < list->size; i++)
    {
        printf("%d : %d\n", i, *((int *)List_get(list, i)));
    }
}


//#ENDIF