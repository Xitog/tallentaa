CLS
SCREEN 7
secteur = 1
secteur:
SELECT CASE secteur
CASE IS = 1
   xmax = 26
   xmin = 1
   ymax = 29
   ymin = 1
      s = 4
END SELECT
LINE (xmin, ymin)-(xmax, ymax), , B
IF s = 4 THEN LINE (xmax, ymax - 1)-(xmax, ymin + 1), 5
IF s = 2 THEN LINE (xmin, ymax - 1)-(xmin, ymin + 1), 5
IF s = 1 THEN LINE (xmax - 1, ymin)-(xmin + 1, ymin), 5
IF s = 3 THEN LINE (xmax - 1, ymax)-(xmin + 1, ymax), 5
x = 5
y = 10
LINE (x, y)-(x, y)
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
WEND
END
droite:
 droite = 1
 GOSUB desaffiche
 GOSUB affiche
 RETURN
 
haut:
 haut = 1
 GOSUB desaffiche
 GOSUB affiche
 RETURN
 
bas:
 bas = 1
 GOSUB desaffiche
 GOSUB affiche
 RETURN
 
gauche:
 gauche = 1
 GOSUB desaffiche
 GOSUB affiche
 RETURN
 
desaffiche:
LINE (x, y)-(x, y), 0
RETURN

affiche:     
        v = x
        w = y
        IF droite = 1 THEN v = x + 1
        IF droite = 1 THEN droite = 0
        IF haut = 1 THEN w = y - 1
        IF haut = 1 THEN haut = 0
        IF bas = 1 THEN w = y + 1
        IF bas = 1 THEN bas = 0
        IF gauche = 1 THEN v = x - 1
        IF gauche = 1 THEN gauche = 0
        IF s = 4 AND v = xmax THEN
        x = v
        GOSUB recherchesec
        END IF
        IF s = 1 AND w = ymin THEN
        y = w
        GOSUB recherchesec
        END IF
        IF s = 2 AND v = xmin THEN
        x = v
        GOSUB recherchesec
        END IF
        IF s = 3 AND w = ymax THEN
        y = w
        GOSUB recherchesec
        END IF
        IF v = xmin OR v = xmax THEN v = x
        IF w = ymin OR w = ymax THEN w = y
        x = v
        y = w
        LINE (x, y)-(x, y)
        RETURN
recherchesec:
       secteur = secteur + 1
SELECT CASE secteur
        CASE IS = 1
                xmax = 26
                xmin = 1
                ymax = 29
                ymin = 1
                s = 4
        END SELECT
        LINE (xmin, ymin)-(xmax, ymax), , B
        IF s = 4 THEN LINE (xmax, ymax - 1)-(xmax, ymin + 1), 5
        IF s = 2 THEN LINE (xmin, ymax - 1)-(xmin, ymin + 1), 5
        IF s = 1 THEN LINE (xmax - 1, ymin)-(xmin + 1, ymin), 5
        IF s = 3 THEN LINE (xmax - 1, ymax)-(xmin + 1, ymax), 5
        RETURN

