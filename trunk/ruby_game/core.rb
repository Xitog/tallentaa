
module Core

module Loggable
	
	def getGid()
		return @gid
	end
	
	def log(l)
	end
 
end

def dist(x1,y1,x2,y2)
	#puts x1.to_s + " " + y1.to_s + " " + x2.to_s + " " + y2.to_s
	a = (x1 - x2)**2
	b = (y1 - y2)**2
	#puts Math.sqrt(a+b)
	return Math.sqrt(a+b)
end

#---------------------------------------------------------------------------

#
# Partie Core Game
#

#---------------------------------------------------------------------
# Gestion de la map et des positions
#---------------------------------------------------------------------

class Doodad
  
  attr_reader :dessin, :size_x, :size_y, :visible
	
  def initialize(p,size_x,size_y,type,bloquant_sur=[1,1])
		if p.instance_of? NilClass
			raise "Position not valid"
		end
		@map = p.map		  # Map du doodad
    @x = p.x					# Position x du doodad
    @y = p.y					# Position y du doodad
    @size_x = size_x	# Size x max
    @size_y = size_y	# Size y max
    @dessin = type		# Le dessin recouvrant un rect(x,y,x+size_x,y+size_y)
		# Designe le rectangle(x,y,x+bloquant[0],y+bloquant[1]) sur lequel on ne peut passer
		@bloquant_sur = bloquant_sur
		@visible = false
		#@visible = visible?
		#if @visible then put end
  end
  
  def in?(x,y)
    if x >= @x and x < @x+@size_x and y >= @y and y < @y+@size_y
      return true
    else
      return false
    end
  end
  
  def at?(x,y)
    return ( x == @x and y == @y)
  end
  
	def ok?(x,y)
		if x >= @x and x < @x+@bloquant_sur[0] and 
			 y >= @y and y < @y+@bloquant_sur[1]
			return false
		else
			return true
		end
	end
	
	def visible?(player) # Si un carré ou se trouve le doodad est découvert, tous sont découverts
		for i in @x...@x+@size_x
			for j in @y...@y+@size_y
				#print i,":",j,"\n"
				#print @map
				#print @map.brou
				#gets
				if @map.brou[player.num][i][j] != 0
					@visible = true
					put(player)
					return true
				end
			end
		end
		return false;
	end
	
	def put(player)
		for i in @x...@x+@size_x
			for j in @y...@y+@size_y
				@map.brou[player.num][i][j] = 1
			end
		end
	end
	
end

class DoodadArray < Array

  def initialize
    super
  end
  
  def <<(e)
    if not e.instance_of?(Doodad)
      raise Exception("Pipo")
    end
    
    #to_a <<(e)          # Essayer de faire super.<<(e) mais cela invoque la même !!
    #super.push(e)
		super
  end
  
  def something_at?(x,y)
    #puts x.to_s + " - " + y.to_s + " - " + (to_a.length-1).to_s
    #puts self.length-1
    #for i in 0..self.length-1
    for i in 0..to_a.length-1
      if to_a[i].at?(x,y)
        return to_a[i]
      end
    end
    return nil
  end
  
	def ok?(x,y)
		for i in to_a
			if not i.ok?(x,y)
				return false
			end
		end
		return true
	end
	
end

