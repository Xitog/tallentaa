
#-------------------------------------------------------------------------------
# Import
#-------------------------------------------------------------------------------

import sys

#-------------------------------------------------------------------------------
# Logging
#-------------------------------------------------------------------------------

try:
    out = sys.stdout.shell
    IDLE = True
except AttributeError:
    out = sys.stdout
    IDLE = False

def success(*msg, sep=' '):
    msg = sep.join(msg)
    if IDLE:
        out.write('[SUCCESS] ' + msg + '\n', 'STRING')
    else:
        out.write(msg + '\n')

def fail(*msg, sep=' '):
    msg = sep.join(msg)
    if IDLE:
        out.write('[FAIL] ' + msg + '\n', 'COMMENT')
    else:
        out.write(msg + '\n')

def info(*msg, sep=' '):
    msg = sep.join(msg)
    if IDLE:
        out.write('[INFO] ' + msg + '\n', 'DEFINITION')
    else:
        out.write(msg + '\n')

def warn(*msg, sep=' '):
    msg = sep.join(msg)
    if IDLE:
        out.write('[WARN] ' + msg + '\n', 'KEYWORD')
    else:
        out.write(msg + '\n')

def error(*msg, sep=' '):
    msg = sep.join(msg)
    if IDLE:
        out.write('[ERROR] ' + msg + '\n', 'COMMENT')
    else:
        out.write(msg + '\n')
