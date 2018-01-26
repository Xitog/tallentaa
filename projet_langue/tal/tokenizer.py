import re

texte = "Ainsi, à longueur de semaine, les prisonniers de la peste se débattirent comme ils le purent. Et quelques-uns d’entre eux, comme Rambert, arrivaient même à imaginer, on le voit, qu’ils agissaient encore en hommes libres, qu’ils pouvaient encore choisir. Mais, en fait, on pouvait dire à ce moment, au milieu du mois d’août, que la peste avait tout recouvert. Il n’y avait plus alors de destins individuels, mais une histoire collective qui était la peste et des sentiments partagés par tous. Le plus grand était la séparation et l’exil, avec ce que cela comportait de peur et de révolte. Voilà pourquoi le narrateur croit qu’il convient, à ce sommet de la chaleur et de la maladie, de décrire la situation générale et, à titre d’exemple, les violences de nos concitoyens vivants, les enterrements des défunts et la souffrance des amants séparés."
print("----------------")
print("Texte")
print("----------------")
print(texte)

tokenize = re.split('[^\w]', texte) # \'-’

# remove empty elements
tokenize = [tok for tok in tokenize if tok != '']

print("----------------")
print("Liste des tokens")
print("----------------")
print(tokenize)

liste_sorted_by_lexico = sorted(tokenize)
liste_sorted_by_length = sorted(liste_sorted_by_lexico, key=len)

print("----------------")
print("Liste classée")
print("----------------")
print(liste_sorted_by_length)


