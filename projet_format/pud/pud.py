from __future__ import print_function
import os
import sys

WORD = 2
LONG = 4

# http://cade.datamax.bg/war2x/pudspec.html

class PUD(object):

    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = os.path.basename(self.filepath)
        self.mapname = self.filename[:-4]

        print("Info file -------------------------")
        print("Reading : " + self.filepath)
        print("Name of the file : " + self.filename)
        print("Name of the map : " + self.mapname)
        content = None
        with open(filepath, "rb") as pud:
            content = pud.read()
        self.content = bytearray(content)
        print("Length of file : " + str(len(self.content)) + " bytes")
        print()
        
        print("Areas -----------------------------") 
        self.type = self.find_suite("TYPE")
        print("pos TYPE = ", self.type)
        self.ver = self.find_suite("VER ")
        print("pos VER  = ", self.ver)
        self.desc = self.find_suite("DESC")
        print("pos DESC = ", self.desc)
        self.ownr = self.find_suite("OWNR")
        print("pos OWNR = ", self.ownr)
        self.era  = self.find_suite("ERA ")
        print("pos ERA  = ", self.era)
        self.era_length = self.read_nbytes_as_int(self.era + LONG, LONG)
        print("\tlength ERA = ", self.era_length)
        self.era_value = self.read_nbytes_as_int(self.era + LONG + LONG, WORD)
        print("\tvalue ERA= ", self.era_value)
        self.erax = self.find_suite("ERAX") # not found
        print("pos ERAX = ", self.erax)
        self.dim  = self.find_suite("DIM ")
        print("pos DIM  = ", self.dim)
        self.dim_size = self.read_nbytes_as_int(self.dim + LONG, LONG)
        self.x = self.read_nbytes_as_int(self.dim + LONG + LONG, WORD)
        self.y = self.read_nbytes_as_int(self.dim + LONG + LONG + WORD, WORD)
        print("\tvalue x = ", self.x)
        print("\tvalue y = ", self.y)
        # 128 or 96 or 64 or 32. x must be equal to y.
        # other areas between:
        # UDTA
        # ALOW
        # UGRD
        # SIDE
        # SGLD
        # SLBR
        # SOIL
        # AIPL
        self.mtxm = self.find_suite("MTXM")
        print("pos MTXM = ", self.mtxm)
        self.mtxm_length = self.read_nbytes_as_int(self.mtxm + LONG, LONG)
        print("\tlength mtxm = ", self.mtxm_length, "bytes")
        # 128*128*2 = 32 768
        #   96*96*2 = 18 432
        #   64*64*2 =  8 192
        #   32*32*2 =  2 048
        self.sqm  = self.find_suite("SQM ")
        print("pos SQM  = ", self.sqm)
        self.oilm = self.find_suite("OILM")
        print("pos OILM = ", self.oilm)
        self.regm = self.find_suite("REGM")
        print("pos REGM = ", self.regm)
        self.unit = self.find_suite("UNIT")
        print("pos UNIT = ", self.unit)
        print()
        
        self.mtxm_content = self.read_nb_square(self.mtxm + LONG + LONG, 1024, 32)
        
    def __len__(self):
        return len(self.content)

    def read_nbytes_as_int(self, pos, length):
        cpt = 0    
        for i in range(0, length):
            cpt += self.content[i + pos] * (256 ** i)
        return cpt

    def read_nb_square(self, pos, nb, size=-1, debug=False):
        print("Started at ", pos, "(= pos mxtm + \"mxtm\" LONG 4 + size LONG 4)")
        map_content = []
        line = []
        cpt = 0
        while cpt < nb:
            #square = self.content[pos + cpt*2] + self.content[pos + cpt*2 + 1] * 256
            square = self.read_nbytes_as_int(pos + cpt * WORD, WORD)
            if debug:
                print(str(cpt) + ". " + "[" + str(pos + cpt * 2) + "] " + '{0:0=4x}'.format(square)) # 4 chars hexa = 2 bytes = 1 word
            line.append(square)
            if len(line) == size:
                map_content.append(line)
                line = []
            cpt += 1
        if size == -1:
            map_content = line
        print("Ended at ", pos + cpt * 2)
        print("With cpt = ", cpt)
        return map_content

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

#filename = r"C:\Documents and Settings\Damien\Bureau\Projet PUD\eau-5-5.pud"
#filename = r"C:\Documents and Settings\Damien\Bureau\Projet PUD\eau-1-1.pud"
filename = r"C:\Documents and Settings\Damien\Bureau\Projet PUD\eau-1-1-31-1.pud"

pud = PUD(filename)
pud.save_to_file()

if False:

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
    
# ils sont separes de 2056 = 1024 * 2 = 32 x 32 x 2
# 2 chars hexa = 16 * 16 = 256 = 1 byte

