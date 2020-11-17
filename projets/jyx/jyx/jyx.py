from tkinter import font

from enum import Enum
from typing import Dict

# Getting now


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

class Fonts:
    COURRIER_NEW_10_BOLD = None
    COURRIER_NEW_10 = None

class KeyConstants:

    MASK_CONTROL = 0x0004

    KEY_A = 65
    KEY_B = 66
    KEY_C = 67
    KEY_D = 68
    KEY_E = 69
    KEY_F = 70
    KEY_G = 71
    KEY_H = 72
    KEY_I = 73
    KEY_J = 74
    KEY_K = 75
    KEY_L = 76
    KEY_M = 77
    KEY_N = 78
    KEY_O = 79
    KEY_P = 80
    KEY_Q = 81
    KEY_R = 82
    KEY_S = 83
    KEY_T = 84
    KEY_U = 85
    KEY_V = 86
    KEY_W = 87
    KEY_X = 88
    KEY_Y = 89
    KEY_Z = 90

    KEY_TAB = 9
    KEY_SHIFT = 16
    KEY_CONTROL = 17
    KEY_ALT = 18
    KEY_VERR_MAJ = 20

    CONTROL_KEYS = [KEY_SHIFT, KEY_CONTROL, KEY_ALT, KEY_VERR_MAJ]

class Level(Enum):
    INFO = 0
    WARNING = 1
    ERROR = 2

class Output(Enum):
    SILENT = 0
    CONSOLE = 1
    POPUP = 2

class Logger:

    def __init__(self, exit_on_error: bool = True):
        self.exit_on_error = exit_on_error
        self.flux = {
            Level.INFO : Output.CONSOLE,
            Level.WARNING : Output.CONSOLE,
            Level.ERROR : Output.CONSOLE,
        }

    def set_warn(self, val: Output) -> None:
        self.flux[Level.WARNING] = val

    def set_info(self, val: Output) -> None:
        self.flux[Level.INFO] = val

    def set_error(self, val: Output) -> None:
        self.flux[Level.ERROR] = val

    def warn(self, msg: str) -> None:
        if self.flux[Level.WARNING] == Output.CONSOLE:
            print('[WARNING] ' + str(msg))
        elif self.flux[Level.WARNING] == Output.POPUP:
            messagebox.showwarning("Warning", str(msg))

    def info(self, msg: str) -> None:
        if self.flux[Level.INFO] == Output.CONSOLE:
            print('[INFO] ' + str(msg))
        elif self.flux[Level.INFO] == Output.POPUP:
            messagebox.showinfo("Information", str(msg))

    def error(self, msg: str) -> None:
        if self.flux[Level.ERROR] == Output.CONSOLE:
            print('[ERROR] ' + str(msg))
        elif self.flux[Level.ERROR] == Output.POPUP:
            messagebox.showerror("Error", str(msg))
        if self.exit_on_error:
            exit()


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
        self.log = Logger(False)
        self.rc = RessourceManager(self.log)
        #self.rc.from_file(r'icons\iconyellowcube16x19_F5i_icon.ico')
        self.rc.from_file(os.path.join(".", "icons", "polar-star.png"))
        self.title = 'Jyx'
        # base options
        self.options['display_tree'] = True
        # create default option file
        else:
            self.write_options()
        self.start()

    def write_options(self):
        config = configparser.ConfigParser()
        config['MAIN'] = {
            'display_tree' : str(self.options['display_tree']),
            'confirm_exit' : str(self.options['confirm_exit']),
        }
        with open(Application.CONFIG_FILE_NAME, 'w') as configfile:
            config.write(configfile)

    def update(self):
        self.after_id = self.root.after(1000, self.update)

    def update_status_bar(self, event):
        s = self.frame.get_current_text().index(tkinter.INSERT)
        self.status_bar.config(text=s)

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

        self.root.bind('<Control-n>', self.menu_new)
        self.root.bind('<Control-t>', self.menu_new_tab)
        self.root.bind('<Control-o>', self.menu_open)
        self.root.bind('<Control-s>', self.menu_save)
        self.root.bind('<Control-q>', self.menu_exit)
        self.root.bind('<Control-a>', self.menu_select_all)
        self.root.bind('<Control-z>', self.menu_undo)
        self.root.bind('<Control-y>', self.menu_redo)
        self.root.bind('<F5>', self.menu_exec)

    def start(self):
        # Fonts
        Fonts.COURRIER_NEW_10 = font.Font(family='Courier New', size=10)
        Fonts.COURRIER_NEW_10_BOLD = font.Font(family='Courier New', size=10, weight='bold')
        # Ressources
        if self.rc.found("polar-star"):
            #self.root.iconbitmap("@...")
            self.root.iconphoto(True, self.rc.get_as_image('polar-star'))
        self.root.minsize(width=800, height=600)
        #root.title("Jyx")
        #root.geometry("600x400")
        self.frame = MyFrame(self)
        for t in self.frame.text:
            t.bind('<Control-v>', self.state_change) #self.menu_paste)
        self.make_menu()
        self.make_status_bar()
        self.set_title()
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

    def run(self):
        self.frame.mainloop()

    #-------------------------------------------------------
    # Menu functions
    #-------------------------------------------------------

    def menu_new_tab(self, event=None):
        self.new_tab()

    def menu_save(self, event=None):
        options = {}
        #options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('lua files', '.lua'), ('python files', '.py'), ('text files', '.txt')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'myfile.' + self.options['lang']
        options['parent'] = self.root
        options['title'] = 'Save file...'
        filename = filedialog.asksaveasfilename(**options) # mode='w',
        if filename:
            self.save(filename)

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

    def menu_cut(self, event=None):
        self.frame.get_current_text().event_generate("<<Cut>>")
        self.state_change()

    def menu_copy(self, event=None):
        self.frame.get_current_text().event_generate("<<Copy>>")

    def menu_paste(self, event=None):
        self.frame.paste(event)
        self.state_change()

    def menu_select_all(self, event=None):
        tab = self.frame.get_current_text()
        tab.tag_add(tkinter.SEL, "1.0", tkinter.END) # Select
        tab.mark_set(tkinter.INSERT, "1.0") # Mark
        tab.see(tkinter.INSERT) # Scroll to insert mark
        #print(tab.count("sel.first", "sel.last"))
        return 'break'

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
    
    #-------------------------------------------------------
    # Text functions
    #-------------------------------------------------------

    def new_tab(self):
        self.frame.make_text()
        self.set_title()
        # Select last tab
        self.frame.notebook.select(self.frame.notebook.index('end')-1)

    def load(self, filename : str):


    def save(self, filename: str, raw: bool=False):
        f = open(filename, mode='w', encoding='utf8')
        content = self.frame.get_current_text().get(1.0, tkinter.END)
        f.write(content)
        f.close()
        if not raw:
            self.state_restart(filename)

    #-------------------------------------------------------
    # State functions
    #-------------------------------------------------------

    def state_restart(self, filename):
        self.log.info("State restared")
        self.frame.set_current_dirty(False)
        self.frame.set_current_path(filename)
        self.set_title()

    def state_change(self, event=None): # in order to bind it to Control-v we need a free parameter event
        if not self.frame.get_current_dirty():
            self.log.info("State changed to dirty")
            self.frame.set_current_dirty(True)
            self.set_title()


