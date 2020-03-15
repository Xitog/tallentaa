from sys import argv
from PIL import Image
from copy import deepcopy

class ImageInfo:

    def __init__(self, filepath):
        i = Image.open(filepath).convert("RGBA")
        s = i.getpixel((0, 0))
        colors = []
        for w in range(i.width):
            for h in range(i.height):
                color = i.getpixel((w, h))
                if color not in colors:
                    colors.append(color)
        self.__colors = colors
        self.width = i.width
        self.height = i.height
        self.img = i
        self.buffer = deepcopy(self.img)

    def get(self, x, y):
        return self.img.getpixel((x, y))

    def colors(self):
        return self.__colors

    def replace(self, old, new):
        for w in range(self.width):
            for h in range(self.height):
                color = self.buffer.getpixel((w, h))
                if color == self.__colors[old]:
                    self.buffer.putpixel((w, h), new)
                else:
                    self.buffer.putpixel((w, h), color)
        self.save("last.png")

    def highlight(self, colnum):
        self.replace(colnum, (255, 0, 255))
        self.save("last.png")

    def reset(self):
        del self.buffer
        self.buffer = deepcopy(self.img)
        self.save("last.png")

    def save(self, output, swap=False):
        if swap:
            del self.img
            self.img = self.buffer
            self.buffer = None
            self.img.save(output)
        else:
            self.buffer.save(output)

#colors[(237,  28, 36, 255)] = (0, 255,   0, 255)
#colors[(255, 127, 39, 255)] = (0,   0, 255, 255)

current = None
commands = {
    'load <file>' : 'load a picture.',
    'list' : 'list all the colors of a picture.',
    'save <file>' : 'save to a file, swap buffer.',
    'reset' : 'reset current buffer to starting image.',
    'highlight <color index>' : 'replace the given color by magenta.',
    'replace <color index> <color>' : 'replace the given color by another.',
    'help' : 'this help.'
    }

def execute(cmd, target):
    global current
    if cmd.startswith('load'):
        cmd, target = cmd.split(' ')
        current = ImageInfo(target)
    elif cmd == 'list':
        colors = current.colors()
        print('Number of colors:', len(colors))
        print('Colors:')
        for i, col in enumerate(colors):
            print(f"\t{i:3d}. R {col[0]:3d} G {col[1]:3d} B {col[2]:3d} A {col[3]:3d}")
    elif cmd.startswith('save'):
        cmd, target = cmd.split(' ')
        current.save(target, True)
    elif cmd.startswith('highlight'):
        cmd, old = cmd.split(' ')
        current.highlight(int(old))
    elif cmd.startswith('replace'):
        cmd, old, newR, newG, newB = cmd.split(' ')
        current.replace(int(old), (int(newR), int(newG), int(newB), 255))
    elif cmd == 'reset':
        current.reset()
    elif cmd == 'help':
        for cmd, desc in commands.items():
            print(f"{cmd:30} : {desc}")
    else:
        print(cmd, 'command not known.')

if __name__ == '__main__':
    print(argv)
    if len(argv) >= 3:
        target = argv[1]
        cmd = argv[2]
        execute(cmd, target)
    else:
        cmd = ''
        while cmd != 'exit':
            cmd = input('>>> ')
            target = 'img.png'
            execute(cmd, target)

