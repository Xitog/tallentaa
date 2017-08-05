from model import * # Todo, link both!

#-------------------------------------------------------------------------------
# Utils
#-------------------------------------------------------------------------------

def find_all(root, tag, elem):
    for child in root:
        if child.tag == tag:
            elem.append(child)
        find_all(child, tag, elem)

#-------------------------------------------------------------------------------
# Model
#-------------------------------------------------------------------------------
 
class ModelBuilder:

    def __init__(self, root):
        self.root = root
        self.types = {}
        self.packages = {}
        self.name = None
        self.levels = []

    def add_type(self, typ):
        self.types[typ.id] = typ
        typ.parent = self

    def add_package(self, pkg):
        self.packages[pkg.id] = pkg
        pkg.parent = self

    def explore(self):
        print(f"There is {len(self.packages)} packages.")
        for kp, vp in self.packages.items():
            vp.explore()
    
    def build_model(self):
        self.parse(self.root, None)
    
    def parse(self, elem, in_package):
        for child in elem:
            # 'ownedLiterals'
            # 'ownedUnits'
            # print(child.tag)
            if child.tag == 'ownedModelRoots':
                self.name = child.attrib['name']
            elif child.tag == 'ownedArchitectures':
                self.levels.append(ArchitectureLevel(child.attrib['name']))
            
            if child.tag in ['ownedDataPkg', 'ownedDataPkgs']:
                print('ownedDataPkg: ' + child.attrib['name'])
                typ = child.attrib['{http://www.w3.org/2001/XMLSchema-instance}type']
                did = child.attrib['id']
                name = child.attrib['name']
                pkg = Package(did, name, typ)
                if in_package is not None:
                    in_package.add_package(pkg)
                else: # all first-level package are directly referenced by the model
                    self.add_package(pkg)
                    self.levels[-1].add_package(pkg)
                self.parse(child, pkg)
            elif child.tag == 'ownedDataTypes':
                #print('ownedDataTypes')
                did = child.attrib['id']
                name = child.attrib['name']
                if 'discrete' in child.attrib:
                    disc = child.attrib['discrete'] # false or true
                else:
                    disc = None
                typ = child.attrib['{http://www.w3.org/2001/XMLSchema-instance}type']
                if 'kind' in child.attrib:
                    kind = child.attrib['kind']
                else:
                    kind = None
                if 'visi' in child.attrib:
                    visi = child.attrib['visibility']
                else:
                    visi = None
                dt = DataType(did, name, typ, disc, kind, visi)
                self.add_type(dt)
                if in_package is not None:
                    in_package.add_type(dt)
            elif child.tag == 'ownedClasses':
                #print('ownedDataClasses')
                cid = child.attrib['id']
                name = child.attrib['name']
                if 'description' in child.attrib:
                    desc = child.attrib['description']
                else:
                    desc = None
                cls = Class(cid, name, desc)
                self.add_type(cls)
                for prop in child:
                    if prop.tag == 'ownedFeatures':
                        # print(prop.attrib)
                        fid = prop.attrib['id']
                        name = prop.attrib['name']
                        typ = prop.attrib['{http://www.w3.org/2001/XMLSchema-instance}type']
                        if 'abstractType' in prop.attrib:
                            atyp = prop.attrib['abstractType']
                        else:
                            atyp = None
                        if 'aggregationKind' in prop.attrib:
                            link = prop.attrib['aggregationKind']
                        else:
                            link = None
                        if 'description' in prop.attrib:
                            desc = prop.attrib['description']
                        else:
                            desc = None
                        feat = Feature(fid, name, typ, atyp, link, desc)
                        cls.add_feature(feat)
                if in_package is not None:
                    in_package.add_type(cls)
            else:
                self.parse(child, in_package)

#-------------------------------------------------------------------------------
# Model classes
#-------------------------------------------------------------------------------
                
class ArchitectureLevel:

    def __init__(self, name):
        self.name = name
        self.packages = []

    def add_package(self, pkg):
        self.packages.append(pkg)

class Package:

    def __init__(self, pid, name, typ):
        self.id = pid
        self.name = name
        self.type = typ
        self.types = {}
        self.sub = {}
        self.parent = None

    def add_type(self, elem):
        elem.pkg = self
        self.types[elem.id] = elem

    def add_package(self, pkg):
        self.sub[pkg.id] = pkg

    def explore(self, level=0):
        print("    " * level + f"{self}")
        for kt, vt in self.types.items():
            print("    " * (level+1) + f"{vt}")
            if type(vt) == Class:
                for f in vt.get_features():
                    print("    " * (level+2) + f"{f}")
            elif type(vt) == DataType:
                pass
        for ks, vs in self.sub.items():
            vs.explore(level+1)
        
    def __str__(self):
        return f"{self.name} ({self.id[-8:]}) [{self.type.split(':')[-1]}]"
    
class Feature:

    def __init__(self, fid, name, typ, atyp, link, desc):
        self.id = fid
        self.name = name
        self.type = typ
        self.cls = atyp
        self.link = link
        self.desc = desc
        self.parent = None
    
    def __str__(self):
        cls = self.get_type()
        if cls is None:
            return f"{self.name} ({self.id[-8:]})"
        else: 
            #return f"{self.name} ({self.id[-8:]}) [{cls}]"
            return f"{self.name} : {cls}"

    def get_type(self):
        if self.cls is None:
            cls = None
        elif self.cls[1:] in self.parent.parent.types:
            cls = self.parent.parent.types[self.cls[1:]]
        else:
            cls = self.cls[1:]
        return cls
        
class Type:

    def __init__(self, tid, name):
        self.parent = None
        self.id = tid
        self.name = name
        self.pkg = None
    
    def __str__(self):
        #return f"{self.name} ({self.id[-8:]})"
        return f"{self.name}"

class DataType(Type):

    def __init__(self, did, name, typ, disc, kind, visi):
        Type.__init__(self, did, name)
        self.type = typ
        self.disc = disc
        self.kind = kind
        self.visi = visi

class Class(Type):

    def __init__(self, cid, name, desc):
        Type.__init__(self, cid, name)
        self.desc = desc
        self.features = []

    def add_feature(self, feature):
        self.features.append(feature)
        feature.parent = self
    
    def get_features(self):
        return self.features
