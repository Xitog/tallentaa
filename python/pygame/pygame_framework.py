import pygame

# 2 layer architecture. An application with X software windows. The application dispatchs events to the right window depending on the pos of the event.

# A Software Window
# update : update
# draw : draw
# on_event : react to an event dispatched by the Application
class Window:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (120, 0, 0)
    
    def inside(self, x, y):
        return x >= self.x and x <= self.x + self.width and y >= self.y and y <= self.y + self.height

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.color = (0, 0, 120)
    
    def update(self):
        self.color = ((self.color[0]+1)%255, self.color[1], self.color[2])
    
    def draw(self, surf):
        pygame.draw.rect(surf, self.color, (self.x, self.y, self.width, self.height), 0)

# The Application
# run : forever loop
# update : update (get io for the application)
# draw : draw
class Application:
    def __init__(self, title, width, height):
        pygame.init()
        self.size = width, height
        self.screen = pygame.display.set_mode(self.size)
        self.main = Window(30, 30, 100, 100)
        pygame.display.set_caption(title)
    
    def run(self):
        while 1:
            self.update()
            self.draw()
    
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if self.main.inside(event.pos[0], event.pos[1]):
                    self.main.on_event(event)
        self.main.update()
     
    def draw(self):
        self.screen.fill((0, 120, 0))
        self.main.draw(self.screen)        
        pygame.display.flip()
        pygame.time.Clock().tick(60)

Application("Test", 800, 600).run()

