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
            "res": "int",
            "default": 0,
            "apply": 1,
            "visible": false
        },
        "area": {
            "res": "int",
            "default": 0,
            "apply": 1,
            "visible": false
        },
        "object": {
            "res": "objects",
            "default": 0,
            "apply": "circle",
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
            "circle": {
                "val": 1,
                "file": "circle.png"
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
    "default_layer": "wall",
    "buttons": "textures"
}