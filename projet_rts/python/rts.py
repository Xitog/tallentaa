#-----------------------------------------------------------------------
# Core : Global Constants & Variables
#-----------------------------------------------------------------------

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
      
CAM_MAX_COL = 20 # = 640 / 32
CAM_MAX_ROW = 15 # = 480 / 32
SCROLLING_ZONE = 10

MAP_MAX_COL = 32
MAP_MAX_ROW = 32
      
ENERGY_INCREASE_BY_TURN = 20
MATTER_INCREASE_BY_TURN = 10
      
MAPS = {}
UNIT_DEFINITIONS = {}
# name
# vision
# speed
# width
# height
# mod_x
# mod_y
# order_start_row_mod
# order_start_col_mod
# creation_time
# available_orders
# life
# regen_life
# shield
# regen_shield
# mana
# regen_mana
# armor
# cost.energy
# cost.matter
# weapon (range, dommage, kind)
# reload
# shadow
# is_aerial
# is_movable
# is_building
# is_builder
# is_creator
# is_producer
WEAPON_DEFINITIONS = {}
# name      : str
# range     : int
# dommage   : int
# kind      : str
IDUnit = 0
MAXGroup = 10

#-----------------------------------------------------------------------
# Core : Data model
#-----------------------------------------------------------------------
   
class Map:

    def __init__(self, name, width, height):
        self.name = name
        self.content = [[]]
        self.passable = passable
        #self.doodads = []
        self.width = width
        self.height = height
        self.triggers = []
    
    @staticmethod
    def load_map(dic):
        "Load a map from a JSON dict"
        if "name" in dic:
            name = dic["name"]
        else:
            raise Exception("Incorrect map format: no name provided")
        if "content" in dic:
            content = dic["content"]
        else:
            raise Exception("Incorrect map format: no content provided")
        if "height" in dic:
            height = dic["height"]
            if height != content.length:
                raise Exception("Incoherent number of rows: " + height + " declared vs " + content.length)
            elif height == 0:
                raise Exception("Empty map with 0 height")
        else:
            raise Exception("Incorrect map format: no height provided")
        if "width" in dic:
            width = dic["width"]
            if width != content[0].length:
                raise Exception("Incoherent number of columns: " + width + " declared vs " + content[0].length)
            elif width == 0:
                raise Exception("Empty map with 0 width")
        else:
            raise Exception("Incorrect map format: no width provided")
        if "triggers" in dic:
          triggers = dic["triggers"]
          triggers_oo = []
          conditions = []
          actions = []
          for c in triggers['conditions']:
            if c[0] === 'ControlUnits':
                conditions.append(new ControlUnits(c[0], c[1], c[2], c[3], c[4], c[5]));
            else:
                raise Exception("Unknown condition : " + c[0])
          for a in triggers['actions']:
            if a[0] === 'Victory':
                actions.append(new Victory(a[0], a[1], a[2]));
            else:
                raise Exception("Unknown action :" + a[0])
          triggers_oo.append(new Trigger(conditions, actions));
        else:
            raise("Incorrect map format: no triggers provided")
        res = make_transition(content)
        return Map(name, res[0], res[1], width, height, triggers_oo);


class Trigger:

    def __init__(self, conditions=[], actions=[]):
        self.conditions = conditions
        self.actions = actions
        self.done = False
        
    def test(self, game):
        for c in self.conditions:
            if !c.test(game):
                return False
        return True
        
    def act(self, game):
        this.done = true;
        for a in self.actions:
            a.act(game)


class Condition:

    def __init__(self, code):
        self.code = code

    def test(game):
        return False
                        
    EQUAL = 1
    GREATER_THAN = 2
    LESSER_THAN = 3
    GREATER_OR_EQUAL = 4
    LESSER_OR_EQUAL = 5
    ANY = 0
    ANYWHERE = 0


class Action:

    def __init__(self, code):
        self.code = code

    def act(game):
        pass


