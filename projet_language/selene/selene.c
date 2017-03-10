#include "lexer.h"
#include "parser.h"

#ifdef TOKENIZER

int main(int argc, char * argv[]) {
    //-----------------------------------------------------
    // Test args
    //-----------------------------------------------------
    printf("Tokenizer v0.1\n");
    int i = 0;
    while (i < argc) {
        printf("[INFO] Arg %i : %s\n", i, argv[i]);
        i += 1;
    }
    if (argc == 2) {
        //printf("[ERROR] Usage : tokenizer.exe filename\n");
        //return 1;
        printf("[INFO] File : %s\n", argv[1]);
        handle_file(argv[1]);
    }
    
    tests();
    
    return 0;
    //exit(EXIT_SUCCESS);
    
}

#endif

#ifdef PARSER

int main(int argc, char * argv[]) {
    printf("Parser v0.1\n");

    Token tokens[MAX_TOKENS];
    int tokens_cpt = 0;
    
    tests();

    // A simple Hello World
    char * test1 = "writeln(\"Hello world!\")";
    printf("\nTest 1 : %s\n", test1);
    memset(tokens, MAX_TOKENS, sizeof(Token));
    tokens_cpt = 0;
    tokenize(test1, strlen(test1), tokens, &tokens_cpt);
    display_tokens(tokens, tokens_cpt);


}

#endif
