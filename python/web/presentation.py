from zipfile import ZipFile
import os # for dir mode
import os.path # for dir mode
import html # for dir mode, escaping url

import xml.etree.ElementTree as et

from model import *
from capella_model import *

#-------------------------------------------------------------------------------
# View / output
#-------------------------------------------------------------------------------

class HTMLOutput:

    def __init__(self, model, name=None):
        self.footer = "  </body>\n</html>"
        self.header = """
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
        
        table.tserver {
            border: 1px solid #d3d3d3;
            font-size: 16px;
            border-collapse:collapse; 
            font-family: consolas;
        }

        table.tserver th {
            background: rgb(224,240,255);
            border: 1px solid #d3d3d3;
            text-align: center;
        }
        
        table.tserver td {
            border: 1px solid #d3d3d3;
            text-align: center;
            padding-right: 4em;
            padding-left: 4em;
        }
        
        table.tserver td:first-child {
            font-weight: bold;
        }
        
        table.tserver tr:hover {
            cursor: default;
            background: rgb(224, 255, 240);
        }
    
        /*
        table.tserver tr:nth-child(odd){ 
            background: white;
        }
        
        table.tserver tr:nth-child(even){
            background: rgb(240,240,240);
        }
        */
        
    </style>
    <script type="text/javascript" src="dtree.js"></script>
  </head>
        """
        self.template = self.header + """

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
    </table>""" + self.footer
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
            'zip' : 'img/file_types/archive.png',
            'jenkins' : 'img/jenkins.png'
        }
        self.lines = []
        # Groups and users
        self.groups = {} # GROUP_NAME : [USER1, USER2, USER4]
        self.users = [] # [USER1, USER2, USER3, USER4]
        self.current_group = None
        # Machines and projects
        self.machines = {}
        self.projects = []
        if type(model) == ModelBuilder:
            self.export_modelcapella(model)
        elif type(model) == Dir:
            self.export_dirtree(model)
        elif type(model) == Component:
            # Tree
            if hasattr(model, 'icon'):
                if model.icon in self.icons:
                    self.lines.append(f"d.icon.root = '{self.icons[model.icon]}';")
            self.export(model)
            f = open("tree" + os.sep + model.name + ".html", 'w')
            template = self.template.replace('__SOMETHING__', '\n'.join(self.lines))
            f.write(template)
            f.close()
            # File rendering
            self.user_matrix_rendering()
            self.machine_overview_rendering()
            self.project_overview_rendering()
        else:
            raise Exception(f"Type invalid: {type(model)}")
    
    def machine_overview_rendering(self):
        matrix_page = self.header
        s = "<body><table class=\"tserver\"><thead>"
        for i in [0, 1, 2, 3]:
            s += "<col style=\"width: 25%\"/>"
        s += "<tr><th>Server</th><th>Clients</th><th>Version</th><th>Projects</th></thead><tbody>"
        servers = [a for a in self.machines if self.machines[a].subtype == 'server']
        servers.sort()
        for n in servers:
            s += f"<tr><td>{self.machines[n].name}</td><td></td><td>{self.machines[n].version}</td><td></td></tr>"
        matrix_page += s
        matrix_page += "</tbody></table>"
        matrix_page += self.footer
        f = open("tree" + os.sep + "machine_overview.html", 'w')
        f.write(matrix_page)
        f.close()
    
    def project_overview_rendering(self):
        matrix_page = self.header
        s = "<body><table class=\"tserver\"><thead>"
        for i in [0, 1, 2, 3, 4, 5, 6]:
            s += "<col style=\"width: 14%\"/>"        
        s += "<tr><th>Project</th><th>Server</th><th>Repository</th><th>Port</th><th>Version</th><th>Config</th><th>Groupe windows</th>"
        #for project in self.projects:
        #
        matrix_page += s
        matrix_page += "</tbody></table>"
        matrix_page += self.footer
        f = open("tree" + os.sep + "project_overview.html", 'w')
        f.write(matrix_page)
        f.close()
        
    def user_matrix_rendering(self):
        matrix_page = self.header
        s = "<body><table class=\"tserver\"><thead>"
        s += f"<col style=\"width: 10%\"/>"
        for group in self.groups:
            s += f"<col style=\"width: {int(90/len(self.groups))}%\"/>"
        s += "<tr><th>User name</th>"
        for group in self.groups:
            s += f"<th>{group}</th>"
        s += "</tr></thead><tbody>"
        self.users.sort()
        ordered_group = list(self.groups.keys())
        ordered_group.sort()
        for user in self.users:
            s += f"<tr><td>{user}</td>"
            for group in ordered_group:
                if user in self.groups[group]:
                    s += "<td align=\"center\"><img src=\"img/check.png\"</td>"
                else:
                    s += "<td></td>"
            s += "</tr>"
        matrix_page += s
        matrix_page += "</tbody></table>"
        matrix_page += self.footer
        f = open("tree" + os.sep + "user_matrix.html", 'w')
        f.write(matrix_page)
        f.close()
    
    def export(self, root, base=-1, last_num=-1):
        # Matrix recording
        if hasattr(root, 'type'):
            if root.type == 'Group':
                if root.name not in self.groups:
                    self.groups[root.name] = []
                    self.current_group = root.name
            elif root.type == 'User':
                if self.current_group is not None and self.current_group in self.groups:
                    self.groups[self.current_group].append(root.name.lower())
                if root.name.lower() not in self.users:
                    self.users.append(root.name.lower())
            elif root.type == 'Machine':
                if root.name not in self.machines:
                    v = "?"
                    if hasattr(root, "version"):
                        v = root.version
                    st = "?"
                    if hasattr(root, "subtype"):
                        st = root.subtype
                    self.machines[root.name] = Machine(root.name, v, st)
            elif root.type == 'Project':
                if root.name not in self.projects:
                    self.projects.append(root.name)
        # Tree production
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
        for lvl in model.levels:
            last_num += 1
            lines.append(f"        d.add({last_num},0,'{lvl.name}', '', '', '', 'img/archi_mel.png', 'img/archi_mel.png');")
            for pak in lvl.packages:
                last_num = xplore(pak, last_num, last_num)
        filename = model.name + ".html"
        print("Producing", filename)
        f = open("tree" + os.sep + filename, 'w')
        template = self.template.replace('__SOMETHING__', '\n'.join(lines))
        f.write(template)
        f.close()

#-------------------------------------------------------------------------------
# Controller
#-------------------------------------------------------------------------------

def produce_presentation(mode, filepath=None, filename=None):
    if mode == 'maestro':
        f = open("maestro.json")
        c = f.read()
        f.close()
        import json
        def explore(name, dic, parent=None):
            root = Component(name, parent)
            for k,v in dic.items():
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
                elif k == "type":
                    root.type = v
                elif k == "version":
                    root.version = v
                elif k == "subtype":
                    root.subtype = v
                elif type(v) == dict:
                    explore(k, v, root)
                else:
                    pass
            return root
        c = json.loads(c)
        root = explore(list(c.keys())[0], list(c.values())[0])
        HTMLOutput(root)
    elif mode == 'file':
        target = os.sep.join([filepath, filename])
        with ZipFile(target) as archive:
            archive.printdir()
            with archive.open(FILE) as file:
                s = file.read()
        #print(s[0:25])
        root = et.fromstring(s)
        #print(root)       
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
    
    from time import gmtime, strftime
    s = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    
    print(f"End of Presentation at {s}")

produce_presentation('maestro')
produce_presentation('file', r"DIR", "ZIPFILE")
