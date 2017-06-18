from map import Layer
from utils import NamedObject, IdObject, Pair
import sys

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
        self.building_types = {}
        self.building_types_ordered = []
        self.is_live = True
        self.mod = mod
    
    def set_name(self, name):
        self.name = name
    
    def set_world(self, game_map):
        self.world = World(self, game_map)
        return self.world

    def set_elem_types(self, elem_types):
        self.elem_types = elem_types
    
    def set_building_types(self, building_types, order):
        self.building_types = building_types
        self.building_types_ordered = order
    
    def create_player(self, name: str, army: str, player_color, x, y, *ress):
        print("creating player #" + str(len(self.players)) + " " + name)
        if name in self.players:
            raise Exception("Already a player with this name")
        arm = self.mod.armies[army]
        self.players[name] = Player(self, name, arm, player_color, x, y, ress)
        return self.players[name]

    def create_unit(self, player_name: str, profile: str, x: int, y: int, life: float):
        sys.stdout.write("creating unit")
        p = self.get_player_by_name(player_name)
        t = self.mod.get_profile(profile)
        if not self.world.is_valid_at(x, y) or not self.world.is_empty_at(x,y):
            raise Exception("False or not empty coordinates : " + str(x) + ", " + str(y) + " p = " + str(self.world.passable_map[y][x]))
        u = Unit(p, t, x, y, life)
        self.world.units.append(u)
        p.units.append(u)
        sys.stdout.write(' #' + str(u.id) + ' ' + profile + ' for ' + player_name + '\n')
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
    
    def __init__(self, game, name, army, player_color, x, y, ress=(0,0)):
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
        self.army = army
        self.x = x
        self.y = y
    
    def update(self):
        # put fog_map
        self.fog.update(2, 1)
        # Update for all units?
        i = 0
        while i < len(self.units):
        #for u in self.units:
            if not self.units[i].update():
                del self.units[i]
                print("deleting unit")
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
            now unit layer has only a ref to the unit in it. The here/moving here info is in passable layer
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

    def set_pos(self, u):
        self.map.set_rect("unit", u.x, u.y, u.width, u.height, u)
        self.map.set_rect("passable", u.x, u.y, u.width, u.height, 1)

    def unset_pos(self, u):
        self.map.set_rect("unit", u.x, u.y, u.width, u.height, 0)
        self.map.set_rect("passable", u.x, u.y, u.width, u.height, 0)
        
    def clean(self, u):
        self.unset_pos(u)
        self.units.remove(u)
    
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

    def get_uni(self, x, y):
        if self.is_valid_at(x, y):
            return self.map.get_at("unit", x, y)
        else:
            return 0

    def get_uni_rect(self, x1, y1, x2, y2):
        deb_x = min(x1, x2)
        fin_x = max(x1, x2)
        deb_y = min(y1, y2)
        fin_y = max(y1, y2)
        return self.map.get_rect("unit", deb_x, deb_y, fin_x - deb_x +1, fin_y - deb_y +1)
    
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

    def get_unit_rect(self, x, y, w, h):
        if self.is_valid_rect(x, y, w, h):
            return

#------------------------------------------------------------------------------
# PROFILE
#------------------------------------------------------------------------------
class Profile(NamedObject):
    
    def __init__(self, name: str, life: int, vision: int, _range: int, speed: int, width: int = 1, height: int = 1):
        NamedObject.__init__(self, name)
        self.life = life
        self.vision = vision
        self.width = width
        self.height = height
        self.range = _range
        self.speed = speed

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
# ORDER
#------------------------------------------------------------------------------
class Order:
    
    def __init__(self, kind, x=0, y=0, target=None):
        print("Creating order %s" % (kind,))
        self.x = x
        self.y = y
        self.target = target
        self.kind = kind

