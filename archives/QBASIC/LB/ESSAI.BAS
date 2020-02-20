
    WindowWidth = 550
    WindowHeight = 410

    nomainwin

    textbox #main.box1, 26, 16, 100, 25
    button #main.button2, "Nouveau", [button2Click], UL, 462, 276, 66, 25
    button #main.button3, "Quitter", [button3Click], UL, 462, 316, 66, 25
    bmpbutton #main.bmpbutton4, "C:\LB142W\VWSIGNON.BMP", [bmpbutton4Click], UL, 26, 16
    texteditor #main.textedit5, 414, 391, 100, 100
    texteditor #main.textedit6, 294, 451, 100, 100
    statictext #main.statictext7, "Maker Perso", 438, 16, 88, 20
    graphicbox #main.graph, 110, 441, 100, 100
    texteditor #main.textedit9, 22, 176, 100, 100
    textbox #main.textbox10, -42, 416, 100, 25
    open "untitled" for graphics as #main
    print #main.graph, "fill palegray; flush"
    print #main, "fill white; flush"