class ControlUnits(Condition):

    def __init__(self, code, cmp, type, player, nb, area) {
        super(Condition, self).__init__(code)
        self.cmp = cmp
        self.type = type
        self.player = player
        self.nb = nb
        self.area = area
        
    def test(game):
        count = 0
        if self.cmp === Condition.GREATER_OR_EQUAL:
            if this.area !== Condition.ANYWHERE:
                for row = self.area[1]; row <= self.area[3]; row++:
                    for col = self.area[0]; col <= this.area[2]; col++) {
                        if game.units[row][col] != 0:
                            if self.player === Condition.ANY:
                               if self.type === Condition.ANY:
                                    count += 1
            return (count >= this.nb)


class Victory(Action):

    def __init__(self, code, message, next_map):
        super(Action, self).__init__(code)
        self.message = message
        self.next_map = next_map
        
    def act(game):
        print(self.message)
        game.load_map(MAPS[self.next_map])


class Order:
    pass


class Move(Order):

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.gid = 'Move'
      
class Attack(Order):

    def __init__(self, target):
        self.target = target
        self.gid = 'Attack'

class CreateOrder(Order):
    pass

class CreateSoldier(CreateOrder):

    def __init__(self):
          self.creation = 'soldier'
          self.gid = 'CreateSoldier'

class CreateScout(CreateOrder):

    def __init__(self):
          self.creation = 'scout'
          self.gid = 'CreateScout'

class CreateBuilder(CreateOrder):

    def __init__(self):
          self.creation = 'builder'
          self.gid = 'CreateBuilder'

class Unit:

    def __init__(self, player, kind, row, col, life=100.0):
        global IDUnit
        self.player = player
        IDUnit += 1;
        self.id = IDUnit
        print('creating unit', self.id, 'at', row, col)
        self.kind = kind
        if self.kind not in UNIT_DEFINITIONS:
            raise Exception("Unknown type for Unit")
        self.row = row
        self.col = col
        self.orders = []
        self.width = UNIT_DEFINITIONS[self.type]['width']
        self.height = UNIT_DEFINITIONS[self.type]['height']
        # modifier for drawing
        self.mod_x = UNIT_DEFINITIONS[self.type]['mod_x']
        self.mod_y = UNIT_DEFINITIONS[self.type]['mod_y']
        # modifier for order
        self.order_start_row_mod = 0
        self.order_start_col_mod = 0
        self.speed = UNIT_DEFINITIONS[self.type]['speed']
        self.life = UNIT_DEFINITIONS[self.type]['max_life']
        self.available_orders = UNIT_DEFINITIONS[self.type]['available_orders']
        if self.kind in UNIT_DEFINITIONS['buildings']:
            self.order_start_row_mod = UNIT_DEFINITIONS[self.type]['order_start_row_mod']
            self.order_start_col_mod = UNIT_DEFINITIONS[self.type]['order_start_col_mod']
            self.creation_counter = -1;
        self.speed_counter = self.speed;
        for row in range(self.row, self.row + self.height):
            for col in range(self.col, self.col + this.width):
                self.player.game.units[row][col] = self
        self.player.game.all_units.append(self)
    
    def __str__(self):
        return f"{self.kind} #{self.id} @({self.row}, {self.col})"
    
    def menu_order(row, col):
        pass

    def order(o, add):
        if (!add):
            self.orders.clear()
        self.orders.append(o)
        
    def move(o): #HERE
          let new_row = this.row;
          let new_col = this.col;
          console.log('I am unit', this.id, 'and I am moving');
          if (o.row > this.row) {
            new_row += 1;
          } else if (o.row < this.row) {
            new_row -= 1;
          }
          if (o.col > this.col) {
            new_col += 1;
          } else if (o.col < this.col) {
            new_col -= 1;
          }
          if (game.units[new_row][new_col] != 0 || !game.pass[new_row][new_col]) {
            if (game.units[new_row][this.col] == 0 && game.pass[new_row][this.col]) {
              new_col = this.col;
            } else if (game.units[this.row][new_col] == 0 && game.pass[this.row][new_col]) {
              new_row = this.row;
            }
          }
          if (game.units[new_row][new_col] == 0 && game.pass[new_row][new_col]) {
            console.log('cleaning', this.row, this.col);
            game.units[this.row][this.col] = 0;
            this.row = new_row;
            this.col = new_col;
            game.units[this.row][this.col] = this;
            console.log('setting', this.id, 'at', this.row, this.col);
            if (o.row == this.row && o.col == this.col) {
              this.orders.shift();
            }
            this.speed_counter = this.speed;
          }
        }
        
        update() {
          if (this.speed_counter == 0 && this.orders.length > 0) {
            let o = this.orders[0];
            if (o instanceof Move) {
              this.move(o);
            }
          } else if (this.speed_counter > 0) {
            this.speed_counter -= 1;
          }
          //console.log(this.life);
        }
      }
      
      //in game : ressources[][] = {} (entre 1=10 et 0.1=1)

