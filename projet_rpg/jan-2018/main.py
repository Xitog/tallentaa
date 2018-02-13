#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

# Personal libs
from matrix_map import MatrixMap
# External libs
import pygame
# Standard libs
import random
import sys
import os

#-------------------------------------------------------------------------------
# Classes
#-------------------------------------------------------------------------------

class Application:

    def __init__(self, title, width, height, ress_dir=os.getcwd()):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.color = (255, 0, 0)
        self.background = (0, 0, 0)
        self.loop = True
        self.down = False
        self.up = False
        self.right = False
        self.left = False
        self.grid = False
        self.cam_x = 0
        self.cam_y = 0
        self.tiles = {}
        self.mods = {}
        self.ress_dir = ress_dir
        self.time_step = 5
        self.game_map = None

    def get_base(self, row, col):
        val = self.game_map.get(row, col, 0)
        return val >> 10

    def get_trans(self, row, col):
        val = self.game_map.get(row, col, 0)
        val2str = f"{val:15b}".replace(' ', '0')
        return int(val2str[5:10], base=2)

    def is_base_or_trans(self, row, col, list_of_val):
        a = self.get_base(row, col)
        if a in list_of_val:
            return list_of_val.index(a)
        b = self.get_trans(row, col)
        if b in list_of_val:
            return list_of_val.index(b)
        return -1
    
    def transitions(self):
        # base texture
        WATER  = 0b0001 # 1
        GROUND = 0b0010 # 2
        GRASS  = 0b0011 # 3
        SAND   = 0b0100 # 4
        for row in range(0, self.game_map.rows):
            for col in range(0, self.game_map.columns):
                me, doo = self.game_map.get(row, col)
                base = me >> 10
                # tests
                if base not in [WATER, GROUND, GRASS, SAND]:
                    raise Exception('Value not correct: ' + str(base) + ' from ' + str(me) + ' @ ' + str(row) + ', ' + str(col))
                if base == WATER:
                    if row - 1 >= 0 and self.get_base(row - 1, col) == GROUND:
                        if row + 1 < self.game_map.rows and self.get_base(row + 1, col) == GROUND:
                            raise Exception(f"Invalid map. Error at: {col}, {row}.")
                    if col - 1 >= 0 and self.get_base(row, col - 1) == GROUND:
                        if col + 1 < self.game_map.columns and self.get_base(row, col + 1) == GROUND:
                            raise Exception(f"Invalid map. Error at: {col}, {row}.")
                # transitions
                if base == WATER:
                    opposed = [GROUND, SAND]
                    opposed_val = [0b000000001000000, 0b000000010000000]
                elif base == GROUND:
                    opposed = [GRASS]
                    opposed_val = [0b000000001100000]
                else:
                    opposed = None
                if opposed is not None:
                    value = me
                    #
                    # Corner calculations
                    #
                    SOUTH_WEST = 0b0000000000011000 # 24
                    SOUTH_EAST = 0b0000000000010100 # 20
                    NORTH_EAST = 0b0000000000010010 # 18
                    NORTH_WEST = 0b0000000000010001 # 17
                    # Has corner?
                    #CORNER    = 0b0000000000010000 # 16
                    if row + 1 < self.game_map.rows and col - 1 >= 0:
                        b = self.get_base(row + 1, col - 1)
                        tst = opposed.index(b) if b in opposed else -1
                        if tst != -1:
                            value |= SOUTH_WEST | opposed_val[tst]
                    if row + 1 < self.game_map.rows and col + 1 < self.game_map.columns:
                        b = self.get_base(row + 1, col + 1)
                        tst = opposed.index(b) if b in opposed else -1
                        if tst != -1:
                            value |= SOUTH_EAST | opposed_val[tst]
                    if row - 1 >= 0 and col - 1 >= 0:
                        b = self.get_base(row - 1, col - 1)
                        tst = opposed.index(b) if b in opposed else -1
                        if tst != -1:
                            value |= NORTH_WEST | opposed_val[tst]
                    if row - 1 >= 0 and col + 1 < self.game_map.columns:
                        b = self.get_base(row - 1, col + 1)
                        tst = opposed.index(b) if b in opposed else -1
                        if tst != -1:
                            value |= NORTH_EAST | opposed_val[tst]
                    backup = value
                    value = me
                    #
                    # Border calculation
                    #
                    NORTH = 0b0000000000000001 # 1
                    EAST  = 0b0000000000000010 # 2
                    SOUTH = 0b0000000000000100 # 4
                    WEST  = 0b0000000000001000 # 8
                    border = 0
                    if row + 1 < self.game_map.rows:
                        b = self.get_base(row + 1, col)
                        tst = opposed.index(b) if b in opposed else -1
                        if tst != -1:
                            value |= SOUTH | opposed_val[tst]
                            border += 1
                    if row - 1 >= 0:
                        b = self.get_base(row - 1, col)
                        tst = opposed.index(b) if b in opposed else -1
                        if tst != -1:
                            value |= NORTH | opposed_val[tst]
                            border += 1
                    if col - 1 >= 0:
                        b = self.get_base(row, col - 1)
                        tst = opposed.index(b) if b in opposed else -1
                        if tst != -1:
                            value |= WEST | opposed_val[tst]
                            border += 1
                    if col + 1 < self.game_map.columns:
                        b = self.get_base(row, col + 1)
                        tst = opposed.index(b) if b in opposed else -1
                        if tst != -1:
                            value |= EAST | opposed_val[tst]
                            border += 1
                    if value == me: # no border modifications, relying on corner modifications
                        value = backup
                    # save changes
                    if value in self.tiles:
                        self.game_map.set(value, row, col, 0)
                    else:
                        print(f'Invalid value {value} for {base} with nb borders = {border}') 
                        self.game_map.set(0, row, col, 0)
                else:
                    self.game_map.set(me, row, col, 0)
    
    def load_ressource(self, dir_path, file_name):
        ress_name = file_name[:-4]
        ress = ress_name.split('_')
        idr = int(ress[0])
        self.tiles[idr] = pygame.image.load(os.path.join(dir_path, file_name)).convert_alpha()
        if len(ress) > 2:
            mods = ress[2].split('x')
            self.mods[idr] = (int(mods[1]), int(mods[0]))
        else:
            self.mods[idr] = (0, 0)
        print('  Loading: ' + file_name)

    def load_dir(self, dir_path):
        """Load a dir of pictures."""
        print('Loading directory: ' + dir_path)
        for filename in os.listdir(dir_path):
            if filename[-4:] == '.png':
                self.load_ressource(dir_path, filename)

    def load_map(self, dir_path, file_name):
        self.game_map = MatrixMap.load_map(dir_path, file_name, debug=False)
        self.transitions()
    
    def load(self):
        # Load textures for tiles
        self.load_dir(os.path.join(self.ress_dir, 'tiles'))
        self.load_dir(os.path.join(self.ress_dir, 'doodads'))
        self.load_dir(os.path.join(self.ress_dir, 'sprites'))
        # Load font
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 12)
        # Load map
        self.load_map(r'..\..\assets\map', 'map01.xlsx')
    
    def start(self):
        print("Start of Application Dungeon of Darkness")
        print(f"Python version : {sys.version.split(' ')[0]}")
        print(f"PyGame version : {pygame.__version__}")
        print(f"SDL version : {'.'.join(map(str, pygame.get_sdl_version()))}")
        self.load()
        self.mainloop()
    
    def mainloop(self):
        old = pygame.time.get_ticks()
        while self.loop:
            self.update()
            self.render()
            while pygame.time.get_ticks() - old < self.time_step: #8: #10: #16:
                pass
            old = pygame.time.get_ticks()

    def update(self):
        # input
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.loop = False
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_DOWN:
                    self.down = False
                if e.key == pygame.K_UP:
                    self.up = False
                if e.key == pygame.K_LEFT:
                    self.left = False
                if e.key == pygame.K_RIGHT:
                    self.right = False
                if e.key == pygame.K_ESCAPE:
                    self.loop = False
                if e.key == pygame.K_TAB:
                    self.grid = not self.grid
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN:
                    self.down = True
                if e.key == pygame.K_UP:
                    self.up = True
                if e.key == pygame.K_LEFT:
                    self.left = True
                if e.key == pygame.K_RIGHT:
                    self.right = True
        # exec
        if self.down:
            self.cam_y += 1
        if self.up:
            self.cam_y -= 1
        if self.right:
            self.cam_x += 1
        if self.left:
            self.cam_x -= 1
                        
    def render_random(self):
        x1 = random.randint(0, self.width - 1)
        y1 = random.randint(0, self.height - 1)
        x2 = random.randint(0, self.width - 1)
        y2 = random.randint(0, self.height - 1)
        pygame.draw.line(self.screen, self.color, (x1, y1), (x2, y2))

    def render(self):
        self.screen.fill(self.background)
        cam_map_start_col = self.cam_x >> 5
        cam_map_start_lin = self.cam_y >> 5
        #print(cam_map_start_col, self.cam_x, self.cam_x % 32, cam_map_start_lin, self.cam_y, self.cam_y % 32)
        start_col = self.cam_x % 32
        start_lin = self.cam_y % 32
        i_lin = 0
        for lin in range(cam_map_start_lin, cam_map_start_lin + 16 + 5): # +5 in order to display higher doodad
            i_col = -1 # larger doodad
            for col in range(cam_map_start_col - 1, cam_map_start_col + 21 + 1): # -1/+1 in order to display smoothly larger doodad. #BUG# -1 is not working
                if 0 <= col < self.game_map.columns and 0 <= lin < self.game_map.rows:
                    tex, doo = self.game_map.get(lin, col)
                    # Textures
                    self.screen.blit(self.tiles[tex], (-start_col + (i_col << 5), -start_lin + (i_lin << 5)))
                    if self.grid:
                        pygame.draw.rect(self.screen, self.color, (-start_col + (i_col << 5), -start_lin + (i_lin << 5), 32, 32), 1)
                    # Doodads
                    if doo != 0:
                        self.screen.blit(self.tiles[doo], (self.mods[doo][1] - start_col + (i_col << 5), self.mods[doo][0] - start_lin + (i_lin << 5)))
                i_col += 1
            i_lin += 1
        self.screen.blit(self.font.render("Youpi", False, self.color), (30, 30))
        pygame.display.update()

    def clean(self):
        pygame.quit()

if __name__ == '__main__':
    a = Application('Dungeon of Darkness', 640, 480, r'..\..\assets\graphic\textures\rpg_32x32')
    a.start()
    a.clean()

