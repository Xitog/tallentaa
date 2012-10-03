# simple role diagram editor
# 14h23

import pygame

class Button:
    
    def __init__(self, name, x, y, size_x, size_y, border_size):
        self.name = name
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.border_size = border_size
        self.selected = False
    
    def draw(self, surf):
        mx, my = pygame.mouse.get_pos()
        if self.selected:
            pygame.draw.rect(surf, (0,0,255), (self.x, self.y, self.size_x, self.size_y), self.border_size)
        elif self.collision(mx, my):
            pygame.draw.rect(surf, (0,255,0), (self.x, self.y, self.size_x, self.size_y), self.border_size)
        else:
            pygame.draw.rect(surf, (0,0,0), (self.x, self.y, self.size_x, self.size_y), self.border_size)
    
    def collision(self, x, y):
        if x >= self.x and x <= self.x+self.size_x and y >= self.y and y <= self.y+self.size_y:
            return True
        else:
            return False
    
    def select(self):
        self.selected = True
    
    def unselect(self):
        self.selected = False

class Role:
    
    def __init__(self, name, x, y, size_x, size_y):
        self.name = name
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.selected = False
        self.border_size = 2
    
    def collision(self, x, y):
        if x >= self.x and x <= self.x+self.size_x and y >= self.y and y <= self.y+self.size_y:
            return True
        else:
            return False
    
    def draw(self, surf):
        mx, my = pygame.mouse.get_pos()
        if self.selected:
            pygame.draw.rect(surf, (0,0,255), (self.x, self.y, self.size_x, self.size_y), self.border_size)
        elif self.collision(mx, my):
            pygame.draw.rect(surf, (0,255,0), (self.x, self.y, self.size_x, self.size_y), self.border_size)
        else:
            pygame.draw.rect(surf, (0,0,0), (self.x, self.y, self.size_x, self.size_y), self.border_size)
    
    def select(self):
        self.selected = True
    
    def unselect(self):
        self.selected = False

class Link:
    
    def __init__(self, name, x1, y1, x2, y2):
        self.name = name
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    def draw(self, surf):
        pygame.draw.line(surf, (0,0,0), (self.x1, self.y1), (self.x2, self.y2), 2)

class Editor:
    
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.title = "Role Diagram Editor"
        self.size = (800, 600)
        self.esc = False
        
        self.build()
        
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)
        while not self.esc:
            self.update()
            self.draw()
            pygame.display.flip()
    
    def build(self):
        self.buttons = []
        self.buttons.append(Button("Selection", 3, 100, 64, 64, 2))
        self.buttons.append(Button("Role", 3, 170, 64, 64, 2))
        self.buttons.append(Button("Lien", 3, 240, 64, 64, 2))
        self.buttons.append(Button("Commentaire", 3, 310, 64, 64, 2))
        self.buttons.append(Button("Lien Commentaire", 3, 380, 64, 64, 2))
        
        self.mode = None
        self.element_selected = None
        self.ecart_mx = -1
        self.ecart_my = -1
        
        self.m_down = False
        
        self.lien_start = None
        
        self.roles = []
        self.links = []
    
    def select(self):
        mx, my = pygame.mouse.get_pos()
        self.element_selected = None
        for r in self.roles:
            if r.collision(mx, my) and self.element_selected is None:
                r.select()
                self.element_selected = r
                self.ecart_mx = mx - r.x
                self.ecart_my = my - r.y
            else:
                r.unselect()
    
    def select_button(self):
        mx, my = pygame.mouse.get_pos()
        self.mode = None
        for b in self.buttons:
            if b.collision(mx, my):
                b.select()
                self.mode = b.name
            else:
                b.unselect()

    def update(self):
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.esc = True
            if self.mode == 'Role':
                if event.type == pygame.MOUSEBUTTONUP:
                    self.m_down = False
                    if mx > 70:
                        self.select()
                        if self.element_selected is None:
                            self.roles.append(Role('ano', mx, my, 128, 64))
                        else:
                            pass
                    elif mx <= 70:
                        self.select_button()
            elif self.mode == 'Lien':
                if event.type == pygame.MOUSEBUTTONUP:
                    self.m_down = False
                    if mx <= 70:
                        self.select_button()
                    elif mx > 70:
                        self.links.append(Link('ano', self.lien_start[0], self.lien_start[1], mx, my))
                    self.lien_start = None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.m_down = True
                    if mx > 70:
                        self.lien_start = (mx, my)
            elif self.mode == 'Selection' or self.mode is None:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mx > 70:
                        self.select()
                        self.m_down = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.m_down = False
                    if mx <= 70:
                        self.select_button()
                if self.m_down and self.element_selected is not None and mx > 70:
                    self.element_selected.x = mx - self.ecart_mx
                    self.element_selected.y = my - self.ecart_my
                    if self.element_selected.x <= 70: self.element_selected.x = 70
    
    def update2(self):
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.esc = True
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                # ai-je clique sur quelque chose ?
                self.element_selected = None
                for r in self.roles:
                    if r.collision(mx, my) and self.element_selected is None:
                        r.select()
                        self.element_selected = r
                        self.ecart_mx = mx - r.x
                        self.ecart_my = my - r.y
                    else:
                        r.unselect()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.m_down = True
                    if mx > 70 and self.mode == 'Lien':
                        self.lien_start = (mx, my)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.m_down = False
                    if event.button == 1:
                        if mx <= 70:
                            self.mode = None
                            for b in self.buttons:
                                if b.collision(mx, my):
                                    b.select()
                                    self.mode = b.name
                                else:
                                    b.unselect()
                        elif mx > 70:
                            # action des modes
                            if self.mode == 'Role':
                                if self.element_selected is None:
                                    self.roles.append(Role('ano', mx, my, 128, 64))
                            elif self.mode == 'Lien':
                                self.links.append(Link('ano', self.lien_start[0], self.lien_start[1], mx, my))
                            elif self.mode == 'Commentaire':
                                print 'C'
                            elif self.mode == 'Lien Commentaire':
                                print 'D'
        if self.m_down:
            if mx > 70:
                if self.element_selected is not None:
                    self.element_selected.x = mx - self.ecart_mx
                    self.element_selected.y = my - self.ecart_my
                elif self.lien_start is not None:
                    pass       
    
    def draw(self):
        self.screen.fill((255,255,255))
        # menu left
        pygame.draw.rect(self.screen, (200,200,200), (0, 0, 70, 600), 0)
        # icons
        for b in self.buttons:
            b.draw(self.screen)
        for r in self.roles:
            r.draw(self.screen)
        if pygame.mouse.get_pos()[0] > 70 and self.m_down and self.lien_start is not None and self.mode == 'Lien':
             pygame.draw.line(self.screen, (0,0,0), self.lien_start, pygame.mouse.get_pos(), 2)
        for l in self.links:
            l.draw(self.screen)

Editor()

