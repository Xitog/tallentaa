#require 'rubygems'

puts "Version 1.04"
name = gets

#
# Organisation
#
#module Tutorial
#  def Tutorial.pipo
#    puts "Cette méthode c du P.I.P.O."
#  end
#end
# Appel
#require "Tutorial"
#Tutorial.pipo

#
# Variables
#
# Affectation
a = 5+1
puts a.class # type deprecated
puts a.object_id # id ''
b = "azerty"
# Tableau
puts "Tableaux : "
tab = [ 1, 2, 3, 4, 5]
puts tab
puts "Eliminé : " # en Python : tab.remove(element)
puts tab-[2,4]
# Range
puts "Range inclusif : "
puts (1..4).to_s
puts "Range exclusif : "
puts 1...4
# Hashes (clé/value)
puts "Hashes :"
g = { "red" => 1, "green" => 2, "blue" => 3}
puts g["red"]
# Définie ou pas
o = 5
puts defined? o # écrit : local-variable

#
# Basic I/O
#
# Ecriture sur la sortie standard
puts "Bonjour"    # puts saute une ligne après
puts "Rebonjour"
print "Alpha"     # pas print
print "Beta\n"
$stdout << "Bonjour monde" << "\n"  # à la C++
# Lecture sur l'entrée standard
print "Entrer votre nom : "
name = gets
puts name

#
# Contrôle des flux
#
# Séquencement : pas besoin de ';' comme Python ;-)
# Sélection
puts "if"
if a == 5
  puts "a est égal à 5"
else
  puts "a est égal à "+a.to_s
end
puts "Unless (if inversé ) :"
unless a == 5
  puts "a est égal à "+a.to_s
else
  puts "a est égal à 5"
end
# Itération
puts "For :"
for i in 0..5
  puts i
end
puts i  # Attention i est toujours défini !
puts "While :"
o = 7
while o>1
  puts o
  o-=1
end
puts "Do :"
5.times do |i|
  puts i
end

#
# Function
#
# Déclaration & Définition
def blob(a, b)
  puts a+b
end
# Appel
blob(2,8) # pas d'espace avant '(' sinon warning

#
# Classe
#
# Déclaration & Définition
class A
  @@a = 22
  def initialize(a)
    @a = a
    puts "a = " + @a.to_s
  end
  def print()
    puts @a
  end
  def static_print()
    puts "Affichage d'une variable statique @@a : " + @@a.to_s
  end
  def A.static_print()
    puts "Statique methode @@a : " + @@a.to_s
  end
  private 
  def aprivate()
    puts "never"
  end
end

class B < A
  def initialize(b)
    super(b+10)
    @b = b
    puts "b = " + @b.to_s
  end
end

a = A.new(11)
a.print()
a.static_print()
puts a.inspect     # très utile pour "visualiser" un objet
puts A.inspect
A.static_print()
#a.aprivate()
b = B.new(5)


