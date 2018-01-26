
# 12h18 ok

class Talker:

    def __init__(self, name):
        self.name = name


class DialogTree:

    Choice = 1
    EndOfDialog = 2

    ALL = {}

    @staticmethod
    def from_file(path):
        f = open(path, 'r', encoding='utf-8')
        lines = f.readlines()
        d = None
        nbline = 1
        levels = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for line in lines:
            level = line.count('    ')
            line = line.strip()
            if line[0] == '[':
                idd = int(line[1:line.index(']')])
                msg = line[line.index(':')+2:]
                typ = DialogTree.Choice
                if msg.find(" EOD") != -1:
                    msg = msg.replace(" EOD", "")
                    typ = DialogTree.EndOfDialog
                msg_i = add_or_get(msg)
                levels[level] = DialogTree.add_or_check(idd, typ, msg_i)
            elif line[0] == '?':
                msg, idd = line.split(' -> ')
                msg = msg[3:].strip()
                #print('    L' + str(nbline) + ' ajout au dialogue ', levels[level-1].idd, 'de', idd)
                levels[level-1].add((int(idd), add_or_get(msg)))
            nbline += 1
    
    @staticmethod
    def add_or_check(idd, typ, msg_i):
        if idd not in DialogTree.ALL:
            #print("Création d'un dialogue :", idd)
            d = DialogTree(idd, typ, msg_i)
        else:
            #print("Référence d'un dialogue :", idd)
            d = DialogTree.ALL[idd]
            if d.idd != idd or d.typ != typ or d.msg != msg_i:
                raise Exception("Incoherent Referenced Dialog")
        return d
    
    @staticmethod
    def start(idd, talker = None, interlocutor = None):
        if idd not in DialogTree.ALL:
            raise Exception("Unique identifier invalid: " + str(idd))
        else:
            d = DialogTree.ALL[idd]
            d.talker = talker
            d.interlocutor = interlocutor
            return d
    
    def __init__(self, idd, typ, msg=None, nodes=None):
        self.talker = None
        self.interlocutor = None
        self.idd = idd
        self.typ = typ
        self.msg = msg
        self.nodes = nodes if nodes is not None else []
        if self.idd in DialogTree.ALL:
            raise Exception("Unique identifier is not unique: " + str(idd))
        DialogTree.ALL[self.idd] = self
    
    def add(self, node):
        self.nodes.append(node)
    
    def get_msg(self, msg_i):
        msg = Localisation.DATA[msg_i]
        if self.talker is not None:
            msg = msg.replace('#PLAYER_NAME#', self.talker.name)
        return msg
    
    def __str__(self):
        s = self.get_msg(self.msg) + "\n"
        if self.typ == DialogTree.Choice:
            i = 1
            for node in self.nodes:
                s += "    " + str(i) + ". " + self.get_msg(node[1]) + "\n"
                i += 1
        return s

    def get_answer(self, nb):
        return self.nodes[nb-1][0]

    def __eq__(self, other):
        tst = (self.typ == other.typ and self.msg == other.msg and len(self.nodes) == len(other.nodes))
        if not tst:
            return False
        else:
            for i in range(0, len(self.nodes)):
                if DialogTree.ALL[self.nodes[i][0]] != DialogTree.ALL[other.nodes[i][0]] or self.nodes[i][1] != other.nodes[i][1]:
                    return False
        return True

def add_or_get(msg):
    if msg in Localisation.DATA.values():
        msg_i = get_id(msg)
    else:
        msg_i = add_msg(msg)
    return msg_i

def get_id(msg):
    for key, val in Localisation.DATA.items():
        if val == msg:
            return key
    return msg

def add_msg(msg):
    mx = len(Localisation.DATA)
    Localisation.DATA[mx+1] = msg
    return mx+1

