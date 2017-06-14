import xml.etree.ElementTree as ET
tree = ET.parse(r'D:\Workspaces\MA_412\MA_412_WS_local_1\EOLE_AF\EOLE_AF.melodymodeller')
root = tree.getroot()
types = {}

import sys

def handling_ownedClasses(elem):
    print(elem)

handlers = { "ownedClasses" : handling_ownedClasses }

def explore(root, level=0):
    children = list(root)
    for child in children:
        # print(" " * level, child.tag)
        if child.tag not in types:
            types[child.tag] = 1
        else:
            types[child.tag] += 1
        if child.tag in handlers:
            handling_ownedClasses(child)
        explore(child, level+1)
        
explore(root)

ordered = sorted(types, key=types.__getitem__)
ordered.reverse()
for key in ordered:
    pass #print(key, types[key])

