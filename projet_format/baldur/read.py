# char: 8-bit (1-byte)
# WORD: 16-bit (2-byte) unsigned integer
# DWORD: 32-bit (4-byte) unsigned integer

filename = "chitin.key"

RES_TYPE = {
    1 : ['bmp', 'binary', 'Windows BMP file'],
    3 : ['tga', 'binary', 'TGA image format'],
    4 : ['wav', 'binary', 'WAV sound file'],
    6 : ['plt', 'binary', 'Bioware Packed Layered Texture'],
    7 : ['ini', 'text (ini)', 'Windows INI file format'],
    10 : ['txt', 'text', 'Text file'],
    2002 : ['mdl', 'mdl', 'Aurora model'],
    2009 : ['nss', 'text', 'NWScript Source'],
    2010 : ['ncs', 'binary', 'NWScript Compiled Script'],
    2012 : ['are', 'gff', 'BioWare Aurora Engine Area file'],
    2013 : ['set', 'text (ini)', 'BioWare Aurora Engine Tileset'],
    2014 : ['ifo', 'gff', 'Module Info File'],
    2015 : ['bic', 'gff', 'Character/Creature'],
    2016 : ['wok', 'mdl', 'Walkmesh'],
    2017 : ['2da', 'text', '2-D Array'],
    2022 : ['txi', 'text', 'Extra Texture Info'],
    2023 : [],
    2025 : [],
    2027 : [],
    2029 : [],
    2030 : [],
    2032 : [],
    2033 : [],
    2035 : [],
    2036 : [],
    2037 : [],
    2038 : [],
    2040 : [],
    2042 : [],
    2044 : [],
    2045 : [],
    2046 : [],
    2047 : [],
    2051 : [],
    2052 : [],
    2053 : [],
    2056 : [],
    2058 : [],
    2060 : [],
    2064 : [],
    2065 : [],
    2066 : [],
    # KOTOR only
    2024 : ['bti'],
    2026 : ['btc'],
    
    3000 : ['lyt'],
    3001 : ['vis'],
    3002 : ['rim'],
    3003 : ['pth'],
    3004 : ['lip'],
    3005 : ['bwm'],
    3006 : ['txb'],
    3007 : ['tpc'],
    3008 : ['mdx'],
    3009 : ['rsv'],
    3010 : ['sig'],
    3011 : ['xbx'],
}

header = {}

with open(filename, "rb") as f:
    # HEADER
    byte = f.read(4)
    header["FileType"] = byte.decode("ascii") 
    byte = f.read(4)
    header["FileVersion"] = byte.decode("ascii")
    byte = f.read(4)
    header["BIFCount"] = int.from_bytes(byte, byteorder='little')
    byte = f.read(4)
    header["KeyCount"] = int.from_bytes(byte, byteorder='little')
    byte = f.read(4)
    header["OffsetToFileTable"] = int.from_bytes(byte, byteorder='little')
    byte = f.read(4)
    header["OffsetToKeyTable"] = int.from_bytes(byte, byteorder='little')
    byte = f.read(4)
    header["BuildYear"] = int.from_bytes(byte, byteorder='little') + 1900
    byte = f.read(4)
    header["BuildDay"] = int.from_bytes(byte, byteorder='little')
    byte = f.read(4) # reserved
    print(f.tell()) # on en est a 36
    # FILE TABLE
    f.seek(header["OffsetToFileTable"]) # Pour se déplacer dans le fichier !!!
    FileTable = []
    nb = 0
    while nb < header["BIFCount"]:
        FileTableElement = {}
        byte = f.read(4)
        FileTableElement["FileSize"] = int.from_bytes(byte, byteorder='little')
        byte = f.read(4)
        FileTableElement["FilenameOffset"] = int.from_bytes(byte, byteorder='little')
        byte = f.read(2)
        FileTableElement["FilenameSize"] = int.from_bytes(byte, byteorder='little')
        byte = f.read(2)
        FileTableElement["Drives"] = int.from_bytes(byte, byteorder='little')
        FileTable.append(FileTableElement)
        nb += 1
    for FileTableElement in FileTable:
        f.seek(FileTableElement["FilenameOffset"])
        byte = f.read(FileTableElement["FilenameSize"])
        FileTableElement["FileName"] = byte.decode("ascii")
    # KEY TABLE
    f.seek(header["OffsetToKeyTable"])
    KeyTable = []
    nb = 0
    while nb < header["KeyCount"]:
        KeyTableElement = {}
        byte = f.read(16)
        KeyTableElement["ResRef"] = byte.decode("ascii") 
        byte = f.read(2)
        KeyTableElement["ResourceType"] = int.from_bytes(byte, byteorder='little')
        byte = f.read(4)
        KeyTableElement["ResID"] = int.from_bytes(byte, byteorder='little')
        KeyTable.append(KeyTableElement)
        nb += 1
    
print(header)
print(FileTable[0])
print(KeyTable[0])
if KeyTable[0]["ResourceType"] in RES_TYPE:
    print(RES_TYPE[KeyTable[0]["ResourceType"]])
for k in KeyTable:
    if k["ResourceType"] not in RES_TYPE:
        print(k["ResourceType"])
    
# while byte != b"":
    