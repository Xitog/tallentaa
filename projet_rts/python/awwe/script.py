# ------------------------------------------------------------------------------
# Scripting the world : Trigger, Zone, Condition & Action
# ------------------------------------------------------------------------------

class Zone:

    def __init__(self, name, x1, y1, x2, y2):
        self.name = name
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


class Trigger:

    def __init__(self, name):
        self.name = name
        self.conditions = []
        self.actions = []
    
    def test_all(self, game):
        for c in self.conditions:
            if not c.test(game):
                return False
        return True
    
    def do_all(self, game):
        for a in self.actions:
            a.do(game)


class Condition:

    def __init__(self, kind, params):
        self.kind = kind
        self.params = params

    def test(self, game):
        if self.kind == 'always':
            return True
        elif self.kind == 'never':
            return False
        elif self.kind == 'player P control OPT1 (exactly/at least/at most) N unit of type T in Zone Z': #'player X control Y unit of type Z':
            if self.params[3] == 'all':
                    player1 = game.get_player_by_name(self.params[0])
                    if self.params[4] == 'everywhere':
                        if self.params[1] == 1:
                            return len(player1.units + player1.buildings) == self.params[2]
                        elif self.params[2] == 2:
                            return len(player1.units + player1.buildings) >= self.params[2]
                        elif self.params[3] == 3:
                            return len(player1.units + player1.buildings) <= self.params[2]
                    else:
                        ref_zone = self.params[4]
                        units = game.get_all_units_in_zone_for_player(ref_zone, self.params[0])
                        #print(ref_zone, units, len(units), self.params[1], self.params[2])
                        if self.params[1] == 1:
                            return len(units) == self.params[2]
                        elif self.params[1] == 2:
                            return len(units) >= self.params[2]
                        elif self.params[1] == 3:
                            return len(units) <= self.params[2]
        else:
            return False

class Action:

    def __init__(self, kind, params):
        self.kind = kind
        self.params = params
        
    def do(self, game):
        if self.kind == 'win':
            game.is_live = False
            game.get_player_by_name(self.params[0]).victorious = True
        elif self.kind == 'give all unit of player P1 to player P2 in Zone Z':
            if self.params[2] != 'everywhere':
                units = game.get_all_units_in_zone_for_player(self.params[2], self.params[0])
                receiver = game.get_player_by_name(self.params[1])
                for u in units:
                    u.player.units.remove(u)
                    u.player = receiver
                    u.player.units.append(u)
        else:
            pass

