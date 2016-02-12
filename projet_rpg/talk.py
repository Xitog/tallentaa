strings = {
    -1 : "Taper sur entrée pour continuer.",
    -2 : "Taper sur entrée pour mettre fin au dialogue.",
    1 : "Bonjour et bienvenue à Narion. Je suis Ramzel, bourgmestre de ce modeste village. Que puis-je faire pour vous... ?",
    2 : "Mon nom est #PLAYER_NAME#. Je cherche une auberge pour me reposer.",
    3 : "Peu importe mon nom. Je cherche une auberge pour me reposer.",
    4 : "[Menaçant] Dégage de là le péquenot !",
    5 : "L'épée scintillante est juste sur ma droite #PLAYER_NAME#. Elle offre une nourriture et un lit corrects pour les aventuriers fourbus.",
    6 : "Très bien mystérieux aventurier. L'épée scintillante est juste sur ma droite, j'espère qu'elle vous conviendra.",
    7 : "Si vous le prenez ainsi. Adieu.",
    8 : "Merci l'ami.",
    9 : "De rien. N'hésitez pas à revenir vers moi si le besoin s'en fait sentir.",
    10 : "Merci.",
}

STR_CONTINUE = -1
STR_END = -2

INTRO = 1
TYPE = 2
TYPE_CHOICE = 1
TYPE_ANSWER = 2
TYPE_END = 3
CHOICES_ANSWER = 3
CHOICES_SUITE = 4
ANSWER = 5
SUITE = 6

dialog_tree = {
    1 : {
        INTRO : 1,
        TYPE : TYPE_CHOICE,
        CHOICES_ANSWER : [2, 3, 4],
        CHOICES_SUITE : [2, 4]
    },
    2 : {
        INTRO : 5,
        TYPE : TYPE_ANSWER,
        ANSWER : 8,
        SUITE : 3,
    },
    3 : {
        INTRO : 9,
        TYPE : TYPE_END,
    },
    4 : {
        INTRO : 6,
        TYPE : TYPE_ANSWER,
        ANSWER : 10,
        SUITE : 5,
    },
    5 : {
        INTRO : 9,
        TYPE : TYPE_END,
    }
}

def resolve_tag(s, locuteur, interlocuteur=None):
    s = s.replace('#PLAYER_NAME#', locuteur.name)
    return s

def do_dialog(d, dialog_tree, locuteur, interlocuteur=None):
    print()
    dialog = dialog_tree[d]
    if interlocuteur is not None:
        print(interlocuteur.name + " : " + resolve_tag(strings[dialog[INTRO]], locuteur))
    else:
        print(resolve_tag(strings[dialog[INTRO]]))
    print()
    if dialog[TYPE] == TYPE_CHOICE:
        nb = 1
        for alternative in dialog[CHOICES_ANSWER]:
            print('[' + str(nb) + ']. ' + resolve_tag(strings[alternative], locuteur))
            nb += 1
        print()
        choice = int(input('Entrer le chiffre correspondant à votre réponse : '))
        #print('>>> ' + resolve_tag(strings[dialog[CHOICES][choice-1]], locuteur))
        do_dialog(dialog[CHOICES_SUITE][choice-1], dialog_tree, locuteur, interlocuteur)
    elif dialog[TYPE] == TYPE_ANSWER:
        print(resolve_tag(strings[dialog[ANSWER]], locuteur))
        print()
        input(strings[STR_CONTINUE])
        do_dialog(dialog[SUITE], dialog_tree, locuteur, interlocuteur)
    elif dialog[TYPE] == TYPE_END:
        input(strings[STR_END])
    else:
        raise Exception("Dialog type unknown")

START = 1

class Obj:
    def __init__(self, name):
        self.name = name

do_dialog(START, dialog_tree, Obj("Bob"), Obj("Rosa"))
