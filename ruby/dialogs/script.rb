Dir.chdir("C:/Linux/Dev/Scripts")
dialogs = File.new("dialogs.txt")

texts = Array.new
texts << "null"
for line in dialogs
	id,text = line.split("\t")
	texts << text.chop
end
puts texts

arbre = File.new("arbres.txt")

#com = gets('Entrez condition pour dialogue (x,fst,def) : ') ???
com = gets().chop!

while com != "end"
	for line in arbre
		line.chop!
		cond, num, seq = line.split("\t")
		#print "[",cond,"] ",num," -> ", seq, "\n"
		if cond == com
			puts texts[num.to_i]
			for s in seq.split(" ")
				#print s, ":", s[0], ":" # s[0] ???
				#print "* ", texts[s[0].to_i], "\n"
				print "* ", texts[s.split(",")[0].to_i], "\n"
			end
		end
	end
	com = gets().chop! # ???
end

puts "END OF SCRIPT"
