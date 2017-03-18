#include "lexer.h"
#include "parser.h"
#include "transpiler_py.h"

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
    printf("\n====== START OF SELENE ======\n\n");
    //printf("Parser v0.1\n");

    tests_lexer();
    tests_parser();
    tests_transpiler_py();

    printf("\n====== END OF SELENE ======\n\n");
}

#endif