class MyFrame(tkinter.Frame):
    """ Extend a Frame, a global container"""

    def __init__(self, app):
        tkinter.Frame.__init__(self, app.root)
        app.root.bind_class("Text", "<<Paste>>", self.paste)
        self.pack(fill=tkinter.BOTH, expand=tkinter.YES) # make it visible
        self.app = app
        self.build()

    def paste(self, event):
        if event is None:
            widget = self.get_current_text()
        else:
            widget = event.widget
        # Delete selection if existing
        try:
            widget.delete("sel.first", "sel.last")
        except:
            pass
        # Insert new text
        widget.insert(tkinter.INSERT, widget.clipboard_get())
        # Don't execute any more binding
        return "break"

    def get_current_text(self):
        return self.text[self.notebook.index("current")]

    def get_text(self, i):
        return self.text[i]

    def get_content(self, i):
        return self.text[i].get(1.0, tkinter.END)

    # no clean...
    def set_content(self, i, content):
        self.text[i].insert("1.0", content)

    def get_current_dirty(self):
        return self.dirty[self.notebook.index("current")]

    def set_current_dirty(self, value):
        self.dirty[self.notebook.index("current")] = value

    def get_dirty(self, i):
        return self.dirty[i]

    def set_dirty(self, i, value):
        self.dirty[i] = value

    def is_dirty(self):
        for i in self.dirty:
            if i:
                return True
        return False

    def get_current_path(self):
        return self.filepaths[self.notebook.index("current")]

    def set_current_path(self, value):
        self.filepaths[self.notebook.index("current")] = value

    def get_path(self, i):
        return self.filepaths[i]

    def set_path(self, i, path):
        self.filepaths[i] = path

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

    def update_text(self, event):
        self.key(event)
        self.app.update_status_bar(event)

    def make_notebook(self: tkinter.Frame):
        self.notebook = ttk.Notebook(self)
        self.text_frames = []
        self.text_scrollbars = []
        self.text = []
        self.filepaths = []
        self.dirty = []
        self.make_text()

    def make_text(self: tkinter.Frame): # with grid: ok :-)
        frame = tkinter.Frame(self.notebook, bd=2, relief=tkinter.SUNKEN)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        #self.xscrollbar = tkinter.Scrollbar(self.text_frame, orient=tkinter.HORIZONTAL)
        #self.xscrollbar.grid(row=1, column=0, sticky=tkinter.E+tkinter.W)

        yscrollbar = tkinter.Scrollbar(frame)
        yscrollbar.grid(row=0, column=1, sticky=tkinter.N+tkinter.S)

        text = tkinter.Text(frame, wrap=tkinter.NONE, bd=0,
                    #xscrollcommand=self.xscrollbar.set,
                    yscrollcommand=yscrollbar.set)
        text.config(font=("consolas", 12), undo=True, wrap='word')

        text.grid(row=0, column=0, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)

        #self.xscrollbar.config(command=self.text.xview)
        yscrollbar.config(command=text.yview)

        self.text_frames.append(frame)
        self.text_scrollbars.append(yscrollbar)
        self.text.append(text)
        self.filepaths.append(None)
        self.dirty.append(False)

        # Notebook parent
        self.notebook.add(frame)

        # Tags
        tag_keyword = text.tag_config("keyword", foreground="blue", font=Fonts.COURRIER_NEW_10_BOLD)
        tag_comment = text.tag_config("comment", foreground="grey", font=Fonts.COURRIER_NEW_10)

        # Tabs
        def tab(event):
            if event.state & KeyConstants.MASK_CONTROL:
                return
            self.get_current_text().insert(tkinter.INSERT, " " * 4)
            return 'break' # Prevent normal behavior

        # Key bindings
        text.bind("<Tab>", tab)
        text.bind("<KeyRelease>", self.update_text)
        text.bind("<ButtonRelease-1>", self.app.update_status_bar)

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

