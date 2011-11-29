
BEGIN {
  puts 'Debut'
}

END { # s'exécute même si y'a des erreurs, traitement des erreurs (affichage par défaut) après
  puts 'Fin'
}

puts 'Hello World'

# Variable prédéfini
puts 'fichier : '+$FILENAME
puts 'fichier courant : '+__FILE__
puts 'SAFE : '+$SAFE.to_s # ne peut être réduite, seulement augmentée

# type de variable
# globale
$globo = 2
# normal
globo = 3
# D'instance : @var
# De classe : @@var

# type de base
my_array = [1,2,3]
my_dict = { 1 => 'pipo', 2 => 'cat'}

# Bloc
begin
  puts 'Hello Block'
end

# Itération
a = 5
while a > 0
  print a.to_s+','
  a-=1
end
puts

until a == 5
  print a.to_s+','
  a+=1
end
puts

a+=1 while a > 7
begin
  a+=1
  print a.to_s+','
end while a > 10
puts

for a in 1..4 # 4 inclus
  print a.to_s+','
end
puts

for a in 1...4 # 4 non inclus
  print a.to_s+','
end
puts

[1,2].each { |i|
  puts 'Holà : '+i.to_s
}

a = 0

# break, redo, next & retry peuvent aussi foutre la merde dans les boucles !

# Sélection
if a == 0
  puts 'a == '+0.to_s
elsif a == 1
  puts 'a == 1'
else
  puts 'a == '+a.to_s
end

unless a!= 0
  puts 'a == 0'
else
  puts 'a != 0'
end

puts 'Pipo' if a == 0

b = "pipo"
case b
  when "pipo"
    puts 'pipo'
  when "zorba"
    puts 'zorba'
  else
    puts 'default'
end

# Définition d'une classe et de méthode et d'accesseur
class Pipo
  attr_reader :var
  
  def Pipo.static_hello
    puts 'Hello Static'
    @@stat_var = 3
  end
  
  def instance_hello
    puts 'Hello Instance'
    @var = 5
  end
  
  def self.stat_var # Attention : self réfère à Pipo
    @@stat_var # Le dernier statement est automatiquement retourné (Nil sinon)
  end
  
  def self.stat_var=(val)
    @@stat_var = val
  end
  
  def pipo(a=5,*b) # *b peut être nul
    puts a
    puts b # puts d'un tableau affiche à la ligne chacun des éléments
  end
  
  def pipo2(a,&c) # &c représente un bloc et peu être nul. Attention : encadré le yield avec block_given
    if block_given?
      yield a # sinon LocalJumpError (no block given)
    end
  end
  
  def pipo3(a,b,c,d)
    puts [a,b,c,d]
  end
  
  def small_pipo(a)
    puts "That's small pipo ! a = "+a.to_s
  end

end

# Appel de méthode
Pipo.static_hello
Pipo::static_hello
p = Pipo.new
p.instance_hello
puts p.var
# Variables statiques et accesseurs
puts 'Pipo.static_var = '+Pipo.stat_var.to_s
Pipo.stat_var = 22
puts 'Pipo.static_var = '+Pipo.stat_var.to_s
# Arguments zarbes et autres joyeusetés
tab = [1,2,3,4]
p.pipo3(*tab) # on éclate le tableau
p.pipo2(5) { |i| puts 'b -> '+i.to_s } # les parenthèses sont optionnelles. Ruby c fou ! mais pas ici !!!
p.pipo2(7)
# Une méthode à la place d'un bloc (on convertit)
p.pipo2(9,&p.method(:small_pipo)) # 13h13 : Si Python c bien, Ruby c dingue !!!
# Une procédure à la place d'un bloc (on convertit)
myproc = proc { |i| puts 'une petite proc ! i = '+i.to_s }
p.pipo2(9,&myproc) #13h14 !
myproc.call(3)
p.pipo 2
p.pipo 2, [3,4]

# alias
$pipo = 4
alias $zorba $pipo
puts $zorba

# module
module Zorba
  CONSTANTE = 1
  def Zorba.m
    puts "Zorba.m"
  end
  def m2
    puts "Zorba.m2"
  end
  def m3
    puts "Zorba.m3"
  end
  module_function :m3 # Fabication d'une COPIE pour le module (pas d'alias)
  P0,P1,P2 = *0...3 # créé un tableau [0,1,2] puis l'éclate pour le répartir dans chaque var
end
puts 'Constante du module Zorba = '+Zorba::CONSTANTE.to_s
Zorba.m
puts 'Constante P2 = '+Zorba::P2.to_s
# Zorba.m2 -> impossible m2 n'est pas available comme fonction de module
Zorba.m3
include Zorba
m2 # 13h28 : Je pense que quand Matz dit les mécanismes internes de Ruby sont complexes, je veux bien le croire !
m3

# Traiter le cas des includes dans les classes (comme des interfaces) aka mixins
# Traiter public, protected, private

#Gestion des exceptions
i = 0
begin
  puts 'Block'
  if i == 0 then raise "PIPO" end
rescue StandardError
  puts 'StandardError detecté'
  i = 1
  retry # pas de ensure
else
  puts 'No exception'
ensure
  puts 'Toujours exécuté'
end
# Lol : 13h35 : y'a catch et throw en plus...

# IO Standard
print 'Enter your name : '
name = gets
name.chomp!
puts 'Your name is '+name+'. What a wonderful name !'

# Quelques méthodes utiles
puts Dir.getwd

require 'socket'
require 'timeout'

# Network & Thread
t = Thread.new { #Un thread est lancé dès sa création
  puts 'Deb'
  z = TCPServer.new('localhost', 8000) # Pas de bind ni de listen ;-)
  puts z
  timeout(10) do
    puts 'Waiting connexion'
    session = z.accept
    puts 'Waiting message'
    data = session.recv(255)
    puts ">>> "+data.to_s # 16h04 : ça marche !!
    session.close
  end
}
  
t2 = TCPSocket.new('localhost', 8000)
puts t2.send("pipo",0).to_s+' nb octects sent'

t.join

# Design Pattern : Singleton
require 'singleton'
class Only
  include Singleton
end
# Un seul et même objet partagé pour cette classe : new est private
a = Only.instance
puts a
b = Only.instance
puts b
