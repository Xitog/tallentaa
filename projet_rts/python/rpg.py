__author__ = 'dgx'

from engine import Texture, Engine, Colors


def load_textures(engine):
    engine.textures = {
        1: Texture('rock', 1, 'grass_1.png', Colors.MINI_MAP_GREEN_HALF, False),
    }


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
    while True:
        # Update + Event
        for event in engine.get_events():
            if event.type == engine.QUIT:
                return False
        # Render
        engine.text(100, 100, "Mini flare 0.1", Colors.YELLOW, 40)
        for i in range(0, 10):
            for j in range(0, 10):
                x = 200 + (j + i) * 32
                y = 200 + (i - j) * 16
                engine.tex(x, y, engine.textures[1].img, 5)
                print(x, y)
        engine.render()


if __name__ == '__main__':
    start()

