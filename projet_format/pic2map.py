from PIL import Image
from os.path import join
from picstat import ImageStat
from datetime import datetime

root = r'C:\Users\DGX\Desktop\Git\tallentaa\projet_tile_grid_editor\mod\rts\graphics'

dark = Image.open(join(root, 'dark-1.png')).convert('RGBA')
grass = Image.open(join(root, 'grass-1.png')).convert('RGBA')
dry = Image.open(join(root, 'dry-1.png')).convert('RGBA')
mud = Image.open(join(root, 'mud-1.png')).convert('RGBA')
water = Image.open(join(root, 'water-1.png')).convert('RGBA')
deep = Image.open(join(root, 'deep-1.png')).convert('RGBA')

ims = ImageStat('map1.png')

print('Resources loaded')
print('Generating map')
start = datetime.now()

res = Image.new('RGBA', (ims.width * 32, ims.height * 32), 'black')

count = 0
old_percent = 0
for col in range(ims.width):
    for row in range(ims.height):
        pix = ims.getpixel(col, row)
        if pix == (170, 218, 255, 255): # blue
            res.paste(water, (col * 32, row * 32))
        elif pix == (235, 233, 229, 255): # gris
            res.paste(mud, (col * 32, row * 32))
        elif pix == (206, 238, 206, 255): # vert
            res.paste(grass, (col * 32, row * 32))
        else:
            pass
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