class Group:

    def __init__(self, player):
        self.content = []
        self.is_building = False
        self.is_friendly = False
        self.player = player
        self.index = 0

    def __len__(self):
        return len(self.content)

    def first(self):
        if len(self.content) > 0:
            return self.content[0]
        else:
            raise Exception("Group empty")

    def copy(self):
        g = Group(self.player)
        g.content = self.content.copy()
        g.is_building = self.is_building
        g.is_friendly = self.is_friendly
        return g
    
    def __contains__(self, u):
        return u in self.content

    def __getitem__(self, i):
        return self.content[i]

    def clear(self):
        self.content = []
        self.is_building = False
        self.is_friendly = False
    
    def append(self, u, adding):
        if MAXGroup is None or len(self.content) < MAXGroup:
            # add an unit to a group
            # if adding is true, the unit is added if the rules are respected
            # if adding is false, the group is cleared and the unit is added
            if not adding:
                self.content = []
            if self.content.length > 0:
                # rules
                # if we are building, we only add if u is building, of same type, of our player
                if this.is_building && u instanceof Building && this.content[0].type == u.type && u.player == this.player:
                    this.content.push(u);
                # if we are not building, we only add if u is not a building, of our player, and we are a friendly group
                elif !this.is_building && !(u instanceof Building) && u.player == this.player && this.is_friendly:
                    this.content.push(u)
            else:
                self.is_friendly = (self.player == u.player)
                self.is_building = (u is Building)
                self.content.append(u)


class Building(Unit):
    pass


      class Turret extends Building {
        
        update() {
          if (this.speed_counter == 0 && this.orders.length > 0) {
            let o = this.orders[0];
            if (o instanceof Attack) {
              this.attack(o.target);
            } else {
              throw 'Incorrect order for Turret';
            }
            this.speed_counter = this.speed;
          }
          if (this.speed_counter > 0) {
            this.speed_counter -= 1;
          }
          if (this.orders.length == 0) {
            // detect enemy. if there is someone give an order of attack.
            for (let row = this.row - this.range; row < this.row + this.range; row++) {
              for (let col = this.col - this.range; col < this.col + this.range; col++) {
                if (row > 0 && col > 0 && row < MAP_MAX_ROW && col < MAP_MAX_COL) {
                  let u = this.player.game.units[row][col];
                  if (u.player != this.player) {
                    this.order(new Attack(u));
                  }
                }
              }
            }
          }
        }
      }
      
      class UnitCreator extends Building {
        
        constructor(player, type, row, col) {
          super(player, type, row, col);
          this.creation_orders = [];
        }
        
        menu_order(row, col) {
          if (this.type == 'barrack') {
            if (row == 1 && col == 0) {
              this.player.energy -= UNIT_DEFINITIONS['soldier']['cost']['energy'];
              this.player.matter -= UNIT_DEFINITIONS['soldier']['cost']['matter'];
              this.order(new CreateSoldier(), true);
            }
          }
        }
        
        order(o, add) {
          if (o instanceof CreateOrder) {
            // auto add
            this.creation_orders.push(o);
          } else {
            if (!add) {
              this.orders.length = 0;
            }
            this.orders.push(o);
          }
        }
        
        update() {
          if (this.creation_orders.length > 0) {
            let o = this.creation_orders[0];
            if (this.creation_counter == -1) { // Ready to create, taking the order into account
              if (o instanceof CreateSoldier) {
                this.creation_counter = UNIT_DEFINITIONS['soldier']['creation_time'];
              }
            } else if (this.creation_counter > 0) { // Order taken into account, creating...
              this.creation_counter -= 1;
            } else if (this.creation_counter == 0) { // Creation finished
              if (o instanceof CreateSoldier) {
                let u = new Unit(this.player, 'soldier', this.row + this.order_start_row_mod, this.col + this.order_start_col_mod);
                u.orders = Array.from(this.orders);
                this.creation_orders.shift();
                this.creation_counter = -1;
              }
            }
          } else if (this.creation_counter == 0) {
            throw "Incorrect state for UnitCreator: creation_counter at 0 and no order, what to create?";
          }
        }
      }
      
      class RessourceProductor extends Building {
        update() {
          if (this.speed_counter == 0) {
            if (this.type == 'generator') {
              this.player.energy += ENERGY_INCREASE_BY_TURN;
            } else if (this.type == 'extractor') {
              this.player.matter += this.player.game.ressources[this.row][this.col] * MATTER_INCREASE_BY_TURN;
            }
            this.speed_counter = this.speed;
          }
          if (this.speed_counter > 0) {
            this.speed_counter -= 1;
          }
        }
      }
      
class Player:

    def __init__(self, game, name, color, row, col, side):
        self.game = game
        self.name = name
        self.color = color
        self.row = row
        self.col = col
        self.side = side
        self.units = []
        self.groups = []
        self.energy = 0
        self.matter = 0

