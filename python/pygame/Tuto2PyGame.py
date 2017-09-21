#-----------------------------------------------------------------------
# Import
#-----------------------------------------------------------------------

import pygame               # L'import principal
from pygame.locals import * # Les codes des touches du clavier

#-----------------------------------------------------------------------
# Start
#-----------------------------------------------------------------------

class Application:
    
    def __init__(self, title, width, height, fps=30):
        pygame.init()
        pygame.display.set_caption(title)
        
        resolution = (width, height)
        flags = pygame.DOUBLEBUF
        best_color_depth = pygame.display.mode_ok(resolution) # 0 = not ok
        
        self.fps = fps
        self.escape = False
        self.screen = pygame.display.set_mode(resolution,flags, best_color_depth)
        self.clock = pygame.time.Clock()

    def update(self):
        pass

    def draw(self):
        pass
    
    def stop(self):
        self.escape = True

    def fill(self, color):
        self.screen.fill(color)

    def rect(self, x, y, w, h, color):
        pygame.draw.rect(self.screen, color, (x, y, w, h), 0)
    
    def run(self):
        while not self.escape:
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.fps) # Limit to x fps maximum

#-----------------------------------------------------------------------
# Specific
#-----------------------------------------------------------------------

area = [[1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,1,1,1,0,1,0,1,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1]]
MOD = 200
SIZE = 10
position = [1,1]        # position vector (point)

class Test(Application):

    def __init__(self):
        Application.__init__(self, 'Tutoriel PyGame', 800, 600)
        self.modx = 0
        self.mody = 0
        
    def update(self):
        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                self.stop()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self.stop()
            elif event.type == KEYDOWN and event.key == K_LEFT:
                self.modx = -1
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                self.modx = 1
            elif event.type == KEYDOWN and event.key == K_UP:
                self.mody = -1
            elif event.type == KEYDOWN and event.key == K_DOWN:
                self.mody = 1
            elif event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_RIGHT:
                    self.modx = 0
                elif event.key == K_DOWN or event.key == K_UP:
                    self.mody = 0
        # Update
        if (area[position[1] + self.mody][position[0] + self.modx] == 0):
            position[0] += self.modx
            position[1] += self.mody
    
    def draw(self):
        # Draw
        self.fill((0,0,0))

        for i in range(0, len(area)):
            line = area[i]
            for j in range(0, len(line)):
                rx = j * SIZE + MOD
                ry = i * SIZE + MOD
                if line[j] == 1:
                    color = (0,255,0)
                else:
                    color = (255,255,255)
                self.rect(rx, ry, SIZE, SIZE, color)

        self.rect(position[0] * SIZE + MOD, position[1] * SIZE + MOD, SIZE, SIZE, (255, 0, 0))

Test().run()
