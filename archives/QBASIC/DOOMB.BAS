SCREEN 7
xcasepre = 5
ycasepre = 14
x = xcasepre * 10
y = ycasepre * 10
CONST esc = 27
ON KEY(13) GOSUB droite
KEY(13) ON
ON KEY(11) GOSUB haut
KEY(11) ON
ON KEY(14) GOSUB bas
KEY(14) ON
ON KEY(12) GOSUB gauche
KEY(12) ON
WHILE INKEY$ <> CHR$(esc)
xcase = xcasepre
ycase = ycasepre
xf = x
yf = y
LOCATE 1, 1
PRINT xcasepre
PRINT ycasepre
LINE (x - 5, y - 5)-(x + 5, y + 5), , B
WEND
CLOSE
END
efface:
        LINE (x, y)-(x, y), 0
        RETURN

droite:
        GOSUB efface
        xf = x + 10
        xcase = xcasepre + 1
        GOSUB affichage
        RETURN

haut:
        GOSUB efface
        yf = y - 10
        ycase = ycasepre - 1
        GOSUB affichage
        RETURN

bas:
        GOSUB efface
        yf = y + 10
        ycase = ycasepre + 1
        GOSUB affichage
        RETURN

gauche:
        GOSUB efface
        xf = x - 10
        xcase = xcasepre - 1
        GOSUB affichage
        RETURN

affichage:
        typecase = 0
        IF xcase = 14 AND ycase = 7 THEN typecase = 1
        IF xcase = 2 AND ycase = 11 THEN typecase = 1
        IF xcase = 2 AND ycase = 16 THEN typecase = 1
        IF xcase = 2 AND ycase = 15 THEN typecase = 1
        IF xcase = 2 AND ycase = 14 THEN typecase = 1
        IF xcase = 2 AND ycase = 13 THEN typecase = 1
        IF xcase = 2 AND ycase = 12 THEN typecase = 1
        IF xcase = 2 AND ycase = 10 THEN typecase = 1
        IF xcase = 2 AND ycase = 9 THEN typecase = 1
        IF xcase = 3 AND ycase = 9 THEN typecase = 1
        IF xcase = 4 AND ycase = 9 THEN typecase = 1
        IF xcase = 4 AND ycase = 8 THEN typecase = 1
        IF xcase = 4 AND ycase = 7 THEN typecase = 1
        IF xcase = 4 AND ycase = 6 THEN typecase = 1
        IF xcase = 4 AND ycase = 5 THEN typecase = 1
        IF xcase = 4 AND ycase = 4 THEN typecase = 1
        IF xcase = 5 AND ycase = 4 THEN typecase = 1
        IF xcase = 6 AND ycase = 4 THEN typecase = 1
        IF xcase = 7 AND ycase = 4 THEN typecase = 1
        IF xcase = 8 AND ycase = 4 THEN typecase = 1
        IF xcase = 9 AND ycase = 4 THEN typecase = 1
        IF xcase = 10 AND ycase = 4 THEN typecase = 1
        IF xcase = 11 AND ycase = 4 THEN typecase = 1
        IF xcase = 12 AND ycase = 4 THEN typecase = 1
        IF xcase = 13 AND ycase = 4 THEN typecase = 1
        IF xcase = 14 AND ycase = 4 THEN typecase = 1
        IF xcase = 14 AND ycase = 3 THEN typecase = 1
        IF xcase = 14 AND ycase = 2 THEN typecase = 1
        IF xcase = 14 AND ycase = 5 THEN typecase = 1
        IF xcase = 14 AND ycase = 6 THEN typecase = 1
        IF xcase = 14 AND ycase = 8 THEN typecase = 1
        IF xcase = 14 AND ycase = 9 THEN typecase = 1
        IF xcase = 14 AND ycase = 10 THEN typecase = 1
        IF xcase = 14 AND ycase = 11 THEN typecase = 1
        IF xcase = 14 AND ycase = 12 THEN typecase = 1
        IF xcase = 14 AND ycase = 13 THEN typecase = 1
        IF xcase = 14 AND ycase = 13 THEN typecase = 1
        IF xcase = 14 AND ycase = 13 THEN typecase = 1
        IF xcase = 14 AND ycase = 14 THEN typecase = 1
        IF xcase = 13 AND ycase = 14 THEN typecase = 1
        IF xcase = 12 AND ycase = 14 THEN typecase = 1
        IF xcase = 9 AND ycase = 14 THEN typecase = 1
        IF xcase = 10 AND ycase = 14 THEN typecase = 1
        IF xcase = 8 AND ycase = 14 THEN typecase = 1
        IF xcase = 7 AND ycase = 14 THEN typecase = 1
        IF xcase = 6 AND ycase = 14 THEN typecase = 1
        IF xcase = 5 AND ycase = 14 THEN typecase = 1
        IF xcase = 4 AND ycase = 14 THEN typecase = 1
        IF xcase = 3 AND ycase = 14 THEN typecase = 1
        IF xcase = 7 AND ycase = 13 THEN typecase = 1
        IF xcase = 7 AND ycase = 12 THEN typecase = 1
        IF xcase = 7 AND ycase = 11 THEN typecase = 1
        IF xcase = 7 AND ycase = 10 THEN typecase = 1
        IF xcase = 7 AND ycase = 9 THEN typecase = 1
        IF xcase = 7 AND ycase = 8 THEN typecase = 1
        IF xcase = 7 AND ycase = 7 THEN typecase = 1
        IF xcase = 6 AND ycase = 7 THEN typecase = 1
        IF xcase = 5 AND ycase = 7 THEN typecase = 1
        IF xcase = 8 AND ycase = 7 THEN typecase = 1
        IF xcase = 9 AND ycase = 7 THEN typecase = 1
        IF xcase = 10 AND ycase = 7 THEN typecase = 1
        IF xcase = 10 AND ycase = 8 THEN typecase = 1
        IF xcase = 10 AND ycase = 9 THEN typecase = 1
        IF xcase = 10 AND ycase = 10 THEN typecase = 1
        IF xcase = 10 AND ycase = 11 THEN typecase = 1
        IF xcase = 11 AND ycase = 11 THEN typecase = 1
        IF xcase = 12 AND ycase = 11 THEN typecase = 1
        IF xcase = 11 AND ycase = 14 THEN typecase = 1
        SELECT CASE typecase
        CASE IS = 1
                x = xf
                y = yf
                xcasepre = xcase
                ycasepre = ycase
        END SELECT
        LINE (x, y)-(x, y)
        RETURN

