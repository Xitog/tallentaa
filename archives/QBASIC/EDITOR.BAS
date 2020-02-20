PRINT "1.Nouveau fichier   2.Ouvrir"
INPUT "Votre choix"; choix
SELECT CASE choix
CASE IS = 2
        INPUT "R‚pertoire  ex: C:\Temp"; rep$
        CHDIR rep$
        FILES
END SELECT
INPUT "Nom du fichier (suivis de .bas): "; n$
IF choix = 1 THEN OPEN n$ FOR OUTPUT AS #1
SELECT CASE choix
CASE IS = 1
        PRINT #1, "CLS"
        PRINT #1, "screen 7"
        PRINT #1, "x = 160"
        PRINT #1, "y = 100"
        PRINT #1, "LINE (x, y)-(x, y)"
        PRINT #1, "GOSUB affiche"
        PRINT #1, "CONST esc = 27"
        PRINT #1, "ON KEY(13) GOSUB droite"
        PRINT #1, "KEY(13) ON"
        PRINT #1, "ON KEY(11) GOSUB haut"
        PRINT #1, "KEY(11) ON"
        PRINT #1, "ON KEY(14) GOSUB bas"
        PRINT #1, "KEY(14) ON"
        PRINT #1, "ON KEY(12) GOSUB gauche"
        PRINT #1, "KEY(12) ON"
        PRINT #1, "WHILE INKEY$ <> CHR$(esc)"
        PRINT #1, "WEND"
        PRINT #1, "END"
        PRINT #1, " droite:"
        PRINT #1, " droite = 1"
        PRINT #1, " GOSUB desaffiche"
        PRINT #1, " GOSUB affiche"
        PRINT #1, " RETURN"
        PRINT #1, " "
        PRINT #1, " haut:"
        PRINT #1, " haut = 1"
        PRINT #1, " GOSUB desaffiche"
        PRINT #1, " GOSUB affiche"
        PRINT #1, " RETURN"
        PRINT #1, " "
        PRINT #1, " bas:"
        PRINT #1, " bas = 1"
        PRINT #1, " GOSUB desaffiche"
        PRINT #1, " GOSUB affiche"
        PRINT #1, " RETURN"
        PRINT #1, " "
        PRINT #1, " gauche:"
        PRINT #1, " gauche = 1"
        PRINT #1, " GOSUB desaffiche"
        PRINT #1, " GOSUB affiche"
        PRINT #1, " RETURN"
        PRINT #1, " "
        PRINT #1, "desaffiche:"
        PRINT #1, "CLS"
        PRINT #1, "RETURN"
        PRINT #1, ""
        PRINT #1, "affiche:"
        PRINT #1, "IF droite = 1 THEN xx = xx + 1"
        PRINT #1, "IF droite = 1 THEN droite = 0"
        PRINT #1, "IF haut = 1 THEN yy = yy - 1"
        PRINT #1, "IF haut = 1 THEN haut = 0"
        PRINT #1, "IF bas = 1 THEN yy = yy + 1"
        PRINT #1, "IF bas = 1 THEN bas = 0"
        PRINT #1, "IF gauche = 1 THEN xx = xx - 1"
        PRINT #1, "IF gauche = 1 THEN gauche = 0"
        PRINT #1, "LINE (x, y)-(x, y)"
END SELECT
IF choix = 2 THEN OPEN n$ FOR APPEND AS #1
SCREEN 7
X1Y1 = 0
x = 1
y = 1
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
ON KEY(1) GOSUB X1Y1
KEY(1) ON
ON KEY(2) GOSUB X2Y2
KEY(2) ON
WHILE INKEY$ <> CHR$(esc)
IF X1Y1 = 1 THEN LINE (x1, y1)-(x, y)
WEND
        PRINT #1, "RETURN"
        PRINT #1, ""
CLOSE
END
desaffiche:
        IF X2Y2 = 0 THEN LINE (x, y)-(x, y), 0
        IF X2Y2 = 1 THEN X2Y2 = 0
        IF X1Y1 = 1 THEN LINE (x1, y1)-(x, y), 0
        RETURN

affiche:
        IF droite = 1 THEN x = x + 1
        IF droite = 1 THEN droite = 0
        IF haut = 1 THEN y = y - 1
        IF haut = 1 THEN haut = 0
        IF bas = 1 THEN y = y + 1
        IF bas = 1 THEN bas = 0
        IF gauche = 1 THEN x = x - 1
        IF gauche = 1 THEN gauche = 0
        LINE (x, y)-(x, y)
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

X1Y1:
        x1 = x
        y1 = y
        X1Y1 = 1
        RETURN

X2Y2:
        x2 = x
        y2 = y
        X1Y1 = 0
        X2Y2 = 1
        'PRINT #1, "line (", x1, ",", y1, ")-(", x2, ",", y2, ")"
        xx = 160
        yy = 100
        bonusx1 = 160 - x1
        bonusx2 = 160 - x2
        bonusy1 = 100 - y1
        bonusy2 = 100 - y2
        PRINT #1, "LINE (xx +", bonusx1, ", yy + ", bonusy1, ")-(xx + ", bonusx2, ", yy + ", bonusy2, ")"
        RETURN




