start         = None
walls         = None
sectors       = None
player        = None
monsters      = []
app_end       = False
mod           = 'MAP'
entities      = []

level = {
    'name' : 'The Deep',
    'walls' : {
         1 : [10, 10, 100, 10],
         2 : [10, 10, 10, 100],
         3 : [10, 100, 100, 100],
         4 : [100, 100, 100, 50],
         5 : [100, 50, 100, 10],
         6 : [100, 50, 130, 50],
         7 : [100, 10, 130, 10],
         8 : [130, 50, 130, 10],
         9 : [130, 10, 160, 10],
        10 : [160, 10, 160, 60],
        11 : [130, 50, 130, 60],
        12 : [130, 60, 160, 60],
        13 : [130, 60, 130, 90],
        14 : [130, 90, 160, 90],
        15 : [160, 90, 160, 60],
        16 : [160, 60, 180, 60],
        17 : [160, 90, 180, 90],
        18 : [180, 90, 180, 120],
        19 : [180, 60, 180, 30],
        20 : [180, 30, 260, 30],
        21 : [180, 120, 260, 120],
        22 : [260, 30, 260, 120],
        23 : [260, 120, 260, 170],
        24 : [260, 170, 100, 170],
        25 : [100, 170, 100, 100],
        26 : [100, 100, 100, 110],
        27 : [100, 110, 150, 110],
        28 : [150, 110, 150, 120],
        29 : [150, 120, 180, 120],
        30 : [210, 90, 230, 90],
        31 : [210, 60, 230, 60],
        32 : [210, 90, 210, 60],
        33 : [230, 90, 230, 60],
        34 : [130, 140, 240, 140],
        35 : [130, 150, 240, 150],
        36 : [130, 150, 130, 140],
        37 : [240, 150, 240, 140],
    },
    'sectors': {
        1: {
            'walls': [
                [1, 0],
                [2, 0],
                [3, 0],
                [4, 0],
                [5, 2]
            ]
        },
        2: {
            'walls': [
                [5, 1],
                [6, 0],
                [7, 0],
                [8, 3]
            ]
        },
        3 : {
            'walls' : [
                [8, 2],
                [9, 0],
                [10, 0],
                [11, 0],
                [12, 4]
            ]
        },
        4 : {
            'walls' : [
                [12, 3],
                [13, 0],
                [14, 0],
                [15, 5]
            ]
        },
        5 : {
            'walls' : [
                [15, 4], # [160, 90, 160, 60],
                [16, 0], # [160, 60, 180, 60],
                [17, 0], # [160, 90, 180, 90],
                [18, 0], # [180, 90, 180, 120],
                [19, 0], # [180, 60, 180, 30],
                [20, 0], # [180, 30, 260, 30],
                [21, 6], # [180, 120, 260, 120],
                [22, 0]  # [260, 30, 260, 120],
            ],
            'inside' : [7]
        },
        6 : {
            'walls' : [
                [21, 5],
                [23, 0],
                [24, 0],
                [25, 0],
                [26, 0],
                [27, 0],
                [28, 0],
                [29, 0]
            ],
            'inside' : [8]
        },
        7 : {
            'walls' : [
                [30, 0],
                [31, 0],
                [32, 0],
                [33, 0]
            ],
        },
        8 : {
            'walls' : [
                [34, 6],
                [35, 6],
                [36, 6],
                [37, 6]
            ]
        }
    },
    'objects' : [
        [50, 50, 'life']
    ]
}


#-----------------------------------------------------------
# Resources
#-----------------------------------------------------------

try:
    greendot = pygame.image.load('green_dot.png').convert_alpha()
except pygame.error:
    greendot = pygame.Surface((10, 10))
    greendot.fill(GREEN)
# res.sprite_life.set_colorkey((255, 0, 255))

text_surface = font.render('Hello', False, (255, 255, 255))
text_rect = text_surface.get_rect()
print('Text rect:', text_rect, 'center =', text_rect.center)
print('Screen rect:', screen.get_rect(), 'center =', screen.get_rect().center)
text_rect.center = screen.get_rect().center
print(text_rect)

#-----------------------------------------------------------
# Functions
#-----------------------------------------------------------

