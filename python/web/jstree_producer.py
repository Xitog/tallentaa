from zipfile import ZipFile
import os # for dir mode
import os.path # for dir mode
import html # for dir mode, escaping url

from model import *

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



#-------------------------------------------------------------------------------
# View / output
#-------------------------------------------------------------------------------

class HTMLOutput:

    def __init__(self, model, name=None):
        self.template = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
  <head>
    <title>Symphony</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link rel="StyleSheet" href="dtree.css" type="text/css" />
    <style>
        a {
            color: rgb(102, 102, 102);
            font-family: Verdana,Geneva,Arial,Helvetica,sans-serif;
            font-size: 11px;
        }
        a:hover {
            color: rgb(222, 42, 42);
        }
    </style>
    <script type="text/javascript" src="dtree.js"></script>
  </head>
  <body style="margin: 0px; padding: 0px; width: 100%; height: 100vh;">
    <table width="100%" height="100%">
      <tr>
        <td width="30%" height="100%" valign="top">
          <div class="actions" style="text-align:right; margin: 0px; padding: 0px; border: 1px solid grey; width: 100%; border-bottom: None;">
            <a href="javascript: d.openAll();">open all</a> | <a href="javascript: d.closeAll();">close all</a>&nbsp;&nbsp;
          </div>
          <div class="dtree" style="border: 1px solid grey; width: 100%;">
            <script type="text/javascript">
            <!--
              function zorba() {
                  alert("ZORBA!");
              }
              d = new dTree('d');
              d.config.inOrder = true;
__SOMETHING__
              document.write(d);
            //-->
            </script>
          </div>
        </td>
        <td width="70%" height="100%">
          <iframe id="panel" width="100%" height="100%" name="panel" src="https://www.w3schools.com"></iframe>
          <!--<div id="pipo">PIPO</div>-->
        </td>
      </tr>
    </table>
  </body>
