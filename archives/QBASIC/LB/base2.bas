       'ittyclok

    titlebar "Maker Perso v1.0" 'Modifie la barre de titre
[main]                          'Etiquette    
    scan                        'Attend un touche
    goto [main]                 'Va à main

[loop]
    if time$ <> time$() then
        time$ = time$()
        titlebar time$
    end if
    scan
    goto [loop]