def make_sub():
    global level
    for k, sector in level['sectors'].items():
        if 'inside' in sector:
            for sk in sector['inside']:
                print(f'Sector {sk} in sector {k}')
                subsector = level['sectors'][sk]
                for w in subsector['walls']:
                    wall = level['walls'][w[0]]
                    goto = w[1]
                    print(f'Adding a wall to sector {k}')
                    if goto == 0:
                        sector['walls'].append([w[0], 0])
                    elif goto == k:
                        sector['walls'].append([w[0], sk]) 
                    else:
                        raise Exception('Not handled.')


def coord2id(wall_segment):
    global level
    for k, w in level['walls'].items():
        if w[0] == wall_segment[0] and w[1] == wall_segment[1] and w[2] == wall_segment[2] and w[3] == wall_segment[3]:
            return k


def get_rect(sector):
    global walls
    min_x = 2000
    min_y = 2000
    max_x = 0
    max_y = 0
    for w in sector['walls']:
        wall = walls[w[0]]
        if wall[0] < min_x: min_x = wall[0]
        if wall[1] < min_y: min_y = wall[1]
        if wall[2] < min_x: min_x = wall[2]
        if wall[3] < min_y: min_y = wall[3]
        if wall[0] > max_x: max_x = wall[0]
        if wall[1] > max_y: max_y = wall[1]
        if wall[2] > max_x: max_x = wall[2]
        if wall[3] > max_y: max_y = wall[3]
    return min_x, min_y, max_x - min_x, max_y - min_y


def is_vert(seg):
    return seg[0] == seg[2]


def is_hori(seg):
    return seg[1] == seg[3]


def intersect_p(seg, point):
    if is_vert(seg): # | même x
        return point[0] == seg[0] and min(seg[1], seg[3]) <= max(seg[1], seg[3])
    elif is_hori(seg):
        return point[1] == seg[1] and min(seg[0], seg[2]) <= max(seg[0], seg[2])
    else:
        raise Exception("Seg not vert nor hori, aborting.")


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
        if is_vert(seg2): # vertical
            if seg1_min_x <= seg2[0] <= seg1_max_x:
                if seg2_min_y <= seg1_min_y <= seg2_max_y: # 221211
                    #print('vertical', seg2[0], 'minxs1', seg1_min_x, 'maxxs1', seg1_max_x, 'minys1', seg1_min_y, 'maxys1', seg1_max_y, seg2_min_y, seg2_max_y)
                    print(f'{turn} crossed', coord2id(seg2))
                    return True
                elif seg2_min_y <= seg1_max_y <= seg2_max_y:  # 112122
                    print(f'{turn} crossed', coord2id(seg2))
                    return True
                elif seg1_min_y <= seg2_min_y and seg1_max_y >= seg2_max_y:  # 11222211
                    print(f'{turn} crossed', coord2id(seg2))
                    return True
        elif is_hori(seg2): # horizontal
            if seg2[1] == seg1[1]: # same line fixée par Y, décrite par X
                if seg2_min_x <= seg1_min_x <= seg2_max_x: # 221211
                    print(f'{turn} crossed', coord2id(seg2))
                    return True
                elif seg2_min_x <= seg1_max_x <= seg2_max_x:  # 112122
                    print(f'{turn} crossed', coord2id(seg2))
                    return True
                elif seg1_min_x <= seg2_min_x and seg1_max_x >= seg2_max_x:  # 11222211
                    print(f'{turn} crossed', coord2id(seg2))
                    return True
        else:
            raise Exception("Wall not angular are not handled")
    elif ab_seg1[1] is None: # vertical
        if seg2[0] == seg2[2]: # vertical
            if seg2[0] == seg1[0]: # same colonne fixée par X, décrite par Y
                if seg2_min_y <= seg1_min_y <= seg2_max_y: # 221211
                    print(f'{turn} crossed', coord2id(seg2))
                    return True
                elif seg2_min_y <= seg1_max_y <= seg2_max_y:  # 112122
                    print(f'{turn} crossed', coord2id(seg2))
                    return True
                elif seg1_min_y <= seg2_min_y and seg1_max_y >= seg2_max_y:  # 11222211
                    print(f'{turn} crossed', coord2id(seg2))
                    return True
        elif seg2[1] == seg2[3]: # horizontal
            if seg1_min_y <= seg2[1] <= seg1_max_y:
                if seg2_min_x <= seg1_min_x <= seg2_max_x: # 221211
                    print(f'{turn} crossed', coord2id(seg2))
                    return True
                elif seg2_min_x <= seg1_max_x <= seg2_max_x:  # 112122
                    print(f'{turn} crossed', coord2id(seg2))
                    return True
                elif seg1_min_x <= seg2_min_x and seg1_max_x >= seg2_max_x:  # 11222211
                    print(f'{turn} crossed', coord2id(seg2))
                    return True
        else:
            raise Exception("Wall not angular are not handled")
    else:
        print(move_left, move_right, move_down, move_up, seg1, ab_seg1)
        if seg2[0] == seg2[2]: # vertical
            raise Exception("A") # True
        elif seg2[1] == seg2[3]: # horizontal
            raise Exception("A") # True
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


