# Created the ‎lundi ‎6 ‎juin ‎2016 (début des tests tkinter)

import tkinter # as tk
from tkinter import ttk # not found in 2.7.11 but found in 3.5.1 :-)
from tkinter import messagebox   

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

class Application():
    
    def __init__(self):
        # root widget, an ordinary window
        self.root = tkinter.Tk()
        self.root.wm_title("Forge")
        self.root.iconbitmap(r'icons\iconyellowcube16x19_F5i_icon.ico')
        self.root.minsize(width=800, height=600)
        self.make_menu()
        self.make_status_bar()
        self.frame = MyFrame(self.root)
    
    def make_menu(self):
        self.menu = tkinter.Menu(self.root)
        self.root.config(menu=self.menu)
        self.filemenu = tkinter.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="New", command=menu_new)
        self.filemenu.add_command(label="Open...", command=menu_open)
        self.filemenu.add_command(label="Save As...", command=menu_save)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=menu_exit)

        self.helpmenu = tkinter.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=self.helpmenu)
        self.helpmenu.add_command(label="About...", command=menu_about)
    
    def make_status_bar(self):
        self.status_bar = tkinter.Label(self.root, bd=1, relief=tkinter.SUNKEN, anchor=tkinter.W)
        self.status_bar.config(text="Hello!")
        #status_bar.update_idletasks()
        self.status_bar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
    
    def run(self):
        self.frame.mainloop()
        # root.destroy()

class MyFrame(tkinter.Frame):
    """ Extend a Frame, a global container"""
    
    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.pack(fill=tkinter.BOTH, expand=tkinter.YES) # make it visible
        self.graphics = {}
        self.build()
    
    def make_tree(self: tkinter.Frame):
        # Loading icons
        self.graphics['pi'] = tkinter.PhotoImage(file="icons/Crystal_Clear_device_blockdevice16.png")
        self.graphics['iconblue'] = tkinter.PhotoImage(file="icons/IconBlueCube16x19.png")
        self.graphics['iconyellow'] = tkinter.PhotoImage(file="icons/IconYellowCube16x19.png")
        self.graphics['iconmagenta'] = tkinter.PhotoImage(file="icons/IconMagentaCube16x19.png")
        # Creating tree
        treeview = ttk.Treeview(self)
        treeview["columns"] = ("text",)
        treeview.column("#0", width=120)
        treeview.heading("#0", text="Nodes")
        treeview.column("text", width=80)
        treeview.heading("text", text="Tag")
        treeview.insert("", 0, text="First entry")
        treeview.insert("", 1, text=" Second entry", image=self.graphics['pi'])
        sub1 = treeview.insert("", 2, text=" Third entry", image=self.graphics['iconyellow'])
        treeview.insert(sub1, 0, text=" 2-1 Entry", image=self.graphics['iconblue'])
        treeview.insert(sub1, 1, text=" 2-2 Entry", image=self.graphics['iconmagenta'])
        # or
        treeview.insert("", 3, "sub2", text="Fourth entry")
        treeview.insert("sub2", 0, text=" 3-1 Entry", image=self.graphics['iconyellow'])
        
        treeview.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.YES)
    
    def make_buttons(self: tkinter.Frame):
        # this label widget is a child of the frame widget
        label = tkinter.Label(self, text="Hello, world!")
        # size itself and make it visible. pack it relative to its parent
        label.pack(side=tkinter.RIGHT)
    
        button2 = tkinter.Button(self, text="Do it", fg="green", command=Application.hello)
        button2.pack(side=tkinter.BOTTOM)
        
        # this button widget is a child of the frame widget. fg = foreground.
        button = tkinter.Button(self, text="QUIT", fg="red", command=self.quit) # or root.destroy?
        button.pack(side=tkinter.BOTTOM)
    
        self.hi_there = tkinter.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.hello
        self.hi_there.pack(side="bottom")
        
    def build(self):
        self.make_tree()
        # self.make_buttons()
        text = tkinter.Text(self)
        text.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=tkinter.YES)
        
    @staticmethod
    def hello():
        print("hello!")

if __name__ == "__main__":
    Application().run()

