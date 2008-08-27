#---------------------------------------------------------------------
# Nom : main.rb
# Auteur : Damien Gouteux
# Rôle : Un jeu de stratégie primitif...
# Version : alpha
# Date Last Modif : Dimanche 16 Octobre 2005
# Date Création : vendredi 23 septembre 2005, 17:39:39
#---------------------------------------------------------------------

#---------------------------------------------------------------------
# Licence : under GNU General Public License (GPL). Copyright DG 2005.
#---------------------------------------------------------------------

#---------------------------------------------------------------------
# TODO:
# -> Particle & Weapons							[13/10/05 Advance]
# -> Batiment & Unit of big size
# -> Better pathfinding
# -> Better menu
# -> Intro vidéo de chaque mission avec alpha augmentant
#	-> IA ennemis
# -> Chargement de cartes + formats de celles-ci
# -> Bug de particule à modifier : quand on tire depuis la gauche, ça touche pas
#---------------------------------------------------------------------

#---------------------------------------------------------------------
# Main Script
#---------------------------------------------------------------------
#module Main

require "Graphic"
#require "Core"
include Graphic
include Core

#name = gets
#p = Player.new("Bob")
#u = Unit.new(p, 1, 1)
#u2 = Unit.new(p, 1, 2)

def save(g,name)
	f = File.new(name,"w")
	Marshal.dump(g,f,20)
	f.close()
end

def load(name)
	f = File.new(name,"r")
	Marshal.restore(f)
	f.close()
end

def main2()
	g = load("svg1.txt")
	p1 = g.getPlayer(0)
	p2 = g.getPlayer(1)
 
	window = MainWindow.new(g, p1)
	window.show
	
end

def main(player, campaign='true', file_to_load='false')
	
	map = Map.new("The betrayal", 32, 32) #20, 12)
	g = Game.new("This game", map, Game::MAX_PLAYER, Game::ExtraFast)

	p1 = Player.new(g, player, Position.new(map, 1, 1))
	p2 = Player.new(g, "Xitog", Position.new(map, 15, 15))
	
	puts p1.getGid()

	u1  = StormTrooper.new(p1,Position.new(map,1,1))
	u2  = R4d5.new(p1,Position.new(map,1,2))
	u3  = StormTrooper.new(p1,Position.new(map,4,5))
	u4  = StormTrooper.new(p1,Position.new(map,5,5))
	u5  = R4d5.new(p1,Position.new(map,6,6))
	u6  = Probe.new(p2,Position.new(map,8,8))
	#u7  = Caserne.new(p1, Position.new(map,12,6))
	#u8  = Usine.new(p1, Position.new(map,17,3))
	u9  = ScoutTrooper.new(p1, Position.new(map,3,9))
	u10 = Tank.new(p1, Position.new(map,4,9))
	u11 = Officer.new(p1, Position.new(map,3,10))
	
	u1.weapons << PistoletLaser
	u2.weapons << CanonLaser
	u3.weapons << Blaster
	
	puts p1
	puts u1
	puts u2
	puts u3
	puts u4
	puts u5
	puts u6
	#puts u7
	#puts u8
	puts u9
	puts u10
	puts u11
        
	puts self
	#puts Unit.nbUnitTotale

	save(g, "svg1.txt")
	
	#a = BuildBat.new(nil, Position.new(map,10,10), Caserne)
	#puts a.uclass
	#puts a.position
	#a = BuildUsine.new(nil, Position.new(map,10,10))
	#puts a.uclass
	#puts a.position
	
	#puts "Verif du brouillard"
	#for i in map.brou
	#	for j in i
	#		print j,","
	#	end
	#end
	#puts
	# equivalent à :
	#print map.brou,"\n"
	# Mieux :
	for i in 0...map.x
		for j in 0...map.y
			print map.brou[0][j][i]
		end
		puts
	end
	
	window = MainWindow.new(g, p1)
	window.show # Appel bloquant !
	
