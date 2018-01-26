#-----------------
# Avec des objets
#-----------------

class A:

    def __init__(self, val):
        self.val = val

    def __lt__(self, other):
        return self.val < other.val

    def __str__(self):
        return str(id(self)) + ' : ' + str(self.val)

    def __repr__(self):
        return str(self)

liste1 = [A(10), A(5)]
liste2 = sorted(liste1)

print(liste1) # ex : [7105872 : 10, 51949968 : 5]
print(liste2) # ex : [51949968 : 5, 7105872 : 10] elle est triée mais même id

liste2[0].val = 22

print(liste1) # ex : [7105872 : 10, 51949968 : 22]
print(liste2) # ex : [51949968 : 22, 7105872 : 10] les deux éléments ont été modifiés

#------------------
# Avec des chaînes
#------------------

liste1 = ["def", "abc"]
liste2 = sorted(liste1)

print(liste1)
print(liste2)

[print(i, id(i)) for i in liste1]
[print(i, id(i)) for i in liste2]

# liste 1 :
#   def 4199680 <= même id
#   abc 5729888
# liste 2 :
#   abc 5729888
#   def 4199680 <= même id