class Map

	include Loggable
	
  attr_reader :name, :map, :x, :y, :brou, :unit, :doodads, :nbPlayers
  
  def initialize(name, x=6, y=6)
    @name = name
    @x = x
    @y = y
		@nbPlayers = 2
    to_s()
		@gid = 'map'
    create
  end
  
	def log(l)
		l.addEntry('map = Map.new("'+@name+'", '+@x.to_s+', '+@y.to_s+')')
	end
	
  def create
    #puts "create"
    #@map = Matrix.zero(7)
    @map = Array.new(@x, Array.new)
    #@brou = Array.new(@x, Array.new)
    @unit = Array.new(@x, Array.new)

    for i in 0..@x-1
      for j in 0..@y-1
        @map[i] += [rand(5)]                  # ONLY FOR TEST
        #@brou[i] += [0]
        @unit[i] += [0]
        #puts @map[i,j]
        #puts @map
        #print "(",i,",",j,")",@map[i][j]," "
      end
      #print "\n"
    end
    #puts "check"
    #for i in 0..6
    #  for j in 0..6
    #    print "(",i,",",j,")",@map[i][j]," "
    #  end
    #  print "\n"
    #end
    #puts "end create"

		# Brou 17/12/05 : le brouillard est spécifique à chaque joueur !
		@brou = Array.new(@nbPlayers, Array.new)
		for i in 0...@nbPlayers
			@brou[i] = Array.new(@x, Array.new)
			for ii in 0..@x-1
				for jj in 0..@y-1
					@brou[i][ii] += [0]
				end
			end
		end
		
		@doodads = DoodadArray.new()
    @doodads << Doodad.new(Position.new(self,10,3),1,2,Doodad::Roc)      # ONLY FOR TEST
		@doodads << Doodad.new(Position.new(self,10,7),2,2,Doodad::Navette,[2,1])	# ONLY FOR TEST
		@doodads << Doodad.new(Position.new(self,14,2),2,1,Doodad::Navette_Small,[2,1]) # ONLY FOR TEST
		
  end
  
  def to_s
    return @name+" ("+@x.to_s+","+@y.to_s+")"
  end
  
	def empty?(x,y,sx=1,sy=1)
		if sx==1 and sy == 1
			return @unit[x][y] == 0
		else # 17/12/05 empty? gère maintenant une taille
			for i in x...x+sx
				for j in y...y+sy
					if @unit[i][j] != 0
						return false
					end
				end
			end
			return true
		end
	end
	
	def brou?(p,x,y,sx=1,sy=1)	# 19/12/2005 y'a t il ne serait-ce qu'un carré en brou ?
		if sx==1 and sy == 1
			return @brou[p.num][x][y] <= 1
		else
			for i in x...x+sx
				for j in y...y+sy
					if @brou[p.num][i][j] <= 1
						return true
					end
				end
			end
			return false
		end
	end
	
  def put(unit)
		if @unit[unit.x][unit.y] != 0
			raise "Impossible de placer l'unité ici"
		end
		if unit.class::Size[0] == 1 and unit.class::Size[1] == 1
			@unit[unit.x][unit.y] = unit
			#if @brou[unit.x][unit.y] == 0
			#	@brou[unit.x][unit.y] = 2 # brou une case occupée est forcément vue
			#else
			#	@brou[unit.x][unit.y] += 1
			#end
		else
			for i in unit.x...unit.x+unit.class::Size[0]
				for j in unit.y...unit.y+unit.class::Size[1]
					@unit[i][j] = unit
					#if @brou[i][j] == 0
					#	@brou[i][j] = 2		# brou une case occupée est forcément vue
					#else
					#	@brou[i][j] += 1
					#end
				end
			end
		end
		# Gestion brouillard [new 16/12/05]
		radius = (unit.vision/32)*2
		ux = unit.x*32+(unit.class::Size[0]-1)*16+16
		uy = unit.y*32+(unit.class::Size[1]-1)*16+16
		up = unit.player.num
		for i in unit.x-radius...unit.x+radius
			for j in unit.y-radius...unit.y+radius
				if i >= 0 and j >= 0 and i < @x and j < @y
					#print ">>> ",dist(i*32+16,j*32+16,(unit.x+16)*32,(unit.y+16)*32),":",unit.vision,"\n"
					if dist(i*32+16,j*32+16,ux,uy) <= unit.vision 
						if @brou[up][i][j] == 0
							@brou[up][i][j] = 2
						else
							@brou[up][i][j] += 1
						end
					end
				end
			end
		end
  end
  
  def remove(unit)
		if unit.class::Size[0] == 1 and unit.class::Size[1] == 1
			@unit[unit.x][unit.y] = 0
		else
			for i in unit.x...unit.x+unit.class::Size[0]
				for j in unit.y...unit.y+unit.class::Size[1]
					@unit[i][j] = 0
				end
			end
		end
		# Neo Radius
		radius = (unit.vision/32)*2
		up = unit.player.num
		for i in unit.x-radius...unit.x+radius
			for j in unit.y-radius...unit.y+radius
				if i >= 0 and j >= 0 and i < @x and j < @y
					#print ">>> ",dist(i*32+16,j*32+16,(unit.x+16)*32,(unit.y+16)*32),":",unit.vision,"\n"
					if dist(i*32+16,j*32+16,unit.x*32+16,unit.y*32+16) <= unit.vision 
						#if @brou[i][j] == unit
							@brou[up][i][j] -= 1
						#end
					end
				end
			end
		end
  end
  
	def array_to_list_of_unit(array, player)
		group = []
		xdeb = array[0];
		ydeb = array[1];
		xfin = array[2];
		yfin = array[3];
		for i in xdeb..xfin
			for j in ydeb..yfin
				if @unit[i][j] != 0 and @unit[i][j].player == player
						group << @unit[i][j]
				end #if
			end #for
		end #for
		if group.length > 0
			group.sort!{ |x,y| 
				x.type <=> y.type
			}
		end
		return group
	end
	
end

class Position

  attr_reader :map, :x, :y

  def initialize(map, x, y)
    @map = map
    @x = x
    @y = y
  end

end

#---------------------------------------------------------------------

class Logger

	def initialize(g)
		@game = g
		@entries = []
	end
	
	def addEntry(s)
		#@entries << '['+time()+'/'+@game.turnElapsed().to_s+'] '+s
		#@entries << '['+@game.turnElapsed().to_s+']'+s.to_s
		@entries << @game.turnElapsed().to_s+'#'+s.to_s
	end
	
	def output(file)
		f = File.new(file,'w')
		#~f.write(@game.name+"\n")
		#~f.write(@game.map.to_s+"\n")
		#~f.write(Game::MAX_PLAYER.to_s+"\n")
		#~f.write(@game.Time.to_s+"\n")
		for i in @entries
			f.write(i.to_s+"\n")
		end
		f.close()
	end
	
	def time()
		t = Time::now
		return t.hour.to_s+':'+t.min.to_s+':'+t.sec.to_s
	end
	