class Game:

    def __init__(self, level):        
        self.level = level
        self.load_map(level)
        #Position.set_level(level)

    def load_map(level):
        self.players = {}
        self.units = []
        self.all_units = []
        self.map = level.content
        self.passable = level.passable
        self.triggers = level.triggers
        for row in range(0, MAP_MAX_ROW):
            self.units[row] = []
            for col in range(0, MAP_MAX_COL):
              self.units[row][col] = 0

    def create_player(name, color, row, col):
        p = Player(self, name, color, row, col)
        self.players[name] = p
        
    def create_unit(self, player, kind, row, col):
        if kind not in UNIT_DEFINITIONS:
            raise Exception("Unknown type for Unit")
        player = self.players[player]
        Unit(player, kind, row, col)
        
    def create_building(self, player, kind, row, col):
        if kind not in UNIT_DEFINITIONS:
            raise Exception("Unknown type for Building")
        player = self.players[player]
        if UNIT_DEFINITIONS[kind]['is_creator']:
            UnitCreator(player, kind, row, col)
        elif UNIT_DEFINITIONS[kind]['is_producer']:
            RessourceProductor(player, kind, row, col)

    def update():
        for t in self.triggers:
            if !t.done:
                if t.test(self):
                    t.act(this)
      
#-----------------------------------------------------------------------
# Graphisme
#-----------------------------------------------------------------------
      
textures = {}

screen = None

mouse_map_col = -1
mouse_map_row = -1
mouse_col = -1
mouse_row = -1

scroll_left = False
scroll_right = False
scroll_up = False
scroll_down = False

