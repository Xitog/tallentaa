#
# Module gérant l'aspect graphique du jeu
#
module Graphic

require "gosu.so"
require "swloe.rb"
require "utils.rb"
include Utils
include Swloe

BLACK = Gosu::Color.new(255,255,255,255)
GREEN = Gosu::Color.new(255,0,255,0)
RED = Gosu::Color.new(255,255,0,0)
BLUE = Gosu::Color.new(255,0,0,255)

#
# Partie GUI
#
class MainWindow < Gosu::Window

	MAX_X = 19
	MAX_Y = 11
	
	def to_images(win, arr, rep="", quiet=true)
		for i in 0..arr.length-1
			if not quiet then puts "Loading : "+rep+arr[i] end
			arr[i] = Gosu::Image.new(self, rep+arr[i], true)
		end
	end
	
	def to_image(win, var, rep="", quiet=true)
		if not quiet then puts "Loading : "+rep+var end
		var = Gosu::Image.new(self, rep+var, true)
	end
	
  #
  # On affiche un jeu pour un joueur précis
  #
  def initialize(game, player)
    @game = game
    @player = player
    @map = game.map
    @group = []
		# Permet de savoir quel sous-groupe on affiche les ordres
    @sous_group_type = nil
		
    @mode_texte = false
    @cmd = ""
    
    @select = false
    @old_pos = [0,0]
    
		# Ordres affichés
		@orders = []
		
    # initialisation
    super(640,480, false, 20)
    @font = Gosu::Font.new(self, "courrier", 20)  # 10 pas mal pour les tous petits trucs
    # titre de la fenétre
    self.caption = "Tutorial Gosu"
    
    #
    # Chargement des fichiers graphiques
    #
    # chargement d'une image
    @image = Gosu::Image.new(self, "graphics/gui/test/red.bmp", true)
    @map_tile = ["red.bmp", "yellow.bmp", "brown.bmp", "green.bmp", "blue.bmp"]
    to_images(self, @map_tile, 'graphics/gui/test/')
    # Les graphismes primaires (version test)
    @map_tile = ["tex_dalle.bmp", "tex_desert.bmp", "tex_desert_x1.bmp", "tex_desert_x2.bmp",
                  "tex_desert_x3.bmp", "tex_desert_x4.bmp", "tex_desert_x5.bmp",
                  "tex_desert_x6.bmp", "tex_herbe.bmp", "tex_herbe_x1.bmp", "tex_herbe_x2.bmp"]
    to_images(self, @map_tile, 'graphics/textures/')
    # Les graphismes du menu
    @menu_tile = ["menu_hg.bmp","menu_h.bmp","menu_hd.bmp","menu_d.bmp","menu_bd.bmp",
                  "menu_b.bmp","menu_bg.bmp","menu_g.bmp","menu_case.bmp",
                  "menu_minimap.bmp","menu_select.bmp"]
    to_images(self, @menu_tile, 'graphics/gui/menu/')
    # Les graphismes de la minimap
    @minimap_tile = ["mini_red.bmp", "mini_yellow.bmp", "mini_brown.bmp", "mini_green.bmp",
                  "mini_blue.bmp", "mini_good.bmp", "mini_bad.bmp"]
    to_images(self, @minimap_tile, 'graphics/gui/minimap/')
    # Les graphismes des ordres dans le menu
		@menu_action = ["menu_action_move.bmp",
										"menu_action_attack.bmp",
										"menu_action_stop.bmp"]
		to_images(self, @menu_action, 'graphics/gui/actions/')
    # Les graphismes des unités
		@units_tile = ["unit.bmp", "unit_select.bmp", "unit_bad.bmp"]
		to_images(self, @units_tile, 'graphics/gui/')
		# Faire toutes les unités
		@units_tile = Array.new(2, Array.new)
		@units_tile[0] = ["u_storm_b.bmp", "u_storm_d.bmp", "u_storm_f.bmp", "u_storm_g.bmp",
											"u_r4d5_b.bmp", "u_r4d5_d.bmp", "u_r4d5_f.bmp", "u_r4d5_g.bmp",
											"u_probe_b.bmp", "u_probe_d.bmp", "u_probe_f.bmp", "u_probe_g.bmp",
											"Bat_Emp_CaserneFermée.bmp", "Bat_Emp_CaserneOuverte.bmp", "Bat_Emp_CaserneOuverte.bmp", "Bat_Emp_CaserneFermée.bmp",
											"Bat_Emp_UsineFermée.bmp", "Bat_Emp_UsineOuverte.bmp", "Bat_Emp_UsineFermée.bmp", "Bat_Emp_UsineOuverte.bmp",
											"Bat_Emp_Generateur.bmp", "Bat_Emp_Generateur.bmp", "Bat_Emp_Generateur.bmp", "Bat_Emp_Generateur.bmp",
											"Bat_Emp_Collecteur.bmp", "Bat_Emp_Collecteur.bmp", "Bat_Emp_Collecteur.bmp", "Bat_Emp_Collecteur.bmp",
											"Radar.bmp","Radar.bmp","Radar.bmp","Radar.bmp",
											"u_scout_b.bmp", "u_scout_d.bmp", "u_scout_f.bmp", "u_scout_g.bmp",
											"u_tank_b.bmp", "u_tank_d.bmp", "u_tank_f.bmp", "u_tank_g.bmp",
											"u_officer_b.bmp", "u_officer_d.bmp", "u_officer_f.bmp", "u_officer_g.bmp",
											"Bat_Emp_SerreFermée.bmp", "Bat_Emp_SerreOuverte.bmp", "Bat_Emp_SerreFermée.bmp", "Bat_Emp_SerreOuverte.bmp",
											"Bat_Emp_ArmurerieFermée.bmp", "Bat_Emp_ArmurerieOuverte.bmp", "Bat_Emp_ArmurerieFermée.bmp", "Bat_Emp_ArmurerieOuverte.bmp",
											"Tourelle.bmp", "Tourelle.bmp", "Tourelle.bmp", "Tourelle.bmp"]
		@units_tile[1] = []
		to_images(self, @units_tile[0], 'graphics/units/')
    # Les graphismes des orientations
    @orientations = ["sens_h.bmp", "sens_d.bmp", "sens_b.bmp", "sens_g.bmp"]
    to_images(self, @orientations, 'graphics/gui/orientations/')
    # Les graphismes des éléments notables sur une carte
    @doodads = ["doodads_roc.bmp", "navette.bmp", "navette_small.bmp"]
    to_images(self, @doodads, 'graphics/doodads/')
    # Les particules élémentaires1
    @particles = ["p_blast.bmp", "p_laser_green.bmp", "p_laser_red.bmp"]
    to_images(self, @particles, 'graphics/effects/')
    # Pour le menu les tiles des unités
		@units_menu = ["Storm.bmp", "R4d5.bmp", "Probe.bmp", "Caserne.bmp", "Usine.bmp", "Generateur.bmp", "Extracteur.bmp", "Radar.bmp", "Scout.bmp", "Tank.bmp", "Officier.bmp", "Centre.bmp", "Armurerie.bmp", "Tourelle.bmp"]
		to_images(self, @units_menu, 'graphics/units_small/')
		# Pour l'ombre des batiments
		s = 'graphics/build_shade/'
		@build_shade = { Tourelle  => Gosu::Image.new(self, s+"32x32.bmp", true),
										 Generateur => Gosu::Image.new(self, s+"32x32.bmp", true),
										 Extracteur => Gosu::Image.new(self, s+"64x64.bmp", true),
										 Caserne => Gosu::Image.new(self, s+"96x96.bmp", true),
										 Usine => Gosu::Image.new(self, s+"96x128.bmp", true),
										 Relais => Gosu::Image.new(self, s+"64x32.bmp", true),
										 Armurerie => Gosu::Image.new(self, s+"64x96.bmp", true),
										 Centre => Gosu::Image.new(self, s+"96x96.bmp", true)
									 }
		
    print "Map : ",@map.to_s,"\n"
    
    @souris = Gosu::Image.new(self, 'graphics/gui/curseur3.bmp', true)
    @selected = Gosu::Image.new(self, 'graphics/gui/selected.bmp', true)
		
		@camera_tile = ['mini_white.bmp']
		to_images(self, @camera_tile, 'graphics/')
		@camera_x = 0
		@camera_y = 0
		
		@brou_tile = ['brou.bmp']
		to_images(self, @brou_tile, 'graphics/')
		
		@active_shade = nil
		@class_to_build = nil
		@active_order = nil # va servir pour tous les ordres passés par le menu
		
		# Son
		#~@s = Gosu::Song.new(self, 'sounds/musics/main.ogg', :stream)
		#~@s.play()
		
		#~@sample = Gosu::Sample.new(self, 'sounds/victory/nihilus.ogg')
		#~@sample.play()
		
  end
  
  #
  # Update le contenu de la fenétre
  #
  def update
	
		# Pour faire bouger la caméra
		if button_down? Gosu::Button::KbRight and @camera_x+MAX_X < @map.x-1
			@camera_x+=1
		elsif button_down? Gosu::Button::KbLeft and @camera_x > 0
			@camera_x-=1
		elsif button_down? Gosu::Button::KbDown and @camera_y+MAX_Y < @map.y-1
			@camera_y+=1
		elsif button_down? Gosu::Button::KbUp and @camera_y > 0
			@camera_y-=1
		end
		#print @camera_x, " to ", @camera_x+MAX_X, " : ", @camera_y, " to ", @camera_y+MAX_Y, "\n"
		
    if not button_down? Gosu::Button::MsLeft
      if @select
        # selection des unites
        # TODO : a faire .... ;-)
        old_pos_x = (@old_pos[0] / 32).to_i
        old_pos_y = (@old_pos[1] / 32).to_i
        mouse_x = ((self.mouse_x) / 32).to_i
        mouse_y = ((self.mouse_y) / 32).to_i
				# Scrolling
				mouse_x += @camera_x
				mouse_y += @camera_y
				if mouse_y >= @map.y
					mouse_y = @map.y-1
				end
				if mouse_x >= @map.x
					mouse_x = @map.x-1
				end
        deb_x = max(0, min( old_pos_x, mouse_x))
        deb_y = max(0, min( old_pos_y, mouse_y))
        fin_x = min(@map.x-1, max( old_pos_x, mouse_x))
        fin_y = min(@map.y-1, max( old_pos_y, mouse_y))
        puts "Selecting from #{deb_x},#{deb_y} to #{fin_x},#{fin_y}"

				#ulist = @map.array_to_list_of_unit([deb_x,deb_y,fin_x,fin_y], @player)
				array = [deb_x,deb_y,fin_x,fin_y]
				if not button_down? Gosu::Button::KbLeftControl and not button_down? Gosu::Button::KbRightControl
					#@group = @player.make_group(ulist)
					@group = @player.make_group(array)
				else
					#@group = @player.make_group_invert(ulist)
					@group = @player.make_group_invert(array)
				end
				
				puts "Selected : "+@group.length.to_s+" units"
				if @group.length > 0
					@sous_group_type = @group[0].class#.type
					@orders = @group[0].get_actions_possibles() #@sous_group_type::ActionOK
					#puts "Sous groupe : " + @sous_group_type.to_s
					#puts "Ordre : " + @orders.to_s
        else
					@sous_group_type = nil
					@orders = [] #.clear LOL : les tableaux : only référence, pas de copie par valeur !!
				end
				#@player.set_main_group(@group)
      end
      @select = false
    end
    
		#puts @game.turnElapsed
		#puts @game.timeElapsed
    @game.update()
  end
  
  #
  # Pour dessiner la fenétre principale
  #
  def draw
    #puts "draw"
    #@image.draw(0,0,0) LOL 17h29 16/12/05 : Je commente cette ligne qui est lé depuis le début du projet !!
    for i in @camera_x..@camera_x+MAX_X
			scroll_i = (i-@camera_x)*32
      for j in @camera_y..@camera_y+MAX_Y
        #@map_tile[rand(5)].draw(i*32,j*32,0)  # de 0 é 4
        #print i,",",j,",",@map.get[i][j],"\n"
        #print i,",",j,",",@gmap.get[i][j],"#"
        #print @map.get[i][j],"/"
        
				scroll_j = (j-@camera_y)*32
				
        # La base
				if @map.brou[@player.num][i][j] != 0
					if @map.brou[@player.num][i][j] != 1
						@map_tile[@map.map[i][j]].draw(scroll_i,scroll_j,0)
					else
						@map_tile[@map.map[i][j]].draw(scroll_i,scroll_j,0)
						@brou_tile[0].draw(scroll_i,scroll_j,0,1,1,Gosu::Color.new(100,0,0,0))
					end
        end
				
        # Doodads
        d = @map.doodads.something_at?(i,j)
        if not d.instance_of? NilClass
          #puts d.size_y
					if not d.visible # s'il n'est pas visible
						d.visible?(@player) # on demande s'il est visible
					end
					if d.visible # s'il est visible on l'affiche
						@doodads[d.dessin].draw(scroll_i,scroll_j+(1-d.size_y)*32,1) # (j+1-d.size_y)*32
					end
				end
        
				# TODO : Code pour afficher l'ouverture des usines quand on a construit
        # Unités
				u = @map.unit[i][j]
        if (u != 0 and @map.brou[@player.num][i][j] > 1)
          if u.player == @player
            if @group.include?(u)
							@selected.draw(scroll_i,scroll_j,0)
						end
						@units_tile[0][u.type*4+u.angle].draw((u.x-@camera_x)*32,(u.y-@camera_y)*32,0)
          else
						@units_tile[0][u.type*4+u.angle].draw((u.x-@camera_x)*32,(u.y-@camera_y)*32,0)
					end
          @orientations[u.angle].draw(scroll_i,scroll_j,0)
        end
				
      end
    end
    #puts "\nend draw"
    #gets
    #puts @mouse_x
    #puts @mouse_y
    a = (self.mouse_x / 32).to_i
    b = (self.mouse_y / 32).to_i
    if not @select
      self.caption = " #{self.mouse_x} / #{self.mouse_y} - #{a} / #{b}"
    else
      c = (@old_pos[0] /32).to_i
      d = (@old_pos[1] /32).to_i
      self.caption = " #{self.mouse_x} / #{self.mouse_y} - #{a} / #{b} - old : #{c} - #{d}"
    end
    draw_particles()
    draw_menu()
    draw_minimap()
    if @group.length > 0
      draw_group()
    else
			@font.draw('Energie : '+@player.energie.to_s, 32*4, 32*(MAX_Y+2), 32, 1, 1, Gosu::Color.new(255,0,128,128))
			@font.draw('Métal   : '+@player.metal.to_s, 32*4, 32*(MAX_Y+3), 32, 1, 1, Gosu::Color.new(255,0,128,128))
		end
		if @game.paused?
			# Faire un truc grisé
			c = Gosu::Color.new(128,128,128,128) # avant 100
			draw_quad(0, 0, c, 640, 0, c, 0, 480, c, 640, 480, c, z=64)
		end
		# Gestion de la souris et de l'ordre en cours
    @souris.draw(self.mouse_x, self.mouse_y, 2)
		if @active_shade != nil and self.mouse_y < (MAX_Y+1)*32
			if @map.empty?((self.mouse_x/32).to_i-@camera_x,(self.mouse_y/32).to_i-@camera_y,@class_to_build::Size[0],@class_to_build::Size[1]) and
			not @map.brou?(@player,(self.mouse_x/32).to_i-@camera_x,(self.mouse_y/32).to_i-@camera_y,@class_to_build::Size[0],@class_to_build::Size[1])
				@active_shade.draw((self.mouse_x/32).to_i*32, (self.mouse_y/32).to_i*32, 1, 1, 1, Gosu::Color.new(100,0,100,0))
			else
				@active_shade.draw((self.mouse_x/32).to_i*32, (self.mouse_y/32).to_i*32, 1, 1, 1, Gosu::Color.new(100,200,0,0))
			end
		end
    if @select
      g = Gosu::Color.new(100,0,255,0)
      #                                       si ici y = fun
      draw_quad(@old_pos[0]-(@camera_x*32), @old_pos[1]-(@camera_y)*32, g, self.mouse_x, @old_pos[1]-(@camera_y)*32, g, @old_pos[0]-(@camera_x)*32, self.mouse_y, g, self.mouse_x, self.mouse_y, g, 32)
    end
    if @mode_texte
      @font.draw('['+@player.name+'] '+@cmd, 32*4, 32*(MAX_Y+2), 32, 1, 1, Gosu::Color.new(255, 0, 128, 128))
    end
  end
  
  # Priorité : 3 -> Particules, 2 -> Doodads, 0 -> sol 1 -> units ??
  def draw_particles()
    p = @game.particlesEngine.p
    for i in 0..p.length-1
      # dessin des particules
			@particles[p[i].typep].draw_rot(p[i].x-(@camera_x*32), p[i].y-(@camera_y*32), 3, p[i].angle)
		end
  end
  
  #
  # Pour dessiner le menu
  #
  def draw_menu()
    for i in 0..MAX_X
      @menu_tile[1].draw(i*32, 32*(MAX_Y+1), 0)
    end
    for i in 0..MAX_X
      @menu_tile[5].draw(i*32, 32*(MAX_Y+3), 0)
    end
    @menu_tile[3].draw(32*(MAX_X), 32*(MAX_Y+2), 0)
    @menu_tile[7].draw(0, 32*(MAX_Y+2), 0)
    @menu_tile[0].draw(0, 32*(MAX_Y+1), 0)
    @menu_tile[2].draw(32*(MAX_X), 32*(MAX_Y+1), 0)
    @menu_tile[4].draw(32*(MAX_X), 32*(MAX_Y+3), 0)
    @menu_tile[6].draw(0, 32*(MAX_Y+3), 0)
    for i in 0..2
      for j in 0..2
        @menu_tile[8].draw(i*32, (j+MAX_Y+1)*32, 0)
        if self.mouse_x >= i*32 and self.mouse_x < (i+1)*32 and
          self.mouse_y >= (j+MAX_Y+1)*32 and self.mouse_y < (j+MAX_Y+2)*32
          @menu_tile[10].draw(i*32, (j+MAX_Y+1)*32,0)
        end
      end
    end
    @menu_tile[9].draw(32*(MAX_X-2), 32*(MAX_Y+1), 0)
		
		# Les ordres
		x = 0
		y = (MAX_Y+1)*32
		for i in @orders
			if i == Move
				@menu_action[0].draw(x, y, 1)
			elsif i == Attack
				@menu_action[1].draw(x, y, 1)
			elsif i == Follow
				@menu_action[2].draw(x, y, 1)
			elsif i == BuildScoutTrooper
				@units_menu[Unit::SCOUTTROOPER].draw(x, y, 1)
			elsif i == BuildStormTrooper
				@units_menu[Unit::STORMTROOPER].draw(x, y, 1)
			elsif i == BuildOfficer
				@units_menu[Unit::OFFICIER].draw(x, y, 1)
			elsif i == BuildTank
				@units_menu[Unit::TANK].draw(x, y, 1)
			elsif i == HoldAt
				nil
			elsif i == FireAt
				nil
			elsif i == BuildGenerateur
				@units_menu[Unit::Generateur].draw(x, y, 1)
			elsif i == BuildExtracteur
				@units_menu[Unit::Extracteur].draw(x, y, 1)
			elsif i == BuildCaserne
				@units_menu[Unit::Caserne].draw(x, y, 1)
			elsif i == BuildUsine
				@units_menu[Unit::Usine].draw(x, y, 1)
			elsif i == BuildRelais
				@units_menu[Unit::Relais].draw(x, y, 1)
			elsif i == BuildArmurerie
				@units_menu[Unit::Armurerie].draw(x, y, 1)
			elsif i == BuildTourelle
				@units_menu[Unit::Tourelle].draw(x, y, 1)
			elsif i == BuildCentre
				@units_menu[Unit::Centre].draw(x, y, 1)
			else
				raise "Order Unknown"
			end
			if x == 64 then x = 0; y += 32 else x += 32 end
			if y > (MAX_Y+4)*32 then raise "Too many orders" end
		end
  end
  
  #
  # Pour dessiner la minicarte
  #
  def draw_minimap() # Faire des ronds mini pour les units ??
    for i in 0..@map.x-1 # MAX_X
      for j in 0..@map.y-1 # MAX_Y
				
				# Dessin d'un carré pour la caméra
				if i == @camera_x and j >= @camera_y and j < @camera_y+MAX_Y
					@camera_tile[0].draw(i*2+(MAX_X-2)*32,j*2+(MAX_Y+1)*32,2)
					@camera_tile[0].draw(i*2+(MAX_X-2)*32,j*2+(MAX_Y+1)*32+1,2)
				elsif i == @camera_x+MAX_X and j >= @camera_y and j < @camera_y+MAX_Y
					@camera_tile[0].draw(i*2+(MAX_X-2)*32,j*2+(MAX_Y+1)*32,2)
					@camera_tile[0].draw(i*2+(MAX_X-2)*32,j*2+(MAX_Y+1)*32+1,2)
				end
				if j == @camera_y and i >= @camera_x and i < @camera_x+MAX_X
					@camera_tile[0].draw(i*2+(MAX_X-2)*32,j*2+(MAX_Y+1)*32,2)
					@camera_tile[0].draw(i*2+(MAX_X-2)*32+1,j*2+(MAX_Y+1)*32,2)
				elsif j == @camera_y+MAX_Y and i >= @camera_x and i < @camera_x+MAX_X
					@camera_tile[0].draw(i*2+(MAX_X-2)*32,j*2+(MAX_Y+1)*32,2)
					@camera_tile[0].draw(i*2+(MAX_X-2)*32+1,j*2+(MAX_Y+1)*32,2)
				end
				# bord droit en bas du cadre caméra
				@camera_tile[0].draw((@camera_x+MAX_X)*2+(MAX_X-2)*32, (@camera_y+MAX_Y)*2+(MAX_Y+1)*32, 2)
				
				if @map.brou[@player.num][i][j] != 0 # brou
				
					#@minimap_tile[@map.map[i][j]].draw(i+(MAX_X-2)*32,j+(MAX_Y+1)*32,0)
					@minimap_tile[@map.map[i][j]].draw(i*2+(MAX_X-2)*32,j*2+(MAX_Y+1)*32,0)
					@minimap_tile[@map.map[i][j]].draw(i*2+(MAX_X-2)*32+1,j*2+(MAX_Y+1)*32,0)
					@minimap_tile[@map.map[i][j]].draw(i*2+(MAX_X-2)*32,j*2+(MAX_Y+1)*32+1,0)
					@minimap_tile[@map.map[i][j]].draw(i*2+(MAX_X-2)*32+1,j*2+(MAX_Y+1)*32+1,0)
        
					if @map.unit[i][j] != 0
						if @map.unit[i][j].player == @player
						# les gentils
							@minimap_tile[5].draw(i*2+(MAX_X-2)*32,j*2+(MAX_Y+1)*32,0)
							@minimap_tile[5].draw(i*2+(MAX_X-2)*32+1,j*2+(MAX_Y+1)*32,0)
							@minimap_tile[5].draw(i*2+(MAX_X-2)*32,j*2+(MAX_Y+1)*32+1,0)
							@minimap_tile[5].draw(i*2+(MAX_X-2)*32+1,j*2+(MAX_Y+1)*32+1,0)
						else
						# les méchants
							@minimap_tile[6].draw(i*2+(MAX_X-2)*32,j*2+(MAX_Y+1)*32,0)
							@minimap_tile[6].draw(i*2+(MAX_X-2)*32+1,j*2+(MAX_Y+1)*32,0)
							@minimap_tile[6].draw(i*2+(MAX_X-2)*32,j*2+(MAX_Y+1)*32+1,0)
							@minimap_tile[6].draw(i*2+(MAX_X-2)*32+1,j*2+(MAX_Y+1)*32+1,0)
						end
					end
				end
				
			end
		end
  end
  
  #
  # Dessine une ligne d'une couleur é une profondeur donnée
  #
  def draw_line(x1, y1, x2, y2, color, size=1, z=0)
    draw_quad(x1,y1,color,x1,y1+size,color,x2+size,y2,color,x2+size,y2+size,color, z)
  end
  
	def draw_rect(x1, y1, x2, y2, color, size=1, full=false, z=0)
		if full
			draw_quad(x1,y1,color,x1,y2,color,x2,y1,color,x2,y2,color, z)
		else
			puts x1.to_s + "," + y1.to_s + " " + x2.to_s + "," + y2.to_s
			draw_line(x1,y1,x1,y2,color,size)
			draw_line(x1,y2,x2,y2,color,size)
			draw_line(x2,y2,x2,y1,color,size)
			draw_line(x2,y1,x1,y1,color,size)
		end
	end
	
  #
  # Dessine le groupe sélectionné
  #
  def draw_group()
    for i in 0..@group.length-1
			@units_menu[@group[i].type].draw((i+4)*32,(MAX_Y+1)*32,0)
			#print @group[i].vie, @group[i].class::VieMax, "\n"
      x = (i+4)*32+((30.0/100.0)*((@group[i].vie*100/@group[i].class::VieMax).to_i));
      draw_line((i+4)*32+1, (MAX_Y+2)*32, x, (MAX_Y+2)*32, RED, 3, 10)
    end
		if @group.length == 1
			#if @group[0].kind_of?(Bat) and @group[0].build_percent < 100
			#	@font.draw(@group[0].class::Name+' ['+@group[0].build_percent.to_s+'%] :', 32*4, 32*(MAX_Y+2)+6, 32, 1, 1, Gosu::Color.new(255, 0, 128, 128))
			#else
				@font.draw(@group[0].class::Name+' :', 32*4, 32*(MAX_Y+2)+6, 32, 1, 1, Gosu::Color.new(255, 0, 128, 128))
			#end
			@font.draw(@group[0].class::Text, 32*4, 32*(MAX_Y+3), 32, 1, 1, Gosu::Color.new(255, 0, 128, 128))
			a = @group[0].get_action()
			if not a.instance_of?(NilClass)
				@font.draw(a.to_s, 32*6, 32*(MAX_Y+1)+12, 32, 1, 1, Gosu::Color.new(255,255,255,0))
			end
		end
  end
  
	#def closeRequest
	#	puts "cl"
	#end
	
	def close
		#t = Time.at(@game.timeElapsed())
		#puts t
		#puts t.strftime("%H:%M:%S")
		t = @game.timeElapsed()
		puts t
		h = (t/3600).to_i
		m = ((t-(h*3600))/60).to_i
		s = (t-(h*3600)-(m*60)).to_i
		printf("%02d:%02d:%02d\n",h,m,s)
		puts @game.turnElapsed()
		@game.terminate
		super
	end
	
  #
  # Gére les boutons et la souris
  #
  def button_down(id)
    
		# Pour quitter le jeu de faéon propre
    if id == Gosu::Button::KbEscape
      close
    end
		
		if button_id_to_char(id) == 'p'
			if @game.paused?
				@game.resume
			else
				@game.pause
			end
		end
		
		# Interactions avec la zone de jeu
		if self.mouse_y < (MAX_Y+1)*32 and self.mouse_x < (MAX_X+1)*32
			# On appuie sur la sélection
			if id == Gosu::Button::MsLeft
				if @active_shade == nil
					@select = true
					@old_pos = [self.mouse_x+(@camera_x*32), self.mouse_y+(@camera_y*32)]
					#print ">>> : ",self.mouse_x+(@camera_x*32),":",self.mouse_y+(@camera_y*32),"\n"
				else
					# Ordre de construction
					if @map.empty?((self.mouse_x/32).to_i-@camera_x,(self.mouse_y/32).to_i-@camera_y,@class_to_build::Size[0],@class_to_build::Size[1])
						# Construire : passer l'ordre é l'unité
						@active_shade = nil
						@class_to_build = nil
						@player.order_to_group(@active_order, 11, Position.new(@map,(self.mouse_x/32).to_i-@camera_x,(self.mouse_y/32).to_i-@camera_y))
						@active_order = nil # A FINIR
					else
						puts "Place not empty"
					end
				end
			end
			# Passage d'ordre
			if id == Gosu::Button::MsRight
				if @active_shade == nil
					x = (self.mouse_x/32).to_i+@camera_x
					y = (self.mouse_y/32).to_i+@camera_y
					@player.order_to_group([x,y,x,y])  
				else
					@active_shade = nil
					@class_to_build = nil
					@active_order = nil
				end
			end
		# Interactions avec le menu
		elsif self.mouse_x < 96
			x = (self.mouse_x/32).to_i
			y = ((self.mouse_y - (MAX_Y+1)*32)/32).to_i
			puts "Click Menu : "+x.to_s+"-"+y.to_s
			o = @orders[x+y*3]
			if not o.instance_of?(NilClass)
				if o.superclass == Build
					for u in @group
						if u.instance_of?(@sous_group_type)
							u.addAction(o.new(u))
						end
					end
				elsif o.superclass == BuildBat
					@active_shade = @build_shade[o::Classe]
					@class_to_build = o::Classe
					@active_order = o
				end
			end
		end
		
    if id == Gosu::Button::KbReturn
      puts "Enter"
      if not @mode_texte
        puts "mode texte on"
	      @mode_texte = true
	      @cmd = ""
      else
        puts "mode texte off"
	      @mode_texte = false
	      puts "texte = "+@cmd
				begin
					eval(@cmd)	# dangereux...
				rescue
					puts "Command error"
				end
      end
    else 
      if @mode_texte
        #puts "a key has been entered"
        a = button_id_to_char(id)
        if a.instance_of? String        # TODO: ne pas ajouter si a == nil -> erreur
    			if button_down? Gosu::Button::KbLeftShift
						a.capitalize!
						if a == ';'
							a = '.'
						elsif a == '&'
							a = '1'
						elsif a == 'é'
							a = '2'
						elsif a == '"'
							a = '3'
						elsif a == "'"
							a = '4'
						elsif a == '('
							a = '5'
						elsif a == '-'
							a = '6'
						elsif a == 'é'
							a = '7'
						elsif a == '_'
							a = '8'
						elsif a == 'é'
							a = '9'
						elsif a == 'é'
							a = '0'
						elsif a == ')'
							a = 'é'
						elsif a == '='
							a = '+'
						elsif a == '*'
							a = 'é'
						end
					end
					@cmd << a
        else
					if button_down? Gosu::Button::KbBackSpace
						@cmd.chop! #.delete_at(@cmd.size-1) 
					end
				end
      end
    end
    
  end
  
end

end