end

#
# Incarne une partie : c'est à dire X joueurs sur une map donnée.
#
class Game
  
	include Loggable
	
	# Paramètre du jeu
	MAX_PLAYER = 2
	MAX_UNIT = 12
	
	# Contrôle du temps
	Normal = 0.075
	Fast = 0.050
	Slow = 0.100
	ExtraFast = 0.025
	ExtraSlow = 0.125
	
  attr_reader :name, :map, :particlesEngine, :glog
  
  def initialize(name, map, nbPlayerMax=MAX_PLAYER, time=Normal)
    @name = name
    @map = map
    @players = []
		@nbPlayerMax = nbPlayerMax
    # Gestion des particules
    @particlesEngine = ParticlesEngine.new(4)
    Particle.setEngine(@particlesEngine)
		@tour = 0
		@start = Time::now
		@Time = time
		@glog = Logger.new(self) #File.new(name+".log","w")
		#@log.write('['+Time::now.to_s+'] '+@name+' : starting game.'+"\n")
		#@log.addEntry(@name+' : starting game.')
		@gid = 'game'
		@map.log(@glog)
		log()
		@pause = false
	end
  
	def log(l=@glog)
		l.addEntry(@gid+' = Game.new("'+@name+'", '+@map.getGid()+', '+@nbPlayerMax.to_s+', '+@Time.to_s+')')
	end
	
	def register(player)
		if @players.length < MAX_PLAYER
			@players << player
			#player.log(@glog)
		else
			raise "too many players -> aborting"
		end
		return (@players.length-1)
	end

	# 20/12/2005 gestion des pauses
	def paused?
		return @pause
	end
	
	def pause
		@pause = true
	end
	
	def resume
		@pause = false
	end
	
  def update()
		if @pause
			return
		end
		@tour += 1
		t_deb = Time::now
    for i in 0..@players.length-1
      @players[i].update()
    end
    @particlesEngine.update_all()
		# Contrôle du temps que prend un tour
		t_duree = Time::now - t_deb
		while t_duree < @Time
			t_duree = Time::now - t_deb
		end
  end
	
	def getPlayer(i)	# Pour Marshal
		return @players[i]
	end
	
	def timeElapsed()
		puts @start
		puts Time::now
		return Time::now-@start
	end
	
	def turnElapsed()
		return @tour
	end
	
	def terminate()
		#@log.write('['+Time::now.to_s+'] '+@name+' : exiting game.'+"\n")
		#@log.close()
		t = Time::now
		tab = []
		tab << t.day
		tab << t.month
		tab << t.year
		tab << t.hour
		min = t.min
		@glog.addEntry(@name+' : exiting game.')
		# Audit 29_03_06 : mise des replays dans répertoire spécifique
		@glog.output('replays/'+@name+'_'+tab.join('_')+'h'+min.to_s+'.log')
	end
	
end

class Replay
	
	def initialize(filename)
		@actions = File.new(filename).readlines()
	end
	
	def replay()
		
	end
	
end

#~class ReplayedGame < Game

	#~def initialize(filename)
		#~file = File.new(filename, 'w')
		#~@actions = file.readlines
		#~# Reste un truc: convertir une chaine en une carte !
		#~super(@actions[0],@actions[1],@actions[2].to_i,@actions[3].to_i)	# Faut les lires dans le fichier !! ou marshalé au début !
	#~end
	
	def update()
		#for i in @actions
			time = # Extraite le truc entre crochet : scanf ?
			if @tour == time
				# Faire l'action
			end
		#end
		super
	end
	
#~end

#---------------------------------------------------------------------
# Gestion des armes
#---------------------------------------------------------------------

#
# Classe arme : pour les armes
#
class Weapon

  attr_reader :velocity, :force, :portee, :typew, :guidee, :nom, :reload_time
  
  def initialize(nom, typew, portee, force, velocity, reload_time=1, typep=0, guidee=false, unit=nil)
    @nom = nom
    @unit = unit
    @typew = typew
    @portee = portee
    @force = force
    @velocity = velocity    # Max = 10
    @guidee = guidee
		@reload_time = reload_time
		@cpt = 0
		@typep = typep
  end
  
	def update()
		if @cpt > 0
			@cpt -= 1
		end
	end
	
  def fire(from_x, from_y, with_angle, cible)
		@cpt = @reload_time
    return Particle.new(self, @typep, from_x, from_y, with_angle, cible)
  end
  
	def ready?
		return @cpt == 0
	end
	
end

