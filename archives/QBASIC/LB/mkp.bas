NOMAINWIN
MENU #1, &Nouveau, &Personnage, [P1], &Armes, [AR1]
MENU #1, &Charger, &Personnage, [P2], &Armes, [AR2]
MENU #1, &Informations, &Info, [APD], &LibertyBasic, [LB]
MENU #1, &Quitter,&Quitter, [Quitter]
WindowWidth = 400
WindowHeight = 400
OPEN "Maker Perso v1.0" for graphics_nsb as #1

rondcoul$="black"
carrecoul$="black"

[bis]
INPUT r$
GOTO [bis]

[P1]
  print #1,"print G"
  goto [bis]
[Rond]
  PRINT #1, "cls"
  PRINT #1, "up"
  PRINT #1, "color "; rondcoul$
  PRINT #1, "goto 200 200"
  PRINT #1, "down"
  PRINT #1, "circle 100"
  PRINT #1, "flush"
  goto [bis]

[Carre]
  PRINT #1, "cls"
  PRINT #1, "up"
  PRINT #1, "color "; carrecoul$
  PRINT #1, "goto 100 100"
  PRINT #1, "down"
  PRINT #1, "box 300 300"
  PRINT #1, "flush"
goto [bis]

[RondRouge]
  rondcoul$="red"
  goto [bis]

[RondBleu]
  rondcoul$="blue"
  goto [bis]

[CarreRouge]
  carrecoul$="red"
  goto [bis]

[CarreBleu]
  carrecoul$="blue"
  goto [bis]

[Quitter]
  CLOSE #1
  END
















