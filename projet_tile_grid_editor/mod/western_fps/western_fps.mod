{
    "filetype" : "mod",
    "version" : 1.0,
    "name" : "Western FPS",
    "licence" : "Creative Commons Zero (CC0)",
    "creator" : "Created at Sparklin Labs by Pixel-boy",
    "websites" : {
        "Pixel-boy" : "https://twitter.com/2pblog1",
        "Sparklin Labs" : "https://sparklinlabs.itch.io/superpowers",
        "Superpowers" : "http://superpowers-html5.com/",
        "Github" : "https://github.com/sparklinlabs/superpowers-asset-packs"
    },
    "layers" : {
        "ground"  : { "res" : "textures",   "default" : "void", "apply" : "redbrick",  "visible" : true },
        "wall"    : { "res" : "textures",   "default" : 0,      "apply" : "greystone", "visible" : true  },
        "ceiling" : { "res" : "textures",   "default" : 0,      "apply" : "red",       "visible" : false },
        "height"  : { "res" : "numbers_HL", "default" : "one",  "apply" : "two",       "visible" : false },
        "area"    : { "res" : "numbers_BR", "default" : 0,      "apply" : "one",       "visible" : false },
        "object"  : { "res" : "objects",    "default" : 0,      "apply" : "ammo",      "visible" : true  }
    },
    "resources" : {
        "textures" : {
            "void"             : { "val" :  1, "file" : "0-placeholder.bmp"            },
            "greystone"        : { "val" :  2, "file" : "1-grey_stone_wall.bmp"        },
            "greystone1stone"  : { "val" :  3, "file" : "2-grey_stone_wall_stone.bmp"  },
            "lightstone"       : { "val" :  4, "file" : "3-light_stone_wall.bmp"       },
            "lightstone1stone" : { "val" :  5, "file" : "4-light_stone_wall_stone.bmp" },
            "lightstone2grass" : { "val" :  6, "file" : "5-light_stone_wall_grass.bmp" },
            "lightwood"        : { "val" :  7, "file" : "6-light_wood_wall.bmp"        },
            "lightwoodwindow"  : { "val" :  8, "file" : "7-light_wood_wall_window.bmp" },
            "darkwood"         : { "val" :  9, "file" : "8-dark_wood_wall.bmp"         },
            "redbrick"         : { "val" : 10, "file" : "9-red_brick_wall.bmp"         },
            "redbrick1light"   : { "val" : 11, "file" : "10-red_brick_wall_light.bmp"  },
            "redbrick2pillar"  : { "val" : 12, "file" : "11-red_brick_wall_pillar.bmp" },
            "redbrick3bars"    : { "val" : 13, "file" : "12-red_brick_wall_bars.bmp"   }
        },
        "objects" : {
            "ammo"       : { "val" :   1, "file" : "object-ammo.png"            },
            "burger"     : { "val" :   2, "file" : "object-burger.png"          },
            "goldkey"    : { "val" :   3, "file" : "object-key-gold.png"        },
            "silverkey"  : { "val" :   4, "file" : "object-key-silver.png"      },
            "heart"      : { "val" :   5, "file" : "object-heart.png"           },
            "start"      : { "val" :   6, "file" : "object-start.png"           },
            "coin"       : { "val" :   7, "file" : "object-coin.png"            },
            "gold-lingo" : { "val" :   8, "file" : "object-gold-lingo.png"      },
            "lantern"    : { "val" :   9, "file" : "object-lantern.png"         },
            "purse"      : { "val" :  10, "file" : "object-purse.png"           },
            "rose"       : { "val" :  11, "file" : "object-rose.png"            },
            "rubis"      : { "val" :  12, "file" : "object-rubis.png"           },
            "badge"      : { "val" :  13, "file" : "object-sheriff-badge.png"   },
            "knife"      : { "val" : 100, "file" : "object-weapon-knife.png"    },
            "pistol"     : { "val" : 101, "file" : "object-weapon-pistol.png"   },
            "shotgun"    : { "val" : 102, "file" : "object-weapon-shotgun.png"  },
            "rifle"      : { "val" : 103, "file" : "object-weapon-rifle.png"    },
            "chaingun"   : { "val" : 104, "file" : "object-weapon-chaingun.png" },
            "dynamite"   : { "val" : 105, "file" : "object-weapon-dynamite.png" }
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
            "ground"  : { "val" : 1, "file" : "layer-ground.png"  },
            "wall"    : { "val" : 2, "file" : "layer-wall.png"    },
            "ceiling" : { "val" : 3, "file" : "layer-ceiling.png" },
            "height"  : { "val" : 4, "file" : "layer-height.png"  },
            "area"    : { "val" : 5, "file" : "layer-area.png"    },
            "object"  : { "val" : 6, "file" : "layer-object.png"  }
        }
    },
    "default_layer" : "wall",
    "has_transition" : false
}