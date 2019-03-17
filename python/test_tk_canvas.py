from tkinter import *

canvas_width = 200
canvas_height = 100

root = Tk()

# Menu

def NewFile():
    print("New File!")

def OpenFile():
    name = askopenfilename()
    print(name)

def About():
    print("This is a simple example of a menu")

def End():
    canvas.destroy()
    root.quit()

menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=NewFile)
filemenu.add_command(label="Open...", command=OpenFile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=End)

helpmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)

# Canvas
canvas = Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

canvas.create_line(0, 0, 200, 100)
canvas.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
canvas.create_rectangle(50, 25, 150, 75, fill="blue")
canvas.create_text(canvas_width / 2, canvas_height / 2, text="Python")

img = PhotoImage(file=r"assets\others\terrain_1\hills.png")
canvas.create_image(20,20, anchor=NW, image=img)

mainloop()

#import sys
#from PySide2.QtWidgets import QApplication, QLabel
                                                   
if __name__ == "__main__":
    #app = QApplication(sys.argv)
    #label = QLabel("Hello World")
    #label.show()
    #sys.exit(app.exec_())
    pass
