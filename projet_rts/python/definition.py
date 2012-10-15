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
    115,
    116,
    117,
    118,
    119,
    120, ]

GROUND_DATA = {
}

#-----------------------------------------------------------------------

# Test TEXTURE
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
]
