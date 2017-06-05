import xml.etree.ElementTree as ET
tree = ET.parse(r'D:\test_xsd2ma.xsd')
root = tree.getroot()
children = list(root)
types = []
for child in children:
    cx = list(child)
    elem = child.attrib['name']
    typ = child.tag.split('}')[1]
    s = elem + ' : ' + typ
    if len(cx) > 0:
        nb = 0
        subtype = cx[nb].tag.split('}')[1]
        # Take no annotations
        if subtype == 'annotation' and len(cx) > 1:
            nb = 1
            subtype = cx[nb].tag.split('}')[1]
        else:
            print('!!! This type has only one annotation and nothing else: ' + s)
        # Analyze subtypes
        if subtype == 'restriction':
            base = cx[nb].attrib['base']
            print(s + ' :: ' + subtype + ' of ' + base)
            if typ + ' : ' + subtype + ' of ' + base not in types:
                types.append(typ + ' : ' + subtype + ' of ' + base)
        elif subtype == 'complexContent':
            cxx = list(cx[nb])
            #print(cxx[0].tag + ' for ' + s)
            if cxx[0].tag.split('}')[1] == 'extension':
                base = cxx[0].attrib['base']
                print(s + ' :: ' + subtype + ' extension of ' + base)
                if typ + ' : ' + subtype + ' extension of ' + base not in types:
                    types.append(typ + ' : ' + subtype + ' extension of ' + base)
        elif subtype == 'sequence':
            cxx = list(cx[nb])
            composed = ''
            for cxxi in cxx:
                if cxxi.tag.split('}')[1] == 'element':
                    composed += cxxi.attrib['type'] + ' '
            print(s + ' :: ' + subtype + ' composed of ' + composed)
            if typ + ' : ' + subtype + ' composed of ' + composed not in types:
                types.append(typ + ' : ' + subtype + ' composed of ' + composed)
        else:
            print(s + ' :: ' + subtype)
            if typ + ' : ' + subtype not in types:
                types.append(typ + ' : ' + subtype)
    else:
        print(s)
        print(typ)
        if typ == 'element':
            typ = elem
        else:
            raise Exception('Unknown type : ' + typ)
        if typ not in types:
            types.append(typ)

# OK, j'ai des séquences vides
# Et j'ai un type "element" qui se balade   <xs:element name="TStatus" type="tns:TStatus"/>
# Il faut que j'arrive à écrire des enum dans le MM
# Il faut que j'arrive à lire un XSD => écrire dans le MM
# Bon j'arrive plus à faire marcher to XSD...

for t in types:
    print('>>> ' + t)

def select_level(name):
    for neighbor in root.iter('ownedArchitectures'):
        if neighbor.attrib['name'] == name:
            return neighbor
    return None

def select_data_package(node):
    return node.find('ownedDataPkg')

class IdMaster:
    
    def __init__(self, seed):
        self.seed = seed
    
    def get_id(self):
        self.seed += 1
        return 'ffffffff-0000-0000-0000-{0:012}'.format(self.seed)

class MelClass:

    def __init__(self, mid, name):
        self.mid = mid
        self.name = name
        self.properties = {}
    
    def add_property(self, p):
        self.properties[p.name] = p

class MelProperty:

    def __init__(self, mid, name, typ, mincard=1, maxcard=1):
        self.mid = mid
        self.name = name
        self.typ = typ
        self.mincard = mincard
        self.maxcard = maxcard

class Perfecto:

    def __init__(self, filename, gid, types):
        self.file = open(filename, 'r')
        self.lines = self.file.readlines()
        self.gid = gid
        self.types = types
    
    def select_level(self, name):
        nb=0
        for line in self.lines:
            if line.find('ownedArchitectures') != -1 and line.find(name.replace(' ', '')) != -1:
                return (nb, line)
            nb+=1
        return None
    
    def select_data_package(self, line):
        for i in range(line, len(self.lines)):
            if self.lines[i].find('ownedDataPkg') != -1:
                return (i, self.lines[i])

    def open_data_package(self, line):
        print(self.lines[line+1])
        if self.lines[line+1].find('/>') != -1:
            self.lines[line+1] = self.lines[line+1].replace('/>', '>')
        self.lines.insert(line+2, '      </ownedDataPkg>\n')
        
    def append_class(self, klass, line):
        if klass.__class__ != MelClass:
            Exception('Klass must be an instance of MelClass')
        s = '        ' + '<ownedClasses xsi:type="org.polarsys.capella.core.data.information:Class"' + '\n'
        self.lines.insert(line, s)
        s = '            ' + 'id="' + klass.mid + '" name="' + klass.name + '"/>' + '\n'
        self.lines.insert(line + 1, s)
        if len(klass.properties) > 0:
            p.open_class(line)
            for name, prop in klass.properties.items():
                s = '           <ownedFeatures xsi:type="org.polarsys.capella.core.data.information:Property"\n'
                self.lines.insert(line + 2, s)
                s = '              id="' + prop.mid + '" name="' + prop.name + '" abstractType="#' + self.types[prop.typ] + '">\n'
                self.lines.insert(line + 3, s)
                s = '            <ownedMinCard xsi:type="org.polarsys.capella.core.data.information.datavalue:LiteralNumericValue"\n'
                self.lines.insert(line + 4, s)
                s = '                id="' + self.gid.get_id() + '" value="' + str(prop.mincard) + '"/>\n'
                self.lines.insert(line + 5, s)
                s = '            <ownedMaxCard xsi:type="org.polarsys.capella.core.data.information.datavalue:LiteralNumericValue"\n'
                self.lines.insert(line + 6, s)
                s = '                id="' + self.gid.get_id() + '" value="' + str(prop.maxcard) + '"/>\n'
                self.lines.insert(line + 7, s)
                s = '          </ownedFeatures>\n'
                self.lines.insert(line + 8, s)
        return line
    
    def open_class(self, line):
        print(self.lines[line+1])
        if self.lines[line+1].find('/>') != -1:
            self.lines[line+1] = self.lines[line+1].replace('/>', '>')
        self.lines.insert(line+2, '        </ownedClasses>\n')
    
    def write(self, filename):
        file = open(filename, 'w')
        for line in self.lines:
            file.write(line)
        file.close()
        
gid = IdMaster(0)

ma_classe = MelClass(gid.get_id(), 'Pipo')
ma_prop = MelProperty(gid.get_id(), 'Prop1', 'Double', 1, 1)
ma_classe.add_property(ma_prop)
ma_prop = MelProperty(gid.get_id(), 'Prop2', 'Integer', 1, 1)
ma_classe.add_property(ma_prop)

p = Perfecto(r'D:\BaseEmpty.melodymodeller', gid, {
            'Double' : '0b22973f-de9e-400f-adac-671ba04f1b69',
            'Integer' : '5d57daa7-e489-49d0-bedd-ad62864852da',
        }
    )

level = p.select_level('Logical Architecture')
if level is not None:
    print('lvl found:', str(level[0]) + ':', level[1])
else:
    print('not found')
    
data = p.select_data_package(level[0])
p.open_data_package(data[0])
if data is not None:
    print('data found:', str(data[0]) + ':', data[1])
else:
    print('not found')

p.append_class(ma_classe, data[0]+2)

p.write('D:\Workspaces\MA_404\MelodyTests\MA_404_WS_NavigationSimple\Empty\Empty.melodymodeller')
