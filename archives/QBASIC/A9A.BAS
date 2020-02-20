'Moteur 2D ALPHA v9.c bug : limite de réapparition/disparition sur l'écran
'  Ne gère que des images en 256 couleurs ! !
'  Attention, ne pas taper trop vite sur les flèches ! ! Sinon on vous
'  indiquera "x" out of bound vous devrez alors utiliser une fois la souris
'  puis vous pourrez retoucher au clavier. 

  dim ZoneJeu(10, 9)
  ZoneJeu(4, 5) = 1     '(+1,+1) sur la carte réelle

'Ouverture fenêtre bis
    WindowWidth = 100+42   '42 valeur bizarre
    WindowHeight = 320+29  '29 idem
    UpperLeftX = 320+49
    UpperLeftY = 1
    open "Fenêtre perso" for graphics_nsb as #fbis

'Ouverture fenêtre (11 sur 10)
    WindowWidth = 320+42   '42 valeur bizarre
    WindowHeight = 320+29  '29 idem
    UpperLeftX = 1
    UpperLeftY = 1
    open "Appuyer sur les flèches" for graphics_nsb as #graph
    print #graph, "when characterInput [fetch]"
    print #graph, "WHEN leftButtonDown [maouse]"
    nomainwin
    print #graph, "fill blue; flush"

'Coordonnées de base
    xperso = 0
    yperso = 0

'Affichage de base
    loadbmp "Chewie", "bmp\32Man.bmp"
    print #graph, "drawbmp Chewie "; xperso ; " "; yperso ;
    unloadbmp "Chewie"

'Configuration (je ne sais pas)
    print #graph, "setfocus"

'Boucle principale
[mainLoop]
    input r$
goto [mainMoop]
[maouse]
    xcase = xperso / 32
    ycase = yperso / 32
    casejeu = ZoneJeu(xcase,ycase)
    if casejeu = 0 then
        loadbmp "Herbe", "bmp\32Herbe2.bmp"
        print #graph, "drawbmp Herbe "; xperso ; " "; yperso ;
        unloadbmp "Herbe"
    end if
    if casejeu = 1 then
        loadbmp "Roc", "bmp\32Herbe.bmp"
        print #graph, "drawbmp Roc "; xperso ; " "; yperso ;
        unloadbmp "Roc"
    end if
    xfutur = xperso
    yfutur = yperso
    if MouseX > xperso then xfutur = xperso +32
    if MouseX < xperso then xfutur = xperso -32
    if MouseY > yperso then yfutur = yperso +32
    if MouseY < yperso then yfutur = yperso -32
    if xperso > 320+42 then xperso = 0   '42 valeur bizarre
    if yperso > 320+29 then yperso = 0   '29 idem
    xperso = xfutur
    yperso = yfutur
    if xperso < 0 then xperso = 362 - 32
    if yperso < 0 then yperso = 349 - 32
    loadbmp "Chewie", "bmp\32Man.bmp"
    print #graph, "drawbmp Chewie "; xperso ; " "; yperso ;
    unloadbmp "Chewie"
goto [mainLoop]

[fetch]
    xcase = xperso / 32
    ycase = yperso / 32
    casejeu = ZoneJeu(xcase,ycase)
    if casejeu = 0 then
        loadbmp "Herbe", "bmp\32Herbe2.bmp"
        print #graph, "drawbmp Herbe "; xperso ; " "; yperso ;
        unloadbmp "Herbe"
    end if
    if casejeu = 1 then
        loadbmp "Roc", "bmp\32Herbe.bmp"
        print #graph, "drawbmp Roc "; xperso ; " "; yperso ;
        unloadbmp "Roc"
    end if

    key$ = Inkey$
        keyValue = asc(right$(key$, 1))
        if keyValue = _VK_RIGHT then xperso = xperso + 32 'notice "Flèche Droite"
        if keyValue = _VK_LEFT  then xperso = xperso - 32 'notice "Flèche Gauche"
        if keyValue = _VK_DOWN then  yperso = yperso + 32 'notice "Flèche bas"
        if keyValue = _VK_UP then    yperso = yperso - 32 'notice "Flèche haut"
        if keyValue = _VK_F1 then goto [quit]
    if xperso > 320+42 then xperso = 0   '42 valeur bizarre
    if yperso > 320+29 then yperso = 0   '29 idem
    if xperso < 0 then xperso = 362 - 32
    if yperso < 0 then yperso = 349 - 32
    loadbmp "Chewie", "bmp\32Man.bmp"
    print #graph, "drawbmp Chewie "; xperso ; " "; yperso ;
    unloadbmp "Chewie"
goto [mainLoop]

[quit]
    close #graph
    close #fbis
    end