# type parmis : laser, grenade, rocket, claser (lasers continus)
# ? faire des classes pour chacune de ces valeurs ??
PistoletLaser = Weapon.new("Pistolet Laser", "Laser", 100, 3, 8.0, 30, 0) # 80 de portée avant
FusilLaser = Weapon.new("Fusil Laser", "Laser", 120, 4, 8.0, 30, 1)
Grenade = Weapon.new("Grenade", "Grenade", 80, 6, 5.0, 50, 0)
Blaster = Weapon.new("Blaster", "Laser", 100, 5, 8.0, 30, 1)
CanonLaser = Weapon.new("Weapon Laser", "Laser", 300, 8, 9.0, 50, 2)

#---------------------------------------------------------------------
# Gestion des tirs
#---------------------------------------------------------------------

#
# Une particule = un laser, un missile...
#
class Particle

  attr_reader :weapon, :x, :y, :typep, :die, :angle
  
  @@engine = nil
  
  def Particle.setEngine(e)
    @@engine = e
  end
  
  def initialize(weapon, typep, x, y, angle, cible)
    @weapon = weapon
    @x = x
    @y = y
    @angle = angle
    @cible = cible
    #@@engine << self
    @@engine.add(self)
		@typep = typep	#@weapon.typew
		@distance = 0
		@die = false
	end
  
  def update()
		#puts "Warn 1"
    #include Math
		#puts "Warn 2"
    # Calcul pour faire avancer la particule
		x = @x + @weapon.velocity * Math.cos(@angle/180.0*Math::PI)
    y = @y + @weapon.velocity * Math.sin(@angle/180.0*Math::PI)
		#puts @x.to_s + "," + @y.to_s + "/" + x.to_s + "," + y.to_s
		@distance += Gosu::distance(@x, @y, x, y)
		#puts @distance.to_s
		@x = x
		@y = y
		if @distance > @weapon.portee
			@die = true #die()
		end
		#puts Gosu::distance(@x,@y,@cible.x*32,@cible.y*32).to_s
		if Gosu::distance(@x,@y,@cible.x*32,@cible.y*32) < 20
			@cible.vie -= @weapon.force
			@die = true
			puts "vie = "+@cible.vie.to_s
		end
  end
  
	#def die()
		#@@engine -= [self]
		#@@engine.sup(self)
		#puts "die "+self.to_s+" reste : "+@@engine.length.to_s 
		#puts @@engine.to_s
		#puts "je meurs :" + @@engine.to_s
	#end
	
end

class ParticlesEngine
	
	attr_reader :p
	
	def initialize (limit)
		@limit = limit
		@p = []
	end
	
	def add(p)
		#puts @p.length.to_s
		if @p.length < @limit
			#puts "added"
			@p << p
		end
	end
	
	def sup(p)
		@p = @p - [p]
		#puts @p.to_s
		if @p.length > @limit
			puts "Error sup"
			exit
		end
	end
	
	def update_all()
		if @p.length > @limit
			puts "Error update :"+@p.length.to_s
			exit
		end
		to_remove = []
		# old style
		#for i in 0..@p.length-1
    #  @p[i].update()
		#	if @p[i].die
		#		to_remove << @p[i]
		#	end
    #end
		# new style
		for i in @p
			i.update()
			if i.die
				to_remove << i
			end
		end
		
		@p = @p - to_remove
	end
	
end

#
# Le particle engine gère toutes les particules (vitesse, avancement, etc...)
#
#class ParticlesEngine < Array
  
	#
	# Initialise un moteur de particule avec une limite de particule gérable
	#
	#def initialize(limit)
	#	@limit = limit
	#	puts "limit = " + @limit.to_s
	#end
	
  #def << (e)
  #  if not e.instance_of? Particle
  #    raise Exception("Error")
  #  end
		##puts "une particule prise en charge !"
    ##to_a << e
		##puts "long : " + length.to_s + " / " + @limit.to_s + " ! "
		#if length < @limit
		#	puts "une particule prise en charge !"
		#	super
		#	return
		#	#super.push(e)
		#end
		#puts "Limits !"
  #end
  
	#def push (e)
		#puts "Ohoh"
	#end
	
	#def +(l)
		#puts "no"
	#end
	
	#def -(l)
		#puts "yes"
	#end
	
  #def update_all()
  #  #puts "long : "+ (length-1).to_s
	#	puts length
	#	if length > 8
	#		exit
	#	end
		
	#	for i in 0..length-1
  #    self[i].update()
  #  end
  #end
  
#end

#---------------------------------------------------------------------
# Gestion des ordres
#---------------------------------------------------------------------

class Action

  attr_reader :name, :move, :unit
  
  def initialize(name, unit)
    @name = name
    @unit = unit
  end

	# A surcharger
	def do()
	end
	
	# A surcharger
	def finish?()
		return true
	end
	
	#def to_s
	#	return 'Action.new('+name.to_s+','+
	#end
	
	def to_s()
		return 'en action...'
	end
	
  #public
  #  @@move = Action.new("Move", nil)
  
end

