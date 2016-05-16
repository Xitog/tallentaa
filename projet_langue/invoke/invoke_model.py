
class RootCollection:

    def __init__(self):
        self.roots = {} # indexed by the root
        self.letters = {}
        self.reverse = {} # verb base => verb base
        self.reverse_letters = {}
    
    def add_root(self, root, irregular, base, **forms):
        if len(root.split(' ')) > 1:
            raise Exception("This is not a root")
        elif root not in self.roots:
            neo_root = Root(root, irregular, base)
            neo_root.forms.update(forms)
            self.roots[root] = neo_root
            if neo_root.first_letter not in self.letters:
                self.letters[neo_root.first_letter] = [neo_root]
            else:
                self.letters[neo_root.first_letter].append(neo_root)
        else:
            self.roots[root].add_verb(base)
        return self.roots[root].get_verb(base)

        
    def get_roots_by_first_letter(self):
        return self.letters
        
    
    def get_roots(self):
        return self.roots
        

    def build_reverse(self):
        for root_key, root in self.roots.items():
            for verb_key, verb in root.get_all_verbs().items():
                for trans_key, trans in verb.get_all_trans().items():
                    if trans_key not in self.reverse:
                        self.reverse[trans_key] = [trans]
                    else:
                        self.reverse[trans_key].append(trans)
                    if trans[0] not in self.reverse_letters:
                        self.reverse_letters[trans[0]] = { trans : [verb] } # { 'd' : { 'desirer' : [V:want, V:wish] } }
                    else:
                        if trans in self.reverse_letters[trans[0]]:
                            self.reverse_letters[trans[0]][trans].append(verb)
                        else:
                            self.reverse_letters[trans[0]][trans] = [verb]


    def get_reverse_by_first_letter(self):
        return self.reverse_letters


class Root:

    def __init__(self, root, irregular, base=None):
        self.root = root
        self.first_letter = root[0]
        self.forms = {}
        self.verbs = {} # indexed by the base of the verb
        if base is not None:
            self.verbs[base] = Verb(self, base)
        self.irregular = irregular
    
    def add_form(self, key, value):
        if key in self.forms:
            raise Exception("This form already exists")
        self.forms[key] = value

        
    def add_verb(self, base):
        if base in self.verbs:
            raise Exception("This verb already exists : " + verb + " for root " + self.root)
        else:
            self.verbs[base] = Verb(self, base)

    
    def get_verb(self, base):
        if base not in self.verbs:
            raise Exception("Base unknown : " + base + " for root " + self.root)
        else:
            return self.verbs[base]

    
    def get_all_verbs(self):
        return self.verbs
    

class Verb:

    def __init__(self, root, base):
        self.root = root
        self.base = base
        self.translations = {} # indexed by ? for now key = value

    
    def add_translation(self, target):
        if target in self.translations:
            raise Exception("This translation already exists : " + target + " for verb " + self.base)
        else:
            self.translations[target] = target


    def get_all_trans(self):
        return self.translations
        
