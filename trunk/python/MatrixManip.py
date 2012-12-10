import random
import sys

#------------------------------------------------------------------------------
# Create a matrix
#------------------------------------------------------------------------------
map_size_x = 6
map_size_y = 8
matrix = []

y = 0
while y < map_size_y:
    line = []
    x = 0
    while x < map_size_x:
        v = random.randint(0, 100)
        if v > 50: val = 1
        else: val = 0
        line.append(val)
        x += 1
    matrix.append(line)
    y += 1

#print matrix

# pour acceder a un element : matrix[y][x] - c'est a dire line puis colonne
matrix[7][5] = 9

def get(matrix, col, line):
    return matrix[line][col]

def set(matrix, col, line, val):
    matrix[line][col] = val

set(matrix, 5, 7, 3)

# Affichage 1
for line in matrix:
    for elem in line:
        sys.stdout.write(str(elem))
        sys.stdout.write(" ")
    sys.stdout.write("\n")

# Affichage 2
while y < map_size_y:
    while x < map_size_x:
        sys.stdout.write(str(matrix[y][x])+' ')
        x += 1
    sys.stdout.write("\n")
    y += 1
    x = 0

# cette representation est tres bien pour afficher mais pour accer au inverser.

#------------------------------------------------------------------------------
# Blur (calcul de X en X)
#------------------------------------------------------------------------------

print

size_blur = 2
x = 0
y = 0

while y < map_size_y:
    while x < map_size_x:
        #sys.stdout.write(str(matrix[y][x])+' ')
        #--- Le carre
        total = 0
        parcours_x = 0
        parcours_y = 0
        while parcours_x < size_blur:
            while parcours_y < size_blur:
                total += matrix[parcours_y + y][parcours_x + x]
                parcours_y += 1
            parcours_x += 1
            parcours_y = 0
        sys.stdout.write(str(total)+" ")
        #---
        x += size_blur
    sys.stdout.write("\n")
    y += size_blur
    x = 0

#a = random.randint(0,100)
#if a > 50:
#    print "hello"