class Localisation:
    
    DATA = {
        1 : "Bonjour étranger ! Vous semblez un peu perdu, puis-je vous aider ?",
        2 : "Dégage, manant !",
        3 : "Oui, mon nom est #PLAYER_NAME# et je cherche Jaïna.",
        4 : "Pourriez-vous m'indiquer un marchand ?",
        5 : "Jaïna se trouve à l'auberge du Cheval blanc, là-bas à côté de la rivière.",
        6 : "Merci, au revoir !",
        7 : "Imbécile !",
        8 : "Igor pourra vous vendre des armes et des potions. Il est au centre du village.",
        9 : "Au revoir étranger !",
        10: "Je cherche Jaïna également."
    }

# Old from a previous attempt
#    -1 : "Taper sur entrée pour continuer.",
#    -2 : "Taper sur entrée pour mettre fin au dialogue.",
#    1 : "Bonjour et bienvenue à Narion. Je suis Ramzel, bourgmestre de ce modeste village. Que puis-je faire pour vous... ?",
#    2 : "Mon nom est #PLAYER_NAME#. Je cherche une auberge pour me reposer.",
#    3 : "Peu importe mon nom. Je cherche une auberge pour me reposer.",
#    4 : "[Menaçant] Dégage de là le péquenot !",
#    5 : "L'épée scintillante est juste sur ma droite #PLAYER_NAME#. Elle offre une nourriture et un lit corrects pour les aventuriers fourbus.",
#    6 : "Très bien mystérieux aventurier. L'épée scintillante est juste sur ma droite, j'espère qu'elle vous conviendra.",
#    7 : "Si vous le prenez ainsi. Adieu.",
#    8 : "Merci l'ami.",
#    9 : "De rien. N'hésitez pas à revenir vers moi si le besoin s'en fait sentir.",
#    10 : "Merci.",
    
DialogTree(1000, DialogTree.Choice, 1, [(1001, 2), (1002, 3), (1003, 4)])
DialogTree(1001, DialogTree.EndOfDialog, 7)
DialogTree(1002, DialogTree.Choice, 5, [(1004, 6), (1005, 4)])
DialogTree(1003, DialogTree.Choice, 8, [(1006, 10), (1004, 6)])
DialogTree(1004, DialogTree.EndOfDialog, 9)
DialogTree(1005, DialogTree.Choice, 8, [(1004, 6)])
DialogTree(1006, DialogTree.Choice, 5, [(1004, 6)])

class DialogExplorer:

    def __init__(self, start):
        while start is not None:
            d = DialogTree.start(start, Talker("Bob"), Talker("Sarah"))
            print("Dialog[" + str(d.idd) + "]", sep='')
            print('>>>', d, end='')
            if d.typ == DialogTree.Choice:
                start = d.get_answer(int(input('Votre choix : ')))
            elif d.typ == DialogTree.EndOfDialog:
                print('End of Dialog')
                start = None

class DialogDumper:

    def __init__(self, start):
        self.explore(start)

    def explore(self, start, level=0):
        #print("    " * level + "EXPLORE", start, level)
        d = DialogTree.start(start)
        #print("    " * level + "Dialog[" + str(d.idd) + "]", sep='')
        #print("    " * level + '>>>', d, end='')
        print("    " * level + "[" + str(d.idd) + "] : " + Localisation.DATA[d.msg], sep='', end='')
        if level > 15:
            raise Exception("Too many level of dialog")
        if d.typ == DialogTree.EndOfDialog:
            print(" EOD")
            if len(d.nodes) > 0:
                s = f"Incoherent dialog: EndOfDialog with children nodes: {d.idd}\n"
                for n in d.nodes:
                    s += f" ({n[0]}, {n[1]})"
                raise Exception(s)
        else:
            print()
        for n in d.nodes:
            print("    " * (level + 1) + "? [" + Localisation.DATA[n[1]] + ' -> ' + str(n[0]), sep='')
            self.explore(n[0], level+2)
        
if __name__ == "__main__":
    DialogExplorer(1000)
    DialogDumper(1000)
    DialogTree.from_file('dialog_test.txt')
    DialogDumper(6000)
    print(DialogTree.ALL[1000] == DialogTree.ALL[6000])
    
