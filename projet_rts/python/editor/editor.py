#-----------------------------------------------------------
# Map Editor for 2D square maps (RTS, RPG)
#-----------------------------------------------------------
# Created: May 11, 2019
# Modified: May 13, 2019

# Imports
# Constants & Global variables
# Menu actions
# Button actions
# Apply texture functions
# GUI
# Main

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

#-----------------------------------------------------------
# Constants & Global variables
#-----------------------------------------------------------

canvas_width = 200
canvas_height = 100

root = Tk()

# Load images
img = True
try:
    root.iconbitmap(r'media\icons\editor.ico')
    save = PhotoImage(file=r"media\icons\save.png")
    deep = PhotoImage(file=r"media\icons\deep-1.png")
    water = PhotoImage(file=r"media\icons\water-1.png")
    mud = PhotoImage(file=r"media\icons\mud-1.png")
    dry = PhotoImage(file=r"media\icons\dry-1.png")
    grass = PhotoImage(file=r"media\icons\grass-1.png")
    dark = PhotoImage(file=r"media\icons\dark-1.png")
except TclError:
    print("Unable to load image.")
    img = False

# Texture codes
DEEP = -2
WATER = -1
MUD = 0
DRY = 1
GRASS = 2
DARK = 3

application_title = 'Map editor'
current_tex = WATER
pencil='1x1'
status_var =  StringVar()
status_var.set('Welcome')
current_map = None
dic = { DEEP : deep, WATER : water, MUD : mud, DRY : dry, GRASS : grass, DARK : dark }

#-----------------------------------------------------------
# Map functions
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
    return dic[n]

#-----------------------------------------------------------
# Menu actions
#-----------------------------------------------------------

def NewFile():
    print("New File!")

def OpenFile():
    name = askopenfilename()
    print(name)

def About():
    showinfo("About", "This is a simple example of a menu")

def menu_file_quit():
    global canvas, root
    canvas.destroy()
    root.destroy()

def menu_tools_check():
    print('Checking map conformity')

def menu_tools_image():
    pass
    
def menu_file_save_as():
    filepath = asksaveasfilename(initialdir = os.getcwd(),title = "Select where to save", filetypes = (("map files","*.map"),("all files","*.*")))
    if filepath != '':
        if not filepath.endswith('.map'):
            filepath += '.map'
        bn = os.path.basename(filepath)
        n = os.path.splitext(bn)[0]
        current_map.set_name(n)
        current_map.to_json(filepath, True)
        root.title(f"{application_title} - {n}")

#-----------------------------------------------------------
# Button actions
#-----------------------------------------------------------

def cmd_save():
    pass

def cmd_deep():
    global current_tex
    current_tex = DEEP
    bt_tex_deep.config(relief=SUNKEN)
    bt_tex_water.config(relief=RAISED)
    bt_tex_mud.config(relief=RAISED)
    bt_tex_dry.config(relief=RAISED)
    bt_tex_grass.config(relief=RAISED)
    bt_tex_dark.config(relief=RAISED)
    
def cmd_water():
    global current_tex
    current_tex = WATER
    bt_tex_deep.config(relief=RAISED)
    bt_tex_water.config(relief=SUNKEN)
    bt_tex_mud.config(relief=RAISED)
    bt_tex_dry.config(relief=RAISED)
    bt_tex_grass.config(relief=RAISED)
    bt_tex_dark.config(relief=RAISED)

def cmd_mud():
    global current_tex
    current_tex = MUD
    bt_tex_deep.config(relief=RAISED)
    bt_tex_water.config(relief=RAISED)
    bt_tex_mud.config(relief=SUNKEN)
    bt_tex_dry.config(relief=RAISED)
    bt_tex_grass.config(relief=RAISED)
    bt_tex_dark.config(relief=RAISED)

def cmd_dry():
    global current_tex
    current_tex = DRY
    bt_tex_deep.config(relief=RAISED)
    bt_tex_water.config(relief=RAISED)
    bt_tex_mud.config(relief=RAISED)
    bt_tex_dry.config(relief=SUNKEN)
    bt_tex_grass.config(relief=RAISED)
    bt_tex_dark.config(relief=RAISED)

def cmd_grass():
    global current_tex
    current_tex = GRASS
    bt_tex_deep.config(relief=RAISED)
    bt_tex_water.config(relief=RAISED)
    bt_tex_mud.config(relief=RAISED)
    bt_tex_dry.config(relief=RAISED)
    bt_tex_grass.config(relief=SUNKEN)
    bt_tex_dark.config(relief=RAISED)

