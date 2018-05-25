# Import
import pygame
from pygame import Surface
from pygame.locals import *
import time
import random

MOVE = 150

class Snake:

    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        
        pygame.init()
        pygame.display.set_caption('Snake')
        resolution : (int, int) = (self.screen_width, self.screen_height)
        flags : int = pygame.DOUBLEBUF
        colors : int = 32
        self.screen : Surface = pygame.display.set_mode( resolution, flags, colors)
        self.screen_buffer : Surface = Surface((self.screen_width, self.screen_height))
        
        self.x = 100
        self.y = 100
        self.part = [[100, 100]]

        self.apple_x = 200
        self.apple_y = 200
        self.apple_width = 20
        self.apple_height = 20

        self.zone = 1
        
        # keys
        self.escape : bool = False
        self.show_minimap : bool = False
        self.right : bool   = True
        self.left : bool    = False
        self.up : bool      = False
        self.down : bool    = False
        self.running : bool = False

        self.zone_time = time.time()
    
    def input(self):
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
                    self.left = False
                    self.down = False
                    self.up = False
                if event.key == K_LEFT:
                    self.left = True
                    self.right = False
                    self.down = False
                    self.up = False
                if event.key == K_UP:
                    self.up = True
                    self.down = False
                    self.right = False
                    self.left = False
                if event.key == K_DOWN:
                    self.down = True
                    self.up = False
                    self.right = False
                    self.left = False
                if event.key == K_LSHIFT:
                    pass
            elif event.type == KEYUP:
                # hud
                if event.key == K_TAB:
                    self.show_minimap = False
                # debug
                if event.key == K_RETURN:
                    pass
                if event.key == K_t:
                    pass
                # movement
                #if event.key == K_RIGHT:
                #    self.right = False
                #if event.key == K_LEFT:
                #    self.left = False
                #if event.key == K_UP:
                #    self.up = False
                #if event.key == K_DOWN:
                #    self.down = False
                if event.key == K_LSHIFT:
                    pass
                # debug
                if event.key == K_SPACE:
                    pass
    
    def update(self, frametime : float):
        next_x = self.part[0][0]
        next_y = self.part[0][1]
        if self.right:
            next_x += MOVE * frametime
        if self.left:
            next_x -= MOVE * frametime
        if self.down:
            next_y += MOVE * frametime
        if self.up:
            next_y -= MOVE * frametime
        self.part[0][0] = next_x
        self.part[0][1] = next_y
        if self.apple_x <= self.part[0][0] < self.apple_x + self.apple_width:
            if self.apple_y <= self.part[0][1] < self.apple_y + self.apple_height:
                self.apple_x = random.randint(self.zone + 3 * self.apple_width, (self.screen_width - self.zone) - 3 * self.apple_width)
                self.apple_y = random.randint(self.zone + 3 * self.apple_height, (self.screen_height - self.zone) - 3 * self.apple_height)
        if time.time() - self.zone_time > 5:
            self.zone += 1
            self.zone_time = time.time()
    
    def draw(self):
        self.screen_buffer.fill((0,0,0))
        for p in self.part:
            pygame.draw.rect(self.screen_buffer, (255, 255, 255), (p[0], p[1], 10, 10), 0)
        # Apple
        pygame.draw.rect(self.screen_buffer, (0,255,0), (self.apple_x, self.apple_y, self.apple_width, self.apple_height), 0)
        # Battle royale
        pygame.draw.rect(self.screen_buffer, (255,0,0), (0, 0, self.screen_width, self.zone), 0)
        pygame.draw.rect(self.screen_buffer, (255,0,0), (0, 0, self.zone, self.screen_height), 0)
        pygame.draw.rect(self.screen_buffer, (255,0,0), (0, self.screen_height - self.zone, self.screen_width, self.zone), 0)
        pygame.draw.rect(self.screen_buffer, (255,0,0), (self.screen_width - self.zone, 0, self.zone, self.screen_height), 0)
        # Display backbuffer
        self.screen.blit(self.screen_buffer, (0,0))
        pygame.display.flip()
    
    def start(self):
        """Main loop"""
        while not self.escape:
            start = time.time()
            self.draw()
            self.input()
            end = time.time()
            self.update(end - start)

if __name__ == '__main__':
    Snake().start()
    pygame.quit()
