SCREEN 7
CLS
'Affichage
FOR ligne = 0 TO 200 STEP 10
LINE (1, ligne)-(300, ligne), 2
NEXT ligne
FOR colonne = 0 TO 300 STEP 10
LINE (colonne, 1)-(colonne, 190), 2
NEXT colonne
'Build
caspos = 1
x = 5
y = 5
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
ON KEY(1) GOSUB allumR
KEY(1) ON
ON KEY(2) GOSUB allumB
KEY(2) ON
ON KEY(3) GOSUB allumV
KEY(3) ON
ON KEY(4) GOSUB allumT
KEY(4) ON
WHILE INKEY$ <> CHR$(esc)
LOCATE 1, 1
PRINT caspos
WEND
CLOSE
END
efface:
        IF E = 0 THEN LINE (x, y)-(x, y), 0
        IF E = 1 THEN LINE (x, y)-(x, y), 4
        IF E = 2 THEN LINE (x, y)-(x, y), 3
        IF E = 3 THEN LINE (x, y)-(x, y), 2
        IF E = 4 THEN LINE (x, y)-(x, y), 6
        IF E <> 0 THEN E = 0
        RETURN

droite:
        GOSUB efface
        x = x + 10
        caspos = caspos + 1
        GOSUB affichage
        RETURN

haut:
        GOSUB efface
        y = y - 10
        caspos = caspos - 10
        GOSUB affichage
        RETURN

bas:
        GOSUB efface
        y = y + 10
        caspos = caspos + 10
        GOSUB affichage
        RETURN

gauche:
        GOSUB efface
        x = x - 10
        caspos = caspos - 1
        GOSUB affichage
        RETURN

affichage:
        LINE (x, y)-(x, y)
        RETURN

allumR:
        LINE (x - 5, y - 5)-(x + 5, y + 5), 4, BF
        'PRINT #1, "line (", x, ",", y, ")-(", x, ",", y, ")"
        E = 1
        RETURN

allumB:
        LINE (x - 5, y - 5)-(x + 5, y + 5), 3, BF
        E = 2
        RETURN

allumV:
        LINE (x - 5, y - 5)-(x + 5, y + 5), 2, BF
        E = 3
        RETURN
allumT:
        LINE (x - 5, y - 5)-(x + 5, y + 5), 6, BF
        E = 4
        RETURN

