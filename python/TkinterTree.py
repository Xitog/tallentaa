# Created the ‎lundi ‎6 ‎juin ‎2016 (début des tests tkinter)

import tkinter # as tk
from tkinter import ttk # not found in 2.7.11 but found in 3.5.1 :-)

class Application(tkinter.Frame):
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
    # root widget, an ordinary window
    root = tkinter.Tk()
    root.wm_title("Forge")
    root.minsize(width=800, height=600)
    app = Application(master=root)
    app.mainloop()
    # root.destroy()
