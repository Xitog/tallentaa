
class Base:
    def __init__(self, def_file='definitions.txt', link_file='links.txt'):
        self.defs = open(def_file).readlines()
        self.links = open(link_file).readlines()
        #print(len(self.defs))
        #print(len(self.links))
        # Make entities
        self.ents = {}
        for d in self.defs:
            self.ents.update({d.split(',')[0] : Entity(d)})
        # Make Links
        for line in self.links:
            l = line.split('.')
            left = l[0]
            right = l[1].rstrip()
            self.ents[left].links.append(right)
            self.ents[right].links.append(left)
    
    def p_entities(self):
        for e in self.ents:
            print("%s == %s" % (e, ents[e].default))
    
    def p_base(self):
        for e in self.ents:
            self.ents[e].info()

class Entity:
    def __init__(self, infos, links=[]):
        self.default = infos.split(',')[0]
        self.infos = infos
        self.links = links[:]
    
    def info(self):
        print("Entity %s" % (self.default,))
        for l in self.links:
            print("  Linked to %s" % (l,))

b = Base()
b.p_base()

