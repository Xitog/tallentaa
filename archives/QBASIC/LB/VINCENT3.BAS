
    WindowWidth = 1024
    WindowHeight = 768

    nomainwin


    open "Master" for graphics as #main
    print #main, "fill black; flush"
    loadbmp "bandeau", "bmp\blank4.bmp"
    print #main, "bandeau"
    print #main, "drawbmp "; "bandeau"; " 0 0"

[main.inputLoop]   'wait here for input event
    'input aVar$
    scan
    print #main, "WHEN leftButtonDown [message]"
    goto [main.inputLoop]

[bandeau]

[message]
    NOTICE "Positionnement : "+chr$(13)+"votre souris est à : "; MouseX;" et à "; MouseY
    close #main
    end