</html>
        """
        self.icons = {
            'add' : 'img/add.png',
            'addons' : 'img/addons.png',
            'addon' : 'img/addon.png',
            'archive' : 'img/archive.png',
            'computer' : 'img/computer.png',
            'folder' : 'img/folder.png',
            'group' : 'img/group.png',
            'home' : 'img/home.png',
            'info' : 'img/info.png',
            'job' : 'img/job.png',
            'explore' : 'img/explore.png',
            'production' : 'img/production.png',
            'integration' : 'img/integration.png',
            'page' : 'img/page.png',
            'user' : 'img/user.png',
            'user_matrix' : 'img/user_matrix.png',
            'project' : 'img/project.png',
            'py' : 'img/file_types/py.png',
            'rb' : 'img/file_types/rb.png',
            'html' : 'img/file_types/html.png',
            'xml' : 'img/file_types/xml.png',
            'folder' : 'img/file_types/folder.png',
            'zip' : 'img/file_types/archive.png'
        }
        self.lines = []
        if type(model) == ModelBuilder:
            self.export_modelcapella(model)
        elif type(model) == Dir:
            self.export_dirtree(model)
        elif type(model) == Component:
            if hasattr(model, 'icon'):
                if model.icon in self.icons:
                    self.lines.append(f"d.icon.root = '{self.icons[model.icon]}';")
            self.export(model)
            f = open("tree" + os.sep + model.name + ".html", 'w')
            template = self.template.replace('__SOMETHING__', '\n'.join(self.lines))
            f.write(template)
            f.close()
        else:
            raise Exception(f"Type invalid: {type(model)}")
    
    def export(self, root, base=-1, last_num=-1):
        num = last_num + 1
        target = ''
        if hasattr(root, 'target'):
            target = root.target
        icon = self.icons['page']
        if hasattr(root, 'icon'):
            if root.icon in self.icons:
                icon = self.icons[root.icon]
        self.lines.append(f"        d.add({num}, {base}, '{root}', '{target}', '', '', '{icon}', '{icon}');")
        base = num
        if issubclass(type(root), Component):
            for c in root.content:
                num = self.export(c, base, num)
        return num
    
    def export_dirtree(self, model):
        lines = [f"d.icon.root = 'img/folderopen.gif';"]
        known_types = { '.py' : 'img/py.png', '.rb' : 'img/rb.png', '.html' : 'img/html.png', '.xml' : 'img/xml.png'}
        def xplore(rep, base, last_num):
            num = last_num + 1
            lines.append(f"        d.add({num}, {base}, '{rep}', '', '', '', 'img/folder.gif', 'img/folderopen.gif');")
            base = num
            for elem in rep.content:
                if type(elem) == File:
                    #print('File', num)
                    num += 1
                    icon = 'img/page.gif'
                    if elem.ext in known_types:
                        icon = known_types[elem.ext]
                    target = 'file:///' + html.escape(os.path.join(rep.path, elem.name)).replace('\\', '/')
                    #target = 'file:///C:/jeux/pipo.txt'
                    lines.append(f"        d.add({num}, {base}, '{elem.name}', '{target}', '', '', '{icon}', '{icon}');")
                elif type(elem) == Dir:
                    #print('Dir', num)
                    num = xplore(elem, base, num)
            return num
        xplore(model, -1, -1)
        f = open("tree" + os.sep + model.name + ".html", 'w')
        template = self.template.replace('__SOMETHING__', '\n'.join(lines))
        f.write(template)
        f.close()
    
    def export_modelcapella(self, model):

        def xplore(pkg, base=0, last_num=0):
            last_num += 1
            if type(pkg) == Package:
                lines.append(f"        d.add({last_num}, {base}, '" + pkg.name + "', '', '', '', 'img/folder_mel.png', 'img/folder_mel.png');")
                base = last_num
            else:
                raise Exception(type(pkg))
            #if len(pkg.types) > 0:
            #    last_num += 1
            #    base_data_type = last_num
            #    lines.append(f"        d.add({base_data_type}, {base}, 'Data types');")
            for typ in pkg.types.values():
                last_num += 1
                if type(typ) == Class:
                    lines.append(f"        d.add({last_num}, {base}, '" + str(typ) + "', '', '', '', 'img/class_mel.png', 'img/class_mel.png');")
                    base_cls = last_num
                    for feat in typ.features:
                        last_num += 1
                        # link for feat
                        feat_typ = feat.get_type()
                        link = f'<a onclick="d.openTo(4, true)">{feat_typ}</a>'
                        lines.append(f"        d.add({last_num}, {base_cls}, '" + feat.name + ':' + link + "', '', '', '', 'img/prop_mel.png', 'img/prop_mel.png');")
                elif type(typ) == DataType:
                    #lines.append(f"        d.add({last_num}, {base_data_type}, '" + str(typ) + "');")
                    lines.append(f"        d.add({last_num}, {base}, '" + str(typ) + "');")
            for sub in pkg.sub.values():
                last_num += 1
                last_num = xplore(sub, base, last_num)
            return last_num
        lines = [f"d.icon.root = 'img/root_mel.png';",
                 f"        d.add(0,-1,'{model.name}');"
        ]
        last_num = 0
        #for pak in m.packages.values():
        for lvl in m.levels:
            last_num += 1
            lines.append(f"        d.add({last_num},0,'{lvl.name}', '', '', '', 'img/archi_mel.png', 'img/archi_mel.png');")
            for pak in lvl.packages:
                last_num = xplore(pak, last_num, last_num)
        f = open("tree" + os.sep + name + ".html", 'w')
        template = self.template.replace('__SOMETHING__', '\n'.join(lines))
        f.write(template)
        f.close()

#-------------------------------------------------------------------------------
# Controller
#-------------------------------------------------------------------------------

mode = 'zorba'

if mode == 'zorba':
    f = open("maestro.json")
    c = f.read()
    f.close()
    import json
    def explore(name, dic, parent=None):
        root = Component(name, parent)
        for k,v in dic.items():
            #print(k, v)
            if k == "icon":
                root.icon = v
            elif k == "display_count":
                root.display_count=(v == 'True')
            elif k == "count_tag":
                root.count_tag = v
            elif k == "level_count":
                root.level_count = v
            elif k == "target":
                root.target = v
            elif k == "__BUILD__":
                rootdir = Dir(v)
                rootdir.build()
                root.content = rootdir.content
            elif type(v) == dict:
                explore(k, v, root)
            else:
                pass
        return root
    c = json.loads(c)
    root = explore(list(c.keys())[0], list(c.values())[0])
    HTMLOutput(root)
elif mode == 'file':
    filepath = r"\\tlstore04\vm_melodyteam_archives\SPACEGATE\model"
    filename = "sgTeam_20170626_090200.zip"
    import os
    target = os.sep.join([filepath, filename])
    with ZipFile(target) as archive:
        archive.printdir()
        with archive.open('sgTeam/sg.melodymodeller') as file:
            s = file.read()
    print(s[0:25])

    import xml.etree.ElementTree as et
    root = et.fromstring(s)
    print(root)
            
    all_classes = []
    find_all(root, '', all_classes)

    m = ModelBuilder(root)
    m.build_model()
    #m.explore()
    HTMLOutput(m, "test")
elif mode == 'dir':
    rootpath = r"C:\Users\vince\Documents\Damien\GitHub\tallentaa"
    root = Dir(rootpath)
    root.build()
    HTMLOutput(root, "test")

# 14h21 zip working!
# 15h04 parcours ok!
# 15h34 DataType géré
# 16h07 Gestion par packages
