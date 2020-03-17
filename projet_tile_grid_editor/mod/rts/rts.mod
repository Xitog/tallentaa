{
    "filetype" : "mod",
    "version" : 1.0,
    "name" : "RTS",
    "licence" : "?",
    "creator" : "?",
    "websites" : {
    },
    "layers" : {
        "ground"  : { "res" : "textures",   "default" : "grass", "apply" : "water",  "visible" : true, "icon" : "ground"  },
        "height"  : { "res" : "numbers_HL", "default" : 0,       "apply" : "one",    "visible" : false, "icon" : "height" },
        "area"    : { "res" : "numbers_BR", "default" : 0,       "apply" : "one",    "visible" : false, "icon" : "area"   },
        "object"  : { "res" : "objects",    "default" : 0,       "apply" : "heart",  "visible" : true, "icon" : "object"  }
    },
    "resources" : {
        "textures" : {
            "deep"  : { "val" : -2, "file" : "deep-1.png"  },
            "water" : { "val" : -1, "file" : "water-1.png" },
            "mud"   : { "val" :  0, "file" : "mud-1.png"   },
            "dry"   : { "val" :  1, "file" : "dry-1.png"   },
            "grass" : { "val" :  2, "file" : "grass-1.png" },
            "dark"  : { "val" :  3, "file" : "dark-1.png"  }
        },
        "objects" : {
            "heart"   : { "val" : 1, "file" : "heart.png"   },
            "goldkey" : { "val" : 2, "file" : "goldkey.png" }
        },
        "numbers_HL" : {
            "one"     : { "val" : 1, "file" : "num_hl_1.png" },
            "two"     : { "val" : 2, "file" : "num_hl_2.png" },
            "three"   : { "val" : 3, "file" : "num_hl_3.png" },
            "four"    : { "val" : 4, "file" : "num_hl_4.png" },
            "five"    : { "val" : 5, "file" : "num_hl_5.png" },
            "six"     : { "val" : 6, "file" : "num_hl_6.png" }
        },
        "numbers_BR" : {
            "one"     : { "val" : 1, "file" : "num_br_1.png" },
            "two"     : { "val" : 2, "file" : "num_br_2.png" },
            "three"   : { "val" : 3, "file" : "num_br_3.png" },
            "four"    : { "val" : 4, "file" : "num_br_4.png" },
            "five"    : { "val" : 5, "file" : "num_br_5.png" },
            "six"     : { "val" : 6, "file" : "num_br_6.png" }
        },
        "icons" : {
            "ground"  : { "val" : 1, "file" : "ground.png"  },
            "wall"    : { "val" : 2, "file" : "wall.png"    },
            "ceiling" : { "val" : 3, "file" : "ceiling.png" },
            "height"  : { "val" : 4, "file" : "height.png"  },
            "area"    : { "val" : 5, "file" : "area.png"    },
            "object"  : { "val" : 6, "file" : "object.png"  }
        }
    },
    "stakeholders" : {
        "Player 1": { "val" : 1, "color" : "blue"   },
        "Player 2": { "val" : 2, "color" : "red"    },
        "Player 3": { "val" : 3, "color" : "green"  },
        "Player 4": { "val" : 4, "color" : "yellow" }
    },
    "default_layer" : "ground",
    "has_transition" : true
}