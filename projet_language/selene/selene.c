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
    
    printf("\n====== START OF PARSER TESTS ======\n");

    printf("\n=== Test 1 ===\n");
    tokens_cpt = test_expression1(tokens);
    AST ast;
    parse(tokens, tokens_cpt, &ast);

    printf("\n=== Test 2 ===\n");
    tokens_cpt = test_expression2(tokens);
    // reset AST
    parse(tokens, tokens_cpt, &ast);
    
    printf("\n====== END OF PARSER TESTS ======\n");
    
    printf("\n====== END OF SELENE ======\n\n");

}

#endif
