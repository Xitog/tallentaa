import tkinter

class Jyx:

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.protocol('WM_DELETE_WINDOW', self.exit)
        self.update_title()
        self.dirty = False
        
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
        text.bind('<<Paste>>', self.paste)
        text.bind('<<Cut>>', self.cut)
        text.bind('<<Copy>>', self.copy)
        text.bind('<KeyPress>', self.update_text)
        #text.bind('<KeyRelease>', self.update_text)

        text.tag_config("a", foreground="blue", underline=1)
        
        frame.pack(fill=tkinter.BOTH, expand=tkinter.YES)

    def paste(self, event):
        content =  self.root.clipboard_get()
        event.widget.insert(tkinter.INSERT, content)
        return 'break'

    def cut(self, event):
        self.root.clipboard_clear()
        self.root.clipboard_append(event.widget.get(tkinter.SEL_FIRST, tkinter.SEL_LAST))        
        event.widget.delete(tkinter.SEL_FIRST, tkinter.SEL_LAST)
        return 'break'

    def copy(self, event):
        self.root.clipboard_clear()
        self.root.clipboard_append(event.widget.get(tkinter.SEL_FIRST, tkinter.SEL_LAST))
        return 'break'

    def update_title(self):
         self.root.wm_title('Jyx')

    def update_text(self, event):
        #print('updated!')
        insert = event.widget.index(tkinter.INSERT)
        if event.keycode == 37: # left
            event.widget.mark_set(tkinter.INSERT, f'{insert}-1c')
            return 'break'
        elif event.keycode == 39:
            event.widget.mark_set(tkinter.INSERT, f'{insert}+1c')
            return 'break'
        elif event.keycode == 8:
            #delete
            return 'break'
        elif event.char == '\r':
            content = '\n'
        elif event.char == '\t':
            content = '    '
        else:
            content = event.char
        print(event)
        event.widget.insert(tkinter.INSERT, content)
        c = event.widget.get("insert linestart", "insert lineend")
        print(c)
        if c.startswith('http://'):
            event.widget.tag_add('a', 'insert linestart', tkinter.INSERT)
        else:
            event.widget.tag_remove('a', 'insert linestart', tkinter.INSERT)
        return 'break'
    
    def exit(self, event=None):
        self.root.destroy()

if __name__ == '__main__':
    Jyx()

