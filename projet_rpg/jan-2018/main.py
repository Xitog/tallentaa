import pygame
import random
import sys
import os

import xlrd

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
        self.cam_x = 0
        self.cam_y = 0
        self.tiles = {}
        self.mods = {}
        self.ress_dir = ress_dir

    def load_map(self):
        file_name = os.path.join(r'..\..\assets\map', 'map01.xlsx')
        workbook = xlrd.open_workbook(file_name, on_demand=False)
        for s in workbook.sheets():
            if s.name == "ground":
                ground = s
            elif s.name == "doodad":
                doodad = s
            elif s.name == "info":
                pass
            else:
                raise Exception("Incorrect Map File: Sheet unknown: " + s.name)
        self.mapx_w = ground.nrows
        self.mapx_h = ground.ncols
        self.mapx = []
        self.doodads = []
        for row in range(0, ground.nrows):
            self.mapx.append([])
            for col in range(0, ground.ncols):
                self.mapx[row].append(int(ground.cell_value(row, col)))
                d = doodad.cell_value(row, col)
                if d != '':
                    self.doodads.append((row, col, d))
        # transitions
        WATER = 2
        GROUND = 3
        for row in range(0, self.mapx_h):
            for col in range(0, self.mapx_w):
                if self.mapx[row][col] == WATER:
                    # test
                    if row - 1 >= 0 and self.mapx[row - 1][col] == GROUND:
                        if row + 1 < self.mapx_h and self.mapx[row + 1][col] == GROUND:
                            raise Exception(f"Invalid map. Error at: {col}, {row}.")
                    if col - 1 >= 0 and self.mapx[row][col - 1] == GROUND:
                        if col + 1 < self.mapx_w and self.mapx[row][col + 1] == GROUND:
                            raise Exception(f"Invalid map. Error at: {col}, {row}.")
                    # custom
                    if row + 1 < self.mapx_h:
                        if self.mapx[row + 1][col] == GROUND:
                            self.mapx[row][col] = 101
                    if col - 1 >= 0:
                        if self.mapx[row][col - 1] == GROUND:
                            self.mapx[row][col] = 103
                    if row - 1 >= 0:
                        if self.mapx[row - 1][col] == GROUND:
                            self.mapx[row][col] = 105
                    if col + 1 < self.mapx_w:
                        if self.mapx[row][col + 1] == GROUND:
                            self.mapx[row][col] = 107
                    if row + 1 < self.mapx_h and col - 1 >= 0:
                        if self.mapx[row + 1][col - 1] == GROUND:
                            self.mapx[row][col] = 102

    def load_ressource(self, filename):
        ress_name = filename[:-4]
        ress = ress_name.split('_')
        idr = int(ress[0])
        self.tiles[idr] = pygame.image.load(os.path.join(self.ress_dir, filename)).convert()
        if len(ress) > 2:
            mods = ress[2].split('x')
            self.mods[idr] = (int(mods[1]), int(mods[0]))
            #print(ress_name, self.mods[idr])
        print('Loading: ' + filename)
    
    def load(self):
        # Load textures for tiles
        for filename in os.listdir(self.ress_dir):
            if filename[-4:] == ".png":
                self.load_ressource(filename)
        # Load font
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 12)
        # Load map
        self.load_map()
    
    def start(self):
        print("Start of Application Dungeon of Darkness")
        print(f"Python version : {sys.version.split(' ')[0]}")
        print(f"PyGame version : {pygame.__version__}")
        print(f"SDL version : {'.'.join(map(str, pygame.get_sdl_version()))}")
        self.load()
        self.mainloop()
    
    def mainloop(self):
        while self.loop:
            self.update()
            self.render()

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
        for lin in range(cam_map_start_lin, cam_map_start_lin + 16):
            i_col = 0
            for col in range(cam_map_start_col, cam_map_start_col + 21):
                if 0 <= col < self.mapx_w and 0 <= lin < self.mapx_h:
                    self.screen.blit(self.tiles[self.mapx[lin][col]], (-start_col + (i_col << 5), -start_lin + (i_lin << 5)))
                i_col += 1
            i_lin += 1
        # doodad
        for d in self.doodads:
            lin = (d[0] - cam_map_start_lin << 5) + self.mods[5][0] - start_lin
            col = (d[1] - cam_map_start_col << 5) + self.mods[5][1] - start_col
            #print(lin, col)
            self.screen.blit(self.tiles[5], (col, lin))
            #self.screen.blit(self.tiles[5], (-start_col + self.mods[5][0] + (lin << 5), -start_lin + self.mods[5][1] + (col << 5)))
        self.screen.blit(self.font.render("Youpi", False, self.color), (30, 30))
        pygame.display.update()
    
    def render2(self):
        self.screen.fill(self.background)
        for lin in range(0, 15):
            for col in range(0, 20):
                self.screen.blit(self.tiles[self.mapx[lin][col]], ((col << 5) + self.cam_x, (lin << 5) + self.cam_y))
        pygame.display.update()
        
    def render3(self):
        self.screen.fill(self.background)
        map_col_start = self.cam_x >> 5
        map_lin_start = self.cam_y >> 5
        i_lin = 0
        for lin in range(map_lin_start, map_lin_start + 15):
            i_col = 0
            for col in range(map_col_start, map_col_start + 20):
                if 0 <= col < mapx_w and 0 <= lin < mapx_h:
                    self.screen.blit(self.tiles[self.mapx[lin][col]], (i_col << 5, i_lin << 5))
                i_col += 1
            i_lin += 1
        pygame.display.update()
        
    def clean(self):
        pygame.quit()

if __name__ == '__main__':
    a = Application('Dungeon of Darkness', 640, 480, r'..\..\assets\graphic\textures\rpg_32x32')
    a.start()
    a.clean()

