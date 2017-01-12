from tkinter import *
from tkinter import filedialog
#from tkinter.filedialog import *

mode = 'TEXT'

def callback():
    print("called the callback!")

def menu_exit():
    global root
    root.destroy()
    #root.quit()
    #exit(0)

def menu_askopenfile():
    """Returns an opened file in read mode."""
    options = {}
    options['defaultextension'] = '.txt'
    options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
    options['initialdir'] = 'C:\\'
    options['initialfile'] = 'myfile.txt'
    options['parent'] = root
    options['title'] = 'This is a title'
    return filedialog.askopenfile(mode='r', **options)

root = Tk()

if mode == 'CANVAS':
    try:
        # Only for windows
        root.state("zoomed")
    except Exception as e:
        print(e)

# root.minsize(root.winfo_screenwidth(), root.winfo_screenheight())
# print(root.wm_maxsize())

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

# toplevel = root.winfo_toplevel()

#------------------------------------------------
# Text
#------------------------------------------------

if mode == 'TEXT':

    options = {}
    txt = Text(root, *options)
    txt.pack()
    
#------------------------------------------------
# Canvas
#------------------------------------------------

elif mode == 'CANVAS':
    
    w = Canvas(root, width=200, height=100)
    w.pack()

    w.create_line(0, 0, 200, 100)
    w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))

    w.create_rectangle(50, 25, 150, 75, fill="blue")

#------------------------------------------------
# Status bar
#------------------------------------------------

status_bar = Label(root, bd=1, relief=SUNKEN, anchor=W)
status_bar.config(text="Hello!")
#status_bar.update_idletasks()
status_bar.pack(side=BOTTOM, fill=X)

mainloop()

