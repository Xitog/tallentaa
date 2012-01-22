
def hello(name):
    print 'hello', name, '!'

def start(name, x, y):
    import pygame
    import pygame.locals
    const = pygame.locals
    pygame.init()
    pygame.display.set_caption(name)
    screen = pygame.display.set_mode((x,y), pygame.DOUBLEBUF, 32)
    loop = True
    while loop:
        for event in pygame.event.get():
            if event.type == const.QUIT:
                loop = False
        pygame.display.flip()

print dir()
#core['first'] = {}
#core['first']['hello'] = hello
register('hello', hello)
register('start', start)
