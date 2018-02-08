__author__ = 'dgx'

# 7/2/18 : I make it work with new awwe architecture
# It's in 64x32 iso

from engine import Engine, Colors
from map import Map, Layer
from utils import Pair


def load_textures(engine):
    engine.set_texture_path(r'..\..\..\assets\graphic\textures\flare_textures_iso')
    engine.load_texture('cursor_1', 1000, 'cursor_1.png')
    engine.load_texture('cursor_2', 1001, 'cursor_2.png')
    engine.load_texture('grass', 0, 'grass_1.png')
    engine.load_texture('rock', 10, 'rock_1.png', 0, -16)
    engine.load_texture('rock', 100, 'rock_1.png', 0, -16)
    #engine.load_texture('tree', 100, 'tree_1.png')  # TODO : Center better the tree

    # engine.textures = {
    #    0: Texture('cursor', 0, 'cursor_1.png', Colors.MINI_MAP_BLUE, False),
    #    1: Texture('grass', 1, 'grass_1.png', Colors.MINI_MAP_GREEN_HALF, False),
    #    100: Texture('tree', 100, 'tree_1.png', Colors.MINI_MAP_BROWN, False),
    # }


def start():
    e = Engine(800, 600)
    load_textures(e)
    while True:
        r = game_loop(e)
        if not r:
            break
    e.stop()
    print('Goodbye')

s_x = 0
start_x = 0
start_y = 200


def matrix_to_screen(i, j):
    global s_x, start_x, start_y
    x = start_x + (j + i) * 32 + s_x
    y = start_y + (i - j) * 16
    return x, y


def screen_to_matrix(x, y):
    global s_x
    x = x - s_x + 32 - start_x
    y = y + 16 - start_y
    x = int(x / 32)
    y = int(y / 16)
    return x, y


def game_loop(engine):
    global s_x, start_x, start_y
    xmap = Map("pipo", 10, 10, {"ground" : Layer("ground", 10, 10, 0)})
    #xmap.set_layer()
    xmap.set_at("ground", 5, 5, 1)
    debug = False
    while True:
        # Update + Event
        for event in engine.get_events():
            if event.type == engine.QUIT:
                return False
            elif event.type == engine.EventTypes.KEY_DOWN:
                if event.key == engine.Keys.LEFT:
                    s_x += 5
                elif event.key == engine.Keys.RIGHT:
                    s_x -= 5
            elif event.type == engine.EventTypes.KEY_UP:
                if event.key == engine.Keys.TAB:
                    debug = not debug
        # Render
        engine.rect(0, 0, 800, 600, Colors.BLACK, 0, 0)
        engine.text(100, 100, "Mini flare 0.1", Colors.YELLOW, 40)
        # Cursor
        mx, my = engine.get_mouse_pos()
        # engine.tex(mx, my, engine.textures[1001], 1000)
        # imx = int((mx - 32 - 200) / 32 - s_x)
        # imy = int((my - 16 - 200) / 16)
        imy = int((((mx - start_x - s_x) / 32) - ((my - start_y) / 16)) / 2)
        imx = int((my - start_y) / 16 + imy)  # TODO : perfect it
        r = screen_to_matrix(mx, my)
        print(mx, my, imx, imy, r[0], r[1])
        # Background
        cpt = 0
        for i in range(0, xmap.width):
            for j in range(0, xmap.height):
                x, y = matrix_to_screen(i, j)
                t = xmap.get_at("ground", i, j)
                engine.tex(x, y, engine.textures[0], 5)
                if t == 1:
                    engine.tex(x, y, engine.textures[10], 10)
                if debug:
                    engine.tex(x, y, engine.textures[1000], 1000)
                    engine.text(x + 32, y + 16, str(i) + ':' + str(j) + ':' + str(cpt), Colors.YELLOW, 1000, True, 10)
                if i == 4 and j == 4:
                    engine.tex(x, y, engine.textures[100], 50)
                if i == imx and j == imy:
                    engine.tex(x, y, engine.textures[1001], 1000)
                # print(x, y)
                cpt += 1
        engine.render()


if __name__ == '__main__':
    start()
