import lex
import yacc
from pypo_lexer import *
from pypo_parser import *

# En deux secondes, les choses sont reprises en mains avec
# RapidSVN et Geany et Ubuntu. Great !

# 001 IF CONDITION MUST BE A BOOLEAN
# 002 VARIABLE DOESN'T EXIST
# 010 INDEX OUT OF BOUND
# 501 MALFORMED AST (class:CLASS, obj:OBJECT)

#print("s last: %s" % (s[len(s)-1],))
#s += "\n"
import sys
#
# SWITCHES
verbose = False
#verbose = True
#from_disk = False
from_disk = True


#
# Print an error
# @param int The code of the error
# @param str The message to display
# @return None
#
def error(error_code, error_msg):
    print("%d : %s" % (error_code, error_msg))
    exit()
#
# Get Ast from string
# @param str The string to parse
# @return ast The Abstract Syntax Tree
#
def get_ast(string):
    ast = yacc.parse(string) #, debug=2)
    return ast

#
# Read a file from its name
# @param str The name of the file to compute
# @return str A string representing the entire file
#
def read(filename):
    f = file(filename)
    s = f.read()
    return s

#
# Get Tokens from string
# @param str String to tokenize
# @return list<Token> List of the tokens
#
def get_tokens(string):
    tokens = lex.input(s)
    l = []
    while 1:
        token = lex.token()
        if not token: break
        l.append(token)
    return l

#
# Compute a file (Read it and send it to compute_string)
# @param str The name of the file to compute
# @return obj The computed value
#
def compute_file(filename):
    return compute_string(read(filename), debug)
#
# Compute a string
# @param str the string to compute
# @return obj The computed value
#
def compute_string(string):
    ast = get_ast(string)
    result = compute(ast)
    return result
#
# Print all vars in root scope
# @return None
#
def dump():
    print("\nListing vars : %i" % len(root.ids))
    for k in root.ids:
        print("%s:%s:%s" % (k, root.ids[k].__class__, root.ids[k]))
#
# Utiliry function to produce tab & indentation
def prod(level):
    s = ''
    for i in range(0,level):
        s+='\t'
    return s

#
# Parse AST and print it
def explore(n, level):
    if n is None:
        print "n is None"
    #print n.__class__
    #print n
    #print "n.code %s" % (n.code,)
    #print "n.parameters %s" % (n.parameters,)
    
    if level != -1:
        fs = prod(level)+n.code
    else:
        print(">>> %s" % (n,))
        fs = n.code
    if n.value is not None:
        #print "afjj"
        fs += "v{%s}" % n.value
    if n.param is not None:
        #print "kjccbb"
        fs += "p[" + explore(n.param,-1) + "]"
    if n.sbg is not None:
        #print "kfjfkjk'"
        fs += "\n"
        fs += explore(n.sbg, level+1)
    if n.sbd is not None:
        #print "bdjfdjfhj"
        fs += "\n"
        fs += explore(n.sbd, level+1)
    return fs

#
# Class Scope
class Scope(object):
    
    root = None
    
    def __init__(self, father=None):
        self.ids = {}
        if father is not None:
            if Scope.root is None:
                raise Exception("Root not created")
            else:
                self.father = father
        else:
            if Scope.root is None:
                self.father = None
                Scope.root = self
            else:
                raise Exception("Root already created")    
    
    def add(self, str, value):
        self.ids[str] = value
    
    def get_safe(self, label, type):
        #print("entre de get : %s : %s : %s" % (label,type,self.ids[label]))
        r = None
        if type is None:
            if label in self.ids: # on l'a ?
                r = self.ids[label]
            elif self.father is not None: # dans le pere ?
                r = self.father.get_safe(label, type)
            else: # on n'a pas de pere
                return None #raise Exception("Id is not known")
        else:
            if label in self.ids:
                if self.ids[label].__class__ == type:
                    r = self.ids[label]
                else:
                    raise Exception("Wrong type")
            else:
                r = self.father.get_safe(label, type)
        #print("sortie de get : %s" % str(r))
        return r
    
    def get(self, label, type=None):
        return self.get_safe(label, type)
    
    def refresh(self, str, value):
        self.add(str, value)
