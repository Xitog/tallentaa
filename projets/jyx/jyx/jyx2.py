import tkinter

class Jyx:

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.protocol('WM_DELETE_WINDOW', self.exit)
        self.update_title()
        
        frame = tkinter.Frame(self.root, bd=2, relief=tkinter.SUNKEN)
        # To make the element at 0,0 grows with the window
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        yscrollbar = tkinter.Scrollbar(frame)
        yscrollbar.grid(row=0, column=1, sticky=tkinter.N+tkinter.S)
        text = tkinter.Text(frame, wrap=tkinter.NONE, bd=0,
                            yscrollcommand=yscrollbar.set)
        text.config(font=('consolas', 12), undo=True, wrap='word')
        text.grid(row=0, column=0, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)
        
        frame.pack(fill=tkinter.BOTH, expand=tkinter.YES)

    def update_title(self):
         self.root.wm_title('Jyx')

    def exit(self, event=None):
        self.root.destroy()

if __name__ == '__main__':
    Jyx()

