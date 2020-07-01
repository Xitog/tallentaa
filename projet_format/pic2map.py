# -----------------------------------------------------------
# MIT Licence (Expat License Wording)
# -----------------------------------------------------------
# Copyright © 2020, Damien Gouteux
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

from PIL import Image
from os.path import join
from picstat import ImageStat
from datetime import datetime

#-------------------------------------------------------------------------------
# Code
#-------------------------------------------------------------------------------

output = 'matrix' # matrix, image

#target = {'name': 'map1.png', 'origin':'gmap'}
target = {'name': 'map_small.PNG', 'origin': 'osm'}
ims = ImageStat(target['name'])

# Make corresponding pair color logical name / rgb
origins = {
    'gmap': {
        'blue' : (170, 218, 255, 255),
        'grey' : (235, 233, 229, 255),
        'green': (206, 238, 206, 255)
    },
    'osm': {
        'blue' : (170, 211, 223, 255),
        'grey' : (242, 239, 233, 255),
        'green': None
    }
}
assoc = origins[target['origin']]

if output == 'image':
    root = r'C:\Users\DGX\Desktop\Git\tallentaa\projet_tile_grid_editor\mod\rts\graphics'

    dark  = Image.open(join(root, 'dark-1.png')).convert('RGBA')
    grass = Image.open(join(root, 'grass-1.png')).convert('RGBA')
    dry   = Image.open(join(root, 'dry-1.png')).convert('RGBA')
    mud   = Image.open(join(root, 'mud-1.png')).convert('RGBA')
    water = Image.open(join(root, 'water-1.png')).convert('RGBA')
    deep  = Image.open(join(root, 'deep-1.png')).convert('RGBA')

    # Make corresponding pair color logical name / rgb
    origins = {
        'gmap': {
            'blue' : (170, 218, 255, 255),
            'grey' : (235, 233, 229, 255),
            'green': (206, 238, 206, 255)
        },
        'osm': {
            'blue' : (170, 211, 223, 255),
            'grey' : (242, 239, 233, 255),
            'green': None
        }
    }

    print('Resources loaded')

    print('Generating map')
    start = datetime.now()

    res = Image.new('RGBA', (ims.width * 32, ims.height * 32), 'black')

    count = 0
    old_percent = 0
    for col in range(ims.width):
        for row in range(ims.height):
            pix = ims.getpixel(col, row)
            if pix == assoc['blue']:
                res.paste(water, (col * 32, row * 32))
            elif pix == assoc['grey']: # gris
                res.paste(mud, (col * 32, row * 32))
            elif pix == assoc['green']: # vert
                res.paste(grass, (col * 32, row * 32))
            else:
                res.paste(mud, (col * 32, row * 32))
            count += 1
            percent = count / ims.total * 100
            if int(percent) > old_percent:
                print(int(percent), '%')
                old_percent = int(percent)

    end_gen = datetime.now()

    print('Saving')

    res.save('res.png')

    end_sav = datetime.now()

    print(f'It took {end_gen-start} to generate.')
    print(f'It took {end_sav-end_gen} to save.')
    print(f'It took {end_sav-start} in total.')
elif output == 'matrix':
    
    DEEP  = 0b00000000 #  0
    WATER = 0b00010000 # 16
    MUD   = 0b00100000 # 32
    DRY   = 0b00110000 # 48
    GRASS = 0b01000000 # 64
    DARK  = 0b01010000 # 80
    
    res = open('ouput.py', 'w')
    res.write('mymap = [\n')
    for col in range(ims.width):
        res.write('    [')
        for row in range(ims.height):
            pix = ims.getpixel(col, row)
            if pix == assoc['blue']:
                res.write(str(WATER) + ', ')
            elif pix == assoc['grey']: # gris
                res.write(str(MUD) + ', ')
            elif pix == assoc['green']: # vert
                res.write(str(GRASS) + ', ')
            else:
                res.write(str(MUD) + ', ')
        res.write('],\n')
    res.write(']\n')
    res.close()
else:
    raise Exception(f'Unknown mode: {output}')
