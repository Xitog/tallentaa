#-----------------------------------------------------------
# Tile Grid Editor for 2D square maps (FPS, RTS, RPG)
#-----------------------------------------------------------
# Created: May 11, 2019
# Last Modified: February 7, 2020
#-----------------------------------------------------------
# Summary
#   Imports
#   Constants & Global variables
#   Texture class
#   Map class
#   Dialog
#   Application class
#     Options
#     Start
#     Exit
#     Mod manipulation
#     Map manipulation
#     GUI building
#     Apply texture functions
#     Button actions
#     Menu actions
#   Main
#-----------------------------------------------------------

#-----------------------------------------------------------
# Imports
#-----------------------------------------------------------

from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showinfo
#from tkinter.ttk import Treeview, Button
import json
import os
import os.path
from functools import partial
import configparser
try:
    from PIL import Image, ImageTk, ImageDraw
    PILLOW = True
except ModuleNotFoundError:
    PILLOW = False
from struct import *

#-----------------------------------------------------------
# Constants & Global variables
#-----------------------------------------------------------

icons = {}

#-----------------------------------------------------------
# Image class
#-----------------------------------------------------------

class SimpleImage:

    def __init__(self, filepath, name=None, num=None):
        self.name = name
        self.num = num
        self.path = filepath
        if PILLOW:
            self.img = Image.open(self.path)
            self.tkimg = ImageTk.PhotoImage(self.img)
        else: # only work with PNG
            self.tkimg = PhotoImage(file=self.path)

#-----------------------------------------------------------
# Map class
#-----------------------------------------------------------

class Map:
    
    def create_matrix(self, max_col, max_row, val):
        matrix = []
        for row in range(max_row):
            r = []
            for col in range(max_col):
                r.append(val)
            matrix.append(r)
        return matrix
    
    def __init__(self, name, max_col, max_row, mod):
        self.set_name(name)
        self.mod = mod
        self.layers = {}
        self.width = max_col
        self.height = max_row
        self.filepath = None

    def add_layer(self, name, val):
        self.layers[name] = self.create_matrix(self.width, self.height, val)
    
    def __repr__(self):
        return f"{self.name} {self.width}x{self.height} [{self.mod}]"
    
    def set_name(self, name):
        self.name = name

    def check(self, row, col, layer):
        if layer not in self.layers:
            raise Exception(f"[ERROR] Layer value unknown: {layer}")
        elif row < 0 or row >= self.height:
            raise Exception(f"[ERROR] Out of row: {row} / {self.height}")
        elif col < 0 or col >= self.width:
            raise Exception(f"[ERROR] Out of col: {col} / {self.width}")
    
    def set(self, row, col, val, layer):
        self.check(row, col, layer)
        self.layers[layer][row][col] = val
    
    def get(self, row, col, layer):
        self.check(row, col, layer)
        return self.layers[layer][row][col]
    
    @staticmethod
    def from_json(filepath):
        f = open(filepath, 'r')
        data = json.load(f)
        f.close()
        m = Map(data["name"], len(data["ground"][0]), len(data["ground"]), data['mod'])
        m.ground = data["ground"]
        m.filepath = filepath
        return m
    
    def to_json(self, filepath, test=False):
        f = open(filepath, 'w')
        s = '{\n'
        s += f'    "name": "{self.name}",\n'
        s += f'    "mod" : "{self.mod}",\n'
        s += '    "ground" : [\n'
        for irow, row in enumerate(self.ground):
            s += '        ['
            for icol, col in enumerate(row):
                if icol != len(row) - 1:
                    s += f'{col}, '
                else:
                    s += f'{col}'
            if irow != len(self.ground) - 1:
                s += '],\n'
            else:
                s += ']\n'
        s += '    ]\n'
        s += '}'
        f.write(s)
        f.close()
        if test:
            try:
                f = open(filepath, 'r')
                data = json.load(f)
                f.close()
            except Exception:
                print('Something went wrong when trying to load map. Map may be corrupted.')
                print('Stack info:')
                traceback.print_exc(file=sys.stdout)
        self.filepath = filepath

#-----------------------------------------------------------
# Dialog
#-----------------------------------------------------------

class Dialog:

    def __init__(self, parent):
        self.top = Toplevel(parent.tk, takefocus=True)
        self.top.title('Map size')
        self.top.resizable(False, False)
        self.top.transient(parent.tk)
        self.parent = parent

        self.build()

        self.top.protocol("WM_DELETE_WINDOW", self.cancel)
        self.top.geometry("+%d+%d" % (parent.tk.winfo_rootx()+50, parent.tk.winfo_rooty()+50))
        self.top.grab_set()
        self.top.wait_window(self.top)
    
    def build(self):
        pass

    def cancel(self):
        print(f"[INFO] {self.__class__.__name__} cancelled")
        self.close()

    def close(self):
        self.top.destroy()

