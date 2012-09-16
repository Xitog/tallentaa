# http://www.pygame.org/docs/tut/intro/intro.html
import sys, pygame

#-----------------------------------------------------------------------
#
# Library
#
#-----------------------------------------------------------------------    
class Application:
    
    #-------------------------------------------------------------------
    # Core
    #-------------------------------------------------------------------
    
    def config(self, x, y):
        self.io = {}
        self.x = x
        self.y = y
        self.filled = 0
        self.esc = False
        return self
    
    def run(self):
        pygame.init()
        size = (self.x, self.y)
        self.screen = pygame.display.set_mode(size)
        while 'quit' not in self.io and not self.esc:
            self.read_io()
            self.update()
            self.screen.fill((0,0,0))
            self.draw()
            pygame.display.flip()
    
    def stop(self):
        self.esc = True
    
    #-------------------------------------------------------------------
    # Placeholders
    #-------------------------------------------------------------------
    
    def update(self):
        pass
    
    def draw(self):
        pass
        
    #-------------------------------------------------------------------
    # I/O
    #-------------------------------------------------------------------
    
    def read_io(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.io['quit'] = pygame.time.get_ticks()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e: self.io['e'] = pygame.time.get_ticks()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_e: del self.io['e']
    
    def key_pressed(self, key):
        if key in self.io: return True
    
    #-------------------------------------------------------------------
    # Graphics
    #-------------------------------------------------------------------
    
    def rectangle(self, x1, y1, x2, y2, color, thickness):
        x = min(x1, x2)
        y = min(y1, y2)
        sx = abs(x1-x2)
        sy = abs(y1-y2)
        pygame.draw.rect(self.screen, color, (x, y, sx, sy), thickness)
    
    def rectangle_size(self, x1, y1, width, height, color, thickness):
        pygame.draw.rect(self.screen, color, (x1, y1, width, height), thickness)
    
    def circle(self, x1, y1, radius, color, thickness):
        pygame.draw.circle(self.screen, color, (x1, y1), radius, thickness)
    
    def fill(self, color):
        self.screen.fill(color)

#-----------------------------------------------------------------------
#
# Client Application
#
#----------------------------------------------------------------------- 
class MyApp(Application):
    
    def update(self):
        if self.key_pressed('e'): self.stop()
    
    def draw(self):
        self.fill((255,255,255))
        self.rectangle(10, 10, 100, 100, (255,0,0), 1)
        self.rectangle_size(100, 100, 10, 10, (0, 0, 255), self.filled)
        self.circle(200, 200, 20, (0, 255, 0), 1)

MyApp().config(800, 600).run()

sys.exit()

"""
            elif key_released('f') and mouse_x > 20:
            if double_click(mouse_right):
            elif button_pressed(mouse_right):
            elif button_released(mouse_right):
        
            line(x1, y1, x2, y2, color, thickness)
            point(x1, y1, color)
            write(x1, y1, text, color, font)
            
"""
