a = """
C
    Pelles C
    Bonjour
Lua
    Au revoir
Magic
    Blob
        Tobacco
    Zorba
End
"""

ID_COUNT = -1
def GET_ID():
    global ID_COUNT
    ID_COUNT += 1
    return ID_COUNT

class Node:

    def __init__(self, idn, parent, level, content):
        self.idn = idn
        self.parent = parent
        self.level = level
        self.content = content
        self.children = []

lines = a.split('\n')
cleaned_lines = []
for line in lines:
    if len(line) > 0:
        cleaned_lines.append(line)
lines = cleaned_lines

i = 0
for line in lines:
    print(i, '. ', line, sep='')
    i += 1

print('------------------')

def read(node, nb, lines):
    print('    ' * (node.level + 1), 'Call read() from', node.content, nb)
    if nb >= len(lines):
        print('    ' * (node.level + 1), 'Return 0', node.content, nb)
        return nb
    i = nb
    while i < len(lines):
        line = lines[i]
        cpt_spaces = 0
        cpt_tabs = 0
        for c in line:
            if c == ' ':
                cpt_spaces += 1
            else:
                break
        cpt_tabs = cpt_spaces // 4
        if node.level < cpt_tabs:
            # children
            new_node = Node(GET_ID(), node, cpt_tabs, line.strip())
            node.children.append(new_node)
            i = read(new_node, i + 1, lines)
        else:
            # children of one its predecessors
            break
    print('    ' * (node.level + 1), 'Return from', node.content, i)
    return i

node = Node(GET_ID(), -1, -1, "Root")
read(node, 0, lines)

def pretty_print(node):
    spacers = "    " * (node.level + 1)
    if node.parent != -1:
        parent = node.parent.content
    else:
        parent = 'ROOT'
    print(spacers + '[' + str(node.idn) + '] ' + node.content, '<', parent)
    for child in node.children:
        pretty_print(child)

pretty_print(node)

