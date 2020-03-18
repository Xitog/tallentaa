import os
import sys

# bytes
WORD = 2
LONG = 4

# http://cade.datamax.bg/war2x/pudspec.html

class PUD:

    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.mapname = os.path.splitext(self.filename)[0]
        content = None
        with open(filepath, "rb") as pud:
            content = pud.read()
        self.content = bytearray(content)
        self.sections = {}
        pos = 0
        while pos < len(self.content):
            tag, length = self.section(pos)
            self.sections[tag] = (pos, length)
            pos += length + 8 # 4 for tag, 4 for length
            print(f"{tag:4} {pos:6d} {len(self.content):6d}")
        # null terminated string
        info = self.sections['DESC']
        self.desc = self.read_str(info[0] + 8, info[1])
        # 128 or 96 or 64 or 32. x must be equal to y.
        info = self.sections['DIM ']
        self.width = self.read_int(info[0] + 8, WORD)
        self.height = self.read_int(info[0] + 8 + WORD, WORD)
        #
        info = self.sections['MTXM']
        self.map = self.read_matrix(info[0], self.width * self.height, self.width)

    def info(self):
        print(f"{self.mapname} {self.width}x{self.height}")
        print(self.desc)
        print(f"Size: {len(self)} bytes")

    def __str__(self):
        return self.mapname

    def __repr__(self):
        return str(self)

    def __len__(self):
        return len(self.content)

    def get(row, col):
        pass

    def __getitem__(self, i):
        return self.content[i]

    def read_str(self, start, length):
        s = ''
        for i in range(length):
            c = chr(self[start + i])
            if c == '\x00':
                break
            s += c
        return s

    def read_int(self, pos, length):
        cpt = 0
        for i in range(0, length):
            cpt += self[i + pos] * (256 ** i)
        return cpt

    def read_matrix(self, pos, size, width):
        content = []
        line = []
        cpt = 0
        values = {}
        while cpt < size:
            elem = self.read_int(pos + cpt * WORD, WORD)
            if elem not in values:
                values[elem] = 0
            values[elem] += 1
            line.append(elem)
            if len(line) == width:
                content.append(line)
                line = []
            cpt += 1
        for val in sorted(values, key=values.get, reverse=True):
            print(f"{val:04x} {values[val]:10d}")
        return content

    def section(self, start):
        "A section is 4 CHARs as a name then a 1 LONG as size then DATA"
        tag = self.read_str(start, 4)
        length = self.read_int(start + 4, 4)
        return tag, length


class PUD2(object):

    def __init__(self, filepath):
        self.era_length = self.read_nbytes_as_int(self.era + LONG, LONG)
        print("\tlength ERA = ", self.era_length)
        self.era_value = self.read_nbytes_as_int(self.era + LONG + LONG, WORD)
        print("\tvalue ERA= ", self.era_value)
        # 128*128*2 = 32 768
        #   96*96*2 = 18 432
        #   64*64*2 =  8 192
        #   32*32*2 =  2 048

    def save_to_file(self):
        out = open(self.mapname + "-out-v2.txt", "w")
        for lin in range(0, 32):
            for col in range(0, 32):
                #sys.stdout.write(' {0:0=4x} '.format(wmap[lin][col]))
                out.write(' {0:0=4x} '.format(self.mtxm_content[lin][col]))
            out.write("\n")
        out.close()
    
    def find_suite(self, suite):
        cpt = 0
        cpt_suite = 0
        start = None
        found = False
        while cpt < len(self.content):
            char = self.content[cpt]
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

filename = "eau-1-1-31-1.pud"
filename = "map-32x32-forest-water-5-5-start-10-10.pud"

pud = PUD(filename)
#pud.save_to_file()

# ils sont separes de 2056 = 1024 * 2 = 32 x 32 x 2
# 2 chars hexa = 16 * 16 = 256 = 1 byte

