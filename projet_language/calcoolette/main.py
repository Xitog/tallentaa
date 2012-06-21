import console
import interpreter
import sys              # version_info
import traceback

core_exec = interpreter.Interpreter()

def todo(console, text):
    global core_exec
    try:
        r = core_exec.do_string(text)
        print r
        #self.interpreter.scope['_'] = r
        console.write(str(r), "fg_blue")    
    except Exception as e:
        console.write("See console for error.", "fg_red")
        print e
        

if __name__ != "__main__":
    raise Exception("Must be launched as principal program")
else:
    core = console.Console(todo)
    ver = sys.version_info
    core.write('+- Welcome to Pypo 0.1 on Python %i.%i' % (ver[0], ver[1]))
    core.write('+- Enter code or type help for more information.')
        
    core.main()

    print '+- Goodbye!'

"""
if console:
    while command != 'exit':
        command = raw_input('>>> ') # +->
        while not clos(command):
            command += '\n' + raw_input('... ')
        if not(command in commands) and not(command.split(' ')[0] in commands):
            #try:
                r = interpreter.do_string(command, stack, scope)
                print r
                scope['_'] = r
            #except Exception as e:
            #    print e
            #finally:
                previous = command
        elif command in commands:
            commands[command]()
        elif command.split(' ')[0] in commands:
            commands[command.split(' ')[0]](*command.split(' '))
"""

