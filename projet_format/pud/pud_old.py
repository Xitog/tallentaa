from __future__ import print_function

#mapname = "eau-5-5"
#filename = r"C:\Documents and Settings\Damien\Bureau\eau-5-5.pud"
#mapname = "eau-1-1"
#filename = r"C:\Documents and Settings\Damien\Bureau\eau-1-1.pud"
mapname = "eau-1-1-31-1"
filename = r"C:\Documents and Settings\Damien\Bureau\eau-1-1-31-1.pud"

print("Reading " + filename)

seq = ["M", "T", "X", "M"]

cpt = 0
with open(filename, "rb") as pud:
    byte = pud.read(1)
    cpt += 1
    while byte != b"":
        if byte == b"M":
            byte = pud.read(1)
            cpt += 1
            if byte == b"T":
                byte = pud.read(1)
                cpt += 1
                if byte == b"X":
                    byte = pud.read(1)
                    cpt += 1
                    if byte == b"M":
                        print("MXTM!", cpt)
        # Do stuff with byte.
        byte = pud.read(1)
        cpt += 1

content = None
with open(filename, "rb") as pud:
    content = pud.read()
content = bytearray(content)

print(content)
print(type(content))
print("len = ", len(content))
#i = content.index("MXTM")
#print(i)

cpt = 0
while cpt < len(content):
    char = content[cpt]
    if char == ord("M"):
        print(chr(char), cpt)
    cpt += 1

print(chr(content[6782]))
print(chr(content[6782+1]))
print(chr(content[6782+2]))
print(chr(content[6782+3]))

def find_suite(content, suite):
    cpt = 0
    cpt_suite = 0
    start = None
    found = False
    while cpt < len(content):
        char = content[cpt]
        if char == ord(suite[cpt_suite]):
            if cpt_suite == 0:
                start = cpt
            cpt_suite += 1
            if cpt_suite == len(suite):
                found = True
                break
        else:
            cpt_suite = 0
        cpt += 1
    if found:
        return start
    else:
        return None

mtxm = find_suite(content, "MTXM")
print(mtxm)

sqm = find_suite(content, "SQM ")
print(sqm)

area = mtxm + 4

def read_nb_square(content, area, nb, size=-1, debug=False):
    map_content = []
    line = []
    cpt = 0
    while cpt < nb:
        #print(">>>", area + cpt*2, len(content))
        square = content[area + cpt*2] + content[area + cpt*2 + 1] * 256
        if debug:
            print(str(cpt) + ". " + "[" + str(area + cpt*2) + "] " + '{0:0=4x}'.format(square)) # 4 chars hexa = 2 bytes = 1 word
        line.append(square)
        if len(line) == size:
            map_content.append(line)
            line = []
        cpt += 1
    if size == -1:
        map_content = line
    return map_content

wmap = read_nb_square(content, area, 1024, 32, False)

import sys

out = open(mapname + "-out.txt", "w")
for lin in range(0, 32):
    for col in range(0, 32):
        #sys.stdout.write(' {0:0=4x} '.format(wmap[lin][col]))
        out.write(' {0:0=4x} '.format(wmap[lin][col]))
    out.write("\n")
out.close()

# ils sont separes de 2056 = 1024 * 2 = 32 x 32 x 2
# 2 chars hexa = 16 * 16 = 256 = 1 byte
