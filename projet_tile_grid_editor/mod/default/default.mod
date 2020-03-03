{
    "filetype": "mod",
    "version": 1.0,
    "name": "Default",
    "licence": "Creative Commons Zero (CC0)",
    "creator": "Created by Damien Gouteux",
    "websites": {
        "Main": "https://xitog.github.io/dgx/"
    },
    "layers": {
        "ground": {
            "res": "textures",
            "default": "blue",
            "apply": "green",
            "visible": true
        },
        "wall": {
            "res": "textures",
            "default": 0,
            "apply": "black",
            "visible": true
        },
        "ceiling": {
            "res": "textures",
            "default": 0,
            "apply": "red",
            "visible": false
        },
        "height": {
            "res": "numbers_HL",
            "default": "one",
            "apply": "two",
            "visible": false
        },
        "area": {
            "res": "numbers_BR",
            "default": 0,
            "apply": "one",
            "visible": false
        },
        "object": {
            "res": "objects",
            "default": 0,
            "apply": "heart",
            "visible": true
        }
    },
    "resources": {
        "textures": {
            "black": {
                "val": 1,
                "file": "black.png"
            },
            "blue": {
                "val": 2,
                "file": "blue.png"
            },
            "green": {
                "val": 3,
                "file": "green.png"
            },
            "red": {
                "val": 4,
                "file": "red.png"
            }
        },
        "objects": {
            "heart": {
                "val": 1,
                "file": "object-heart.png"
            },
            "goldkey": {
                "val": 2,
                "file": "object-goldkey.png"
            }
        },
        "numbers_HL": {
            "one": {
                "val": 1,
                "file": "num_hl_1.png"
            },
            "two": {
                "val": 2,
                "file": "num_hl_2.png"
            },
            "three": {
                "val": 3,
                "file": "num_hl_3.png"
            },
            "four": {
                "val": 4,
                "file": "num_hl_4.png"
            },
            "five": {
                "val": 5,
                "file": "num_hl_5.png"
            },
            "six": {
                "val": 6,
                "file": "num_hl_6.png"
            }
        },
        "numbers_BR": {
            "one": {
                "val": 1,
                "file": "num_br_1.png"
            },
            "two": {
                "val": 2,
                "file": "num_br_2.png"
            },
            "three": {
                "val": 3,
                "file": "num_br_3.png"
            },
            "four": {
                "val": 4,
                "file": "num_br_4.png"
            },
            "five": {
                "val": 5,
                "file": "num_br_5.png"
            },
            "six": {
                "val": 6,
                "file": "num_br_6.png"
            }
        },
        "icons": {
            "ground": {
                "val": 1,
                "file": "layer-ground.png"
            },
            "wall": {
                "val": 2,
                "file": "layer-wall.png"
            },
            "ceiling": {
                "val": 3,
                "file": "layer-ceiling.png"
            },
            "height": {
                "val": 4,
                "file": "layer-height.png"
            },
            "area": {
                "val": 5,
                "file": "layer-area.png"
            },
            "object": {
                "val": 6,
                "file": "layer-object.png"
            }
        }
    },
    "default_layer": "wall",
    "has_transition": true
}