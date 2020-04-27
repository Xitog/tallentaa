#include <stdio.h>
#include <stdlib.h>

int main(int argc, char * argv[]) {
    FILE * f = fopen("test.ash", "r");
    char * dest = calloc(200, sizeof(char));
    fread(dest, 100, 100, f);
    printf("%s\n", dest);
    fclose(f);
    return 0;
}
