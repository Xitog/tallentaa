require 'socket'

#def client(port)
def client(hote= '127.0.0.1', port = 2000)
	#hote = 'localhost'
	print('Trying ', hote, ' ...')
	STDOUT.flush
	s = TCPsocket.open(hote,port) 
	print(" termine\n")
	print("adresse source   : ", s.addr.join(":"), "\n")
	print("adresse distante : ", s.peeraddr.join(":"), "\n")
	cmd = ''
	s.write("\n")
	while cmd != 'exit'
		cmd = gets()
		s.write(cmd+"\n")
		#i = s.send(cmd)
		#puts i
	end
	#while gets()
		#s.write($_)
		#print(s.readline)
	#end
	s.close
	
end
