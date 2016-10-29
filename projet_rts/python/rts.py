#! /usr/bin/env python

__version__ = "$Revision: 1 $"

# http://ezide.com/games/code_examples/example.py
# http://pygame.org/docs/ref/draw.html#pygame.draw.rect

# div X and Y by 32 + math.trunc -> give the square where we are
# multiply by 32 -> give where we start to display

import math
from engine import *
from game import Pair


def load_textures(engine):
    engine.set_texture_path('..\\..\\assets\\tiles32x32')
    engine.load_texture('rock', 1, 'rock_brown.png')  # Colors.MINI_MAP_BROWN_DARK, False
    engine.load_texture('tree', 25, '25_arbre_1.png', -32, -96)  # Colors.MINI_MAP_GREEN_DARK, False
    engine.load_texture('tree', 26, '26_arbre_2.png', -32, -64)  # Colors.MINI_MAP_GREEN_DARK, False
    # Real textures
    engine.load_texture('grass', 100, 'grass_two_leaves.png')  # Colors.MINI_MAP_GREEN_LIGHT
    engine.load_texture('ground', 200, 'ground.png')  # Colors.MINI_MAP_BROWN
    engine.load_texture('water', 300, 'water0.png')  # Colors.MINI_MAP_BLUE_LIGHT, False),
    engine.load_texture('w1', 9100, 'w1.png')  # Colors.MINI_MAP_BLUE_LIGHT, False
    engine.load_texture('w2', 9200, 'w2.png')  # Colors.MINI_MAP_BLUE_LIGHT, False
    engine.load_texture('w3', 9300, 'w3.png')  # Colors.MINI_MAP_BLUE_LIGHT, False
    engine.load_texture('w4', 9400, 'w4.png')  # Colors.MINI_MAP_BLUE_LIGHT, False
    engine.load_texture('w5', 9500, 'w5.png')  # Colors.MINI_MAP_BLUE_LIGHT, False
    engine.load_texture('w6', 9600, 'w6.png')  # Colors.MINI_MAP_BLUE_LIGHT, False
    engine.load_texture('w7', 9700, 'w7.png')  # Colors.MINI_MAP_BLUE_LIGHT, False
    engine.load_texture('w8', 9800, 'w8.png')  # Colors.MINI_MAP_BLUE_LIGHT, False
    engine.load_texture('water741', 8100, 'water741.png')  # Colors.MINI_MAP_BLUE_LIGHT, False
    engine.load_texture('x2', 8200, 'x2.png')  # Colors.MINI_MAP_BLUE_LIGHT, False
    engine.load_texture('x24', 8300, 'x24.png')  # Colors.MINI_MAP_BLUE_LIGHT, False
    engine.load_texture('x4', 8400, 'x4.png')  # Colors.MINI_MAP_BLUE_LIGHT, False
    engine.load_texture('water85', 8500, 'water85.png')  # Colors.MINI_MAP_BLUE_LIGHT, False
    engine.load_texture('water325', 8700, 'water325.png')  # Colors.MINI_MAP_BLUE_LIGHT, False
    engine.load_texture('water981', 8900, 'water981.png')  # Colors.MINI_MAP_BLUE_LIGHT, False
    # Brou & Black
    surf_brou = pygame.Surface((32, 32))
    surf_brou.set_alpha(200, pygame.RLEACCEL)
    surf_brou.fill((32, 32, 32, 128))
    engine.load_texture('brou', 10000, surf_brou)  # Colors.MINI_MAP_FOG, False
    surf_black = pygame.Surface((32, 32))
    surf_black.set_alpha(255, pygame.RLEACCEL)
    surf_black.fill((0, 0, 0, 255))
    engine.load_texture('black', 11111, surf_black)  # Colors.MINI_MAP_BLACK, False
    # Unit
    engine.set_texture_path('..\\..\\assets\\buildings\\')
    engine.load_texture('turret', 20001, 'cc3by_five_archers_turret_base.png')  # Colors.MINI_MAP_BLUE, False),
    engine.set_texture_path('..\\..\\assets\\32x32\\entities\\')
    engine.load_texture('skeleton_face', 50001, 'skeleton_face.png', -16, -48)

    # Computed textures
    # 1300 : Texture('grass_water_lm', 1200, 'grass_water_ml.png', MINI_MAP_BLUE_LIGHT, False),
    # minimap color depends !!!

    # 91 : Texture('w1', 91, 'w1.png', MINI_MAP_GREEN_LIGHT, False),
    # 92 : Texture('w2', 92, 'w2.png', MINI_MAP_GREEN_LIGHT, False),
    # 93 : Texture('w3', 93, 'w3.png', MINI_MAP_GREEN_LIGHT, False),
    # 94 : Texture('w4', 94, 'w4.png', MINI_MAP_GREEN_LIGHT, False),
    # 95 : Texture('w5', 95, 'w5.png', MINI_MAP_GREEN_LIGHT, False),
    # 96 : Texture('w6', 96, 'w6.png', MINI_MAP_GREEN_LIGHT, False),
    # 97 : Texture('w7', 97, 'w7.png', MINI_MAP_GREEN_LIGHT, False),
    # 98 : Texture('w8', 98, 'w8.png', MINI_MAP_GREEN_LIGHT, False),

    # Mixing Texture
    for a in [9100, 9200, 9300, 9400, 9500, 9600, 9700, 9800, 8100, 8200, 8300, 8400, 8500, 8700, 8900]:
        for b in [100]:
            s = pygame.Surface((32, 32))
            s.blit(engine.textures[b].surf, (0, 0))
            s.blit(engine.textures[a].surf, (0, 0))
            if a > 9000:
                n = b*10+a-9000
            else:
                n = b*10+1000+a-8000
            engine.load_texture(str(n), n, s)  # engine.textures[a].mini, engine.textures[a].passable


class CameraStorm:
    pass