#-----------------------------------------------------------
# Test framework
#-----------------------------------------------------------

class TestSession:

    def __init__(self):
        self.nb_test = 0
        self.nb_failure = 0

    def test(self, expression, expected):
        try:
            calc = eval(expression)
        except TypeError:
            print(expression, type(expression))
        self.nb_test += 1
        res = calc == expected
        s = f"Computed= {str(calc):5} Expected= {str(expected):5} Res= {str(res):5} Expr= {expression}"
        if res:
            print(s)
        else:
            self.nb_failure += 1
        sys.stderr.write(s + '\n')

    def dashboard(self):
        nb_success = self.nb_test - self.nb_failure
        print('==========================================')
        print(f"Number of tests   : {self.nb_test:4d} ({round(self.nb_test/self.nb_test*100,0):3.0f}%)")
        sys.stderr.write(f"Number of failure : {self.nb_failure:4d} ({round(self.nb_failure/self.nb_test*100,0):3.0f}%)\n")
        print(f"Number of ok      : {nb_success:4d} ({round(nb_success/self.nb_test*100,0):3.0f}%)")
        print('==========================================')

ts = TestSession()
seg1 = (10, 10, 50, 50)
ts.test('is_vert((10, 10, 10, 100))', True)
ts.test('is_vert(seg1)', False)
ts.test('True', False)
# intersect_p verti
segtest1 = (10, 10, 10, 100)
ts.test('intersect_p(segtest1, (10, 10))', True)
ts.test('intersect_p(segtest1, (10, 100))', True)
ts.test('intersect_p(segtest1, (10, 15))', True)
ts.test('intersect_p(segtest1, (10, 30))', True)
ts.test('intersect_p(segtest1, (10, 45))', True)
ts.test('intersect_p(segtest1, (11, 10))', False)
# intersect_p hori
segtest2 = (10, 25, 100, 25)
ts.test('intersect_p(segtest2, (10, 25))', True)
ts.test('intersect_p(segtest2, (100, 25))', True)
ts.test('intersect_p(segtest2, (30, 25))', True)
ts.test('intersect_p(segtest2, (45, 25))', True)
ts.test('intersect_p(segtest2, (10, 26))', False)
#
ts.dashboard()

#-----------------------------------------------------------
# Data Model
#-----------------------------------------------------------

class Object:

    IDN = 0
    
    def __init__(self, kind, x, y, a=0, s=None):
        Object.IDN += 1
        self.idn = Object.IDN
        self.kind = kind
        self.x = x
        self.y = y
        self.a = a
        self.sector = s
    
    def activate(self, player):
        if self.kind == 'life':
            player.mod_life(10)
            self.remove = True

    def update(self):
        pass

    def __str__(self):
        return f"{self.kind}#{self.idn} @ (x {int(self.x)}, y {int(self.y)}, s{self.sector})"


