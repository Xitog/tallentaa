import math
import os # for dir mode
import os.path # for dir mode

#-------------------------------------------------------------------------------
# Model generic
#-------------------------------------------------------------------------------

class Leaf:

    def __init__(self, name, parent=None, icon=None):
        self.name = name
        self.parent = parent
        if parent is not None:
            if not issubclass(type(parent), Component):
                raise Exception("Parent must be a Component or a subclass of it.")
            parent.content.append(self)
        self.icon = icon
    
    def __str__(self):
        return self.name

class Component(Leaf):
    def __init__(self, name, parent=None, icon=None, display_count=False, count_tag=None, level_count=math.inf):
        Leaf.__init__(self, name, parent, icon)
        self.content = []
        self.display_count = display_count
        self.count_tag = count_tag
        self.level_count = level_count
    
    def count(self, lvl=1):
        c = len(self.content)
        if lvl < self.level_count:
            for e in self.content:
                if issubclass(type(e), Component):
                    c += e.count(lvl+1)
        return c
    
    def __str__(self):
        if self.display_count:
            if self.count_tag is None:
                return f"{self.name} ({self.count()})"
            else:
                return f"{self.name} ({self.count()} {self.count_tag})"
        else:
            return Leaf.__str__(self)

#-------------------------------------------------------------------------------
# Model for file system exploration
#-------------------------------------------------------------------------------

class File(Leaf):

    def __init__(self, name, parent=None):
        Leaf.__init__(self, name, parent)
        if parent is not None and type(parent) != Dir:
            raise Exception("Parent must be a Dir.")
        self.ext = os.path.splitext(name)[1]
        self.icon = self.ext[1:]

    def to_json_object(self):
        root = {}
        #root['name'] = self.name
        #root['ext'] = self.ext
        root['icon'] = self.icon
        root['type'] = 'File'
        return root
    
class Dir(Component):

    def __init__(self, path, parent=None):
        Component.__init__(self, os.path.basename(path), parent)
        self.path = path
        self.icon = 'folder'
    
    def __str__(self):
        return f"{self.name} ({self.count()})"
    
    def add(self, elem):
        if type(elem) not in [Dir, File]:
            raise Exception("Unknown type. Must be Dir or File.")
        if elem.parent != self:
            elem.parent = self
        if elem not in self.content:
            self.content.append(elem)

    def build(rep):
        for elem in os.listdir(rep.path):
            fullpath = os.path.join(rep.path, elem)
            if os.path.isdir(fullpath):
                d = Dir(fullpath)
                rep.add(d)
                d.build()
            else:
                f = File(elem)
                rep.add(f)

    def to_json_object(self):
        root = {}
        root['icon'] = 'folder'
        root['display_count'] = 'True'
        root['count_tag'] = 'files and directories'
        root['type'] = 'Dir'
        for c in self.content:
            root[c.name] = c.to_json_object()
        return root

#-------------------------------------------------------------------------------
# Model for group
#-------------------------------------------------------------------------------

class User(Leaf):
    
    def to_json_object(self):
        root = {}
        root['icon'] = self.icon
        root['type'] = 'User'
        return root

class Group(Component):
    
    def __str__(self):
        return f"{self.name} ({self.count()} users)"
    
    def count(self):
        "Restrict counting to users and users of subgroup"
        c = 0
        for u in self.content:
            if issubclass(type(u), User):
                c += 1
            elif issubclass(type(u), Group):
                c += u.count()
        return c

    def build(self):
        os.system(f'net group {self.name} /domain > tmp')
        f = open('tmp', 'r')
        content = f.read()
        content = content.replace("La commande s'est termin‚e correctement.\n\n", '')
        f.close()
        os.remove('tmp')
        delimiter = '-------------------------------------------------------------------------------'
        index = content.find(delimiter)
        content = content[index+len(delimiter)+1:]
        users = []
        inside = False
        for c in content:
            if c not in [' ', '\t', '\n', '\r']:
                if not inside:
                    inside = True
                    word = c
                else:
                    word +=c
            else:
                if inside:
                    inside = False
                    users.append(word)
        for u in users:
            User(u, self, 'user')

    def to_json_object(self):
        root = {}
        root['icon'] = 'group'
        root['type'] = 'Group'
        root['display_count'] = 'True'
        root['count_tag'] = 'users'
        root['level_count'] = 1
        for c in self.content:
            root[c.name] = c.to_json_object()
        return root

#-------------------------------------------------------------------------------
# Model for machine & server
#-------------------------------------------------------------------------------

class Project(Component):
    pass

class Machine:
    
    def __init__(self, name, version, subtype):
        self.name = name
        self.version = version # string like '4.0.4'
        self.subtype = subtype # client or server
