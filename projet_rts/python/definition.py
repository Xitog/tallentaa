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
    124,
    125,
    126,
    127,
    128,
    129,
    130,
    131,
    132,
    133,
    134,
    135,
    136,
    137,
    138,
    139,
    140,
    141,
    142,
    143,
    144,
    145, 
    146,
    147,
    148, ]

GROUND_DATA = {
}

class Tile:
    def __init__(self, name):
        self.name = name
        self.tex = None

LAYER2_DATA = {
    1000 : Tile('coin_bas_droit1'),
    2000 : Tile('coin_bas_droit2'),
    3000 : Tile('coin1'),
    4000 : Tile('coin2'),
    5000 : Tile('coin3'),
    6000 : Tile('coin4'),
    7000 : Tile('coin5'),
    8000 : Tile('mur_bout1'),
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
    Texture('fin_mur1', tex=[[125]], passable=[[1]]),
    Texture('fin_mur2', tex=[[126]], passable=[[1]]),
    Texture('fin_mur3', tex=[[127]], passable=[[1]]),
    Texture('fin_mur4', tex=[[128]], passable=[[1]]),
    Texture('fin_mur5', tex=[[129]], passable=[[1]]),
    Texture('fin_mur6', tex=[[130]], passable=[[1]]),
    Texture('fin_mur7', tex=[[131]], passable=[[1]]),
    Texture('fin_mur8', tex=[[132]], passable=[[1]]),
    Texture('bidule_tipi', tex=[[133]], passable=[[1]]),
    Texture('sable_herbe1', tex=[[134]]),
    Texture('sable_herbe2', tex=[[135]]),
    Texture('sable_herbe3', tex=[[136]]),
    Texture('sable_herbe4', tex=[[137]]),
    Texture('sable_herbe5', tex=[[138]]),
    Texture('sable_herbe6', tex=[[139]]),
    Texture('sable_herbe7', tex=[[140]]),
    Texture('sable_herbe8', tex=[[141]]),
    Texture('sable_herbe9', tex=[[142]]),
    Texture('sable_herbe10', tex=[[143]]),
    Texture('sable_herbe11', tex=[[144]]),
    Texture('sable_herbe12', tex=[[145]]),
    Texture('sable_herbe13', tex=[[146]]),
    Texture('sable_herbe14', tex=[[147]]),
    Texture('sable_herbe15', tex=[[148]]),
]

#-----------------------------------------------------------------------
# Doodads
#-----------------------------------------------------------------------

class Doodad:
    def __init__(self, name_ico, name_tex=None, dev_x=0, dev_y=0, size_x=1, size_y=1):
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
    Doodad('speeder_ico', 'speeder', 0, 0, 2, 1),
    Doodad('coin_bas_droit1', 'coin_bas_droit1', 0, 0, 1, 1),
    Doodad('coin_bas_droit2', 'coin_bas_droit2', 0, 0, 1, 1),
    Doodad('coin_bas_gauche1'),
    Doodad('coin_bas_gauche2'),
    Doodad('coin_haut_droit'),
    Doodad('coin_haut_gauche'),
    Doodad('mur_bas1'),
    Doodad('mur_bas2'),
    Doodad('mur_bas3'),
    Doodad('mur_bas4'),
    Doodad('mur_droit1'),
    Doodad('mur_droit2'),
    Doodad('mur_gauche'),
    Doodad('mur_haut'),
]

class Use:
    def __init__(self, obj, x, y):
        self.obj = obj
        self.x = x
        self.y = y

#-----------------------------------------------------------------------
# Entities
#-----------------------------------------------------------------------

class Entity:
    def __init__(self, name_ico, name_tex=None, size_x=1, size_y=1, dev_x=0, dev_y=0):
        self.name_ico = name_ico
        self.name_tex = name_tex
        self.size_x = size_x
        self.size_y = size_y
        self.dev_x = dev_x
        self.dev_y = dev_y
        self.ico = None
        self.tex = None

ENTITIES = [
    Entity('900'), 
    Entity('904'), 
    Entity('908'), 
    Entity('912'), 
    Entity('916'), 
    Entity('920'), 
    Entity('924'), 
    Entity('928'), 
    Entity('932'), 
    Entity('936'), 
    Entity('940'), 
    Entity('944'), 
    Entity('948'), 
    Entity('952'), 
    Entity('956'), 
    Entity('tour_ico', 'tour', 1, 1, -32, -96), 
    Entity('bat1_ico', 'bat1', 2, 2),
]
