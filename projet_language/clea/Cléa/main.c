#include <stdio.h>
#include <ctype.h>

int main(int argc, char *argv[]) {
    char var1 = 'd';
    if isalpha(var1) {
        printf("Is alpha! : %c\n", var1);
    }
    char var2 = '5';
    if isdigit(var2) {
        printf("Is digit! : %c\n", var2);
    }
    char var3 = '\t';
    if isspace(var3) {
        printf("Is space!\n");
    }
}
