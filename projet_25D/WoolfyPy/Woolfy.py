# http://lodev.org/cgtutor/raycasting.html ***
# http://lodev.org/cgtutor/files/raycaster_flat.cpp ***
# http://www.cplusplus.com/reference/clibrary/cmath/fabs/
# http://www.student.kuleuven.be/~m0216922/CG/raycasting.html
# http://www.pygame.org/docs/tut/newbieguide.html
# http://www.permadi.com/tutorial/raycast/
#   http://www.permadi.com/tutorial/raycast/rayc8.html distorsion
# http://cython.org/

# Import
import pygame
import math
import time

from pygame.locals import *
from pygame import Surface
from datetime import datetime

#sprite1 = pygame.image.load('flower.png').convert()
#sprite1.set_colorkey((255,0,255))

def tile2color(index : int):
    """
        Get a color for a tile in the map
        Authorized input values: 1, 2, 3, 4, 5, 6, 7
    """
    color : (int, int, int) = (255, 255, 0)
    if index == 1:
        color = (255, 0, 0)
    elif index == 2:
        color = (0, 255, 0)
    elif index == 3:
        color = (0, 0, 255)
    elif index == 4:
        color = (255, 255, 255)
    elif index == 5:
        color = (120, 120, 120)
    elif index == 6:
        color = (120, 0, 120)
    elif index == 7:
        color = (0, 0, 120)
    return color


def color2string(color : (int, int, int)):
    """Get a describing string for a color"""
    if color == (255, 255, 255):
        return 'white'
    elif color == (255, 0, 0):
        return 'red'
    elif color == (0, 255, 0):
        return 'green'
    elif color == (0, 0, 255):
        return 'blue'
    elif color == (120, 120, 120):
        return 'grey'
    elif color == (120, 0, 120):
        return 'dark purple'
    elif color == (0, 0, 120):
        return 'dark blue'
    else:
        return str(color)


class Level:
    
    def __init__(self, name : str, area : [[int]]):
        self.name : str = name
        self.area : [[int]] = area
        self.height :int = len(area)
        if self.height == 0:
            raise Exception("Empty map")
        self.width : int = len(area[0])


