//-----------------------------------------------------------------------------
// Libraries
//-----------------------------------------------------------------------------

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>
#include <assert.h>
#include "tokenizer_lib.h"

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
