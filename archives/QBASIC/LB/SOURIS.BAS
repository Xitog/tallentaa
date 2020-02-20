
    WindowWidth = 1024
    WindowHeight = 768

    nomainwin

    open "untitled" for graphics as #main
    print #main, "fill black; flush"


[main.inputLoop]   'wait here for input event
    'input aVar$
    scan
    print #main, "WHEN leftButtonDown [action]"
    goto [main.inputLoop]

[action]
    'IF
    NOTICE "Positionnement : "+chr$(13)+"votre souris est à : "; MouseX;" et à "; MouseY
    close #main
    end



