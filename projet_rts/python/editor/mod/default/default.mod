{
    "filetype": "mod",
    "version": 1.0,
    "name": "default",
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
            "res": "numbers",
            "default": "one",
            "apply": "two",
            "visible": false
        },
        "area": {
            "res": "numbers",
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
                "file": "heart.png"
            },
            "goldkey": {
                "val": 2,
                "file": "goldkey.png"
            }
        },
        "numbers": {
            "one": {
                "val": 1,
                "file": "one.png"
            },
            "two": {
                "val": 2,
                "file": "two.png"
            },
            "three": {
                "val": 3,
                "file": "three.png"
            },
            "four": {
                "val": 4,
                "file": "four.png"
            },
            "five": {
                "val": 5,
                "file": "five.png"
            }
        },
        "icons": {
            "ground": {
                "val": 1,
                "file": "ground.png"
            },
            "wall": {
                "val": 2,
                "file": "wall.png"
            },
            "ceiling": {
                "val": 3,
                "file": "ceiling.png"
            },
            "height": {
                "val": 4,
                "file": "height.png"
            },
            "area": {
                "val": 5,
                "file": "area.png"
            },
            "object": {
                "val": 6,
                "file": "object.png"
            }
        }
    },
    "default_layer": "wall"
}