#-------------------------------------------------------------------------------
# Import
#-------------------------------------------------------------------------------

import os       # to choose the map
import struct   # to save to a binary format
import pygame   # to produce an image
import random   # for variability

try:
    import xlrd
except ModuleNotFoundError:
    print('[FAIL] Unable to use this script without xlrd.')
    print('[FAIL] Install it before with: pip install xlrd')
    exit()

#-------------------------------------------------------------------------------
# Global constants
#-------------------------------------------------------------------------------

WATER = 0
MUD = 1
GRASS = 2
DRY = 3
DARK = 4
DEEP = 5

TEXTURES = {
    (51, 51, 153) : WATER, # ( 83, 141, 213) : 0, # water
    (153, 51, 0)  : MUD,   # (151,  71,   6) : 1, # mud
    (0, 128, 0)   : GRASS,
    (70, 25, 0)   : DRY,
    (0, 51, 0)    : DARK,
    (0, 0, 102)   : DEEP,
    (128, 128, 0) : 600,     # (255, 255, 0) : 3, # sand
    (255, 255, 0) : 700,     # (148, 138, 84) : 9, # level
}
TEXTURES_NAMES = {
    WATER : 'water',
    MUD   : 'mud',
    GRASS : 'grass',
    DRY   : 'dry',
    DARK  : 'dark',
    DEEP  : 'deep',
    4 : 'sand',
    9 : 'level'
}

PLAYERS = {
    None : 0, # neutral (for doodads)
    (0, 0, 255) : 1, # player one
    (255, 0, 0) : 2, # player two
}

#-------------------------------------------------------------------------------
# Data model
#-------------------------------------------------------------------------------

class Trigger:

    def __init__(self):
        self.conditions = []
        self.actions = []