# peut - être pas besoin....
class GroupAction

	attr_reader :aclass
	
	def initialize(aclass, par1=nil, par2=nil)
		@aclass = aclass
		@par1 = par1
		@par2 = par2
	end
	
	def make(u)
	
		if @par1.instance_of?(NilClass)
			a = @aclass.new(u)
		elsif @par2.instance_of?(NilClass)
			a = @aclass.new(u,@par1)
		else
			a = @aclass.new(u,@par1,@par2)
		end
		return a
		
	end

end

class Move < Action

  attr_reader :x, :y
  
  def initialize(unit, x, y)
    super("Move", unit)
    @x = x
    @y = y
		##@told = Time::now
  end
  
  def do()
    #puts "x = "+unit.x.to_s+" y = "+unit.y.to_s+" xd = "+@x.to_s+" yd = "+@y.to_s
    ##r = Time::now-@told
		#puts "Rap : "+@unit.rapidite.to_s
		#puts "Result : "+r.to_s
		#puts @told
		#if r > @unit.rapidite
			x2 = @unit.x
			if @unit.x < @x
				x2 = @unit.x + 1
				@unit.angle = 1
			elsif @unit.x > @x
				x2 = @unit.x - 1
				@unit.angle = 3
			end
			y2 = @unit.y
			if @unit.y < @y
				y2 = @unit.y + 1
				@unit.angle = 2
			elsif @unit.y > @y
				y2 = @unit.y - 1
				@unit.angle = 0
			end
			if @unit.map.unit[x2][y2] == 0 and @unit.map.doodads.ok?(x2,y2) #@unit.map.doodads.something_at?(x2,y2) == nil
				@unit.pos(x2,y2)
			else
				# Là faut réfléchir, pour l'instant on fait rien et on attend
			end
		#	@told = Time::now
		#end
  end
  
  def finish?()
    return (@unit.x == @x and @unit.y == @y) 
  end
  
	def to_s()
		return 'en mouvement vers ['+@x.to_s+','+@y.to_s+']'
	end
	
end

#
# Action d'attaquer une unité
#
class Attack < Action

  def initialize(unit, cible)
    super("Attack", unit)
    @cible = cible
		puts "attack on "+cible.to_s
		puts "nb weapons : "+unit.weapons.length.to_s
  end
  
  def do()
		
		# gestion de l'angle
		if @unit.x < @cible.x
			@unit.angle = 1
		elsif @unit.x > @cible.x
			@unit.angle = 3
		end
		if @unit.y < @cible.y
			@unit.angle = 2
		elsif @unit.y > @cible.y
			@unit.angle = 0
		end
		
    if @unit.weapons.length > 0
			d = dist(@unit.x, @unit.y, @cible.x, @cible.y)
			#puts (d*32).to_s+" "+@unit.weapons[0].portee.to_s
			if d*32 > @unit.weapons[0].portee
				m = Move.new(@unit, @cible.x, @cible.y)
				m.do()
			else
				# Calcul de l'angle
				#puts "I do something"
				a = Gosu::angle(@unit.x, @unit.y, @cible.x, @cible.y)
				a -= 90
				if a < 0
					a += 360
				end
				#puts a
			
				# Feu !
				if @unit.weapons[0].ready?
					@unit.weapons[0].fire(@unit.x*32+16, @unit.y*32+16, a, @cible)
				end
			end
		end
  end
  
  def finish?()
    return (@cible.vie <= 0) 
  end
  
	def to_s()
		return 'attaque : '+@cible.class.to_s+' ('+@cible.vie.to_s+')'
	end
	
end

class Follow < Action
	def initialize(unit, cible)
		super("Follow",unit)
		@cible = cible
		puts 'Following '+@cible.to_s
	end
	
	def do()
		# TODO : se rapprocher de l'unité cible
		d = dist(@unit.x,@unit.y,@cible.x,@cible.y)
		if d > 5
			# on est trop loin
			m = Move.new(@unit, @cible.x, @cible.y)
			m.do()
		end
	end
	
	def finish?()
		return false
	end
	
	def to_s()
		return 'suivant :'+@cible.to_s
	end
	
end

class FireAt < Action
	def initialize(unit, position)
		super("FireAt",position)
		@position = position
		puts 'Firing at '+@position.to_s
	end
	
	def do()
		# TODO : se rapprocher à portée puis faire feu
	end
	
	def finish?()
		return false
	end
	
	def to_s()
		return 'tirant sur ['+@position.x.to_s+','+@position.y.to_s+']' 
	end
	
end

# Attente en tenant la position
class HoldAt < Action
	
	def initialize(unit)
		super("Hold",unit)
		puts 'Holding here for '+unit.to_s
	end
	
	def do()
		# TODO : faudra ajouter de tirer si une unité passe à portée
	end
	
	def finish?()
		return false
	end
	
	def to_s()
		return 'tient la position ['+@unit.x.to_s+','+@unit.y.to_s+'].'
	end
	
end

