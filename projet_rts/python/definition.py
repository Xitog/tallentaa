#-----------------------------------------------------------------------
# Explications
# GROUND_DEF est une liste listant les fichiers servant de textures de
# base. Ils sont charges dans GROUND_DATA, un dictionnaire ayant pour ID
# le chiffre dans GROUND_DEF et comme objet la surface chargee.
#
# FICHIER : "100.png" GROUND_DEF : [100] GROUND_DATA : {100:<Surface>}
# 
# TEXTURES est une liste des textures qui peuvent etre composees de un
# ou plusieurs fichiers (voir la matrice tex). Une texture ne sert qu'a
# deposer plus facilement des fichiers qui vont ensemble.
#
# Faire une texture :
#  - Preparer les differents fichiers + 1 fichier _ico
#  - Enregistrer le chiffre des fichiers dans GROUND_DEF
#  - Enregistrer l'assemblage dans TEXTURES (avec la matrice de passabilite)
#-----------------------------------------------------------------------

DIRECTORY = './media/textures/'
EXTENSION = '.png'

GROUND_DEF = [
    0,
    100, 
    101, 
    102, 
    103, 
    104, 
    105, 
    106, 
    107, 
    108, 
    109, 
    110, 
    111, 
    112, 
    113, 
    114,
    115, # dragon squelette
    116,
    117,
    118,
    119,
    120,
    121, # soucoupe
    122,
    123,
    124, ]

GROUND_DATA = {
}

#-----------------------------------------------------------------------
# Textures
#-----------------------------------------------------------------------

class Texture:
    def __init__(self, name, size_x=1, size_y=1, ico=None, tex=[[0]], passable=[[0]]): 
        self.name = name
        self.size_x = size_x
        self.size_y = size_y
        self.ico = ico
        self.tex = tex
        self.passable = passable
        self.content_ico = None


TEXTURES = [
    Texture('vide', tex=[[0]]),
    Texture('sable1', tex=[[100]]),
    Texture('sable2', tex=[[101]]),
    Texture('sable3', tex=[[102]]),
    Texture('sable4', tex=[[103]]),
    Texture('sable5', tex=[[104]]),
    Texture('trou_de_ver', tex=[[105]], passable=[[1]]),
    Texture('rocs1', tex=[[106]]),
    Texture('rocs2', tex=[[107]]),
    Texture('rocs3', tex=[[108]]),
    Texture('herbe1', tex=[[109]]),
    Texture('herbe2', tex=[[110]]),
    Texture('herbe3', tex=[[111]]),
    Texture('herbe4', tex=[[112]]),
    Texture('dalle1', tex=[[113]]),
    Texture('dalle2', tex=[[114]] ),
    Texture('squelette', 4, 2, '115_ico', [ [115, 117, 118, 0] ,
                                            [116, 0,   119, 120] ],
                                          [ [ 1, 1, 1, 0],
                                            [ 1, 0, 1, 1] ]),
    Texture('soucoupe', 2, 2, '121_ico', [ [121, 122],
                                           [123, 124] ],
                                         [ [1, 1],
                                           [1, 1] ]),
]

#-----------------------------------------------------------------------
# Doodads
#-----------------------------------------------------------------------

class Doodad:
    def __init__(self, name_ico, name_tex, dev_x, dev_y, size_x, size_y):
        self.name_ico = name_ico
        self.name_tex = name_tex
        self.dev_x = dev_x
        self.dev_y = dev_y
        self.size_x = size_x
        self.size_y = size_y
        self.ico = None
        self.tex = None

# icons
DOODADS = [
    Doodad('900', 'none', 0, 0, 1, 1),
    Doodad('tree1_ico', 'tree1', -48, -4*32, 1, 1),
    Doodad('tree2_ico', 'tree2', -48, -4*32, 1, 1),
    Doodad('tree3_ico', 'tree3', -48, -4*32, 1, 1),
]

#-----------------------------------------------------------------------
# Entities
#-----------------------------------------------------------------------

ENTITY_DATA = [ 
    '900', 
    '904', 
    '908', 
    '912', 
    '916', 
    '920', 
    '924', 
    '928', 
    '932', 
    '936', 
    '940', 
    '944', 
    '948', 
    '952', 
    '956', 
    'tour_ico', 
    'bat1_ico' 
]

class EntityDef:
    def __init__(self, graph):
        self.graph = graph

