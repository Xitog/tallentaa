from typing import Dict

import subprocess
import stat

# Tokenize from rey
import sys
try:
    sys.path.append('../../projets/ash')
    from ashlang import Tokenizer, Token
except ModuleNotFoundError:
    ASH_TOKENIZER = False
else:
    ASH_TOKENIZER = True

class RessourceManager:

    def __init__(self, logger: Logger):
        self.ressources: Dict[str, str] = {}
        self.log: Logger = logger

    def from_file(self, filepath: str) -> None:
        key = os.path.splitext(os.path.basename(filepath))[0] # suppress .extension
        if os.path.isfile(filepath):
            self.ressources[key] = filepath
            self.log.info('Ressource registered from file: ' + filepath)
        else:
            self.ressources[key] = None
            self.log.error('Ressource could not be found: ' + filepath)

    def get(self, key: str) -> str:
        return self.ressources[key]

    def get_as_image(self, key: str) -> tkinter.PhotoImage:
        if self.found(key):
            return tkinter.PhotoImage(file=self.ressources[key])
        raise Exception("Ressource could not be found")

    def found(self, key: str) -> bool:
        return key in self.ressources and self.ressources[key] is not None

class Application:

    def __init__(self):
        self.rc = RessourceManager(self.log)
        self.rc.from_file(os.path.join(".", "icons", "polar-star.png"))
        self.options['display_tree'] = True

    def update(self):
        self.after_id = self.root.after(1000, self.update)

    def set_title(self):
        current = self.frame.notebook.index("current")
        for i in range(0, self.frame.notebook.index('end')):
            file = self.frame.get_path(i)
            if file is None:
                file = "New"
            dirty = ""
            if self.frame.get_dirty(i):
                dirty = " *"
            if i == current:
                self.root.wm_title(self.title + " " + Application.VERSION + " - " + file + dirty)
            self.frame.notebook.tab(i, text=os.path.basename(file) + dirty)

    def make_menu(self):
        "Build the menu"
        self.display_tree = tkinter.BooleanVar()
        self.display_tree.set(self.options['display_tree'])

        self.options_menu = tkinter.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Options", menu=self.options_menu)
        self.options_menu.add_checkbutton(label="Display Tree", onvalue=True, offvalue=False, variable=self.display_tree, command=self.restart)

    def start(self):
        # Ressources
        if self.rc.found("polar-star"):
            #self.root.iconbitmap("@...")
            self.root.iconphoto(True, self.rc.get_as_image('polar-star'))
        self.root.minsize(width=800, height=600)
        #root.title("Jyx")
        #root.geometry("600x400")
        self.update()

    def save_opt(self):
        self.options['confirm_exit'] = self.confirm_exit.get()
        self.write_options()

    def restart(self):
        # Save
        f = self.frame
        contents = []
        paths = []
        dirtyness = []
        nb = f.notebook.index('end')
        current = f.notebook.index("current")
        for i in range(0, nb):
            contents.append(f.get_content(i))
            paths.append(f.get_path(i))
            dirtyness.append(f.get_dirty(i))
        del f
        self.options['display_tree'] = self.display_tree.get()
        self.options['confirm_exit'] = self.confirm_exit.get()
        self.root.after_cancel(self.after_id)
        self.menu_exit()
        self.write_options()
        self.start()
        f = self.frame # new value!
        for i in range(0, nb):
            if i > 0:
                self.new_tab()
            f.set_content(i, contents[i])
            f.set_path(i, paths[i])
            f.set_dirty(i, dirtyness[i])
        self.set_title()
        self.frame.notebook.select(current)

    def menu_undo(self, event=None):
        try:
            self.frame.get_current_text().edit_undo()
            self.state_change()
        except tkinter.TclError:
            self.log.warn("Nothing to undo")

    def menu_redo(self, event=None):
        try:
            self.frame.get_current_text().edit_redo()
            self.state_change()
        except tkinter.TclError:
            self.log.warn("Nothing to redo")

    def menu_exec(self, event=None):
        if not lang_has(self.options['lang'], 'execute'):
            return
        filepath = self.frame.get_current_path()
        if filepath is None:
            filepath = os.path.join(os.getcwd(), 'temp.' + self.options['lang'])
            self.save(filepath, raw=True) # will not set any filepath nor dirty state (still dirty)
        self.log.info('Executing: ' + filepath)
        if hasattr(os, 'startfile'): # Windows only
            #os.startfile(filepath)
            subp = 'python'
        else:
            #os.system(filepath)
            subp = 'python3'
            os.chmod(filepath, stat.S_IXUSR | stat.S_IWUSR | stat.S_IRUSR)
        cmd = subprocess.run([subp, filepath], capture_output=True)
        stdout = cmd.stdout.decode() # from bytes to str
        print(stdout)

    def make_tree(self: tkinter.Frame):
        # Loading icons
        self.app.rc.from_file("icons/Crystal_Clear_device_blockdevice16.png")
        self.app.rc.from_file("icons/IconBlueCube16x19.png")
        self.app.rc.from_file("icons/IconYellowCube16x19.png")
        self.app.rc.from_file("icons/IconMagentaCube16x19.png")
        # Creating tree
        # borderwidth seems not to work on windows
        #ttk.Style().configure(  '.', # every class of object
        #    relief = 'flat',  # flat ridge for separator
        #    borderwidth = 0,  # zero width for the border
        #)
        self.treeview = ttk.Treeview(self)
        #self.treeview["columns"] = ("text",)
        self.treeview.column("#0", width=120)
        self.treeview.heading("#0", text="Nodes")
        #self.treeview.column("text", width=80)
        #self.treeview.heading("text", text="Tag")
        self.treeview.insert("", 0, text="First entry")
        if self.app.rc.found('Crystal_Clear_device_blockdevice16'):
            self.treeview.insert("", 1, text=" Second entry", image=self.app.rc.get_as_image('Crystal_Clear_device_blockdevice16'))
        else:
            self.treeview.insert("", 1, text=" Second entry")
        if self.app.rc.found('IconYellowCube16x19'):
            sub1 = self.treeview.insert("", 2, text=" Third entry", image=self.app.rc.get_as_image('IconYellowCube16x19'))
        else:
            sub1 = self.treeview.insert("", 2, text=" Third entry")
        if self.app.rc.found('IconBlueCube16x19'):
            self.treeview.insert(sub1, 0, text=" 2-1 Entry", image=self.app.rc.get_as_image('IconBlueCube16x19'))
        else:
            self.treeview.insert(sub1, 0, text=" 2-1 Entry")
        if self.app.rc.found('IconMagentaCube16x19'):
            self.treeview.insert(sub1, 1, text=" 2-2 Entry", image=self.app.rc.get_as_image('IconMagentaCube16x19'))
        else:
            self.treeview.insert(sub1, 1, text=" 2-2 Entry")
        # or
        self.treeview.insert("", 3, "sub2", text="Fourth entry")
        if self.app.rc.found('IconYellowCube16x19'):
            self.treeview.insert("sub2", 0, text=" 3-1 Entry", image=self.app.rc.get_as_image('IconYellowCube16x19'))
        else:
            self.treeview.insert("sub2", 0, text=" 3-1 Entry")

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

    def tokenizer(self):
        lang = self.app.options['lang']
        if not lang_has(lang, 'tokenize'):
            return
        debug = True
        text = self.get_current_text()
        content = text.get(1.0, tkinter.END)
        tokens = Tokenizer(lang).tokenize(content, debug)
        # Clear all tags
        for tag in text.tag_names():
            text.tag_remove(tag, 1.0)
        # Put tags
        if debug:
            print('------------')
            print('Setting tags')
            print('------------')
        for t in tokens:
            deb = '1.0+%ic' % t.start
            end = '1.0+%ic' % (t.start + t.length)
            if debug:
                print(t)
                print(deb)
                print(end)
            if t.typ == Token.Keyword:
                print('TAGGING KWD')
                text.tag_add("keyword", deb, end)
            elif t.typ == Token.Comment:
                print('TAGGING CMT')
                text.tag_add("comment", deb, end) 

    def key(self, event):
        text = self.get_current_text()
        # no refresh on control keys
        if event.keycode in KeyConstants.CONTROL_KEYS:
            return
        #print("pressed", "char", repr(event.char), "keycode", event.keycode, "state", event.state, "type", event.type, "ctrl", event.state & KeyConstants.MASK_CONTROL)
        #print(dir(event))
        if event.state & KeyConstants.MASK_CONTROL and event.keycode not in [ KeyConstants.KEY_X, KeyConstants.KEY_V]:
            return
        self.app.state_change()
        self.tokenizer()
        s = text.get(1.0, tkinter.END)
        w = ''
        start = 0
        for i in range(0, len(s)):
            w += s[i]
            if w == 'lua ':
                print("youpi!")
                deb = '1.0+%d chars' % start
                print(deb)
                end = '1.0+%d chars' % i
                print(end)
                text.tag_add("keyword", deb, end)
                w = ''
                start = i
                print(w, len(w))

        #self.xscrollbar = tkinter.Scrollbar(self.text_frame, orient=tkinter.HORIZONTAL)
        #self.xscrollbar.grid(row=1, column=0, sticky=tkinter.E+tkinter.W)
        text.grid(row=0, column=0, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)
        
    def build(self):
        if self.app.options['display_tree']:
            self.make_tree()
            self.make_notebook()
            #self.treeview.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.YES)
            #self.notebook.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=tkinter.YES)
            self.treeview.place( relx = 0.0, rely = 0.0, relwidth = 0.2, relheight = 1.0 )
            self.notebook.place( relx = 0.2, rely = 0.0, relwidth = 0.8, relheight = 1.0 )
        else:
            self.make_notebook()
            #self.notebook.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=tkinter.YES)
            self.notebook.place( relx = 0.0, rely = 0.0, relwidth = 1.0, relheight = 1.0 )