class Entity(Object):

    def __init__(self, kind, x, y, a=0, s=None, ia=False):
        super().__init__(kind, x, y, a, s)
        self.life = 100
        self.speed = 0.2
        self.remove = False
        self.ia = ia
        self.ia_state = 'stand'
        self.ia_cpt = 30
        self.x_old = self.x
        self.y_old = self.y
    
    def update(self):
        if self.ia:
            self.x_old = self.x
            self.y_old = self.y
            if self.ia_state == 'stand' or self.ia_cpt == 0:
                r = randint(1, 4)
                if r == 1:   self.ia_state = 'left'
                elif r == 2: self.ia_state = 'right'
                elif r == 3: self.ia_state = 'top'
                elif r == 4: self.ia_state = 'down'
                self.ia_cpt = 50
            if self.ia_state == 'left':    self.x -= 1
            elif self.ia_state == 'right': self.x += 1
            elif self.ia_state == 'top':   self.y -= 1
            elif self.ia_state == 'down':  self.y += 1
            self.ia_cpt -= 1
        if self.x_old != self.x or self.y_old != self.y:
            self.check_collision()
        self.dir = self.update_dir()
    
    def mod_life(self, amount):
        self.life = min(max(0, self.life + amount), 999)
        print(f"{self.kind} life set to {self.life:3d}")
    
    def check_collision(self):
        if self.x != self.x_old and self.y != self.y_old:
            raise Exception('MULTI AXIS MOVE FORBIDDEN')
        old_sectors = []
        old_walls = []
        while True:
            old_sectors.append(self.sector)
            for w in sectors[self.sector]['walls']:
                if w[0] not in old_walls:
                    wall = walls[w[0]]
                    goto = w[1]
                    if intersect([self.x_old, self.y_old, self.x, self.y], wall):
                        old_walls.append(w[0])
                        if goto == 0:
                            self.x = self.x_old
                            self.y = self.y_old
                            break
                        elif goto not in old_sectors:
                            if intersect_p(wall, (self.x, self.y)):
                                print(str(self), f'{turn} not changing to new=', goto, 'because we are ON the wall staying at', self.sector)
                            else:
                                print(str(self), f'{turn} changing sector new=', goto, 'old=', self.sector)
                                self.sector = goto
                            break
                        else:
                            print(str(self), f'{turn} not changing to new=', goto, 'because sector already crossed staying at', self.sector)
            if self.sector in old_sectors:
                break

#-----------------------------------------------------------
# Start
#-----------------------------------------------------------

make_sub()
start         = level['start']
walls         = level['walls']
sectors       = level['sectors']
player        = Entity('Player', start[0], start[1], start[2], start[3])
for m in level['monsters']:
    monsters.append(Entity(m['kind'], m['x'], m['y'], m['a'], m['s'], ia=True))
entities      = [player, Entity('life', 20, 20)] + monsters

while not app_end:
    # Drawing picture
    screen.fill(BLACK)
    if mod == 'GAME':
        for i in range(SCREEN_WIDTH):
            pygame.draw.line(screen, GREEN, (i, 50), (i, 150))
        pygame.draw.line(screen, RED, (140, 0), (140, 200))
        screen.blit(greendot, (30, 30))
        screen.blit(text_surface, text_rect)
    elif mod == 'MAP':
        life_surface = font.render(str(player.life), False, (255, 255, 255))
        screen.blit(life_surface, (280, 180))
        pygame.draw.rect(screen, (50, 50, 50), get_rect(level['sectors'][player.sector]))
        for sector_key, sector in sectors.items():
            for w in sector['walls']:
                wall = walls[w[0]]
                goto = w[1]
                color = WHITE if goto == 0 else RED
                pygame.draw.line(screen, color, (wall[0], wall[1]), (wall[2], wall[3]))
                pygame.draw.rect(screen, GREEN,
                                 (wall[0] - 2, wall[1] - 2, 5, 5), 1)
                pygame.draw.rect(screen, (0, 255, 0),
                                 (wall[2] - 2, wall[3] - 2, 5, 5), 1)
            for e in entities:
                if e.kind == 'life':
                    screen.blit(greendot, (e.x - 16, e.y - 16))
        pygame.draw.line(screen, RED, (player.x_old, player.y_old),
                         (player.x, player.y))

        for m in monsters:
            pygame.draw.rect(screen, RED, (m.x - 2, m.y - 2, 5, 5))
            pygame.draw.line(screen, RED, (m.x, m.y), m.dir, 1)
    pygame.display.flip()
    
    # Updating
    player.x_old = player.x
    player.y_old = player.y
    if forward:    player.x, player.y = player.update_dir()
    if backward:   player.x, player.y = player.update_dir(-1)
    if player.x != player.x_old and player.y != player.y_old:
        player.x = player.x_old
    # Check for object activation
    for e in entities:
        dist = math.sqrt((player.x-e.x)*(player.x-e.x) + (player.y-e.y)*(player.y-e.y))
        if dist < 10:
            e.activate(player)
        e.update()
    entities[:] = [o for o in entities if not o.remove]
