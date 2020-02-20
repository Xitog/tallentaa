cls
notice "Make with Liberty Basic, Enjoy!"
v = 1.0
titlebar "Maker Perso v";v
[mainLoop]
level = 1
input "Prénom  : ";p$
input "Nom     : ";n$
input "Surnom  : ";s$
print "Classe (mage [1], guerrier [2], voleur [3], multiclasse [4])"
input "Choix   : ";choix
if choix = 4 then print "MultiClasse (paladin [5])"
if choix = 4 then input "Choix   : ";choix
open "perso.sav" for output as #1
print #1,p$
print #1,n$
print #1,s$
print #1,choix
print #1,level
close #1
cls
open "perso.sav" for input as #1
input #1,p$
print "Prénom enregistré <";p$;">"
input #1,n$
print "Nom enregistré    <";n$;">"
input #1,s$
print "Surnom enregistré <";s$;">"
input #1,choix
input #1,level
if choix = 1 then print "Mage <LVL:";level;">"
if choix = 2 then print "Guerrier <LVL:";level;">"
if choix = 3 then print "Voleur <LVL:";level;">"
if choix = 5 then print "Paladin <LVL:";level;">"
close #1
[quit]

  ' bring up a confirmation box to be sure that
  ' the user wants to quit
  confirm "Are you sure you want to QUIT?"; answer$
  if answer$ = "no" then [mainLoop]
end
  'confirm "Press y and I wish that Satan coming to you"