#------------------------------------------------------------------------------
# UNIT
#------------------------------------------------------------------------------
class Unit(IdObject):
    
    def __init__(self, player, profile, x, y, plife):
        IdObject.__init__(self)
        self.player = player
        self.world = player.game.world
        
        self.x = x
        self.y = y
        self.real_x = x * 32 + 16
        self.real_y = y * 32 + 16
        
        self.width = profile.width
        self.height = profile.height

        self.life = int(profile.life * plife)
        self.vision = profile.vision
        self.range = profile.range
        self.speed = profile.speed

        self.cpt_move = 0
        self.cpt_fire = 0

        self.profile = profile
        self.world.set_pos(self)
        
        self.orders = []

        # Transitional movement system (TMS)
        self.transition = None
        self.destination = None
        self.previous32 = None
        
    def update(self):
        old_x = self.x
        old_y = self.y
        
        if self.life <= 0:
            self.world.clean(self)
            return False
        
        if len(self.orders) > 0:
            order = self.orders[0]
            if order.kind == 'go':
                res = self.go(order.x, order.y)
                if res:
                    del self.orders[0]
            elif order.kind == 'attack': #UNTESTED
                # check if the unit is not in transit
                if get_dist(self.x, self.y, order.target.x, order.target.y) > self.range or (self.real_x - 16) % 32 != 0 or (self.real_y - 16) % 32 != 0:
                    self.go(order.target.x, order.target.y)
                else:
                    res = self.attack(o.target)
                    if res:
                        del self.orders[0]
        
        return True
    
    def order(self, o):
        self.orders = [o]

    def add_order(self, o):
        self.orders.append(o)

    def go(self, x: int, y: int):
        if self.cpt_move > 0:
            self.cpt_move -= 1
            return False
        else:
            self.cpt_move = self.speed

        self.world.unset_pos(self)
        
        if self.destination is None:
            # 32 en 32
            from_x = self.x
            from_y = self.y
            to_x = x
            to_y = y
            
            n_x = -1
            n_y = -1
            going_x = 0
            going_y = 0
            if to_x > from_x:
                n_x = from_x + 1
                going_x = 1
            elif to_x < from_x:
                n_x = from_x - 1
                going_x = -1
            elif to_x == from_x:
                n_x = from_x
            if to_y > from_y:
                n_y = from_y + 1
                going_y = 1
            elif to_y < from_y:
                n_y = from_y - 1
                going_y = -1
            elif to_y == from_y:
                n_y = from_y

            if not self.world.is_empty_at(n_x, n_y):
                print("blocked!")
                if going_x == 1 and going_y == 1:
                    test = (from_x, n_y, n_x, from_y)
                elif going_x == 1 and going_y == 0:
                    test = (n_x, n_y + 1, n_x, n_y - 1)
                elif going_x == 1 and going_y == -1:
                    test = (from_x, n_y, n_x, from_y)
                elif going_x == 0 and going_y == 1:
                    test = (from_x - 1, n_y, from_x + 1, n_y)
                elif going_x == 0 and going_y == 0:
                    pass  # not a move
                elif going_x == 0 and going_y == -1:
                    test = (from_x - 1, n_y, from_x + 1, n_y)
                elif going_x == -1 and going_y == 1:
                    test = (from_x, n_y, n_x, from_y)
                elif going_x == -1 and going_y == 0:
                    test = (n_x, n_y + 1, n_x, n_y - 1)
                elif going_x == -1 and going_y == -1:
                    test = (from_x, n_y, n_x, from_y)

                if self.world.is_valid_at(test[0], test[1]):
                    if self.world.is_empty_at(test[0], test[1]):
                        #print("trying : " + str(test[0]) + ", " + str(test[1]))
                        n_x = test[0]
                        n_y = test[1]
                    elif self.world.is_empty_at(test[2], test[3]):
                        #print("trying : " + str(test[2]) + ", " + str(test[3]))
                        n_x = test[2]
                        n_y = test[3]
                if n_x == self.old_x and n_y == self.old_y:
                    return True  # no loop !
            
            if self.player.world.is_empty_at(n_x, n_y):
                self.destination = Pair(n_x * 32 + 16, n_y * 32 + 16)
                self.world.set_trace(n_y, n_x, self) # CODE: IN MOVEMENT
        
        if self.destination is not None and self.transition is None:
            self.transition = Pair(self.x * 32 + 16, self.y * 32 + 16)

        if self.transition != self.destination:
            if self.transition.x < self.destination.x:
                self.transition.x += self.speed_step
            elif self.transition.x > self.destination.x:
                self.transition.x -= self.speed_step
            if self.transition.y < self.destination.y:
                self.transition.y += self.speed_step
            elif self.transition.y > self.destination.y:
                self.transition.y -= self.speed_step

        if self.transition is not None:
            self.real_x = self.transition.x
            self.real_y = self.transition.y
        else:
            self.real_x = self.x * 32 + 16
            self.real_y = self.y * 32 + 16

        if self.destination == self.transition and self.destination is not None:
            self.old_x = self.x
            self.old_y = self.y
            self.x = int((self.destination.x - 16) / 32)
            self.y = int((self.destination.y - 16) / 32)
            self.destination = None
            self.transition = None

        self.world.set_pos(self)
        # Fog
        # self.light(self.x, self.y, 1, 1, self.vision)

        #print(self.x, self.y, "tr= ", self.transition, "dst= ", self.destination) # Add details on pathfinding (verbose)
        return self.x == x and self.y == y
    
#------------------------------------------------------------------------------
# BUILDING
#------------------------------------------------------------------------------
class Building(Unit):

    def __init__(self, player, x, y, profile, constructed, plife):
        Unit.__init__(self, player, x, y, profile, plife)
        self.constructed = constructed
