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
    
    #16h13 : première image affichée !
    #16h15 : YES !
    pi = PhotoImage(file="icons/Crystal_Clear_device_blockdevice16.png")
    iconblue = PhotoImage(file="icons/IconBlueCube16x19.png")
    iconyellow = PhotoImage(file="icons/IconYellowCube16x19.png")
    iconmagenta = PhotoImage(file="icons/IconMagentaCube16x19.png")
    
    treeview = ttk.Treeview(frame)
    treeview["columns"] = ("text",)
    treeview.column("text", width=80)
    treeview.heading("text", text="Text")
    treeview.insert("", 0, text="First entry")
    treeview.insert("", 1, text=" Second entry", image=pi)
    sub1 = treeview.insert("", 2, text=" Third entry", image=iconyellow)
    treeview.insert(sub1, 0, text=" 2-1 Entry", image=iconblue)
    treeview.insert(sub1, 1, text=" 2-2 Entry", image=iconmagenta)
    # or
    treeview.insert("", 3, "sub2", text="Fourth entry")
    treeview.insert("sub2", 0, text=" 3-1 Entry", image=iconyellow)
    
    treeview.pack(side=BOTTOM)
    
    # make the root widget appears
    root.mainloop()
    # can be necessary to truly terminate the app
    # root.destroy()

def hello():
    print("hello!")

if __name__ == "__main__":
    main()