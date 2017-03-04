#include "tokenizer_lib.h"

#ifdef PARSER

int main(int argc, char * argv[]) {
    printf("Parser v0.1\n");

    Token tokens[MAX_TOKENS];
    int tokens_cpt = 0;

    // A simple Hello World
    char * test1 = "writeln(\"Hello world!\")";
    printf("\nTest 1 : %s\n", test1);
    memset(tokens, MAX_TOKENS, sizeof(Token));
    tokens_cpt = 0;
    tokenize(test1, strlen(test1), tokens, &tokens_cpt);
    display_tokens(tokens, tokens_cpt);
}

#endif
