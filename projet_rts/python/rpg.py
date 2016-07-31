__author__ = 'dgx'

from engine import Engine, Colors


def load_textures(engine):
    engine.set_texture_path('..\\..\\assets\\tiles64x32')
    engine.load_texture('cursor', 0, 'cursor_1.png')
    engine.load_texture('grass', 1, 'grass_1.png')
    engine.load_texture('tree', 100, 'tree_1.png')  # TODO : Center better the tree

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


def game_loop(engine):
    s_x = 0
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
        engine.tex(mx - 32, my - 16, engine.textures[0], 15)
        # imx = int((mx - 32 - 200) / 32 - s_x)
        # imy = int((my - 16 - 200) / 16)
        imy = int((((mx - 200 - s_x) / 32) - ((my - 200) / 16)) / 2)
        imx = int((my - 200) / 16 + imy)  # TODO : perfect it
        print(mx, my, imx, imy)
        # Background
        for i in range(0, 10):
            for j in range(0, 10):
                x = 200 + (j + i) * 32 + s_x
                y = 200 + (i - j) * 16
                engine.tex(x, y, engine.textures[1], 5)
                if debug:
                    engine.tex(x, y, engine.textures[0], 6)
                    engine.text(x + 32, y + 16, str(i) + ':' + str(j), Colors.YELLOW, 7, True, 10)
                if i == 4 and j == 4:
                    engine.tex(x, y, engine.textures[100], 10)
                if i == imx and j == imy:
                    engine.tex(x, y, engine.textures[0], 8)
                # print(x, y)
        engine.render()


if __name__ == '__main__':
    start()
