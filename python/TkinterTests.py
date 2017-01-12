# https://www.python.org/

# http://effbot.org/tkinterbook/tkinter-index.htm
# http://effbot.org/tkinterbook/tkinter-hello-tkinter.htm
# http://effbot.org/tkinterbook/tkinter-hello-again.htm

# http://effbot.org/tkinterbook/text.htm

# https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview

# http://knowpapa.com/ttk-treeview/
# https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview

from tkinter import *
from tkinter import ttk # not found in 2.7.11 but found in 3.5.1 :-)

def main():
    global hello
    # root widget, an ordinary window
    root = Tk()
    
    # a frame widget is a simple container
    frame = Frame(root)
    # make the frame visible (even if there is nothing in it yet)
    frame.pack()
    
    # this label widget is a child of the frame widget
    label = Label(frame, text="Hello, world!")
    # size itself and make it visible. pack it relative to its parent
    label.pack(side=LEFT)
    
    button2 = Button(frame, text="Do it", fg="green", command=hello)
    button2.pack(side=RIGHT)

    # this button widget is a child of the frame widget. fg = foreground.
    button = Button(frame, text="QUIT", fg="red", command=frame.quit)
    #
    button.pack(side=RIGHT)

    text = Text(frame)
    text.pack(side=BOTTOM)

    treeview = ttk.Treeview(frame)
    treeview["columns"] = ("text",)
    treeview.column("text", width=80)
    treeview.heading("text", text="Text")
    treeview.insert("", 0, text="First entry")
    treeview.insert("", 1, text="Second entry")
    sub1 = treeview.insert("", 2, text="Third entry")
    treeview.insert(sub1, 0, text="2-1 Entry")
    treeview.insert(sub1, 1, text="2-2 Entry")
    # or
    treeview.insert("", 3, "sub2", text="Fourth entry")
    treeview.insert("sub2", 0, text="3-1 Entry")
    
    treeview.pack(side=BOTTOM)
    
    # make the root widget appears
    root.mainloop()
    # can be necessary to truly terminate the app
    root.destroy()

def hello():
    print("hello!")

if __name__ == "__main__":
    main()
