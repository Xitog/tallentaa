import pygame

from map import Map
from interaction import Camera, InputHandler, AudioHandler
from engine import Engine, Colors
from gui import Menu
from core import Game, Player, Mod, Army, Profile
from typing import Type

TEXTURE_PATH = r"..\..\..\assets\graphic\textures\plain_colors_32"
SPRITE_PATH = r"..\..\..\assets\graphic\sprites\lpc"
AUDIO_PATH = r"..\..\..\assets\audio\musics"
MAP_PATH = r"..\..\..\assets\map"

FutureWar = Mod("Future War", {
        "RedScum" : Army("Red Scum", {
            "barracks" : Profile("Barracks", 300, vision=3, width=2, height=3),
            "soldier" : Profile("Soldier", 50, vision=3),
            "heavy" : Profile("Heavy soldier", 80, vision=3)
        }),
        "BlueAngels": Army("Blue Angels", {
            "Defender" : Profile("Defender", 60, vision=3)
        }),
    }
)

def load_textures(engine: Type[Engine]):
    engine.set_texture_path(TEXTURE_PATH)
    engine.load_texture("darkness", -1, "black.png")
    engine.load_texture("water", 0, "blue.png")
    engine.load_texture("ford", 1, "light_blue.png")
    engine.load_texture("deep water", 2, "dark_blue.png")
    engine.load_texture("earth", 10, "brown.png")
    engine.load_texture("mud", 20, "dark_brown.png")
    engine.load_texture("grass", 30, "green.png")
    engine.load_texture("dark grass", 40, "dark_green.png")
    engine.load_texture("moutain", 50, "orange.png")
    engine.load_texture("rock", 60, "grey.png")
    engine.set_texture_path(SPRITE_PATH)
    engine.load_sprite("male", "male_walkcycle.png", -16, -32, 64, 64)

class Application:

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.fps = 30.0
        self.camera = None
        self.handler = None
        self.engine = None
        self.audio = None
    
    def set_caption(self):
        pygame.display.set_caption("RTS Project - {:.2f}".format(self.clock.get_fps()))
    
    def start(self):
        self.engine = Engine(800, 600)
        load_textures(self.engine)
        while True:
            r = self.menu_loop() 
            if not r:
                break
        self.engine.stop()
        print('Goodbye')  
    
    def menu_loop(self):
        m = Menu(self.engine)
        m.menu_start()
        while True:
            s = m.update()
            m.render()
            self.engine.render()
            if s['clicked'] is not None:
                break
        if s['clicked'] in ['Campaign', 'Skirmish']:
            game = Game('Test 1', FutureWar)
            worldmap = Map.from_csv("World map", "textures", MAP_PATH + r"\worldmap.csv")
            #worldmap = Map.from_csv("World map", "textures", MAP_PATH + r"\smallmap.csv")
            print("worldmap width = ", worldmap.width)
            print("worldmap height = ", worldmap.height)
            game.set_world(worldmap)
            player1 = Player(game, "Bob", "RedScum", Colors.GREEN, (0, 0))
            player2 = Player(game, "Hicks", "BlueAngels", Colors.BLUE, (4, 4))
            #plant = Building(Hicks, x=4, y=4, profile=FutureWar.get_profile("barracks"), constructed=1, plife=0.50)
            #s1 = Unit(Hicks, x=9, y=9, profile=FutureWar.get_profile("soldier"), plife=0.50)
            #TrainingGround.create_unit("Zoltan", "Defender", 4, 7)
            #writeln(f"plant life = {plant.life}")
            
            self.camera = Camera(800, 600, worldmap, player1, self.engine)
            self.handler = InputHandler(self.camera, auto_scroll_zone=-1)
            self.audio = AudioHandler(AUDIO_PATH)
            self.audio.play("ds.ogg")
            r = self.game_loop(game)
            return r
        elif s['clicked'] == 'Options':
            pass
        elif s['clicked'] == 'Quit':
            return False
    
    def in_game_menu_loop(self):
        m = Menu(self.engine)
        m.menu_pause()
        while True:
            s = m.update()
            m.render()
            self.engine.render()
            if s['clicked'] is not None: break
        if s['clicked'] == 'Options':
            pass
        else:
            return s['clicked']
       
    def game_loop(self, game): 
        start_time = pygame.time.get_ticks()
        self.clock.tick(self.fps)
        while True:
            res_gam = game.update()
            res_han = self.handler.update()
            self.camera.render()
            self.engine.render()
            self.clock.tick(self.fps)
            self.set_caption()
            if not res_han:
                self.audio.pause()
                r = self.in_game_menu_loop()
                if r != 'Resume':
                    break
                self.audio.resume()
                self.handler.resume()
            if not res_gam: 
                r = 'Game Finished'
                break
        if r in ('Game Finished', 'Quit'):
            print('Game has ended.')
            end_time = pygame.time.get_ticks()
            for p in game.get_players().values():
                if p.victorious:
                    print('\tPlayer ' + p.name + ' is victorious!')
                else:
                    print('\tPlayer ' + p.name + ' has been defeated.')
            print('\tMetal = ' + str(self.camera.actor.min))
            print('\tEnergy = ' + str(self.camera.actor.sol))
            print('Game has started at ' + str(start_time))
            print('Game had ended at ' + str(end_time))
            duration_milli_sec = end_time - start_time
            duration_sec = duration_milli_sec // 1000
            duration_min, duration_sec = divmod(duration_sec, 60)
            duration_hour, duration_min = divmod(duration_min, 60)
            print('Game duration: ' + str(duration_hour) + 'h' + str(duration_min) + 'm' + str(duration_sec) + 's')
            print('Press enter to quit.')
            return False
        elif r == 'Quit to main menu':
            return True

if __name__ == '__main__':
    import sys
    _maj, _min = sys.version_info[:2]
    print('Starting on Python ' + str(_maj) + "." + str(_min) + " with pygame " + pygame.version.ver)
    
    # No profiling
    Application().start()
    exit()

# import time
## import server
# import threading
# import queue

# g_queue = queue.Queue()

## g_server = server.Server("localhost", 2222, g_queue)

# def start_server():
    # g_server.start()
    
## g_server_thread = threading.Thread(target=start_server)
## g_server_thread.start()

# def update():
    # print("Update")
    # if not g_queue.empty():
        # while not g_queue.empty():
            # val = g_queue.get_nowait()
            # print("I got a value in the queue = ", val)

# def render():
    # pass #print("Affichage")

# def main_loop():
    # try:
        # start = time.time()
        # interval = 6
        # done = False
        # fps = 0
        # last_sec = 0
        # refresh = False
        # while not done:
            # elapsed = time.time() - start
            # if refresh:
                # last_sec = int(elapsed)
                # refresh = False
            ## print(elapsed)
            # if elapsed >= interval:
                # update()
                # start = time.time()
                ## fps count
                # refresh = True
            # render()
            ## fps count
            # if last_sec != int(elapsed): # one second has passed
                # last_sec = int(elapsed)
                # print("FPS = ", fps) # 300 avec un simple print, 1 500 000 sinon !
                # fps = 0
            # else:
                # fps += 1
    # except KeyboardInterrupt:
        # pass

# def render():
    # for lin in m:
        # for col in lin:
            # if len(col) == 1: sys.stdout.write(" " + col + "  ")
            # else: sys.stdout.write(" " + col + " ")
        # sys.stdout.write("\n")