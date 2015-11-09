
# bug : on a une iteration vertical. a droite, une autre iteration vertical qui mange! une colonne du rectangle de gauche cree lors de la precedente operation. cela ne devrait pas arriver !
# bug : parfois le range plante.

import sys
import random

class Rect:

    UID = 1
    
    def __init__(self, x, y, w, h, base = None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        Rect.UID += 1
        if base is None:
            self.base = Rect.UID
        else:
            self.base = base

    def info(self):
        print("rect at %i, %i with width = %i and height = %i" % (self.x, self.y, self.w, self.h))

    def divide(self, minimum):
        h_or_v = random.randint(1, 100)
        if h_or_v >= 50: #horizontal split
            cut = random.randint(1+minimum, self.h-minimum)
            print("horizontal at %i on (%i, %i, %i, %i)" % (cut, self.x, self.y, self.w, self.h))
            r1 = Rect(self.x, self.y, self.w, cut)
            r2 = Rect(self.x, cut, self.w, self.h-cut)
        else: #vertical split
            cut = random.randint(1+minimum, self.w-minimum)
            print("vertical at %i on (%i, %i, %i, %i)" % (cut, self.x, self.y, self.w, self.h))
            r1 = Rect(self.x, self.y, cut, self.h)
            r2 = Rect(cut, self.y, self.w-cut, self.h)
        r1.info()
        r2.info()
        return (r1, r2)

class Zone(Rect):

    def __init__(self, x, y, w, h, base, hollow):
        Rect.__init__(self, x, y, w, h, base)
        self.hollow = hollow
        self.content = []
        for i in range(0, self.h):
            l = []
            for j in range(0, self.w):
                if i > 0 and i < self.h-1 and j > 0 and j < self.w-1 and self.hollow:
                    l.append(0)
                else:
                    l.append(self.base)
            self.content.append(l)

    def draw(self):
        for i in range(0, self.h):
            for j in range(0, self.w):
                sys.stdout.write(str(self.content[i][j]))
            sys.stdout.write("\n")

    def apply(self, rect, content):
        for i in range(rect.y, rect.h+rect.y):
            for j in range(rect.x, rect.w+rect.x):
                self.content[i][j] = content

root = Zone(0, 0, 32, 32, 1, False)
print("Start : ")
root.draw()
print("--------\n\n\n")

def bsp_dungeon(rect, zone, iterations):
    if iterations == 0: return
    else: iterations -= 1
    r1, r2 = rect.divide(2)
    zone.apply(r1, r1.base)
    zone.apply(r2, r2.base)
    print("iteration no. %i" % (iterations))
    zone.draw()
    print("\n\n\n")
    bsp_dungeon(r1, zone, iterations)
    bsp_dungeon(r2, zone, iterations)
    
bsp_dungeon(root, root, 2)
root.draw()

