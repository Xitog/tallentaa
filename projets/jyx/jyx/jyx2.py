import tkinter as tk
from tkinter import ttk

MENU_FILE = 'File'
MENU_FILE_NEW = 'New'
MENU_FILE_NEW_TAB = 'New Tab'
MENU_FILE_OPEN = 'Open...'
MENU_FILE_SAVE = 'Save As...'
MENU_FILE_RUN = 'Run Script'
MENU_FILE_EXIT = 'Exit'

class Jyx:

    def __init__(self):
        self.root = tk.Tk()
        self.root.protocol('WM_DELETE_WINDOW', self.exit)
        self.text = JyxText(self)
        self.menu = JyxMenu(self)
        self.root.config(menu=self.menu)
        self.update_title()
        self.root.mainloop()

    def get_root(self):
        return self.root

    def update_title(self):
        dirty = ' *' if self.text.dirty else ''
        self.root.wm_title('Jyx' + dirty)

    def exit(self, event=None):
        self.root.destroy()

    def new(self, event=None):
        pass

    def new_tab(self, event=None):
        pass

    def open(self, event=None):
        pass

    def save(self, event=None):
        pass

    def run(self, event=None):
        pass


class JyxMenu(tk.Menu):

    def __init__(self, parent):
        tk.Menu.__init__(self, parent.get_root())
        self.parent = parent
        self.filemenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label=MENU_FILE, menu=self.filemenu)
        self.filemenu.add_command(label=MENU_FILE_NEW, command=self.parent.new, accelerator="Ctrl+N")
        self.filemenu.add_command(label=MENU_FILE_NEW_TAB, command=self.parent.new_tab, accelerator="Ctrl+T")
        self.filemenu.add_command(label=MENU_FILE_OPEN, command=self.parent.open, accelerator="Ctrl+O")
        self.filemenu.add_command(label=MENU_FILE_SAVE, command=self.parent.save, accelerator="Ctrl+S")
        self.filemenu.add_separator()
        self.filemenu.add_command(label=MENU_FILE_RUN, command=self.parent.run, accelerator="F5")
        self.filemenu.add_separator()
        self.filemenu.add_command(label=MENU_FILE_EXIT, command=self.parent.exit, accelerator="Ctrl+Q")

        """
        self.editmenu = tkinter.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Edit", menu=self.editmenu)
        self.editmenu.add_command(label="Undo", command=self.menu_undo, accelerator="Ctrl+Z")
        self.editmenu.add_command(label="Redo", command=self.menu_redo, accelerator="Ctrl+Y")
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Cut", command=self.menu_cut, accelerator="Ctrl+X")
        self.editmenu.add_command(label="Copy", command=self.menu_copy, accelerator="Ctrl+C")
        self.editmenu.add_command(label="Paste", command=self.menu_paste, accelerator="Ctrl+V")
        self.editmenu.add_command(label="Select All", command=self.menu_select_all, accelerator="Ctrl+A")

        self.display_tree = tkinter.BooleanVar()
        self.display_tree.set(self.options['display_tree'])
        self.confirm_exit = tkinter.BooleanVar()
        self.confirm_exit.set(self.options['confirm_exit'])

        self.options_menu = tkinter.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Options", menu=self.options_menu)
        self.options_menu.add_checkbutton(label="Display Tree", onvalue=True, offvalue=False, variable=self.display_tree, command=self.restart)
        self.options_menu.add_checkbutton(label="Confirm Exit", onvalue=True, offvalue=False, variable=self.confirm_exit, command=self.save_opt)

        # Language
        self.log.info(f"{len(languages)} language definitions loaded.")
        self.lang = tkinter.StringVar()
        if self.options['lang'] not in languages:
            self.log.error(f"{self.options['lang']} not in known languages. Reseting to {languages[default_language]['label']}.")
            self.lang.set(default_language)
        else:
            self.lang.set(self.options['lang'])
        self.log.info("self.lang = " + self.lang.get())

        self.langmenu = tkinter.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Language", menu=self.langmenu)

        base = {}
        families = {}
        for lang, prop in languages.items():
            if prop['family'] is None:
                base[lang] = prop
                continue
            elif prop['family'] not in families:
                families[prop['family']] = {}
            families[prop['family']][lang] = prop
        for lang in sorted(base):
            self.langmenu.add_radiobutton(label=languages[lang]['label'], variable=self.lang, value=lang, command=self.update_lang)
        self.langmenu.add_separator()
        for fam in sorted(families):
            menu = tkinter.Menu(self.langmenu, tearoff=0)
            self.langmenu.add_cascade(label=fam, menu=menu)
            for lang in sorted(families[fam]):
                menu.add_radiobutton(label=languages[lang]['label'], variable=self.lang, value=lang, command=self.update_lang)#, indicatoron=0

        if not lang_has(self.options['lang'], 'execute'):
            self.filemenu.entryconfig(Application.RUN_COMMAND, state=tkinter.DISABLED)
        
        self.helpmenu = tkinter.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=self.helpmenu)
        self.helpmenu.add_command(label="About...", command=self.menu_about)

        self.root.bind('<Control-n>', self.menu_new)
        self.root.bind('<Control-t>', self.menu_new_tab)
        self.root.bind('<Control-o>', self.menu_open)
        self.root.bind('<Control-s>', self.menu_save)
        self.root.bind('<Control-q>', self.menu_exit)
        self.root.bind('<Control-a>', self.menu_select_all)
        self.root.bind('<Control-z>', self.menu_undo)
        self.root.bind('<Control-y>', self.menu_redo)
        self.root.bind('<F5>', self.menu_exec)
        """

