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
        PRINT #1, "secteur = 1"
        PRINT #1, "Secteur:"
        PRINT #1, "SELECT CASE SECTEUR"
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
IF X1Y1 = 1 THEN LINE (x1, y1)-(x, y), , B
WEND
        PRINT #1, "END SELECT"
        PRINT #1, ""
CLOSE
END
desaffiche:
        SELECT CASE X1Y1
        CASE IS = 1
        IF x < x1 THEN xds = x1 - 1
        IF x > x1 THEN xds = x1 + 1
        IF y > y1 THEN yds = y1 + 1
        IF y < y1 THEN yds = y1 - 1
        LINE (x, y)-(xds, yds), 0, B
        END SELECT

        IF X2Y2 = 0 AND X1Y1 = 0 THEN LINE (x, y)-(x, y), 0
        IF X2Y2 = 1 THEN X2Y2 = 0
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
        IF x1 < x2 THEN
        xmax = x2
        xmin = x1
        END IF
        IF x1 > x2 THEN
        xmax = x1
        xmin = x2
        END IF
        IF y1 < y2 THEN
        ymax = y2
        ymin = y1
        END IF
        IF y1 > y2 THEN
        ymax = y1
        ymin = y2
        END IF
        secteur = secteur + 1
        PRINT #1, "CASE IS =", secteur
        PRINT #1, "   xmax =", xmax
        PRINT #1, "   xmin =", xmin
        PRINT #1, "   ymax =", ymax
        PRINT #1, "   ymin =", ymin
        LINE (x1, y1)-(x2, y2), , BF
        RETURN

