'D‚finition ‚cran 320 * 200 avec pixel et texte
CLS
SCREEN 7
'Coordonn‚es de base
depart = 0
xcasepre = 2
ycasepre = 16
x = xcasepre * 10
y = ycasepre * 10
'D‚finition des Getkey
CONST esc = 27
ON KEY(13) GOSUB droite
KEY(13) ON
ON KEY(11) GOSUB haut
KEY(11) ON
ON KEY(14) GOSUB bas
KEY(14) ON
ON KEY(12) GOSUB gauche
KEY(12) ON
'Boucle principale du jeu
WHILE INKEY$ <> CHR$(esc)
xcase = xcasepre
ycase = ycasepre
xf = x
yf = y
LOCATE 1, 1
PRINT xcasepre
PRINT ycasepre
PRINT A
PRINT B
LINE (x - 5, y - 5)-(x + 5, y + 5), , B
IF depart = 0 THEN GOSUB affichage
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
        'Ce qui suit constitue le niveau. Typecase = 1, il y a un chemin
        GOSUB MatrixLevel1
        IF depart = 0 THEN depart = 1
        SELECT CASE typecase
        CASE IS = 0
                RETURN
        CASE IS = 1
                CLS
                x = xf
                y = yf
                xcasepre = xcase
                ycasepre = ycase
        'Nous effectuons un premier affichage 3D
                'D‚terminons les 4 prochaines cases
        caseav1 = ycasepre - 1
        caseav2 = ycasepre - 2
        caseav3 = ycasepre - 3
        caseav4 = ycasepre - 4
        casegav = xcasepre - 1
        casedav = xcasepre + 1
        xcase = xcasepre
                'Now, testons -les pour savoir leurs types cases
        FOR A = 1 TO 4
        xcase = xcasepre
                SELECT CASE A
                CASE IS = 1
                        ycase = caseav1
                        x1 = 0
                        x2 = 320
                        y1 = 0
                        y2 = 200
                CASE IS = 2
                        ycase = caseav2
                CASE IS = 3
                        ycase = caseav3
                CASE IS = 4
                        ycase = caseav4
                END SELECT
                typecase = 0
                GOSUB MatrixLevel1
                typecasea = typecase
        SELECT CASE A
        CASE IS = 1
                SELECT CASE typecasea
                CASE IS = 0
                        LINE (x1, y1)-(x2, y1)
                        LINE (x1, y2)-(x2, y2)
                        RETURN
                CASE IS = 1
                        LINE (x1 + 40, y1 + 25)-(x1 + 40, y2 - 25)
                        LINE (x2 - 40, y1 + 25)-(x2 - 40, y2 - 25)
                END SELECT
        xcase = xcasepre - 1
        ycase = ycaseav1
        GOSUB MatrixLevel1
        typecaseg = typecase
                SELECT CASE typecaseg
                CASE IS = 0
                        LINE (x1, y1)-(x1 + 40, y1 + 25)
                        LINE (x1, y2)-(x1 + 40, y2 - 25)
                CASE IS = 1
                        LINE (x1 + 40, y1 + 25)-(x1, y1 + 25)
                        LINE (x1 + 40, y2)-(x1, y2)
                END SELECT
        xcase = xcasepre + 1
        ycase = ycaseav1
        GOSUB MatrixLevel1
        typecased = typecase
                SELECT CASE typecased
                CASE IS = 0
                        LINE (320, 0)-(280, 25)
                        LINE (320, 200)-(280, 175)
                CASE IS = 1
                        LINE (280, 25)-(320, 25)
                        LINE (280, 175)-(320, 175)
                END SELECT
        CASE IS = 2
                SELECT CASE typecasea
                CASE IS = 0
                        LINE (40, 175)-(280, 175)
                        LINE (40, 25)-(280, 25)
                        RETURN
                CASE IS = 1
                        LINE (80, 50)-(80, 150)
                        LINE (240, 50)-(240, 150)
                        LINE (40, 25)-(80, 50)
                        LINE (40, 175)-(80, 150)
                        LINE (280, 25)-(240, 50)
                        LINE (280, 175)-(240, 150)
                END SELECT
        CASE IS = 3
                SELECT CASE typecasea
                CASE IS = 0
                        LINE (80, 150)-(240, 150)
                        LINE (80, 50)-(240, 50)
                        RETURN
                CASE IS = 1
                        LINE (200, 75)-(200, 125)
                        LINE (120, 75)-(120, 125)
                        LINE (80, 50)-(120, 75)
                        LINE (80, 150)-(120, 125)
                        LINE (240, 50)-(200, 75)
                        LINE (240, 150)-(200, 125)
                 END SELECT
        CASE IS = 4
                SELECT CASE typecasea
                CASE IS = 0
                        LINE (120, 125)-(200, 125)
                        LINE (120, 75)-(200, 75)
                        RETURN
                CASE IS = 1
                        LINE (160, 100)-(160, 100)
                        LINE (120, 75)-(160, 100)
                        LINE (120, 125)-(160, 100)
                        LINE (200, 75)-(160, 100)
                        LINE (200, 125)-(160, 100)
                END SELECT
        END SELECT
        NEXT A
        END SELECT
        LINE (x, y)-(x, y)
        RETURN

MatrixLevel1:
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
RETURN