#-----------------------------------------------------------------------
# Core functions : load, start, run, update, draw
#-----------------------------------------------------------------------
      
      function load() {
        for (let o of document.images) {
          textures[o.id] = o;
        }
      }
      
      function start() {
        screen = document.getElementById('screen');
        screen.onmousemove = on_mouse_move;
        window.onclick = on_mouse_left_click;
        window.oncontextmenu = on_mouse_right_click;
        window.onkeydown = on_key_down;
        window.onkeyup = on_key_up;
        window.setInterval(run, 33);
        load();
        run();
      }
      
      function run() {
        update();
        draw();
      }
      
      class Menu {
        constructor() {
          this.show = true;
          this.height = 64;
          this.width = 320;
          this.x = 0;
          this.y = CAM_MAX_ROW * 32 - this.height;
        }
        
        draw(ctx) {
          if (camera.selected.length > 0 && camera.selected.is_friendly) {
            // Background
            ctx.fillStyle = 'rgb(30, 30, 30)';
            ctx.fillRect(this.x, this.y, this.width, this.height);
            // Border
            ctx.strokeStyle = 'rgb(255, 242, 0)';
            ctx.strokeRect(this.x, this.y, this.width, this.height);
            // Available Orders (auto)
            if (!camera.selected.is_building) {
              ctx.drawImage(textures['Move'], this.x, this.y);
              ctx.drawImage(textures['Attack'], this.x + 32, this.y);
            } else {
              if (camera.selected.first.type == 'barrack') {
                ctx.strokeStyle = 'rgb(0, 128, 0)';
                ctx.strokeRect(this.x, this.y + 32, this.width / 2, 1);
                ctx.drawImage(textures['CreateSoldier'], this.x, this.y + 32);
                ctx.drawImage(textures['CreateScout'], this.x + 32, this.y + 32);
                ctx.drawImage(textures['CreateBuilder'], this.x + 64, this.y + 32);
              }
            }
            // Info on unit
            if (camera.selected.length == 1 && camera.selected.first instanceof UnitCreator) {
                ctx.font = '10px arial';
                ctx.fillStyle = 'rgb(255, 242, 0)';
                ctx.fillText('Orders: ' + camera.selected.first.orders.length, this.x + 170, this.y + 10);
                ctx.fillText('Creation orders: ' + camera.selected.first.creation_orders.length, this.x + 170, this.y + 20);
                ctx.fillText('Counter: ' + camera.selected.first.creation_counter, this.x + 170, this.y + 30);
            }
          }
        }
        
        click(mouse_col, mouse_row) {
          let row = CAM_MAX_ROW - Math.floor(mouse_row / 32);
          let col = Math.floor(mouse_col / 32);
          for (let u of camera.selected) {
            u.menu_order(row, col);
          }
        }
        
        inside(mouse_col, mouse_row) {
          return (mouse_row >= this.y && mouse_col <= this.width);
        }
      }
      
      class Minimap {
        constructor(x, y) {
          this.show = true;
          this.size = 3;
          this.x = x;
          this.y = y;
          this.max_x = this.x + this.size * 32;
          this.max_y = this.y + this.size * 32;
        }
        
        draw(ctx) {
          let row = 0;
          let col = 0;
          for (let x = this.x; x < this.max_x; x += this.size) {
            for (let y = this.y; y < this.max_y; y += this.size) {
              let val = game.map[row][col][0];
              if (game.units[row][col] != 0) {
                if (game.units[row][col].player == camera.player) {
                  val = 'unit';
                } else {
                  val = 'enemy';
                }
              }
              switch (val) {
                case 'unit':
                  ctx.fillStyle = 'rgb(0, 255, 0)';
                  ctx.fillRect(x, y, this.size, this.size);
                  break;
                case 'enemy':
                  ctx.fillStyle = 'rgb(255, 0, 0)';
                  ctx.fillRect(x, y, this.size, this.size);
                  break;
                case '0':
                  ctx.fillStyle = 'rgb(49, 86, 98)';
                  ctx.fillRect(x, y, this.size, this.size);
                  break;
                case '1':
                  ctx.fillStyle = 'rgb(126, 82, 18)';
                  ctx.fillRect(x, y, this.size, this.size);
                  break;
                case '2':
                  ctx.fillStyle = 'rgb(41, 102, 0)';
                  ctx.fillRect(x, y, this.size, this.size);
                  break;
                default:
                  throw "Center not defined";
              }
              row += 1;
            }
            col += 1;
            row = 0;
          }
          ctx.strokeStyle = 'rgb(255, 242, 0)';
          ctx.beginPath();
          ctx.rect(this.x, this.y, this.size*32, this.size*32);
          ctx.stroke();
        }
      }
      
      class Camera {
        constructor(player) {
          this.player = player;
          this.minimap = new Minimap(SCREEN_WIDTH - 3 * 32, SCREEN_HEIGHT - 3 * 32);
          this.menu = new Menu();
          this.row = player.row;
          this.col = player.col;
          this.selected = new Group(this.player);
          this.prev_selected = null;
          this.gui = true;
        }
        
        save_selection() {
          this.prev_selected = this.selected.copy();
        }
      
        restore_selection() {
          if (this.prev_selected) {
            this.selected = this.prev_selected;
          }
        }
      }
      
      function update() {
        game.update();
        for (let u of game.all_units) {
          u.update();
        }
        let old_cam_col = camera.col;
        let old_cam_row = camera.row;
        if (scroll_right) {
          camera.col = (camera.col > 0 ? camera.col - 1 : 0);
        } else if (scroll_left) {
          camera.col = (camera.col < (MAP_MAX_COL - CAM_MAX_COL) ? camera.col + 1 : camera.col);
        } else if (scroll_up) {
          camera.row = (camera.row > 0 ? camera.row - 1 : 0);
        } else if (scroll_down) {
          camera.row = (camera.row < (MAP_MAX_ROW - CAM_MAX_ROW) ? camera.row + 1 : camera.row);
        }
        // update mouse coordinates on the map!
        if (old_cam_col != camera.col || old_cam_row != camera.row) {
          if (camera.col < old_cam_col) {
            mouse_map_col -= 1;
          } else if (camera.col > old_cam_col) {
            mouse_map_col += 1;
          }
          if (camera.row < old_cam_row) {
            mouse_map_row -= 1;
          } else if (camera.row > old_cam_row) {
            mouse_map_row += 1;
          }
        }
      }
      
      function draw_element(ctx, e) {
        if (e instanceof Building) {
          draw_building(ctx, e);
        } else if (e instanceof Unit) {
          draw_unit(ctx, e);
        } else {
          console.log('Type unknown:', typeof(e), e.constructor.name);
        }
      }
      
      function draw_unit(ctx, u) {
        let posx = (u.col - camera.col) * 32 + 16;
        let posy = (u.row - camera.row) * 32 + 16;
        // Draw Unit
        ctx.fillStyle = u.player.color;
        ctx.beginPath();
        ctx.arc(posx, posy, 10, 0, 2 * Math.PI);
        ctx.fill();
        // Circle of selection
        if (camera.selected.includes(u)) {
          if (u.player == camera.player) {
            ctx.strokeStyle = 'rgb(0, 255, 0)';
          } else {
            ctx.strokeStyle = 'rgb(255, 0, 0)';
          }
          ctx.beginPath();
          ctx.arc(posx, posy, 15, 0, 2 * Math.PI);
          ctx.stroke();
        }
        // Life
        if (u.player == camera.player) {
          let percent = u.life / UNIT_DEFINITIONS[u.type]['max_life'];
          ctx.fillStyle = 'rgb(30, 30, 30)';
          ctx.fillRect(posx - 16, posy + 12, 32, 4);
          ctx.fillStyle = 'rgb(0, 255, 0)';
          ctx.fillRect(posx - 16, posy + 12, 32 * percent, 4);
        }
      }
      
      function draw_building(ctx, u) {
        let posx = (u.col - camera.col) * 32 + u.mod_x;
        let posy = (u.row - camera.row) * 32 + u.mod_y;
        // Draw Building
        if (camera.selected.includes(u)) {
          ctx.drawImage(textures[u.type + "_selected"], posx, posy);
        } else {
          ctx.drawImage(textures[u.type], posx, posy);
        }
        // Life
        if (u.player == camera.player) {
          posx = (u.col - camera.col) * 32; // + u.mod_x;
          posy = (u.row + u.height - camera.row) * 32; // + u.mod_y;
          let percent = u.life / UNIT_DEFINITIONS[u.type]['max_life'];
          ctx.fillStyle = 'rgb(30, 30, 30)';
          ctx.fillRect(posx, posy - 4, 32 * u.width, 4);
          ctx.fillStyle = 'rgb(0, 255, 0)';
          ctx.fillRect(posx, posy - 4, 32 * u.width * percent, 4);
        }
      }
      
      function draw() {
        if (screen.getContext) {
          let ctx = screen.getContext('2d');
          for (let row = 0; row < CAM_MAX_ROW; row++) {
            for (let col = 0; col < CAM_MAX_COL; col++) {
              let r = row + camera.row;
              let c = col + camera.col;
              let img = game.map[r][c];
              try {
                ctx.drawImage(textures[img], col * 32, row * 32);
              } catch (e) {
                console.log("Image=", img, "Type=", typeof(img), "Exception=", e);
                throw "End";
              }
              let u = game.units[r][c];
              if (u != 0) {
                draw_element(ctx, u);
              }
            }
          }
          // orders
          for (let u of camera.selected) {
            if (u.orders.length > 0 && u.player == camera.player) {
              let start_col = (u.col + u.order_start_col_mod - camera.col) * 32 + 16;
              let start_row = (u.row + u.order_start_row_mod - camera.row) * 32 + 16;
              let next_col = start_col;
              let next_row = start_row;
              for (let o of u.orders) {
                if (o instanceof Move) {
                  // Line
                  ctx.strokeStyle = 'rgb(255, 0, 0)';
                  ctx.beginPath();
                  ctx.moveTo(next_col, next_row);
                  ctx.lineTo((o.col - camera.col) * 32 + 16, (o.row - camera.row) * 32 + 16);
                  ctx.stroke();
                  // Target
                  ctx.fillStyle = 'rgb(255, 0, 0)';
                  ctx.beginPath();
                  ctx.arc((o.col - camera.col) * 32 + 16, (o.row - camera.row) * 32 + 16, 5, 0, 2 * Math.PI);
                  ctx.fill();
                  // Chain
                  next_col = (o.col - camera.col) * 32 + 16;
                  next_row = (o.row - camera.row) * 32 + 16;
                }
              }
              draw_element(ctx, u);
            }
          }
          // Minimap
          if (camera.minimap.show && camera.gui) {
            camera.minimap.draw(ctx);
          }
          if (camera.gui) {
            camera.menu.draw(ctx);
          }
          // Mouse
          if (mouse_map_col != -1 || mouse_map_row != -1) {
            ctx.strokeStyle = 'rgb(0, 255, 0)';
            ctx.strokeRect(Math.floor(mouse_col / 32) * 32, Math.floor(mouse_row / 32) * 32, 32, 32);
          }
          // Info on player
          ctx.font = '10px arial';
          ctx.fillStyle = 'rgb(255, 242, 0)';
          ctx.fillText('Energy: ' + camera.player.energy, 10, 10);
          ctx.fillText('Matter: ' + camera.player.matter, 10, 20);
        } else {
          alert("Your browser must support canvas to play.");
        }
      }
      
