
  'bitmap.bas
  'demonstrate the bitmap command for bmpbuttons
  WindowWidth = 248
  WindowHeight = 175
  nomainwin
  'loadbmp "arrow", "bmp\arrwbttn.bmp"
  'loadbmp "blue", "bmp\bluebttn.bmp"
  bmpbutton #main.button1, "bmp\Closedg.bmp", [button1Click], UL, 22, 11
  bmpbutton #main.button2, "bmp\Okdg.bmp", [button2Click], UL, 22, 46
  open "DG buttons" for graphics as #main
  print #main, "fill black; flush" 'change les couleurs ici !

[main.inputLoop]   'wait here for input events
  input aVar$
  goto [main.inputLoop]

[button1Click]   'Perform action for the button named 'button1'
  'print #main.button2, "setfocus"
  'print #main.button2, "bitmap arrow"
  'print #main.button1, "bitmap blue"
  close #main
  end
  goto [main.inputLoop]

[button2Click]   'Perform action for the button named 'button2'
  'print #main.button1, "setfocus"
  'print #main.button1, "bitmap arrow"
  'print #main.button2, "bitmap blue"
  goto [main.inputLoop]

  end
