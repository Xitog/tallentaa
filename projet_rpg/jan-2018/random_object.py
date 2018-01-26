import random
from datetime import datetime
random.seed(datetime.now())

# j'avais un truc pour faire des tableaux de random : de 0 à 5 => X, de 5 à 10 => Y.
# et j'avais vu que la bibliothèque base gérée ça !

object_type = {
    "Weapon": {
        "Sword" : {
            "Daguer" : {},
            "Sword" : {},
            "Bastard Sword" : {},
            "Two-handed Sword" : {},
            "Great Sword" : {},
        },
        "Haxe" : {
            "Haxe" : {},
            "Great Haxe" : {},
        },
        "Wand" : {
            "Wand" : {},
            "Staff" : {},
            "Great Staff" : {},
        },
        "Bow" : {
            "Bow" : {},
            "Great Bow" : {},
        },
    },
    "Ring" : {},
    "Mantle" : {},
    "Armor" : {
        "Cloak" : {},
        "Leather Armor" : {},
        "Brigandine" : {},
        "Coat of plates" : {},
        "Cuirass" : {},
        "Plate armour" : {},
    },
    "Scroll" : {},
    "Helmet" : {
        "Helmet" : {},
        "Bascinet" : {},
        "Sallet" : {},
        "Great helm" : {},
    },
}

modifiers = {
    "Sharp" : {
        "pos" : -1,
        "for" : ["Weapon"],
        "mod" : ["DOM", "10"]
    },
    "Renforced" : {
        "pos" : -1,
        "for" : ["Armor", "Helmet"],
        "mod" : ["DEF", "10"],
    },
    "pain" : {
        "pos" : 1,
        "for" : ["Weapon"],
        "mod" : ["DOM", "20"],
    },
}

def make_object(level):
    dico = object_type
    while type(dico) == dict and len(dico) > 0:
        typ = random.choice(list(dico))
        dico = dico[typ]
    #print(typ)
    mod = random.choice(list(modifiers))
    if modifiers[mod]["pos"] == -1:
        print(mod, typ)
    else:
        print(typ, "of", mod)

if __name__ == '__main__':
    make_object(7)

