#-----------------------------------------------------------
# Imports
#-----------------------------------------------------------

from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
#from tkinter.ttk import Treeview, Button

#-----------------------------------------------------------
# Constants & Global variables
#-----------------------------------------------------------

canvas_width = 200
canvas_height = 100

root = Tk()

#-----------------------------------------------------------
# Load images
#-----------------------------------------------------------

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

def End():
    global canvas, root
    canvas.destroy()
    root.destroy()

#-----------------------------------------------------------
# Button actions
#-----------------------------------------------------------

current_tex = water

def cmd_save():
    pass

def cmd_deep():
    global current_tex
    current_tex = deep
    bt_tex_deep.config(relief=SUNKEN)
    bt_tex_water.config(relief=RAISED)
    bt_tex_mud.config(relief=RAISED)
    bt_tex_dry.config(relief=RAISED)
    bt_tex_grass.config(relief=RAISED)
    bt_tex_dark.config(relief=RAISED)
    
def cmd_water():
    global current_tex
    current_tex = water
    bt_tex_deep.config(relief=RAISED)
    bt_tex_water.config(relief=SUNKEN)
    bt_tex_mud.config(relief=RAISED)
    bt_tex_dry.config(relief=RAISED)
    bt_tex_grass.config(relief=RAISED)
    bt_tex_dark.config(relief=RAISED)

def cmd_mud():
    global current_tex
    current_tex = mud
    bt_tex_deep.config(relief=RAISED)
    bt_tex_water.config(relief=RAISED)
    bt_tex_mud.config(relief=SUNKEN)
    bt_tex_dry.config(relief=RAISED)
    bt_tex_grass.config(relief=RAISED)
    bt_tex_dark.config(relief=RAISED)

def cmd_dry():
    global current_tex
    current_tex = dry
    bt_tex_deep.config(relief=RAISED)
    bt_tex_water.config(relief=RAISED)
    bt_tex_mud.config(relief=RAISED)
    bt_tex_dry.config(relief=SUNKEN)
    bt_tex_grass.config(relief=RAISED)
    bt_tex_dark.config(relief=RAISED)

def cmd_grass():
    global current_tex
    current_tex = grass
    bt_tex_deep.config(relief=RAISED)
    bt_tex_water.config(relief=RAISED)
    bt_tex_mud.config(relief=RAISED)
    bt_tex_dry.config(relief=RAISED)
    bt_tex_grass.config(relief=SUNKEN)
    bt_tex_dark.config(relief=RAISED)

def cmd_dark():
    global current_tex
    current_tex = dark
    bt_tex_deep.config(relief=RAISED)
    bt_tex_water.config(relief=RAISED)
    bt_tex_mud.config(relief=RAISED)
    bt_tex_dry.config(relief=RAISED)
    bt_tex_grass.config(relief=RAISED)
    bt_tex_dark.config(relief=SUNKEN)

#-----------------------------------------------------------
# GUI
#-----------------------------------------------------------

root.title("Editor")

# Menu
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New...", command=NewFile)
filemenu.add_command(label="Open...", command=OpenFile)
filemenu.add_command(label="Save", command=OpenFile)
filemenu.add_command(label="Save As...", command=OpenFile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=End)

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

varPlayer = IntVar()
varPlayer.set(1)

playermenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Player", menu=playermenu)
playermenu.add_radiobutton(label="Player 1", variable=varPlayer, value=1)
playermenu.add_radiobutton(label="Player 2", variable=varPlayer, value=2)

helpmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)

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
status = Label(content, text="Status bar", relief=SUNKEN, anchor=E)

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

applyTex = False

def startTex(event):
    global applyTex
    applyTex = True
    putTex(event)

def putTex(event):
    if applyTex:
        canvas = event.widget
        x32 = canvas.canvasx(event.x) // 32
        y32 = canvas.canvasy(event.y) // 32
        print(x32, y32)
        if 0 <= x32 < 32 and 0 <= y32 < 32:
            canvas.create_image(x32 * 32, y32 * 32, anchor=NW, image=current_tex)

def endTex(event):
    global applyTex
    applyTex = False



canvas.create_line(0, 0, 200, 100)
canvas.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
canvas.create_rectangle(50, 25, 150, 75, fill="blue")
canvas.create_text(canvas_width / 2, canvas_height / 2, text="Python")
canvas.bind('<ButtonPress-1>', startTex)
canvas.bind('<B1-Motion>', putTex)
canvas.bind('<ButtonRelease-1>', endTex)

for row in range(0, 32):
    for col in range(0, 32):
        canvas.create_image(row * 32, col * 32, anchor=NW, image=grass)

root.mainloop()
                                         
if __name__ == "__main__":
    pass
