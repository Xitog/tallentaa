# irb(main):012:0> Card.class_variables
# => ["@@carreau_sept"]

class Card
	
	attr_reader :num, :color, :name, :str_norm, :str_att
	
	private :initialize
	
	CARREAU = 1
	COEUR = 2
	TREFLE = 3
	PIQUE = 4
	
	AS = 1
	SEPT = 7
	HUIT = 8
	NEUF = 9
	DIX = 10
	VALET = 11
	DAME = 12
	ROI = 13
	
	def initialize(num,color,name,str_norm,str_att)
		@num=num
		@color = color
		@name = name
		@str_norm = str_norm
		@str_att = str_att
	end
	
	def to_s
		return @name
	end
	
	@@carreau_sept = Card.new(SEPT,CARREAU,"sept de carreau",1,1)
	@@carreau_huit = Card.new(HUIT,CARREAU,"huit de carreau",2,2)
	@@carreau_neuf = Card.new(NEUF,CARREAU,"neuf de carreau",3,7)
	@@carreau_dix = Card.new(DIX,CARREAU,"dix de carreau",7,5)
	@@carreau_valet = Card.new(VALET,CARREAU,"valet de carreau",4,8)
	@@carreau_dame = Card.new(DAME,CARREAU,"dame de carreau",5,3)
	@@carreau_roi = Card.new(ROI,CARREAU,"roi de carreau",6,4)
	@@carreau_as = Card.new(AS,CARREAU,"as de carreau",8,6)
	
	@@coeur_sept = Card.new(SEPT,COEUR,"sept de coeur",1,1)
	@@coeur_huit = Card.new(HUIT,COEUR,"huit de coeur",2,2)
	@@coeur_neuf = Card.new(NEUF,COEUR,"neuf de coeur",3,7)
	@@coeur_dix = Card.new(DIX,COEUR,"dix de coeur",7,5)
	@@coeur_valet = Card.new(VALET,COEUR,"valet de coeur",4,8)
	@@coeur_dame = Card.new(DAME,COEUR,"dame de coeur",5,3)
	@@coeur_roi = Card.new(ROI,COEUR,"roi de coeur",6,4)
	@@coeur_as = Card.new(AS,COEUR,"as de coeur",8,6)
	
	@@trefle_sept = Card.new(SEPT,TREFLE,"sept de trefle",1,1)
	@@trefle_huit = Card.new(HUIT,TREFLE,"huit de trefle",2,2)
	@@trefle_neuf = Card.new(NEUF,TREFLE,"neuf de trefle",3,7)
	@@trefle_dix = Card.new(DIX,TREFLE,"dix de trefle",7,5)
	@@trefle_valet = Card.new(VALET,TREFLE,"valet de trefle",4,8)
	@@trefle_dame = Card.new(DAME,TREFLE,"dame de trefle",5,3)
	@@trefle_roi = Card.new(ROI,TREFLE,"roi de trefle",6,4)
	@@trefle_as = Card.new(AS,TREFLE,"as de trefle",8,6)
	
	@@pique_sept = Card.new(SEPT,PIQUE,"sept de pique",1,1)
	@@pique_huit = Card.new(HUIT,PIQUE,"huit de pique",2,2)
	@@pique_neuf = Card.new(NEUF,PIQUE,"neuf de pique",3,7)
	@@pique_dix = Card.new(DIX,PIQUE,"dix de pique",7,5)
	@@pique_valet = Card.new(VALET,PIQUE,"valet de pique",4,8)
	@@pique_dame = Card.new(DAME,PIQUE,"dame de pique",5,3)
	@@pique_roi = Card.new(ROI,PIQUE,"roi de pique",6,4)
	@@pique_as = Card.new(AS,PIQUE,"as de pique",8,6)
	
end

class Deck
	
	def initialize
	end
	
	def shuffle
	end
	
	def cut
	end
	
end

class Player

	def initialize(game,cards,pos)
		@hand = cards
		@game = game
		@pos = pos
		@game.register(self)
	end
	
end

class Game

	def intialize(start_player)
		@players = [start_player]
		@starter = start_player
		@turn = 0
	end
	
	def register(player)
		@players << player
	end
	
	def wait_player
		while @players
	end
	
	def start_auction
	end
	
	def start_game
	end
	
	def start_turn
	end
	
	def resolve_turn
	end
	
	def end_game
	end
	
end
