#-------------------------------------------------------------------------------
# Tree utilities
#-------------------------------------------------------------------------------

# This module provides the class Component to handle Tree data structure.
# if Component.is_root() => it's a tree
# if Component.is_leaf() => it's a leaf
# if len(Component.children) == 0 => it's a leaf
#
# Each Component has a name and a value and a level.
#
# Level of root is zero.
# Index of first child is zero.
#
# Tree can be created from a dictionary (like json data loaded in memory)
#
# Damien Gouteux, 2017
#-------------------------------------------------------------------------------

class Component:
    
    def __init__(self, name='', parent=None, value=None):
        self.name = name
        self.parent = parent
        if self.parent is not None:
            self.level = self.parent.level + 1
        else:
            self.level = 0
        self.value = value
        self.children = []
    
    def is_root(self):
        return self.parent is None

    def is_leaf(self):
        return len(self.children) == 0

    def add(self, e):
        if type(e) != Component:
            name = str(e)
            if hasattr(e, 'name'):
                name = e.name
            e = Component(name, self, e)
        self.children.append(e)
    
    def __str__(self):
        return "    " * self.level + f"{self.name} ({self.level})"

    def dump(self):
        print(self)
        for c in self.children:
            c.dump()

    # { 'a' : 123, 'b' : 456, 'c' : { 'd' : 'abc' } }
    @staticmethod
    def from_dict(name, dic, parent=None):
        root = Component(name, parent)
        for k, v in dic.items():
            if type(v) == dict:
                root.add(Component.from_dict(k, v, root))
            else:
                root.add(v)
        return root

def test_tree():
    tree = Component('My root')
    tree.add(5)
    tree.add(6)
    tree.dump()
    data = {
        'a' : 123,
        'b' : 456,
        'c' : {
            'd' : 'abc'
        }
    }
    print('-----')
    tree2 = Component.from_dict('Tree 2', data)
    tree2.dump()

if __name__ == '__main__':
    test_tree()
