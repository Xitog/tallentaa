'D‚finition ‚cran 320 * 200 avec pixel et texte
CLS
SCREEN 7
'Coordonn‚es de base
postete = 1
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
LINE (x - 5, y - 5)-(x + 5, y + 5), , B
IF postete = 1 THEN LINE (x, y)-(x, y - 5)
IF postete = 2 THEN LINE (x, y)-(x + 5, y)
IF postete = 3 THEN LINE (x, y)-(x, y + 5)
IF postete = 4 THEN LINE (x, y)-(x - 5, y)
IF depart = 0 THEN GOSUB affichage
WEND
CLOSE
END
efface:
        LINE (x, y)-(x, y), 0
        RETURN

droite:
        GOSUB efface
        postete = postete + 1
        IF postete = 5 THEN postete = 1
        GOSUB affichage
        RETURN

haut:
        GOSUB efface
        IF postete = 1 THEN yf = y - 10
        IF postete = 2 THEN xf = x + 10
        IF postete = 3 THEN yf = y + 10
        IF postete = 4 THEN xf = x - 10
        IF postete = 1 THEN ycase = ycasepre - 1
        IF postete = 2 THEN xcase = xcasepre + 1
        IF postete = 3 THEN ycase = ycasepre + 1
        IF postete = 4 THEN xcase = xcasepre - 1
        GOSUB affichage
        RETURN

bas:
        GOSUB efface
        IF postete = 1 THEN yf = y + 10
        IF postete = 2 THEN xf = x - 10
        IF postete = 3 THEN yf = y - 10
        IF postete = 4 THEN xf = x + 10
        IF postete = 1 THEN ycase = ycasepre + 1
        IF postete = 2 THEN xcase = xcasepre - 1
        IF postete = 3 THEN ycase = ycasepre - 1
        IF postete = 4 THEN xcase = xcasepre + 1
        GOSUB affichage
        RETURN

gauche:
        GOSUB efface
        postete = postete - 1
        IF postete = 0 THEN postete = 4
        GOSUB affichage
        RETURN

affichage:
        'Ce qui suit constitue le niveau. Typecase = 1, il y a un chemin
        GOSUB MatrixLevel1
        IF depart = 0 THEN depart = 1
        IF typecase = 0 THEN RETURN
        CLS
        x = xf
        y = yf
        xcasepre = xcase
        ycasepre = ycase
        'Nous effectuons un premier affichage 3D
        'Etape nø1 : d‚terminer la vue (4 positions) du h‚ros (var : postete)
        'A l'aide de postete on d‚terminons les 4 prochaines cases 
        SELECT CASE postete
                CASE IS = 1
                        caseav1 = ycasepre - 1
                        caseav2 = ycasepre - 2
                        caseav3 = ycasepre - 3
                        caseav4 = ycasepre - 4
                        xcase = xcasepre
                        caseavd = xcasepre + 1
                        caseavg = xcasepre - 1
                CASE IS = 2
                        caseav1 = xcasepre + 1
                        caseav2 = xcasepre + 2
                        caseav3 = xcasepre + 3
                        caseav4 = xcasepre + 4
                        ycase = ycasepre
                        caseavd = ycase + 1
                        caseavg = ycase - 1
                CASE IS = 3
                        caseav1 = ycasepre + 1
                        caseav2 = ycasepre + 2
                        caseav3 = ycasepre + 3
                        caseav4 = ycasepre + 4
                        xcase = xcasepre
                        caseavd = xcasepre - 1
                        caseavg = xcasepre + 1
                CASE IS = 4
                        caseav1 = xcasepre - 1
                        caseav2 = xcasepre - 2
                        caseav3 = xcasepre - 3
                        caseav4 = xcasepre - 4
                        ycase = ycasepre
                        caseavd = ycase - 1
                        caseavg = ycase + 1
        END SELECT
        'Now, testons les pour savoir leurs types cases
        A = 1
