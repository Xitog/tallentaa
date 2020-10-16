"""
    Ash
    ---
    A simple lexer / parser / interpreter / python transpiler for a small language inspired by Lua/Ruby
"""

#
# Imports
#

import os.path
import sys # for writing debug info
import traceback

from ashlang.ashlexer import Tokenizer
from ashlang.ashparser import Parser
from ashlang.ashtranspiler import TranspilerDirectPython
from ashlang.ashinterpreter import Interpreter

#
# Globals
#
__version__ = '0.0.1'
__py_version__ = f'{sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}'

#
# Console
#

class FallBack:
    def write(self, msg, color):
        sys.stdout.write(msg)


class Console:

    def __init__(self):
        try:
            # Works only in IDLE
            self.out = sys.stdout.shell
        except AttributeError:
            self.out = FallBack()
        self.outputs = []
    
    def error(self, msg):
        self.out.write('[ERROR] ' + str(msg) + '\n', 'COMMENT')

    def info(self, msg):
        self.out.write('[INFO]  ' + str(msg) + '\n', 'DEFINITION')
    
    def put(self, msg):
        self.outputs.append(msg)
        self.out.write(str(msg), 'TODO')

    def puts(self, msg):
        self.outputs.append(msg)
        self.out.write(str(msg) + '\n', 'TODO')


console = Console()

#
# Main
#

def read(filepath):
    f = open(filepath, mode='r', encoding='utf8')
    c = f.read()
    f.close()
    return c

def run(command, interpreter, mode='full', debug=False, output=None):
    global console
    tokenizer = Tokenizer()
    parser = Parser()
    transpiler = TranspilerDirectPython()
    console.outputs = []

    tokens = []
    ast = None
    res = None
    try:
        tokens = tokenizer.tokenize(command)
        if mode == 'tokenize': return tokens
        ast = parser.parse(tokens)
        if mode == 'transpile':
            trans = transpiler.transpile(ast)
            return trans
        res = interpreter.do_ast(ast)
        console.puts('= ' + str(res))
    except Exception as e:
        console.error(e)
        traceback.print_exc(file=sys.stdout)
    
    if debug:
        filename = output if output is not None else 'last.html'
        f = open(filename, mode='w', encoding='utf8')
        f.write('<html>\n  <body>\n')
        f.write('    <h2>Command</h2>\n      <pre>\n')
        f.write(command)
        f.write('    </pre>\n')
        f.write('    <h2>Tokens</h2>\n      <table border="1">\n')
        for i, t in enumerate(tokens):
            f.write(f'      <tr><td>{i}</td><td>{t.typ.name}</td><td>{t.val}</td></tr>\n')
        f.write('    </table>\n')
        f.write('    <h2>Abstract syntax tree</h2>\n')
        if ast is not None:
            f.write(ast.to_html())
        else:
            f.write('    <p>No AST defined.</p>\n')
        f.write('    <h2>Outputs</h2>\n      <table border="1">\n')
        for t in console.outputs:
            f.write('      <tr><td>' + str(t) + '</td></tr>\n')
        f.write('    </table>\n')
        f.write('    <h2>Result</h2>\n')
        f.write('    <h1>' + str(res) + '</h1>\n')
        f.write('  </body>\n</html>')
        f.close()
                
def main():
    debug = False
    mode = 'full'
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        f = open(filepath, mode='r')
        data = f.read()
        f.close()
        interpreter = Interpreter(console).do(data)
    else:
        interpreter = Interpreter(console)
        print(f'Ash {__version__} on Python {__py_version__}.\nType "help" for more information.')
        while True:
            command = input('ash> ')
            if command == 'exit':
                break
            elif command == 'help':
                print(f'Ash {__version__} on Python {__py_version__}. 2017-2020')
                print('help      : this help')
                print('tests     : run multiple tests')
                print('reset     : reset interpreter')
                print('debug     : set/unset debug. You can specify true or false')
                print('locals    : get local variable')
                print('exec <f>  : execute a file')
                print('trans <f> : transpile a file')
                print('full      : mode full: tokenize, parse, interpret')
                print('tokenize  : mode only produce tokens')
                print('transpile : mode only transpile to python')
                print('exit      : exit this shell')
            elif command.startswith('debug'):
                args = command.split(' ')
                if len(args) < 2:
                    debug = not debug
                else:
                    debug = True if args[1] == 'true' else False
                console.info(f'Debug set to {debug}.')
            elif command == 'locals':
                for k in sorted(interpreter.vars):
                    print(f"{k:10}", interpreter.vars[k])
            elif command.startswith('transXXX'):
                args = command.split(' ')
                args = command.split(' ')
                if len(args) < 2:
                    console.error('You must indicate a file to process.')
                else:
                    arg = args[1]
                    if not arg.endswith('.ash'):
                            arg += '.ash'
                    if not os.path.isfile(arg):
                        console.error('File ' + arg + ' does not exist')
                    else:
                        c = read(arg)
                        tokenizer = Tokenizer()
                        parser = Parser()
                        console.outputs = []
                        tokens = tokenizer.tokenize(c)
                        ast = parser.parse(tokens)
                        TranspilerPython().transpile(ast.root, 'last.py') 
            elif command.startswith('exec') or command == 'tests':
                if command == 'tests': # hack
                    command = 'exec tests'
                args = command.split(' ')
                if len(args) < 2:
                    console.error('You must indicate a file to process.')
                else:
                    arg = args[1]
                    if os.path.isdir(arg):
                        files = os.listdir(arg)
                        cpt = 0
                        max_file = 0
                        for f in files:
                            if f.endswith('.ash'):
                                max_file += 1
                        for f in files:
                            if f.endswith('.ash'):
                                cpt += 1
                                console.info(f'Executing {f} ({cpt}/{max_file})')
                                filename = os.path.join(arg, f)
                                html_output = os.path.join(arg, 'html', f)
                                c = read(filename)
                                run(c, interpreter, only_tokenize, debug, html_output[:-4] + '.html')
                    else:
                        if not arg.endswith('.ash'):
                            arg += '.ash'
                        if not os.path.isfile(arg):
                            console.error('File ' + arg + ' does not exist')
                        else:
                            c = read(arg)
                            run(c, interpreter, only_tokenize, debug)
            elif command == 'reset':
                interpreter = Interpreter()
            elif command == 'tests':
                read_tests('./tests/tests.txt')
            elif command in ['full', 'tokenize', 'transpile']:
                mode = command
                print(f'Mode set to {mode}')
            else:
                try:
                    res = run(command, interpreter, mode, debug)
                    if mode == 'tokenize':
                        print(command)
                        start_line = ''
                        for i, r in enumerate(res):
                            while len(start_line) < r.start:
                                start_line += ' '
                            si = str(i)
                            start_line += si + '_' * (r.length - len(si))
                        print(start_line)
                        for i, r in enumerate(res):
                            print(i, r)
                    elif mode == 'transpile':
                        print(res)
                except Exception as e:
                    console.error(f'Exception: {e}')
                    traceback.print_exception(*sys.exc_info())

if __name__ == '__main__':
    main()
