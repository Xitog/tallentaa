# Created the ‎lundi ‎6 ‎juin ‎2016 (début des tests tkinter)

import tkinter # as tk
from tkinter import ttk # not found in 2.7.11 but found in 3.5.1 :-)
from tkinter import filedialog
from tkinter import messagebox   


class Application():
    
    def __init__(self):
        # root widget, an ordinary window
        self.root = tkinter.Tk()
        self.set_title()
        self.root.iconbitmap(r'icons\iconyellowcube16x19_F5i_icon.ico')
        self.root.minsize(width=800, height=600)
        self.update()
        self.make_menu()
        self.make_status_bar()
        self.frame = MyFrame(self.root)
        self.text = self.frame.text
    
    def update(self):
        print("hello")
        self.root.after(1000, self.update)

    def set_title(self, filename=None):
        if filename is None:
            self.root.wm_title("Forge - New *")
        else:
            self.root.wm_title("Forge - " + filename)
    
    def make_menu(self):
        self.menu = tkinter.Menu(self.root)
        self.root.config(menu=self.menu)
        self.filemenu = tkinter.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="New", command=self.menu_new)
        self.filemenu.add_command(label="Open...", command=self.menu_open)
        self.filemenu.add_command(label="Save As...", command=self.menu_save)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.menu_exit)

        self.helpmenu = tkinter.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=self.helpmenu)
        self.helpmenu.add_command(label="About...", command=self.menu_about)
    
    def make_status_bar(self):
        self.status_bar = tkinter.Label(self.root, bd=1, relief=tkinter.SUNKEN, anchor=tkinter.W)
        self.status_bar.config(text="Hello!")
        #status_bar.update_idletasks()
        self.status_bar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
    
    def run(self):
        self.frame.mainloop()
        # root.destroy()
    
    #-------------------------------------------------------
    # Menu functions
    #-------------------------------------------------------
    
    def menu_about(self):
        messagebox.showinfo("About", "Jyx - Damien Gouteux, 2017. Made with ❤")

    def menu_exit(self):
        self.root.destroy()
        #root.quit()
        #exit(0)

    def menu_new(self):
        self.new()
    
    def menu_open(self):
        """Returns an opened file in read mode."""
        options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'myfile.txt'
        options['parent'] = self.root
        options['title'] = 'This is a title'
        self.load(filedialog.askopenfilename(**options))

    def menu_save(self):
        options = {}
        #options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'myfile.txt'
        options['parent'] = self.root
        options['title'] = 'This is a title'
        filename = filedialog.asksaveasfilename(**options)
        if filename:
            self.save(filename)

    #-------------------------------------------------------
    # Text functions
    #-------------------------------------------------------

    def new(self):
        self.clear()
        self.set_title()
    
    def clear(self):
        self.text.delete("1.0", tkinter.END)

    def load(self, filename : str):
        self.text.delete("1.0", tkinter.END)
        f = open(filename, mode='r')
        content = f.read()
        f.close()
        self.clear()
        self.text.insert("1.0", content)
        self.set_title(filename)

    def save(self, filename : str):
        f = open(filename, mode='w')
        content = self.text.get(1.0, tkinter.END)
        f.write(content)
        f.close()
        self.set_title(filename)


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

    def make_text(self: tkinter.Frame): # with pack: scrollbar too big when expanding
        self.text_frame = tkinter.Frame(self)
        self.text_frame.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=tkinter.YES)
        
        self.text = tkinter.Text(self.text_frame)
        self.text.config(font=("consolas", 12), undo=True, wrap='word')
        self.text.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.YES)
        
        # Tabs
        def tab(arg):
            print("tab pressed")
            self.text.insert(tkinter.INSERT, " " * 4)
            return 'break' # Prevent normal behavior
        self.text.bind("<Tab>", tab)
        
        # Scrollbar
        self.scrollbar = tkinter.Scrollbar(self.text_frame, command=self.text.yview)
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=tkinter.YES)
        self.text['yscrollcommand'] = self.scrollbar.set

    def make_text(self: tkinter.Frame): # with grid: ok :-)
        self.text_frame = tkinter.Frame(self, bd=2, relief=tkinter.SUNKEN)

        self.text_frame.grid_rowconfigure(0, weight=1)
        self.text_frame.grid_columnconfigure(0, weight=1)

        #self.xscrollbar = tkinter.Scrollbar(self.text_frame, orient=tkinter.HORIZONTAL)
        #self.xscrollbar.grid(row=1, column=0, sticky=tkinter.E+tkinter.W)

        self.yscrollbar = tkinter.Scrollbar(self.text_frame)
        self.yscrollbar.grid(row=0, column=1, sticky=tkinter.N+tkinter.S)

        self.text = tkinter.Text(self.text_frame, wrap=tkinter.NONE, bd=0,
                    #xscrollcommand=self.xscrollbar.set,
                    yscrollcommand=self.yscrollbar.set)
        self.text.config(font=("consolas", 12), undo=True, wrap='word')
        
        self.text.grid(row=0, column=0, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)

        #self.xscrollbar.config(command=self.text.xview)
        self.yscrollbar.config(command=self.text.yview)

        self.text_frame.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=tkinter.YES)
    
    def build(self):
        self.make_tree()
        # self.make_buttons()
        self.make_text()
    
    def hello(self):
        print("hello!")

if __name__ == "__main__":
    Application().run()

