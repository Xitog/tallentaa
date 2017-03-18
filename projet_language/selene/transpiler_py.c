#include "transpiler_py.h"

void write_node(FILE * f, Node * ast) {
    if (ast->type == BINARY_OPERATION) {
        write_node(f, ast->left);
        fprintf(f, " %s ", ast->content->content);
        write_node(f, ast->right);
        //fprintf(f, "\n");
    } else if (ast->type == INTEGER_LITTERAL) {
        fprintf(f, "%s", ast->content->content);
    } else {
        assert(false);
    }
}

void transpile_py(char * filename, Node * ast) {
    FILE * f = fopen(filename, "w");
    // Special
    fprintf(f, "print(");
    write_node(f, ast);
    fprintf(f, ")\n");
    fclose(f);
    printf("\n  Transpiling to %s finished.\n\n", filename);
}

void tests_transpiler_py(void) {

    Token tokens[MAX_TOKENS];
    int tokens_cpt = 0;
    Node * ast;

    printf("\n====== START OF TRANSPY TESTS ======\n");

    printf("\n=== Test 1 ===\n");
    tokens_cpt = test_expression1(tokens);
    ast = parse(tokens, tokens_cpt);
    display_ast(ast);
    transpile_py("test1.py", ast);
    system("python.bat test1.py");

    printf("\n====== END OF TRANSPY TESTS ======\n");

}