# Attente active : note : il faudra changer l'algo de traitement
# des actions : si pas d'action, on fait Wait !
class Wait < Action
	
	def initialize(unit)
		super("Wait",unit)
	end
	
	def do()
		# si on nous attaque, on contre attaque
	end
	
	def finish?()
		return false
	end
	
	def to_s()
		return 'attend.'
	end
	
end

class Build < Action

	#@@map = nil
	
	#def Build.set_map(map)
	#	@@map = map
	#end
	
	def initialize(unit, uclass)
		super("Build",unit)
		@uclass = uclass
		@cpt = 0
		@finish = false
		#if @@map.instance_of?(NilClass)
		#	raise "Build Error : map not initialized"
		#end
	end
	
	def do()
		puts @cpt
	  if @cpt < @uclass::TimeToBuild
			@cpt += 1
	  else
			# faire une nouvelle unitée
			puts "unité construite"
			# Algo
			# Regarder si la place est vide
			x = @unit.x+@unit.class::Sortie[0]
			y = @unit.y+@unit.class::Sortie[1]
			if @unit.map.empty?(x,y)
			# Si oui -> construire l'unité à l'emplacement de sortie
				u = @uclass::new(@unit.player, Position.new(@unit.map,x,y))
				u.angle = 2
				@finish = true
			# Si non -> attendre et afficher un message
			else
				puts "construction impossible"
			end
		end
	end
	
	def finish?()
		return @finish #@cpt > @uclass::TimeToBuild
	end
	
	def to_s()
		return 'construit '+@uclass.to_s+' : '+(@cpt*100/@uclass::TimeToBuild).to_i.to_s+'%'
	end
	
end

#Action passive que font les bâtiments en train d'être construit
class Building < Action

	def initialize(unit)
		super('Building',unit)
	end
	
	# Action passive, on fait rien dans do
	def do()
	end
	
	def to_s()
		return 'En construction : ['+self.unit.build_percent.to_s+'%]'
	end
	
	def finish?()
		return unit.build_percent == 100
	end
	
end

class BuildBat < Action

	#attr_reader :uclass, :position
	
	Classe = nil
	
	def initialize(unit, position, uclass)
		super("BuildBat",unit)
		@position = position
		@uclass = uclass
		@cpt = 0
		@finish = false
		@state = 0
		#puts @uclass
	end
	
	def do()
		if @state == 0
			@neounit = @uclass.new(@unit.player, @position, 0)
			@neounit.addAction(Building.new(@neounit))
			@state = 1
		end
		#print @neounit.udist(@unit), "youpi\n"
		if @neounit.udist(@unit) > 1
			# on est trop loin
			arr = @neounit.nearestPoint(@unit)
			m = Move.new(@unit, arr[0], arr[1])
			m.do()
		else
			#puts @neounit.build_percent
			#puts @neounit.vie
			if @neounit.build_percent < 100
				@neounit.build()
			else
				@finish = true
			end
		end
	end
	
	def finish?()
		return @finish
	end
	
	def to_s()
		return 'construit '+@uclass.to_s+'()' # compteur
	end
	
end

#---------------------------------------------------------------------
# Gestion du coeur du jeu
#---------------------------------------------------------------------

class IA

	def initialize(player)
	end
	
end

class IA_Player < IA
end

# En as-t-on besoin maintenant que on a l'ordre Wait ??
class IA_Unit < IA
end

