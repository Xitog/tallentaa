import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_ESCAPE, K_DOWN, K_UP, K_RIGHT, K_LEFT, K_TAB

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
                [100, 50, 100, 10, 1],
                [100, 50, 130, 50, 0],
                [100, 10, 130, 10, 0],
                [130, 50, 130, 10, 3]
            ]
        },
        3 : {
            'walls' : [
                [130, 50, 130, 10, 2],
                [130, 10, 160, 10, 0],
                [160, 10, 160, 60, 0],
                [130, 50, 130, 60, 0],
                [130, 60, 160, 60, 4]
            ]
        },
        4 : {
            'walls' : [
                [130, 60, 160, 60, 3],
                [130, 60, 130, 90, 0],
                [130, 90, 160, 90, 0],
                [160, 90, 160, 60, 0]
            ]
        }
    }
}

def get_rect(sector):
    min_x = 2000
    min_y = 2000
    max_x = 0
    max_y = 0
    for w in sector['walls']:
        if w[0] < min_x: min_x = w[0]
        if w[1] < min_y: min_y = w[1]
        if w[2] < min_x: min_x = w[2]
        if w[3] < min_y: min_y = w[3]
        if w[0] > max_x: max_x = w[0]
        if w[1] > max_y: max_y = w[1]
        if w[2] > max_x: max_x = w[2]
        if w[3] > max_y: max_y = w[3]
    return min_x, min_y, max_x - min_x, max_y - min_y


def intersect(seg1, seg2):
    ab_seg1 = ab(seg1)
    seg1_min_x = min(seg1[0], seg1[2])
    seg1_max_x = max(seg1[0], seg1[2])
    seg1_min_y = min(seg1[1], seg1[3])
    seg1_max_y = max(seg1[1], seg1[3])
    seg2_min_x = min(seg2[0], seg2[2])
    seg2_max_x = max(seg2[0], seg2[2])
    seg2_min_y = min(seg2[1], seg2[3])
    seg2_max_y = max(seg2[1], seg2[3])
    if ab_seg1[0] is None: # horizontal
        if seg2[0] == seg2[2]: # vertical
            if seg1_min_x <= seg2[0] <= seg1_max_x:
                if seg2_min_y <= seg1_min_y <= seg2_max_y: # 221211
                    #print('vertical', seg2[0], 'minxs1', seg1_min_x, 'maxxs1', seg1_max_x, 'minys1', seg1_min_y, 'maxys1', seg1_max_y, seg2_min_y, seg2_max_y)
                    print('crossed')
                    return True
                elif seg2_min_y <= seg1_max_y <= seg2_max_y:  # 112122
                    print('crossed')
                    return True
                elif seg1_min_y <= seg2_min_y and seg1_max_y >= seg2_max_y:  # 11222211
                    print('crossed')
                    return True
        elif seg2[1] == seg2[3]: # horizontal
            if seg2[1] == seg1[1]: # same line fixée par Y, décrite par X
                if seg2_min_x <= seg1_min_x <= seg2_max_x: # 221211
                    print('crossed')
                    return True
                elif seg2_min_x <= seg1_max_x <= seg2_max_x:  # 112122
                    print('crossed')
                    return True
                elif seg1_min_x <= seg2_min_x and seg1_max_x >= seg2_max_x:  # 11222211
                    print('crossed')
                    return True
        else:
            raise Exception("Wall not angular are not handled")
    elif ab_seg1[1] is None: # vertical
        if seg2[0] == seg2[2]: # vertical
            if seg2[0] == seg1[0]: # same colonne fixée par X, décrite par Y
                if seg2_min_y <= seg1_min_y <= seg2_max_y: # 221211
                    print('crossed')
                    return True
                elif seg2_min_y <= seg1_max_y <= seg2_max_y:  # 112122
                    print('crossed')
                    return True
                elif seg1_min_y <= seg2_min_y and seg1_max_y >= seg2_max_y:  # 11222211
                    print('crossed')
                    return True
        elif seg2[1] == seg2[3]: # horizontal
            if seg1_min_y <= seg2[1] <= seg1_max_y:
                if seg2_min_x <= seg1_min_x <= seg2_max_x: # 221211
                    print('crossed')
                    return True
                elif seg2_min_x <= seg1_max_x <= seg2_max_x:  # 112122
                    print('crossed')
                    return True
                elif seg1_min_x <= seg2_min_x and seg1_max_x >= seg2_max_x:  # 11222211
                    print('crossed')
                    return True
        else:
            raise Exception("Wall not angular are not handled")
    else:
        if seg2[0] == seg2[2]: # vertical
            return True
        elif seg2[1] == seg2[3]: # horizontal
            return True
        else:
            raise Exception("Wall not angular are not handled")
    return False


