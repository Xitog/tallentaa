import random
from PIL import Image, ImageDraw, ImageFont

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

    def __init__(self, parent, name, region=None):
        self.parent = parent
        self.name = name
        self.left = None
        self.right = None
        self.region = region
        self.code = self.path()

    @staticmethod
    def create_tree(level, parent=None, name='root'):
        root = Node(parent, name)
        if level > 0:
            root.left = Node.create_tree(level - 1, root, 'A')
            root.right = Node.create_tree(level - 1, root, 'B')
        return root

    def path(self):
        path = ''
        if not self.is_root():
            path += self.parent.path() + '.' + self.name
        else:
            path += self.name
        return path

    def is_root(self):
        return self.parent is None or not isinstance(self.parent, Node)

    def has_children(self):
        return self.left is not None

    def is_leaf(self):
        return self.left is None and self.right is None

    def __str__(self):
        if self.region is None:
            return self.code
        return f'{self.code} : {repr(self.region)}'

    def __repr__(self):
        return f'<Node {self}>'

    def link(self, region):
        if not isinstance(region, Region):
            typ = region.__class__.__name__
            raise TypeError(f'Inappropriate argument type: {typ}')
        self.region = region

    def get_region(self):
        if self.region is None:
            raise Exception('Region is not set.')
        return self.region

    def get_leaves(self):
        res = []
        if self.has_children():
            res += self.left.get_leaves()
            res += self.right.get_leaves()
        elif self.is_leaf():
            res.append(self)
        return res

    def get_node(self, code, node=None):
        if node is None:
            node = self.root
        if node.code == code:
            return node
        if node.has_children():
            res = self.get_node(code, node.left)
            if res is None:
                res = self.get_node(code, node.right)
            if res is not None:
                return res
        return None


class Region:
    
    HORIZONTAL = 1
    VERTICAL = 2

    def __init__(self, parent, x, y, width, height):
        self.parent = parent
        if parent is not None:
            if not parent.x <= x <= parent.x + parent.width:
                raise Exception(f'Minor x out of parent: {x} in {parent}')
            if not parent.x <= x + width <= parent.x + parent.width:
                raise Exception(f'Major x out of parent: {x+height} in {parent}')
            if not parent.y <= y <= parent.y + parent.height:
                raise Exception(f'Minor y out of parent: {y} in {parent}')
            if not parent.y <= y + height <= parent.y + parent.height:
                raise Exception(f'Major y out of parent: {y+width} in {parent}')
        if x < 0:
            raise Exception('x must be superior to 0')
        if y < 0:
            raise Exception('y must be superior to 0')
        self.x = x
        self.y = y
        if width < 0:
            raise Exception('Width must be superior to 0')
        if height < 0:
            raise Exception('Height must be superior to 0')
        self.width = width
        self.height = height
        self.size = (self.width, self.height)
        self.cx = x + width // 2
        self.cy = y + height // 2
        self.center = (self.cx, self.cy)
        self.division = None
        self.where = None
        self.remain = None
        self.room = None

    def divide(self, percent=0):
        self.percent_width = percent * self.width # authorized variation
        self.percent_height = percent * self.height
        dice = random.randint(1, 100)
        if dice > 50:
            # Region(10, 10, 5, 5) => from 10, 10 to 14, 14.
            # height = 5 so where = 2, remain = 3
            # top = Region(10, 10, 5, 2) => from 10, 10 to 14, 11.
            # bottom = Region(10, 12, 5, 3) => from 10, 12 to 14, 14.
            self.division = Region.HORIZONTAL
            self.where = self.height // 2
            self.remain = self.height - self.where
            # top
            region1 = Region(self, self.x, self.y, self.width, self.where)
            # bottom
            region2 = Region(self, self.x, self.y + self.where, self.width, self.remain)
        else:
            self.division = Region.VERTICAL
            self.where = self.width // 2
            self.remain = self.width - self.where
            # left
            region1 = Region(self, self.x, self.y, self.where, self.height)
            # right
            region2 = Region(self, self.x + self.where, self.y, self.remain, self.height)
        return (region1, region2)
    
    def __str__(self):
        message = f'({self.x}, {self.y}, {self.width}, {self.height})'
        if self.room is not None:
            message += ' with ' + repr(self.room)
        return message

    def __repr__(self):
        return f'<Region {self}>'

    def is_divided(self):
        return self.division is not None

    def make_room(self):
        self.room = Room()


class Room:

    def __init__(self):
        pass

    def __str__(self):
        return f'x'

    def __repr__(self):
        return f'<Room {self}>'


class BSP:
    "Binary space tree"

    def __init__(self, levels, area=None):
        if area is not None and isinstance(area, Area):
            self.area = area
        elif area is not None and isinstance(area, tuple) and \
             len(area) == 2 and isinstance(area[0], int) and \
             isinstance(area[1], int):
            self.area = Area(area[0], area[1])
        else:
            self.area = Area(32, 32)
        self.root = Node.create_tree(levels)
        self.populate()

    def populate(self, node=None, region=None):
        if node is None:
            node = self.root
        if region is None:
            node.link(Region(None, 0, 0, self.area.width, self.area.height))
        else:
            node.link(region)
        if node.has_children():
            r1, r2 = node.region.divide()
            self.populate(node.left, r1)
            self.populate(node.right, r2)
        else:
            node.get_region().make_room()

    def print(self, node=None, level=0):
        if node is None:
            node = self.root
        print('    ' * level, str(node))
        if node.has_children():
            self.print(node.left, level+1)
            self.print(node.right, level+1)

    def get_area(self):
        return self.area

    def __getitem__(self, code):
        target = self.get_node(code)
        if target is not None:
            return target.region
        return None

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


class Renderer:

    def __init__(self, scale=32):
        self.scale = 32
        self.colors = [
            (255, 255, 255, 255), (255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255),
            (255, 255, 0, 255), (0, 255, 255, 255), (255, 0, 255, 255), (192, 192, 192, 255),
            (192, 0, 0, 255), (192, 192, 0, 255), (192, 0, 192, 255), (192, 192, 192, 255)]

    def get_color(self, nb):
        return nb % len(self.colors)

    def render(self, bsp, filepath="out.png"):
        area = bsp.get_area()
        image = Image.new("RGBA", (area.width * self.scale, area.height * self.scale),
                          (0, 0, 0, 255))
        pencil = ImageDraw.Draw(image)
        self.draw(pencil, bsp.root)
        image.save(filepath)

    def draw(self, pencil, node, level=0, nb=0):
        region = node.region
        region.color = self.colors[self.get_color(nb)]
        x1 = region.x * self.scale + level * 2
        y1 = region.y * self.scale + level * 2
        x2 = (region.x + region.width) * self.scale - level * 2
        y2 = (region.y + region.height) * self.scale - level * 2
        print(f'draw {region.x:5d} {region.y:5d} {region.width:5d} {region.height:5d} {x1:5d}, {y1:5d}, {x2:5d}, {y2:5d} level={level} nb={nb}')
        pencil.rectangle([x1, y1, x2, y2], outline=region.color)
        x3 = region.cx * self.scale
        y3 = region.cy * self.scale
        pencil.text((x3, y3), node.code, region.color, ImageFont.load_default())
        if node.has_children():
            self.draw(pencil, node.left, level + 1, nb + 1)
            self.draw(pencil, node.right, level + 1, nb + 2)


if __name__ == '__main__':
    for _ in range(1000):
        bsp = BSP(5, (50, 50)) # 2, (10, 10)
    bsp.print()
    renderer = Renderer()
    renderer.render(bsp)