#
# Un joueur contrôle des unités et est contrôlé soit pas un humain,
# soit par une IA.
#
class Player

	include Loggable
	
	# Attribut en lecture seule
  attr_reader :name, :num, :energie, :metal
  attr_writer :energie, :metal
	
	# Fonction CORE
	# Constructeur
  def initialize(game, name, position, energie=0, metal=0)
    @name = name
    @map = position.map
    @x = position.x
    @y = position.y
		@energie = energie
		@metal = metal
    @units = []
    #@main_group = []	# Pour éviter des IF : faire que main_group = groups[11]
    @groups = Array.new(11, Array.new) # 10 = Main Group
		@game = game
		@num = @game.register(self)
		case @num
			when 0
				@gid = 'player1'
			when 1
				@gid = 'player2'
			else
				raise 'error :'+@num.to_s
		end
		log()
  end
  
	def log(l=@game.glog)
		l.addEntry(@gid+' = Player.new('+@game.getGid()+', "'+@name+'", Position.new('+@map.getGid()+', '+@x.to_s+', '+@y.to_s+'))')
	end
	
  # Gestion des groupes
	# Positionne le groupe principal
  def set_main_group(group)
    #@main_group = group
		@groups[10] = group
	end
  
	# Sélectionne des unités dans une zone donnée
	# Paramètres : 
	#		array(xdeb,ydeb,xfin,yfin) -> zone de sélection
	#		num	-> numéro où sauvegarder le groupe : 0 <= num <= 9
	#		Si num n'est pas précisé, sauvegarde dans le groupe principale.
	# Retour :
	#		Une référence vers le nouveau groupe sélectionné, trié
	# Exception :
	#		Si num ne respecte pas ses limites, une exception d'index out
	#		of bound peut être levé.
	# Gestion des groupes 3.0
	# Action loggée
	def make_group(units, num=11)
		#@game.log.addEntry(@name+' : new group '+num.to_s)
		@game.glog.addEntry(@gid+'.make_group(['+units.join(',')+'],'+num.to_s+')')
		units = @map.array_to_list_of_unit(units, self)
		@groups[num] = []
		#return add_in_group(units, num)
		for u in units
			if not @groups[num].include?(u)
				@groups[num] << u
			end # if
		end # for
		@groups[num].sort!{ |x,y|
			x.type <=> y.type
		}
		return @groups[num]
	end
	
	# Gestion des Groupes 3.0
	# Action loggée
	def make_group_invert(units, num=11)
		@game.glog.addEntry(@gid+'.make_group(['+units.join(',')+'],'+num.to_s+')')
		units = @map.array_to_list_of_unit(units, self)
		#@game.log.addEntry(@name+' : new inverted group '+num.to_s)
		for u in units
			if not @groups[num].include?(u)
				@groups[num] << u
			else
				@groups[num].delete(u)
			end # if
		end # for
		@groups[num].sort!{ |x,y|
			x.type <=> y.type
		}
		return @groups[num]
	end
	
	# Gestion des groupes 3.0
	# Donne un ordre 'order' au groupe 'num'
	# Paramètres : order, num
	# Notes : ne donne l'ordre à l'unité que si elle est compatible
	# Action loggée
	def order_to_group(object, par1=11, par2=nil)
		#puts "j",object,object.class
		if object.instance_of? Array
			#puts "Ho"
			order_to_group_arr(object, par1)
		elsif object.kind_of? Class #Action
			#puts "Eye"
			order_to_group_act(object, par1, par2)
		end
	end
	
	def order_to_group_act(action, num, position)
		if action.instance_of?(Class) #action.instance_of?(BuildBat)
			#g = GroupAction.new(action.class, position, action.class::Classe)
			g = GroupAction.new(action, position)#, action::Classe)
			#@game.glog.addEntry(@gid+'.order_to_group(['+array.join(',')+'], '+num.to_s+')') # A REVOIR
			for u in @groups[num]
				u.setAction(g.make(u))
			end
		end
	end
	
	def order_to_group_arr(array, num=11) #avant order num = groupe (11 = principal)
		x = array[0]
		y = array[1]
		e = @map.unit[x][y]
		if e == 0 or @map.brou[@num][x][y] <= 1
			# Mouvement
			g = GroupAction.new(Move, x, y)
		elsif e.player != self
			# Attaque
			g = GroupAction.new(Attack, e)
		else
			# Follow
			g = GroupAction.new(Follow, e)
		end
		@game.glog.addEntry(@gid+'.order_to_group(['+array.join(',')+'], '+num.to_s+')')
		for u in @groups[num]
			if u.class::ActionOK.include?(g.aclass)
				u.setAction(g.make(u))
			end
		end
	end
	
	#~def add_in_group(units, num=11)
		#~@game.log.addEntry(@name+' : adding to group '+num.to_s)
		#~for u in units
			#~if not @groups[num].include?(u)
				#~@groups[num] << u
			#~end # if
		#~end # for
		#~@groups[num].sort!{ |x,y|
			#~x.type <=> y.type
		#~}
		#~return @groups[num]
	#~end
	
	#~def del_in_group(units, num=11)
		#~@game.log.addEntry(@name+' : deleting into group '+num.to_s)
		#~for u in units
			#~@groups[num].delete(u)
		#~end
		#~if @group[num].length > 0
			#~@groups[num].sort!{ |x,y| 
				#~x.type <=> y.type
			#~}
		#~end
		#~return @groups[num]
	#~end
	
	# Gestion des groupes (1.0)
	# Sauve un groupe et l'associe à un numéro num
  def save_group(group, num)
    @groups[num] = group
  end
  
	# Gestion des groupes
	# Détruit le groupe de numéro num
  def delete_group(num)
    @groups[num] = []
  end
	
	# Gestion des unités
	# Ajoute une unité à un joueur en la créant en indiquant où ?
  #def addUnit(u)#type, position, size=[1,1])
	#	@log.write('['+Time::now+'] '+@name+' : adding unit ')
  #  if @units.length < Game::MAX_UNIT
  #    #u = Unit.new(self, type, position, size)
  #    u.activate()
	#		@units += [u]
  #    return u
  #  else
  #    puts "too many units for that player -> aborting"
  #  end
  #end
  
	# Gestion des unités
	# Retourne le nombre d'unité appartenant au joueur
  def nbUnits()
    return @units.length
  end
  
	# Fonctions utilitaires
	# Retourne une chaîne représentant le joueur
  def to_s()
    return @name + " (" + @units.length.to_s() + ")"
  end
  
	# Fonction CORE
	# Update le joueur ( = le fait jouer)
  def update()
		to_remove = []
    for i in 0..@units.length-1
      @units[i].main()
			if @units[i].vie <= 0
				to_remove << @units[i]
				@units[i].die()
			end
    end
		@units -= to_remove
  end
  
	def register(u)
		if @units.length < Game::MAX_UNIT
      u.activate()
			@units += [u]
      return u
    else
      raise "too many units for player "+self.to_s
    end
	end
	
