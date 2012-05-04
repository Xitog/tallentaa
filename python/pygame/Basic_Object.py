# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

class Color:
  Red = (255, 0, 0)
  Green = (0, 255, 0)
  Blue = (0, 0, 255)

class Window:
  
  def __init__(self, x=800, y=600, title='Basic PyGame'):
    pygame.init()
    pygame.display.set_caption(title)
    resolution = (x, y)
    flags = pygame.DOUBLEBUF
    best_color_depth = pygame.display.mode_ok(resolution)
    self.screen = pygame.display.set_mode(resolution, flags, best_color_depth)
    self.clock = pygame.time.Clock()
    self.width = x
    self.height = y
    self.font = pygame.font.SysFont(pygame.font.get_default_font(), 16)
    self.escape = False

  def write(self, text, x, y):
    global font
    s = font.render(text, True, (255,0,0))
    sx, sy = s.get_size()
    self.screen.blit(s, (int(x-sx/2), int(y-sy/2)))
  
  def update(self):
    for event in pygame.event.get():
      if event.type == QUIT:
        self.escape = True
      elif event.type == KEYDOWN and event.key == K_ESCAPE:
        self.escape = True
  
  def draw(self):
    self.screen.fill(Color.Blue)
  
  def run(self):
    while not self.escape:
      self.update()
      self.draw()
      pygame.display.flip()
      self.clock.tick(60) # FPS limit

w = Window(800,600)
w.run()