def cmd_dark():
    global current_tex
    current_tex = DARK
    bt_tex_deep.config(relief=RAISED)
    bt_tex_water.config(relief=RAISED)
    bt_tex_mud.config(relief=RAISED)
    bt_tex_dry.config(relief=RAISED)
    bt_tex_grass.config(relief=RAISED)
    bt_tex_dark.config(relief=SUNKEN)

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
    if 0 <= x32 < 32 and 0 <= y32 < 32:
        tex = num2tex(current_tex)
        canvas.create_image(x32 * 32, y32 * 32, anchor=NW, image=tex)
        current_map.set(y32, x32, current_tex)

#-----------------------------------------------------------
# GUI
#-----------------------------------------------------------

root.title(f"{application_title} - New map")

# Menu
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New...", command=NewFile)
filemenu.add_command(label="Open...", command=OpenFile)
filemenu.add_command(label="Save", command=OpenFile)
filemenu.add_command(label="Save As...", command=menu_file_save_as)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=menu_file_quit)

editmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Edit", menu=editmenu)

viewmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="View", menu=viewmenu)
viewmenu.add_command(label="Toolbar")
viewmenu.add_command(label="Status Bar")
viewmenu.add_command(label="Animate")
viewmenu.add_command(label="Mini Map")

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
if img:
    bt_tex_save = Button(toolbar, image=save, width=32, height=32, command=cmd_save)
    bt_tex_deep = Button(toolbar, image=deep, width=32, height=32, command=cmd_deep)
    bt_tex_water = Button(toolbar, image=water, width=32, height=32, command=cmd_water, relief=SUNKEN)
    bt_tex_mud = Button(toolbar, image=mud, width=32, height=32, command=cmd_mud)
    bt_tex_dry = Button(toolbar, image=dry, width=32, height=32, command=cmd_dry)
    bt_tex_grass = Button(toolbar, image=grass, width=32, height=32, command=cmd_grass)
    bt_tex_dark = Button(toolbar, image=dark, width=32, height=32, command=cmd_dark)
else:
    bt_tex_save = Button(toolbar, text="Save")
    bt_tex_deep = Button(toolbar, text="De")
    bt_tex_water = Button(toolbar, text="Wa")
    bt_tex_mud = Button(toolbar, text="Mu")
    bt_tex_dry = Button(toolbar, text="Dr")
    bt_tex_grass = Button(toolbar, text="Gr")
    bt_tex_dark = Button(toolbar, text="Da")

sep1 = Label(toolbar, text=" ")
x_scrollbar = Scrollbar(content, orient=HORIZONTAL)
y_scrollbar = Scrollbar(content, orient=VERTICAL)
canvas = Canvas(content,
                scrollregion=(0, 0, 32*32, 32*32),
                xscrollcommand=x_scrollbar.set,
                yscrollcommand=y_scrollbar.set)
status = Label(content, textvariable = status_var, relief=SUNKEN, anchor=E)

content.pack(fill=BOTH,expand=True)
toolbar.pack(side=TOP, fill=X)
y_scrollbar.pack(side=RIGHT, fill=Y)
x_scrollbar.pack(side=BOTTOM, fill=X)
canvas.pack(side=TOP, fill=BOTH, expand=True)
x_scrollbar.config(command=canvas.xview)
y_scrollbar.config(command=canvas.yview)
status.pack(side=BOTTOM, fill=X)
bt_tex_save.pack(side=LEFT)
sep1.pack(side=LEFT)
bt_tex_deep.pack(side=LEFT)
bt_tex_water.pack(side=LEFT)
bt_tex_mud.pack(side=LEFT)
bt_tex_dry.pack(side=LEFT)
bt_tex_grass.pack(side=LEFT)
bt_tex_dark.pack(side=LEFT)

# Canvas
canvas.create_line(0, 0, 200, 100)
canvas.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
canvas.create_rectangle(50, 25, 150, 75, fill="blue")
canvas.create_text(canvas_width / 2, canvas_height / 2, text="Python")
canvas.bind('<ButtonPress-1>', put_texture)
canvas.bind('<B1-Motion>', put_texture)
#canvas.bind('<ButtonRelease-1>', end_texture)
canvas.bind('<Motion>', refresh_status_bar)

#-----------------------------------------------------------
# Main
#-----------------------------------------------------------

if __name__ == "__main__":
    current_map = Map('New', 32, 32, 2)
    for row in range(0, 32):
        for col in range(0, 32):
            val = current_map.get(row, col)
            tex = num2tex(val)
            canvas.create_image(row * 32, col * 32, anchor=NW, image=tex)
    root.mainloop()