class ChooseObjectDialog(Dialog):

    def build(self):
        self.object = None
        
        self.top.iconbitmap(os.path.join('media', 'icons', 'editor.ico'))
        Label(self.top, text="Select object:").pack()
        
        wh = Frame(self.top)
        
        ln = len(self.parent.objects)
        nb_rows = ln // 6 + 1
        nb_elem_by_row = ln // nb_rows
        cp = 0
        objnames = list(self.parent.objects.keys())
        for row in range(0, nb_rows):
            for col in range(0, nb_elem_by_row):
                b = Button(wh, image=self.parent.objects[objnames[cp]].tkimg, width=32, height=32, command=partial(self.setval, objnames[cp]))
                b.grid(row=row, column=col)
                #print(row, col, objnames[cp], self.parent.objects[objnames[cp]].tkimg)
                cp += 1
        
        wh.pack(side=TOP, fill=BOTH)
        
        b = Button(self.top, text="Cancel", command=self.submit)
        b.pack(pady=5)

    def setval(self, val):
        print(f"[INFO] {val}")
        self.object = val
        self.close()
    
    def submit(self):
        self.close()

class ChooseSizeDialog(Dialog):
    
    def build(self):
        self.width = None
        self.height = None
        
        self.top.iconbitmap(os.path.join('media', 'icons', 'editor.ico'))
        
        Label(self.top, text="Map size:").pack()
        
        available_width = [32, 64, 128, 256]
        available_height = [32, 64, 128, 256]

        wh = Frame(self.top)
        
        self.widthVar = IntVar()
        self.widthVar.set(32)
        self.heightVar = IntVar()
        self.heightVar.set(32)

        w_group = LabelFrame(wh, text="Width", padx=5, pady=5)
        for w in available_width:
            b = Radiobutton(w_group, text=str(w), variable=self.widthVar, value=w)
            b.pack()
        w_group.pack(side=LEFT, padx=5)
        
        h_group = LabelFrame(wh, text="Height", padx=5, pady=5)
        for h in available_height:
            b = Radiobutton(h_group, text=str(h), variable=self.heightVar, value=h)
            b.pack()
        h_group.pack(side=RIGHT, padx=5)

        wh.pack(side=TOP, fill=X)
        
        b = Button(self.top, text="OK", command=self.submit)
        b.pack(pady=5)
    
    def submit(self):
        self.width = self.widthVar.get()
        self.height = self.heightVar.get()
        self.close()

#-----------------------------------------------------------
# Layer handler
#-----------------------------------------------------------

class LayerHandler:

    def __init__(name, default, pencil=1):
        self.name = name
        self.default = default
        self.pencil = pencil
        self.min = None
        self.max = None
        self.type = None # SimpleImage or Integer

#-----------------------------------------------------------
# Application class
#-----------------------------------------------------------