class Camera:
    
    def __init__(self, engine, width, height, scroll, player):
        self.engine = engine
        self.screen = self.engine.screen
        self.width = width
        self.height = height
        self.size = width, height
        self.scroll = scroll
        self.player = player
        self.auto_scroll_zone = 10
        self.game = player.game
        self.x = 0
        self.y = 0
        self.SELECT_X = 0
        self.SELECT_Y = 0
        self.SELECT_R = False
        self.GUI_interface_y = 480
        self.GUI_mini_map_x = 22 * 32
        self.GUI_display = True
        self.selected = []
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.add_mod = False
        self.mode = 'normal'  # or build
        self.build_type = None
        self.build_size = None
        self.not_enough_ress = 0
        self.dev_mode = False
        self.ALLOW_BEYOND_MAP_SCROLLING = False
        self.NB_SQUARE_WIDTH = 25
        self.NB_SQUARE_HEIGHT = 15


    def select_zone(self, x, y, w, h):  # , player)
        x //= 32
        y //= 32
        w //= 32
        h //= 32
        ul = []
        if x == w and y == h:  # a square
            u = self.player.world.get_unit_at(x, y)
            if u is not None:
                ul.append(u)
        else:  # a zone
            for i in range(x, w):
                for j in range(y, h):
                    # print(i, j, self.player.world.unit_map[j][i])
                    u = self.player.world.get_unit_at(i, j)
                    # print(u)
                    if u is not None:
                        ul.append(u)
        # DEBUG
        # for u in ul:
        #    print(u)
        return ul

    def x2r(self, x):
        return x * 32 + self.x + 16

    def y2r(self, y):
        return y * 32 + self.y + 16

    def update(self):
        
        mx, my = self.engine.get_mouse_pos()
        
        for event in self.engine.get_events():
            if event.type == self.engine.QUIT:
                return False
            elif event.type == self.engine.EventTypes.KEY_DOWN:
                if event.key == self.engine.Keys.ESCAPE:
                    return False
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
                elif event.key == self.engine.Keys.SPACE:
                    self.scroll += 1
                elif event.key == self.engine.Keys.B:
                    if self.mode == 'normal':
                        self.mode = 'build'
                        self.build_type = self.player.game.building_types_ordered[0]
                        self.build_size = Pair(2, 1)
                    else:
                        self.mode = 'normal'
                    # print(self.mode)
                elif event.key == self.engine.Keys.TAB:
                    self.GUI_display = not self.GUI_display
                    # print(self.GUI_display)
                elif event.key == self.engine.Keys.RETURN:
                    self.dev_mode = not self.dev_mode
                    # print(self.dev_mode)
                else:
                    print(event.key)
            elif event.type == self.engine.EventTypes.MOUSE_BUTTON_DOWN:
                if event.button == 1:
                    if not self.SELECT_R:
                        self.SELECT_R = True
                        self.SELECT_X = mx - self.x
                        self.SELECT_Y = my - self.y
            elif event.type == self.engine.EventTypes.MOUSE_BUTTON_UP:
                self.SELECT_R = False
                if event.button == self.engine.Keys.MOUSE_LEFT:  # Left Button
                    # print(self.SELECT_Y, self.GUI_interface_y)
                    if my > self.GUI_interface_y:  # Interface click
                        # if self.mode == 'normal':
                        # CLICK FOR A BUILDING
                        # pour voir si on n'a pas "ripé" sur un bouton de construction ou la minimap
                        if self.SELECT_Y > self.GUI_interface_y:
                            a = mx // 32
                            b = (my-self.GUI_interface_y) // 32
                            # print(a,b)
                            nb = a + b * 3
                            if 0 <= nb < len(self.player.game.building_types_ordered):
                                btn = self.player.game.building_types_ordered[nb]
                                bt = self.player.game.building_types[btn]
                                self.mode = 'build'
                                self.build_type = btn
                                self.build_size = Pair(bt.grid_w, bt.grid_h)
                            if mx > self.GUI_mini_map_x:  # Mini map click
                                a = int((mx - self.GUI_mini_map_x) / 3)
                                b = int((my - self.GUI_interface_y) / 3)
                                if a < self.player.world.size32.x and b < self.player.world.size32.y:
                                    # print("self x, y old", self.x, self.y)
                                    # print("minimap", a, b)
                                    self.x = -a * 32 + 384  # 12 * 32 (pour 800 px)
                                    self.y = -b * 32 + 224 + 24  #  9 * 32 + 24 (600%32) (pour 600px) TODO: make generic
                                    # print("self x, y new", self.x, self.y)
                    elif self.mode == 'normal':
                        deb_x = min(self.SELECT_X, mx - self.x)
                        fin_x = max(self.SELECT_X, mx - self.x)
                        deb_y = min(self.SELECT_Y, my - self.y)
                        fin_y = max(self.SELECT_Y, my - self.y)
                        ul = self.select_zone(deb_x, deb_y, fin_x, fin_y)
                        if not self.add_mod:
                            self.selected = []
                        if len(ul) > 1:
                            for u in ul:
                                if u.player == self.player:
                                    if u not in self.selected:
                                        self.selected.append(u)
                        elif len(ul) == 1:
                            if ul[0].player == self.player:
                                self.selected.append(ul[0])
                            else:
                                if not self.add_mod:
                                    self.selected = ul # on peut selectionner une et une seule unite ennemie
                    elif self.mode == 'build':
                        # repeated code in render
                        xx = (mx - self.x) // 32
                        yy = (my - self.y) // 32
                        # center the thing
                        cw = self.build_size.x // 2
                        ch = self.build_size.y // 2
                        # test if ok
                        v = self.player.world.is_empty_zone(xx-cw, yy-ch, self.build_size.x, self.build_size.y)
                        if v:
                            # Final Building Here
                            bt = self.player.game.building_types[self.build_type]
                            if self.player.min >= bt.cost[0] and self.player.sol >= bt.cost[1]:
                                self.player.min -= bt.cost[0]
                                self.player.sol -= bt.cost[1]
                                self.player.game.create_building(self.player.name, xx-cw, yy-ch, self.build_type)
                            else:
                                self.not_enough_ress = 10
                        if not self.add_mod: # multiple construction orders
                            self.mode = 'normal'
                elif event.button == self.engine.Keys.MOUSE_RIGHT:  # Right Button
                    if self.mode == 'build':
                        self.mode = 'normal'
                    elif len(self.selected) == 1 and self.selected[0].player != self.player:
                        print('1 select from other player : todo : display info')
                        pass
                    else:
                        print('button right')
                        cy = (my - self.y) // 32
                        cx = (mx - self.x) // 32
                        if self.player.world.is_valid(cx, cy):
                            u = self.player.world.get_unit_at(cx, cy)
                            if u is None:
                                self.game.order_move(self.selected, cx, cy, self.add_mod)
                            elif u.player == self.player:
                                self.game.order_move(self.selected, cy, cx, self.add_mod)
                            else: # u.player != self.player:
                                self.game.order_attack(self.selected, u, self.add_mod)
                elif event.button == 2:  # Middle Button
                    print('button 3')

        # Scroll on border with the mouse
        if self.left or mx < self.auto_scroll_zone:
            self.x += self.scroll
        if self.right or mx > self.width - self.auto_scroll_zone:
            self.x -= self.scroll
        if self.down or my > self.height - self.auto_scroll_zone:
            self.y -= self.scroll
        if self.up or my < self.auto_scroll_zone:
            self.y += self.scroll
        # Block scroll to the map
        if not self.ALLOW_BEYOND_MAP_SCROLLING:
            if self.x > 0:
                self.x = 0
            elif self.x < -(self.player.world.size32.x - self.NB_SQUARE_WIDTH) * 32:
                self.x = -(self.player.world.size32.x - self.NB_SQUARE_WIDTH) * 32
            if self.y > 0:
                self.y = 0
            elif self.y < -(self.player.world.size32.y - self.NB_SQUARE_HEIGHT) * 32:
                self.y = -(self.player.world.size32.y - self.NB_SQUARE_HEIGHT) * 32

        return True

    def render(self):
        self.render_game()
        if self.GUI_display:
            self.render_gui()

    def render_game(self):
        mx, my = pygame.mouse.get_pos()  # repeat from main_loop
        first_square = (-self.x//32, -self.y//32)
        self.screen.fill(Colors.BLACK.value)

        # Sol
        # for yy in range(0, self.player.world.size32.y):
        for yy in range(first_square[1], min(first_square[1] + self.NB_SQUARE_HEIGHT + 4, self.player.world.size32.y)): # 4 = LARGEST SPRITE HEIGHT
            for xx in range(first_square[0], min(first_square[0] + self.NB_SQUARE_WIDTH + 3, self.player.world.size32.x)): # 3 = LARGET SPRITE WIDTH
                t = self.player.world.world_map[yy][xx]
                d = self.player.world.passable_map[yy][xx]
                dx = xx * 32 + self.x
                dy = yy * 32 + self.y
                # draw terrain
                self.engine.tex(dx, dy, self.engine.textures[t], 0)
                if d != 0 and d != 99:  # there is visible blocking doodad, 0 = passable, 99 = invisible and not passable
                    self.engine.tex(dx + self.engine.textures[d].mod_x, dy + self.engine.textures[d].mod_y, self.engine.textures[d], 0.5)
                    if self.dev_mode:
                        self.engine.rect(dx, dy, 32, 32, Colors.RED, 1, 1)
                # draw unit
                su = self.player.world.unit_map[yy][xx]
                if su == 0:
                    pass  # Empty
                elif su[0] in (-1, 1):  # en mouvement, carreau reserve ou en position
                    if su[0] == -1:
                        self.engine.rect(dx + 1, dy + 1, 31, 31, Colors.HALF_RED, 1, 1)
                    elif su[0] == 1:  # en position
                        self.engine.rect(dx + 1, dy + 1, 31, 31, Colors.HALF_BLUE, 1, 1)
                    u = su[1]
                    if u in self.selected:
                        if len(u.orders) > 0:
                            lx = u.real_x + self.x
                            ly = u.real_y + self.y
                            for o in u.orders:
                                if o.kind == 'go':
                                    self.engine.circle(self.x2r(o.x), self.y2r(o.y), 5, Colors.GREEN, 0, 1)
                                    self.engine.line(lx, ly, self.x2r(o.x), self.y2r(o.y), Colors.GREEN, 1, 1)
                                    lx = self.x2r(o.x)
                                    ly = self.y2r(o.y)
                                elif o.kind == 'attack':
                                    #pygame.draw.circle(self.screen, RED, (o.target.x*32+16 + self.x, o.target.y*32+16 + self.y), 5, 0)
                                    self.engine.line(lx, ly, self.x2r(o.target.x), self.y2r(o.target.y), Colors.RED, 1, 1)
                                    lx = self.x2r(o.target.x)
                                    ly = self.y2r(o.target.y)
                        self.engine.circle(u.real_x + self.x, u.real_y + self.y, u.size, u.player.color, 0, 1)
                        if u.player == self.player:
                            self.engine.circle(u.real_x + self.x, u.real_y + self.y, u.size+3, Colors.GREEN, 2, 1)
                            self.engine.tex(u.real_x + self.x, u.real_y + self.y, self.engine.textures[50001], 3)
                        else:
                            self.engine.circle(u.real_x + self.x, u.real_y + self.y, u.size+3, Colors.RED, 2, 1)
                            self.engine.tex(u.real_x + self.x, u.real_y + self.y, self.engine.textures[50001], 3)
                    else:
                        self.engine.circle(u.real_x + self.x, u.real_y + self.y, u.size, u.player.color, 0, 1)
                        self.engine.tex(u.real_x + self.x, u.real_y + self.y, self.engine.textures[50001], 3)
                elif su[0] == 2:  # Building
                    u = su[1]
                    self.engine.tex(u.x * 32 + self.x, u.y * 32 + self.y, self.engine.textures[20001], 2)
                    #if xx == u.grid_x and yy == u.grid_y:
                    #    self.engine.rect(dx, dy, u.type.grid_w * 32, u.type.grid_h * 32, u.player.color, 0, 2)
                    if u in self.selected:
                        self.engine.rect(u.x * 32 + self.x, u.y * 32 + self.y, u.type.grid_w * 32, u.type.grid_h * 32, Colors.GREEN, 2, 2)
                # draw fog or black
                fog = self.player.fog_map[yy][xx]
                if fog == 0:
                    self.engine.tex(dx, dy, self.engine.textures[11111], 10)
                elif fog == 1:
                    self.engine.tex(dx, dy, self.engine.textures[10000], 10)
                # DEBUG
                if self.dev_mode:
                    self.engine.text(dx, dy, "%(v)04d" % {"v": self.player.world.debug_map[yy][xx]}, Colors.RED, 1)
                
        # Cursor
        if self.mode == 'normal':
            if self.SELECT_R:
                r = xrect(self.SELECT_X + self.x, self.SELECT_Y + self.y, mx, my)
                self.engine.rect(r[0], r[1], r[2], r[3], Colors.WHITE, 1, 1)
        elif self.mode == 'build':
            xx = (mx - self.x) // 32
            yy = (my - self.y) // 32
            # center the thing
            cw = self.build_size.x // 2
            ch = self.build_size.y // 2
            # test if ok
            v = self.player.world.is_empty_zone(xx-cw, yy-ch, self.build_size.x, self.build_size.y)
            if v:
                c = Colors.GREEN
            else:
                c = Colors.RED
            self.engine.rect((xx-cw)*32+self.x, (yy-ch)*32+self.y, self.build_size.x*32, self.build_size.y*32, c, 0, 1)
        
        # Particles
        for p in self.player.world.particles.core:
            if p.kind == 'blue sphere':
                #print('Particle at ', p.x + self.x, ', ', p.y + self.y, ' aiming at ', p.tx, ', ', p.ty, ' ttl=', p.ttl)
                self.engine.circle(int(p.x + self.x), int(p.y + self.y), 3, Colors.BLUE, 0, 3)
    
    def render_gui(self):
        # Background
        self.engine.rect(0, self.GUI_interface_y, self.width-1, 200, Colors.GREY, 0, 40) # fond
        self.engine.line(0, self.GUI_interface_y, self.width-1, self.GUI_interface_y, Colors.BLUE, 1, 50)
        for xx in range(0, 3):
            for yy in range(0, 3):
                self.engine.rect(xx * 32, yy * 32 + self.GUI_interface_y, 32, 32, Colors.BLUE, 1, 50)
        self.engine.line(self.GUI_mini_map_x - 1, self.GUI_interface_y, self.GUI_mini_map_x - 1, self.GUI_interface_y + 96, Colors.BLUE, 1, 40)
        self.engine.line(self.GUI_mini_map_x - 1, self.GUI_interface_y + 96, self.width-1, self.GUI_interface_y + 96, Colors.BLUE, 1, 40)
        
        # Build menu
        xs = 8
        ys = self.GUI_interface_y + 8
        for btn in self.player.game.building_types_ordered:
            bt = self.player.game.building_types[btn]
            self.engine.text(xs, ys, bt.name[0:3], Colors.YELLOW, 40)
            xs += 32
            if xs > 72:
                xs = 8
                ys += 32
        
        # Metal (min) & Energie (sol)
        min = int(self.player.min)
        sol = int(self.player.sol)
        if self.not_enough_ress > 0:
            text = "M : %(min)04d E : %(sol)04d NOT ENOUGH RESSOURCES!" % {"min" : min, "sol" : sol}
            col = Colors.RED
            self.not_enough_ress -= 1
        else:
            text = "M : %(min)04d E : %(sol)04d" % {"min" : min, "sol" : sol}
            col = Colors.YELLOW
        self.engine.text(5, self.GUI_interface_y+104, text, col, 50)
        
        # Mini map
        for yy in range(0, self.player.world.size32.y):
            for xx in range(0, self.player.world.size32.x):
                t = self.player.world.world_map[yy][xx]
                d = self.player.world.passable_map[yy][xx]
                if d != 0 and d != 99:
                    self.engine.rect(xx * 3 + self.GUI_mini_map_x, yy * 3 + self.GUI_interface_y +1, 3, 3, self.game.textures_info[d].mini, 0, 50)
                else:
                   self.engine.rect(xx * 3 + self.GUI_mini_map_x, yy * 3 + self.GUI_interface_y +1, 3, 3, self.game.textures_info[t].mini, 0, 50)
                u = self.player.world.unit_map[yy][xx]
                if u != 0:
                    if u[0] == 1 or u[0] == 2:
                        self.engine.rect(xx * 3 + self.GUI_mini_map_x, yy * 3 + self.GUI_interface_y +1, 3, 3, u[1].player.color, 0, 50)
                fog = self.player.fog_map[yy][xx]
                if fog == 0:
                    self.engine.rect(xx * 3 + self.GUI_mini_map_x, yy * 3 + self.GUI_interface_y +1, 3, 3, self.game.textures_info[11111].mini, 0, 50)
                elif fog == 1:
                    self.engine.rect(xx * 3 + self.GUI_mini_map_x, yy * 3 + self.GUI_interface_y +1, 3, 3, self.game.textures_info[10000].mini, 0, 50)


class Particles:
    
    def __init__(self):
        self.core = []

    def add(self, p):
        self.core.append(p)

    def update(self):
        i = 0
        #saved = []
        while i < len(self.core):
            ttl = self.core[i].update()
            if ttl <= 0:
                del self.core[i]
                #print(ttl, len(self.core))
            else:
                i += 1
                #print(ttl, len(self.core))


class Particle:
    
    def __init__(self, kind, parent, target, speed, damage, guided=True):
        print(parent.x, parent.y)
        self.kind = kind
        self.x = parent.x  * 32 + 16
        self.y = parent.y  * 32 + 16
        self.speed = speed
        self.damage = damage
        self.target = target
        self.guided = guided
        self.tx = self.target.x * 32 + 16
        self.ty = self.target.y * 32 + 16
        self.ttl = 100
    
    def update(self):
        
        self.ttl -= 1
        
        if self.guided:
            self.tx = self.target.x * 32 + 16
            self.ty = self.target.y * 32 + 16
        
        a = -get_angle(self.x, self.y, self.tx, self.ty)
        #print(self.x, ', ', self.y, ' to ', self.tx, ', ', self.ty, ' with angle of ', a, ' cos : ', math.cos(a), ' sin : ', math.sin(a))
        #input()
        
        self.x += math.cos(a) * self.speed
        self.y += -math.sin(a) * self.speed
        
        if self.target.hit(self.x, self.y):
            ttl = 0
            self.target.life -= self.damage
            print('Touché : ', self.target, self.target.life)
            return ttl
        
        return self.ttl


# unit_map can be : 0 : void, (1, u) : unit u is here, (-1, u) : unit u is moving here
class World:
    
    def __init__(self, game, world_map, textures_info):
        self.game = game
        self.particles = Particles()
        if len(world_map) == 0:
            raise Exception("Empty map detected")
        self.size32 = Pair(len(world_map[0]), len(world_map))
        self.unit_map = World.create_map(self.size32.x, self.size32.y, 0)
        self.world_map = World.create_map(self.size32.x, self.size32.y, 0)
        self.passable_map = World.create_map(self.size32.x, self.size32.y, 0)
        self.debug_map = World.create_map(self.size32.x, self.size32.y, 0)
        # separate [128] => 100 (in world map) + 28 (in passable_map or 99
        # if texture not passable by default (and no doodad can be put on it))
        for yy in range(0, self.size32.y):
            for xx in range(0, self.size32.x):
                r = world_map[yy][xx]
                self.world_map[yy][xx] = (r // 100) * 100
        
        for yy in range(0, self.size32.y):
            for xx in range(0, self.size32.x):
                r = world_map[yy][xx]  # 101, 228, 312
                self.passable_map[yy][xx] = r % 100
                r = self.world_map[yy][xx]  # 100, 200, 300
                if not self.game.textures_info[r].passable:  # TODO: we need the texture info only here
                    self.passable_map[yy][xx] = 99
        
        # Computation of passage from tex to tex
        world_map2 = World.create_map(self.size32.x, self.size32.y, 0)
        for yy in range(0, self.size32.y):
            for xx in range(0, self.size32.x):
                r = self.world_map[yy][xx]
                
                # On travaille en base 2 sur 8 positions (de 0 à 7)
                b0 = 1
                b1 = 2
                b2 = 4
                b3 = 8
                b4 = 16
                b5 = 32
                b6 = 64
                b7 = 128
                sum = 0
                
                # On commence en haut à gauche, puis on tourne dans le sens horaire
                # 1 = différent 0 = égal (2 = bord : non, cela revient à pas de différence !)
                # ligne du haut
                if yy > 1 and xx > 1:
                    if self.world_map[yy-1][xx-1] != r:
                        sum += 1 * b0 # sinon 0*b0 donc rien
                if xx > 1:
                    if self.world_map[yy][xx-1] != r:
                        sum += 1 * b1
                if yy < self.size32.y - 1 and xx > 1:
                    if self.world_map[yy+1][xx-1] != r:
                        sum += 1 * b2
                # ligne du milieu, gauche
                if yy < self.size32.y - 1:
                    if self.world_map[yy+1][xx] != r:
                        sum += 1 * b3
                # ligne du bas, en partant de la gauche
                if yy < self.size32.y - 1 and xx < self.size32.x - 1:
                    if self.world_map[yy+1][xx+1] != r:
                        sum += 1 * b4
                if xx < self.size32.x - 1:
                    if self.world_map[yy][xx+1] != r:
                        sum += 1 * b5
                if yy > 1 and xx < self.size32.x - 1:
                    if self.world_map[yy-1][xx+1] != r:
                        sum += 1 * b6
                # ligne du milieu, droit
                if yy > 1:
                    if self.world_map[yy-1][xx] != r:
                        sum += 1 * b7
                
                self.debug_map[yy][xx] = sum
                
                world_map2[yy][xx] = self.world_map[yy][xx]
                if r == 300 and sum != 0: # 0 = eau au milieu
                    # coin
                    if sum == 199 or sum == 135 or sum == 131: # coin haut gauche
                        world_map2[yy][xx] = 1100
                    elif sum == 241 or sum == 240: # coin haut droit
                        world_map2[yy][xx] = 1300
                    elif sum == 124 or sum == 56 or sum == 120: # coin bas droit
                        world_map2[yy][xx] = 1500
                    elif sum == 31 or sum == 15: # coin bas gauche
                        world_map2[yy][xx] = 1700
                    # milieu
                    elif sum == 193: #2920: # milieu haut
                        world_map2[yy][xx] = 1200
                    elif sum == 112 or sum == 48: #3240: # milieu droit
                        world_map2[yy][xx] = 1400
                        #print('modified! at', yy, xx, 'to', world_map2[yy][xx])
                    elif sum == 28: #120: # milieu bas
                        world_map2[yy][xx] = 1600
                    elif sum == 7 or sum == 3: #2200: # milieu gauche
                        world_map2[yy][xx] = 1800
                    # les coins bizarres, entre deux diag /
                    elif sum == 1:
                        world_map2[yy][xx] = 2200
                    elif sum == 16:
                        world_map2[yy][xx] = 2400
                    elif sum == 17:
                        world_map2[yy][xx] = 2300
                    elif sum == 19:
                        world_map2[yy][xx] = 2500
                    elif sum == 49:
                        world_map2[yy][xx] = 2700
                    elif sum == 100:
                        world_map2[yy][xx] = 2900
                    elif sum == 70:
                        world_map2[yy][xx] = 2100
                    else:
                        print("unidentified transition for texture :", sum, "at", xx, ":", yy)
                
                # if xx < self.size32.x - 1:
                    # r_middle_right = world_map[xx+1][yy]
                    # if r_middle_right != r:
                        # if r_middle_right == 300:
                            ## self.world_map[xx][yy] = 1300
                            # self.passable_map[xx][yy] = 98
                # if xx > 1:
                    # r_middle_left = world_map[xx-1][yy]
                    # if r_middle_left != r:
                        # if r_middle_left == 300:
                            # self.passable_map[xx][yy] = 94
                # if yy > 1:
                    # r_top_center = world_map[xx][yy-1]
                    # if r_top_center != r:
                        # if r_top_center == 300:
                            # self.passable_map[xx][yy] = 96 # why?
                # if yy < self.size32.y - 1:
                    # r_bottom_center = world_map[xx][yy+1]
                    # if r_bottom_center != r:
                        # if r_bottom_center == 300:
                            # self.passable_map[xx][yy] = 92 #why?
        
        self.world_map = world_map2
        self.units = []
    
    def is_valid(self, x, y):
        return 0 <= x < self.size32.x and 0 <= y < self.size32.y

    def is_valid_zone(self, x, y, w, h):
        if 0 <= x < self.size32.x and 0 <= y < self.size32.y:
            if x + w < self.size32.x and y + h <= self.size32.y:
                return True
        return False
    
    def is_empty_zone(self, x, y, w, h):
        if not self.is_valid_zone(x, y, w, h):
            return False
        else:
            for i in range(x, x+w):
                for j in range(y, y+h):
                    if self.passable_map[j][i] != 0 and self.unit_map[j][i] != 0:
                        return False
            return True
    
    def is_empty(self, x, y):  # no unit, no blocking terrain
        return self.passable_map[y][x] == 0 and self.unit_map[y][x] == 0
    
    def is_unit(self, x, y):
        return self.unit_map[y][x] != 0 and self.unit_map[y][x][0] != -1  # 1 (unit) or 2 (building)
    
    def get_unit_at(self, x, y):
        if 0 <= x < self.size32.x and 0 <= y < self.size32.y:
            su = self.unit_map[y][x]
            if su != 0 and su[0] != -1:
                return su[1]
    
    @staticmethod
    def create_map(lines, columns, value):
        content = []
        for i in range(0, lines):
            line = []
            for j in range(0, columns):
                line.append(value)
            content.append(line)
        return content


class Game:
    
    def __init__(self, name):
        self.name = name
        self.world = None
        self.zones = {}
        self.players = {}
        self.triggers = {}
        self.elem_types = {}
        self.unit_types = {}
        self.building_types = {}
        self.building_types_ordered = []
        self.is_live = True
    
    def set_name(self, name):
        self.name = name
    
    def set_map(self, game_map):
        self.world = World(self, game_map, self.elem_types)

    def set_elem_types(self, elem_types):
        self.elem_types = elem_types

    def set_unit_types(self, unit_types):
        self.unit_types = unit_types
    
    def set_building_types(self, building_types, order):
        self.building_types = building_types
        self.building_types_ordered = order
    
    def create_player(self, name, player_color, *ress):
        print("creating player")
        if name in self.players:
            raise Exception("Already a player with this name")
        self.players[name] = Player(self, name, player_color, ress)

    def create_unit(self, player_name, x, y, unit_types_name):
        sys.stdout.write("creating unit")
        p = self.get_player_by_name(player_name)
        ut = self.get_unit_types_by_name(unit_types_name)
        if not self.world.is_valid(x, y) or not self.world.is_empty(x,y):
            raise Exception("False or not empty coordinates : " + str(x) + ", " + str(y) + " p = " + str(self.world.passable_map[y][x]))
        u = Unit(ut, p, x, y)
        self.world.units.append(u)
        p.units.append(u)
        sys.stdout.write(' :: unit #' + str(u.id) + ' created\n')
        return u.id
        
    def create_building(self, player_name, x, y, building_type_name):
        sys.stdout.write("creating building")
        p = self.get_player_by_name(player_name)
        bt = self.get_building_type_by_name(building_type_name)
        if not self.world.is_valid_zone(x, y, bt.grid_w, bt.grid_h) or not self.world.is_empty_zone(x, y, bt.grid_w, bt.grid_h):
            raise Exception("False or not empty coordinates : " + str(x) + ", " + str(y))
        b = Building(p, bt, x, y)
        self.world.units.append(b) 
        p.buildings.append(b)
        sys.stdout.write(' :: building #' + str(b.id) + ' created\n')
        return b.id
        
    def create_trigger(self, name):
        self.triggers[name] = Trigger(name)
        
    def create_condition(self, ref, kind, *params):
        self.triggers[ref].conditions.append(Condition(kind, params))
    
    def create_action(self, ref, kind, *params):
        self.triggers[ref].actions.append(Action(kind, params))
    
    def create_zone(self, name, x1, y1, x2, y2):
        self.zones[name] = Zone(name, x1, y1, x2, y2)
    
    #def order_move(self, units, x : int, y : int, add : bool):
    def order_move(self, units, x, y, add):
        sys.stdout.write('Move ')
        for u in units:
            sys.stdout.write(str(u) + ' ')
            if add:
                sys.stdout.write('(delayed) ')
                u.add_order(Order('go', x, y))
            else:
                u.order(Order('go', x, y))
        sys.stdout.write('to ' + str(x) + ', ' + str(y) + '\n')
    
    def order_attack(self, units, target, add):
        sys.stdout.write('Attack ')
        for u in units:
            sys.stdout.write(str(u) + ' ')
            if add:
                sys.stdout.write('(delayed) ')
                u.add_order(Order('attack', target=target))
            else:
                u.order(Order('attack', target=target))
        sys.stdout.write('target => ' + str(target) + ' at ' + str(target.x) + ', ' + str(target.y) + '\n')
    
    def get_player_by_name(self, player_name):
        if player_name not in self.players:
            raise Exception("Unknown player : " + player_name)
        return self.players[player_name]

    def get_unit_types_by_name(self, unit_types_name):
        if unit_types_name not in self.unit_types:
            raise Exception("Unknown unit type : " + unit_types_name)
        return self.unit_types[unit_types_name]
        
    def get_building_type_by_name(self, building_type_name):
        if building_type_name not in self.building_types:
            raise Exception("Unknown building type : " + building_type_name)
        return self.building_types[building_type_name]
    
    def get_all_units_in_zone_for_player(self, ref_zone, ref_player):
        p = self.players[ref_player]
        z = self.zones[ref_zone]
        units = []
        for i in range(z.x1, z.x2):
            for j in range(z.y1, z.y2):
                u = self.world.get_unit_at(i, j)
                if u is not None and u.player == p:
                    units.append(u)
        return units
    
    def get_players(self):
        return self.players
    
    #def get_units_by_id(self, ids):
    #    units = []
    #    cpt = 0
    #    for u in self.world.units:
    #        if u.uid in ids:
    #            units.append(u)
    #            cpt += 1
    #    if cpt != len(ids):
    #        raise Exception("ID of unit unknown detected !!!")
    #    return units
    
    def update(self):
        # Triggers and actions
        for key, value in self.triggers.items():
            if value.test_all(self):
                value.do_all(self)
        # Particles
        self.world.particles.update()
        # Players & units
        for key, value in self.players.items():
            value.update()
        return self.is_live


class Player:
    
    def __init__(self, game, name, player_color, ress):
        self.game = game
        self.name = name
        self.world = game.world
        self.color = player_color
        self.units = []
        self.buildings = []
        self.min = ress[0]
        self.sol = ress[1]
        self.victorious = False
        self.fog_map = World.create_map(self.world.size32.x, self.world.size32.y, 0)  # bytearray(MAP_SIZE * MAP_SIZE)  # memoryview(bytearray(MAP_SIZE * MAP_SIZE))  #

    def update(self):
        # put fog_map
        for yy in range(0, self.world.size32.y):
            for xx in range(0, self.world.size32.x):
                fog = self.fog_map[yy][xx]
                if fog == 2:
                    self.fog_map[yy][xx] = 1
        # Update for all units?
        i = 0
        while i < len(self.units):
        #for u in self.units:
            if not self.units[i].update():
                self.world.units.remove(self.units[i])
                del self.units[i]
                print("deleting unit")
                # del u
            i += 1
        for b in self.buildings:
            b.update()


class Order:
    def __init__(self, kind=None, x=0, y=0, target=None):
        self.x = x
        self.y = y
        self.target = target
        self.kind = kind


class BuildLoad:

    def __init__(self):
        pass


class WeaponType:

    #def __init__(self, name : str, range : int, reload : int):
    def __init__(self, name, range, reload):
        self.name = name
        self.range = range
        self.reload = reload


class BuildingType:

    #def __init__(self, name : str, grid_h : int, grid_w : int, life : int, cost : int, build_load : BuildLoad = None, weapon_type : WeaponType = None):
    def __init__(self, name, grid_h, grid_w, life, cost, vision, build_load = None, weapon_type = None):
        self.name = name
        self.grid_h = grid_h
        self.grid_w = grid_w
        self.life = life
        self.cost = cost
        self.vision = vision
        self.build_load = build_load
        self.weapon_type = weapon_type


class GameObject:
 
    seed = 0
    
    def __init__(self, player):
        self.id = GameObject.seed + 1
        GameObject.seed = self.id
        self.player = player

    def light(self, x, y, w, h, dist):
        self.radius_effect(2, x, y, w, h, dist)
    
    def radius_effect(self, value, x, y, w, h, dist):
        if h == 1 and w == 1:
            # print()
            for yy in range(max(0, y - dist -1), min(self.player.world.size32.y, y + h + dist +1)):
                for xx in range(max(0, x - dist -1), min(self.player.world.size32.x, x + w + dist +1)):
                    #if xx != x or yy != y:
                    #    print("{0:.2f}".format(round(get_dist(xx, yy, x, y), 2)), ' ', end="")
                    #else:
                    #    print('xxxx  ', end="")
                    d = round(get_dist(xx, yy, x, y), 2) 
                    if  d <= dist:
                        self.player.fog_map[yy][xx] = value
                    elif dist < d <= dist + 1:
                        self.player.fog_map[yy][xx] = max(1, self.player.fog_map[yy][xx])
                # print()
        else:
            # print()
            # print("x", x)
            # print("y", y)
            # print("dist", dist)
            # print("yy min", max(0, y - dist))
            # print("yy max", min(self.player.world.size32.y, y + h + dist))
            # print("xx min", max(0, x - dist))
            # print("xx max", min(self.player.world.size32.x, x + w + dist))
            for yy in range(max(0, y - dist), min(self.player.world.size32.y, y + h + dist)):
                for xx in range(max(0, x - dist), min(self.player.world.size32.x, x + w + dist)):
                    if xx < x and yy < y:
                        # print(xx, yy, "1:{0:.2f}".format(round(get_dist(xx, yy, x, y), 2)), ' ', end="", flush=True)
                        d = round(get_dist(xx, yy, x, y), 2)
                        if d <= dist:
                            self.player.fog_map[yy][xx] = value
                        elif dist < d <= dist + 1:
                            self.player.fog_map[yy][xx] = max(1, self.player.fog_map[yy][xx])
                    elif x <= xx < x+w and yy < y:
                        # print(xx, yy, "2:{0:.2f}".format(round(get_dist(xx, yy, xx, y), 2)), ' ', end="", flush=True)
                        d = round(get_dist(xx, yy, xx, y), 2)
                        if d <= dist:
                            self.player.fog_map[yy][xx] = value
                        elif dist < d <= dist + 1:
                            self.player.fog_map[yy][xx] = max(1, self.player.fog_map[yy][xx])
                    elif xx >= x+w and yy < y:
                        # print(xx, yy, "3:{0:.2f}".format(round(get_dist(xx, yy, x+w-1, y), 2)), ' ', end="", flush=True)
                        d = round(get_dist(xx, yy, x + w - 1, y), 2)
                        if d <= dist:
                            self.player.fog_map[yy][xx] = value
                        elif dist < d <= dist + 1:
                            self.player.fog_map[yy][xx] = max(1, self.player.fog_map[yy][xx])
                    elif xx < x and y <= yy < y+h:
                        # print(xx, yy, "4:{0:.2f}".format(round(get_dist(xx, yy, x, yy), 2)), ' ', end="", flush=True)
                        d = round(get_dist(xx, yy, x, yy), 2)
                        if d <= dist:
                            self.player.fog_map[yy][xx] = value
                        elif dist < d <= dist + 1:
                            self.player.fog_map[yy][xx] = max(1, self.player.fog_map[yy][xx])
                    elif x <= xx < x+w and y <= yy < y+h:
                        # print(xx, yy, "5:xxxx", ' ', end="")
                        self.player.fog_map[yy][xx] = value
                    elif xx >= x+w and y <= yy < y+h:
                        # print(xx, yy, "6:{0:.2f}".format(round(get_dist(xx, yy, x+w-1, yy), 2)), ' ', end="", flush=True)
                        d = round(get_dist(xx, yy, x + w - 1, yy), 2)
                        if d <= dist:
                            self.player.fog_map[yy][xx] = value
                        elif dist < d <= dist + 1:
                            self.player.fog_map[yy][xx] = max(1, self.player.fog_map[yy][xx])
                    elif xx < x and yy >= y+h:
                        # print(xx, yy, "7:{0:.2f}".format(round(get_dist(xx, yy, x, yy+h-1), 2)), ' ', end="", flush=True)
                        d = round(get_dist(xx, yy, x, y + h - 1), 2)
                        if d <= dist:
                            self.player.fog_map[yy][xx] = value
                        elif dist < d <= dist + 1:
                            self.player.fog_map[yy][xx] = max(1, self.player.fog_map[yy][xx])
                    elif x <= xx < x+w and yy >= y+h:
                        # print(xx, yy, "8:{0:.2f}".format(round(get_dist(xx, yy, xx, y+h-1), 2)), ' ', end="", flush=True)
                        d = round(get_dist(xx, yy, xx, y + h - 1), 2) 
                        if d <= dist:
                            self.player.fog_map[yy][xx] = value
                        elif dist < d <= dist + 1:
                            self.player.fog_map[yy][xx] = max(1, self.player.fog_map[yy][xx])
                    elif xx >= x+w and yy >= y+h:
                        # print(xx, yy, "9:{0:.2f}".format(round(get_dist(xx, yy, x+w-1, y+h-1), 2)), ' ', end="", flush=True)
                        d = round(get_dist(xx, yy, x + w - 1, y + h - 1), 2) 
                        if d <= dist:
                            self.player.fog_map[yy][xx] = value
                        elif dist < d <= dist + 1:
                            self.player.fog_map[yy][xx] = max(1, self.player.fog_map[yy][xx])
                    # else:
                    #     print(xx, yy, "wtf  ", end="", flush=True)
                # print()
            # exit()


class Building(GameObject):

    # def __init__(self, player : Player, type : BuildingType, grid_x : int, grid_y : int):
    def __init__(self, player, b_type, x, y):  # grid_x, grid_y
        GameObject.__init__(self, player)
        self.type = b_type
        self.x = x
        self.y = y
        self.vision = b_type.vision
        self.life = b_type.life
        
        self.orders = []
        for i in range(x, x + b_type.grid_w):
            for j in range(y, y + b_type.grid_h):
                self.player.world.unit_map[j][i] = (2, self) # STILL, BUILDING

        # Fog
        self.light(self.x, self.y, self.type.grid_w, self.type.grid_h, self.vision)

    def __str__(self):
        return str(id(self)) + ' (' + self.type.name + ')'
    
    def update(self):
        if self.life <= 0:
            for i in range(self.x, self.x + self.type.grid_w):
                for j in range(self.y, self.y + self.type.grid_h):
                    self.player.world.unit_map[j][i] = 0
            return False
        if self.type.name == "Mine":
            self.player.min += 0.2
            if self.player.min > 9999:
                self.player.min = 9999
        elif self.type.name == "Solar":
            self.player.sol += 0.2
            if self.player.sol > 9999:
                self.player.sol = 9999
        # Fog
        self.light(self.x, self.y, self.type.grid_w, self.type.grid_h, self.vision)
        return True  # Very Important
    
    def order(self, o):
        self.orders = [o]

    def add_order(self, o):
        self.orders.append(o)

    def hit(self, x, y):
        x1 = self.x * 32
        y1 = self.y * 32
        w = self.type.grid_w * 32
        h = self.type.grid_h * 32
        return x1 <= x <= x1 + w and y1 <= y <= y1 + h


class UnitType:

    def __init__(self, name, size, vision, range, life, dom, speed, reload):
        self.name = name
        self.size = size
        self.vision = vision
        self.range = range
        self.life = life
        self.dom = dom
        self.speed = speed
        self.reload = reload


class Unit(GameObject):
    
    def __init__(self, utype, player, x, y):
        GameObject.__init__(self, player)
        self.type = utype
        self.real_x = x * 32 + 16
        self.real_y = y * 32 + 16
        self.x = x
        self.y = y
        self.size = utype.size
        self.range = utype.range
        self.vision = utype.vision
        self.life = utype.life
        self.dom = utype.dom
        self.reload = utype.reload
        
        self.orders = []
        self.cpt = 0
        self.cpt_move = 0
        self.speed_move = 1
        self.speed_step = utype.speed  # must be 1 or a multiple of 2 - 2 before
        self.old_x = x
        self.old_y = y

        # Transitional movement system (TMS)
        self.transition = None
        self.destination = None
        self.previous32 = None

        # Fog
        self.light(self.x, self.y, 1, 1, self.vision)

    def __str__(self):
        return 'Unit #' + str(self.id) + ' (' + self.type.name + ')'

    def update(self):
        old_x = self.x
        old_y = self.y
        self.player.world.unit_map[self.y][self.x] = 0
        # print 'update ', len(self.orders)
        if self.life <= 0:
            return False

        if len(self.orders) > 0:
            o = self.orders[0]
            if o.kind == 'go':
                r = self.go(o.x, o.y)
                if r:
                    del self.orders[0]
            elif o.kind == 'attack':
                # print(self.range, get_dist(self.x, self.y, o.target.x, o.target.y)) # check if the unit is not 'in transit'
                if get_dist(self.x, self.y, o.target.x, o.target.y) > self.range or (self.real_x - 16) % 32 != 0 or (self.real_y - 16) % 32 != 0:
                    self.go(o.target.x, o.target.y)
                else:
                    r = self.attack(o.target)
                    if r:
                        del self.orders[0]
        self.player.world.unit_map[self.y][self.x] = (1, self) # CODE: STILL, UNIT

        # Fog
        self.light(self.x, self.y, 1, 1, self.vision)

        return True

    # def order(self, o : Order):
    def order(self, o):
        self.orders = [o]

    def add_order(self, o):
        self.orders.append(o)
    
    def attack(self, target):
        if self.cpt <= 0:
            self.player.world.particles.add(Particle('blue sphere', self, target, 10, 100))
            self.cpt = self.reload
        else:
            self.cpt -= 1
        if target.life <= 0:
            return True
        else:
            return False
    
    def go(self, x: int, y: int):
        if self.cpt_move > 0:
            self.cpt_move -= 1
            return False
        else:
            self.cpt_move = self.speed_move

        if self.destination is None:
            # 32 en 32
            from_x = self.x
            from_y = self.y
            to_x = x
            to_y = y

            # print 'destination x,y = ', x,y
            # print 'destination/32 x,y = ', to_x32, to_y32

            n_x = -1
            n_y = -1
            going_x = 0
            going_y = 0
            if to_x > from_x:
                n_x = from_x + 1
                going_x = 1
            elif to_x < from_x:
                n_x = from_x - 1
                going_x = -1
            elif to_x == from_x:
                n_x = from_x
            if to_y > from_y:
                n_y = from_y + 1
                going_y = 1
            elif to_y < from_y:
                n_y = from_y - 1
                going_y = -1
            elif to_y == from_y:
                n_y = from_y

            if not self.player.world.is_empty(n_x, n_y):
                print("blocked!")
                if going_x == 1 and going_y == 1:
                    test = (from_x, n_y, n_x, from_y)
                elif going_x == 1 and going_y == 0:
                    test = (n_x, n_y + 1, n_x, n_y - 1)
                elif going_x == 1 and going_y == -1:
                    test = (from_x, n_y, n_x, from_y)
                elif going_x == 0 and going_y == 1:
                    test = (from_x - 1, n_y, from_x + 1, n_y)
                elif going_x == 0 and going_y == 0:
                    pass  # not a move
                elif going_x == 0 and going_y == -1:
                    test = (from_x - 1, n_y, from_x + 1, n_y)
                elif going_x == -1 and going_y == 1:
                    test = (from_x, n_y, n_x, from_y)
                elif going_x == -1 and going_y == 0:
                    test = (n_x, n_y + 1, n_x, n_y - 1)
                elif going_x == -1 and going_y == -1:
                    test = (from_x, n_y, n_x, from_y)

                if self.player.world.is_valid(test[0], test[1]):
                    if self.player.world.is_empty(test[0], test[1]):
                        #print("trying : " + str(test[0]) + ", " + str(test[1]))
                        n_x = test[0]
                        n_y = test[1]
                    elif self.player.world.is_empty(test[2], test[3]):
                        #print("trying : " + str(test[2]) + ", " + str(test[3]))
                        n_x = test[2]
                        n_y = test[3]
                if n_x == self.old_x and n_y == self.old_y:
                    return True  # no loop !

            if self.player.world.is_empty(n_x, n_y):
                self.destination = Pair(n_x * 32 + 16, n_y * 32 + 16)
                self.player.world.unit_map[n_y][n_x] = (-1, self) # CODE: IN MOVEMENT

        if self.destination is not None and self.transition is None:
            self.transition = Pair(self.x * 32 + 16, self.y * 32 + 16)

        if self.transition != self.destination:
            if self.transition.x < self.destination.x:
                self.transition.x += self.speed_step
            elif self.transition.x > self.destination.x:
                self.transition.x -= self.speed_step
            if self.transition.y < self.destination.y:
                self.transition.y += self.speed_step
            elif self.transition.y > self.destination.y:
                self.transition.y -= self.speed_step

        if self.transition is not None:
            self.real_x = self.transition.x
            self.real_y = self.transition.y
        else:
            self.real_x = self.x * 32 + 16
            self.real_y = self.y * 32 + 16

        if self.destination == self.transition and self.destination is not None:
            self.old_x = self.x
            self.old_y = self.y
            self.x = int((self.destination.x - 16) / 32)
            self.y = int((self.destination.y - 16) / 32)
            self.destination = None
            self.transition = None

        #print(self.x, self.y, "tr= ", self.transition, "dst= ", self.destination) # Add details on pathfinding (verbose)
        return self.x == x and self.y == y

    def hit(self, x, y):
        return get_dist(x, y, self.x * 32 + 16, self.y * 32 + 16) < self.size


# ------------------------------------------------------------------------------
# Scripting the world : Trigger, Zone, Condition & Action
# ------------------------------------------------------------------------------

class Zone:

    def __init__(self, name, x1, y1, x2, y2):
        self.name = name
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


class Trigger:

    def __init__(self, name):
        self.name = name
        self.conditions = []
        self.actions = []
    
    def test_all(self, game):
        for c in self.conditions:
            if not c.test(game):
                return False
        return True
    
    def do_all(self, game):
        for a in self.actions:
            a.do(game)


class Condition:

    def __init__(self, kind, params):
        self.kind = kind
        self.params = params

    def test(self, game):
        if self.kind == 'always':
            return True
        elif self.kind == 'never':
            return False
        elif self.kind == 'player P control OPT1 (exactly/at least/at most) N unit of type T in Zone Z': #'player X control Y unit of type Z':
            if self.params[3] == 'all':
                    player1 = game.get_player_by_name(self.params[0])
                    if self.params[4] == 'everywhere':
                        if self.params[1] == 1:
                            return len(player1.units + player1.buildings) == self.params[2]
                        elif self.params[2] == 2:
                            return len(player1.units + player1.buildings) >= self.params[2]
                        elif self.params[3] == 3:
                            return len(player1.units + player1.buildings) <= self.params[2]
                    else:
                        ref_zone = self.params[4]
                        units = game.get_all_units_in_zone_for_player(ref_zone, self.params[0])
                        #print(ref_zone, units, len(units), self.params[1], self.params[2])
                        if self.params[1] == 1:
                            return len(units) == self.params[2]
                        elif self.params[1] == 2:
                            return len(units) >= self.params[2]
                        elif self.params[1] == 3:
                            return len(units) <= self.params[2]
        else:
            return False

class Action:

    def __init__(self, kind, params):
        self.kind = kind
        self.params = params
        
    def do(self, game):
        if self.kind == 'win':
            game.is_live = False
            game.get_player_by_name(self.params[0]).victorious = True
        elif self.kind == 'give all unit of player P1 to player P2 in Zone Z':
            if self.params[2] != 'everywhere':
                units = game.get_all_units_in_zone_for_player(self.params[2], self.params[0])
                receiver = game.get_player_by_name(self.params[1])
                for u in units:
                    u.player.units.remove(u)
                    u.player = receiver
                    u.player.units.append(u)
        else:
            pass


# -----------------------------------------------------------------------------
# Tools
# ------------------------------------------------------------------------------

def get_angle(x1, y1, x2, y2):
    dx, dy = get_diff(x1, y1, x2, y2)
    return math.atan2(dy, dx)


def get_diff(x1, y1, x2, y2):
    return x2 - x1, y2 - y1
        

def get_dist(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def xrect(x1, y1, x2, y2):
    tx = abs(x1 - x2)
    ty = abs(y1 - y2)
    if x1 > x2:
        rx = x2
    else:
        rx = x1
    if y1 > y2:
        ry = y2
    else:
        ry = y1
    return pygame.Rect(rx, ry, tx, ty)


# ------------------------------------------------------------------------------
# Menu
# ------------------------------------------------------------------------------


class Button:

    def __init__(self, menu, text, x, y, w, h, c, ctext, cover, cclicked, size):
        self.text = text
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.color = c
        self.color_text = ctext
        self.color_over = cover
        self.color_clicked = cclicked
        self.size = size
        self.clicked = False
        self.menu = menu
    
    def update(self):
        if self.clicked:
            self.menu.state['clicked'] = self.text
    
    def render(self):
        mx, my = self.menu.engine.get_mouse_pos()
        if self.clicked:
            c = self.color_clicked
        elif self.is_in(mx, my):
            c = self.color_over
        else:
            c = self.color
        self.menu.engine.rect(self.x, self.y, self.width, self.height, c, 1, 1) # fond
        self.menu.engine.rect(self.x-5, self.y-5, self.width+10, self.height+10, c, 1, 1) # fond
        self.menu.engine.text(self.x + self.width/2, self.y + self.height/2, self.text, self.color_text, 2, True, self.size) # texte
    
    def is_in(self, x, y):
        return self.x <= x < self.x + self.width and self.y <= y <= self.y + self.height

    def click(self):
        self.clicked = True


class Menu:
    
    def __init__(self, engine):
        self.engine = engine
        self.buttons = []
        self.state = {'clicked': None}

    def menu_start(self):
        def pipo():
            pass

        self.buttons.append(Button(self, "Campaign", self.engine.size[0]/2-100, self.engine.size[1]/2-15-90, 200, 30,
                                   Colors.DARK_BLUE, Colors.YELLOW, Colors.LIGHT_BLUE, Colors.YELLOW, 18))
        self.buttons.append(Button(self, "Skirmish", self.engine.size[0]/2-100, self.engine.size[1]/2-15-30, 200, 30,
                                   Colors.DARK_BLUE, Colors.YELLOW, Colors.LIGHT_BLUE, Colors.YELLOW, 18))
        self.buttons.append(Button(self, "Options", self.engine.size[0]/2-100, self.engine.size[1]/2-15+30, 200, 30,
                                   Colors.DARK_BLUE, Colors.YELLOW, Colors.LIGHT_BLUE, Colors.YELLOW, 18))
        self.buttons.append(Button(self, "Quit", self.engine.size[0]/2-100, self.engine.size[1]/2-15+90, 200, 30,
                                   Colors.DARK_BLUE, Colors.YELLOW, Colors.LIGHT_BLUE, Colors.YELLOW, 18))
        
    def menu_pause(self):
        self.buttons.append(Button(self, "Quit to main menu", self.engine.size[0]/2-100, self.engine.size[1]/2-15-90, 200, 30, Colors.DARK_BLUE, Colors.YELLOW, Colors.LIGHT_BLUE, Colors.YELLOW, 18))
        self.buttons.append(Button(self, "Resume", self.engine.size[0]/2-100, self.engine.size[1]/2-15-30, 200, 30, Colors.DARK_BLUE, Colors.YELLOW, Colors.LIGHT_BLUE, Colors.YELLOW, 18))
        self.buttons.append(Button(self, "Options", self.engine.size[0]/2-100, self.engine.size[1]/2-15+30, 200, 30, Colors.DARK_BLUE, Colors.YELLOW, Colors.LIGHT_BLUE, Colors.YELLOW, 18))
        self.buttons.append(Button(self, "Quit", self.engine.size[0]/2-100, self.engine.size[1]/2-15+90, 200, 30, Colors.DARK_BLUE, Colors.YELLOW, Colors.LIGHT_BLUE, Colors.YELLOW, 18))
    
    def update(self):
        for event in self.engine.get_events():
            if event.type == self.engine.QUIT:
                self.state['clicked'] = 'Quit'
            elif event.type == self.engine.EventTypes.KEY_DOWN:
                if event.key == self.engine.Keys.ESCAPE:
                    self.state['clicked'] = 'Quit'
            elif event.type == self.engine.EventTypes.MOUSE_BUTTON_UP:
                mx, my = self.engine.get_mouse_pos()
                if event.button == self.engine.Keys.MOUSE_LEFT:
                    for b in self.buttons:
                        if b.is_in(mx, my):
                            b.click()
        for b in self.buttons:
            b.update()
        return self.state
    
    def render(self):
        self.engine.fill(Colors.BLACK)
        for b in self.buttons:
            b.render()




class Application:

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.fps = 30.0
    
    def set_caption(self):
        pygame.display.set_caption("RTS Project - {:.2f}".format(self.clock.get_fps()))
    
    def start(self):
        e = Engine(800, 600)
        load_textures(e)
        while True:
            r = self.menu_loop(e) 
            if not r:
                break
        e.stop()
        print('Goodbye')  
    
    def menu_loop(self, engine):
        m = Menu(engine)
        m.menu_start()
        while True:
            s = m.update()
            m.render()
            engine.render()
            if s['clicked'] is not None:
                break
        if s['clicked'] in ['Campaign', 'Skirmish']:
            g = Game('Test 1')
            c = configure(g, engine)
            r = self.game_loop(g, c, engine)
            return r
        elif s['clicked'] == 'Options':
            pass
        elif s['clicked'] == 'Quit':
            return False
    
    def in_game_menu_loop(self, engine):
        m = Menu(engine)
        m.menu_pause()
        while True:
            s = m.update()
            m.render()
            engine.render()
            if s['clicked'] is not None: break
        if s['clicked'] == 'Options':
            pass
        else:
            return s['clicked']
       
    def game_loop(self, game, camera, engine): 
        start_time = pygame.time.get_ticks()
        self.clock.tick(self.fps)
        while True:
            res_gam = game.update()
            res_cam = camera.update()
            camera.render()
            engine.render()
            self.clock.tick(self.fps)
            self.set_caption()
            if not res_cam:
                r = self.in_game_menu_loop(engine)
                if r != 'Resume':
                    break
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
            print('\tMetal = ' + str(camera.player.min))
            print('\tEnergy = ' + str(camera.player.sol))
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


class TextureInfo:

    def __init__(self, mini_map_color, passable):
        self.mini = mini_map_color
        self.passable = passable


def mod_basic(game, engine):

    game.set_elem_types(engine.textures)  # TODO: pass only what we need (passable information see World class)
    game.set_unit_types({"soldier": UnitType("Soldier", size=10, vision=3, range=10, life=100, dom=5, speed=8, reload=50),
                         "elite": UnitType("Elite", size=10, vision=4, range=10, life=100, dom=10, speed=8, reload=50),
                         "big": UnitType("Big", size=20, vision=2, range=30, life=300, dom=20, speed=8, reload=50)})
    game.set_building_types({"mine": BuildingType("Mine", 2, 2, 100, (0,50), 2),
                             "solar": BuildingType("Solar", 1, 2, 80, (0, 50), 2),
                             "radar": BuildingType("Radar", 1, 1, 80, (50, 200), 2),
                             "barracks": BuildingType("Barracks", 3, 2, 300, (50, 100), 2),
                             "factory": BuildingType("Factory", 3, 2, 500, (200, 200), 2),
                             "laboratory": BuildingType("Laboratory", 2, 2, 250, (100, 400), 2),
                            }, ["solar", "mine", "radar", "barracks", "factory", "laboratory"])

    game.textures_info = {
        1: TextureInfo(Colors.MINI_MAP_BROWN_DARK, False),  # mini, passable
        25: TextureInfo(Colors.MINI_MAP_GREEN_DARK, False),
        26: TextureInfo(Colors.MINI_MAP_GREEN_DARK, False),
        # Real textures
        100: TextureInfo(Colors.MINI_MAP_GREEN_LIGHT, True),
        200: TextureInfo(Colors.MINI_MAP_BROWN, True),
        300: TextureInfo(Colors.MINI_MAP_BLUE_LIGHT, False),
        9100: TextureInfo(Colors.MINI_MAP_BLUE_LIGHT, False),
        9200: TextureInfo(Colors.MINI_MAP_BLUE_LIGHT, False),
        9300: TextureInfo(Colors.MINI_MAP_BLUE_LIGHT, False),
        9400: TextureInfo(Colors.MINI_MAP_BLUE_LIGHT, False),
        9500: TextureInfo(Colors.MINI_MAP_BLUE_LIGHT, False),
        9600: TextureInfo(Colors.MINI_MAP_BLUE_LIGHT, False),
        9700: TextureInfo(Colors.MINI_MAP_BLUE_LIGHT, False),
        9800: TextureInfo(Colors.MINI_MAP_BLUE_LIGHT, False),
        8100: TextureInfo(Colors.MINI_MAP_BLUE_LIGHT, False),
        8200: TextureInfo(Colors.MINI_MAP_BLUE_LIGHT, False),
        8300: TextureInfo(Colors.MINI_MAP_BLUE_LIGHT, False),
        8400: TextureInfo(Colors.MINI_MAP_BLUE_LIGHT, False),
        8500: TextureInfo(Colors.MINI_MAP_BLUE_LIGHT, False),
        8700: TextureInfo(Colors.MINI_MAP_BLUE_LIGHT, False),
        8900: TextureInfo(Colors.MINI_MAP_BLUE_LIGHT, False),
        10000: TextureInfo(Colors.MINI_MAP_FOG, False),
        11111: TextureInfo(Colors.MINI_MAP_BLACK, False),
        20001: TextureInfo(Colors.MINI_MAP_BLUE, False),
    }
    # Mixing Texture
    for a in [9100, 9200, 9300, 9400, 9500, 9600, 9700, 9800, 8100, 8200, 8300, 8400, 8500, 8700, 8900]:
        for b in [100]:
            if a > 9000:
                n = b*10+a-9000
            else:
                n = b*10+1000+a-8000
            game.textures_info[n] = TextureInfo(game.textures_info[a].mini, game.textures_info[a].passable)


def level_E1L1(game):
    
    game.set_name('The rescue party')
    # 100 ground +1 rock 200 grass 300 water | len(my_map[0]) | len(my_map)
    game.set_map([
        [101, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 101, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 200, 200, 200, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 300, 300, 300, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 300, 300, 300, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 300, 300, 300, 100, 100, 100, 100, 100],
        [100, 100, 100, 200, 200, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 200, 200, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 101, 101, 101, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 100, 100, 100, 100, 300, 300, 300, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 300, 300, 300, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 300, 300, 300, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 101, 100, 100, 100, 100, 100, 100, 100, 100, 100, 300, 300, 300, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 300, 300, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 300, 300, 300, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 300, 300, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 300, 300, 300, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 101, 101, 101, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 101, 100, 101, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 101, 101, 101, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 300, 300, 100, 100, 100, 300, 300, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 125, 125, 126, 100, 100, 100, 100, 100, 100, 100, 100, 300, 300, 100, 100, 100, 300, 300, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 100, 100, 100, 100, 300, 300, 100, 100, 100, 100, 100, 300, 300, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 100, 100, 100, 100, 100, 100, 100, 100, 100, 300, 300, 100, 100, 100, 100, 100, 300, 300, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        ])
    
    game.create_player("Bob", Colors.YELLOW, 100, 100)
    game.create_player("Henry", Colors.SKY_BLUE, 0, 0)
    game.create_player("Neutral", Colors.GREY, 20, 20)
    
    game.create_unit("Bob", 1, 1, "soldier")
    game.create_unit("Bob", 3, 3, "elite")
    game.create_unit("Neutral", 20, 20, "soldier")
    
    game.create_unit("Henry", 12, 12, "big")
    game.create_unit("Henry", 18, 14, "soldier")
    
    game.create_building("Bob", 5, 5, "mine")
    game.create_building("Henry", 22, 22, "mine")

    game.create_trigger('t1')
    game.create_condition('t1', 'player P control OPT1 (exactly/at least/at most) N unit of type T in Zone Z', 'Henry', 1, 0, 'all', 'everywhere')
    game.create_action('t1', 'win', 'Bob')
    
    game.create_trigger('t2')
    game.create_zone('z1', 17, 17, 23, 23)
    game.create_condition('t2', 'player P control OPT1 (exactly/at least/at most) N unit of type T in Zone Z', 'Bob', 2, 1, 'all', 'z1')
    #game.create_action('t2', 'win', 'Bob')
    game.create_action('t2', 'give all unit of player P1 to player P2 in Zone Z', 'Neutral', 'Bob', 'z1')
    

def configure(g, e):
    mod_basic(g, e)
    try:
        import maps.e1l1
        maps.e1l1.load(g, Colors)
    except ImportError as ie:
        level_E1L1(g)
    return Camera(e, 800, 600, 5, g.get_player_by_name("Bob"))  # x, y, scroll, player


if __name__ == '__main__': 

    #
    # ABC 
    # H0D   
    # GFE
    #
    #print( math.degrees(get_angle(2, 2, 1, 1))) # 0 -> A +135
    #print( math.degrees(get_angle(2, 2, 2, 1))) # 0 -> B +90
    #print( math.degrees(get_angle(2, 2, 3, 1))) # 0 -> C +45
    #print( math.degrees(get_angle(2, 2, 3, 2))) # 0 -> D 000
    #print( math.degrees(get_angle(2, 2, 3, 3))) # 0 -> E -45
    #print( math.degrees(get_angle(2, 2, 2, 3))) # 0 -> F -90
    #print( math.degrees(get_angle(2, 2, 1, 3))) # A -> G -135
    #print( math.degrees(get_angle(2, 2, 1, 2))) # A -> H +180 // -180
    
    import sys
    _maj, _min = sys.version_info[:2]
    print('Starting on Python ' + str(_maj) + "." + str(_min) + " with pygame " + pygame.version.ver)
    
    # No profiling
    Application().start()
    exit()
    
    # For Profiling
    import cProfile, pstats, io
    pr = cProfile.Profile()
    pr.enable()
    
    Application().start()
    
    pr.disable()
    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())
    prof = open('profile.txt', 'w')
    prof.write(s.getvalue())
    prof.close()
    
    exit()