class Application:
    """
        FPS 2.5D
        movement : up, down, right, left arrow
        run : left shit
        map : tab
        restart : enter
        texture wall or not : T
        exit : escape
    """
    
    def load_texture(self, filename : str, where : int):
        # Load
        s : Surface = pygame.image.load(filename)
        z : [int] = []
        for i in range(0, self.TEXTURE_MAX):
            z.append(0)
        i = 0
        if s.get_height() != 64 or s.get_width() != 64:
            raise Exception("Wrong texture size")
        for ii in range(0, s.get_height()):
            for jj in range(0, s.get_width()):
                t = tuple(s.get_at((jj,ii)))
                z[i] = t[0] * 256 * 256 + t[1] * 256 + t[2]
                i+=1
                #print("%s for %s" % (z[i-1],i-1))
        self.textures[where] = z
    
    def __init__(self):
        
        self.level : Level = Level("Test map 01", [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,2,2,2,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1],
            [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,3,0,0,0,3,0,0,0,1],
            [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,2,2,0,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,5,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,7,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,7,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,7,0,0,0,0,1],
            [1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,4,0,0,0,0,5,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,4,0,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ])
        
        self.screen_width : int = 640  #300 320 640
        self.screen_height : int = 480 #200 240 480
        self.half_height : int = self.screen_height // 2
        self.FPS : int = 60
        
        pygame.init()
        pygame.display.set_caption('Woolfy 3D')
        resolution : (int, int) = (800,600)
        flags : int = pygame.DOUBLEBUF
        print(pygame.display.mode_ok(resolution))
        # 0 : not ok, !0: best color depth
    
        self.screen : Surface = pygame.display.set_mode(resolution, flags, 32)
        self.screen_buffer : Surface = Surface((self.screen_width, self.screen_height))
        #clock = pygame.time.Clock()
    
        self.position : [float, float] = [22.0,12.0]      # position vector (point)
        self.direction : [float, float] = [-1.0,0.0]      # direction vector
        self.camera : [float, float] = [0.0, 0.66]        # camera plane (orthogonal to direction vector) 2 * atan(0.66/1.0)=66
        
        self.modx : float = 0.0
        self.mody : float = 0.0
        
        self.escape : bool = False
        self.show_minimap : bool = False
    
        self.right : bool   = False
        self.left : bool    = False
        self.up : bool      = False
        self.down : bool    = False
        self.running : bool = False
        
        self.wall_buffer : [int] = []
    
        self.ROTATION_FACTOR : float = 1.5 # 3.0
        self.MOVEMENT_FACTOR : float = 3.0 # 5.0
        self.RUNNING_FACTOR : float  = 4.5
        
        self.CEILING_COLOR : (int, int, int) = (115, 115, 115)
        self.FLOOR_COLOR : (int, int, int) = (230, 230, 230)
        
        self.TEXTURED_WALL : bool = False
        self.TEXTURE_WIDTH : int  = 64
        self.TEXTURE_HEIGHT : int = 64
        self.TEXTURE_MAX : int = self.TEXTURE_WIDTH * self.TEXTURE_HEIGHT # 4096
        
        self.textures : [[int]] = [[0]]
        self.load_texture("tex.bmp", 0)
        
        for s in range(0, self.screen_width):
            self.wall_buffer.append(0)

        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 20)

    
    def restart(self):
        self.position = [22.0,12.0]
        self.direction = [-1.0,0.0]
        self.camera = [0.0, 0.66]
    

    def wait_for_key(self, key, **values):
        for k, v in values.items():
            print(k, v)
        loop = True
        while loop:
            for event in pygame.event.get():
                if event.type == KEYUP:
                    if event.key == K_SPACE:
                        loop = False
    
    def update(self):
        """Handle events"""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.escape = True
            elif event.type == KEYDOWN:
                # hud
                if event.key == K_ESCAPE:
                    self.escape = True
                if event.key == K_TAB:
                    self.show_minimap = True
                # movement
                if event.key == K_RIGHT:
                    self.right = True
                if event.key == K_LEFT:
                    self.left = True
                if event.key == K_UP:
                    self.up = True
                if event.key == K_DOWN:
                    self.down = True
                if event.key == K_LSHIFT:
                    self.running = True
            elif event.type == KEYUP:
                # hud
                if event.key == K_TAB:
                    self.show_minimap = False
                # debug
                if event.key == K_RETURN:
                    self.restart()
                if event.key == K_t:
                    self.TEXTURED_WALL = not self.TEXTURED_WALL
                # movement
                if event.key == K_RIGHT:
                    self.right = False
                if event.key == K_LEFT:
                    self.left = False
                if event.key == K_UP:
                    self.up = False
                if event.key == K_DOWN:
                    self.down = False
                if event.key == K_LSHIFT:
                    self.running = False
                # debug
                if event.key == K_SPACE:
                    print('Writing dump of screen')
                    tag = datetime.now().strftime('%Y-%m-%d_%Hh%Mm%S')
                    f = open(tag + '_dump.txt', 'w')
                    for s in range(0, width):
                        f.write(str(s) + '. color= ' + color2string(buffer[s][0]) + ', startDraw= ' + str(buffer[s][1]) + ', startEnd= ' + str(buffer[s][2]) + '\n')
                    f.close()
        
        self.rotSpeed : float = self.frameTime * self.ROTATION_FACTOR
        self.moveSpeed : float = self.frameTime * self.MOVEMENT_FACTOR
        if self.running:
            self.moveSpeed = self.frameTime * self.RUNNING_FACTOR
        
        # rotate to the right
        if self.left:
            # both camera direction and camera plane must be rotated
            oldDirX = self.direction[0]
            self.direction[0] = self.direction[0] * math.cos(-self.rotSpeed) - self.direction[1] * math.sin(-self.rotSpeed)
            self.direction[1] = oldDirX * math.sin(-self.rotSpeed) + self.direction[1] * math.cos(-self.rotSpeed)
            oldPlaneX = self.camera[0]
            self.camera[0] = self.camera[0] * math.cos(-self.rotSpeed) - self.camera[1] * math.sin(-self.rotSpeed)
            self.camera[1] = oldPlaneX * math.sin(-self.rotSpeed) + self.camera[1] * math.cos(-self.rotSpeed)
        if self.right:
            # both camera direction and camera plane must be rotated
            oldDirX = self.direction[0]
            self.direction[0] = self.direction[0] * math.cos(self.rotSpeed) - self.direction[1] * math.sin(self.rotSpeed)
            self.direction[1] = oldDirX * math.sin(self.rotSpeed) + self.direction[1] * math.cos(self.rotSpeed)
            oldPlaneX = self.camera[0]
            self.camera[0] = self.camera[0] * math.cos(self.rotSpeed) - self.camera[1] * math.sin(self.rotSpeed)
            self.camera[1] = oldPlaneX * math.sin(self.rotSpeed) + self.camera[1] * math.cos(self.rotSpeed)
        if self.down:
            try:        
                if self.level.area[int(self.position[0] + self.direction[0] * self.moveSpeed)][int(self.position[1])] == False:
                    self.position[0] += self.direction[0] * self.moveSpeed
                if self.level.area[int(self.position[0])][int(self.position[1] + self.direction[1] * self.moveSpeed)] == False:
                    self.position[1] += self.direction[1] * self.moveSpeed
            except Exception as e:
                print(int(self.position[0] + self.direction[0] * self.moveSpeed))
                print(int(self.position[1] + self.direction[1] * self.moveSpeed))
                print(e)
        if self.up:
            if self.level.area[int(self.position[0] - self.direction[0] * self.moveSpeed)][int(self.position[1])] == False:
                self.position[0] -= self.direction[0] * self.moveSpeed
            if self.level.area[int(self.position[0])][int(self.position[1] - self.direction[1] * self.moveSpeed)] == False:
                self.position[1] -= self.direction[1] * self.moveSpeed
    
    
    def draw(self):
        """Draw"""
        #self.screen.fill((0,0,0))
        #screen.blit(sprite1, (100, 100))
        
        # Background
        #------------
        pygame.draw.rect(self.screen_buffer, self.CEILING_COLOR, (0, 0, self.screen_width, self.half_height), 0)
        pygame.draw.rect(self.screen_buffer, self.FLOOR_COLOR, (0, self.half_height, self.screen_width, self.half_height), 0)
        
        # Raytracing 2.5D
        #-----------------
        for s in range(0, self.screen_width):
            # calculate ray position and direction 
            cameraX = 2 * s / float(self.screen_width) - 1 #x-coordinate in camera space
            rayDirX = self.direction[0] + self.camera[0] * cameraX
            rayDirY = self.direction[1] + self.camera[1] * cameraX
            
            # which box of the map we're in  
            mapX = int(self.position[0]); # rayPosX
            mapY = int(self.position[1]); # rayPosY
            
            # length of ray from current position to next x or y-side
            sideDistX = 0.0
            sideDistY = 0.0
            
            # Added by me
            if rayDirX == 0: rayDirX = 0.00001
            if rayDirY == 0: rayDirY = 0.00001
            
            #length of ray from one x or y-side to next x or y-side
            deltaDistX = math.sqrt(1 + (rayDirY * rayDirY) / (rayDirX * rayDirX))
            deltaDistY = math.sqrt(1 + (rayDirX * rayDirX) / (rayDirY * rayDirY))
            perpWallDist = 0.0
           
            # what direction to step in x or y-direction (either +1 or -1)
            stepX = 0
            stepY = 0
            
            hit = 0 # was there a wall hit?
            side = 0 # was a NS or a EW wall hit?
            
            # calculate step and initial sideDist
            if rayDirX < 0:
                stepX = -1
                sideDistX = (self.position[0] - mapX) * deltaDistX
            else:
                stepX = 1
                sideDistX = (mapX + 1.0 - self.position[0]) * deltaDistX
            if rayDirY < 0:
                stepY = -1
                sideDistY = (self.position[1] - mapY) * deltaDistY
            else:
                stepY = 1
                sideDistY = (mapY + 1.0 - self.position[1]) * deltaDistY

            # perform DDA
            while hit == 0:
                # jump to next map square, OR in x-direction, OR in y-direction
                if sideDistX < sideDistY:
                    sideDistX += deltaDistX
                    mapX += stepX
                    side = 0
                else:
                    sideDistY += deltaDistY
                    mapY += stepY
                    side = 1
                # Check if ray has hit a wall
                if self.level.area[mapX][mapY] > 0: hit = 1
            
            # Calculate distance projected on camera direction (oblique distance will give fisheye effect!)
            if side == 0:
                perpWallDist = abs((mapX - self.position[0] + (1 - stepX) / 2) / rayDirX) # fabs
            else:
                perpWallDist = abs((mapY - self.position[1] + (1 - stepY) / 2) / rayDirY) # fabs
            
            # Added by me
            if perpWallDist == 0: perpWallDist = 0.00001
            
            # Calculate height of line to draw on screen
            lineHeight = int(float(self.screen_height) / float(perpWallDist))

            #self.wait_for_key(K_SPACE, rayDirX=rayDirX, rayDirY=rayDirY, stepX=stepX, stepY=stepY, perpWallDist=perpWallDist, lineHeight=lineHeight)
            
            # Calculate lowest and highest pixel to fill in current stripe
            drawStart = int(-lineHeight / 2 + self.half_height)
            if drawStart < 0: drawStart = 0
            drawEnd = int(lineHeight / 2 + self.half_height)
            if drawEnd >= self.screen_height: drawEnd = self.screen_height - 1
            
            # choose wall color and store color and drawStart and drawEnd
            self.wall_buffer[s] = (
                tile2color(self.level.area[mapX][mapY]),
                drawStart,
                drawEnd,
                # for texture
                perpWallDist,
                rayDirX,
                rayDirY,
                lineHeight,
                side
            )
        
        # Walls drawing
        #-------------------
        if self.TEXTURED_WALL:
            quick_buffer = pygame.PixelArray(self.screen_buffer)
            for column in range(0, self.screen_width):
                color = self.wall_buffer[column][0]
                draw_start = self.wall_buffer[column][1]
                draw_end = self.wall_buffer[column][2]
                perp_wall_dist = self.wall_buffer[column][3]
                ray_dir_x = self.wall_buffer[column][4]
                ray_dir_y = self.wall_buffer[column][5]
                line_height = self.wall_buffer[column][6]
                side = self.wall_buffer[column][7]
                
                # where exactly the wall was hit
                wall_x = 0.0
                if side == 0:
                    wall_x = self.position[1] + perp_wall_dist * ray_dir_y
                else:
                    wall_x = self.position[0] + perp_wall_dist * ray_dir_x
                wall_x -= math.floor(wall_x)
                
                # x coordinate on the texture
                texX = int(wall_x * float(self.TEXTURE_WIDTH))
                
                if side == 0 and ray_dir_x > 0: texX = self.TEXTURE_WIDTH - texX - 1
                if side == 1 and ray_dir_y < 0: texX = self.TEXTURE_WIDTH - texX - 1
                
                # ME BICOLOR TEXTURE
                # if texX > 32: color = ((color[0]+100)%255,color[1],color[2])
                
                ## ME Now y
                for yy in range(draw_start, draw_end):
                    dd = yy * 256 - self.screen_height * 128 + line_height * 128 # 256 and 128 factors to avoid floats
                    texY = int(((dd * self.TEXTURE_HEIGHT) / line_height) / 256)
                    # ME Hum... Normalement les textures font 64 !!!
                    if texY < 0 or texY > 63:
                        if texY < 0:
                            texY = 64 + texY
                        else:
                            texY = texY & 63
                    # get pixel color from texture
                    color = 0
                    pixel = int(self.TEXTURE_HEIGHT * texY + texX)
                    if 0 <= pixel < self.TEXTURE_MAX:
                        color = self.textures[0][pixel]
                    else:
                        raise Exception("Pixel = " + str(pixel) + ", texX = " + str(texX) + ", texY = " + str(texY))
                    # make color darker for y-sides: R, G and B byte each divided through two with a "shift" and an "and"              
                    if side == 1: color = (int(color) >> 1) & 8355711
                    try:
                        #self.screen.set_at((column, yy), color)
                        quick_buffer[column, yy] = color
                    except TypeError: # Py3.0 no need now
                        print("Color ERROR : " + str(color))
            del quick_buffer
        else:
            for column in range(0, self.screen_width):
                color = self.wall_buffer[column][0]
                draw_start = self.wall_buffer[column][1]
                draw_end = self.wall_buffer[column][2]
                pygame.draw.line(self.screen_buffer, color, (column, draw_start), (column, draw_end), 1)
        
        # Show minimap and player
        #-------------------------
        if self.show_minimap:
            REPX = 320
            REPY = 10
            SIZE = 10
            for i in range(0, self.level.height):
                line = self.level.area[i]
                for j in range(0, self.level.width):
                    rx = i * SIZE + REPX
                    ry = (len(line) - j) * SIZE + REPY # Y AXIS INVERTED
                    color = tile2color(line[j])
                    pygame.draw.rect(self.screen_buffer, color, (rx,ry,SIZE,SIZE),0)
                    pygame.draw.rect(self.screen_buffer, (0, 0, 0), (rx, ry, SIZE, SIZE), 1)

            pos_x = int(self.position[0]*SIZE + REPX)
            pos_y = self.level.height*SIZE-int(self.position[1]*SIZE) + REPY # Y AXIS INVERTED
            pygame.draw.rect(self.screen_buffer, (255,0,0), (pos_x, pos_y, SIZE, SIZE), 0)    
            #screen.set_at((pos_x,pos_y), (255,0,0))
            dir_x = pos_x+SIZE/2+self.direction[0]*SIZE
            dir_y = pos_y+SIZE/2-self.direction[1]*SIZE # Y AXIS INVERTED
            pygame.draw.line(self.screen_buffer, (255,0,0), (pos_x+SIZE/2, pos_y+SIZE/2), (dir_x, dir_y), 1)

        # Information
        #-------------
        s : Surface = self.font.render("camera = " + '%.3f' % self.camera[0] + " || " + '%.3f' % self.camera[1], True, (255, 0, 255), (255, 255, 255))
        self.screen_buffer.blit(s, (0, 0))
        s = self.font.render("position = " + '%.3f' % self.position[0] + " || " + '%.3f' % self.position[1], True, (255, 255, 0), (0, 0, 0))
        self.screen_buffer.blit(s, (0, 20))
        
        # Display backbuffer
        self.screen.blit(self.screen_buffer, (0,0))
        pygame.display.flip()
        
        
    def run(self):
        """Main loop"""
        while not self.escape:
            start = time.time()
            self.draw()
            end = time.time()
            self.frameTime : int = start - end
            self.update()


if __name__ == '__main__':
    Application().run()
    pygame.quit()
