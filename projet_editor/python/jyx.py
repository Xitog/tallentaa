#!/usr/bin/env python3
# Created the ‎lundi ‎6 ‎juin ‎2016 (début des tests tkinter)

import configparser
import os.path

import tkinter
from tkinter import ttk # not found in 2.7.11 but found in 3.5.1 :-)
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font

from enum import Enum
from typing import Dict

# Tokenize from rey
import sys
sys.path.append('../../projets/ash')
from ashlang import Tokenizer, Token

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
        self.version = '0.0.1'
        # config
        self.options = {}
        # base options
        self.options['display_tree'] = True
        self.options['confirm_exit'] = True
        self.options['lang'] = 'txt'
        # try to load options
        if os.path.isfile(self.title + '.ini'):
            config = configparser.ConfigParser()
            config.read(self.title + '.ini')
            if 'MAIN' in config:
                if 'display_tree' in config['MAIN']:
                    self.options['display_tree'] = (config['MAIN']['display_tree'] == 'True')
                    self.log.info('Display tree is : ' + str(self.options['display_tree']))
                if 'confirm_exit' in config['MAIN']:
                    self.options['confirm_exit'] = (config['MAIN']['confirm_exit'] == 'True')
                    self.log.info('Confirm exit is : ' + str(self.options['confirm_exit']))
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
        with open(self.title + '.ini', 'w') as configfile:
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
                self.root.wm_title(self.title + " " + self.version + " - " + file + dirty)
            self.frame.notebook.tab(i, text=os.path.basename(file) + dirty)

    def make_menu(self):
        "Build the menu"
        self.menu = tkinter.Menu(self.root)
        self.root.config(menu=self.menu)
        self.filemenu = tkinter.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="New", command=self.menu_new, accelerator="Ctrl+N")
        self.filemenu.add_command(label="New Tab", command=self.menu_new_tab, accelerator="Ctrl+T")
        self.filemenu.add_command(label="Open...", command=self.menu_open, accelerator="Ctrl+O")
        self.filemenu.add_command(label="Save As...", command=self.menu_save, accelerator="Ctrl+S")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Run Script", command=self.menu_exec, accelerator="F5")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.menu_exit, accelerator="Ctrl+Q")

        self.editmenu = tkinter.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Edit", menu=self.editmenu)
        self.editmenu.add_command(label="Undo", command=self.menu_undo, accelerator="Ctrl+Z")
        self.editmenu.add_command(label="Redo", command=self.menu_redo, accelerator="Ctrl+Y")
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Cut", command=self.menu_cut, accelerator="Ctrl+X")
        self.editmenu.add_command(label="Copy", command=self.menu_copy, accelerator="Ctrl+C")
        self.editmenu.add_command(label="Paste", command=self.menu_paste) #, accelerator="Ctrl+V")
        self.editmenu.add_command(label="Select All", command=self.menu_select_all, accelerator="Ctrl+A")

        self.display_tree = tkinter.BooleanVar()
        self.display_tree.set(self.options['display_tree'])
        self.confirm_exit = tkinter.BooleanVar()
        self.confirm_exit.set(self.options['confirm_exit'])

        self.options_menu = tkinter.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Options", menu=self.options_menu)
        self.options_menu.add_checkbutton(label="Display Tree", onvalue=True, offvalue=False, variable=self.display_tree, command=self.restart)
        self.options_menu.add_checkbutton(label="Confirm Exit", onvalue=True, offvalue=False, variable=self.confirm_exit, command=self.restart)

        self.lang = tkinter.StringVar()
        self.lang.set(self.options['lang'])

        self.langmenu = tkinter.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Language", menu=self.langmenu)
        # Plain text
        self.langmenu.add_radiobutton(label="Plain text (.txt)", variable=self.lang, value="txt", command=self.update_lang)#, indicatoron=0
        self.langmenu.add_separator()
        # Lightweight markup language
        self.langmenu.add_radiobutton(label="DG Log (.dgl)", variable=self.lang, value="dgl", command=self.update_lang)
        self.langmenu.add_radiobutton(label="Textile (.txl)", variable=self.lang, value="txl", command=self.update_lang)
        self.langmenu.add_separator()
        # Script language
        self.langmenu.add_radiobutton(label="JavaScript (.js)", variable=self.lang, value="js", command=self.update_lang)
        self.langmenu.add_radiobutton(label="Lua (.lua)", variable=self.lang, value="lua", command=self.update_lang)
        self.langmenu.add_radiobutton(label="Python (.py)", variable=self.lang, value="py", command=self.update_lang)#, indicatoron=0
        self.langmenu.add_radiobutton(label="Rey (.rey)", variable=self.lang, value="rey", command=self.update_lang)
        self.langmenu.add_radiobutton(label="Ruby (.rb)", variable=self.lang, value="rb", command=self.update_lang)
        self.langmenu.add_separator()
        # Compiled language
        self.langmenu.add_radiobutton(label="C (.c, .h)", variable=self.lang, value="c", command=self.update_lang)
        self.langmenu.add_radiobutton(label="Java (.java)", variable=self.lang, value="java", command=self.update_lang)
        self.langmenu.add_separator()
        # Data format
        self.langmenu.add_radiobutton(label="INI (.ini)", variable=self.lang, value="ini", command=self.update_lang)
        self.langmenu.add_radiobutton(label="JSON (.json)", variable=self.lang, value="json", command=self.update_lang)#, indicatoron=0
        self.langmenu.add_radiobutton(label="XML (.xml, .xsd)", variable=self.lang, value="xml", command=self.update_lang)#, indicatoron=0

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

    def make_status_bar(self):
        self.status_bar = tkinter.Label(self.root, bd=1, relief=tkinter.SUNKEN)
        self.status_bar.config(text="Hello!", anchor=tkinter.E, padx=20)
        #status_bar.update_idletasks()
        self.status_bar.pack(side=tkinter.BOTTOM, fill=tkinter.X)

    def update_lang(self):
        #self.log.info("self.lang = " + self.lang.get())
        self.options['lang'] = self.lang.get()

    def start(self):
        # root widget, an ordinary window
        self.root = tkinter.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.menu_exit)
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
        # self.log.set_error(Logger.POPUP) # if we do that before initialize Tk, an empty window appear
        # self.log.set_warn(Logger.POPUP)

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

    def menu_about(self):
        messagebox.showinfo("About", self.title + " - " + self.version + "\nMade with ❤\nDamien Gouteux, 2017\n")

    def menu_exit(self, event=None):
        self.exit()

    def menu_new(self, event=None):
        self.new()

    def menu_new_tab(self, event=None):
        self.new_tab()

    def menu_open(self, event=None):
        """Returns an opened file in read mode."""
        options = {}
        #options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('lua files', '.lua'), ('python files', '.py'), ('text files', '.txt')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'myfile.' + self.options['lang']
        options['parent'] = self.root
        options['title'] = 'Open file...'
        self.load(filedialog.askopenfilename(**options)) # mode='r',

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
        self.frame.get_current_text().event_generate("<<Paste>>")
        self.state_change()

    def menu_select_all(self, event=None):
        self.frame.escape_refresh(2)
        self.frame.get_current_text().tag_add(tkinter.SEL, "1.0", tkinter.END)

    def menu_exec(self, event=None):
        filepath = self.filepath
        if filepath is None:
            filepath = os.path.join(os.getcwd(), 'temp.' + self.options['lang'])
            self.save(filepath)
        self.log.info('Executing: ' + filepath)
        os.startfile(filepath)

    #-------------------------------------------------------
    # Text functions
    #-------------------------------------------------------

    def new(self):
        self.clear()
        self.state_restart(None)

    def new_tab(self):
        self.frame.make_text()
        self.set_title()
        # Select last tab
        self.frame.notebook.select(self.frame.notebook.index('end')-1)

    def clear(self):
        self.frame.get_current_text().delete("1.0", tkinter.END)

    def load(self, filename : str):
        f = open(filename, mode='r', encoding='utf8')
        try:
            content = f.read()
        except UnicodeDecodeError as ude:
            self.log.error("Encoding error: unable to open file: " + filename)
            print(ude)
            return
        f.close()
        self.clear()
        self.frame.get_current_text().insert("1.0", content) # or END
        self.state_restart(filename)

    def save(self, filename : str):
        f = open(filename, mode='w', encoding='utf8')
        content = self.frame.get_current_text().get(1.0, tkinter.END)
        f.write(content)
        f.close()
        self.state_restart(filename)

    def exit(self):
        if self.frame.is_dirty() and self.options['confirm_exit']:
            if messagebox.askyesno("Unsaved changes", "There are unsaved changes. Do you really want to quit " + self.title + "?", default=messagebox.NO):
                self.root.destroy()
        else:
            self.root.destroy()
        #root.quit()
        #exit(0)

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
        self.pack(fill=tkinter.BOTH, expand=tkinter.YES) # make it visible
        self.app = app
        self.build()
        self._escape_refresh = 0

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
        debug = True
        text = self.get_current_text()
        content = text.get(1.0, tkinter.END)
        #print('||',content,'||', sep='')
        if self.app.options['lang'] == 'txt':
            return
        else:
            print(self.app.options['lang'])
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

    # There is a bug when doing Ctrl+A : the refresh (call to key function) "let" the first character outside the selected area!
    # To prevent this, we do this
    def escape_refresh(self, nb):
        self._escape_refresh = nb

    def key(self, event):
        text = self.get_current_text()
        # no refresh on control keys
        if event.keycode in KeyConstants.CONTROL_KEYS:
            return
        #print("pressed", "char", repr(event.char), "keycode", event.keycode, "state", event.state, "type", event.type, "ctrl", event.state & KeyConstants.MASK_CONTROL)
        #print(dir(event))
        #print('>>>', self._escape_refresh)
        # and event.type == tkinter.EventType.KeyRelease:
        if event.state & KeyConstants.MASK_CONTROL and event.keycode not in [ KeyConstants.KEY_X, KeyConstants.KEY_V]:
            return
        if self._escape_refresh > 0:
            self._escape_refresh -= 1
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


if __name__ == "__main__":
    Application().run()