class Map:

    def __init__(self, name):
        self.name = name
        self.ground = []
        self.units = []
        self.width = 0
        self.height = 0
        self.values = []
        self.trans = []
        self.trans_values = {}
        self.level = []
        self.triggers = []
    
    def __str__(self):
        return f"{self.name} (W={self.width}, H={self.height})"

    def __repr__(self):
        return str(self)
    
    def get(self, row, col):
        u = self.units[row][col]
        t = self.ground[row][col]
        return [TEXTURES_NAMES[t], u.code, u.player]

    def output_binary(self, filename):
        f = open(filename, mode='wb')
        # header
        f.write(struct.pack('i', 1)) # version
        f.write(struct.pack('i', self.width))
        f.write(struct.pack('i', self.height))
        f.write(struct.pack('i', len(self.name)))
        f.write(self.name.encode('ascii', 'ignore'))
        # data now
        for irow in range(0, len(self.ground)):
            for icol in range(0, len(self.ground[irow])):
                f.write(struct.pack('i', self.ground[irow][icol]))
        # TODO: units
        f.close()

    def refresh_size(self):
        self.height = len(self.ground)
        self.width = len(self.ground[0])

    def transition(self, debug=False):
        modified = {
            WATER : [MUD, DEEP],
            MUD   : [GRASS, DRY],
            GRASS : [DARK],
            DRY : [],
            DARK : [],
            DEEP : [],
        }
        # Make the matrix
        self.trans = []
        for row in range(0, self.height):
            tr = []
            for col in range(0, self.width):
                tr.append(0)
            self.trans.append(tr)
        # Do transition
        print('[INFO] Transitions of map', self.width, 'x', self.height)
        #print('..... Transition on map of Width = ', self.width, 'Height =', self.height)
        #random = 1
        for trow in range(0, self.height):
            for tcol in range(0, self.width):
                calc = 0
                power = [4, 5, 6, 3, 0, 7, 2, 1, 0]
                center = self.ground[trow][tcol]
                opposed = None
                for row in range(trow - 1, trow + 2):
                    for col in range(tcol - 1, tcol + 2):
                        val = power.pop()
                        if (row != trow or col != tcol) and 0 <= row < self.height and 0 <= col < self.width:
                            # Get opposed
                            if self.ground[row][col] != center:
                                # Check IF opposed is not defined AND if the other texture encountered modifies the center
                                if opposed is None and self.ground[row][col] in modified[center]:
                                    opposed = self.ground[row][col]
                                # Check IF opposed is defined AND if the other texture is different from the opposed
                                elif opposed is not None and self.ground[row][col] in modified[center] and opposed != self.ground[row][col]:
                                    raise Exception("Surrounded by two different textures, aborting at ", row, col, "opp=", opposed, "found=", self.ground[row][col], "me=", center)
                            # Calculate transition
                            if self.ground[row][col] == opposed:
                                calc += 2**val
                if debug:
                    print(f'* Cell : x={tcol},y={trow} is {center} with trans {calc:5d} {calc:08b}')
                # Keycode Center Opposed N E S W NW NE SE SW
                Cen3, Cen2, Cen1, Opp3, Opp2, Opp1, N, E, S, W, NW, NE, SE, SW, Rand1, Rand2, Rand3 = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16
                key = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                if center == WATER: pass
                elif center == MUD: key[Cen1] = 1
                elif center == GRASS: key[Cen2] = 1
                elif center == DRY: key[Cen1] = 1; key[Cen2] = 1
                elif center == DARK: key[Cen3] = 1
                elif center == DEEP: key[Cen3] = 1; key[Cen1] = 1
                else: raise Exception('Invalid center : ' + str(center))
                if opposed is not None:
                    if opposed == MUD: key[Opp1] = 1
                    elif opposed == GRASS: key[Opp2] = 1
                    elif opposed == DRY: key[Opp2] = 1; key[Opp1] = 1
                    elif opposed == DARK: key[Opp3] = 1
                    elif opposed == DEEP: key[Opp3] = 1; key[Opp1] = 1
                    else: raise Exception('Invalid opposed : ' + str(opposed))
                else:
                    key[Opp3] = key[Cen3]
                    key[Opp2] = key[Cen2]
                    key[Opp1] = key[Cen1]
                #key[Opp] = opposed if opposed is not None else center
                if calc & 0b00000010: key[N] = 1
                if calc & 0b00001000: key[E] = 1
                if calc & 0b00100000: key[S] = 1
                if calc & 0b10000000: key[W] = 1
                # Corners only if no borders
                if key[N] == 0 and key[E] == 0 and key[S] == 0 and key[W] == 0:
                    if calc & 0b00000001: key[NW] = 1
                    if calc & 0b00000100: key[NE] = 1
                    if calc & 0b00010000: key[SE] = 1
                    if calc & 0b01000000: key[SW] = 1
                # Keycode to string
                if key[Cen3] == 0 and key[Cen2] == 0 and key[Cen1] == 0: suffix = 'water'
                elif key[Cen3] == 0 and key[Cen2] == 0 and key[Cen1] == 1: suffix = 'mud'
                elif key[Cen3] == 0 and key[Cen2] == 1 and key[Cen1] == 0: suffix = 'grass'
                elif key[Cen3] == 0 and key[Cen2] == 1 and key[Cen1] == 1: suffix = 'dry'
                elif key[Cen3] == 1 and key[Cen2] == 0 and key[Cen1] == 0: suffix = 'dark'
                elif key[Cen3] == 1 and key[Cen2] == 0 and key[Cen1] == 1: suffix = 'deep'
                else: raise Exception('Center not known :' + str(key[Cen3]) + str(key[Cen2]) + str(key[Cen1]) + str(type(key[Cen1])))
                if key[Cen3] != key[Opp3] or key[Cen2] != key[Opp2] or key[Cen1] != key[Opp1]:
                    if key[Opp3] == 0 and key[Opp2] == 0 and key[Opp1] == 1: prefix = 'mud'
                    elif key[Opp3] == 0 and key[Opp2] == 1 and key[Opp1] == 0: prefix = 'grass'
                    elif key[Opp3] == 0 and key[Opp2] == 1 and key[Opp1] == 1: prefix = 'dry'
                    elif key[Opp3] == 1 and key[Opp2] == 0 and key[Opp1] == 0: prefix = 'dark'
                    elif key[Opp3] == 1 and key[Opp2] == 0 and key[Opp1] == 1: prefix = 'deep'
                    else: raise Exception('Opposed not know: ' + str(key[Opp3]) + str(key[Opp2]) + str(key[Opp1]))
                else: prefix = ''
                root = ''
                if key[N] == 1: root += 'n'
                if key[E] == 1: root += 'e'
                if key[S] == 1: root += 's'
                if key[W] == 1: root += 'w'
                if key[NW] == 1: root += 'cnw'
                if key[NE] == 1: root += 'cne'
                if key[SE] == 1: root += 'ces'
                if key[SW] == 1: root += 'csw'
                # Variability
                threshold = 90
                if key[Cen3] == key[Opp3] and key[Cen2] == key[Opp2] and key[Cen1] == key[Opp1]:
                    threshold = 50
                frandom = 1
                if random.randint(1, 100) >= threshold:
                    frandom = 2
                if frandom == 1:
                    key[Rand1] = 1
                elif frandom == 2:
                    key[Rand2] = 1
                key = [str(k) for k in key]
                calc = int(''.join(key), 2)
                if root != '' or prefix != '':
                    calc_str = f'{prefix}-{root}-{suffix}-{frandom}'
                else:
                    calc_str = f'{suffix}-1'
                # Set trans map
                self.trans[trow][tcol] = calc_str
                # Save all different values
                if calc not in self.trans_values:
                    self.trans_values[calc] = calc_str
                elif self.trans_values[calc] != calc_str:
                    raise Exception('Computed string keycode does not match the registered one!')
        # Print all transition
        if debug:
            print('All transitions')
            for key, val in self.trans_values.items():
                print(f'\t {val:15s} {key:5d} {key:013b}')
    
    def take_screenshot(self, name=None):
        "Make a picture of the map."
        pygame.init()
        screen = pygame.display.set_mode((100, 100), pygame.DOUBLEBUF, 32)
        paths = [
            r'..\graphic\textures\wyrmsun_32x32\mud_water',
            r'..\graphic\textures\wyrmsun_32x32\dry_mud',
            r'..\graphic\textures\wyrmsun_32x32\grass_mud',
            r'..\graphic\textures\wyrmsun_32x32\dark_grass',
            r'..\graphic\textures\wyrmsun_32x32\deep_water',
            r'..\graphic\textures\wyrmsun_32x32\base',
            r'..\graphic\textures\wyrmsun_32x32\doodads',
        ]
        textures = {}
        for p in paths:
            for f in os.listdir(p):
                texname = os.path.splitext(f)[0]
                textures[texname] = pygame.image.load(p + os.sep + f).convert_alpha()
        surf = pygame.Surface((self.width * 32, self.height * 32))
        for trow in range(0, self.height):
            for tcol in range(0, self.width):
                try:
                    # Background texture
                    surf.blit(textures[self.trans[trow][tcol]], (tcol * 32, trow * 32))
                    # Unit or doodad
                    if self.units[trow][tcol] is not None:
                        surf.blit(textures[self.units[trow][tcol]], (tcol * 32, trow * 32))
                except KeyError:
                    print("[FAIL] Texture not found:")
                    print("...    ", self.trans[trow][tcol], "row =", trow, "col =", tcol)
                    #exit()
        if name is None:
            name = self.name
        pygame.image.save(surf, 'output' + os.sep + name + ".png")
        pygame.quit()
        return
    
    def generate_js(self, file_name, key):
        print('[INFO] Generate JavaScript map in ' + file_name + ' with key ' + key)
        out = open(file_name, mode='w', encoding='utf8')
        out.write('const ' + self.name.upper() + ' = {\n')
        out.write('    name : "' + self.name + '",\n')
        out.write('    content : [\n')
        for irow in range(self.height):
            out.write('        [')
            for icol in range(self.width):
                out.write(str(self.ground[irow][icol]))
                if icol < self.width - 1:
                    out.write(', ')
            out.write('], // ' + f"{irow:02}" + '\n')
        out.write('    ],\n')
        out.write('    width : ' + str(self.width) + ',\n')
        out.write('    height : ' + str(self.height) + ',\n')
        out.write('    triggers : [\n')
        for trig in self.triggers:
            out.write('        {\n')
            out.write("            'conditions' : [\n")
            for i in range(len(trig.conditions)):
                out.write('                ' + str(trig.conditions[i]))
                if i < len(trig.conditions) - 1: out.write(',\n')
                else: out.write('\n')
            out.write("            ],\n")
            out.write("            'actions' : [\n")
            for i in range(len(trig.actions)):
                out.write('                ' + str(trig.actions[i]))
                if i < len(trig.actions) - 1: out.write(',\n')
                else: out.write('\n')
            out.write("            ]\n")
            out.write('        }\n')
        out.write('    ]\n')
        out.write('};\n\n')
        out.write('MAPS["' + key + '"] = load_map(' + self.name.upper() + ');\n')
    
    @staticmethod
    def from_xls(file_name, sheet_name, debug=False):
        wb = xlrd.open_workbook(file_name, formatting_info=1)
        #s = wb.sheets()[0]
        if sheet_name is None:
            s = wb.sheet_by_index(0)
            my_map = Map(wb.sheet_names()[0])
        else:
            s = wb.sheet_by_name(sheet_name)
            my_map = Map(sheet_name)
        tex = []
        uni = []
        lvl = []
        current_level = 0
        for row in range(0, s.nrows):
            cur_tex = []
            cur_uni = []
            cur_lvl = []
            for col in range(0, s.ncols):
                cell = s.cell(row, col)
                style = wb.xf_list[cell.xf_index]
                # Récupération du fond de la cellule
                # Background
                background = style.background.pattern_colour_index
                try:
                    background = TEXTURES[wb.colour_map[background]]
                except KeyError:
                    print('[ERR] Error of texture color')
                    print('Key =', background)
                    print('Color =', wb.colour_map[background])
                    print('Row =', row)
                    print('Col =', col)
                    for col in wb.colour_map:
                        print(col, wb.colour_map[col])
                    exit()
                cur_tex.append(background)
                # Border XFBorder Object
                doodad = None
                if style.border.left_line_style != 0:
                    current_level += 1
                    cur_lvl.append(current_level)
                    if style.border.top_line_style != 0:
                        doodad = 'cliff-nw'
                    elif style.border.bottom_line_style != 0:
                        doodad = 'cliff-sw'
                    else:
                        doodad = 'cliff-w'
                elif style.border.right_line_style != 0:
                    cur_lvl.append(current_level)
                    current_level -= 1
                    if style.border.top_line_style != 0:
                        doodad = 'cliff-ne'
                    elif style.border.bottom_line_style != 0:
                        doodad = 'cliff-es'
                    else:
                        doodad = 'cliff-e'
                else:
                    if style.border.top_line_style != 0:
                        doodad = 'cliff-n'
                    elif style.border.bottom_line_style != 0:
                        doodad = 'cliff-s'
                    cur_lvl.append(current_level)
                if background not in my_map.values:
                    my_map.values.append(background)
                if len(cell.value) != 0:
                    if doodad is not None:
                        raise Exception('No doodad and unit at the same case!')
                    # Récupération du texte de la cellule
                    txt = cell.value
                    #cur_uni.append(cell.value)
                    # Récupération de la couleur de la font
                    font = wb.font_list[style.font_index].colour_index
                    #cur_fnt.append(font.colour_index)
                    try:
                        player = PLAYERS[wb.colour_map[font]]
                    except KeyError:
                        print('[ERR] Error of font color')
                        print('Key =', font)
                        print('Color =', wb.colour_map[font])
                        print('Row =', row)
                        print('Col =', col)
                        for col in wb.colour_map:
                            print(col, wb.colour_map[col])
                        exit()
                    cur_uni.append(Unit(txt, player))
                else:
                    cur_uni.append(doodad)
                    #cur_uni.append('_')
                    #cur_fnt.append('    0')
            tex.append(cur_tex)
            uni.append(cur_uni)
            lvl.append(cur_lvl)
        my_map.ground = tex
        my_map.units = uni
        my_map.level = lvl
        my_map.refresh_size()
        if debug:
            print('Valeurs de textures:')
            for vt in my_map.values:
                print('\t', vt)
        return my_map


