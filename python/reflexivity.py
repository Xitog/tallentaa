# bytecode interpreter
# http://docs.python.org/library/stdtypes.html
# http://docs.python.org/library/dis.html
# http://docs.python.org/library/compiler.html

import dis
def fun_test():
    a = 255
    a = 228
    a = 255
dis.dis(fun_test)

for k in dis.opmap:
    print k, dis.opmap[k]
print

code = {
    # data
    'INTEGER' : 10,
    'FLOAT' : 11,
    'BOOLEAN' : 12,
    'CHAR' : 13,
    'STRING' : 14,
    'LIST' : 15,
    'HASH' : 16,
    #
    'SHORT' : 5,
    # op ar bin & un
    'ADD' : 20,
    'SUB' : 21,
    'INV' : 22,
    'DIV' : 23,
    'INTDIV' : 24,
    'MUL' : 25,
    'MOD' : 26,
    'POW' : 27,
    # op bool bin & un
    'AND' : 30,
    'OR' : 31,
    'XOR' : 32,
    'NOT' : 33,
    # op compare
    'LT' : 40,
    'LE' : 41,
    'GT' : 42,
    'GE' : 43,
    'EQ' : 44,
    'NQ' : 45,
    # op bit binn & un
    'BIN_AND' : 50,
    'BIN_OR' : 51,
    'BIN_XOR' : 52,
    'BIN_NOT' : 53,
    'SHIFT_LEFT' : 54,
    'SHIFT_RIGHT' : 55,
    # jumps
    'JUMP' : 60,
    'JUMP_IF_FALSE' : 61,
    'JUMP_IF_TRUE' : 62,
    # others
    'REM' : 70
}

test = [
    'SHORT 5',
    'SHORT 5',
    'ADD'
]

# convert stack to string
def convert_to_s(stack):
    r = ''
    i = 0
    for s in stack:
        r += s
        r += '\n'
    return r

# http://docs.python.org/library/io.html
# convert stack to binary
def convert_to_bin(stack):
    b = bytearray()
    for s in stack:
        l = s.split(' ')
        command = l[0]
        arg = None
        if len(l) > 1:
            arg = l[1]
        print command, arg

print(convert_to_s(test))
convert_to_binwhy LOAD_FAST argument PYTHON BYTECODE(test)

print
print '***'
print
import parser
#st = parser.expr('a + 5') # eval
st = parser.suite('a = 5') # exec
print parser.isexpr(st)
print parser.issuite(st)

code = parser.compilest(st)
dis.disassemble(code)
print dir(code)
#code = st.compile('file.py')
# http://docs.python.org/library/inspect.html
print
print 'argc : ', code.co_argcount           # number of arguments (not including * or ** args)
print 'consts : ', code.co_consts           # tuple of constants used in the bytecode
print 'names : ', code.co_names             # tuple of names of local variables
print 'nlocals : ', code.co_nlocals         # number of local variables
print 'code : ', code.co_code               # string of raw compiled bytecode
print 'var names : ', code.co_varnames      # tuple of names of arguments and local variables
print 'stack size :', code.co_stacksize     # virtual machine stack space required
print
eval(code)
print a


b = bytearray()