AGA:
        SELECT CASE A
                CASE IS = 1
                        IF postete = 1 OR postete = 3 THEN ycase = caseav1
                        IF postete = 1 OR postete = 3 THEN xcase = xcasepre'xcase = xcasepre
                        IF postete = 2 OR postete = 4 THEN xcase = caseav1
                        IF postete = 2 OR postete = 4 THEN ycase = ycasepre'xcase = xcasepre
                        x1 = 0
                        x2 = 320
                        y1 = 0
                        y2 = 200
                CASE IS = 2
                        IF postete = 1 OR postete = 3 THEN ycase = caseav2
                        IF postete = 1 OR postete = 3 THEN xcase = xcasepre'xcase = xcasepre
                        IF postete = 2 OR postete = 4 THEN xcase = caseav2
                        IF postete = 2 OR postete = 4 THEN ycase = ycasepre'xcase = xcasepre
                        x1 = 40
                        y1 = 25
                        x2 = 280
                        y2 = 175
                CASE IS = 3
                        IF postete = 1 OR postete = 3 THEN ycase = caseav3
                        IF postete = 1 OR postete = 3 THEN xcase = xcasepre'xcase = xcasepre
                        IF postete = 2 OR postete = 4 THEN xcase = caseav3
                        IF postete = 2 OR postete = 4 THEN ycase = ycasepre'xcase = xcasepre
                        x1 = 80
                        y1 = 50
                        x2 = 240
                        y2 = 150
                CASE IS = 4
                        IF postete = 1 OR postete = 3 THEN ycase = caseav4
                        IF postete = 1 OR postete = 3 THEN xcase = xcasepre'xcase = xcasepre
                        IF postete = 2 OR postete = 4 THEN xcase = caseav4
                        IF postete = 2 OR postete = 4 THEN ycase = ycasepre'xcase = xcasepre
                        x1 = 120
                        y1 = 75
                        x2 = 200
                        y2 = 125
        END SELECT
        GOSUB MatrixLevel1
        typecasea = typecase
                SELECT CASE typecasea
                CASE IS = 0
                        LINE (x1, y1)-(x2, y1)
                        LINE (x1, y2)-(x2, y2)
                        RETURN
                CASE IS = 1
                        LINE (x1 + 40, y1 + 25)-(x1 + 40, y2 - 25)
                        LINE (x2 - 40, y1 + 25)-(x2 - 40, y2 - 25)
                END SELECT
        IF postete = 1 OR postete = 3 THEN xcase = caseavg
        IF postete = 2 OR postete = 4 THEN ycase = caseavg
        IF A = 1 AND postete = 1 OR A = 1 AND postete = 3 THEN ycase = caseav1
        IF A = 2 AND postete = 1 OR A = 2 AND postete = 3 THEN ycase = caseav2
        IF A = 3 AND postete = 1 OR A = 3 AND postete = 3 THEN ycase = caseav3
        IF A = 4 AND postete = 1 OR A = 4 AND postete = 3 THEN ycase = caseav4
        IF A = 1 AND postete = 2 OR A = 1 AND postete = 4 THEN xcase = caseav1
        IF A = 2 AND postete = 2 OR A = 2 AND postete = 4 THEN xcase = caseav2
        IF A = 3 AND postete = 2 OR A = 3 AND postete = 4 THEN xcase = caseav3
        IF A = 4 AND postete = 2 OR A = 4 AND postete = 4 THEN xcase = caseav4
        GOSUB MatrixLevel1
        typecaseg = typecase
                SELECT CASE typecaseg
                CASE IS = 0
                        LINE (x1, y1)-(x1 + 40, y1 + 25)
                        LINE (x1, y2)-(x1 + 40, y2 - 25)
                CASE IS = 1
                        LINE (x1 + 40, y1 + 25)-(x1, y1 + 25)
                        LINE (x1 + 40, y2 - 25)-(x1, y2 - 25)
                END SELECT
        IF postete = 1 OR postete = 3 THEN xcase = caseavd
        IF postete = 2 OR postete = 4 THEN ycase = caseavd
        IF A = 1 AND postete = 1 OR A = 1 AND postete = 3 THEN ycase = caseav1
        IF A = 2 AND postete = 1 OR A = 2 AND postete = 3 THEN ycase = caseav2
        IF A = 3 AND postete = 1 OR A = 3 AND postete = 3 THEN ycase = caseav3
        IF A = 4 AND postete = 1 OR A = 4 AND postete = 3 THEN ycase = caseav4
        IF A = 1 AND postete = 2 OR A = 1 AND postete = 4 THEN xcase = caseav1
        IF A = 2 AND postete = 2 OR A = 2 AND postete = 4 THEN xcase = caseav2
        IF A = 3 AND postete = 2 OR A = 3 AND postete = 4 THEN xcase = caseav3
        IF A = 4 AND postete = 2 OR A = 4 AND postete = 4 THEN xcase = caseav4
        GOSUB MatrixLevel1
        typecased = typecase
                SELECT CASE typecased
                CASE IS = 0
                        LINE (x2, y1)-(x2 - 40, y1 + 25)
                        LINE (x2, y2)-(x2 - 40, y2 - 25)
                CASE IS = 1
                        LINE (x2 - 40, y1 + 25)-(x2, y1 + 25)
                        LINE (x2 - 40, y2 - 25)-(x2, y2 - 25)
                END SELECT
        A = A + 1
        IF A < 5 THEN GOSUB AGA
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

