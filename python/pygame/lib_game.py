# http://www.pygame.org/docs/tut/intro/intro.html
import sys, pygame

# Gestion de:
#   - double click avec gestion sentitivity
#   - unification pygame.draw (= line, rectangle, circle) et surface.set_at (= point)
#   - rectancle(x1, y1, x2, y2) et non plus (x, y, width, height)
#   - gestion fps

#-----------------------------------------------------------------------
#
# Library
#
#-----------------------------------------------------------------------
class Application:
    
    #-------------------------------------------------------------------
    # Core
    #-------------------------------------------------------------------
    
    def config(self, x=800, y=600, title="lib_game"):
        self.io = {}
        self.released = {}
        self.x = x
        self.y = y
        self.title = title
        self.clock = pygame.time.Clock()
        self.fixed_fps = 60
        # constants
        self.filled = 0
        # state variables
        self.esc = False
        self.configured = True
        # double click
        self.last_button = None
        self.last_time = None
        self.dbl = False
        self.sensitivity = 200
        return self
    
    def run(self):
        # autoconfig
        try:
            self.configured
        except AttributeError:
            self.configured = False
        if not self.configured:
            self.config()
        # start
        pygame.init()
        size = (self.x, self.y)
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption(self.title)
        while 'quit' not in self.io and not self.esc:
            self.clock.tick(self.fixed_fps)
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
        self.released.clear()
        self.dbl = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.io['quit'] = pygame.time.get_ticks()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e: self.io['e'] = pygame.time.get_ticks()
                elif event.key == pygame.K_f: self.io['f'] = pygame.time.get_ticks()
            elif event.type == pygame.KEYUP:
                k = None
                if event.key == pygame.K_e: k = 'e'
                elif event.key == pygame.K_f: k = 'f'
                if k is not None:
                    del self.io[k]
                    self.released[k] = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: self.io['mouse_left'] = pygame.time.get_ticks()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: 
                    del self.io['mouse_left']
                    self.released['mouse_left'] = True
                    # dbl
                    #if self.last_time is not None: print pygame.time.get_ticks() - self.last_time
                    if self.last_button == 'mouse_left' and pygame.time.get_ticks() - self.last_time < self.sensitivity:
                        self.dbl = True
                    self.last_button = 'mouse_left'
                    self.last_time = pygame.time.get_ticks()
    
    def is_pressed(self, key):
        if key in self.io: return True
    
    def is_released(self, key):
        if key in self.released: return True
    
    def double_click(self, button):
        if self.last_button == button and self.dbl == True:
            return True
    
    #-------------------------------------------------------------------
    # Graphics
    #-------------------------------------------------------------------
    
    def rectangle(self, x1, y1, x2, y2, color=(0, 0, 0), thickness=1):
        x = min(x1, x2)
        y = min(y1, y2)
        sx = abs(x1-x2)
        sy = abs(y1-y2)
        pygame.draw.rect(self.screen, color, (x, y, sx, sy), thickness)
    
    def rectangle_size(self, x1, y1, width, height, color=(0, 0, 0), thickness=1):
        pygame.draw.rect(self.screen, color, (x1, y1, width, height), thickness)
    
    def circle(self, x1, y1, radius, color=(0, 0, 0), thickness=1):
        pygame.draw.circle(self.screen, color, (x1, y1), radius, thickness)
    
    def fill(self, color=(255, 255, 255)):
        self.screen.fill(color)
    
    def write(self, x1, y1, text, color=(0, 0, 0), size=12, background=(255, 255, 255), font='normal'):
        bold = False
        italic = False
        if font == 'bold': bold = True
        elif font == 'italic': italic = True
        f = pygame.font.SysFont('Arial', size, bold, italic)
        s = f.render(text, True, color, background)
        self.screen.blit(s, (x1, y1))
        if font == 'underlined':
            self.line(x1, y1+s.get_height(), x1+s.get_width(), y1+s.get_height(), color)
    
    def line(self, x1, y1, x2, y2, color, thickness=1):
        pygame.draw.line(self.screen, color, (x1, y1), (x2, y2), thickness)
    
    def point(self, x1, y1, color=(0, 0, 0)):
        self.screen.set_at((x1, y1), color)
    
    #-------------------------------------------------------------------
    # Others
    #-------------------------------------------------------------------
    
    def fps(self):
        return self.clock.get_fps()
    
#-----------------------------------------------------------------------
#
# Client Application
#
#----------------------------------------------------------------------- 
class MyApp(Application):
    
    def __init__(self):
        self.circle_size = 1
        self.red_circle = False
        self.blue_circle = False
        self.time = 0
    
    def update(self):
        if self.is_pressed('e'): self.stop()
        if self.is_pressed('f') or self.is_pressed('mouse_left'): self.circle_size += 1
        else: self.circle_size = 1
        if self.is_released('f'): self.red_circle = True
        if self.is_released('mouse_left'): self.blue_circle = True
        if self.double_click('mouse_left'):
            self.time = 10
    
    def draw(self):
        self.fill((255,255,255))
        self.rectangle(10, 10, 100, 100, (255,0,0), 1)
        self.rectangle_size(100, 100, 10, 10, (0, 0, 255), self.filled)
        self.circle(200, 200, 20, (0, 255, 0), 1)
        self.write(300, 300, "Hello", (255, 255, 255), 18, (255, 0, 0), 'bold')
        self.write(400, 300, "World!")
        self.write(450, 300, "Hello", font='underlined')
        self.line(400, 320, 430, 320, (0, 0, 0), 1)
        self.rectangle(500, 500, 550, 550)
        self.circle(500, 100, self.circle_size, (0, 255, 0), self.filled)
        self.write(600, 20, str(self.fps()))
        if self.red_circle:
            self.circle(30, 500, 20, (255, 0, 0), self.filled)
        if self.blue_circle:
            self.circle(70, 500, 20, (0, 0, 255), self.filled)
        for i in xrange(0, 100):
            self.point(i, 70)
        if self.time > 0:
            self.fill((0, 255, 0))
            self.time -= 1

#MyApp().config(800, 600).run()
MyApp().run()

sys.exit()