end

def main3()
	t = true
	player = 'Bob'
	logo = 'pipo/pipo.png'
	find = true
	game1 = 'empty'
	game2 = 'empty'
	battle1 = 'empty'
	battle2 = 'empty'
	cmd = 'none'
	map = 'A desperate issue'
	
	#require 'curses'
	while t
		#Curses::clear
		#for i in 1..30
		#	puts
		#end
		puts '*******************************'
		puts '* Star Wars : Lord of Expanse *'
		puts '*******************************'
		puts '1 - Launch campaign'
		puts '2 - Load Game 1 ['+game1.to_s+']'
		puts '3 - Load Game 2 ['+game2.to_s+']'
		puts
		puts '4 - Start Battle'
		puts '5 - Load Saved Battle 1'
		puts '6 - Load Saved Battle 2'
		puts
		puts '7 - Set Player name ['+player+']'
		puts '8 - Set Logo ['+logo+'] ['+find.to_s+']'
		puts '9 - Set Map ['+map.to_s+']'
		puts
		puts '0 - Exit'
		puts t
		puts cmd
		print 'choice : '
		cmd = gets()
		cmd.chomp!
		if cmd == '1'
			main(player, true)	# Lance la campagne
			t = false
		elsif cmd == '2'
			main(player, true, game1)
		elsif cmd == '3'
			main(player, true, game2)
		elsif cmd == '4'
			main(player, false)
		elsif cmd == '5'
			main(player, false, battle1)
		elsif cmd == '6'
			main(player, false, battle2)
		elsif cmd == '7'
			print 'Enter the new name : '
			player = gets()
			player.chomp!
		elsif cmd == '8'
			#print 'Enter the file of the new logo : '
			#logo = gets()
			#logo.chomp!
			#find = File::exist?(logo)
			dic = []
			d = Dir.new('graphics/logo')
			d.each() { |filename|
				if filename != '.' and filename != '..'
					dic << filename.gsub('.png','').gsub('.PNG','')
				end
			}
			j = 1
			for i in dic
				puts j.to_s+' - '+i
				j += 1
			end
			print 'Enter the number of the new logo : '
			logo = gets()
			logo.chomp!
			logo = dic[logo.to_i-1]
		elsif cmd == '9'
			# Audit 29_03_06 : Dynamique, on charge le contenu du répertoire 'maps'
			dic = []
			d = Dir.new('maps')
			d.each() { |filename|
				if filename != '.' and filename != '..'
					dic << filename.gsub('.map','')
				end
			}
			j = 1
			for i in dic
				puts j.to_s+' - '+i
				j += 1
			end
			print 'Enter the number of the new map : '
			map = gets()
			map.chomp!
			map = dic[map.to_i-1]
		elsif cmd == '0'
			t = false
		else
			raise 'Order Unknown'
		end
		puts
		puts
	end
	puts '==> Goodbye'
	exit()
end

#
# Essai d'un modèle client serveur
#

require 'socket'

def serveur()
	
	serveur = TCPserver.open(2000)
	adresse = serveur.addr
	adresse.shift										# Enlève "AF_INET"
	printf("Le serveur est sur %s\n", adresse.join(":"))
	
	#while true
		Thread::start(serveur.accept) do |s|	# s est un TCPSocket
			print(s, "est acceptée\n")
			s.gets()
			puts 'e'
			while s.gets()
				s.write($_)
			end
			print(s, "est terminée\n")
			s.close
		end
	#end
	
end

def client(port)

	hote = 'localhost'
	print('Trying ', hote, ' ...')
	STDOUT.flush
	s = TCPsocket.open(hote,port) 
	print(" terminé\n")
	print("adresse source   : ", s.addr.join(":"), "\n")
	print("adresse distante : ", s.peeraddr.join(":"), "\n")
	while gets()
		s.write($_)
		print(s.readline)
	end
	s.close
	
end

main3()

puts 'Hello World'
