#ifndef TRANSPILER_PY
#define TRANSPILER_PY

//-----------------------------------------------------------------------------
// Libraries
//-----------------------------------------------------------------------------

#include "lexer.h"
#include "parser.h"

//-----------------------------------------------------------------------------
// Prototypes
//-----------------------------------------------------------------------------

void transpile_py(char * filename, Node * ast);
void tests_transpiler_py(void);

#endif
