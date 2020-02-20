SCREEN 0
PRINT "Bienvenu … PONG SOLO"
PRINT "V‚rifier que num lock est d‚sacitiv‚"
PRINT "Utiliser les flŠches du pav‚ num‚rique"
FOR d = 1 TO 45000
NEXT d
CLS
SCREEN 7
PRINT "PONG SOLO BY DG"
LINE (60, 40)-(260, 150), , B
dgg = 1
aller = 1
x1 = 61
x2 = 76
v1 = 244
v2 = 259
bx = 160
by = 95
LINE (x1, 148)-(x2, 148)
LINE (x1, 147)-(x2, 147)
'LINE (v1, 42)-(v2, 42)
'LINE (v1, 43)-(v2, 43)
LINE (bx, by)-(bx - 1, by - 1), , B
CONST esc = 27
ON KEY(13) GOSUB droite
KEY(13) ON
ON KEY(12) GOSUB gauche
KEY(12) ON
WHILE INKEY$ <> CHR$(esc)
points = points + 1
LINE (bx, by)-(bx - 1, by - 1), , B
FOR t = 1 TO 300
NEXT t
LINE (bx, by)-(bx - 1, by - 1), 0, B
IF dgg = 1 THEN bx = bx - 1
IF dgd = 1 THEN bx = bx + 1
IF aller = 1 THEN by = by - 1
IF retour = 1 THEN by = by + 1
IF bx = 62 THEN dgg = 0
IF bx = 62 THEN dgd = 1
IF bx = 258 THEN dgd = 0
IF bx = 258 THEN dgg = 1
IF by = 42 THEN aller = 0
IF by = 42 THEN retour = 1
IF by = 147 AND bx >= x1 AND bx <= x2 THEN retour = 0
IF by = 147 AND bx >= x1 AND bx <= x2 THEN aller = 1
IF by = 149 THEN GOSUB fin
WEND
END
droite:
        IF x2 = 259 THEN RETURN
        LINE (x1, 148)-(x2, 148), 0
        LINE (x1, 147)-(x2, 147), 0
        x1 = x1 + 1
        x2 = x2 + 1
        LINE (x1, 148)-(x2, 148)
        LINE (x1, 147)-(x2, 147)
        RETURN
gauche:
        IF x1 = 61 THEN RETURN
        LINE (x1, 148)-(x2, 148), 0
        LINE (x1, 147)-(x2, 147), 0
        x1 = x1 - 1
        x2 = x2 - 1
        LINE (x1, 148)-(x2, 148)
        LINE (x1, 147)-(x2, 147)
        RETURN
fin:
        CLS
        PRINT "Game Over"
        PRINT points

