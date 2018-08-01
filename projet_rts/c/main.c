#include <stdio.h>
#include <stdlib.h>

int main (int argc, char * argv[]) {
    
    int size = 0;
    char name[256];

    FILE * file = fopen("map.txt", "r");
    fscanf(file, "%s", name);
    for (int i = 0; i < 256; i++) {
        if (name[i] == '_') {
            name[i] = ' ';
        }
    }

    printf("Name = %s\n", name);

    fscanf(file, "%d", &size);
    printf("Size = %d\n", size);

    int ** lines = (int **) malloc(sizeof(int *) * size);
    for (int i = 0; i < size; i++) {
        lines[i] = (int *) malloc(sizeof(int) * size);
    }

    for (int row = 0; row < size; row++) {
        for (int col = 0; col < size; col++) {
            fscanf(file, "%d", &lines[row][col]);
        }
    }
    
    fclose(file);

    for (int row = 0; row < size; row++) {
        for (int col = 0; col < size; col++) {
            printf("%d ", lines[row][col]);
        }
        printf("\n");
    }

    return 0;
}
