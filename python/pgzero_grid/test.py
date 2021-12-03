import pgzrun
import random

#alien = Actor('alien')
#alien.pos = 100, 56

WIDTH = 640
HEIGHT = 480

NB_COL = WIDTH // 32
NB_LIN = HEIGHT // 32

print(NB_COL, 'x', NB_LIN)

def create_matrix(col, lin, default=0):
    matrix = []
    for y in range(0, lin):
        matrix.append([])
        for x in range(0, col):
            matrix[-1].append(default)
    return matrix

def display_matrix(matrix):
    print(f'Matrix ({len(matrix[0])} x {len(matrix)})')
    for y in range(0, NB_LIN):
        for x in range(0, NB_COL):
            print(matrix[y][x], end='')
        print()
    print()

#matrix = [[0] * NB_COL] * NB_LIN
matrix = create_matrix(NB_COL, NB_LIN)
display_matrix(matrix)

for y in range(0, NB_LIN):
    for x in range(0, NB_COL):
        if random.randint(1, 6) > 3:
            matrix[y][x] = 1

display_matrix(matrix)

def draw():
    for c in range(0, NB_COL):
        for l in range(0, NB_LIN):
            screen.draw.rect(Rect((c*32, l*32), (32, 32)), (0, 128,0))
            if matrix[l][c] == 1:
                screen.draw.filled_rect(Rect((c*32, l*32), (32, 32)), (128, 0,128))
    #alien.draw()

def update():
    pass
    #alien.left += 2
    #if alien.left > WIDTH:
    #    alien.right = 0

def on_mouse_down(pos):
    col = pos[0] // 32
    lin = pos[1] // 32
    print(col, 'x', lin, matrix[lin][col])
    #if alien.collidepoint(pos):
    #    print("Eek!")
    #    sounds.eep.play()
    #    alien.image = 'alien_hurt'
    #    clock.schedule_unique(set_alien_normal, 1.0)
    #else:
    #    print("You missed me!")

def set_alien_normal():
    alien.image = 'alien'

pgzrun.go()
