from map import Layer
from utils import NamedObject, IdObject

#-------------------------------------------------------------------------------
# GAME
#-------------------------------------------------------------------------------
class Game(NamedObject):
    
    def __init__(self, name, mod):
        NamedObject.__init__(self, name)
        self.world = None
        self.zones = {}
        self.players = {}
        self.triggers = {}
        self.elem_types = {}
        self.unit_types = {}
        self.building_types = {}
        self.building_types_ordered = []
        self.is_live = True
        self.mod = mod
    
    def set_name(self, name):
        self.name = name
    
    def set_world(self, game_map):
        self.world = World(self, game_map)

    def set_elem_types(self, elem_types):
        self.elem_types = elem_types

    def set_unit_types(self, unit_types):
        self.unit_types = unit_types
    
    def set_building_types(self, building_types, order):
        self.building_types = building_types
        self.building_types_ordered = order
    
    def create_player(self, name, player_color, *ress):
        print("creating player")
        if name in self.players:
            raise Exception("Already a player with this name")
        self.players[name] = Player(self, name, player_color, ress)

    def create_unit(self, player_name, x, y, unit_types_name):
        sys.stdout.write("creating unit")
        p = self.get_player_by_name(player_name)
        ut = self.get_unit_types_by_name(unit_types_name)
        if not self.world.is_valid(x, y) or not self.world.is_empty(x,y):
            raise Exception("False or not empty coordinates : " + str(x) + ", " + str(y) + " p = " + str(self.world.passable_map[y][x]))
        u = Unit(ut, p, x, y)
        self.world.units.append(u)
        p.units.append(u)
        sys.stdout.write(' :: unit #' + str(u.id) + ' created\n')
        return u.id
        
    def create_building(self, player_name, x, y, building_type_name):
        sys.stdout.write("creating building")
        p = self.get_player_by_name(player_name)
        bt = self.get_building_type_by_name(building_type_name)
        if not self.world.is_valid_zone(x, y, bt.grid_w, bt.grid_h) or not self.world.is_empty_zone(x, y, bt.grid_w, bt.grid_h):
            raise Exception("False or not empty coordinates : " + str(x) + ", " + str(y))
        b = Building(p, bt, x, y)
        self.world.units.append(b) 
        p.buildings.append(b)
        sys.stdout.write(' :: building #' + str(b.id) + ' created\n')
        return b.id
        
    def create_trigger(self, name):
        self.triggers[name] = Trigger(name)
        
    def create_condition(self, ref, kind, *params):
        self.triggers[ref].conditions.append(Condition(kind, params))
    
    def create_action(self, ref, kind, *params):
        self.triggers[ref].actions.append(Action(kind, params))
    
    def create_zone(self, name, x1, y1, x2, y2):
        self.zones[name] = Zone(name, x1, y1, x2, y2)
    
    #def order_move(self, units, x : int, y : int, add : bool):
    def order_move(self, units, x, y, add):
        sys.stdout.write('Move ')
        for u in units:
            sys.stdout.write(str(u) + ' ')
            if add:
                sys.stdout.write('(delayed) ')
                u.add_order(Order('go', x, y))
            else:
                u.order(Order('go', x, y))
        sys.stdout.write('to ' + str(x) + ', ' + str(y) + '\n')
    
    def order_attack(self, units, target, add):
        sys.stdout.write('Attack ')
        for u in units:
            sys.stdout.write(str(u) + ' ')
            if add:
                sys.stdout.write('(delayed) ')
                u.add_order(Order('attack', target=target))
            else:
                u.order(Order('attack', target=target))
        sys.stdout.write('target => ' + str(target) + ' at ' + str(target.x) + ', ' + str(target.y) + '\n')
    
    def get_player_by_name(self, player_name):
        if player_name not in self.players:
            raise Exception("Unknown player : " + player_name)
        return self.players[player_name]

    def get_unit_types_by_name(self, unit_types_name):
        if unit_types_name not in self.unit_types:
            raise Exception("Unknown unit type : " + unit_types_name)
        return self.unit_types[unit_types_name]
        
    def get_building_type_by_name(self, building_type_name):
        if building_type_name not in self.building_types:
            raise Exception("Unknown building type : " + building_type_name)
        return self.building_types[building_type_name]
    
    def get_all_units_in_zone_for_player(self, ref_zone, ref_player):
        p = self.players[ref_player]
        z = self.zones[ref_zone]
        units = []
        for i in range(z.x1, z.x2):
            for j in range(z.y1, z.y2):
                u = self.world.get_unit_at(i, j)
                if u is not None and u.player == p:
                    units.append(u)
        return units
    
    def get_players(self):
        return self.players
    
    #def get_units_by_id(self, ids):
    #    units = []
    #    cpt = 0
    #    for u in self.world.units:
    #        if u.uid in ids:
    #            units.append(u)
    #            cpt += 1
    #    if cpt != len(ids):
    #        raise Exception("ID of unit unknown detected !!!")
    #    return units
    
    def update(self):
        # Triggers and actions
        for key, value in self.triggers.items():
            if value.test_all(self):
                value.do_all(self)
        # Particles
        # self.world.particles.update()
        # Players & units
        for key, value in self.players.items():
            value.update()
        return self.is_live

