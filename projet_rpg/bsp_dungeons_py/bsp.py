class Area:
    "A matrix area. Store by columns."
    
    def __init__(self, width, height, default=0):
        self.width = width
        self.height = height
        self.content = []
        for x in range(width):
            column = []
            for y in range(height):
                column.append(default)
            self.content.append(column)

    def set(self, x, y, val):
        self.content[x][y] = val

    def get(self, x, y):
        return self.content[x][y]


class Node:

    def __init__(self, parent, name, divide):
        self.parent = parent
        self.name = name
        self.left = None
        self.right = None
        if divide > 0:
            self.left = Node(self, 'A', divide - 1)
            self.right = Node(self, 'B', divide - 1)
        self.code = self.path()

    def path(self):
        path = ''
        if not self.is_root():
            path += self.parent.path() + '.' + self.name
        else:
            path += self.name
        return path

    def is_root(self):
        return self.parent == None

    def has_children(self):
        return self.left is not None

    def is_leaf(self):
        return self.left is None and self.right is None

    def __str__(self):
        return self.code

    def __repr__(self):
        return str(self)

    def get_leaves(self):
        res = []
        if self.has_children():
            res += self.left.get_leaves()
            res += self.right.get_leaves()
        elif self.is_leaf():
            res.append(self)
        return res

class BSP:
    "Binary space tree"

    def __init__(self, divide, area=None):
        self.divide = divide
        if area is not None and isinstance(area, Area):
            self.area = area
        else:
            self.area = Area(32, 32)
        self.root = Node(None, 'root', divide)

    def print(self, node=None, level=0):
        if node is None:
            node = self.root
        print('    ' * level, str(node))
        if node.has_children():
            self.print(node.left, level+1)
            self.print(node.right, level+1)

    def get_leaves(self, code, node=None):
        if node is None:
            node = self.root
        res = []
        if node.code == code:
            res = node.get_leaves()
        elif node.has_children():
            res += self.get_leaves(code, node.left)
            res += self.get_leaves(code, node.right)
        return res

if __name__ == '__main__':
    bsp_tree = BSP(8)
    bsp_tree.print()
