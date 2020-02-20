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
IF choix = 1 THEN PRINT #1, "screen 7"
IF choix = 2 THEN OPEN n$ FOR APPEND AS #1
SCREEN 7
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
KEY 15, CHR$(&H4) + CHR$(&H1F)          'Etablit Ctrl+S comme KEY 15.
ON KEY(15) GOSUB Enregistre
KEY(15) ON
WHILE INKEY$ <> CHR$(esc)
WEND
CLOSE
END
droite:
        IF E = 0 THEN LINE (x, y)-(x, y), 0
        IF E = 1 THEN E = 0
        x = x + 1
        GOSUB affichage
        RETURN

haut:
        IF E = 0 THEN LINE (x, y)-(x, y), 0
        IF E = 1 THEN E = 0
        y = y - 1
        GOSUB affichage
        RETURN

bas:
        IF E = 0 THEN LINE (x, y)-(x, y), 0
        IF E = 1 THEN E = 0
        y = y + 1
        GOSUB affichage
        RETURN

gauche:
        IF E = 0 THEN LINE (x, y)-(x, y), 0
        IF E = 1 THEN E = 0
        x = x - 1
        GOSUB affichage
        RETURN

affichage:
        LINE (x, y)-(x, y)
        RETURN

Enregistre:
        PRINT #1, "line (", x, ",", y, ")-(", x, ",", y, ")"
        E = 1
        RETURN

