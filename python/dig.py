# -*- coding: utf-8 -*-
# Dig!

# Tron STR

# Import
import pygame
from pygame.locals import *

# Init
pygame.init()
pygame.display.set_caption('Dig Edit')

MAXX = 1024 #800
MAXY = 768  #600
resolution = (MAXX,MAXY)
flags = pygame.DOUBLEBUF
screen = pygame.display.set_mode(resolution,flags,32)

escape = False
clock = pygame.time.Clock()

v = 1
n = 32
s = 32
lvl = [[v]*n for x in xrange(n)]
alt = [[0]*n for x in xrange(n)]

act = False

item = 'Water'
mode = 'Texture'

MAPX = 100
MAPY = 0

textures = {
    'Désert' : '1_Desert.bmp',
    'Water' : '2_Basic2.png',
    'Vallée Haut Gauche' : '11_HG.bmp',
    'Vallée Haut Milieu ou Montagne Bas Milieu' : '12_HM.bmp',
    'Vallée Haut Droit' : '13_HD.bmp',
    'Vallée Milieu Droit ou Montagne Milieu Gauche' : '14_MD.bmp',
    'Vallée Bas Droit' : '15_BD.bmp',
    'Vallée Bas Milieu ou Montagne Haut Milieu' : '16_BM.bmp',
    'Vallée Bas Gauche' : '17_BG.bmp',
    'Vallée Milieu Gauche ou Montagne Milieu Droit' : '18_MG.bmp',
    'Montagne Haut Gauche' : '20_Montagne_HG.bmp',
    'Montagne Haut Droit' : '21_Montagne_HD.bmp',
    'Montagne Bas Droit' : '22_Montagne_BD.bmp',
    'Montagne Bas Gauche' : '23_Montagne_BG.bmp',
    'MX HG' : '111_HG.png',
    'MX HM' : '112_HM.png',
    'MX HD' : '113_HD.png',
    'MX MD' : '114_MD.png',
    'MX BD' : '115_BD.png',
    'MX BM' : '116_BM.png',
    'MX BG' : '117_BG.png',
    'MX MG' : '118_MG.png',
    
    'ZZ HG' : '121_HG.png',
    'ZZ HD' : '123_HD.png',
    'ZZ BD' : '125_BD.png',
    'ZX BG' : '127_BG.png',
}

doodads = {
    'Desert Tree 1' : '101_DesertTree1.png',
    'Desert Tree 2' : '102_DesertTree2.png',
    'Desert Tree 3' : '103_DesertTree3.png'
}

modes = {'Texture': textures, 'Doodad':doodads, 'Object': {}}

keys = textures.keys()
kk = 0

class Texture:
    def __init__(self, filename, alpha=255):
        try:
            s = filename.rstrip('.bmp')
            s = s.rstrip('.png')
            elements = s.split('_') #filename.rstrip('.bmp').split('_')
            self.id = int(elements[0])
            elements = elements[1:]
            self.name = ' '.join(elements)
            self.surf = pygame.image.load(filename).convert()
            self.surf.set_colorkey((255,0,255))
            self.surf.set_alpha(alpha)
            self.x = self.surf.get_size()[0]
            self.y = self.surf.get_size()[1]
            print 'Loaded ressource %s @%s as %s %dx%d' % (filename,self.id, self.name, self.x, self.y)
        except pygame.error as e:
            print 'Load error %s : %s' % (filename, str(e))

selector = Texture('0_Selector.png', 192)

quick = {}

for k in modes:
    print '----> Loading %s' % (k,)
    for i in modes[k]:
        t = Texture(modes[k][i])
        modes[k][i] = t
        quick[t.id] = t.surf

print "Mode: ", mode
print "Item: ", item

import sys

pygame.mouse.set_pos([400,300])

cam_x = 0
cam_y = 0
pres = 10

activated = False
"""
class RefInteger:
    def __init__(self, val):
        self.val = val
    def get(self):
        return self.val
    def set(self, val):
        self.val = val
"""