class Unit:

    def __init__(self, code, player):
        self.code = code
        self.player = player

#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------

def display(matrix):
    for row in matrix:
        for col in row:
            print(col, end=' ')
        print()


def test(file_name, sheet_name, debug=False):
    wb = xlrd.open_workbook(file_name, formatting_info=1)
    if sheet_name is None:
        s = wb.sheet_by_index(0)
        my_map = Map(wb.sheet_names()[0])
    else:
        s = wb.sheet_by_name(sheet_name)
        my_map = Map(sheet_name)
    if debug:
        print(my_map.name)
    background_values = {}
    font_color_values = {}
    for row in range(0, s.nrows):
        for col in range(0, s.ncols):
            cell = s.cell(row, col)
            style = wb.xf_list[cell.xf_index]
            background = style.background.pattern_colour_index
            if background not in background_values:
                background_values[background] = 1
            else:
                background_values[background] += 1
            if cell.value is not None and cell.value != '':
                font = wb.font_list[style.font_index].colour_index
                if font not in font_color_values:
                    font_color_values[font] = 1
                else:
                    font_color_values[font] += 1
    if debug:
        print('BACKGROUNDS')
        for bgv in sorted(background_values, key=background_values.get, reverse=True):
            nb = background_values[bgv]
            print('\t', 'k=', bgv, 'nb=', nb, 'col=', wb.colour_map[bgv])
        print('FONT COLORS')
        for fnt in sorted(font_color_values, key=font_color_values.get, reverse=True):
            nb = font_color_values[fnt]
            print('\t', 'k=', fnt, 'nb=', nb, 'col=', wb.colour_map[fnt])


