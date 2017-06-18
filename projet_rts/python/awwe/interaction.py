from engine import Colors, Engine
import os.path
import pygame
from typing import Type

#-------------------------------------------------------------------------------
# AUDIOHANDLER
#-------------------------------------------------------------------------------
class AudioHandler:
    
    def __init__(self, path="."):
        self.path = path
    
    def set_path(self, path):
        self.path = path
    
    def play(self, filename):
        pygame.mixer.music.load(os.path.join(self.path, filename))
        pygame.mixer.music.play()
    
    def pause(self):
        pygame.mixer.music.pause()
    
    def resume(self):
        pygame.mixer.music.unpause()

#-------------------------------------------------------------------------------
# INPUTHANDLER
#-------------------------------------------------------------------------------
class InputHandler:

    NORMAL = 0
    BUILD = 1
    
    def __init__(self, camera, scroll=5, auto_scroll_zone=10):
        self.camera = camera
        self.camera.handler = self
        self.world = camera.focus
        self.engine = camera.engine
        self.actor = camera.actor
        self.add_mod = False
        self.go_on = True
        self.mode = InputHandler.NORMAL
        # scrolling
        self.scroll = scroll
        self.auto_scroll_zone = auto_scroll_zone
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        # selection
        self.selected = []
        self.select = False
        self.select_x = 0
        self.select_y = 0
    
    def resume(self):
        self.go_on = True
    
    def handler(self, x, y, mx, my):
        for event in self.engine.get_events():
            if event.type == self.engine.QUIT:
                self.go_on = False
            elif event.type == self.engine.EventTypes.KEY_DOWN:
                if event.key == self.engine.Keys.ESCAPE:
                    self.go_on = False
                elif event.key in (self.engine.Keys.DOWN, 115):
                    self.down = True
                elif event.key in (self.engine.Keys.UP, 119):
                    self.up = True
                elif event.key in (self.engine.Keys.LEFT, 97):
                    self.left = True
                elif event.key in (self.engine.Keys.RIGHT, 100):
                    self.right = True
                elif event.key == self.engine.Keys.LSHIFT:
                    print('add_mod!')
                    self.add_mod = True
            elif event.type == self.engine.EventTypes.KEY_UP:
                if event.key in (self.engine.Keys.DOWN, 115):
                    self.down = False
                elif event.key in (self.engine.Keys.UP, 119):
                    self. up = False
                elif event.key in (self.engine.Keys.LEFT, 97):
                    self.left = False
                elif event.key in (self.engine.Keys.RIGHT, 100):
                    self.right = False
                elif event.key == self.engine.Keys.LSHIFT:
                    self.add_mod = False
                    print('stop add mod!')
                elif event.key == self.engine.Keys.CTRL_LEFT:
                    self.scroll += 1
                elif event.key == self.engine.Keys.CTRL_RIGHT:
                    self.scroll = max(self.scroll-1, 0)
                elif event.key == self.engine.Keys.SPACE:
                    self.GUI_display = not self.GUI_display
                elif event.key == self.engine.Keys.TAB:
                    self.camera.debug = not self.camera.debug
                else:
                    print("Unknown key: " + str(event.key))
            elif event.type == self.engine.EventTypes.MOUSE_BUTTON_DOWN:
                if event.button == 1:
                    if not self.select:
                        self.select = True
                        self.select_x = mx - x
                        self.select_y = my - y
            elif event.type == self.engine.EventTypes.MOUSE_BUTTON_UP:
                self.select = False
                if event.button == self.engine.Keys.MOUSE_LEFT:  # Left Button
                    if my > self.camera.GUI_interface_y:  # Interface click
                        pass
                    elif self.mode == InputHandler.NORMAL:
                        # print("%d %d %d %d" % (self.select_x // 32, self.select_y // 32, (mx - x) // 32, (my - y) // 32))
                        units = self.world.get_uni_rect(self.select_x // 32, self.select_y // 32, (mx - x) // 32, (my - y) // 32)
                        if not self.add_mod:
                            self.selected = []
                        if len(units) > 1:
                            for u in units:
                                if u.player == self.actor:
                                    if u not in self.selected:
                                        self.selected.append(u)
                        elif len(units) == 1:
                            if units[0].player == self.actor:
                                self.selected.append(units[0])
                            else:
                                if not self.add_mod:
                                    self.selected = units # on peut selectionner une et une seule unite ennemie
                elif event.button == self.engine.Keys.MOUSE_RIGHT:  # Right Button
                    if self.mode == InputHandler.BUILD:
                        self.mode = InputHandler.NORMAL
                    elif len(self.selected) == 1 and self.selected[0].player != self.actor:
                        print('1 select from other player : todo : display info')
                        pass
                    else:
                        print('button right')
                        cy = (my - y) // 32
                        cx = (mx - x) // 32
                        if self.world.is_valid_at(cx, cy):
                            unit = self.world.get_unit_at(cx, cy)
                            if unit is None:
                                self.world.game.order_move(self.selected, cx, cy, self.add_mod)
                            elif unit.player == self.player:
                                self.world.game.order_move(self.selected, cy, cx, self.add_mod)
                            else: # u.player != self.player:
                                self.world.game.order_attack(self.selected, unit, self.add_mod)
                                
    def update(self):

        mx, my = self.engine.get_mouse_pos()
        self.handler(self.camera.x, self.camera.y, mx, my)
        
        x = 0
        y = 0
        
        # Scroll on border with the mouse
        if self.left or mx < self.auto_scroll_zone:
            x = self.scroll
        if self.right or mx > self.camera.width - self.auto_scroll_zone:
            x = -self.scroll
        if self.down or my > self.camera.height - self.auto_scroll_zone:
            y = -self.scroll
        if self.up or my < self.auto_scroll_zone:
            y = self.scroll
        
        self.camera.move_coordinate(x, 0)
        self.camera.move_coordinate(0, y)
        
        return self.go_on

#-------------------------------------------------------------------------------
# CAMERA
#-------------------------------------------------------------------------------
class Camera:
    
    def __init__(self, width, height, focus=None, actor=None, engine=None, gui_inteface_y=480, base=32):
        self.width = width
        self.height = height
        self.size = width, height
        self.GUI_interface_y = gui_inteface_y
        self.GUI_display = True
        self.dev_mode = False
        self.ALLOW_BEYOND_MAP_SCROLLING = False
        self.NB_SQUARE_WIDTH = int(width/base)
        self.NB_SQUARE_HEIGHT = int(gui_inteface_y/base)
        self.x = 0
        self.y = 0
        self.SELECT_X = 0
        self.SELECT_Y = 0
        self.focus = focus
        self.actor = actor
        self.engine = engine
        self.BASE = base
        self.debug = False
        self.handler = None
    
    def is_valid_at(self, x, y):
        # Block scroll to the map
        if not self.ALLOW_BEYOND_MAP_SCROLLING and self.focus is not None:
            return (self.focus.width - self.NB_SQUARE_WIDTH) * -self.BASE < x <= 0 and (self.focus.height - self.NB_SQUARE_WIDTH) * -self.BASE < y <= 0
        else:
            return True
        
    def move_coordinate(self, x, y):
        if self.is_valid_at(x+self.x, y+self.y):
            self.x += x
            self.y += y
    
    def render(self):
        self.render_game()
        if self.GUI_display:
            self.render_gui()
    
    def render_game(self):
        first_square = (-self.x//32, -self.y//32)
        self.engine.fill(Colors.BLACK)
        # Ground
        for yy in range(first_square[1], min(first_square[1] + self.NB_SQUARE_HEIGHT + 4, self.actor.world.height)): # 4 = LARGEST SPRITE HEIGHT
            for xx in range(first_square[0], min(first_square[0] + self.NB_SQUARE_WIDTH + 3, self.actor.world.width)): # 3 = LARGET SPRITE WIDTH
                tex = self.focus.get_tex(xx, yy)
                pas = self.focus.get_pas(xx, yy)
                uni = self.focus.get_uni(xx, yy)
                dx = xx * 32 + self.x
                dy = yy * 32 + self.y
                # draw ground
                self.engine.tex(dx, dy, self.engine.textures[tex], 0)
                # draw passable
                if pas != 0:
                    self.engine.tex(dx, dy, self.engine.textures[102], 0.5)
                    
                    # self.engine.rect(dx, dy, 32, 32, Colors.RED, 1, 1)
                    #if pas != 0: # there is visible blocking doodad, 0 = passable, 99 = invisible and not passable
                    #    self.engine.tex(dx + self.engine.textures[pas].mod_x, dy + self.engine.textures[pas].mod_y, self.engine.textures[pas], 0.5)
                        
                # draw unit
                if uni != 0 and pas == 1:
                    self.engine.spr(uni.real_x + self.x -16, uni.real_y + self.y -16, self.engine.sprites["male"], 18, 10)
                # draw selected
                    if uni in self.handler.selected:
                        self.engine.tex(dx, dy, self.engine.textures[101], 0.5)
                # debug
                if self.debug:
                    pass
        # Cursor
        mx, my = self.engine.get_mouse_pos()
        if self.handler.mode == InputHandler.NORMAL:
            if self.handler.select:
                r = self.xrect(self.handler.select_x + self.x, self.handler.select_y + self.y, mx, my)
                self.engine.rect(r[0], r[1], r[2], r[3], Colors.GREEN, 1, 1)
    
    def render_gui(self):
        pass

    def xrect(self, x1, y1, x2, y2): # used only once
        tx = abs(x1 - x2) # add one?
        ty = abs(y1 - y2) # add one?
        if x1 > x2:
            rx = x2
        else:
            rx = x1
        if y1 > y2:
            ry = y2
        else:
            ry = y1
        return pygame.Rect(rx, ry, tx, ty)

#------------------------------------------------------------------------------
# Basic Textual Representation (BTR)
#------------------------------------------------------------------------------

import sys

def write(s):
    sys.stdout.write(str(s))

def writeln(s):
    sys.stdout.write(str(s) + "\n")

def newline():
    sys.stdout.write("\n")

#------------------------------------------------------------------------------
# TEXTCAMERA
#------------------------------------------------------------------------------
from map import Map, Layer

class TextCamera:
    
    def __init__(self, world: Type[Map], size):
        self.world = world
        self.size = size
        self.view = []
        for x in range(0, self.size):
            self.view.append([])
            for y in range(0, self.size):
                self.view[x].append(".")
    
    def render(self, raw=False):
        self.render_map(raw)
        write(" ")
        for y in range(0, self.size):
            write(f" {y:02d}")
        newline()
        for x in range(0, self.size):
            write(f"{x:02d} ")
            for y in range(0, self.size):
                write(self.view[y][x] + "  ") # invert view
            newline()
        
    def render_map(self, raw=False):
        """Output the map on the console."""
        print(f"== Map {self.world.name}")
        #for layer_key in self.world.layers:
        #    self.render_layer(self.world.layers[layer_key], raw)
        self.render_layer(self.world.layers["ground"], raw)
        
    def render_layer(self, layer: Type[Layer], raw=False):
        """Output a layer of the map on the console."""
        print(f"-- Layer {layer.get_name()}")
        for x in range(0, layer.width):
            for y in range(0, layer.height):
                val = layer.get_at(x, y)
                if raw:
                    self.view[x][y] = f"{val:04d}"
                else:
                    self.view[x][y] = self.render_tile(layer, val)
    
    def render_tile(self, layer, val):
        if layer.name == "ground":
            if val == 1000:
                return ','
            elif val == 2000:
                return '_'
            elif val == 0:
                return '~'
            elif val == Tiles.COAST:
                return '_'
            elif val == Tiles.WATER:
                return '~'
            else:
                return str(val)
        elif layer.name == "fog":
            if val == 0:
                return '~'
            else:
                return ' '
        else:
            return str(val)

    #from ctypes import * # cf colorama
    #STD_OUTPUT_HANDLE = -11
    #class COORD(Structure):
    #    pass
    #COORD._fields_ = [("X", c_short), ("Y", c_short)]
    #
    #def print_at(r, c, s):
    #    h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    #    windll.kernel32.SetConsoleCursorPosition(h, COORD(c, r))
    #    c = s.encode("windows-1252")
    #    windll.kernel32.WriteConsoleA(h, c_char_p(c),  len(c), None, None)
    #print_at(6, 3, "Hello") # 13h46 yes !
