from tkinter import *
from tkinter import filedialog
from tkinter import font

def callback():
    print("called the callback!")

def menu_exit():
    global root
    root.destroy()

def menu_load():
    """Returns an opened file in read mode."""
    global txt
    options = {}
    options['defaultextension'] = '.txt'
    options['filetypes'] = [('text files', '.txt'), ('python files', '.py'), ('lua files', '.lua'), ('all files', '.*')]
    options['initialdir'] = 'C:\\'
    options['initialfile'] = 'myfile.txt'
    options['parent'] = root
    options['title'] = 'Load file...'
    f = filedialog.askopenfile(mode='r', **options)
    s = f.read()
    f.close()
    txt.delete(1.0, END) 
    txt.insert(END, s)

def menu_save():
    global txt
    options['defaultextension'] = '.txt'
    options['filetypes'] = [('text files', '.txt'), ('python files', '.py'), ('lua files', '.lua'), ('all files', '.*')]
    options['initialdir'] = 'C:\\'
    options['initialfile'] = 'myfile.txt'
    options['parent'] = root
    options['title'] = 'Save file...'
    f = filedialog.asksaveasfile(mode='w', **options)
    s = txt.get(1.0, END)
    f.write(s)
    f.close()
    
root = Tk()
root.title("Jyx")
root.geometry("600x400")

#------------------------------------------------
# Menu
#------------------------------------------------

menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=callback)
filemenu.add_command(label="Open...", command=menu_load)
filemenu.add_command(label="Save...", command=menu_save)
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

pol_cn_bold = font.Font(family='Courier New', size=10, weight='bold')
tag_keyword = txt.tag_config("keyword", foreground="blue", font=pol_cn_bold)

def key(event):
    global txt
    #print("pressed", repr(event.char))
    s = txt.get(1.0, END)
    w = ''
    start = 1
    for i in range(0, len(s)):
        w += s[i]
        if w == 'lua ':
            print("youpi!")
            deb = '1.0+%ic' % start
            print(deb)
            end = '1.0+%ic' % i
            print(end)
            txt.tag_add("keyword", deb, end)
            w = ''
            start = i
        print(w, len(w))

txt.bind("<KeyRelease>", key)

#------------------------------------------------
# Status bar
#------------------------------------------------

status_bar = Label(root, bd=1, relief=SUNKEN, anchor=W)
status_bar.config(text="Hello!")
#status_bar.update_idletasks()
status_bar.pack(side=BOTTOM, fill=X)

mainloop()

