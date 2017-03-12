from tkinter import *
from tkinter import filedialog
from tkinter import messagebox   
#from tkinter.filedialog import *

# global : pour changer ou déclarer in a function

# 00h40 : Tkinter relit les fichiers... mais je croyais déjà l'avoir fait !!! Chez mes parents sans save ???
# http://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format os.path.basename
# http://stackoverflow.com/questions/2395431/using-tkinter-in-python-to-edit-the-title-bar root.vm_title
# http://stackoverflow.com/questions/5322027/how-to-erase-everything-from-the-tkinter-text-widget txt.delete("1.0", END)
# http://effbot.org/tkinterbook/tkinter-standard-dialogs.htm
# 045 : fin PC

# [ok] charger
# sauvegarder
# colorisation du format log
# colorisation du format lua
# undo/redo

mode = 'TEXT'

def clear():
    root.wm_title("* New")
    txt.delete("1.0", END)

def load(filename : str):
    txt.delete("1.0", END)
    f = open(filename, mode='r')
    content = f.read()
    f.close()
    clear()
    txt.insert("1.0", content)
    root.wm_title(filename)

def save(filename : str):
    f = open(filename, mode='w')
    content = txt.get(1.0,END)
    f.write(content)
    f.close()
    root.wm_title(filename)

def callback():
    print("called the callback!")

def menu_about():
    messagebox.showinfo(
        "About",
        "Jyx - Damien Gouteux, 2017. Made with ❤"
    )

def menu_new():
    clear()

def menu_exit():
    root.destroy()
    #root.quit()
    #exit(0)

def menu_open():
    """Returns an opened file in read mode."""
    options = {}
    options['defaultextension'] = '.txt'
    options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
    options['initialdir'] = 'C:\\'
    options['initialfile'] = 'myfile.txt'
    options['parent'] = root
    options['title'] = 'This is a title'
    load(filedialog.askopenfilename(**options))

def menu_save():
    options = {}
    #options['defaultextension'] = '.txt'
    options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
    options['initialdir'] = 'C:\\'
    options['initialfile'] = 'myfile.txt'
    options['parent'] = root
    options['title'] = 'This is a title'
    filename = filedialog.asksaveasfilename(**options)
    if filename:
        save(filename)
    
root = Tk()
root.wm_title("* New")

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
filemenu.add_command(label="New", command=menu_new)
filemenu.add_command(label="Open...", command=menu_open)
filemenu.add_command(label="Save As...", command=menu_save)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=menu_exit)

helpmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=menu_about)

# toplevel = root.winfo_toplevel()

#------------------------------------------------
# Text
#------------------------------------------------

if mode == 'TEXT':

    options = {}
    
    txt = Text(root, *options)
    txt.pack()
    
    def tab(arg):
        print("tab pressed")
        txt.insert(INSERT, " " * 4)
        return 'break' # Prevent normal behavior
    
    txt.bind("<Tab>", tab)
    
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

