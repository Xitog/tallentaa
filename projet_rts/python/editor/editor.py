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
# Texture class
#-----------------------------------------------------------

class Texture:

    def __init__(self, rep, name, num, filename):
        self.name = name
        self.num = num
        self.first = filename
        self.path = os.path.join(rep, self.first)
        if PILLOW:
            self.img = Image.open(self.path)
            self.tkimg = ImageTk.PhotoImage(self.img)
        else: # only work with PNG
            self.tkimg = PhotoImage(file=self.path)

#-----------------------------------------------------------
# Map class
#-----------------------------------------------------------

class Map:

    def __init__(self, name, max_col, max_row, mod, default=0):
        self.set_name(name)
        self.mod = mod
        self.ground = []
        for row in range(max_row):
            r = []
            for col in range(max_col):
                r.append(default)
            self.ground.append(r)
        self.width = max_col
        self.height = max_row
        self.filepath = None

    def __repr__(self):
        return f"{self.name} {self.width}x{self.height} [{self.mod}]"
    
    def set_name(self, name):
        self.name = name

    def set(self, row, col, tex):
        self.ground[row][col] = tex

    def get(self, row, col):
        return self.ground[row][col]

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

class ChooseSizeDialog:

    def __init__(self, parent):
        self.width = None
        self.height = None
        
        self.top = Toplevel(parent, takefocus=True)
        self.top.title('Select grid size')
        self.top.resizable(False, False)
        self.top.transient(parent)
        
        Label(self.top, text="Choose grid size :").pack()

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
        
        b = Button(self.top, text="OK", command=self.ok)
        b.pack(pady=5)

        self.top.protocol("WM_DELETE_WINDOW", self.cancel)
        self.top.geometry("+%d+%d" % (parent.winfo_rootx()+50, parent.winfo_rooty()+50))
        self.top.grab_set()
        self.top.wait_window(self.top)

    def cancel(self):
        self.top.destroy()
    
    def ok(self):
        self.width = self.widthVar.get()
        self.height = self.heightVar.get()
        self.top.destroy()

#-----------------------------------------------------------
# Dialog
#-----------------------------------------------------------

class ChooseSizeDialog:

    def __init__(self, parent):
        self.width = None
        self.height = None
        
        self.top = Toplevel(parent, takefocus=True)
        self.top.title('Map size')
        self.top.resizable(False, False)
        self.top.transient(parent)
        
        Label(self.top, text="Map size :").pack()

        #self.e = Entry(self.top)
        #self.e.pack(padx=5)

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
        
        b = Button(self.top, text="OK", command=self.ok)
        b.pack(pady=5)

        self.top.protocol("WM_DELETE_WINDOW", self.cancel)
        self.top.geometry("+%d+%d" % (parent.winfo_rootx()+50, parent.winfo_rooty()+50))
        self.top.grab_set()
        self.top.wait_window(self.top)

    def cancel(self):
        self.top.destroy()
    
    def ok(self):
        self.width = self.widthVar.get()
        self.height = self.heightVar.get()
        self.top.destroy()

#-----------------------------------------------------------
# Application class
#-----------------------------------------------------------