class Application:

    def __init__(self, title=None, width=None, height=None):
        self.title = 'Tile Grid Editor'
        self.base_geometry = { 'w' : 600, 'h' : 400, 'geometry' : '600x400+0+0'}
        self.old_geometry = self.base_geometry
        self.load_options()
        self.create_default_mod()
        self.all_mods = self.detect_mods()
        self.mod_data = None
        self.tk = None
        self.start_new_map(title, width, height)

    #-----------------------------------------------------------
    # Options
    #-----------------------------------------------------------
    def load_options(self):
        self.options = {}
        self.options['show_grid'] = False
        self.options['confirm_exit'] = True
        self.options['mod'] = 'rts'
        if os.path.isfile('config.ini'):
            config = configparser.ConfigParser()
            config.read('config.ini')
            if 'MAIN' in config:
                if 'show_grid' in config['MAIN']:
                    self.options['show_grid'] = (config['MAIN']['show_grid'] == 'True')
                if 'confirm_exit' in config['MAIN']:
                    self.options['confirm_exit'] = (config['MAIN']['confirm_exit'] == 'True')
                if 'confirm_exit' in config['MAIN']:
                    self.options['confirm_exit'] = (config['MAIN']['confirm_exit'] == 'True')
                if 'mod' in config['MAIN']:
                    self.options['mod'] = config['MAIN']['mod']
        # create default option file
        else:
            self.write_options()
        print('[INFO] All options:')
        for o in self.options:
            print(f"[INFO]     {o:15} = {self.options[o]}")
    
    def change_option(self, opt, value):
        print(f"[INFO] Setting option {opt} to {value}")
        self.options[opt] = value
        self.write_options()
    
    def write_options(self):
        config = configparser.ConfigParser()
        config['MAIN'] = {
            'show_grid' : str(self.options['show_grid']),
            'confirm_exit' : str(self.options['confirm_exit']),
            'mod' : self.options['mod'],
        }
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    
    #-----------------------------------------------------------
    # Start
    #-----------------------------------------------------------
    def start_new_map(self, title=None, width=None, height=None):
        title = 'New map' if title is None else title
        width = 32 if width is None else width
        height = 32 if height is None else height
        self.load_mod()
        self.dirty = False
        self.set_map(Map(title, width, height, self.options['mod']))
        for lay in self.mod_data['layers']:
            lay_cont = lay['content']
            def_code = lay['default']
            if lay_cont != '__integer__':
                content = self.mod_data[lay_cont]
                def_num = content[def_code]
            else:
                def_num = def_code
            self.map.add_layer(lay['name'], def_num) # set the map and its size
        self.build_gui() # need the size of the map in order to create the scrollbars
        self.refresh_map() # need the canvas in order to display the map
        self.run()

    def start_load_mod(self, mod=None, amap=None):
        # load a different mod or a map with optionnally a new mod
        if mod is None and amap is None:
            return
        elif mod is None:
            mod = amap.mod
        if mod != self.options['mod']:
            self.clean_mod_buttons()
            self.change_option('mod', mod)
            self.init_mod()
            self.load_mod_graphics()
            self.build_mod_buttons()
        if amap is None:
            self.restart_new_map()
        else:
            self.set_map(amap)
            self.canvas.config(scrollregion=(0, 0, self.map.width * 32, self.map.height * 32))
            self.refresh_map() # need the canvas in order to display the map
    
    def start_load_map(self, mapfilepath):
        print(f'[INFO] Loading {mapfilepath}')
        amap = Map.from_json(mapfilepath)
        print(f'[INFO] Mod of map is {amap.mod}')
        self.start_load_mod(amap=amap)
    
    def restart_new_map(self, title=None, width=None, height=None):
        title = 'New map' if title is None else title
        width = 32 if width is None else width
        height = 32 if height is None else height
        self.dirty = False
        valdef = self.mod_data['textures_code'][self.default_tex]
        self.set_map(Map(title, width, height, self.options['mod'], valdef)) # set the map and its size
        self.canvas.config(scrollregion=(0, 0, self.map.width * 32, self.map.height * 32))
        self.refresh_map() # need the canvas in order to display the map

    def set_map(self, amap):
         self.dirty = False
         self.map = amap
    
    #-----------------------------------------------------------
    # Exit
    #-----------------------------------------------------------
    def safe_exit_app(self):    
        sure = True
        if self.dirty and self.options['confirm_exit']: 
            sure = messagebox.askyesno("Unsaved changes", "There are unsaved changes.\nDo you really want to quit?", default=messagebox.NO)
        if sure:
            self.exit_app()
    
    def exit_app(self):
        print('[INFO] exiting')
        self.old_geometry['w'] = self.tk.winfo_width()
        self.old_geometry['h'] = self.tk.winfo_height() + 20 # don't know why but the window is downsized of 20 pixels compared to asked geometry
        self.old_geometry['geometry'] = f"{self.old_geometry['w']}x{self.old_geometry['h']}+0+0"
        if self.tk is not None:
            #self.canvas.delete("all")
            self.canvas.destroy()
            self.tk.destroy()
            self.tk = None
        print('[INFO] end of exiting')
    
    def is_linked(self):
        return self.map.filepath is not None

    #-----------------------------------------------------------
    # Mod manipulation
    #-----------------------------------------------------------
    def create_default_mod(self):
        mod_dir = os.path.join(os.getcwd(), 'mod')
        os.makedirs(mod_dir, exist_ok=True)
        default_dir = os.path.join(mod_dir, 'default')
        os.makedirs(default_dir, exist_ok=True)
        f = open(os.path.join(default_dir, 'default.mod'), mode='w', encoding='utf8')
        data = {
            "filetype" : "mod",
            "version" : 1.0,
            "name" : "default",
            "layers" : [
                {'code': "wal", 'name': "walls",   'content': "textures",    'default': "blue",   'show': True},
                {'code': "grd", 'name': "ground",  'content': "textures",    'default': "black",  'show': True},
                {'code': "cei", 'name': "ceiling", 'content': "textures",    'default': "red",    'show': False},
                {'code': "are", 'name': "area",    'content': "__integer__", 'default': 0,        'show': True},
                {'code': "obj", 'name': "objects", 'content': "objects",     'default': "circle", 'show': True}
            ],
            "textures" :{
                "__none__" : {'val': 0},
                "black" :    {'val': 1, 'file': "black.png"},
                "blue"  :    {'val': 2, 'file': "blue.png"},
                "green" :    {'val': 3, 'file': "green.png"},
                "red"   :    {'val': 4, 'file': "red.png"}
            },
            "objects" : {
                "__none__" : {'val': 0},
                "circle"   : {'val': 1, 'file': "circle.png"}
            },
            "default_layer" : "wal",
            "buttons" : "textures",
        }
        json.dump(data, f, indent='    ')
        graphics_dir = os.path.join(default_dir, 'graphics')
        os.makedirs(graphics_dir, exist_ok=True)
        color = {
            'green'  : b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x02\x00\x00\x00\xfc\x18\xed\xa3\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x0e\xc3\x00\x00\x0e\xc3\x01\xc7o\xa8d\x00\x00\x006IDATHK\xed\xcd\xa1\x01\x000\x08\xc4\xc0\xa7\xa3t\x9e.\xcb\x865\xf8(\\\xceD\xa6n\xbfl:\xd35\x0e\x90\x03\xe4\x009@\x0e\x90\x03\xe4\x009@\x0e\x90\x03\x90|&y\x01_\xc9\xe9\xe5\xe5\x00\x00\x00\x00IEND\xaeB`\x82',
            'blue'   : b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x02\x00\x00\x00\xfc\x18\xed\xa3\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x0e\xc3\x00\x00\x0e\xc3\x01\xc7o\xa8d\x00\x00\x00NIDATHK\xb5\xc71\r\x000\x0c\xc0\xb0\xf2\x87Qt\x85\xb1?\xb7'\xf9\xf1\xcc\xde_=\xd7s=\xd7s=\xd7s=\xd7s=\xd7s=\xd7s=\xd7s=\xd7s=\xd7s=\xd7s=\xd7s=\xd7s=\xd7s=\xd7s=\xd7s\xbd\xb5\xf7\x00\x1b\xdf([v\xdd\xdf|\x00\x00\x00\x00IEND\xaeB`\x82",
            'red'    : b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x02\x00\x00\x00\xfc\x18\xed\xa3\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x0e\xc3\x00\x00\x0e\xc3\x01\xc7o\xa8d\x00\x00\x007IDATHK\xed\xcd\xa1\x01\x000\x08\xc4\xc0\xa7sTv\xff\xcd\xd8\xa1\x06\x1f\x85\xcb\x99\xc8T\xdf\x97Mg\xba\xc6\x01r\x80\x1c \x07\xc8\x01r\x80\x1c \x07\xc8\x01r\x00\x92\x0f\xd1\x10\x01m\x9a\xa8\x01\x8a\x00\x00\x00\x00IEND\xaeB`\x82',
            'black'  : b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x02\x00\x00\x00\xfc\x18\xed\xa3\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x0e\xc3\x00\x00\x0e\xc3\x01\xc7o\xa8d\x00\x00\x00\x1aIDATHK\xed\xc1\x01\r\x00\x00\x00\xc2\xa0\xf7O\xedf\x0e \x00\x00\x80\xab\x01\x0c \x00\x016"\n\xad\x00\x00\x00\x00IEND\xaeB`\x82',
            'circle' : b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x02\x00\x00\x00\xfc\x18\xed\xa3\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x0e\xc3\x00\x00\x0e\xc3\x01\xc7o\xa8d\x00\x00\x00\xccIDATHK\xed\x961\x0e\xc20\x0cES\x8e\xc0\x0c\x1b\xdc\xff@\x8c\xccp\x85`\xe4(\xb4q\xb0\x7fZ\xbb\x03\xe2-\x8dT\xfb\xff|[\xaa:\xe5\x9c\x93\xe0y\xbe\xf2\xe1x\xbf\xf1AA/^\x18\xd4R\x89l\x06\x8b\x0f\xe5\xa96\x10\xcd[\xbc\xb8\x18\xe8\rL\xad\x19*\xfe$@\xa06D}\xce\xdb`\xb4\x07\x84e\xc7\x12\xac`z\x9c.\xe5\x18Cx\x82\xbf\x81I\xbc\x01\xf29\xdbBl\x02\xba\xfdo,9h\r,\xbb\xd7\x88\xdcCT\xc1\x1d\x97\xec\x18b.\xb5H\xe0\xe2\xd1\x88\xb4#r\xcc\xc1tv\xb0\xc5C\xf6z.\xb9{\xb3\xfe\x9f\x1d3\xf43\xf0-\xb7f@ \x1e\xfaH\x8d\x11\x99\xfb0\x0b\x8c\x04\x15\x19\xc5\x94f\xd0%7r\xa0:\x81&XIJ/jdW5\xf8\xe4]\x82\x00\x00\x00\x00IEND\xaeB`\x82'
        }
        for c in color:
            f = open(os.path.join(graphics_dir, c + '.png'), mode='wb')
            f.write(color[c])
            f.close()

    def detect_mods(self):
        all_mods = []
        mod_dir = os.path.join(os.getcwd(), 'mod')
        for mod in os.listdir(mod_dir):
            if os.path.isdir(os.path.join(os.getcwd(), 'mod', mod)):
                all_mods.append(mod)
        return all_mods
    
    def load_mod(self):
        print(f"[INFO] Loading mod *** {self.options['mod']} ***")
        mod_dir = os.path.join(os.getcwd(), 'mod', self.options['mod'])
        mod_file = os.path.join(mod_dir, self.options['mod'] + '.mod')
        mod_graphics = os.path.join(mod_dir, 'graphics')
        f = open(mod_file, 'r', encoding='utf8')
        self.mod_data = json.load(f)
        f.close()
        self.mod_data['graphics_dir'] = mod_graphics
        self.current_layer = self.mod_data["default_layer"]
        self.nb_layers = len(self.mod_data["layers"])
        self.current_pencil = []
        self.current_apply = []
        self.visible_layers = {}
        self.resources = {}
        self.num2resources = {}
        for lay in self.mod_data["layers"]:
            if lay['content'] not in self.resources and lay['content'] != '__integer__':
                self.resources[lay['content']] = {}
                self.num2resources[lay['content']] = {} # get texture object by number
            self.current_apply.append(lay["default"])
            self.current_pencil.append(1)
            self.visible_layers[lay['name']] = lay['show']
        self.current_start_pos = None
    
    def menu_change_pencil(self, index, value, op):
        if self.varPencils.get() != self.current_pencil:
            self.current_pencil = self.varPencils.get()
        for val, bt in self.bt_pencils.items():
            if val == self.current_pencil:
                bt.config(relief=SUNKEN)
            else:
                bt.config(relief=RAISED)
    
    def menu_change_mod(self, index, value, op):
        if self.varMods.get() != self.options['mod']:
            if self.dirty and self.options['confirm_exit']: 
                save = messagebox.askyesno("Unsaved changes", "Do you want to save unsaved changes on the current map?", default=messagebox.YES)
                if save:
                    self.save_map()
            self.start_load_mod(self.varMods.get())

    def load_mod_graphics(self):
        # Load mod textures. Tk() object must be created.
        # {name:>18} ({num:4d}) in file {self.mod_data['textures_files'][name]}
        g = {}
        for file in os.listdir(self.mod_data['graphics_dir']):
            try:
                print(f"[INFO] Loading graphic {file:18}")
                g[file] = SimpleImage(os.path.join(self.mod_data['graphics_dir'], file)) #, name, num, self.mod_data['textures_files'][name]) # get texture object by name
            except TclError:
                print(f"[ERROR] Impossible to load texture.")
        print(f"[INFO] {len(g)} graphics loaded")
        # Load resources
        for keyres in self.resources:
            data = self.mod_data[keyres]
            for code, content in data.items():
                if code == '__none__': continue
                self.resources[keyres][code] = g[content['file']]
                self.resources[keyres][code].num = content['val']
                self.resources[keyres][code].name = code
                self.num2resources[keyres][content['val']] = self.resources[keyres][code]
            print(f"[INFO]   -> including {len(self.resources[keyres])} {keyres} loaded")
    
    def build_mod_buttons(self):
        # Create texture buttons for the mod. Tk() object must be created.
        self.bt_textures = {}
        bt = self.mod_data['buttons']
        print('>>>', bt, self.resources)
        for _, res in self.resources[bt].items():
            print(res)
            print(f'[INFO] Creating button for {bt} : {res.name}')
            self.bt_textures[res.name] = Button(self.toolbar, image=res.tkimg, width=32, height=32, command=partial(self.bt_change_tex, res.tkimg))
            if self.current_layer == bt and self.current_apply[bt] == res.name:
                self.bt_textures[res.name].config(relief=SUNKEN)
            self.bt_textures[res.name].pack(side=LEFT)
    
    def clean_mod_buttons(self):
        # Clean texture buttons for the mod. Tk() object must be created.
        for _, b in self.bt_textures.items():
            b.destroy()
    
    #-----------------------------------------------------------
    # Map manipulation
    #-----------------------------------------------------------
    def rename_map(self, name):
        self.map.set_name(name)
        self.dirty = True
        self.refresh_title()
    
    def save_map(self, filepath=None):
        if filepath is None and self.map.filepath is None:
            name, filepath = self.get_target()
            if name is None:
                print("[INFO] Unable to save to None")
                return
        elif filepath is None:
            filepath = self.map.filepath
        self.map.to_json(filepath, True)
        self.dirty = False
        self.refresh_title()
    
    def refresh_title(self):
        if self.map is None:
            txt = f'{self.title}'
        else:
            dirty = '*' if self.dirty else ''
            txt = f'{self.title} - {self.map.name} {dirty}'
        self.tk.title(txt)

    def refresh_tile(self, row, col):
        for lay, visible in self.visible_layers.items():
            if not visible: continue
            XXX
        
        ntex = self.map.get(row, col, Map.TEXTURE)
        nobj = self.map.get(row, col, Map.OBJECT)
        tex = self.num2tex[ntex]
        self.canvas.create_image(col * 32, row * 32, anchor=NW, image=tex.tkimg)
        if nobj != 0:
            obj = self.num2obj[nobj]
            self.canvas.create_image(col * 32, row * 32, anchor=NW, image=obj.tkimg)
        if self.options['show_grid']:
            self.canvas.create_rectangle(col * 32, row * 32, (col + 1) * 32, (row + 1) * 32, outline='black')
    
    def refresh_map(self):
        for row in range(0, self.map.height):
            for col in range(0, self.map.width):
                self.refresh_tile(row, col)
        self.refresh_title()

    def refresh_map(self):
        img = Image.new('RGB', (self.map.width * 32, self.map.height * 32), color = 'black')
        for row in range(0, self.map.height):
            for col in range(0, self.map.width):
                val = self.map.get(row, col)
                tex = self.num2tex[val].img
                img.paste(tex, (col * 32, row * 32))
                if self.options['show_grid']:
                    d = ImageDraw.Draw(img)
                    d.rectangle((col * 32, row * 32, (col + 1) * 32, (row + 1) * 32), fill=None, outline='black', width=1)
        self.background = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=NW, image=self.background)
        self.refresh_title()
    
    def set_show_grid(self, index, value, op):
        self.change_option('show_grid', not self.options['show_grid'])
        print('set', 'i=', index, 'v=', value, 'op=', op, 'show_grid=', self.options['show_grid'])
        self.refresh_map()
    
    def get_show_grid(self, index, value, op):
        print('get', 'i=', index, 'v=', value, 'op=', op, 'show_grid=', self.options['show_grid'])
        return self.options['show_grid']

    #-----------------------------------------------------------
    # GUI building
    #-----------------------------------------------------------
    def build_gui(self):
        print("[INFO] Building GUI")
        #if self.tk is not None:
        #    self.exit_app()
        #else:
        self.tk = Tk()
        self.tk.protocol("WM_DELETE_WINDOW", self.safe_exit_app)

        self.load_mod_graphics()
        
        # Load images
        BASE_ICONS = True
        try:
            self.tk.iconbitmap(os.path.join('media', 'icons', 'editor.ico'))
            basedir = os.path.join('media', 'icons')
            icons['new'] = PhotoImage(file=os.path.join(basedir, 'Actions-document-new-icon.png'))
            icons['open'] = PhotoImage(file=os.path.join(basedir, 'Actions-document-open-icon.png'))
            icons['save'] = PhotoImage(file=os.path.join(basedir, 'Actions-document-save-icon.png'))
            icons['save_as'] = PhotoImage(file=os.path.join(basedir, 'Actions-document-save-as-icon.png'))
            icons['1x1'] = PhotoImage(file=os.path.join(basedir, 'Little.png'))
            icons['3x3'] = PhotoImage(file=os.path.join(basedir, 'Medium.png'))
            icons['5x5'] = PhotoImage(file=os.path.join(basedir, 'Big.png'))
            icons['objects'] = PhotoImage(file=os.path.join(basedir, 'Objects.png'))
        except TclError:
            print("[ERROR] Unable to load button icons. No button will be created.")
            BASE_ICONS = False
        
        print("[INFO] Creating menu")
        # Menu
        menu = Menu(self.tk)
        self.tk.config(menu=menu)
        filemenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New...", command=self.menu_file_new)
        filemenu.add_command(label="Open...", command=self.menu_file_open)
        filemenu.add_command(label="Save", command=self.menu_file_save)
        filemenu.add_command(label="Save As...", command=self.menu_file_save_as)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.menu_file_exit)

        editmenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Edit", menu=editmenu)
        
        self.varShowGrid = BooleanVar()
        self.varShowGrid.set(self.options['show_grid'])
        #self.varShowGrid.trace('r', app.get_show_grid)
        self.varShowGrid.trace('w', self.set_show_grid)

        viewmenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="View", menu=viewmenu)
        viewmenu.add_command(label="Toolbar")
        viewmenu.add_command(label="Status Bar")
        viewmenu.add_command(label="Animate")
        viewmenu.add_command(label="Mini Map")
        viewmenu.add_checkbutton(label="Show Grid", variable=self.varShowGrid)

        self.varPencils = IntVar()
        self.varPencils.set(1)
        self.varPencils.trace('w', self.menu_change_pencil)
        
        toolsmenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Tools", menu=toolsmenu)
        pencilmenu = Menu(toolsmenu, tearoff=0)
        toolsmenu.add_cascade(label="Pencils", menu=pencilmenu)
        pencilmenu.add_radiobutton(label="1x1", variable=self.varPencils, value=1)
        pencilmenu.add_radiobutton(label="3x3", variable=self.varPencils, value=3)
        pencilmenu.add_radiobutton(label="5x5", variable=self.varPencils, value=5)
        toolsmenu.add_command(label="Check", command=self.menu_tools_check)
        toolsmenu.add_separator()
        export_sta = "normal" if PILLOW else "disabled"
        toolsmenu.add_command(label="Export image", command=self.menu_tools_export_image, state=export_sta)
        toolsmenu.add_command(label="Export binary", command=self.menu_tools_export_binary)
        
        self.varMods = StringVar()
        self.varMods.set(self.options['mod'])
        self.varMods.trace('w', self.menu_change_mod)
        
        modsmenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Mods", menu=modsmenu)
        for mod in self.all_mods:
            modsmenu.add_radiobutton(label=mod.upper(), variable=self.varMods, value=mod)
        
        self.varPlayer = IntVar()
        self.varPlayer.set(1)
        
        playermenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Player", menu=playermenu)
        playermenu.add_radiobutton(label="Player 1", variable=self.varPlayer, value=1)
        playermenu.add_radiobutton(label="Player 2", variable=self.varPlayer, value=2)
        
        helpmenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.menu_about)
        
        # Frame
        self.content = Frame(self.tk)
        self.content.pack_propagate(0) # don't let the widget inside it resize it
        self.tk.geometry(self.old_geometry['geometry'])
        #self.tk.state('zoomed')

        # Button bar
        print("[INFO] Creating toolbar")
        self.toolbar = Frame(self.content)

        if BASE_ICONS:
            bt_new = Button(self.toolbar, image=icons['new'], width=32, height=32, command=self.menu_file_new)
            bt_open = Button(self.toolbar, image=icons['open'], width=32, height=32, command=self.menu_file_open)
            bt_save = Button(self.toolbar, image=icons['save'], width=32, height=32, command=self.menu_file_save)
            bt_save_as = Button(self.toolbar, image=icons['save_as'], width=32, height=32, command=self.menu_file_save_as)
        
            self.bt_pencils = {}
            self.bt_pencils[1] = Button(self.toolbar, image=icons['1x1'], width=32, height=32, command=lambda: self.bt_change_pencil(1), relief=SUNKEN)
            self.bt_pencils[3] = Button(self.toolbar, image=icons['3x3'], width=32, height=32, command=lambda: self.bt_change_pencil(3), relief=RAISED)
            self.bt_pencils[5] = Button(self.toolbar, image=icons['5x5'], width=32, height=32, command=lambda: self.bt_change_pencil(5), relief=RAISED)

            bt_object = Button(self.toolbar, image=icons['objects'], width=32, height=32, command=self.menu_choose_object)
            
            bt_new.pack(side=LEFT)
            bt_open.pack(side=LEFT)
            bt_save.pack(side=LEFT)
            bt_save_as.pack(side=LEFT)
            sep1 = Label(self.toolbar, text=" ")
            sep1.pack(side=LEFT)
            for _, bt in self.bt_pencils.items():
                bt.pack(side=LEFT)
            sep2 = Label(self.toolbar, text=" ")
            sep2.pack(side=LEFT)
            bt_object.pack(side=LEFT)
            sep3 = Label(self.toolbar, text= " ")
            sep3.pack(side=LEFT)
        
        self.build_mod_buttons()

        # Canvas
        print("[INFO] Creating canvas")
        x_scrollbar = Scrollbar(self.content, orient=HORIZONTAL)
        y_scrollbar = Scrollbar(self.content, orient=VERTICAL)
        self.canvas = Canvas(self.content,
                        scrollregion=(0, 0, self.map.width * 32, self.map.height * 32),
                        xscrollcommand=x_scrollbar.set,
                        yscrollcommand=y_scrollbar.set)

        # Status bar
        print("[INFO] Creating status bar")
        self.status_var =  StringVar()
        self.status_var.set('Welcome')
        status = Label(self.content, textvariable = self.status_var, relief=SUNKEN, anchor=E)

        # Packing
        print("[INFO] Packing GUI")
        self.content.pack(fill=BOTH,expand=True)
        self.toolbar.pack(side=TOP, fill=X)
        y_scrollbar.pack(side=RIGHT, fill=Y)
        x_scrollbar.pack(side=BOTTOM, fill=X)
        self.canvas.pack(side=TOP, fill=BOTH, expand=True)
        x_scrollbar.config(command=self.canvas.xview)
        y_scrollbar.config(command=self.canvas.yview)
        status.pack(side=BOTTOM, fill=X)
        
        # Canvas
        print("[INFO] Binding")
        #canvas.create_line(0, 0, 200, 100)
        #canvas.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
        #canvas.create_rectangle(50, 25, 150, 75, fill="blue")
        #canvas.create_text(canvas_width / 2, canvas_height / 2, text="Python")
        self.canvas.bind('<ButtonPress-1>', self.put_texture)
        self.canvas.bind('<B1-Motion>', self.put_texture)
        #canvas.bind('<ButtonRelease-1>', end_texture)
        self.canvas.bind('<Motion>', self.refresh_status_bar)
        print("[INFO] GUI init end")
    
    def run(self):
        self.tk.mainloop()

    #-----------------------------------------------------------
    # Apply texture functions
    #-----------------------------------------------------------
    def get_map_coord(self, event):
        x32 = int(self.canvas.canvasx(event.x) // 32)
        y32 = int(self.canvas.canvasy(event.y) // 32)
        return x32, y32

    def refresh_status_bar(self, event):
        x32, y32 = self.get_map_coord(event)
        if 0 <= x32 < 32 and 0 <= y32 < 32:
            self.status_var.set(f"x/col = {x32}, y/row = {y32}")

    def put_texture(self, event):
        x32, y32 = self.get_map_coord(event)
        print(f'[INFO] {y32} {x32} l={self.current_layer} t={self.current_tex} o={self.current_object}')
        if self.current_pencil == 1:
            start_x = x32
            end_x = x32 + 1
            start_y = y32
            end_y = y32 + 1
        elif self.current_pencil == 3:
            start_x = x32 - 1
            end_x = x32 + 2
            start_y = y32 - 1
            end_y = y32 + 2
        elif self.current_pencil == 5:
            start_x = x32 - 2
            end_x = x32 + 3
            start_y = y32 - 2
            end_y = y32 + 3
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                if 0 <= x < self.map.width and 0 <= y < self.map.height:
                    if self.current_layer == Map.TEXTURE:
                        val = self.textures[self.current_tex].num
                    elif self.current_layer == Map.OBJECT:
                        val = self.objects[self.current_object].num
                    self.map.set(y, x, val, self.current_layer)
                    self.refresh_tile(y, x)
        self.dirty = True
        self.refresh_title()
    
    #-----------------------------------------------------------
    # Button and menu actions
    #-----------------------------------------------------------
    def bt_change_tex(self, tkimg):
        for key, bt in self.bt_textures.items():
            if self.textures[key].tkimg == tkimg:
                bt.config(relief=SUNKEN)
                self.current_tex = self.textures[key].name
            else:
                bt.config(relief=RAISED)
        self.current_layer = Map.TEXTURE
    
    def bt_change_pencil(self, p):
        for key, bt in self.bt_pencils.items():
            if key == p:
                bt.config(relief=SUNKEN)
            else:
                bt.config(relief=RAISED)
        self.current_pencil = p
        self.varPencils.set(p)
        
    def menu_change_pencil(self, index, value, op):
        if self.varPencils.get() != self.current_pencil:
            self.current_pencil = self.varPencils.get()
        for val, bt in self.bt_pencils.items():
            if val == self.current_pencil:
                bt.config(relief=SUNKEN)
            else:
                bt.config(relief=RAISED)
    
    def menu_file_new(self):
        d = ChooseSizeDialog(self)
        if d.width is not None:
            self.restart_new_map('New map', d.width, d.height)
    
    def menu_file_open(self):
        filepath = askopenfilename(initialdir = os.getcwd(), title = "Select a file to open", filetypes = (("map files","*.map"),("all files","*.*")))
        if filepath != '' and os.path.isfile(filepath):
            self.start_load_map(filepath)
    
    def menu_file_save(self):
        if self.is_linked():
            self.save_map()
        else:
            self.menu_file_save_as()
    
    def get_target(self):
        filepath = asksaveasfilename(initialdir = os.getcwd(), title = "Select where to save", filetypes = (("map files","*.map"),("all files","*.*")))
        if filepath != '':
            if not filepath.endswith('.map'):
                filepath += '.map'
            bn = os.path.basename(filepath)
            n = os.path.splitext(bn)[0]
            return n, filepath # mymap C:\...\mymap.map
        else:
            return None, None
    
    def menu_file_save_as(self):
        name, filepath = self.get_target()
        if name is not None:
            self.rename_map(name)
            self.save_map(filepath)
    
    def menu_file_exit(self):
        res = self.exit_app()
    
    def menu_about(self):
        showinfo("About", "This is a simple example of a menu")
    
    def menu_tools_check(self):
        print('Checking map conformity')
    
    def menu_tools_export_binary(self):
        s = pack('<hlf', 1, 2, 3.5) # h:short=2 l:long=4 f:float=4
        f = open(f"{self.map.name}.bin", "wb")
        f.write(s)
        f.close()
        print(f"[INFO] Map exported as binary in file {self.map.name}.bin")
    
    def menu_tools_export_image(self):
        if not PILLOW:
            return
        img = Image.new('RGB', (self.map.width * 32, self.map.height * 32), color = 'black')
        for row in range(0, self.map.height):
            for col in range(0, self.map.width):
                val = self.map.get(row, col)
                tex = self.num2tex[val].img
                img.paste(tex, (col * 32, row * 32))
                if self.options['show_grid']:
                    d = ImageDraw.Draw(img)
                    d.rectangle((col * 32, row * 32, (col + 1) * 32, (row + 1) * 32), fill=None, outline='black', width=1)
        img.save(f'{self.map.name}.png')
        print(f"[INFO] Map exported as image in file {self.map.name}.png")

    def menu_choose_object(self):
        o = ChooseObjectDialog(self)
        if o.object is not None:
            self.current_layer = Map.OBJECT
            self.current_object = o.object

#-----------------------------------------------------------
# Main
#-----------------------------------------------------------

if __name__ == "__main__":
    app = Application()
