import pygame

pygame.init()

surf = pygame.image.load(r"C:\Users\damie_000\Documents\GitHub\tallentaa\projet_format\yodata\output\1.png")

pixels = pygame.PixelArray(surf)

colors = {}

for lin in range(0, 32):
    for col in range(0, 32):
        v = pixels[lin, col]
        if v not in colors:
            colors[v] = 1
        else:
            colors[v] += 1

print("Mapped int", "RGB", "Nb")

for key, nb in colors.items():
    print(key, surf.unmap_rgb(key), nb)

# deux couleurs seulement pour le sable !
# -7883793 (239, 179, 135, 255) 644
# -8145929 (247, 179, 131, 255) 380