#-------------------------------------------------------------------------------
# PLAYER
#-------------------------------------------------------------------------------
class Player(NamedObject):
    
    def __init__(self, game, name, army, player_color, ress=(0,0)):
        NamedObject.__init__(self, name)
        self.game = game
        self.world = game.world
        self.color = player_color
        self.units = []
        self.buildings = []
        self.min = ress[0]
        self.sol = ress[1]
        self.victorious = False
        self.fog = Layer("fog", self.world.width, self.world.height, 0)
        self.army = self.game.mod.armies[army]
    
    def update(self):
        # put fog_map
        self.fog.update(2, 1)
        # Update for all units?
        i = 0
        while i < len(self.units):
        #for u in self.units:
            if not self.units[i].update():
                self.world.units.remove(self.units[i])
                del self.units[i]
                print("deleting unit")
                # del u
            i += 1
        for b in self.buildings:
            b.update()

#-------------------------------------------------------------------------------
# WORLD
#-------------------------------------------------------------------------------
class World:
    
    def __init__(self, game, map):
        """
            map has only one layer: "textures". we will had one layer for unit, another for passable
            before, unit layer was (x, y) where x was 1 (here) or -1 (moving here) and y the id
            now unit layer has only id of unit in it. The here/moving here info is in passable layer
        """
        self.game = game
        #self.particles = Particles()
        self.map = map
        self.width = map.width
        self.height = map.height
        self.map.add_layer("unit", 0)
        self.map.add_layer("passable", 0) # can be : 0 : passable, 1 : unit is here (see unit map), 2 : unit u is moving here (see unit map), 10 : impassable
        self.units = []
        self.EMPTY = 0
    
    def get_tex(self, x, y):
        if self.is_valid_at(x, y):
            return self.map.get_at("textures", x, y)
        else:
            return -1
    
    def get_pas(self, x, y):
        if self.is_valid_at(x, y):
            return self.map.get_at("passable", x, y)
        else:
            return 0
    
    def is_valid_at(self, x, y):
        return self.map.is_valid_at(x, y)

    def is_valid_rect(self, x, y, w, h):
        return self.map_is_valid_rect(x, y, w, h)
    
    def is_empty_rect(self, x, y, w, h):
        if self.is_valid_rect(x, y, w, h):
            return self.map.is_equal_rect("passable", x, y, w, h, self.EMPTY)
        else:
            return False
    
    def is_empty_at(self, x, y):
        return self.map.is_equal_at("passable", x, y, self.EMPTY)
    
    def is_unit(self, x, y):
        if self.is_valid_at(x, y):
            return not self.map.is_equal_at("unit", x, y, self.EMPTY)
        else:
            return False
    
    def get_unit_at(self, x, y):
            if self.is_unit(x, y):
                return self.map.get_at("unit", x, y)

#------------------------------------------------------------------------------
# PROFILE
#------------------------------------------------------------------------------
class Profile(NamedObject):
    
    def __init__(self, name: str, life: int, vision: int, width: int = 1, height: int = 1):
        NamedObject.__init__(self, name)
        self.life = life
        self.vision = vision
        self.width = width
        self.height = height

#-------------------------------------------------------------------------------
# ARMY
#-------------------------------------------------------------------------------
class Army(NamedObject):

    def __init__(self, name, profiles):
        NamedObject.__init__(self, name)
        self.profiles = profiles
        
#-------------------------------------------------------------------------------
# MOD
#-------------------------------------------------------------------------------
class Mod(NamedObject):

    def __init__(self, name, armies):
        NamedObject.__init__(self, name)
        self.armies = armies
        self.all_profiles = {}
        for arm in self.armies:
            for pro in self.armies[arm].profiles:
                if pro in self.all_profiles:
                    raise Exception(f"Duplicated Profile {pro}!")
                else:
                    self.all_profiles[pro] = self.armies[arm].profiles[pro]

    def get_profile(self, name):
        if name not in self.all_profiles:
            raise Exception(f"Unknown profile {name}!")
        else:
            return self.all_profiles[name]

#------------------------------------------------------------------------------
# UNIT
#------------------------------------------------------------------------------
class Unit(IdObject):

    def __init__(self, player, x, y, profile, plife):
        IdObject.__init__(self)
        self.player = player
        self.map = player.game.map
        self.x = x
        self.y = y
        self.width = profile.width
        self.height = profile.height
        self.life = int(profile.life * plife)
        self.vision = profile.vision
        self.profile = profile
        self.map.set_rect("ground", self.x, self.y, self.width, self.height, self.id)
        self.map.set_circle_from_rect("fog", self.x, self.y, self.width, self.height, self.vision, 1)

#------------------------------------------------------------------------------
# BUILDING
#------------------------------------------------------------------------------
class Building(Unit):

    def __init__(self, player, x, y, profile, constructed, plife):
        Unit.__init__(self, player, x, y, profile, plife)
        self.constructed = constructed