def around(x,y,s):
    xstart = x-s
    xend = x+s
    ystart = y-s
    yend = y+s
    xx = xstart
    yy = ystart
    l = []
    while xx <= xend:
        while yy <= yend:
            print '(', x,y,')', xx, '/', xend, yy, '/', yend
            if yy >= 0 and xx >= 0 and yy < n and xx < n and (yy != y or xx != x):
                l.append(yy+xx*n)#append(alt[yy][xx])
            yy += 1
        xx += 1
        yy = ystart
    for e in l:
        print '>>', e
    return l

#alt = [[RefInteger(0)]*n for x in range(n)]

def decode(v):
    return v/32, v-(v/32)*32

def impact(x,y,v):
    alt[y][x] = v
    #lst0 = around(x,y,2)
    #for e in lst0:
    #    xx, yy = decode(e)
    #    if alt[yy][xx] == 2:

    lst = around(x,y,1)
    for e in lst:
        xx, yy = decode(e)
        if alt[yy][xx] == 0:
            alt[yy][xx] = v/2
        elif alt[yy][xx] == v/2:
            check(xx,yy)
        #print id(e)
        #if e.get() == 0:
        #    e.set(v/2)

def print_map():
    print ">>> Map"
    for i in range(0, n):
        for j in range(0, n):
            sys.stdout.write(str(alt[i][j])) #sys.stdout.write(str(lvl[i][j]))
        print

def check(x,y):
    if y > 1 and x > 1 and y < n-1 and x < n-1 and alt[y-1][x-1] == 2 and alt[y+1][x+1] == 2 and alt[y+1][x-1] != 2:
    #    print "Diag G-D"
    #    #print_map()
    #    #raw_input()
        alt[y][x] = 2
        impact(x,y,2)
    if y > 1 and y < n-1 and alt[y-1][x] == 2 and alt[y+1][x] == 2:
        print "Verticale"
        #print_map()
        #raw_input()
        alt[y][x] = 2
        impact(x,y,2)
    if y > 1 and x < n-1 and alt[y-1][x+1] == 2 and alt[y+1][x-1] == 2 and alt[y-1][x+1] != 2:
    #    print "Diag D-G"
    #    #print_map()
    #    #raw_input()
        alt[y][x] = 2
        impact(x,y,2)
    if x > 1 and x < n-1 and alt[y][x-1] == 2 and alt[y][x+1] == 2:
        print "Horizontale"
        #print_map()
        #raw_input()
        alt[y][x] = 2
        impact(x,y,2)

# 19h00 semble OK
# 19h05 : corrigé un bug de diagonale et finalement, pas besoin des diagonales !!!!
# 19h24 : si il les faut. Il faut juste ne pas en faire qu'en s'est déjà relié par le point inverse. Putain quel algo !

font = pygame.font.SysFont(pygame.font.get_default_font(), 16)

surfmap = pygame.Surface((MAXX-MAPX, MAXY-MAPY))
menu = pygame.Surface((MAPX,MAXY))

# 15h31 : python de référence à la con !!! J'obtenais vraiment un truc louche (du style il modifiait plusieurs objets !!!)
# 

def get(k):
    x,y = decode(k)
    return alt[y][x]

def key(x,y):
    return y+x*n

for k in quick:
    print k, k.__class__, quick[k]

