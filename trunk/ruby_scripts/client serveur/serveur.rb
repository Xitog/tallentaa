require 'socket'

Nb_Connexion_Max = 1

def serveur()
	
	serveur = TCPserver.open(2000)
	adresse = serveur.addr
	print('1 - ', adresse.join(':'), "\n")
	adresse.shift										# Enlève "AF_INET"
	print('2 - ', adresse.join(':'), "\n")
	printf("Le serveur est sur %s\n", adresse.join(":"))
	
	nb_connexion = 0
	connexions = Array.new(Nb_Connexion_Max, 0)
	
	while nb_connexion < Nb_Connexion_Max
		connexions[nb_connexion] = Thread::start(serveur.accept) do |s|	# s est un TCPSocket
			print(s, "est acceptée\n")
			nb_connexion += 1
			while s.gets()
				c = s.readline
				print c
				if c == "end\n"
					print(s, "est terminée\n")
					puts '==> Goodbye'
					s.close()
					Thread::exit()
				end
				#s.flush
				#print(s.readline)
				#print(s.read)
				#s.write($_)
			end
			#print(s, "est terminée\n")
			#timeout(1) {
			#	s.close
			#}
		end
		puts nb_connexion
	end
	
	for i in connexions
		if i.instance_of?(Thread)
			i.join
		end
	end
	
end

