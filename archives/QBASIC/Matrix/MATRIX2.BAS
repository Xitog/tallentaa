CLS
PRINT "------------------------------------------------------------------------------"
PRINT "MAP EDITOR 2D BY DAMIEN GOUTEUX"
PRINT "USE CTRL FOR HELP"
PRINT "FOR EVERY MATRIX-GAME 2D OR 3D"
PRINT "------------------------------------------------------------------------------"
INPUT "X= (max 10)"; xmap
INPUT "Y= (max 10)"; ymap
INPUT "R‚solutin (7 ou 9) "; R
CLS
REDIM newboard(1 TO xmap, 1 TO ymap)
SCREEN R
d = 0
FOR a = 1 TO xmap STEP 1
c = 0
FOR b = 1 TO ymap STEP 1
LINE (d, c)-(d + 8, c + 8), , B
c = c + 8
NEXT b
d = d + 8
NEXT a
CONST esc = 27
xgraph = 4
ygraph = 4
xtab = 1
ytab = 1
PRESET (xgraph, ygraph), 4
ON KEY(13) GOSUB droite
KEY(13) ON
ON KEY(11) GOSUB haut
KEY(11) ON
ON KEY(14) GOSUB bas
KEY(14) ON
ON KEY(12) GOSUB gauche
KEY(12) ON
ON KEY(1) GOSUB Tex1
KEY(1) ON
ON KEY(2) GOSUB Tex2
KEY(2) ON
ON KEY(3) GOSUB Tex3
KEY(3) ON
ON KEY(4) GOSUB Tex4
KEY(4) ON
ON KEY(10) GOSUB Enregistre
KEY(10) ON
WHILE INKEY$ <> CHR$(esc)
LOCATE 1, 12
PRINT xtab; "/"; xmap
LOCATE 2, 12
PRINT ytab; "/"; ymap
LOCATE 3, 12
PRINT "Pav‚ num‚rique pour bouger"
LOCATE 4, 12
PRINT "F1,F2,F3 pour remplir"
LOCATE 5, 12
PRINT "Echap pour quitter"
WEND
ERASE newboard
END
droite:
        IF xgraph = xmap * 8 - 4 THEN RETURN
        GOSUB desaffiche
        xgraph = xgraph + 8
        xtab = xtab + 1
        PRESET (xgraph, ygraph), 4
        RETURN
haut:
        IF ygraph = 4 THEN RETURN
        GOSUB desaffiche
        ygraph = ygraph - 8
        ytab = ytab - 1
        PRESET (xgraph, ygraph), 4
        RETURN
bas:
        IF ygraph = ymap * 8 - 4 THEN RETURN
        GOSUB desaffiche
        ygraph = ygraph + 8
        ytab = ytab + 1
        PRESET (xgraph, ygraph), 4
        RETURN

gauche:
        IF xgraph = 4 THEN RETURN
        GOSUB desaffiche
        xgraph = xgraph - 8
        xtab = xtab - 1
        PRESET (xgraph, ygraph), 4
        RETURN

desaffiche:
        'PRESET (xgraph, ygraph), 0
        IF newborad(xtab, ytab) = 0 THEN PRESET (xgraph, ygraph), 0
        IF newboard(xtab, ytab) = 6 THEN PRESET (xgraph, ygraph), 6
        IF newboard(xtab, ytab) = 4 THEN PRESET (xgraph, ygraph), 4
        IF newboard(xtab, ytab) = 2 THEN PRESET (xgraph, ygraph), 2
        IF newboard(xtab, ytab) = 1 THEN PRESET (xgraph, ygraph), 1
        RETURN

Tex1:
        LINE (xgraph - 3, ygraph - 3)-(xgraph + 3, ygraph + 3), 6, BF
        newboard(xtab, ytab) = 6
        RETURN

Tex2:
        LINE (xgraph - 3, ygraph - 3)-(xgraph + 3, ygraph + 3), 4, BF
        newboard(xtab, ytab) = 4
        RETURN

Tex3:
        LINE (xgraph - 3, ygraph - 3)-(xgraph + 3, ygraph + 3), 2, BF
        newboard(xtab, ytab) = 2
        RETURN

Tex4:
        LINE (xgraph - 3, ygraph - 3)-(xgraph + 3, ygraph + 3), 1, BF
        newboard(xtab, ytab) = 1
        RETURN

Enregistre:
        LOCATE 6, 12
        PRINT "Nom fichier (8 lettres max): "
        LOCATE 7, 12
        INPUT ; n$
        LOCATE 7, 12
        PRINT "Niveau sauv‚e..."
        OPEN n$ FOR OUTPUT AS #1
        PRINT #1, "REDIM niveau( 1 TO", xmap, ",(1TO", ymap, ")"
        FOR a = 1 TO xmap
        FOR b = 1 TO ymap
        PRINT #1, "niveau(", a, ",", b, ") = ", newboard(a, b)
        NEXT b
        NEXT a
        LOCATE 7, 12
        PRINT "                 "
        RETURN

