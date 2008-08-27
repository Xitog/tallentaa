#
# Ce module inclut le noyau du jeu et l'étend. C'est à dire qu'il ajoute
# les éléments spécifiques à Star Wars, Lord of the expanse.
# Ces éléments sont deux trois catégories :
#		-> Ordres
#		-> Unitées
#		-> Doodads
#
module Swloe

require "core.rb"
include Core

class Core::Unit
	
	STORMTROOPER = 0
	R4D5 = 1
	PROBE = 2
	Caserne = 3
	Usine = 4
	Generateur = 5
	Extracteur = 6
	Relais = 7
	SCOUTTROOPER = 8
	TANK = 9
	OFFICIER = 10
	Centre = 11
	Armurerie = 12
	Tourelle = 13
	
end

class Core::Doodad

  Roc = 0
  Navette = 1
  Navette_Small = 2

end

# Les ordres de SWLOE
class BuildStormTrooper < Build

	def initialize(unit)
		super(unit, StormTrooper)
	end
	
end

class BuildScoutTrooper < Build

	def initialize(unit)
		super(unit, ScoutTrooper)
	end
	
end

class BuildOfficer < Build

	def initialize(unit)
		super(unit, Officer)
	end
	
end

class BuildTank < Build

	def initialize(unit)
		super(unit, Tank)
	end
	
end

# Les bâtiments du jeu

class Caserne < Constructor
	
	TimeToBuild = 80
	ActionOK = [BuildScoutTrooper, BuildStormTrooper, BuildOfficer]
	Name = "Caserne"
	Text = "Forme des soldats."
	Size = [3,3]
	Sortie = [1,3]
	Vision = 80
	
	def initialize(player, position, build=100)
		super(player, Unit::Caserne, position, build)#, [3,3], [])
	end
	
end

class Usine < Constructor

	TimeToBuild = 100 #120
	ActionOK = [BuildTank]
	Name = "Usine"
	Text = "Construit des véhicules."
	Size = [3,4]
	Sortie = [1,4]
	Vision = 80
	
	def initialize(player, position, build=100)
		super(player, Unit::Usine, position, build)#, [3,4], [])
	end

end

class Generateur < Bat

	TimeToBuild = 100 #120
	ActionOK = []
	Name = "Generateur"
	Text = "Génère de l'énergie."
	Size = [1,1]
	Vision = 10
	
	def initialize(player, position, build=100)
		super(player, Unit::Generateur, position, build)#, [1,1], [])
	end

	def set_default_order
		# place here the default order for batiment like generator or extractor
		addAction(Generate.new(self))
	end
	
end

class Extracteur < Bat

	TimeToBuild = 60
	ActionOK = []
	Name = "Extracteur"
	Text = "Extrait le minerai des sous-sols d'une planète."
	Size = [2,2]
	Vision = 10
	
	def initialize(player, position, build=100)
		super(player, Unit::Extracteur, position, build)#, [2,2], [])
	end

	def set_default_order
		# place here the default order for batiment like generator or extractor
		addAction(Extract.new(self))
	end
	
end

class Relais < Bat

	TimeToBuild = 90 #160
	ActionOK = []
	Name = "Relais Rayon de Mort"
	Text = "Arme absolue impériale ce classe III."
	Size = [2,1]
	Vision = 60
	
	def initialize(player, position, build=100)
		super(player, Unit::Relais, position, build)#, [2,1], [])
	end

end

class Centre < Bat

	TimeToBuild = 90 #160
	ActionOK = []
	Name = "Centre de Recherche"
	Text = "R&D Impérial : Ruby powered."
	Size = [2,1]
	Vision = 50
	
	def initialize(player, position, build=100)
		super(player, Unit::Centre, position, build)#, [2,1], [])
	end

end

class Armurerie < Bat

	TimeToBuild = 90 #160
	ActionOK = []
	Name = "Armurerie"
	Text = "Armurerie impériale."
	Size = [2,1]
	Vision = 20
	
	def initialize(player, position, build=100)
		super(player, Unit::Armurerie, position, build)#, [2,1], [])
	end

end

class Tourelle < Bat

	TimeToBuild = 90 #160
	ActionOK = []
	Name = "Tourelle de défense"
	Text = "Défense légère impériale."
	Size = [2,1]
	Vision = 70
	
	def initialize(player, position, build=100)
		super(player, Unit::Tourelle, position, build)#, [2,1], [])
	end

end

# Ordre de construction de Bâtiment

class BuildCaserne < BuildBat

	Classe = Caserne
	
	def initialize(unit,position)
		super(unit,position,Caserne)
	end
	
