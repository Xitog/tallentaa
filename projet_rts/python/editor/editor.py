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
# GUI
#-----------------------------------------------------------

img = True
try:
    save = PhotoImage(file=r"icons\save.png")
    deep = PhotoImage(file=r"icons\deep-1.png")
    water = PhotoImage(file=r"icons\water-1.png")
    mud = PhotoImage(file=r"icons\mud-1.png")
    dry = PhotoImage(file=r"icons\dry-1.png")
    grass = PhotoImage(file=r"icons\grass-1.png")
    dark = PhotoImage(file=r"icons\dark-1.png")
except TclError:
    print("Unable to load image.")
    img = False

root.iconbitmap(r'icons\editor.ico')
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
    bt_tex_save = Button(toolbar, image=save, width=32, height=32)
    bt_tex_deep = Button(toolbar, image=deep, width=32, height=32)
    bt_tex_water = Button(toolbar, image=water, width=32, height=32)
    bt_tex_mud = Button(toolbar, image=mud, width=32, height=32)
    bt_tex_dry = Button(toolbar, image=dry, width=32, height=32)
    bt_tex_grass = Button(toolbar, image=grass, width=32, height=32)
    bt_tex_dark = Button(toolbar, image=dark, width=32, height=32)
else:
    bt_tex_save = Button(toolbar, text="Save")
    bt_tex_deep = Button(toolbar, text="De")
    bt_tex_water = Button(toolbar, text="Wa")
    bt_tex_mud = Button(toolbar, text="Mu")
    bt_tex_dry = Button(toolbar, text="Dr")
    bt_tex_grass = Button(toolbar, text="Gr")
    bt_tex_dark = Button(toolbar, text="Da")

sep1 = Label(toolbar, text=" ")
canvas = Canvas(content)
status = Label(content, text="Status bar", relief=SUNKEN, anchor=E)

content.pack(fill=BOTH,expand=True)
toolbar.pack(side=TOP, fill=X)
canvas.pack(side=TOP, fill=BOTH, expand=True)
status.pack(side=BOTTOM, fill=X)
bt_tex_save.pack(side=LEFT)
sep1.pack(side=LEFT)
bt_tex_deep.pack(side=LEFT)
bt_tex_water.pack(side=LEFT)
bt_tex_mud.pack(side=LEFT)
bt_tex_dry.pack(side=LEFT)
bt_tex_grass.pack(side=LEFT)
bt_tex_dark.pack(side=LEFT)

canvas.create_line(0, 0, 200, 100)
canvas.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
canvas.create_rectangle(50, 25, 150, 75, fill="blue")
canvas.create_text(canvas_width / 2, canvas_height / 2, text="Python")

#canvas.create_image(20,20, anchor=NW, image=img)

root.mainloop()
                                         
if __name__ == "__main__":
    pass
