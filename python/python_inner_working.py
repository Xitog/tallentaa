# ‎created: lundi ‎24 ‎juillet ‎2017, ‏‎15:41:08
# just a start

import parser
import symbol
import token

# st = parser.expr('a + 5')
st = parser.expr('5')

def display(level, node):
    if node.__class__ == tuple:
        #print('tuple')
        for i in range(0, len(node)):
            display(level+1, node[i])
    else:
        if node in symbol.sym_name:
            print("    " + " " * level + symbol.sym_name[node])
        elif node in token.tok_name:
            print("    " + " " * level + token.tok_name[node])
        else:
            print("    " + " " * level + str(node))

display(0, st.totuple())