#-----------------------------------------------------------------------
# UI : Input handling
#-----------------------------------------------------------------------
      
      // Consts
      
      const KEY_UP = 38;
      const KEY_DOWN = 40;
      const KEY_RIGHT = 39;
      const KEY_LEFT = 37;
      const KEY_BACKSPACE = 8;
      const KEY_M = 77;
      const KEY_H = 72;
      
      // Functions
      
      function on_mouse_move(event) {
        event = event || window.event;
        // Mouse coordinates
        let screenRect = screen.getBoundingClientRect();
        mouse_col = event.pageX - screenRect.left;
        mouse_row = event.pageY - screenRect.top;
        mouse_map_col = Math.floor(mouse_col / 32) + camera.col;
        mouse_map_row = Math.floor(mouse_row / 32) + camera.row;
        // Scrolling
        scroll_left = false;
        scroll_right = false;
        scroll_up = false;
        scroll_down = false;
        if (mouse_col < SCROLLING_ZONE) {
          scroll_right = true;
        } else if (mouse_col > SCREEN_WIDTH - SCROLLING_ZONE) {
          scroll_left = true;
        }
        if (mouse_row < SCROLLING_ZONE) {
          scroll_up = true;
        } else if (mouse_row > SCREEN_HEIGHT - SCROLLING_ZONE) {
          scroll_down = true;
        }
      }
      
      var clicked = false;
      var iTimer;
      
      function on_mouse_left_click(event) {
        console.log('row:', mouse_map_row, 'col:', mouse_map_col);
        if (camera.menu.inside(mouse_col, mouse_row) && camera.gui) {
          camera.menu.click(mouse_col, mouse_row);
          return false;
        }
        if (event.button == 0) {
          console.log('row', mouse_map_row, 'col', mouse_map_col);
          // unselected current group (do that only if there is an unit to hold the selection)
          if (!event.ctrlKey) {
            camera.save_selection();
            camera.selected.clear();
          }
          // select
          if (mouse_map_row >= 0 && mouse_map_row < MAP_MAX_ROW && mouse_map_col >= 0 && mouse_map_col < MAP_MAX_COL) {
            let u = game.units[mouse_map_row][mouse_map_col];
            if (u) {
              camera.selected.add(u, event.ctrlKey);
            }
          }
        }
        /*
        if (!clicked) {
          console.log('Left Click');
          clicked = true;
          iTimer = setTimeout(function() { clicked = false; }, 250);
        } else if (iTimer < 10) {
          console.log('Double Click');
          clicked = false;
          clearTimeout(iTimer);
        }
        */
      }
      
      function on_mouse_right_click(event) {
        if (camera.menu.inside(mouse_col, mouse_row) && camera.gui) {
          return false;
        }
        event = window.event || event;
        console.log("Right click");
        for (let u of camera.selected) {
          if (u.player == camera.player) {
            console.log("Sending order move to unit", u.id, 'to', 'row', mouse_map_row, 'col', mouse_map_col);
            if (u.available_orders.includes(Move)) {
              u.order(new Move(mouse_map_row, mouse_map_col), event.ctrlKey);
            }
          }
        }
        return false;     // prevent default menu
      }
      
      function on_key_up(event) {
        event = window.event || event;
        if (event.keyCode == KEY_UP) {
          scroll_up = false;
        } else if (event.keyCode == KEY_DOWN) {
          scroll_down = false;
        } else if (event.keyCode == KEY_RIGHT) {
          scroll_left = false;
        } else if (event.keyCode == KEY_LEFT) {
          scroll_right = false;
        } else if (event.keyCode == KEY_BACKSPACE) {
          camera.restore_selection();
        } else if (event.keyCode == KEY_M) {
          camera.minimap.show = !camera.minimap.show;
        } else if (event.keyCode == KEY_H) {
          camera.gui = !camera.gui;
        } else {
          console.log('Unbound up key:', event.keyCode);
        }
      }
      
      function on_key_down(event){
        event = window.event || event;
        if (event.keyCode == KEY_UP) {
          scroll_up = true;
        } else if (event.keyCode == KEY_DOWN) {
          scroll_down = true;
        } else if (event.keyCode == KEY_RIGHT) {
          scroll_left = true;
        } else if (event.keyCode == KEY_LEFT) {
          scroll_right = true;
        } else {
          console.log('Unbound down key:', event.keyCode);
        }
        //return false; // prevent default
      }
      
