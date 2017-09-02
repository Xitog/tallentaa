import xml.etree.ElementTree as et
import dg_tree

class XMLConverter:

    # Transform a et.Element to a tree of components
    def xml2component(self, elem : et.Element, parent=None, name=None, select_tags=[]):
        tag = elem.tag.replace('{http://www.polarsys.org/capella/core/modeller/0.8.0}', '')
        if tag not in select_tags:
            print('tag refused: ', elem.tag)
            return
        else:
            print('tag accepted: ', elem.tag)
        if name is None:
            name = elem.attrib['id']
        root = Component(name, parent)
        for k, v in elem.attrib.items():
            setattr(root, k, v)
        for child in elem:
            xml2component(child, root, select_tags=select_tags)
        return root

