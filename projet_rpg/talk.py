strings = {
    1 : "Bonjour et bienvenue à Narion. Je suis Ramzel, bourgmestre de ce modeste village. Que puis-je faire pour vous... ?",
    2 : "Mon nom est #PLAYER_NAME#. Je cherche une auberge pour me reposer.",
    3 : "Peu importe mon nom. Je cherche une auberge pour me reposer.",
    4 : "[Menaçant] Dégage de là le péquenot !",
}

INTRO = 1
TYPE = 2
TYPE_CHOICE = 1
CHOICES = 3

dialog_tree = {
    1 : {
        INTRO : 1,
        TYPE : TYPE_CHOICE,
        CHOICES : [2, 3, 4],
    }
}

def print_dialog(d, dialog_tree, locuteur, interlocuteur):
    dialog = dialog_tree[d]
    print(interlocuteur.name + " : " + strings[dialog[INTRO]])
    if dialog[TYPE] == TYPE_CHOICE:
        nb = 1
        for alternative in dialog[CHOICES]:
            print(str(nb) + '. ' + strings[alternative].replace('#PLAYER_NAME#', locuteur.name))
            nb += 1
        choice = int(input('Entrer le chiffre correspondant à votre réponse : '))
        print('>>> ' + strings[dialog[CHOICES][choice-1]])
        
START = 1

class Obj:
    def __init__(self, name):
        self.name = name

print_dialog(START, dialog_tree, Obj("Bob"), Obj("Rosa"))
