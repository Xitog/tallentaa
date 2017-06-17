from engine import Engine, Colors

#-------------------------------------------------------------------------------
# BUTTON
#-------------------------------------------------------------------------------
class Button:

    def __init__(self, menu, text, x, y, w, h, c, ctext, cover, cclicked, size):
        self.text = text
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.color = c
        self.color_text = ctext
        self.color_over = cover
        self.color_clicked = cclicked
        self.size = size
        self.clicked = False
        self.menu = menu
    
    def update(self):
        if self.clicked:
            self.menu.state['clicked'] = self.text
    
    def render(self):
        mx, my = self.menu.engine.get_mouse_pos()
        if self.clicked:
            c = self.color_clicked
        elif self.is_in(mx, my):
            c = self.color_over
        else:
            c = self.color
        self.menu.engine.rect(self.x, self.y, self.width, self.height, c, 1, 1) # fond
        self.menu.engine.rect(self.x-5, self.y-5, self.width+10, self.height+10, c, 1, 1) # fond
        self.menu.engine.text(self.x + self.width/2, self.y + self.height/2, self.text, self.color_text, 2, True, self.size) # texte
    
    def is_in(self, x, y):
        return self.x <= x < self.x + self.width and self.y <= y <= self.y + self.height

    def click(self):
        self.clicked = True

#-------------------------------------------------------------------------------
# MENU
#-------------------------------------------------------------------------------
class Menu:
    
    def __init__(self, engine):
        self.engine = engine
        self.buttons = []
        self.state = {'clicked': None}

    def menu_start(self):
        def pipo():
            pass

        self.buttons.append(Button(self, "Campaign", self.engine.size[0]/2-100, self.engine.size[1]/2-15-90, 200, 30,
                                   Colors.DARK_BLUE, Colors.YELLOW, Colors.LIGHT_BLUE, Colors.YELLOW, 18))
        self.buttons.append(Button(self, "Skirmish", self.engine.size[0]/2-100, self.engine.size[1]/2-15-30, 200, 30,
                                   Colors.DARK_BLUE, Colors.YELLOW, Colors.LIGHT_BLUE, Colors.YELLOW, 18))
        self.buttons.append(Button(self, "Options", self.engine.size[0]/2-100, self.engine.size[1]/2-15+30, 200, 30,
                                   Colors.DARK_BLUE, Colors.YELLOW, Colors.LIGHT_BLUE, Colors.YELLOW, 18))
        self.buttons.append(Button(self, "Quit", self.engine.size[0]/2-100, self.engine.size[1]/2-15+90, 200, 30,
                                   Colors.DARK_BLUE, Colors.YELLOW, Colors.LIGHT_BLUE, Colors.YELLOW, 18))
        
    def menu_pause(self):
        self.buttons.append(Button(self, "Quit to main menu", self.engine.size[0]/2-100, self.engine.size[1]/2-15-90, 200, 30, Colors.DARK_BLUE, Colors.YELLOW, Colors.LIGHT_BLUE, Colors.YELLOW, 18))
        self.buttons.append(Button(self, "Resume", self.engine.size[0]/2-100, self.engine.size[1]/2-15-30, 200, 30, Colors.DARK_BLUE, Colors.YELLOW, Colors.LIGHT_BLUE, Colors.YELLOW, 18))
        self.buttons.append(Button(self, "Options", self.engine.size[0]/2-100, self.engine.size[1]/2-15+30, 200, 30, Colors.DARK_BLUE, Colors.YELLOW, Colors.LIGHT_BLUE, Colors.YELLOW, 18))
        self.buttons.append(Button(self, "Quit", self.engine.size[0]/2-100, self.engine.size[1]/2-15+90, 200, 30, Colors.DARK_BLUE, Colors.YELLOW, Colors.LIGHT_BLUE, Colors.YELLOW, 18))
    
    def update(self):
        for event in self.engine.get_events():
            if event.type == self.engine.QUIT:
                self.state['clicked'] = 'Quit'
            elif event.type == self.engine.EventTypes.KEY_DOWN:
                if event.key == self.engine.Keys.ESCAPE:
                    self.state['clicked'] = 'Quit'
            elif event.type == self.engine.EventTypes.MOUSE_BUTTON_UP:
                mx, my = self.engine.get_mouse_pos()
                if event.button == self.engine.Keys.MOUSE_LEFT:
                    for b in self.buttons:
                        if b.is_in(mx, my):
                            b.click()
        for b in self.buttons:
            b.update()
        return self.state
    
    def render(self):
        self.engine.fill(Colors.BLACK)
        for b in self.buttons:
            b.render()