class Application:

    def __init__(self, title=None, width=None, height=None):
        self.title = 'Tile Grid Editor'
        self.base_geometry = { 'w' : 600, 'h' : 400, 'geometry' : '600x400+0+0'}
        self.old_geometry = self.base_geometry
        self.load_options()
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
        self.init_mod()
        self.dirty = False
        self.map = Map(title, width, height, self.options['mod'], self.default_tex) # set the map and its size
        self.build_gui() # need the size of the map in order to create the scrollbars
        self.refresh_map() # need the canvas in order to display the map
        self.run()

    def start_load_mod(self, mod):
        if mod == self.options['mod']:
            return
        else:
            self.exit_app()
            self.change_option('mod', mod)
            self.start_new_map()

    def start_load_map(self, mapfilepath):
        self.map = Map.from_json(mapfilepath)
        self.dirty = False
        if self.map.mod != self.options['mod']:
            self.exit_app()
            self.change_option('mod', self.map.mod)
            self.init_mod()
            self.build_gui() # need the size of the map in order to create the scrollbars
            self.refresh_map() # need the canvas in order to display the map
            self.run()
        else:
            self.canvas.config(scrollregion=(0, 0, self.map.width * 32, self.map.height * 32))
            self.refresh_map() # need the canvas in order to display the map

    def restart_new_map(self, title=None, width=None, height=None):
        title = 'New map' if title is None else title
        width = 32 if width is None else width
        height = 32 if height is None else height
        self.dirty = False
        self.map = Map(title, width, height, self.options['mod'], self.default_tex) # set the map and its size
        self.canvas.config(scrollregion=(0, 0, self.map.width * 32, self.map.height * 32))
        self.refresh_map() # need the canvas in order to display the map

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
            "textures_code" : {
                "blue"  : 1,
                "green" : 2,
                "red"   : 3,
            },
            "textures_files" : {
                "blue"  : "blue.png",
                "green" : "green.png",
                "red"   : "red.png",
            },
            "ground_default" : "blue",
            "cursor_default" : "green",
            "has_button" : True,
            "has_transition" : False
        }
        json.dump(data, f, indent='    ')
        graphics_dir = os.path.join(default_dir, 'graphics')
        os.makedirs(graphics_dir, exist_ok=True)
        color = {
            'green' : b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x02\x00\x00\x00\xfc\x18\xed\xa3\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x0e\xc3\x00\x00\x0e\xc3\x01\xc7o\xa8d\x00\x00\x006IDATHK\xed\xcd\xa1\x01\x000\x08\xc4\xc0\xa7\xa3t\x9e.\xcb\x865\xf8(\\\xceD\xa6n\xbfl:\xd35\x0e\x90\x03\xe4\x009@\x0e\x90\x03\xe4\x009@\x0e\x90\x03\x90|&y\x01_\xc9\xe9\xe5\xe5\x00\x00\x00\x00IEND\xaeB`\x82',
            'blue'  : b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x02\x00\x00\x00\xfc\x18\xed\xa3\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x0e\xc3\x00\x00\x0e\xc3\x01\xc7o\xa8d\x00\x00\x00NIDATHK\xb5\xc71\r\x000\x0c\xc0\xb0\xf2\x87Qt\x85\xb1?\xb7'\xf9\xf1\xcc\xde_=\xd7s=\xd7s=\xd7s=\xd7s=\xd7s=\xd7s=\xd7s=\xd7s=\xd7s=\xd7s=\xd7s=\xd7s=\xd7s=\xd7s=\xd7s\xbd\xb5\xf7\x00\x1b\xdf([v\xdd\xdf|\x00\x00\x00\x00IEND\xaeB`\x82",
            'red'   : b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x02\x00\x00\x00\xfc\x18\xed\xa3\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x0e\xc3\x00\x00\x0e\xc3\x01\xc7o\xa8d\x00\x00\x007IDATHK\xed\xcd\xa1\x01\x000\x08\xc4\xc0\xa7sTv\xff\xcd\xd8\xa1\x06\x1f\x85\xcb\x99\xc8T\xdf\x97Mg\xba\xc6\x01r\x80\x1c \x07\xc8\x01r\x80\x1c \x07\xc8\x01r\x00\x92\x0f\xd1\x10\x01m\x9a\xa8\x01\x8a\x00\x00\x00\x00IEND\xaeB`\x82',
        }
        for c in color:
            f = open(os.path.join(graphics_dir, c + '.png'), mode='wb')
            f.write(color[c])
            f.close()
    
    def init_mod(self):
        print(f"[INFO] Loading mod *** {self.options['mod']} ***")
        self.all_mods = []
        self.textures = {}
        self.num2tex = {}
        self.all_mods = []
        mod_dir = os.path.join(os.getcwd(), 'mod')
        loading_mod_error = False
        if not os.path.isdir(mod_dir):
            print('[ERROR] No mod directory found. Creating default mod.')
            loading_mod_error = True
        else:
            found = False
            for mod in os.listdir(mod_dir):
                if os.path.isdir(os.path.join(os.getcwd(), 'mod', mod)):
                    self.all_mods.append(mod)
                if mod == self.options['mod']:
                    found = True
            if not found:
                print(f"[ERROR] No self.options['mod'] mod directory found. Creating default mod.")
                loading_mod_error = True
            else:
                mod_file = os.path.join(mod_dir, self.options['mod'], self.options['mod'] + '.mod')
                if not os.path.isfile(mod_file):
                    print(f"[ERROR] No {self.options['mod']} mod file found. Creating default mod mod file.")
                    loading_mod_error = True
                mod_graphics = os.path.join(mod_dir, self.options['mod'], 'graphics')
                print(mod_graphics)
                if not os.path.isdir(mod_graphics):
                    print(f"[ERROR] No {self.options['mod']} graphics dir found. Creating default mod graphics dir.")
                    loading_mod_error = True
        if loading_mod_error:
            self.create_default_mod()
            self.change_option('mod', 'default')
            mod_dir = os.path.join(os.getcwd(), 'mod')
            if not os.path.isdir(mod_dir):
                raise Exception('[ERROR] No mod directory found.')
            mod_file = os.path.join(mod_dir, self.options['mod'], self.options['mod'] + '.mod')
            if not os.path.isfile(mod_file):
                raise Exception(f"[ERROR] No {self.options['mod']} mod file found.")
            mod_graphics = os.path.join(mod_dir, self.options['mod'], 'graphics')
            if not os.path.isdir(mod_graphics):
                raise Exception(f"[ERROR] No {self.options['mod']} graphics dir found.")
        f = open(mod_file, 'r', encoding='utf8')
        self.mod_data = json.load(f)
        self.mod_data['graphics_dir'] = mod_graphics
        if not os.path.isdir(mod_graphics):
            raise Exception('[ERROR] No graphics dir for mod. Impossible to start.')
        self.current_tex = self.mod_data['textures_code'][self.mod_data['cursor_default']]
        self.default_tex = self.mod_data['textures_code'][self.mod_data['ground_default']]
        self.current_pencil = '1x1'

    def menu_change_mod(self, index, value, op):
        if self.varMods.get() != self.options['mod']:
            if self.dirty and self.options['confirm_exit']: 
                save = messagebox.askyesno("Unsaved changes", "Do you want to save unsaved changes on the current map?", default=messagebox.YES)
                if save:
                    self.save_map()
            self.start_load_mod(self.varMods.get())
    
    #-----------------------------------------------------------
    # Map manipulation
    #-----------------------------------------------------------
    def edit_map(self, col, lin, val):
        self.map.set(lin, col, val)
        self.dirty = True
        self.refresh_title()
    
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
    
    def refresh_map(self):
        for row in range(0, self.map.height):
            for col in range(0, self.map.width):
                val = self.map.get(row, col)
                tex = self.num2tex[val]
                self.canvas.create_image(col * 32, row * 32, anchor=NW, image=tex.tkimg)
                if self.options['show_grid']:
                    self.canvas.create_rectangle(col * 32, row * 32, (col + 1) * 32, (row + 1) * 32, outline='black')
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

        # Load mod textures
        for name, num in self.mod_data['textures_code'].items():
            try:
                print(f"[INFO] Loading textures {name:>18} ({num:4d}) in file {self.mod_data['textures_files'][name]}")
                self.textures[name] = Texture(self.mod_data['graphics_dir'], name, num, self.mod_data['textures_files'][name]) # get texture object by name
                self.num2tex[self.textures[name].num] = self.textures[name] # get texture object by number
            except TclError:
                print(f"[ERROR] Impossible to load texture.")
        print(f"[INFO] {len(self.textures)} textures loaded")
        
        # Load images
        BASE_ICONS = True
        try:
            self.tk.iconbitmap(r'media\icons\editor.ico')
            basedir = os.path.join('media', 'icons')
            icons['new'] = PhotoImage(file=os.path.join(basedir, 'Actions-document-new-icon.png'))
            icons['open'] = PhotoImage(file=os.path.join(basedir, 'Actions-document-open-icon.png'))
            icons['save'] = PhotoImage(file=os.path.join(basedir, 'Actions-document-save-icon.png'))
            icons['save_as'] = PhotoImage(file=os.path.join(basedir, 'Actions-document-save-as-icon.png'))
            icons['1x1'] = PhotoImage(file=os.path.join(basedir, 'Little.png'))
            icons['3x3'] = PhotoImage(file=os.path.join(basedir, 'Medium.png'))
            icons['5x5'] = PhotoImage(file=os.path.join(basedir, 'Big.png'))
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
        
        toolsmenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Tools", menu=toolsmenu)
        toolsmenu.add_command(label="Check", command=self.menu_tools_check)
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
        toolbar = Frame(self.content)

        if BASE_ICONS:
            bt_new = Button(toolbar, image=icons['new'], width=32, height=32, command=self.menu_file_new)
            bt_open = Button(toolbar, image=icons['open'], width=32, height=32, command=self.menu_file_open)
            bt_save = Button(toolbar, image=icons['save'], width=32, height=32, command=self.menu_file_save)
            bt_save_as = Button(toolbar, image=icons['save_as'], width=32, height=32, command=self.menu_file_save_as)
        
            self.bt_pencils = {}
            self.bt_pencils['1x1'] = Button(toolbar, image=icons['1x1'], width=32, height=32, command=lambda: self.set_pencil('1x1'), relief=SUNKEN)
            self.bt_pencils['3x3'] = Button(toolbar, image=icons['3x3'], width=32, height=32, command=lambda: self.set_pencil('3x3'), relief=RAISED)
            self.bt_pencils['5x5'] = Button(toolbar, image=icons['5x5'], width=32, height=32, command=lambda: self.set_pencil('5x5'), relief=RAISED)
        
        self.bt_all = {}
        for _, tex in self.textures.items():
            self.bt_all[tex.name] = Button(toolbar, image=tex.tkimg, width=32, height=32, command=partial(self.bt_refresh, tex.tkimg))
            if self.current_tex == tex.num:
                self.bt_all[tex.name].config(relief=SUNKEN)

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
        toolbar.pack(side=TOP, fill=X)
        y_scrollbar.pack(side=RIGHT, fill=Y)
        x_scrollbar.pack(side=BOTTOM, fill=X)
        self.canvas.pack(side=TOP, fill=BOTH, expand=True)
        x_scrollbar.config(command=self.canvas.xview)
        y_scrollbar.config(command=self.canvas.yview)
        status.pack(side=BOTTOM, fill=X)

        if BASE_ICONS:
            bt_new.pack(side=LEFT)
            bt_open.pack(side=LEFT)
            bt_save.pack(side=LEFT)
            bt_save_as.pack(side=LEFT)
            sep1 = Label(toolbar, text=" ")
            sep1.pack(side=LEFT)
            for _, bt in self.bt_pencils.items():
                bt.pack(side=LEFT)
            sep2 = Label(toolbar, text=" ")
            sep2.pack(side=LEFT)

        for _, bt in self.bt_all.items():
            bt.pack(side=LEFT)

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
        if self.current_pencil == '1x1':
            start_x = x32
            end_x = x32 + 1
            start_y = y32
            end_y = y32 + 1
        elif self.current_pencil == '3x3':
            start_x = x32 - 1
            end_x = x32 + 2
            start_y = y32 - 1
            end_y = y32 + 2
        elif self.current_pencil == '5x5':
            start_x = x32 - 2
            end_x = x32 + 3
            start_y = y32 - 2
            end_y = y32 + 3
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                if 0 <= x < self.map.width and 0 <= y < self.map.height:
                    tex = self.num2tex[self.current_tex]
                    self.canvas.create_image(x * 32, y * 32, anchor=NW, image=tex.tkimg)
                    if self.options['show_grid']:
                        self.canvas.create_rectangle(x * 32, y * 32, (x + 1) * 32, (y + 1) * 32, outline='black')
                    self.edit_map(x, y, self.current_tex)

    #-----------------------------------------------------------
    # Button actions
    #-----------------------------------------------------------
    def bt_refresh(self, tkimg):
        for key, bt in self.bt_all.items():
            if self.textures[key].tkimg == tkimg:
                bt.config(relief=SUNKEN)
                self.current_tex = self.textures[key].num
            else:
                bt.config(relief=RAISED)

    def set_pencil(self, p):
        for key, bt in self.bt_pencils.items():
            if key == p:
                bt.config(relief=SUNKEN)
            else:
                bt.config(relief=RAISED)
        self.current_pencil = p

    #-----------------------------------------------------------
    # Menu actions
    #-----------------------------------------------------------
    def menu_file_new(self):
        d = ChooseSizeDialog(self.tk)
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

#-----------------------------------------------------------
# Main
#-----------------------------------------------------------

if __name__ == "__main__":
    app = Application()