#-----------------------------------------------------------------------
# Transition system
#-----------------------------------------------------------------------
      
      var modified = {
        "0" : [1],
        "1" : [2],
        "2" : [],
        "3" : [],
      };
      
      var trans_matrix = [];
      var pass_matrix = [];
      
      function transition_one(trow, tcol, content) {
        let calc = 0;
        let pow = 8;
        let center = content[trow][tcol]; // game.map
        let opposed = null;
        outerloop:
        for (let row = trow - 1; row <= trow + 1; row++) {
          for (let col = tcol - 1; col <= tcol + 1; col++) {
            if (row != trow || col != tcol) {
              if (row >= 0 && row < MAP_MAX_ROW && col >= 0 && col < MAP_MAX_COL) {
                // Get opposed
                if (content[row][col] != center) {
                  // Check IF opposed is NOT defined AND if the other texture encountered modifies the center
                  if (!opposed && modified[center].includes(content[row][col])) {
                    opposed = content[row][col];
                  // Check IF opposed is defined AND if the other texture is different from the opposed
                  } else if (opposed && opposed != content[row][col] && modified[center].includes(content[row][col])) {
                    console.log("Surrounded by two different textures, aborting at ", row, col, "opp=", opposed, "found=", content[row][col], "me=", center);
                    break outerloop;
                  }
                }
                // Calculate transition
                if (content[row][col] == opposed) {
                  calc += 1 * Math.pow(2, pow);
                }
              }
              pow -= 1;
            }
          }
        }
        let cal = [center, 0, 
                   0, 0, 0, 0,
                   0, 0, 0, 0];
        let O = 1;
        let N = 2 + 0;
        let E = 2 + 1;
        let S = 2 + 2;
        let W = 2 + 3;
        let NW = 6 + 0;
        let NE = 6 + 1;
        let SE = 6 + 2;
        let SW = 6 + 3;
        if ([0, 1].includes(center)) {
          opposed = modified[center]; // Earth
          // Borders
          if (trow > 0 && content[trow - 1][tcol] == opposed) { cal[O] = opposed; cal[N] = 1; }
          if (tcol > 0 && content[trow][tcol - 1] == opposed) { cal[O] = opposed; cal[W] = 1; }
          if (trow < MAP_MAX_ROW - 2 && content[trow + 1][tcol] == opposed) { cal[O] = opposed; cal[S] = 1; }
          if (tcol < MAP_MAX_COL - 2 && content[trow][tcol + 1] == opposed) { cal[O] = opposed; cal[E] = 1; }
          // Corners only if no borders
          if (cal[N] == 0 && cal[E] == 0 && cal[S] == 0 && cal[W] == 0) {
            if (trow > 0 && tcol > 0 && content[trow - 1][tcol - 1] == opposed) { cal[O] = opposed; cal[NW] = 1; }
            if (trow > 0 && tcol < MAP_MAX_COL - 2 && content[trow - 1][tcol + 1] == opposed) { cal[O] = opposed; cal[NE] = 1; }
            if (trow < MAP_MAX_ROW - 2 && tcol < MAP_MAX_COL - 2 && content[trow + 1][tcol + 1] == opposed) { cal[O] = opposed; cal[SE] = 1; }
            if (trow < MAP_MAX_ROW - 2 && tcol > 0 && content[trow + 1][tcol - 1] == opposed) { cal[O] = opposed; cal[SW] = 1; }
          }
        }
        trans_matrix[trow][tcol] = cal.join('');
        if (center > 0) {
          pass_matrix[trow][tcol] = true;
        }
      }
      
      function make_transition(content) {
        trans_matrix = [];
        pass_matrix = [];
        // Prepare trans_matrix
        for (let row = 0; row < MAP_MAX_ROW; row++) {
          trans_matrix[row] = [];
          pass_matrix[row] = [];
          for (let col=0; col < MAP_MAX_COL; col++) {
            trans_matrix[row][col] = '3000000000';
            pass_matrix[row][col] = false;
          }
        }
        // Do transitions
        for (let row=0; row < MAP_MAX_ROW; row++) {
          for (let col=0; col < MAP_MAX_COL; col++) {
            transition_one(row, col, content);
          }
        }
        // Swap
        return [trans_matrix, pass_matrix];
      }

#-----------------------------------------------------------------------
# Missions
#-----------------------------------------------------------------------

def E1L1(): 
    game = Game("A lost cause", MAPS["E1M1"])

    game.create_player('Sarah', 'rgb(0, 128, 255)', 0, 0)
    game.create_player('Tom', 'rgb(255, 127, 39)', 2, 2)
    game.create_unit('Sarah', 'soldier', 5, 5)
    game.create_unit('Sarah', 'soldier', 5, 6)
    game.create_unit('Tom', 'soldier', 10, 6)
    game.create_building('Sarah', 'barrack', 17, 18)
    game.create_building('Sarah', 'generator', 23, 16)
    game.create_building('Sarah', 'factory', 18, 5)

    camera = Camera(game.players['Sarah'])
