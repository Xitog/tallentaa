G = 0
while G<31
print G
G = G + 1
wend
notice "Comptage fini" 'Affiche fen�tre
print "Print" 'Affiche print
if G = 31 then print "G = ";G
WindowWidth = 248 'D�fini largeur
WindowHeight = 175 'D�fini longueur
'nomainwin        'Enl�ve la fen�tre d'execution windows
loadbmp "arrow", "bmp\arrwbttn.bmp"
loadbmp "blue", "bmp\bluebttn.bmp"
bmpbutton #main.button1, "bmp\blank4.bmp", [button1Click], UL, 22, 11
bmpbutton #main.button2, "bmp\blank4.bmp", [button2Click], UL, 22, 46

