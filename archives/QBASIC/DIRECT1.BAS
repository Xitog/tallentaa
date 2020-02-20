CLS
x = 10
y = 2
LOCATE y, x
PRINT "x"
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
        CLS
        x = x + 1
        LOCATE y, x
        PRINT "x"
        RETURN
haut:
        CLS
        y = y - 1
        LOCATE y, x
        PRINT "x"
        RETURN
bas:
        CLS
        y = y + 1
        LOCATE y, x
        PRINT "x"
        RETURN

gauche:
        CLS
        x = x - 1
        LOCATE y, x
        PRINT "x"
        RETURN