class JyxText(tk.Text):

    def __init__(self, parent):
        tk.Text.__init__(self, parent.get_root())
        self.parent = parent
        self.dirty = False
        
        frame = ttk.Frame(self.parent.get_root()) #, bd=2, relief=tk.SUNKEN)
        # To make the element at 0,0 grows with the window
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        yscrollbar = ttk.Scrollbar(frame)
        yscrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)
        self.text = tk.Text(frame, wrap=tk.NONE, bd=0,
                            yscrollcommand=yscrollbar.set)
        self.text.config(font=('consolas', 12), undo=True, wrap='word')
        self.text.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.text.bind('<<Paste>>', self.paste)
        self.text.bind('<<Cut>>', self.cut)
        self.text.bind('<<Copy>>', self.copy)
        self.text.bind('<KeyPress>', self.update_text_before)
        self.text.bind('<KeyRelease>', self.update_text_after)

        self.text.tag_config("a", foreground="blue", underline=1)

        self.start = None
        
        frame.pack(fill=tk.BOTH, expand=tk.YES)
        self.text.focus_force()

    #
    # Handling of state
    #
    def write(self, content, at=tk.INSERT):
        self.text.insert(at, content)
        self.dirty = True
        self.parent.update_title()

    def delete(self, first, last=None):
        self.text.delete(first, last)
        self.dirty = True
        self.parent.update_title()

    #
    # Handling of selection: deleting, getting, selecting and unselecting
    #
    def selection_delete(self):
        self.delete(tk.SEL_FIRST, tk.SEL_LAST)
        self.selection_clear()

    def selection_get(self):
        return self.text.get(tk.SEL_FIRST, tk.SEL_LAST)

    def selection_set(self, index1, index2):
        if self.text.compare(index1, '<', index2):
            self.text.tag_add('sel', f'{index1}', f'{index2}')
        else:
            self.text.tag_add('sel', f'{index2}', f'{index1}')

    def selection_clear(self):
        self.text.tag_remove('sel', '1.0', tk.END)

    #
    # Basic functions
    #
    def paste(self, event):
        content =  self.root.clipboard_get()
        event.widget.insert(tk.INSERT, content)
        return 'break'

    def cut(self, event):
        self.copy(event)
        self.selection_delete()
        return 'break'

    def copy(self, event):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.selection_get())
        return 'break'

    def update_text_before(self, event):
        text = event.widget
        Shift = 0x0001
        if event.keysym in ['Left', 'Right', 'Up', 'Down', 'End', 'Home']: # 37, 39
            codes = {
                'Left': 'insert-1c',
                'Right': 'insert+1c',
                'Up': 'insert-1l',
                'Down': 'insert+1l',
                'End': 'insert lineend',
                'Home': 'insert linestart'
            }
            nex = codes[event.keysym]
            if len(text.tag_ranges('sel')) == 0:
                self.start = text.index(tk.INSERT)
            else:
                self.selection_clear()
            if Shift & event.state:
                self.selection_set(nex, self.start)
            text.mark_set(tk.INSERT, f'{nex}')
            return 'break'
        elif event.keysym == 'BackSpace':
            if len(text.tag_ranges('sel')) > 0:
                self.selection_delete()
            else:
                text.mark_set(tk.INSERT, 'insert-1c')
                self.delete(tk.INSERT)
            return 'break'
        elif event.keysym == 'Delete':
            if len(text.tag_ranges('sel')) > 0:
                self.selection_delete()
            return 'break'
        elif event.keysym == 'Escape':
            self.selection_clear()
            return 'break'
        elif event.char == '\r':
            content = '\n'
        elif event.char == '\t':
            content = '    '
        elif event.keysym == 'space':
            content = ' '
        elif event.char.isprintable(): #isalnum()
            print(event)
            content = event.char
        else:
            print('Unknown:', event)
            return 'break'
        if len(text.tag_ranges('sel')) > 0:
            self.selection_delete()
        self.write(content)
        c = event.widget.get("insert linestart", "insert lineend")
        print(c)
        if c.startswith('http://'):
            text.tag_add('a', 'insert linestart', tk.INSERT)
        else:
            text.tag_remove('a', 'insert linestart', tk.INSERT)
        text.see(tk.INSERT)
        return 'break'

    def update_text_after(self, event):
        #print('h', event)
        res = event.widget.search('--> ', "insert linestart", "insert lineend")
        while res != '':
            print(res)
            self.delete(res, res + '+4c')
            self.write(res, '→ ')
            res = event.widget.search('--> ', res, "insert lineend")
        return 'break'


if __name__ == '__main__':
    Jyx()

