
def matrix_create(width: int, height: int, base: object):
    a = []
    for lin in range(0, height):
        a.append([])
        for col in range(0, width):
            a[-1].append(base)
    return a

def matrix_create_copy(matrix):
    a = matrix_create(matrix_width(matrix), matrix_height(matrix), 0)
    for y in range(0, len(matrix)):
        for x in range(0, len(matrix[y])):
            a[y][x] = matrix[y][x]
    return a

def matrix_display(matrix):
    print(f'Display : Width {matrix_width(matrix)} Height {matrix_height(matrix)}')
    for y in range(0, len(matrix)):
        for x in range(0, len(matrix[y])):
            print(f'{matrix[y][x]:0>1} ', end='')
        print()

def matrix_identity(matrix1, matrix2):
    for y in range(0, len(matrix1)):
        for x in range(0, len(matrix1[y])):
            if matrix1[y][x] != matrix2[y][x]:
                return False
    return True

def matrix_set(matrix, col: int, lin: int, value: int):
    #print(f'Set : {value} at x/col {col}, y/lin {lin}')
    matrix[lin][col] = value

def matrix_get(matrix, col: int, lin: int):
    return matrix[lin][col]

def matrix_intelliset(matrix, col: int, lin: int, value: int):
    print(f'Intelliset : {value} at x/col {col}, y/lin {lin}')
    matrix[lin][col] = value

def matrix_width(matrix):
    return len(matrix[0])

def matrix_height(matrix):
    return len(matrix)

def matrix_check(matrix, col: int, lin: int):
    return 0 <= col < matrix_width(matrix) and 0 <= lin < matrix_height(matrix)

def matrix_screenshot(matrix):
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    background = pygame.Surface((32 * matrix_width(matrix), 32 * matrix_height(matrix)))
    background.fill((128,255,128))
    
    eau_terre = [
        pygame.image.load(r"U:\Transfert\borders\data\eau-terre-01.png").convert(),
        pygame.image.load(r"U:\Transfert\borders\data\eau-terre-02.png").convert(),
        pygame.image.load(r"U:\Transfert\borders\data\eau-terre-03.png").convert(),
        pygame.image.load(r"U:\Transfert\borders\data\eau-terre-04.png").convert(),
        pygame.image.load(r"U:\Transfert\borders\data\eau-terre-05.png").convert(),
        pygame.image.load(r"U:\Transfert\borders\data\eau-terre-06.png").convert(),
        pygame.image.load(r"U:\Transfert\borders\data\eau-terre-07.png").convert(),
        pygame.image.load(r"U:\Transfert\borders\data\eau-terre-08.png").convert(),
        pygame.image.load(r"U:\Transfert\borders\data\eau.png").convert()
    ]
    
    for y in range(0, len(matrix)):
        for x in range(0, len(matrix[y])):
            if matrix[y][x] == 'E':
                background.blit(eau_terre[-1], (x * 32, y * 32))
    
    background = background.convert()
    pygame.image.save(background, r"U:\Transfert\borders\output\saved.png")
    pygame.quit()

d = matrix_create(10, 5, 0)
matrix_set(d, 9, 0, 8)
matrix_display(d)
print(f"Matrix check 20, 30: {matrix_check(d, 20, 30)}")
print(f"Matrix check 10, 4: {matrix_check(d, 10, 4)}")
print(f"Matrix check 9, 5: {matrix_check(d, 9, 5)}")
print(f"Matrix check 9, 4: {matrix_check(d, 9, 4)}")

import random
for y in range(0, matrix_height(d)):
    for x in range(0, matrix_width(d)):
        u = random.randint(0, 9)
        if u > 7:
            matrix_set(d, x, y, '~')
matrix_display(d)
d2 = matrix_create_copy(d)

for y in range(0, matrix_height(d)):
    for x in range(0, matrix_width(d)):
        # E0 0E  
        # 0E E0
        if matrix_get(d, x, y) == '~': # around only ground 'g' or '~'
            if y > 0 and matrix_get(d, x, y - 1) not in ['g', '~']:
                matrix_set(d, x, y - 1, 'g')
            if x > 0 and matrix_get(d, x - 1, y) not in ['g', '~']:
                matrix_set(d, x - 1, y, 'g')
            if y > 0 and x > 0 and matrix_get(d, x - 1, y - 1) not in ['g', '~']:
                matrix_set(d, x - 1, y - 1, 'g')
            if y < matrix_height(d) - 1 and matrix_get(d, x, y + 1) not in ['g', '~']:
                matrix_set(d, x, y + 1, 'g')
            if x < matrix_width(d) - 1 and matrix_get(d, x + 1, y) not in ['g', '~']:
                matrix_set(d, x + 1, y, 'g')
            if y < matrix_height(d) - 1 and x < matrix_width(d) - 1 and matrix_get(d, x + 1, y + 1) not in ['g', '~']:
                matrix_set(d, x + 1, y + 1, 'g')
            if x < matrix_width(d) - 1 and y > 0 and matrix_get(d, x + 1, y - 1) not in ['g', '~']:
                matrix_set(d, x + 1, y - 1, 'g')
            if y < matrix_height(d) - 1 and x > 0 and matrix_get(d, x - 1, y + 1) not in ['g', '~']:
                matrix_set(d, x - 1, y + 1, 'g')
        elif matrix_get(d, x, y) == 'g':
            pass # test en diag. si eau, il devient eau.
            
        #if y < matrix_height(d) - 1 and x < matrix_width(d) - 1:
        #    if matrix_get(d, x, y) == 'E' and matrix_get(d, x + 1, y + 1) == 'E':
        #        matrix_set(d, x + 1, y, 'E')
        #        matrix_set(d, x, y + 1, 'E')
        #if y > 0 and x > 0:
        #    if matrix_get(d, x, y) == 'E' and matrix_get(d, x - 1, y - 1) == 'E':
        #        matrix_set(d, x - 1, y, 'E')
        #        matrix_set(d, x, y - 1, 'E')

matrix_display(d)

print(f"Matrix identity: {matrix_identity(d, d2)}")

matrix_screenshot(d)