def ab(quad):
    if quad[0] == quad[2]: # vertical x1=x2
        return quad[0], None
    elif quad[1] == quad[3]: # horizontal y1=y2
        return None, quad[1]
    else:
        a = (quad[1] - quad[3]) / (quad[0] - quad[2])
        b = quad[1] - a * quad[0]
    return a, b

app_end       = False
player_sector = 1
player_x      = 30
player_y      = 50
player_x_old  = player_x
player_y_old  = player_y
player_speed  = 0.2
move_left     = False
move_right    = False
move_up       = False
move_down     = False
mod           = 'MAP'

while not app_end:
    # Drawing picture
    screen.fill((0, 0, 0))
    if mod == 'GAME':
        for i in range(SCREEN_WIDTH):
            pygame.draw.line(screen, (0, 255, 0), (i, 50), (i, 150))
        pygame.draw.line(screen, (255, 0, 0), (140, 0), (140, 200))
    elif mod == 'MAP':
        for sector_key, sector in level['sectors'].items():
            if player_sector == sector_key:
                pygame.draw.rect(screen, (50, 50, 50), get_rect(sector))
            for w in sector['walls']:
                color = (255, 255, 255) if w[4] == 0 else (255, 0, 0)
                pygame.draw.line(screen, color, (w[0], w[1]), (w[2], w[3]))
                pygame.draw.rect(screen, (0, 255, 0),
                                 (w[0] - 2, w[1] - 2, 5, 5), 1)
                pygame.draw.rect(screen, (0, 255, 0),
                                 (w[2] - 2, w[3] - 2, 5, 5), 1)
        screen.blit(text_surface, text_rect)
        pygame.draw.line(screen, (255, 0, 0), (player_x_old, player_y_old),
                         (player_x, player_y))
        pygame.draw.rect(screen, (0, 0, 255), (player_x - 2, player_y - 2, 5, 5))
    pygame.display.flip()
    # Setting framerate
    # dt = clock.tick(30)
    dt = clock.tick_busy_loop(30)  # more accurate
    #print(f'Elapsed: {dt} milliseconds')
    # Handling events
    for event in pygame.event.get():
        if event.type == QUIT:
            app_end = True
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:   app_end    = True
            elif event.key == K_DOWN:   move_down  = True
            elif event.key == K_UP:     move_up    = True
            elif event.key == K_LEFT:   move_left  = True
            elif event.key == K_RIGHT:  move_right = True
            else:
                print(f"{event.key:4d}", event.unicode)
        elif event.type == KEYUP:
            if event.key == K_ESCAPE:   app_end    = False
            elif event.key == K_DOWN:   move_down  = False
            elif event.key == K_UP:     move_up    = False
            elif event.key == K_LEFT:   move_left  = False
            elif event.key == K_RIGHT:  move_right = False
            elif event.key == K_TAB:
                mod = 'GAME' if mod == 'MAP' else 'MAP'
    # Updating
    player_x_old = player_x
    player_y_old = player_y
    if move_down:  player_y += player_speed * dt
    if move_up:    player_y -= player_speed * dt
    if move_left:  player_x -= player_speed * dt
    if move_right: player_x += player_speed * dt
    # Check wall
    old_sectors = []
    while True:
        old_sectors.append(player_sector)
        for w in level['sectors'][player_sector]['walls']:
            if intersect([player_x_old, player_y_old, player_x, player_y], w):
                if w[4] == 0:
                    player_x = player_x_old
                    player_y = player_y_old
                    break
                elif w[4] not in old_sectors:
                    player_sector = w[4]
                    print('changing sector', w[4])
                    break
        if player_sector in old_sectors:
            break

pygame.quit()

# 14h57 : first change of sector
# 15h02 : ça marche ! il faut mémoriser
# 16h42 : croisements verticaux aussi mais y'a des bugs
