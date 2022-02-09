# Move this file in 1.0 to work
# Many thanks to the people behind the following pages:
# - https://moddingwiki.shikadi.net/wiki/GameMaps_Format
# - https://github.com/id-Software/wolf3d/blob/master/WOLFSRC/ID_CA.C
# - https://vpoupet.github.io/wolfenstein/docs/files.html
# - https://fabiensanglard.net/gebbwolf3d/
# - https://www.vgmaps.com/Atlas/PC/index.htm
# You rocks!

#---------------------------------------------------------------------
# Header file
#---------------------------------------------------------------------

class Header:

    def __init__(self, filename):
        f = open(filename, 'rb')
        try:
            # 
            self.magic = int.from_bytes(f.read(2), byteorder='little', signed=False)
            self.ptr = []
            for i in range(0, 100):
                # UINT32LE
                self.ptr.append(int.from_bytes(f.read(4), byteorder='little', signed=False))
            # Display
            print('Magic:', hex(self.magic))
            for i in range(0, 100):
                if (self.ptr[i] == 0xffffffff): # ptr to headers
                    break
                print(f"    Ptr {i:5d} {hex(self.ptr[i])}")
        except Exception as e:
            print(e)
        f.close()

h = Header("maphead.wl1")

#---------------------------------------------------------------------
# Content file
#---------------------------------------------------------------------

f = open("maptemp.wl1", "rb")
filetype = f.read(8).decode(encoding='ascii')
print('Format:', filetype)

class Level:

    def __init__(self):
        self.name = ''
        self.width = 0
        self.height = 0

    def __str__(self):
        return f"{self.name} {self.width}x{self.height}"


def read_level(h, f, num):
    lvl = Level()
    # For, 0, we are pointing on first level header after 8 bytes, corresponding to h.ptr[0]
    if f.tell() != h.ptr[num]:
        raise Exception(f"We are not at the beginning of the first level: {f.tell()} vs {h.ptr[num]}")

    # Uncompressed level header is 38 bytes
    lvl.offPlane0 = int.from_bytes(f.read(4), byteorder='little', signed=True)
    lvl.offPlane1 = int.from_bytes(f.read(4), byteorder='little', signed=True)
    lvl.offPlane2 = int.from_bytes(f.read(4), byteorder='little', signed=True)
    # All length are compressed
    lvl.lenPlane0 = int.from_bytes(f.read(2), byteorder='little', signed=False)
    lvl.lenPlane1 = int.from_bytes(f.read(2), byteorder='little', signed=False)
    lvl.lenPlane2 = int.from_bytes(f.read(2), byteorder='little', signed=False)
    lvl.width = int.from_bytes(f.read(2), byteorder='little', signed=False)
    lvl.height = int.from_bytes(f.read(2), byteorder='little', signed=False)
    lvl.name = f.read(16).decode(encoding='ascii')

    print(f"Plane0 offset={lvl.offPlane0:5d} length={lvl.lenPlane0:5d}")
    print(f"Plane1 offset={lvl.offPlane1:5d} length={lvl.lenPlane1:5d}")
    print(f"Plane2 offset={lvl.offPlane2:5d} length={lvl.lenPlane2:5d}")

    HEADER_SIZE = 38
    if f.tell() != HEADER_SIZE + h.ptr[num]:
        raise Exception(f"We are not at the beginning of a level data! : {f.tell()} vs {HEADER_SIZE + h.ptr[num]}")

    lvl.data0 = f.read(lvl.lenPlane0) # for size
    lvl.data1 = f.read(lvl.lenPlane1)
    lvl.data2 = f.read(lvl.lenPlane2)

    # normalement, on est à un header du prochain h.ptr :
    print(f"f.tell() = {f.tell()} vs h.ptr[next] = {h.ptr[num+1]}")

    # diff de 4
    mis = f.read(4).decode(encoding='ascii')
    print('===>', mis) # signature !ID!

    return lvl


def rwle_expand(h, data):
    size = int.from_bytes(data[0:2], byteorder='little', signed=False)
    print('Final size in byte =       ', size)
    plane = []
    i = 2
    while i < len(data):
        v = int.from_bytes(data[i:i+2], byteorder='little', signed=False)
        i += 2
        if v == h.magic:
            count = int.from_bytes(data[i:i+2], byteorder='little', signed=False)
            i += 2
            value = int.from_bytes(data[i:i+2], byteorder='little', signed=False)
            i += 2
            plane += [value] * count
        else:
            plane.append(v)
    print('Length of plane (word)=    ', len(plane))
    return plane


def analyze(plane):
    from collections import Counter
    c = Counter(plane)
    print('Number of values:', len(c))
    for k, v in sorted(c.items(), key=lambda i: i[1], reverse=True):
        print(f"    {k:5d} => {v:5d}")


def to_matrix(lvl, plane):
    matrix = []
    row = 0
    line = 0
    for line in range(0, lvl.height):
        matrix.append(plane[line * lvl.width:(line + 1) * lvl.width])
    return matrix


def to_csv(name, matrix):
    f = open(name, mode='w', encoding='ascii')
    for line in matrix:
        f.write(";".join([str(row) for row in line]) + "\n")
    f.close()

lvl0 = read_level(h, f, 0)
plane = rwle_expand(h, lvl0.data0)
analyze(plane)
matrix = to_matrix(lvl0, plane)
to_csv('output0.csv', matrix)

lvl1 = read_level(h, f, 1)
plane = rwle_expand(h, lvl1.data0)
analyze(plane)
matrix = to_matrix(lvl1, plane)
to_csv('output1.csv', matrix)

f.close()

print(lvl0)
print('Compressed length in byte =', lvl0.lenPlane0)
print('64 x 64=                   ', 64 * 64)
print('  in word x2 =             ', 64 * 64 * 2)
print('Lenght of data =           ', len(lvl0.data0))

print(lvl1)