#
#
def isiterable(obj):
    r = False
    if getattr(obj, '__iter__', False):
        r = True
    elif isinstance(obj, basestring):
        r = True
    return r
#
# Root scope
root = Scope()
scope = root
glb_break = False
#
# Functions
glb_functions = {}

def pypo_print(parameters):
    for p in parameters:
        if p.__class__ == str: # "\\n" problem
            p = p.decode('string_escape')
        sys.stdout.write(str(p))
    return None

def pypo_println(parameters):
    for p in parameters:
        if p.__class__ == str:
            p = p.decode('string_escape')
        sys.stdout.write(str(p))
        sys.stdout.write("\n")
    return None

def pypo_range(parameters):
    if len(parameters) > 2:
        raise Exception("Too much parameters")
    else:
        r = range(parameters[0], parameters[1]+1)
        return r

#
# Parse AST and compute it
def compute(n):
    global glb_break
    if n.__class__ != Node:
        error(501, "MALFORMED AST (class:%s, obj:%s)" % (n.__class__,n))
    
    if n.code == '=':
        scope.add(n.param.value, compute(n.sbg))
        return scope.get(n.param.value)
    elif n.code == '+=':
        scope.refresh(n.param.value, scope.get(n.param.value) + compute(n.sbg))
        return scope.get(n.param.value)
    elif n.code == '-=':
        scope.refresh(n.param.value, scope.get(n.param.value) - compute(n.sbg))
        return scope.get(n.param.value)
    elif n.code == '*=':
        scope.refresh(n.param.value, scope.get(n.param.value) * compute(n.sbg))
        return scope.get(n.param.value)
    elif n.code == '/=':
        scope.refresh(n.param.value, scope.get(n.param.value) / compute(n.sbg))
        return scope.get(n.param.value)
    elif n.code == '//=':
        scope.refresh(n.param.value, scope.get(n.param.value) // compute(n.sbg))
        return scope.get(n.param.value)
    elif n.code == '%=':
        scope.refresh(n.param.value, scope.get(n.param.value) % compute(n.sbg))
        return scope.get(n.param.value)
    elif n.code == 'IF':
        r = compute(n.param)
        if r.__class__ != bool:
            error(1, 'IF CONDITION MUST BE A BOOLEAN')
        if r:
            return compute(n.sbg)
        elif n.sbd is not None:
            return compute(n.sbd)
        else:
            return None
    elif n.code == 'UNLESS':
        r = compute(n.param)
        if r.__class__ != bool:
            error(1, 'IF CONDITION MUST BE A BOOLEAN')
        if not r:
            return compute(n.sbg)
        elif n.sbd is not None:
            return compute(n.sbd)
        else:
            return None
    elif n.code == 'WHILE':
        while compute(n.param) and not glb_break:
            compute(n.sbg)
        if not glb_break: # if it's an break end, we reset it.
            glb_break = False
    elif n.code == 'FOR':
        scope.add(n.value, None)
        r = compute(n.param)
        if not isiterable(r):
            Exception("Is not iterable")
        #print ">>> ", r, " : ", r.__class__
        ### il affichait 'Node' mais ne voulait pas faire r.code car pour lui ct une liste...
        for i in r:
            scope.refresh(n.value, i)
            compute(n.sbg)
        return None
    elif n.code == 'BREAK':
            glb_break = True
            return None
    elif n.code == '+':
        return compute(n.sbg) + compute(n.sbd)
    elif n.code == '-':
        if n.sbd is not None:
            return compute(n.sbg) - compute(n.sbd)
        else:
            return -compute(n.sbg)
    elif n.code == '/':
        return compute(n.sbg) / compute(n.sbd)
    elif n.code == '*':
        return compute(n.sbg) * compute(n.sbd)
    elif n.code == '%':
        return compute(n.sbg) % compute(n.sbd)
    elif n.code == '**':
        return compute(n.sbg) ** compute(n.sbd)
    elif n.code == '//':
        return compute(n.sbg) // compute(n.sbd)
    elif n.code in ('INT', 'FLOAT', 'BOOL', 'STRING'):
        return n.value
    elif n.code in ('LIST'):
        #x = compute(n.sbg)
        #print ">>> ", x, " : ", x.__class__
        return compute(n.sbg) # on compute un noeud de type "param" == liste
    elif n.code == 'and':
        return compute(n.sbg) and compute(n.sbd)
    elif n.code == 'or':
        return compute(n.sbg) or compute(n.sbd)
    elif n.code == 'not':
        return not compute(n.sbg)
    elif n.code == '==':
        return compute(n.sbg) == compute(n.sbd)
    elif n.code == '!=':
        return compute(n.sbg) != compute(n.sbd)
    elif n.code == '>':
        return compute(n.sbg) > compute(n.sbd)
    elif n.code == '>=':
        return compute(n.sbg) >= compute(n.sbd)
    elif n.code == '<':
        return compute(n.sbg) < compute(n.sbd)
    elif n.code == '<=':
        return compute(n.sbg) <= compute(n.sbd)
    elif n.code == 'in':
        gauche = compute(n.sbg)
        droite = compute(n.sbd)
        if not isiterable(droite):
            Exception("Is not iterable")
        return gauche in droite
    elif n.code == 'ID':
        #if not n.value in scope.ids:
        #    error(2, "VARIABLE DOESN'T EXIST")
        s = scope.get(n.value)
        if s is None:
            try:
                s = eval(n.value)
            except:
                error(2, "VARIABLE DOESN'T EXIST")
        #print("RRR : %s = %s" % (str(n.value),str(s)))
        return s # le bug etait la : avais oublie le return. Rajout. Or entre temps, introduit le meme bug dans get !
    elif n.code == 'INDEX_OPERATOR':
        indexed = compute(n.sbg)
        parameter = compute(n.sbd)
        if parameter <= 0 or parameter > len(indexed):
            error(10, "INDEX OUT OF BOUND")
        return indexed[parameter-1]
        #s = scope.get(n.value)
        #if s is None:
        #    try:
        #        s = eval(n.value)
        #    except:
        #        error(2, "VARIABLE DOESN'T EXIST")
        #parameter = compute(n.param)
        #if parameter <= 0 or parameter > len(s):
        #    error(10, "INDEX OUT OF BOUND")
        #else:
        #    return s[parameter-1]
    elif n.code == 'DEF_FUN':
        pass
    elif n.code == 'DEF_FUN_NOPARAM':
        pass
    elif n.code == 'FUNCALL':
        parameters = compute(n.sbg)
        if n.param.value == 'println':
            return pypo_println(parameters)
        elif n.param.value == 'print':
            return pypo_print(parameters)
        elif n.param.value == 'range':
            return pypo_range(parameters)
    elif n.code == 'PARAMS':
        if n.sbg is not None and n.sbd is None: # Terminal
            return [compute(n.sbg)]
        elif n.sbg is not None and n.sbd is not None: # Liste de parametres
            gauche = compute(n.sbg) # le terminal est tjs a gauche, c donc de la que viendra la liste
            droite = compute(n.sbd) # la on aura la liste des arguments
            gauche.append(droite)
            return gauche
        elif n.sbg is None and n.sbd is not None:
            raise Exception("The list should be in the right arm!")
        elif n.sbg is None and n.sbd is None:
            raise Exception("Everything is None dude. Alright?")
        #return compute(n.sbg) # IL VA FALLOIR UNE PILE POUR EMPILER LES RES DES COMPUTESs
    elif n.code == 'PROGRAM':
        if n.sbd is not None:
            compute(n.sbg)
            return compute(n.sbd)
        elif n.sbg is not None:
            return compute(n.sbg)
        else:
            return None
    else:
        raise Exception("CODE UNKNOWN")

#
# Gui
class GuiTreeView:
    
    def make_tree(self, guitree, parent, node):
        code = node.code
        sbg = node.sbg
        sbd = node.sbd
        param = node.param
        value = node.value
        
        s = code
        
        if value is not None:
            s += (" = %s" % (str(value),))
        
        if param is not None:
            s += (" %s" % (param,))
        
        neo = guitree.append(parent, [s])
        
        if sbg is not None:
            self.make_tree(guitree, neo, sbg)
        
        if sbd is not None:
            self.make_tree(guitree, neo, sbd)
    
    # close the window and quit
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def __init__(self, tree):
        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("AST Gui View")
        self.window.set_size_request(500, 500)
        self.window.connect("delete_event", self.delete_event)

        # create a TreeStore with one string column to use as the model
        self.treestore = gtk.TreeStore(str)

        # we'll add some data now - 4 rows with 3 child rows each
        self.make_tree(self.treestore, None, tree)
        
        # create the TreeView using treestore
        self.treeview = gtk.TreeView(self.treestore)

        # create the TreeViewColumn to display the data
        self.tvcolumn = gtk.TreeViewColumn('Column 0')

        # add tvcolumn to treeview
        self.treeview.append_column(self.tvcolumn)

        # create a CellRendererText to render the data
        self.cell = gtk.CellRendererText()

        # add the cell to the tvcolumn and allow it to expand
        self.tvcolumn.pack_start(self.cell, True)

        # set the cell "text" attribute to column 0 - retrieve text
        # from that column in treestore
        self.tvcolumn.add_attribute(self.cell, 'text', 0)

        # make it searchable
        self.treeview.set_search_column(0)

        # Allow sorting on the column
        self.tvcolumn.set_sort_column_id(0)

        # Allow drag and drop reordering of rows
        self.treeview.set_reorderable(True)

        self.window.add(self.treeview)

        self.window.show_all()

gui = True

if __name__ == '__main__':
    s = read('essai.pypo')
    if verbose:
        l = get_tokens(s)
        for tok in l:
            if tok.type != 'NEWLINE':
                print "line %d:%s(%s)"%(tok.lineno, tok.type, tok.value)
            else:
                print("line %d:%s(\\n)"%(tok.lineno, tok.type))
    ast = get_ast(s)
    if verbose:
        string_repr = explore(ast,0)
        out = file('out.txt','w')
        out.write(string_repr)
        out.close()
        # A l'ecran. Pas bien si prog trop long.
        #print result.__class__
        #print(string_repr)
        #print("------------------ End Explore ------------------")
    result = compute(ast)
    dump()
    print("Result = %s of type %s" % (result, result.__class__))
    if gui:
        import pygtk
        pygtk.require('2.0')
        import gtk
        print ast.__class__
        tvexample = GuiTreeView(ast)
        gtk.main()
    exit()

# DEPRECATED BELOW

#
# Main function
if __name__ == '__main__':
    if not from_disk:
        s = ''
        while s != 'exit':
            s = raw_input('>>> ')
            if s == 'dump':
                dump()
            elif s != 'exit':
                compute_string(s, True)
    elif from_disk:
        files = ('essai.pypo',)
        compute_file(files[0], True)
        dump()
        #files = ('tests/pypo_essai.txt', 
        #         'tests/pypo_essai_error.txt')
        #compute_file(files[1], True)
    else:
        print "TEST"
        tests = (("a = 3"    , 3), 
                 ('b = "abc"', 'abc')
                )
        for test in tests:
            if compute_string(test[0]) == test[1]:
                print("OK")
            else:
                print("NO")