end

class Unit
	
  attr_reader :vie, :x, :y, :map, :angle, :player, :weapons, :type, :vision, :rapidite #,:size, :actionOK
  attr_writer :angle, :weapons, :vie
  
  #attr_reader :nbUnitTotale
  
  @@nbUnitTotale = 0
	
	ActionOK = [Move, Attack, Follow]
	TimeToBuild = 40
	Name = "Unit"
	Text = "A simple unit."
	Size = [1,1]
	Vision = 90
	VieMax = 100
	
	def get_actions_possibles()
		return self.class::ActionOK
	end
	
	def nearestPoint(u) # 20/12/05 Retourne le point le + proche entre deux unités
		dist = 99999
		xi = -1
		yj = -1
		for i in @x...@x+self.class::Size[0]
			for j in @y...@y+self.class::Size[1]
				if dist(i,j,u.x,u.y) < dist
					dist = dist(i,j,u.x,u.y)
					xi = i
					yj = j
				end
			end
		end
		return [xi,yj]
	end
	
	def udist(u) # 20/12/05 Retourne la distance entre deux unités
		dist = 99999
		for i in @x...@x+self.class::Size[0]
			for j in @y...@y+self.class::Size[1]
				if dist(i,j,u.x,u.y) < dist
					dist = dist(i,j,u.x,u.y)
				end
			end
		end
		return dist
	end
	
  # Constructeur
  def initialize(player, type, position)#, size=[1,1], actionOK=[Move,Attack,Follow])
    @player = player
    @map = position.map
    @x = position.x
    @y = position.y
    @@nbUnitTotale += 1
		#@size = size
    #@map.put(self)
    @vie = self.class::VieMax
    @actions = []
    @angle = 0
    @weapons = []
		@type = type
		#@actionOK = actionOK
		@vision = self.class::Vision
    #if not player.register(self)
    # return false
    #end
		@rapidite = 2#0.17 #1.0 trop lent. 0.50 lent aussi. 0.20 ca va 0.17 0.15 rapide
		#puts @rapidite
		#puts :rapidite
		@player.register(self)
		@cpt = @rapidite
  end
  
	def activate()
		@map.put(self)
	end
	
  def to_s()
    return "Unit of " + @player.name + " (" + @x.to_s() + "," + @y.to_s() + ") - [" + Size[0].to_s + "," + Size[1].to_s + "] ["+self.class::Name+"]" 
  end
  
  # Gestion des actions
  def setAction(a)
    @actions = [a]
  end
  
  def addAction(a)
    @actions << a
  end
  
  def clearActions()
    @actions.clear()
  end
  
	def can_do?(a)
		return self.class::ActionOK.include?(a) #@actionOK.include?(a)
	end
	
	def get_action()
		return @actions[0]
	end
	
  def main()
		if @cpt > 0
			@cpt -= 1
		else
			if @actions.length > 0
				#if @actions[0].instance_of? Move
					@actions[0].do()
					if @actions[0].finish?
						@actions.delete_at(0)
					end
				#end
			end
			@cpt = @rapidite
		end
		if @weapons.length > 0
			@weapons[0].update()
		end
  end
  
  def pos(x,y)
    @map.remove(self)
    @x = x
    @y = y
    @map.put(self)
  end
  
	def die()
		clearActions()
		@map.remove(self)
	end
	
end

class Bat < Unit
	
	attr_reader :build_percent
	
	def initialize(player, type, position, build=100)
		super(player, type, position)
		@build_percent = build
		set_vie()
	end
	
	def get_action_possible()
		if @build_percent < 100
			return []
		else
			return self.class::ActionOK
		end
	end
	
	def build()
		if @build_percent < 100
			@build_percent += (100/self.class::TimeToBuild).to_i
			if @build_percent > 100
				@build_percent = 100
			end
			if @build_percent == 100
				set_default_order
			end
			set_vie()
		end
	end
	
	def set_vie()
		#ovie = vie
		ini = (self.class::VieMax/10).to_i
		@vie =  ini + ((self.class::VieMax-ini)*@build_percent/100).to_i
		#print ini, " : ", ovie, " >> ", @vie, ":", @build_percent, "::", (((self.class::VieMax-ini)/100)*@build_percent), "\n"
		#gets
	end
	
	def set_default_order
		# place here the default order for batiment like generator or extractor
	end
	
	#def main()
	#	puts self.get_action.class.to_s+' '+@build_percent.to_s
	#	super
	#end
	
	#def main()
	#	if @build_percent == 100
	#		super
	#	end
	#end
	
end

class Constructor < Bat

	Sortie = [1,0]	# Emplacement de la sortie des unités construites
									# par défaut en face de soi.
	
end

end
