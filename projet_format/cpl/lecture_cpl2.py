import xml.etree.ElementTree as ET
import sys

# on repart de cpl2 +on fusionne cpl0
# deux types éléments n'ont pas d'id, chacun ayant 1 exemple dans ce modèle : languages et bodies

class CapellaModel:

    def __init__(self, filepath):
        tree = ET.parse(filepath)
        self.root = tree.getroot()
        self.types = {}
        self.has_id = {}
        self.handlers = {}
        self.elements_by_id = {}
        self.elements_by_tag = {}
    
    def explore(self):
        #self.handlers["ownedClasses"] = CapellaModel.read_ownedClasses
        self.explore_element(self.root)
    
    def explore_element(self, element, level=0):
        # print(" " * level, element.tag)
        if element.tag not in self.types:
            self.types[element.tag] = 1
            self.elements_by_tag[element.tag] = [element]
            if "id" in element.attrib:
                self.has_id[element.tag] = True
                self.elements_by_id[element.attrib["id"]] = element
            else:
                self.has_id[element.tag] = False
        else:
            self.types[element.tag] += 1
            self.elements_by_tag[element.tag].append(element)
        children = list(element)
        for child in children:
            self.explore_element(child, level+1)
        #if child.tag in self.handlers:
        #    self.handlers[child.tag](self, child)
    
    def stats(self):
        ordered = sorted(self.types, key=self.types.__getitem__)
        ordered.reverse()
        for key in ordered:
            print(key, self.types[key], self.has_id[key])
    
    # Global search function (in all the model)
    def get_by_tag(self, tag):
        return self.elements_by_tag[tag]
    
    def create_classes(self):
        for elem_cls in self.elements_by_tag["ownedClasses"]:
            print("Class " + element.attrib["name"])
        #children = list(element)
        #for child in children:
        #    if child.tag == "ownedFeatures":
        #        self.read_ownedFeatures(child)
    
    def read_ownedFeatures(self, element):
        print("    Attribute " + element.attrib["name"])
    
    # Local search function (in an element)
    def find_by_tag(self, value):
        return self.find_children_by_tag(self.root, value)
    
    def find_children_by_tag(self, element, value):
        res = []
        for child in element:
            if child.tag == value:
                res.append(child)
        return res
    
    def find_by_attr(self, criterium, value):
        return self.find_children_by_attr(self.root, criterium, value)
    
    def find_children_by_attr(self, element, criterium, value):
        res = []
        for child in element:
            if criterium in child.attrib:
                if child.attrib[criterium] == value:
                    res.append(child)
        return res

def display_children(e, what=None):
    """
        If what is a str: display each child with the the value of the attribute for each child
        If what is a list not empty: display each child with the values of the attributes asked
        If what is a list empty: display each child with the values of ALL attributes
    """
    for child in e:
        if what is None or isinstance(what, bool):
            if what:
                print(child.tag, child.attrib)
            else:
                print("tag: " + child.tag)
        elif isinstance(what, list):
            print("tag: " + child.tag)
            if len(what) == 0:
                for a in child.attrib:
                    print("\tattr: " + a + " -> " + child.attrib[a])
            else:
                for a in what:
                    print("\tattr: " + a + " -> " + child.attrib[a])
        elif isinstance(what, str):
            print("tag: " + child.tag, what + " -> " + child.attrib[what])
        else:
            Exception("Incorrect type for what: must be bool or list")

filepath = r"D:\Workspaces\MA_404\MelodyTests\MA_404_WS_simplest_model\Simplest\Simplest.melodymodeller"
#filepath = r'D:\Workspaces\MA_412\MA_412_WS_local_1\EOLE_AF\EOLE_AF.melodymodeller'
cm = CapellaModel(filepath)
cm.explore()
cm.stats()
print()
print("Classes : " + str(len(cm.get_by_tag("ownedClasses"))))
for elem in cm.get_by_tag("ownedClasses"): print("Class " + elem.attrib["name"])
print()
print("Model Roots : " + str(len(cm.get_by_tag("ownedModelRoots"))))
for elem in cm.get_by_tag("ownedModelRoots"): print("System engineering " + elem.attrib["name"])
print()
print("Architectures : " + str(len(cm.get_by_tag("ownedArchitectures"))))
for elem in cm.get_by_tag("ownedArchitectures"): print("Level " + elem.attrib["name"])
print()
print("Data packages : " + str(len(cm.get_by_tag("ownedDataPkg"))))
for elem in cm.get_by_tag("ownedDataPkg"): print("Data package " + elem.attrib["name"])
print()

ownedModelRoots = cm.find_by_tag("ownedModelRoots")[0]
print('----------Children of Root----------')
display_children(ownedModelRoots, "name")
print('----------Attributes of the Children of Root----------')
display_children(ownedModelRoots, [])
print('----------Logical Architecture----------')
la = cm.find_children_by_attr(ownedModelRoots, "name", "Logical Architecture")[0]
display_children(la)
print('----------ownedDataPkg----------')
la_data_pkg = cm.find_children_by_tag(la, "ownedDataPkg")[0]
display_children(la_data_pkg)
print('----------ownedDataPkgs----------')
la_data_pkgs = cm.find_children_by_tag(la_data_pkg, "ownedDataPkgs")[0]
display_children(la_data_pkgs)
print('-----------------------------------')
