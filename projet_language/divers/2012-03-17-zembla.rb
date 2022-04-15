# Une liste d'éléments.
# Deux choses héritent d'éléments :
#	Token
#	Node
# On commence par le Token le plus prioritaire
# On le prend, on construit un noeud, puis on y met les opérandes
# On remplace dans la liste les opérandes et le Token le + prio par un Node
#
# Un node, comme branche G et D prend soit un node, soit un Token, donc 
# un Element !

class Element
end

class Token < Element
	attr_reader :value
	def initialize(value)
		@value = value
	end
	def to_s
		@value.to_s
	end
end

class Node < Element
	attr_reader :middle, :left, :right
	def initialize(middle, left, right)
		@middle = middle
		@left = left
		@right = right
	end
	def to_s
		'('+@middle.to_s+','+@left.to_s+','+@right.to_s+')'
	end
end

e2 = Token.new('2')
eAdd =Token.new('+')
e3 = Token.new('3')
eMul = Token.new('*')
e4 = Token.new('4')

list = [e2, eAdd, e3,eMul,e4]

for e in list
	puts e
end

prio = { '+' => 1, '*' => 2 }

while list.length > 1
	puts 'iteration one'
	most = -1
	mosti = -1
	i = 0
	for e in list
		if e.class == Token and prio.has_key? e.value then
            puts 'eval = ' + e.value.to_s
            puts 'most = ' + most.to_s
            puts 'prio = ' + prio[e.value].to_s
			if prio[e.value] > mosti then
				most = e
				mosti = i
			end
		end
		i+=1
	end
	n = Node.new(most, list[mosti-1], list[mosti+1])
	puts 'new node ! :'
	puts n
	list.delete_at(mosti+1)
	puts 'one deletion'
	for e in list
		puts e
	end
	list.delete_at(mosti-1)
	puts 'two deletion'
	list[mosti-1] = n

	for e in list
		puts e
	end
	
	puts 'lenght = '
	puts list.length
end

# 11h17 : ça marche avec 2+3*4

def interpret(list)
    return compute(list[0])
end

def compute(element)
    if element.class == Node then
        puts "it's a node!"
        node = element
        if node.middle.value == '*' then
            return compute(node.left) * compute(node.right)
        elsif node.middle.value == '+' then
            return compute(node.left) + compute(node.right)
        end
    elsif element.class == Token then
        puts "it's an element!"
        return element.value.to_i
    else
        puts element.class
    end
end

puts 'result = ' + interpret(list).to_s

# 11h24 : et je l'interprète now !
