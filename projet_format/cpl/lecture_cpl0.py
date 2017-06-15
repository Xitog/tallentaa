import xml.etree.ElementTree as ET
import os

#path = r"Z:\Workspaces\WS_empty\Empty"
#modeller = "Empty.melodymodeller"
#aird = "Empty.aird"
#target = path + os.sep + modeller

target = r"Z:\Workspaces\WS_simplest_model\Simplest\Simplest.melodymodeller"

tree = ET.parse(target)
root = tree.getroot()
ownedModelRoots = root.find("ownedModelRoots")

def find(e, criterium, value):
    for child in e:
        if criterium in child.attrib:
            if child.attrib[criterium] == value:
                return child

def display(e, what=None):
    for child in e:
        if what is None or isinstance(what, bool):
            if what:
                print(child.tag, child.attrib)
            else:
                print(child.tag)
        elif isinstance(what, list):
            print(child.tag)
            for a in what:
                print("\t" + child.attrib[a])
        elif isinstance(what, str):
            print(child.tag, child.attrib[what])
        else:
            Exception("Incorrect type for what: must be bool or list")

print('----------Root----------')
display(ownedModelRoots, "name")
print('---------Logical Architecture---------')
la = find(ownedModelRoots, "name", "Logical Architecture")
display(la)
print('-----------ownedDataPkg-----------')
la_data_pkg = la.find("ownedDataPkg")
display(la_data_pkg)
print('-------------------------')
la_data_pkgs = la_data_pkg.find("ownedDataPkgs")
display(la_data_pkgs)
print('-------------------------')

