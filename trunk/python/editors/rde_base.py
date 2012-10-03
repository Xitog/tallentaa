# simple role diagram editor
# 14h23

import pygame

class Editor:
    
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.title = "Role Diagram Editor"
        self.size = (800, 600)
        self.esc = False
        
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)
        while not self.esc:
            self.update()
            self.draw()
            pygame.display.flip()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.esc = True
    
    def draw(self):
        self.screen.fill((255,255,255))

Editor()

