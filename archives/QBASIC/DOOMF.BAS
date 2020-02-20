CLS
SCREEN 7
LINE (0, 0)-(320, 200), 8, BF
LINE (0, 0)-(25, 25), , B
xbase = 12.5
ybase = 12.5
x = 12.5
y = 0
LINE (xbase, ybase)-(x, y)
position = 1
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
LINE (xbase, ybase)-(x, y)
WEND
CLOSE
END
droite:
        droite = 1
        GOSUB desaffiche
        GOSUB affiche
        droite = 0
        RETURN

haut:
        haut = 1
        GOSUB desaffiche
        GOSUB affiche
        haut = 0
        RETURN

bas:
        bas = 1
        GOSUB desaffiche
        GOSUB affiche
        bas = 0
        RETURN

gauche:
        gauche = 1
        GOSUB desaffiche
        GOSUB affiche
        gauche = 0
        RETURN

desaffiche:
        CLS
        RETURN

affiche:
        SELECT CASE position
        CASE IS = 1
                IF droite = 1 THEN x = x + 12.5
                IF droite = 1 THEN position = 2
                IF droite = 1 THEN RETURN
                IF gauche = 1 THEN x = x - 12.5
                IF gauche = 1 THEN position = 8
                IF gauche = 1 THEN RETURN
                IF haut = 1 THEN ybase = ybase - 12.5
                IF haut = 1 THEN y = y - 12.5
                IF haut = 1 THEN RETURN
                IF bas = 1 THEN ybase = ybase + 12.5
                IF bas = 1 THEN y = y + 12.5
                IF bas = 1 THEN RETURN
                CASE IS = 2
                IF droite = 1 THEN y = y + 12.5
                IF droite = 1 THEN position = 3
                IF droite = 1 THEN RETURN
                IF gauche = 1 THEN x = x - 12.5
                IF gauche = 1 THEN position = 1
                IF gauche = 1 THEN RETURN
                IF haut = 1 THEN ybase = ybase - 12.5
                IF haut = 1 THEN y = y - 12.5
                IF haut = 1 THEN xbase = xbase + 12.5
                IF haut = 1 THEN x = x + 12.5
                IF haut = 1 THEN RETURN
                IF bas = 1 THEN ybase = ybase + 12.5
                IF bas = 1 THEN y = y + 12.5
                IF bas = 1 THEN xbase = xbase - 12.5
                IF bas = 1 THEN x = x - 12.5
                IF bas = 1 THEN RETURN
        CASE IS = 3
                IF droite = 1 THEN y = y + 12.5
                IF droite = 1 THEN position = 4
                IF droite = 1 THEN RETURN
                IF gauche = 1 THEN y = y - 12.5
                IF gauche = 1 THEN position = 2
                IF gauche = 1 THEN RETURN
                IF haut = 1 THEN xbase = xbase + 12.5
                IF haut = 1 THEN x = x + 12.5
                IF haut = 1 THEN RETURN
                IF bas = 1 THEN xbase = xbase - 12.5
                IF bas = 1 THEN x = x - 12.5
                IF bas = 1 THEN RETURN
        CASE IS = 4
                IF droite = 1 THEN x = x - 12.5
                IF droite = 1 THEN position = 5
                IF droite = 1 THEN RETURN
                IF gauche = 1 THEN y = y - 12.5
                IF gauche = 1 THEN position = 3
                IF gauche = 1 THEN RETURN
                IF haut = 1 THEN xbase = xbase + 12.5
                IF haut = 1 THEN x = x + 12.5
                IF haut = 1 THEN ybase = ybase + 12.5
                IF haut = 1 THEN y = y + 12.5
                IF haut = 1 THEN RETURN
                IF bas = 1 THEN ybase = ybase - 12.5
                IF bas = 1 THEN y = y - 12.5
                IF bas = 1 THEN xbase = xbase - 12.5
                IF bas = 1 THEN x = x - 12.5
                IF bas = 1 THEN RETURN
         CASE IS = 5
                IF droite = 1 THEN x = x - 12.5
                IF droite = 1 THEN position = 6
                IF droite = 1 THEN RETURN
                IF gauche = 1 THEN x = x + 12.5
                IF gauche = 1 THEN position = 4
                IF gauche = 1 THEN RETURN
                IF haut = 1 THEN ybase = ybase + 12.5
                IF haut = 1 THEN y = y + 12.5
                IF haut = 1 THEN RETURN
                IF bas = 1 THEN ybase = ybase - 12.5
                IF bas = 1 THEN y = y - 12.5
                IF bas = 1 THEN RETURN
         CASE IS = 6
                IF droite = 1 THEN y = y - 12.5
                IF droite = 1 THEN position = 7
                IF droite = 1 THEN RETURN
                IF gauche = 1 THEN x = x + 12.5
                IF gauche = 1 THEN position = 5
                IF gauche = 1 THEN RETURN
                IF haut = 1 THEN ybase = ybase + 12.5
                IF haut = 1 THEN y = y + 12.5
                IF haut = 1 THEN xbase = xbase - 12.5
                IF haut = 1 THEN x = x - 12.5
                IF haut = 1 THEN RETURN
                IF bas = 1 THEN ybase = ybase - 12.5
                IF bas = 1 THEN y = y - 12.5
                IF bas = 1 THEN xbase = xbase + 12.5
                IF bas = 1 THEN x = x + 12.5
                IF bas = 1 THEN RETURN
         CASE IS = 7
                IF droite = 1 THEN y = y - 12.5
                IF droite = 1 THEN position = 8
                IF droite = 1 THEN RETURN
                IF gauche = 1 THEN y = y + 12.5
                IF gauche = 1 THEN position = 6
                IF gauche = 1 THEN RETURN
                IF haut = 1 THEN xbase = xbase - 12.5
                IF haut = 1 THEN x = x - 12.5
                IF haut = 1 THEN RETURN
                IF bas = 1 THEN xbase = xbase + 12.5
                IF bas = 1 THEN x = x + 12.5
                IF bas = 1 THEN RETURN
        
         CASE IS = 8
                IF droite = 1 THEN x = x + 12.5
                IF droite = 1 THEN position = 1
                IF droite = 1 THEN RETURN
                IF gauche = 1 THEN y = y + 12.5
                IF gauche = 1 THEN position = 7
                IF gauche = 1 THEN RETURN
                IF haut = 1 THEN ybase = ybase - 12.5
                IF haut = 1 THEN y = y - 12.5
                IF haut = 1 THEN xbase = xbase - 12.5
                IF haut = 1 THEN x = x - 12.5
                IF haut = 1 THEN RETURN
                IF bas = 1 THEN ybase = ybase + 12.5
                IF bas = 1 THEN y = y + 12.5
                IF bas = 1 THEN xbase = xbase + 12.5
                IF bas = 1 THEN x = x + 12.5
                IF bas = 1 THEN RETURN
         END SELECT
         LINE (xbase, ybase)-(x, y), 8
         RETURN

