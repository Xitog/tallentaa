import pygame
from pygame.locals import *

MOUSE_LEFT = 1
MOUSE_MIDDLE = 2
MOUSE_RIGHT = 3

MIN = {
        K_a : 'a',
        K_b : 'b',
        K_c : 'c',
        K_d : 'd',
        K_e : 'e',
        K_f : 'f',
        K_g : 'g',
        K_h : 'h',
        K_i : 'i',
        K_j : 'j',
        K_k : 'k',
        K_l : 'l',
        K_m : 'm',
        K_n : 'n',
        K_o : 'o',
        K_p : 'p',
        K_q : 'q',
        K_r : 'r',
        K_s : 's',
        K_t : 't',
        K_u : 'u',
        K_v : 'v',
        K_w : 'w',
        K_x : 'x',
        K_y : 'y',
        K_z : 'z',
}

MAJ = {
        K_a : 'A',
        K_b : 'B',
        K_c : 'C',
        K_d : 'D',
        K_e : 'E',
        K_f : 'F',
        K_g : 'G',
        K_h : 'H',
        K_i : 'I',
        K_j : 'J',
        K_k : 'K',
        K_l : 'L',
        K_m : 'M',
        K_n : 'N',
        K_o : 'O',
        K_p : 'P',
        K_q : 'Q',
        K_r : 'R',
        K_s : 'S',
        K_t : 'T',
        K_u : 'U',
        K_v : 'V',
        K_w : 'W',
        K_x : 'X',
        K_y : 'Y',
        K_z : 'Z',
}

# 2 layer architecture. An application with X software windows. The application dispatchs events to the right window depending on the pos of the event.
    
class Element:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def draw(self, surf):
        pass
    def on(self, x, y):
        return self.x == x and self.y == y
    def write(self, surf, txt, x, y, color=(0,0,0)):
        font = pygame.font.SysFont(pygame.font.get_default_font(), 16, False, False)
        s = font.render(txt, True, color)
        surf.blit(s, (x,y))

class Class(Element):
    def __init__(self, x, y):
        Element.__init__(self, x, y)
        self.width = 40
        self.height = 60
        self.name = ""
    
    def draw(self, surf):
        pygame.draw.rect(surf, (0, 0, 0), (self.x, self.y, self.width, self.height), 1)
        self.write(surf, self.name, self.x, self.y)
    
    def on(self, x, y):
        return x >= self.x and x <= self.x + self.width and y >= self.y and y <= self.y + self.height

# A Software Window
# update : update
# draw : draw
# on_event : react to an event dispatched by the Application
class Window:
    def __init__(self, parent, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (120, 0, 0)
        self.parent = parent
        # drag & drop
        self.selected = None
        self.difx = 0
        self.dify = 0
        # line
        self.line = False
        self.sx = 0
        self.sy = 0
        # writing
        self.txt = None
        self.txt_x = 0
        self.txt_y = 0
        self.txt_selected = None
    
    def inside(self, x, y):
        return x >= self.x and x <= self.x + self.width and y >= self.y and y <= self.y + self.height
    
    # clear for a rectangle !
    def clear(self, x, y, avoid=None):
        something = None
        for e in self.parent.elements:
            if e.on(x,y) or e.on(x+40, y) or e.on(x, y+60) or e.on(x+40, y+60):
                if e == avoid: continue
                something = e
                break
        return something
    
    def something(self, x, y):
        for e in self.parent.elements:
            if e.on(x,y):
                return e
        return None
    
    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.selected is not None: # drag & drop
                if self.line: # not drag & drop but line
                    self.line = False
                    x, y = event.pos
                    e = self.something(x, y)
                    if e is not None and e != self.selected: # link
                        print "linking", e, "to", self.selected
                self.selected = None
                return
            if event.button == MOUSE_LEFT:
                x, y = event.pos
                if self.clear(x,y) is None:
                    self.parent.elements.append(Class(event.pos[0], event.pos[1]))
            elif event.button == MOUSE_MIDDLE: # writing
                x, y = event.pos
                e = self.something(x, y)
                if e is not None:
                    self.txt_x, self.txt_y = event.pos
                    self.txt = ""
                    self.txt_selected = e
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == MOUSE_LEFT:
                x, y = event.pos
                e = self.something(x, y)
                if e is not None:
                    # secret of drag & drop
                    self.selected = e
                    self.difx = e.x - x
                    self.dify = e.y - y
            elif event.button == MOUSE_RIGHT:
                x, y = event.pos
                e = self.something(x, y)
                if e is not None:
                    self.line = True
                    self.selected = e
                    self.sx = x
                    self.sy = y
        elif event.type == pygame.KEYUP:
            if self.txt is not None:
                if event.key in MIN:
                    if event.mod & (KMOD_SHIFT | KMOD_CAPS):
                        self.txt += MAJ[event.key]
                    else:
                        self.txt += MIN[event.key]
                elif event.key == K_BACKSPACE:
                    self.txt = self.txt[0:len(self.txt)-1]
                elif event.key == K_RETURN:
                    self.txt_selected.name = self.txt
                    self.txt = None

    def update(self):
        if self.selected is not None:
            if not self.line: # drag & drop
                x, y = pygame.mouse.get_pos()
                nx = x + self.difx
                ny = y + self.dify
                if self.clear(nx, ny, self.selected) is None:
                    self.selected.x = nx
                    self.selected.y = ny
                elif self.clear(nx, self.selected.y, self.selected) is None:
                    self.selected.x = nx
                elif self.clear(self.selected.x, ny, self.selected) is None:
                    self.selected.y = ny
    
    def draw(self, surf):
        self.parent.write("Bonjour", 20, 30)
        for e in self.parent.elements:
            e.draw(surf)
        if self.selected is not None:
            if self.line: # line
                mx, my = pygame.mouse.get_pos()
                pygame.draw.line(surf, (0, 0, 0), (self.sx, self.sy), (mx, my), 1)
        if self.txt is not None:
            self.parent.write(self.txt, self.txt_x, self.txt_y)

# The Application
# run : forever loop
# update : update (get io for the application)
# draw : draw
class Application:
    def __init__(self, title, width, height):
        pygame.init()
        self.size = width, height
        self.screen = pygame.display.set_mode(self.size)
        self.main = Window(self, 0, 0, 800, 600)
        pygame.display.set_caption(title)
        self.elements = []
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 16, False, False)
    
    def write(self, txt, x, y, color=(0,0,0)):
        s = self.font.render(txt, True, color)
        self.screen.blit(s, (x,y))
    
    def run(self):
        while 1:
            self.update()
            self.draw()
    
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: exit()
            if event.type in [pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN]:
                if self.main.inside(event.pos[0], event.pos[1]):
                    self.main.on_event(event)
            elif event.type == pygame.KEYUP:
                self.main.on_event(event)
        
        self.main.update()
     
    def draw(self):
        self.screen.fill((255, 255, 255))
        self.main.draw(self.screen)        
        pygame.display.flip()
        pygame.time.Clock().tick(60)

#fonts = pygame.font.get_fonts()
#for f in fonts:
#    print f

Application("Test", 800, 600).run()

