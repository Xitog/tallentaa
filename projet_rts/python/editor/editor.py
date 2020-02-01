#-----------------------------------------------------------
# Map Editor for 2D square maps (RTS, RPG)
#-----------------------------------------------------------
# Created: May 11, 2019
# Modified: January 28, 2020
#-----------------------------------------------------------
# Summary
#   Imports
#   Mods
#   Constants & Global variables
#   Map class
#   Application class
#   Menu actions
#   Button actions
#   Apply texture functions
#   GUI building
#   Main
#-----------------------------------------------------------

#-----------------------------------------------------------
# Imports
#-----------------------------------------------------------

from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showinfo
#from tkinter.ttk import Treeview, Button
import json
import os
import os.path
from functools import partial

#-----------------------------------------------------------
# Mods
#-----------------------------------------------------------
mod_cur = 'rts'
mod_dir = os.path.join(os.getcwd(), 'mod')
if not os.path.isdir(mod_dir):
    raise Exception('No mod directory. Impossible to start.')
else:
    found = False
    for mod in os.listdir(mod_dir):
        if mod == mod_cur:
            found = True
            break
    mod_file = os.path.join(mod_dir, mod_cur, mod_cur + '.mod')
    if not found:
        raise Exception('Current mod not found. Impossible to start.')
    elif not os.path.isfile(mod_file):
        raise Exception(f'No mod file {mod_file} found. Impossible to start.')
    else:
        f = open(mod_file, 'r', encoding='utf8')
        mod_data = json.load(f)
        mod_graphics = os.path.join(mod_dir, mod_cur, 'graphics')
        if not os.path.isdir(mod_graphics):
            raise Exception('No graphics dir for mod. Impossible to start.')

#-----------------------------------------------------------
# Constants & Global variables
#-----------------------------------------------------------

canvas_width = 200
canvas_height = 100

root = Tk()
icons = {}
textures = {}

class Texture:

    def __init__(self, rep, name, num):
        self.name = name
        self.num = num
        self.first = self.name + '-1.png'
        self.path = os.path.join(rep, self.first)
        self.tkimg = PhotoImage(file=self.path)

# Load images
img = True
try:
    root.iconbitmap(r'media\icons\editor.ico')
    basedir = os.path.join('media', 'icons')
    icons['new'] = PhotoImage(file=os.path.join(basedir, 'Actions-document-new-icon.png'))
    icons['open'] = PhotoImage(file=os.path.join(basedir, 'Actions-document-open-icon.png'))
    icons['save'] = PhotoImage(file=os.path.join(basedir, 'Actions-document-save-icon.png'))
    icons['save_as'] = PhotoImage(file=os.path.join(basedir, 'Actions-document-save-as-icon.png'))
    icons['1x1'] = PhotoImage(file=os.path.join(basedir, 'Little.png'))
    icons['3x3'] = PhotoImage(file=os.path.join(basedir, 'Medium.png'))
    icons['5x5'] = PhotoImage(file=os.path.join(basedir, 'Big.png'))
    for name, num in mod_data['textures'].items():
        textures[name] = Texture(mod_graphics, name, num)
except TclError:
    raise("Unable to load image. Impossible to start.")
    #img = False

current_tex = mod_data['cursor_default']

current_pencil = '1x1'

status_var =  StringVar()
status_var.set('Welcome')

#-----------------------------------------------------------
# Map class
#-----------------------------------------------------------

class Map:

    def __init__(self, name, max_col, max_row, default=0):
        self.set_name(name)
        self.ground = []
        for row in range(max_row):
            r = []
            for col in range(max_col):
                r.append(default)
            self.ground.append(r)

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
        m = Map(data["name"], len(data["ground"][0]), len(data["ground"]), mod_data["ground_default"])
        m.ground = data["ground"]
        return m
    
    def to_json(self, filepath, test=False):
        f = open(filepath, 'w')
        s = '{\n'
        s += f'    "name": "{self.name}",\n'
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

def num2tex(n):
    for _, tex in textures.items():
        if tex.num == n:
            return tex.tkimg


#-----------------------------------------------------------
# Application class
#-----------------------------------------------------------

