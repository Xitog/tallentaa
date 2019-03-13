#-------------------------------------------------------------------------------
# Import
#-------------------------------------------------------------------------------

import os       # to choose the map
import struct   # to save to a binary format

try:
    import xlrd
except ModuleNotFoundError:
    print('[ERR] Unable to use this script without xlrd.')
    print('[ERR] Install it before with: pip install xlrd')
    exit()

#-------------------------------------------------------------------------------
# Global constants
#-------------------------------------------------------------------------------

TEXTURES = {
    (51, 51, 153) : 0, # ( 83, 141, 213) : 0, # water
    (153, 51, 0) : 1,  # (151,  71,   6) : 1, # mud
    (0, 128, 0) : 2,   # grass
    (128, 128, 0) : 3, # (255, 255, 0) : 3, # sand
    (255, 255, 0) : 9, # (148, 138, 84) : 9, # level
}
TEXTURES_NAMES = {
    0 : 'water',
    1 : 'mud',
    2 : 'grass',
    3 : 'sand',
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

class Map:

    def __init__(self, name):
        self.name = name
        self.ground = []
        self.units = []
        self.width = 0
        self.height = 0

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


def test(name):
    wb = xlrd.open_workbook(name, formatting_info=1)
    s = wb.sheet_by_index(0)
    print(wb.sheet_names()[0])
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
    print('BACKGROUNDS')
    for bgv in sorted(background_values, key=background_values.get, reverse=True):
        nb = background_values[bgv]
        print('\t', 'k=', bgv, 'nb=', nb, 'col=', wb.colour_map[bgv])
    print('FONT COLORS')
    for fnt in sorted(font_color_values, key=font_color_values.get, reverse=True):
        nb = font_color_values[fnt]
        print('\t', 'k=', fnt, 'nb=', nb, 'col=', wb.colour_map[fnt])


def xls2map(name):
    wb = xlrd.open_workbook(name, formatting_info=1)
    #s = wb.sheets()[0]
    s = wb.sheet_by_index(0)
    my_map = Map(wb.sheet_names()[0])
    tex = []
    uni = []
    #fnt = []
    for row in range(0, s.nrows):
        cur_tex = []
        cur_uni = []
        #cur_fnt = []
        for col in range(0, s.ncols):
            cell = s.cell(row, col)
            style = wb.xf_list[cell.xf_index]
            # Récupération du fond de la cellule
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
            if len(cell.value) != 0:
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
                cur_uni.append(None)
                #cur_uni.append('_')
                #cur_fnt.append('    0')
        tex.append(cur_tex)
        uni.append(cur_uni)
        #fnt.append(cur_fnt)
    my_map.ground = tex
    my_map.units = uni
    my_map.refresh_size()
    return my_map

#-------------------------------------------------------------------------------
# Main code
#-------------------------------------------------------------------------------

GO = 0
if __name__ == '__main__':
    print('[INF] Searching in', os.getcwd())
    files = os.listdir(os.getcwd())
    files = [f for f in files if f[-4:] == '.xls']
    if len(files) == 0:
        print('[ERR] No map found in current working directory.')
        exit()
    for i in range(0, len(files)):
        print(f'{i:4d}. {files[i]}')
    if GO is None:
        try:
            num = int(input('Enter the number of the map: '))
        except ValueError:
            print('[ERR] Enter a number.')
            exit()
    else:
        num = GO
    if num < 0 or num >= len(files):
        print('[ERR] Wrong map number.')
        exit()
    else:
        name = files[i]
    print('[INF] Opening', name)
    test(name)
    my_map = xls2map(name)
    my_map.output_binary(my_map.name.replace(' ', '_') + '.map')

