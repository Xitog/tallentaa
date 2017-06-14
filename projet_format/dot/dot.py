import tkinter
import os.path
import os

def refresh():
    global photo, label
    os.chdir(r"C:\QuickGraphTmpDir")
    os.system("dot.exe -Tpng pipo.txt -O")
    photo = tkinter.PhotoImage(file=fname)
    label.configure(image=photo)
    label.image = photo

root = tkinter.Tk()
root.wm_title("Dot on Python")
root.iconbitmap(r'D:\Tools\Scripts\Python27\DLLs\pyc.ico')

photo = None

fname = r"C:\QuickGraphTmpDir\pipo.txt.png"

frame = tkinter.Frame(root)
frame.pack(fill=tkinter.BOTH, expand=1)

if os.path.isfile(fname):
    photo = tkinter.PhotoImage(file=fname)

if photo is not None:
    label = tkinter.Label(frame, image=photo)
else:
    label = tkinter.Label(frame, text="No picture")
label.image = photo # keep a reference!
label.pack()

buttons = tkinter.Frame(frame, bg="blue")
#buttons.pack(fill=tkinter.BOTH, expand=1)
buttons.pack()

button_refresh = tkinter.Button(buttons, text="Refresh", fg="green", command=refresh)
button_refresh.pack(side=tkinter.LEFT, padx=3)
button_quit = tkinter.Button(buttons, text="Quit", fg="red", command=frame.quit)
button_quit.pack(side=tkinter.LEFT, padx=3)


root.mainloop()
try:
    root.destroy()
except tkinter.TclError:
    print("ok")

# 12h43 : yes ! display a picture
# 13h58 : yes ! refresh is working!
# 14h38 : on peut avoir du HTML dans dot !
# p16 on peut faire des rangs aussi
# p18 on peut faire des ports aussi
# 14h55 : on peut avoir des fleches bidirectionnelles :-)