class Application:

    def __init__(self, tk, m=None):
        self.tk = tk
        self.canvas = None
        self.title = 'Map editor'
        self.map = m
        self.filepath = None
        self.dirty = False
        self.show_grid = False

    def link_canvas(self, canvas):
        self.canvas = canvas

    def is_linked(self):
        return self.filepath is not None
    
    def create_map(self, name, width, height, default):
        self.map = Map(name, width, height, default)
        self.filepath = None
        self.dirty = False
        self.refresh_map()

    def change_map(self, col, lin, val):
        self.map.set(lin, col, val)
        self.dirty = True
        self.refresh_title()
    
    def rename_map(self, name):
        self.map.set_name(name)
        self.dirty = True
        self.refresh_title()

    def load_map(self, filepath):
        self.map = Map.from_json(filepath)
        self.filepath = filepath
        self.dirty = False
        self.refresh_map()
    
    def save_map(self, filepath=None):
        if filepath is None and self.filepath is None:
            raise Exception("Cannot save to None")
        elif filepath is None:
            filepath = self.filepath
        self.map.to_json(filepath, True)
        self.filepath = filepath
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
        for row in range(0, 32):
            for col in range(0, 32):
                val = self.map.get(row, col)
                tex = num2tex(val)
                self.canvas.create_image(col * 32, row * 32, anchor=NW, image=tex)
                if self.show_grid:
                    self.canvas.create_rectangle(col * 32, row * 32, (col + 1) * 32, (row + 1) * 32, outline='black')
        self.refresh_title()

    def set_show_grid(self, index, value, op):
        self.show_grid = not self.show_grid
        print('set', 'i=', index, 'v=', value, 'op=', op, 'show_grid=', self.show_grid)
        self.refresh_map()

    def get_show_grid(self, index, value, op):
        print('get', 'i=', index, 'v=', value, 'op=', op, 'show_grid=', self.show_grid)
        return self.show_grid
        
        
    def quit(self):
        self.canvas.destroy()
        self.tk.destroy()

app = Application(root)

#-----------------------------------------------------------
# Menu actions
#-----------------------------------------------------------

def menu_file_new():
    app.create_map('New map', 32, 32, default=mod_data["ground_default"])

def menu_file_open():
    filepath = askopenfilename(initialdir = os.getcwd(), title = "Select a file to open", filetypes = (("map files","*.map"),("all files","*.*")))
    if filepath != '':
        app.load_map(filepath)

def menu_file_save():
    if app.is_linked():
        app.save_map()
    else:
        menu_file_save_as()

def menu_file_save_as():
    filepath = asksaveasfilename(initialdir = os.getcwd(), title = "Select where to save", filetypes = (("map files","*.map"),("all files","*.*")))
    if filepath != '':
        if not filepath.endswith('.map'):
            filepath += '.map'
        bn = os.path.basename(filepath)
        n = os.path.splitext(bn)[0]
        app.rename_map(n)
        app.save_map(filepath)

def menu_file_exit():
    global app
    app.quit()
    del app

def About():
    showinfo("About", "This is a simple example of a menu")


def menu_tools_check():
    print('Checking map conformity')

def menu_tools_image():
    pass

#-----------------------------------------------------------
# Button actions
#-----------------------------------------------------------

def bt_refresh(tkimg):
    global current_tex
    for key, bt in bt_all.items():
        if textures[key].tkimg == tkimg:
            bt.config(relief=SUNKEN)
            current_tex = textures[key].num
        else:
            bt.config(relief=RAISED)

def set_pencil(p):
    global current_pencil
    for key, bt in bt_pencils.items():
        if key == p:
            bt.config(relief=SUNKEN)
        else:
            bt.config(relief=RAISED)
    current_pencil = p

#-----------------------------------------------------------
# Apply texture functions
#-----------------------------------------------------------

def get_map_coord(event):
    x32 = int(canvas.canvasx(event.x) // 32)
    y32 = int(canvas.canvasy(event.y) // 32)
    return x32, y32

def refresh_status_bar(event):
    x32, y32 = get_map_coord(event)
    if 0 <= x32 < 32 and 0 <= y32 < 32:
        status_var.set(f"x/col = {x32}, y/row = {y32}")

def put_texture(event):
    x32, y32 = get_map_coord(event)
    if current_pencil == '1x1':
        start_x = x32
        end_x = x32 + 1
        start_y = y32
        end_y = y32 + 1
    elif current_pencil == '3x3':
        start_x = x32 - 1
        end_x = x32 + 2
        start_y = y32 - 1
        end_y = y32 + 2
    elif current_pencil == '5x5':
        start_x = x32 - 2
        end_x = x32 + 3
        start_y = y32 - 2
        end_y = y32 + 3
    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            if 0 <= x < 32 and 0 <= y < 32:
                tex = num2tex(current_tex)
                canvas.create_image(x * 32, y * 32, anchor=NW, image=tex)
                if app.show_grid:
                    canvas.create_rectangle(x * 32, y * 32, (x + 1) * 32, (y + 1) * 32, outline='black')
                app.change_map(x, y, current_tex)

#-----------------------------------------------------------
# GUI building
#-----------------------------------------------------------

# Menu
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New...", command=menu_file_new)
filemenu.add_command(label="Open...", command=menu_file_open)
filemenu.add_command(label="Save", command=menu_file_save)
filemenu.add_command(label="Save As...", command=menu_file_save_as)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=menu_file_exit)

editmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Edit", menu=editmenu)

varShowGrid = BooleanVar()
varShowGrid.set(app.show_grid)
varShowGrid.trace('r', app.get_show_grid)
varShowGrid.trace('w', app.set_show_grid)

viewmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="View", menu=viewmenu)
viewmenu.add_command(label="Toolbar")
viewmenu.add_command(label="Status Bar")
viewmenu.add_command(label="Animate")
viewmenu.add_command(label="Mini Map")
viewmenu.add_checkbutton(label="Show Grid", variable=varShowGrid)

toolsmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Tools", menu=toolsmenu)
toolsmenu.add_command(label="Check", command=menu_tools_check)
toolsmenu.add_command(label="Export image", command=menu_tools_image)

varPlayer = IntVar()
varPlayer.set(1)

playermenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Player", menu=playermenu)
playermenu.add_radiobutton(label="Player 1", variable=varPlayer, value=1)
playermenu.add_radiobutton(label="Player 2", variable=varPlayer, value=2)

helpmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)

# Frame & button bar
content = Frame(root, width=600, height=600)
toolbar = Frame(content)

bt_new = Button(toolbar, image=icons['new'], width=32, height=32, command=menu_file_new)
bt_open = Button(toolbar, image=icons['open'], width=32, height=32, command=menu_file_open)
bt_save = Button(toolbar, image=icons['save'], width=32, height=32, command=menu_file_save)
bt_save_as = Button(toolbar, image=icons['save_as'], width=32, height=32, command=menu_file_save_as)

bt_pencils = {}
bt_pencils['1x1'] = Button(toolbar, image=icons['1x1'], width=32, height=32, command=lambda: set_pencil('1x1'), relief=SUNKEN)
bt_pencils['3x3'] = Button(toolbar, image=icons['3x3'], width=32, height=32, command=lambda: set_pencil('3x3'), relief=RAISED)
bt_pencils['5x5'] = Button(toolbar, image=icons['5x5'], width=32, height=32, command=lambda: set_pencil('5x5'), relief=RAISED)
#bt_pencils['1x1'].config(relief=SUNKEN)

bt_all = {}
for _, tex in textures.items():
    bt_all[tex.name] = Button(toolbar, image=tex.tkimg, width=32, height=32, command=partial(bt_refresh, tex.tkimg))
    if current_tex == tex.num:
        bt_all[tex.name].config(relief=SUNKEN)

# Canvas
x_scrollbar = Scrollbar(content, orient=HORIZONTAL)
y_scrollbar = Scrollbar(content, orient=VERTICAL)
canvas = Canvas(content,
                scrollregion=(0, 0, 32*32, 32*32),
                xscrollcommand=x_scrollbar.set,
                yscrollcommand=y_scrollbar.set)
app.link_canvas(canvas)

# Status
status = Label(content, textvariable = status_var, relief=SUNKEN, anchor=E)

# Packing
content.pack(fill=BOTH,expand=True)
toolbar.pack(side=TOP, fill=X)
y_scrollbar.pack(side=RIGHT, fill=Y)
x_scrollbar.pack(side=BOTTOM, fill=X)
canvas.pack(side=TOP, fill=BOTH, expand=True)
x_scrollbar.config(command=canvas.xview)
y_scrollbar.config(command=canvas.yview)
status.pack(side=BOTTOM, fill=X)

bt_new.pack(side=LEFT)
bt_open.pack(side=LEFT)
bt_save.pack(side=LEFT)
bt_save_as.pack(side=LEFT)
sep1 = Label(toolbar, text=" ")
sep1.pack(side=LEFT)

for _, bt in bt_pencils.items():
    bt.pack(side=LEFT)
sep2 = Label(toolbar, text=" ")
sep2.pack(side=LEFT)

for _, bt in bt_all.items():
    bt.pack(side=LEFT)

# Canvas
#canvas.create_line(0, 0, 200, 100)
#canvas.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
#canvas.create_rectangle(50, 25, 150, 75, fill="blue")
#canvas.create_text(canvas_width / 2, canvas_height / 2, text="Python")
canvas.bind('<ButtonPress-1>', put_texture)
canvas.bind('<B1-Motion>', put_texture)
#canvas.bind('<ButtonRelease-1>', end_texture)
canvas.bind('<Motion>', refresh_status_bar)

#-----------------------------------------------------------
# Main
#-----------------------------------------------------------

if __name__ == "__main__":
    app.create_map("New map", 32, 32, mod_data["ground_default"])
    root.mainloop()