end

class BuildUsine < BuildBat

	Classe = Usine
	
	def initialize(unit,position)
		super(unit,position,Usine)
	end
	
end

class BuildGenerateur < BuildBat

	Classe = Generateur
	
	def initialize(unit,position)
		super(unit,position,Generateur)
	end
	
end

class BuildExtracteur < BuildBat

	Classe = Extracteur
	
	def initialize(unit,position)
		super(unit,position,Extracteur)
	end
	
end

class BuildArmurerie < BuildBat

	Classe = Armurerie
	
	def initialize(unit,position)
		super(unit,position,Armurerie)
	end

end

class BuildCentre < BuildBat

	Classe = Centre
	
	def initialize(unit,position)
		super(unit,position,Centre)
	end

end

class BuildRelais < BuildBat

	Classe = Relais
	
	def initialize(unit,position)
		super(unit,position,Relais)
	end

end

class BuildTourelle < BuildBat

	Classe = Tourelle
	
	def initialize(unit,position)
		super(unit,position,Tourelle)
	end

end

class Extract < Action

	def initialize(unit)
		super("Extract",unit)
		@temp = 0
	end
	
	def do()
		# On ajoute toutes les X secondes au joueur de l'unit
		@temp += 1
		if @temp == 5
			@temp = 0
			self.unit.player.metal += 2
		end
	end
	
	def to_s
		return 'Extraction...'
	end
	
	def finish?()
		return false
	end
	
end

class Generate < Action

	def initialize(unit)
		super("Generate",unit)
		@temp = 0
	end
	
	def do()
		# On ajoute toutes les X secondes au joueur de l'unit
		@temp += 1
		if @temp == 5
			@temp = 0
			self.unit.player.energie += 2
		end
	end
	
	def to_s
		return 'Génération énergie...'
	end
	
	def finish?()
		return false
	end
	
end

#
#
# Unités du jeu SWLOE
#
#

class StormTrooper < Unit

	TimeToBuild = 160
	ActionOK = [Core::Move,Core::Attack,Core::Follow]
	Name = "StormTrooper"
	Text = "Le coeur des forces de l'Empire."
	Size = [1,1]
	Vision = 90
	
	def initialize(player, position)
		super(player, Unit::STORMTROOPER, position)
	end
	
	def StormTrooper.to_s()
		return 'StormTrooper'
	end
	
end

class ScoutTrooper < Unit

	TimeToBuild = 160
	ActionOK = [Core::Move,Core::Attack,Core::Follow]
	Name = "ScoutTrooper"
	Text = "Unitée de reconnaissance légère."
	Size = [1,1]
	Vision = 100
	
	def initialize(player, position)
		super(player, Unit::SCOUTTROOPER, position)
	end
	
	def ScoutTrooper.to_s()
		return 'ScoutTrooper'
	end
	
end

class Tank < Unit

	TimeToBuild = 160
	ActionOK = [Core::Move,Core::Attack,Core::Follow]
	Name = "Tank d'assaut"
	Text = "Unitée d'assaut superlourde."
	Size = [1,1]
	Vision = 90
	
	def initialize(player, position)
		super(player, Unit::TANK, position)
	end
	
	def Tank.to_s()
		return 'Tank'
	end
	
end

class Probe < Unit

	TimeToBuild = 40
	ActionOK = [Core::Move,Core::Attack,Core::Follow]
	Name = "Sonde"
	Text = "Une unitée de reconnaissance rapide."
	Size = [1,1]
	Vision = 100
	
	def initialize(player, position)
		super(player, Unit::PROBE, position)
	end
	
	def Probe.to_s()
		return 'Probe'
	end
	
end

class R4d5 < Unit

	TimeToBuild = 160
	ActionOK = [Core::Move,Core::Attack,Core::Follow,
							BuildUsine, BuildCaserne, BuildGenerateur,
							BuildExtracteur, BuildArmurerie, BuildTourelle]
	Name = "R4-D5"
	Text = "Droïde utilitaire."
	Size = [1,1]
	Vision = 60

	def initialize(player, position)
		super(player, Unit::R4D5, position)
	end
	
	def R4d5()
		return 'R4-D5'
	end
	
end

class Officer < Unit

	TimeToBuild = 160
	ActionOK = [Core::Move,Core::Attack,Core::Follow]
	Name = "Officier Impérial"
	Text = "Dirige et motive les troupes de l'Empire."
	Size = [1,1]
	Vision = 90

	def initialize(player, position)
		super(player, Unit::OFFICIER, position)
	end
	
	def Officer.to_s()
		return 'Officer'
	end
	
end

end