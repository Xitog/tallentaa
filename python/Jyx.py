from tkinter import *
from tkinter import filedialog

def callback():
    print("called the callback!")

def menu_exit():
    global root
    root.destroy()

def menu_askopenfile():
    global txt
    """Returns an opened file in read mode."""
    options = {}
    options['defaultextension'] = '.txt'
    options['filetypes'] = [('text files', '.txt'), ('python files', '.py'), ('lua files', '.lua'), ('all files', '.*')]
    options['initialdir'] = 'C:\\'
    options['initialfile'] = 'myfile.txt'
    options['parent'] = root
    options['title'] = 'This is a title'
    f = filedialog.askopenfile(mode='r', **options)
    s = f.read()
    txt.delete(1.0, END) 
    txt.insert(END, s)

root = Tk()

#------------------------------------------------
# Menu
#------------------------------------------------

menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=callback)
filemenu.add_command(label="Open...", command=menu_askopenfile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=menu_exit)

helpmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=callback)

#------------------------------------------------
# Text
#------------------------------------------------

options = {}
txt = Text(root, *options)
txt.pack()

#------------------------------------------------
# Status bar
#------------------------------------------------

status_bar = Label(root, bd=1, relief=SUNKEN, anchor=W)
status_bar.config(text="Hello!")
#status_bar.update_idletasks()
status_bar.pack(side=BOTTOM, fill=X)

mainloop()