# Main loop
while not escape:
    
    m = pygame.mouse.get_pos()
    mx = m[0]
    my = m[1]
    mxg = (m[0]-cam_x-MAPX)/s
    myg = (m[1]-cam_y-MAPY)/s
    if mxg < 0: mxg = 0
    elif mxg > 31: mxg = 31
    if myg < 0: myg = 0
    elif myg > 31 : myg = 31

    if activated:    
        if mx < pres:
            cam_x += 1
        elif mx > MAXX-pres:
            cam_x -= 1
        if my < pres:
            cam_y += 1
        elif my > MAXY-pres:
            cam_y -= 1
    
    #print 'MX:',m[0],'MY:',m[1],'GridX:',mxg,'GridY:',myg, 'CamX:',cam_x, 'CamY:',cam_y
    
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            escape = True
        if event.type == MOUSEMOTION:
            activated = True
        if event.type == MOUSEBUTTONDOWN:
            #print event.button
            if event.button == 1:
                act = True
            elif event.button == 2:
                pass
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                act = False
            elif event.button == 2:
                print_map()
            elif event.button == 4:
                kk+=1
                kk%=len(textures)
                item = keys[kk] #textures[keys[kk]]                
                print item
                #if item == 'Grass': item = 'Water'
                #else: item = 'Grass'
                #print item
            elif event.button == 5:
                kk-=1
                if kk < 0: kk=len(textures)-1
                item = keys[kk]
                print item

        if act:
            impact(mxg, myg, 2)
            lvl[myg][mxg] = modes[mode][item].id

    # Update
    # Draw
    screen.fill((128,128,128))

    # Menu
    
    menu.fill((0,0,255))
    i = 0
    j = 0
    for ee in quick:
        sf = font.render("FUCK", True, (255,0,0))
        menu.blit(sf, (0,0))
        #screen.blit(sf, (0,0))
        menu.blit(quick[ee], (i*s, j*s))
        i+=1
        if i%3 == 0:
            i=0
            j+=1
    screen.blit(menu, (0,0))

    # Game
    
    surfmap.fill((0,0,0))
    
    for i in range(0, n):
        for j in range(0, n):
            if j*s+cam_y > MAXY: break
            #surfmap.blit(quick[lvl[j][i]], (i*s+cam_x,j*s+cam_y))
            if alt[j][i] == 1:
                #surfmap.blit(quick['1'], (i*s+cam_x,j*s+cam_y))
                hg = key(i-1,j-1)
                mh = key(i,j-1)
                hd = key(i+1,j-1)
                md = key(i+1, j)
                bd = key(i+1, j+1)
                mb = key(i, j+1)
                bg = key(i-1, j+1)
                mg = key(i-1, j)
                #all = [hg, mh, hd, md, bd, mb, bg, mg]
                #opposes = { hg : bd, mh : mb, hd : bg, mg : md }
                if get(mg) == 2:
                    if get(hg) == 2 and get(mh) == 2:
                        surfmap.blit(quick[125], (i*s+cam_x,j*s+cam_y))
                    elif get(hd) == 2 and get(mh) == 2:
                        surfmap.blit(quick[123], (i*s+cam_x,j*s+cam_y))
                    else:
                        surfmap.blit(quick[114], (i*s+cam_x,j*s+cam_y))
                elif get(md) == 2:
                    if get(hg) == 2 and get(mh) == 2:
                        surfmap.blit(quick[123], (i*s+cam_x,j*s+cam_y))
                    elif get(hd) == 2 and get(mh) == 2:
                        surfmap.blit(quick[125], (i*s+cam_x,j*s+cam_y))
                    else:
                        surfmap.blit(quick[118], (i*s+cam_x,j*s+cam_y))
                elif get(mh) == 2:
                    if get(mg) == 2 and get(mb) == 2:
                        surfmap.blit(quick[123], (i*s+cam_x,j*s+cam_y))
                    elif get(md) == 2 and get(mb) == 2:
                        surfmap.blit(quick[127], (i*s+cam_x,j*s+cam_y))
                    else:
                        surfmap.blit(quick[116], (i*s+cam_x,j*s+cam_y))
                elif get(mb) == 2:
                    if get(md) == 2 and get(mb) == 2:
                        surfmap.blit(quick[127], (i*s+cam_x,j*s+cam_y))
                    elif get(mg) == 2 and get(mb) == 2:
                        surfmap.blit(quick[123], (i*s+cam_x,j*s+cam_y))
                    else:
                        surfmap.blit(quick[112], (i*s+cam_x,j*s+cam_y))
                elif get(hg) == 2:
                    surfmap.blit(quick[125], (i*s+cam_x,j*s+cam_y))
                elif get(hd) == 2:
                    surfmap.blit(quick[127], (i*s+cam_x,j*s+cam_y))
                elif get(bg) == 2:
                    surfmap.blit(quick[123], (i*s+cam_x,j*s+cam_y))
                elif get(bd) == 2:
                    surfmap.blit(quick[121], (i*s+cam_x,j*s+cam_y))
            sf = font.render(str(alt[j][i]), True, (255,0,0))
            surfmap.blit(sf, (i*s+cam_x,j*s+cam_y))
        if i*s+cam_x > MAXX: break
    
    screen.blit(surfmap, (MAPX, MAPY))
    
    surfmap.blit(selector.surf, (mxg*s+cam_x, myg*s+cam_y))

    pygame.display.flip()
    
    # Limit to 60 fps maximum
    clock.tick(60)

