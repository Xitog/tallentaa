INPUT v
INPUT w
CLS
SCREEN 7
x = 0
y = 0
LINE (113 + x, 85 + y)-(113 + x, 85 + y)
LINE (114 + x, 84 + y)-(114 + x, 84 + y)
LINE (115 + x, 83 + y)-(115 + x, 83 + y)
LINE (116 + x, 82 + y)-(116 + x, 82 + y)
LINE (117 + x, 81 + y)-(117 + x, 81 + y)
LINE (118 + x, 82 + y)-(118 + x, 82 + y)
LINE (119 + x, 83 + y)-(119 + x, 83 + y)
LINE (120 + x, 84 + y)-(120 + x, 84 + y)
LINE (121 + x, 85 + y)-(121 + x, 85 + y)
LINE (122 + x, 85 + y)-(122 + x, 85 + y)
LINE (123 + x, 84 + y)-(123 + x, 84 + y)
LINE (124 + x, 83 + y)-(124 + x, 83 + y)
LINE (125 + x, 84 + y)-(125 + x, 84 + y)
LINE (126 + x, 85 + y)-(126 + x, 85 + y)
LINE (126 + x, 86 + y)-(126 + x, 86 + y)
LINE (126 + x, 87 + y)-(126 + x, 87 + y)
LINE (125 + x, 88 + y)-(125 + x, 88 + y)
LINE (124 + x, 87 + y)-(124 + x, 87 + y)
LINE (123 + x, 87 + y)-(123 + x, 87 + y)
LINE (122 + x, 87 + y)-(122 + x, 87 + y)
LINE (121 + x, 87 + y)-(121 + x, 87 + y)
LINE (120 + x, 88 + y)-(120 + x, 88 + y)
LINE (119 + x, 89 + y)-(119 + x, 89 + y)
LINE (118 + x, 89 + y)-(118 + x, 89 + y)
LINE (117 + x, 89 + y)-(117 + x, 89 + y)
LINE (116 + x, 89 + y)-(116 + x, 89 + y)
LINE (113 + x, 87 + y)-(113 + x, 87 + y)
LINE (112 + x, 87 + y)-(112 + x, 87 + y)
LINE (111 + x, 87 + y)-(111 + x, 87 + y)
LINE (112 + x, 85 + y)-(112 + x, 85 + y)
LINE (111 + x, 84 + y)-(111 + x, 84 + y)
LINE (110 + x, 83 + y)-(110 + x, 83 + y)
LINE (109 + x, 84 + y)-(109 + x, 84 + y)
LINE (108 + x, 85 + y)-(108 + x, 85 + y)
LINE (108 + x, 86 + y)-(108 + x, 86 + y)
LINE (108 + x, 87 + y)-(108 + x, 87 + y)
LINE (109 + x, 88 + y)-(109 + x, 88 + y)
LINE (110 + x, 87 + y)-(110 + x, 87 + y)
LINE (111 + x, 87 + y)-(111 + x, 87 + y)
LINE (112 + x, 87 + y)-(112 + x, 87 + y)
LINE (113 + x, 87 + y)-(113 + x, 87 + y)
LINE (114 + x, 88 + y)-(114 + x, 88 + y)
LINE (115 + x, 89 + y)-(115 + x, 89 + y)
'Ce rectangle d‚limite le vaisseau
'LINE (126 + x + 1, 89 + y + 1)-(108 + x - 1, y + 81 - 1), , B
DIM avion(1 TO 100)
GET (126 + x + 1, 89 + y + 1)-(108 + x - 1, 81 + y - 1), avion
CONST esc = 27
ON KEY(13) GOSUB droite
KEY(13) ON
ON KEY(11) GOSUB haut
KEY(11) ON
ON KEY(14) GOSUB bas
KEY(14) ON
ON KEY(12) GOSUB gauche
KEY(12) ON
KEY 15, CHR$(&H4) + CHR$(&H1F)          'Etablit Ctrl+S comme KEY 15.
ON KEY(15) GOSUB Enregistre
KEY(15) ON
WHILE INKEY$ <> CHR$(esc)
WEND
CLOSE
END
desaffiche:
        PUT (108 + x - 1, 81 + y - 1), avion, XOR
        RETURN

affiche:
        IF droite = 1 THEN x = x + v
        IF droite = 1 THEN droite = 0
        IF haut = 1 THEN y = y - w
        IF haut = 1 THEN haut = 0
        IF bas = 1 THEN y = y + w
        IF bas = 1 THEN bas = 0
        IF gauche = 1 THEN x = x - v
        IF gauche = 1 THEN gauche = 0
        PUT (108 + x - 1, 81 + y - 1), avion, XOR
        RETURN

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

Enregistre:
        PRINT #1, "line (", x, ",", y, ")-(", x, ",", y, ")"
        E = 1
        RETURN


