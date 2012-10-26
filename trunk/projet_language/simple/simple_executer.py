from simple_parser import *

# Simple BIB

def send_to_int(value, message):
    if message == 'abs':
        return abs(value)
    else:
        raise Exception('FUNCTION NOT UNDERSTOOD %s' % (message,))

def send_to_flt(value, message):
    if message == 'abs':
        return abs(value)
    else:
        raise Exception('FUNCTION NOT UNDERSTOOD %s' % (message,))

# Simple Execute

def execute(ast):
    if ast.sbg is not None and ast.sbg.__class__ == list and ast.sbd is None and ast.typ == 'list' and ast.par == 'sta':
        r = None
        for statement in ast.sbg:
            r = execute(statement)
        return r
    if ast.typ == 'binop':
        if ast.par == '+':
            return execute(ast.sbg) + execute(ast.sbd)
        elif ast.par == '-':
            return execute(ast.sbg) - execute(ast.sbd)
        elif ast.par == '/':
            return float(execute(ast.sbg)) / execute(ast.sbd)
        elif ast.par == '//':
            return int(execute(ast.sbg)) / int(execute(ast.sbd))
        elif ast.par == '*':
            return execute(ast.sbg) * execute(ast.sbd)
        elif ast.par == '%':
            return execute(ast.sbg) % execute(ast.sbd)
        elif ast.par == '**':
            return execute(ast.sbg) ** execute(ast.sbd)
        elif ast.par == '.':
            left = execute(ast.sbg)
            if left.__class__ == int: return send_to_int(left, ast.sbd)
            elif left.__class__ == float: return send_to_flt(left, ast.sbd)
            else: raise Exception('CALL MSG TO UNSPECIFIED TYPE')
    elif ast.typ == 'unaop':
        if ast.par == '-':
            return -execute(ast.sbg)
    elif ast.typ == 'value':
        if ast.par == 'int':
            return ast.sbg
        elif ast.par == 'flt':
            return ast.sbg
        elif ast.par == 'str':
            return ast.sbg
    print ast.__class__
    print ast.sbg
    print ast.sbd
    print ast.typ
    print ast.par
    raise Exception('AST NOT UNDERSTOOD')

#-----------------------------------------------------------------------

def cmd_exit():
    pass

shell = True
commands = { 'exit' : cmd_exit}
Root = {}

def compute_string(string, scope):
    ast = get_ast(string)
    if ast is None:
        print 'ERROR : Ast could not be generated.'
    else:
        if DEBUG:
            print('Ast built')
            print('Exploring')
            explore(ast)
        return execute(ast)

if __name__ == '__main__':
    if shell:
        s = ''
        while s != 'exit':
            String = s
            s = raw_input('> ')
            if s in commands:
                commands[s]()
            else:
                s += "\n"
                if DEBUG: disp(s)
                while good(s) != 0:
                    s2 = raw_input('. ')                    
                    s += s2
                    s += "\n"
                    if DEBUG: disp(s)
                result = compute_string(s, Root)
                #Root.vars['_'] = result
                print result
    else:
        files = ('essai.pypo',)
        String = read(files[0])
        compute_string(String)
        dump()
