import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_ESCAPE, K_DOWN, K_UP, K_RIGHT, K_LEFT

pygame.init()
pygame.display.set_caption('2.5D Engine')
SCREEN_WIDTH, SCREEN_HEIGHT = 320, 200
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
clock = pygame.time.Clock()

font = pygame.font.Font(None, 24)
text_surface = font.render('Hello', False, (255, 255, 255))
text_rect = text_surface.get_rect()
print('Text rect:', text_rect, 'center =', text_rect.center)
print('Screen rect:', screen.get_rect(), 'center =', screen.get_rect().center)
text_rect.center = screen.get_rect().center
print(text_rect)

level = {
    'sectors': {
        1: {
            'walls': [
                [10, 10, 100, 10, 0],
                [10, 10, 10, 100, 0],
                [10, 100, 100, 100, 0],
                [100, 100, 100, 50, 0],
                [100, 50, 100, 10, 2]
            ]
        },
        2: {
            'walls': [
                [100, 50, 100, 10, 2],
                [100, 50, 130, 50, 0],
                [100, 10, 130, 10, 0],
                [130, 50, 130, 10, 0]
            ]
        },
    }
}

app_end    = False
sector     = 1
player_x   = 10
player_y   = 10
move_left  = False
move_right = False
move_up    = False
move_down  = False

while not app_end:
    # Drawing picture
    screen.fill((0, 0, 0))
    for i in range(SCREEN_WIDTH):
        pygame.draw.line(screen, (0, 255, 0), (i, 50), (i, 150))
    for sk, sv in level['sectors'].items():
        for w in sv['walls']:
            color = (255, 255, 255) if w[4] == 0 else (255, 0, 0)
            pygame.draw.line(screen, color, (w[0], w[1]), (w[2], w[3]))
            pygame.draw.rect(screen, (0, 255, 0), (w[0] - 2, w[1] - 2, 5, 5),
                             1)
            pygame.draw.rect(screen, (0, 255, 0), (w[2] - 2, w[3] - 2, 5, 5),
                             1)
    screen.blit(text_surface, text_rect)
    pygame.draw.line(screen, (255, 0, 0), (140, 0), (140, 200))
    pygame.draw.rect(screen, (0, 0, 255), (player_x - 2, player_y - 2, 5, 5))
    pygame.display.flip()
    # Setting framerate
    # dt = clock.tick(30)
    dt = clock.tick_busy_loop(30)  # more accurate
    print(f'Elapsed: {dt} milliseconds')
    # Handling events
    for event in pygame.event.get():
        if event.type == QUIT:
            app_end = True
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                app_end = True
            elif event.key == K_DOWN:
                move_down = True
            elif event.key == K_UP:
                move_up = True
            elif event.key == K_LEFT:
                move_left = True
            elif event.key == K_RIGHT:
                move_right = True
            else:
                print(f"{event.key:4d}", event.unicode)
        elif event.type == KEYUP:
            if event.key == K_ESCAPE:
                app_end = False
            elif event.key == K_DOWN:
                move_down = False
            elif event.key == K_UP:
                move_up = False
            elif event.key == K_LEFT:
                move_left = False
            elif event.key == K_RIGHT:
                move_right = False
    # Updating
    if move_down:  player_y += 1
    if move_up:    player_y -= 1
    if move_left:  player_x -= 1
    if move_right: player_x += 1

pygame.quit()
