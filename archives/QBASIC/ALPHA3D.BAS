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
        IF depart = 0 THEN depart = 1
        SELECT CASE typecase
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
        FOR A = 1 TO 12
        'Testons les murs de devant le h‚ros
        SELECT CASE A
        CASE IS = 1
                ycase = caseav1
        CASE IS = 2
                ycase = caseav2
        CASE IS = 3
                ycase = caseav3
        CASE IS = 4
                ycase = caseav4
        'Testons les murs sur le cot‚ du h‚ros
        CASE IS = 5
                ycase = caseav1
                xcase = casegav
        CASE IS = 6
                ycase = caseav1
                xcase = casedav
        CASE IS = 7
                ycase = caseav2
                xcase = casedav
        CASE IS = 8
                ycase = caseav2
                xcase = casegav
        CASE IS = 9
                ycase = caseav3
                xcase = casegav
        CASE IS = 10
                ycase = caseav3
                xcase = casedav
        CASE IS = 11
                ycase = caseav4
                xcase = casegav
        CASE IS = 12
                ycase = caseav4
                xcase = casedav
        END SELECT
        'Testons
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
        'Affichons maintenant les types cases.
        IF typecase = 0 AND A = 1 THEN LINE (0, 0)-(320, 200), , BF
        IF typecase = 0 AND A = 2 THEN LINE (40, 175)-(280, 25), , BF
        IF typecase = 0 AND A = 3 THEN LINE (80, 150)-(240, 50), , BF
        IF typecase = 0 AND A = 4 THEN LINE (120, 125)-(200, 75), , BF
        IF typecase = 0 AND A = 5 THEN LINE (0, 200)-(40, 175)
        IF typecase = 0 AND A = 5 THEN LINE (0, 0)-(40, 25)
        IF typecase = 1 AND A = 5 THEN LINE (40, 175)-(0, 175)
        IF typecase = 1 AND A = 5 THEN LINE (40, 25)-(0, 25)
        IF typecase = 0 AND A = 6 THEN LINE (320, 0)-(280, 25)
        IF typecase = 0 AND A = 6 THEN LINE (320, 200)-(280, 175)
        IF typecase = 1 AND A = 6 THEN LINE (280, 175)-(320, 175)
        IF typecase = 1 AND A = 6 THEN LINE (280, 25)-(320, 25)
        IF typecase = 0 AND A = 7 THEN LINE (280, 175)-(240, 150)
        IF typecase = 0 AND A = 7 THEN LINE (280, 25)-(240, 50)
        IF typecase = 1 AND A = 7 THEN LINE (240, 150)-(280, 150)
        IF typecase = 1 AND A = 7 THEN LINE (240, 50)-(280, 50)
        IF typecase = 0 AND A = 8 THEN LINE (40, 175)-(80, 150)
        IF typecase = 0 AND A = 8 THEN LINE (40, 25)-(80, 50)
        IF typecase = 1 AND A = 8 THEN LINE (80, 150)-(40, 150)
        IF typecase = 1 AND A = 8 THEN LINE (80, 50)-(40, 50)
        IF typecase = 0 AND A = 9 THEN LINE (80, 150)-(120, 125)
        IF typecase = 0 AND A = 9 THEN LINE (80, 50)-(120, 75)
        IF typecase = 1 AND A = 9 THEN LINE (120, 125)-(80, 125)
        IF typecase = 1 AND A = 9 THEN LINE (120, 75)-(80, 75)
        IF typecase = 0 AND A = 10 THEN LINE (240, 150)-(200, 125)
        IF typecase = 0 AND A = 10 THEN LINE (240, 50)-(200, 75)
        IF typecase = 1 AND A = 10 THEN LINE (200, 125)-(240, 125)
        IF typecase = 1 AND A = 10 THEN LINE (200, 75)-(240, 75)
        IF typecase = 0 AND A = 11 THEN LINE (120, 125)-(160, 100)
        IF typecase = 0 AND A = 11 THEN LINE (120, 75)-(160, 100)
        IF typecase = 1 AND A = 11 THEN LINE (160, 100)-(120, 100)
        IF typecase = 0 AND A = 12 THEN LINE (200, 75)-(160, 100)
        IF typecase = 0 AND A = 12 THEN LINE (200, 125)-(160, 100)
        IF typecase = 1 AND A = 12 THEN LINE (160, 100)-(200, 100)
        NEXT A
        END SELECT
        LINE (x, y)-(x, y)
        RETURN