def do(file_name, sheet_name, screenshot=False):
    print('[INFO] Opening file', file_name)
    if sheet_name is not None:
        print('[INFO] Opening sheet', sheet_name)
    test(file_name, sheet_name)
    my_map = Map.from_xls(file_name, sheet_name)
    #my_map.output_binary(my_map.name.replace(' ', '_') + '.map')
    my_map.transition(screenshot)
    return my_map


#-------------------------------------------------------------------------------
# Main code
#-------------------------------------------------------------------------------

PRELOAD_FILE = 'maps01.xls'
PRELOAD_SHEETS = ['Archipelago'] # 'IslandHill1' 'Hill1' 'TestBig1' 'TestDarkGrass1' 'TestWaterMudDryGrass1' 'TestWaterMud1' 'TestWaterMud2' 'TestWaterMudGrass1' 'TestWaterMudDry1'
GO = None
SCREENSHOT = False
if __name__ == '__main__':
    if PRELOAD_FILE is None:
        print('[INFO] Searching in', os.getcwd())
        files = os.listdir(os.getcwd())
        files = [f for f in files if f[-4:] == '.xls']
        if len(files) == 0:
            print('[FAIL] No map found in current working directory.')
            exit()
        for i in range(0, len(files)):
            print(f'{i:4d}. {files[i]}')
        if GO is None:
            try:
                num = int(input('Enter the number of the map: '))
            except ValueError:
                print('[FAIL] Enter a number.')
                exit()
        else:
            num = GO
        if num < 0 or num >= len(files):
            print('[FAIL] Wrong map number.')
            exit()
        else:
            file_name = files[i]
            sheet_name = None
        my_map = do(file_name, sheet_name)
        if SCREENSHOT: my_map.take_screenshot()
    else:
        file_name = PRELOAD_FILE
        for sheet_name in PRELOAD_SHEETS:
            my_map = do(file_name, sheet_name)
            if SCREENSHOT: my_map.take_screenshot()
            my_trig = Trigger()
            my_trig.conditions = [
                ['ControlUnits', 4, 0, 0, 1, [1, 31, 7, 31]]
            ]
            my_trig.actions = [
                ['Victory', 'You Win', 'E1M2']
            ]
            my_map.triggers.append(my_trig)
            my_map.generate_js('test.js', 'E1M1')
            my_map.take_screenshot()
