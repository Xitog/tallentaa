#!/usr/bin/env python3

#
# Imports
#

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font

import json # for loading/saving options
from datetime import datetime # for now()
import os # for getcwd()
import os.path # for basename()
from enum import Enum

#
# Globals and constants
#

DEFAULT_CONFIG = """{
    "options": {
        "tongue": {
            "value": "fr",
            "msg": "tongue"
        },
        "confirm": {
            "value": false,
            "msg":"confirm"
        },
        "basename": {
            "value": false,
            "msg": "basename"
        },
        "treeview": {
            "value": true,
            "msg": "treeview"
        }
    },
    "messages": {
        "en" : {
            "started"    : "Started",
            "about_msg"  : "Made with ❤",
            "unsaved"    : "Unsaved changes",
            "unsaved_msg": "There are unsaved changes.\\nDo you really want to quit Jyx?",
            "open file"  : "Open file...",
            "save file"  : "Save file...",
            "filter all" : "all files",
            "file name"  : "myfile"
        }
    },
    "menu": {
        "en": {
            "tongue"     : "English",
            "file"       : "File",
            "new"        : "New",
            "open"       : "Open...",
            "save"       : "Save",
            "save as"    : "Save As...",
            "save all"   : "Save All",
            "run"        : "Run Script",
            "exit"       : "Exit",
            "edit"       : "Edit",
            "undo"       : "Undo",
            "redo"       : "Redo",
            "cut"        : "Cut",
            "copy"       : "Copy",
            "paste"      : "Paste",
            "select all" : "Select all",
            "clear"      : "Clear",
            "options"    : "Options",
            "tongues"    : "Tongues",
            "confirm"    : "Confirm before exit",
            "basename"   : "Display only the name",
            "languages"  : "Languages",
            "help"       : "Help",
            "about"      : "About..."
        }
    },
    "languages" : {
        "text" : {
            "label": "Plain text",
            "extension": [".txt"],
            "family": "",
            "support": ""
        }
    }
}
"""

#
# Classes
#

class Level(Enum):
    INFO = 0
    WARNING = 1
    ERROR = 2

class Output(Enum):
    SILENT = 0
    CONSOLE = 1
    POPUP = 2

class Logger:

    def __init__(self, exit_on_error: bool = True,
                 info=Output.CONSOLE,
                 warn=Output.CONSOLE,
                 error=Output.CONSOLE):
        self.exit_on_error = exit_on_error
        self.flux = {
            Level.INFO : info,
            Level.WARNING : warn,
            Level.ERROR : error,
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


#-------------------------------------------------------------------------------

class Jyx:

    TITLE = 'Jyx'
    RUN_COMMAND = 6
    CONFIG_FILE_NAME = 'jyx.json'
    VERSION = '0.0.1'
    
    def __init__(self):
        self.log = Logger(exit_on_error=False, info=Output.CONSOLE, warn=Output.POPUP, error=Output.POPUP)
        # Load data
        try:
            f = open(Jyx.CONFIG_FILE_NAME, 'r', encoding='utf8')
        except FileNotFoundError:
            f = open(Jyx.CONFIG_FILE_NAME, 'w', encoding='utf8')
            f.write(DEFAULT_CONFIG)
            f.close()
            f = open(Jyx.CONFIG_FILE_NAME, 'r', encoding='utf8')
        self.data = json.load(f)
        f.close()
        # Init
        self.root = tk.Tk()
        self.root.protocol('WM_DELETE_WINDOW', self.exit)
        self.root.minsize(width=800, height=600)
        icon = self.load_icon('polar-star.png')
        if icon is not None:
            self.root.iconphoto(True, icon)
        # Fonts
        self.fonts = {}
        self.fonts['COURRIER_NEW_10'] = font.Font(family='Courier New', size=10)
        self.fonts['COURRIER_NEW_10_BOLD'] = font.Font(family='Courier New', size=10, weight='bold')
        # Options
        self.options = {}
        for opt, info in self.data['options'].items():
            self.options[opt] = JyxOption.load(opt, info)
        self.langage = tk.StringVar()
        self.langage.set(self.data['default_language'])
        # UI components
        self.notebook = JyxNotebook(self)
        self.treeview = JyxTree(self)
        # Prend tout Y (relheight = 1.0), se positionne à 0.2 pour le notebook
        self.treeview.place(relx=0.0, rely =0.0, relwidth =0.2, relheight =1.0)
        self.notebook.place(relx=0.2, rely =0.0, relwidth =0.8, relheight =1.0)
        self.menu = JyxMenu(self)
        self.root.config(menu=self.menu)
        # Updall vars, cannot be called until the menu is completed
        self.update_all_options() 
        self.update_title()
        # Tags
        #self.tags = {}
        #self.tags['keyword'] = self.notebook.get_text().tag_config("keyword", foreground="blue", font=self.fonts['COURRIER_NEW_10_BOLD'])
        #self.tags['comment'] = self.notebook.get_text().tag_config("comment", foreground="grey", font=self.fonts['COURRIER_NEW_10'])
        #self.tags['test'] = self.notebook.note.get_text().tag_config("a", foreground="blue", underline=1)
        # Starting
        self.auto_update()
        self.root.mainloop()

    def load_icon(self, name: str) -> tk.PhotoImage:
        res = None
        try:
            res = tk.PhotoImage(file=os.path.join('icons', name))
        except:
            self.log.info(f'Resource {name} could not be found')
        return res

    def get_root(self):
        return self.root

    def auto_update(self):
        self.after_id = self.root.after(5000, self.auto_update)
        #self.root.bell()
        print('hello')

    def update_langage(self):
        print('update langage')

    def update_title(self):
        dirty = ' *' if self.notebook.is_dirty() else ''
        tongue = self.options['tongue'].get()
        if self.notebook.get_filepath() is None:
            file = self.data['menu'][tongue]['new']              
        elif self.options['basename'].get():
            file = os.path.basename(self.notebook.get_filepath())
        else:
            file = self.notebook.get_filepath()
        i = self.notebook.current_index() + 1
        nb = len(self.notebook)
        self.root.wm_title(f"{Jyx.TITLE} {Jyx.VERSION} - {i}/{nb} {file}{dirty}")

    def update_status(self, event=None):
        self.menu.status_bar.configure(text=self.notebook.get_position())

    def update_all_options(self):
        for key in self.options:
            self.update(key, True)

    def update(self, varname, init=False):
        if varname not in self.options:
            raise Exception(f'Variable unknown: {varname}')
        opt = self.options[varname]
        val = opt.get()
        print(f"option {opt.name} = {val}")
        if varname == 'language':
            if not self.has(f"languages.{val}.support", "execute"):
                self.menu.file_menu.entryconfig(Jyx.RUN_COMMAND, state=tk.DISABLED)
            else:
                self.menu.file_menu.entryconfig(Jyx.RUN_COMMAND, state=tk.ACTIVE)
        elif varname == 'tongue' and not init:
            self.menu.relabel(old=opt.prev, new=val)
            self.notebook.relabel(val)
        elif varname == 'basename' and not init:
            self.update_title()
        elif varname == 'treeview':
            if val and not init:
                self.treeview.place(relx=0.0, rely =0.0, relwidth =0.2, relheight =1.0)
                self.notebook.place(relx=0.2, rely =0.0, relwidth =0.8, relheight =1.0)
            elif not val:
                self.treeview.place_forget()
                self.notebook.place(relx=0.0, rely =0.0, relwidth =1.0, relheight =1.0)
        opt.prev = val

    def has(self, prop, value, content=None):
        #print('has', prop, value) #, content)
        if content is None:
            content = self.data
        exploded = prop.split('.')
        if exploded[0] not in content:
            return False
        elif len(exploded) == 1:
            if type(content[exploded[0]]) in [str, int]:
                return content[exploded[0]] == value
            elif type(content[exploded[0]]) == list:
                return value in content[exploded[0]]
            else:
                raise Exception('Type not handled')
        else:
            return self.has('.'.join(exploded[1:]), value, content[exploded[0]])

    def exit(self, event=None):
        tongue = self.options['tongue'].get()
        if self.notebook.is_anyone_dirty() and self.options['confirm'].get():
            title = self.data['messages'][tongue]['unsaved']
            msg = self.data['messages'][tongue]['unsaved_msg']
            if messagebox.askyesno("Unsaved changes", msg, default=messagebox.NO):
                self.root.destroy()
        else:
            self.root.destroy()

    def new(self, event=None):
        self.notebook.new_tab()
        self.update_title()
        self.update_status()

    def save(self, event=None):
        if self.notebook.get_filepath() is None:
            self.save_as(event)
        else:
            self.note.save()

    def save_as(self, event=None):
        tongue = self.options['tongue'].get()
        lang = self.notebook.current().lang
        options = {}
        #options['defaultextension'] = '.txt'
        options['filetypes'] = [
            (self.data['messages'][tongue]['filter all'], '.*'),
            ('lua files', '.lua'),
            ('python files', '.py'),
            ('text files', '.txt')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = self.data['messages'][tongue]['file name'] + self.data['languages'][lang]['extension'][0]
        options['parent'] = self.root
        options['title'] = self.data['messages'][tongue]['save file']
        filename = filedialog.asksaveasfilename(**options) # mode='w',
        if type(filename) == str and len(filename) > 0:
            self.notebook.save(filename)

    def open(self, event=None):
        tongue = self.options['tongue'].get()
        lang = self.notebook.current().lang
        options = {}
        #options['defaultextension'] = '.txt'
        options['filetypes'] = [(self.data['messages'][tongue]['filter all'], '.*')]
        options['initialdir'] = os.getcwd()
        options['initialfile'] = self.data['messages'][tongue]['file name'] + self.data['languages'][lang]['extension'][0]
        options['parent'] = self.root
        options['title'] = self.data['messages'][tongue]['open file']
        filename = filedialog.askopenfilename(**options)
        if type(filename) == str and len(filename) > 0:
            print(filename)
            f = open(filename, mode='r', encoding='utf8')
            content = None
            try:
                content = f.read()
            except UnicodeDecodeError as ude:
                log.error("[ERROR] Encoding error: unable to open file: " + filename)
                print(ude)
            finally:
                f.close()
            if content is not None:
                self.notebook.open(filename, content)

    def run(self, event=None):
        pass

    def about(self, event=None):
        tongue = self.options['tongue'].get()
        title = self.data['menu'][tongue]['about']
        msg = self.data['messages'][tongue]['about_msg']
        messagebox.showinfo(title, f"{Jyx.TITLE} - {Jyx.VERSION}\n{msg}\nDamien Gouteux\n2017 - {datetime.now().year}\n")


class JyxOption:

    def __init__(self, name, val, msg):
        self.name = name
        self.val = val
        self.typ = type(val)
        self.msg = msg
        if self.typ == str:
            self.var = tk.StringVar()
        elif self.typ == bool:
            self.var = tk.BooleanVar()
        else:
            raise Exception(f"Option type not handled for {self.name} of type {self.typ}")
        self.var.set(self.val)
        self.prev = self.val

    @staticmethod
    def load(key, dic):
        return JyxOption(key, dic['value'], dic['msg'])

    def get(self):
        return self.var.get()


class JyxMenu(tk.Menu):

    def __init__(self, jyx):
        tk.Menu.__init__(self, jyx.get_root())
        self.jyx = jyx
        self.build()

    def relabel(self, old, new):
        #last = self.index(tk.END)
        #for item in range(last + 1)
        data = self.jyx.data

        self.entryconfig(data['menu'][old]['file'], label=data['menu'][new]['file'])
        self.entryconfig(data['menu'][old]['edit'], label=data['menu'][new]['edit'])
        self.entryconfig(data['menu'][old]['options'], label=data['menu'][new]['options'])
        self.entryconfig(data['menu'][old]['languages'], label=data['menu'][new]['languages'])
        self.entryconfig(data['menu'][old]['help'], label=data['menu'][new]['help'])
        
        self.file_menu.entryconfig(data['menu'][old]['new'], label=data['menu'][new]['new'])
        self.file_menu.entryconfig(data['menu'][old]['open'], label=data['menu'][new]['open'])
        self.file_menu.entryconfig(data['menu'][old]['save'], label=data['menu'][new]['save'])
        self.file_menu.entryconfig(data['menu'][old]['save as'], label=data['menu'][new]['save as'])
        self.file_menu.entryconfig(data['menu'][old]['save all'], label=data['menu'][new]['save all'])
        self.file_menu.entryconfig(data['menu'][old]['run'], label=data['menu'][new]['run'])
        self.file_menu.entryconfig(data['menu'][old]['exit'], label=data['menu'][new]['exit'])

        self.edit_menu.entryconfig(data['menu'][old]['undo'], label=data['menu'][new]['undo'])
        self.edit_menu.entryconfig(data['menu'][old]['redo'], label=data['menu'][new]['redo'])
        self.edit_menu.entryconfig(data['menu'][old]['cut'], label=data['menu'][new]['cut'])
        self.edit_menu.entryconfig(data['menu'][old]['copy'], label=data['menu'][new]['copy'])
        self.edit_menu.entryconfig(data['menu'][old]['paste'], label=data['menu'][new]['paste'])
        self.edit_menu.entryconfig(data['menu'][old]['select all'], label=data['menu'][new]['select all'])
        self.edit_menu.entryconfig(data['menu'][old]['clear'], label=data['menu'][new]['clear'])

        self.options_menu.entryconfig(data['menu'][old]['tongues'], label=data['menu'][new]['tongues'])
        self.options_menu.entryconfig(data['menu'][old]['confirm'], label=data['menu'][new]['confirm'])
        self.options_menu.entryconfig(data['menu'][old]['basename'], label=data['menu'][new]['basename'])
        
        self.help_menu.entryconfig(data['menu'][old]['about'], label=data['menu'][new]['about'])

        self.status_bar.config(text=data['messages'][new]['started'])

    def build(self):
        data = self.jyx.data
        tongue = self.jyx.options['tongue'].get()
        languages = self.jyx.data['languages']
        
        self.file_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label=data['menu'][tongue]['file'], menu=self.file_menu)
        self.file_menu.add_command(label=data['menu'][tongue]['new'], command=self.jyx.new,
                                   accelerator="Ctrl+N")
        self.file_menu.add_command(label=data['menu'][tongue]['open'], command=self.jyx.open,
                                   accelerator="Ctrl+O")
        self.file_menu.add_command(label=data['menu'][tongue]['save'], command=self.jyx.save,
                                   accelerator="Ctrl+S")
        self.file_menu.add_command(label=data['menu'][tongue]['save as'], command=self.jyx.save_as,
                                   accelerator="Ctrl+Shift+S")
        self.file_menu.add_command(label=data['menu'][tongue]['save all'], command=self.jyx.save,
                                   accelerator="Ctrl+Alt+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label=data['menu'][tongue]['run'], command=self.jyx.run,
                                   accelerator="F5")
        self.file_menu.add_separator()
        self.file_menu.add_command(label=data['menu'][tongue]['exit'], command=self.jyx.exit,
                                   accelerator="Ctrl+Q")

        self.edit_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label=data['menu'][tongue]['edit'], menu=self.edit_menu)
        self.edit_menu.add_command(label=data['menu'][tongue]['undo'], command=lambda: self.jyx.notebook.send('undo'),
                                   accelerator="Ctrl+Z")
        self.edit_menu.add_command(label=data['menu'][tongue]['redo'], command=lambda: self.jyx.notebook.send('redo'),
                                   accelerator="Ctrl+Y")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label=data['menu'][tongue]['cut'], command=lambda: self.jyx.notebook.send('cut'),
                                   accelerator="Ctrl+X")
        self.edit_menu.add_command(label=data['menu'][tongue]['copy'], command=lambda: self.jyx.notebook.send('copy'),
                                   accelerator="Ctrl+C")
        self.edit_menu.add_command(label=data['menu'][tongue]['paste'], command=lambda: self.jyx.notebook.send('paste'),
                                   accelerator="Ctrl+V")
        self.edit_menu.add_command(label=data['menu'][tongue]['select all'],
                                   command=lambda: self.jyx.notebook.send('select all'),
                                   accelerator="Ctrl+A")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label=data['menu'][tongue]['clear'],
                                   command=lambda: self.jyx.notebook.send('clear'))
        
        """
        self.display_tree = tkinter.BooleanVar()
        self.display_tree.set(self.options['display_tree'])
        self.options_menu.add_checkbutton(label="Display Tree", onvalue=True, offvalue=False, variable=self.display_tree, command=self.restart)
        """

        self.options_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label=data['menu'][tongue]['options'], menu=self.options_menu)
        tongues = data['menu'].keys()
        sub_tongue_menu = tk.Menu(self.options_menu, tearoff=0)
        self.options_menu.add_cascade(label=data['menu'][tongue]['tongues'], menu=sub_tongue_menu)
        for tong in sorted(tongues):
            sub_tongue_menu.add_radiobutton(label=data['menu'][tong]['tongue'],
                                            variable=self.jyx.options['tongue'].var,
                                            value=tong,
                                            command=lambda: self.jyx.update('tongue'))
        self.options_menu.add_checkbutton(label=data['menu'][tongue]['confirm'], onvalue=True, offvalue=False,
                                          variable=self.jyx.options['confirm'].var,
                                          command=lambda: self.jyx.update('confirm'))
        self.options_menu.add_checkbutton(label=data['menu'][tongue]['basename'], onvalue=True, offvalue=False,
                                          variable=self.jyx.options['basename'].var,
                                          command=lambda: self.jyx.update('basename'))
        self.options_menu.add_checkbutton(label=data['menu'][tongue]['treeview'], onvalue=True, offvalue=False,
                                          variable=self.jyx.options['treeview'].var,
                                          command=lambda: self.jyx.update('treeview'))
        
        self.langmenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label=data['menu'][tongue]['languages'], menu=self.langmenu)

        base = {}
        families = {}
        for lang, prop in languages.items():
            if prop['family'] == "":
                base[lang] = prop
                continue
            elif prop['family'] not in families:
                families[prop['family']] = {}
            families[prop['family']][lang] = prop
        for lang in sorted(base):
            self.langmenu.add_radiobutton(label=languages[lang]['label'],
                                          variable=self.jyx.langage,
                                          value=lang,
                                          command=self.jyx.update_langage)
        if len(families) > 0:
            self.langmenu.add_separator()
        for fam in sorted(families):
            menu = tk.Menu(self.langmenu, tearoff=0)
            self.langmenu.add_cascade(label=fam, menu=menu)
            for lang in sorted(families[fam]):
                menu.add_radiobutton(label=languages[lang]['label'],
                                     variable=self.jyx.langage,
                                     value=lang,
                                     command=self.jyx.update_langage)

        self.help_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label=data['menu'][tongue]['help'], menu=self.help_menu)
        self.help_menu.add_command(label=data['menu'][tongue]['about'], command=self.jyx.about)

        # Status bas
        self.status_bar = tk.Label(self.jyx.get_root(), bd=1, relief=tk.SUNKEN)
        self.status_bar.config(text=data['messages'][tongue]['started'], anchor=tk.E, padx=20)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        """
        self.root.bind('<Control-n>', self.menu_new)
        self.root.bind('<Control-o>', self.menu_open)
        self.root.bind('<Control-s>', self.menu_save)
        self.root.bind('<Control-q>', self.menu_exit)
        self.root.bind('<Control-a>', self.menu_select_all)
        self.root.bind('<Control-z>', self.menu_undo)
        self.root.bind('<Control-y>', self.menu_redo)
        self.root.bind('<F5>', self.menu_exec)
        """


class JyxTree(ttk.Treeview):

    def __init__(self, jyx):
        ttk.Treeview.__init__(self, jyx.get_root())

    
class JyxNotebook(ttk.Notebook):

    def __init__(self, jyx):
        ttk.Notebook.__init__(self, jyx.get_root())
        self.jyx = jyx

        # To make the element at 0,0 grows with the window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.notes = []
        self.new_tab(self)
        self.pack(fill=tk.BOTH, expand=tk.YES)
        self.bind('<<NotebookTabChanged>>', self.on_tab_change)
        self.current().focus()

    def relabel(self, new):
        for i in range(self.index('end')):
            if self.notes[i].filepath is None:
                self.notes[i].update_title()

    def new_tab(self, lang=None):
        if lang is None: lang = self.jyx.data['default_language']
        jn = JyxNote(self, lang)
        self.add(jn.frame, text=self.jyx.data['menu'][self.jyx.options['tongue'].get()]['new'])
        jn.index = self.index('end') - 1
        self.select(jn.index)
        self.notes.append(jn)
        jn.focus()
        return jn.index

    def on_tab_change(self, event):
        self.jyx.update_title()
        self.jyx.update_status()
        
    def current(self):
        return self.notes[self.index("current")]

    def current_index(self):
        return self.index("current")

    def __len__(self):
        return self.index("end")

    def get_position(self):
        return self.current().text.index(tk.INSERT)

    def is_anyone_dirty(self):
        for i in range(self.index("end")):
            if self.notes[i].dirty:
                return True
        return False
    
    def is_dirty(self):
        return self.current().dirty

    def get_filepath(self):
        return self.current().filepath

    def open(self, filename, content):
        _, ext = os.path.splitext(filename)
        lang = self.jyx.data['options']['default_language']
        for key, lg in self.jyx.data['languages'].items():
            if ext in lg['extension']:
                lang = key
                break
        if self.current().dirty or self.current().filepath is not None or len(self) > 1:
            self.new_tab(lang)
        else:
            self.notes[self.index("current")].lang = lang
        self.current().load(filename, content)

    def send(self, order):
        if order == 'cut':
            self.current().cut()
        elif order == 'paste':
            self.current().paste()
        elif order == 'copy':
            self.current().copy()
        elif order == 'select all':
            self.current().select_all()
        elif order == 'clear':
            self.current().clear()
        elif order == 'undo':
            self.current().undo()
        elif order == 'redo':
            self.current().redo()


class JyxNote:

    MOD_SHIFT = 0x0001
    MOD_CONTROL = 0x0004

    def __init__(self, notebook, lang):
        self.notebook = notebook

        self.frame = ttk.Frame(self.notebook) #, bd=2, relief=tk.SUNKEN)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        
        self.scrollbar = ttk.Scrollbar(self.frame)
        self.scrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)

        self.text = tk.Text(self.frame, wrap=tk.NONE, bd=0, undo=True,
                            yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.text.yview)
        
        self.text.config(font=('consolas', 12), undo=True, wrap='word')
        self.text.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        #self.text.bind('<<Paste>>', self.paste)
        #self.text.bind('<<Cut>>', self.cut)
        #self.text.bind('<<Copy>>', self.copy)
        self.text.bind('<KeyPress>', self.update_text_before)
        self.text.bind('<KeyRelease>', self.update_text_after)
        self.text.bind('<ButtonRelease-1>', self.notebook.jyx.update_status)

        self.filepath = None
        self.dirty = False
        self.lang = lang

    def focus(self):
        self.text.focus_force()

    def update_title(self):
        dirty = ' *' if self.dirty else ''
        tongue = self.notebook.jyx.options['tongue'].get()
        if self.filepath is None:
            file = self.notebook.jyx.data['menu'][tongue]['new']
        else:
            file = os.path.basename(self.filepath)
        self.notebook.tab(self.index, text=f"{file}{dirty}")
        self.notebook.jyx.update_title()

    #
    # Handling of state and deleting, writing, loading and saving
    #
    def save(self, filename=None):
        if filename is None:
            filename = self.get_filepath()
        f = open(filename, mode='w', encoding='utf8')
        content = self.text.get(1.0, tk.END)
        f.write(content)
        f.close()
        self.dirty = False
        self.filepath = filename
        self.update_title()
    
    def load(self, filename, content):
        self.clear()
        self.text.insert('1.0', content)
        self.text.edit_reset()
        self.dirty = False
        self.filepath = filename
        self.text.see(tk.INSERT)
        self.update_title()
    
    def write(self, content, at=tk.INSERT):
        self.text.insert(at, content)
        self.text.edit_separator()
        self.dirty = True
        self.update_title()

    def delete(self, first, last=None):
        self.text.delete(first, last)
        self.text.edit_separator()
        self.dirty = True
        self.update_title()

    def undo(self):
        try:
            self.text.edit_undo()
            self.dirty = True
            self.update_title()
        except tk.TclError:
            self.notebook.jyx.log.info("Nothing to undo")

    def redo(self):
        try:
            self.text.edit_redo()
            self.dirty = True
            self.update_title()
        except tk.TclError:
            self.notebook.jyx.log.info("Nothing to redo")

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
            self.text.tag_add(tk.SEL, f'{index1}', f'{index2}')
        else:
            self.text.tag_add(tk.SEL, f'{index2}', f'{index1}')

    def selection_clear(self):
        self.text.tag_remove(tk.SEL, '1.0', tk.END)

    #
    # Basic functions (called from menu without event)
    #
    def paste(self, event=None):
        content = self.notebook.jyx.root.clipboard_get()
        self.text.insert(tk.INSERT, content)
        self.text.see(tk.INSERT)
        return 'break'

    def cut(self, event=None):
        self.copy(event)
        self.selection_delete()
        self.text.see(tk.INSERT)
        return 'break'

    def copy(self, event=None):
        self.notebook.jyx.root.clipboard_clear()
        self.notebook.jyx.root.clipboard_append(self.selection_get())
        return 'break'

    def select_all(self, event=None):
        self.selection_clear()
        self.selection_set('1.0', tk.END)
        self.text.mark_set(tk.INSERT, tk.END)
        self.text.see(tk.INSERT)
        return 'break'

    def clear(self, event=None):
        self.select_all(event)
        self.selection_delete()

    #
    # React to key events
    #
    def update_text_before(self, event):
        print('update')
        text = event.widget
        if JyxNote.MOD_CONTROL & event.state:
            print(event.keysym)
            if event.keysym == 'a':
                self.select_all()
            elif event.keysym in ['n', 't']:
                self.notebook.new_tab()
            elif event.keysym == 'z':
                self.undo()
            elif event.keysym == 'y':
                self.redo()
            elif event.keysym == 'c':
                self.copy()
            elif event.keysym == 'x':
                self.cut()
            elif event.keysym == 'v':
                self.paste()
            else:
                self.notebook.jyx.log.warn('Event not handled: ' + event.keysym)
                return 'break'
            return 'break'
        elif event.keysym == 'Control_L':
            return 'break'
        elif event.keysym in ['Left', 'Right', 'Up', 'Down', 'End', 'Home']: # 37, 39
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
            if JyxNote.MOD_SHIFT & event.state:
                self.selection_set(nex, self.start)
            text.mark_set(tk.INSERT, f'{nex}')
            text.see(tk.INSERT)
            self.notebook.jyx.update_status()
            return 'break'
        elif event.keysym == 'BackSpace':
            if len(text.tag_ranges('sel')) > 0:
                self.selection_delete()
            else:
                text.mark_set(tk.INSERT, 'insert-1c')
                self.delete(tk.INSERT)
            self.notebook.jyx.update_status()
            return 'break'
        elif event.keysym == 'Delete':
            if len(text.tag_ranges('sel')) > 0:
                self.selection_delete()
            self.notebook.jyx.update_status()
            return 'break'
        elif event.keysym == 'Escape':
            self.selection_clear()
            self.notebook.jyx.update_status()
            return 'break'
        elif event.char == '\r':
            content = '\n'
        elif event.char == '\t':
            content = '    '
        elif event.keysym == 'space':
            content = ' '
        elif event.char.isprintable(): #isalnum()
            self.notebook.jyx.log.info(event)
            content = event.char
        else:
            self.notebook.jyx.log.info('Unknown:', event)
            return 'break'
        if len(text.tag_ranges('sel')) > 0:
            self.selection_delete()
        self.write(content)
        c = event.widget.get("insert linestart", "insert lineend")
        self.notebook.jyx.log.info(c)
        if c.startswith('http://'):
            text.tag_add('a', 'insert linestart', tk.INSERT)
        else:
            text.tag_remove('a', 'insert linestart', tk.INSERT)
        text.see(tk.INSERT)
        self.notebook.jyx.update_status()
        return 'break'

    def update_text_after(self, event):
        if self.notebook.jyx.has(f"languages.{self.lang}.support", "tokenize"):
            self.nootebook.jyx.log.info("tokens available!")
        #else:
        #    self.notebook.jyx.log.info("no tokens")
        #print('h', event)
        res = event.widget.search('--> ', "insert linestart", "insert lineend")
        while res != '':
            self.notebook.jyx.log.info(res)
            self.delete(res, res + '+4c')
            self.write(res, '→ ')
            res = event.widget.search('--> ', res, "insert lineend")
        return 'break'

    #
    # Tag
    #
    def tag(self):
        if not self.notebook.jyx.has(f"languages.{self.lang}.support", "tokenize"):
            return
        # Clear all tags
        for tag in text.tag_names():
            text.tag_remove(tag, 1.0)
        content = self.text.get(1.0, tk.END)
        tokens = Lexer().lex(self.lang, content)

#-------------------------------------------------------------------------------

class Token:

    def __init__(self, pos, typ, value):
        self.pos = pos
        self.typ = typ
        self.val = value

    def __str__(self):
        return f"({self.val}:{self.typ}@{self.pos})"

class Machine:

    def __init__(self):
        self.states = {}

    def add(self, name):
        s = State(name)
        self.states[name] = s
        return s

    def run(self, iterable, discard=None):
        tokens = []
        state = self.states['init']
        nb = 0
        length = 0
        while nb < len(iterable):
            nex = state.react(iterable, nb)
            elem = iterable[nb]
            if nex is None:
                raise Exception(f'Not suitable next state for {elem} at {nb} in {state.name}')
            if nex.arrival == state.name:
                nb += len(nex)
                length += len(nex)
                print(f'Staying in {state} at char {elem}')
            else:
                if nex.take:
                    nb += len(nex)
                    length += len(nex)
                if nex.verse is True:
                    print(f'Moving on {nex.arrival} at char {elem} without creating token')
                elif discard is None or state.name not in discard:
                    tokens.append(Token(nb - length, state.name, content[nb - length:nb]))
                    length = 0
                    print(f'Moving on {nex.arrival} at char {elem} and creating token {state.name}')
            state = self.states[nex.arrival]
        if length != 0:
            #if nex.verse is True:
            #    raise Exception(f'Finishing on state {state.name} which is versing')
            if discard is None or state.name not in discard:
                tokens.append(Token(len(iterable) - length, state.name, content[len(iterable) - length:]))
        return tokens

    def dot(self, filename):
        f = open(filename, mode='w', encoding='utf8')
        f.write('digraph graphname {\n')
        for _, s in self.states.items():
            for t in s.trans:
                f.write(f"    {s.name} -> {t.arrival} [label=\"{t.on_str()}\"];\n")
        f.write('}\n')
        f.close()

class State:

    def __init__(self, name):
        self.name = name
        self.trans = []
        self.substates = {}

    def __str__(self):
        return f"({self.name} {len(self.trans)} tra {len(self.substates)} sub)"

    def add(self, on, arrival, pos=None, nex=None, take=False, verse=False):
        self.trans.append(Transition(self, on, arrival, pos, nex, take, verse))

    def sub(self, name, iterable):
        self.substates[name] = iterable

    def react(self, iterable, index):
        matches = []
        for trans in self.trans:
            #print('>', iterable[index:index+len(trans)])
            if trans.match(iterable[index:index+len(trans)]):
                matches.append(trans)
        if len(matches) == 0:
            return None
        elif len(matches) > 1:
            maxlen = 0
            for m in matches:
                if len(m) > maxlen:
                    maxlen = len(m)
            filtered_maxlen = []
            for m in matches:
                if len(m) == maxlen:
                    filtered_maxlen.append(m)
            if len(filtered_maxlen) > 1:
                s = ''
                for m in filtered_maxlen:
                    s += str(m) + ' '
                raise Exception(f'Ambiguous transitions on {elem}: {s}')
            else:
                return filtered_maxlen[0]
        elif len(matches) == 1:
            return matches[0]


class Elem:

    def __init__(self, char=None, all_digit=False, all_alpha=False, all_blank=False, any_char=False, class_chars=None):
        self.char = char
        self.all_digit = all_digit
        self.all_alpha = all_alpha
        self.all_blank = all_blank
        self.any_char = any_char
        self.class_chars = class_chars
        if (self.all_digit or self.all_alpha or self.all_blank or self.class_chars is not None) and self.char is not None:
            raise Exception('Cannot define an elem with a literal char and a modifier or a class')

    def __str__(self):
        if self.char is not None:
            if self.char == '"':
                return '\\"'
            else:
                return self.char
        elif self.all_digit and self.all_alpha:
            return '<alnum>'
        elif self.all_digit:
            return '<digit>'
        elif self.all_alpha:
            return '<alpha>'
        elif self.all_blank:
            return '<blank>'
        elif self.any_char:
            return '<any>'
        elif self.class_chars is not None:
            return str(self.class_chars)

    def match(self, thing):
        if self.char is not None:
            return thing == self.char
        elif self.any_char is True:
            return thing != '\n'
        elif self.all_digit and self.all_alpha:
            return thing.alnum()
        elif self.all_digit is True:
            return thing.isdigit()
        elif self.all_alpha is True:
            return thing.isalpha()
        elif self.all_blank is True:
            return elem in [' ', '\t']
        elif self.class_chars is not None:
            return thing in self.class_chars
        

class Transition:

    def __init__(self, origin, on, arrival, pos, nex, take, verse=False):
        self.origin = origin
        self.on = []
        cnt = len(on)
        while cnt := len(on) > 0:
            if on.startswith('<digit>'):
                self.on.append(Elem(all_digit=True))
                on = on[7:]
            elif on.startswith('<alpha>'):
                self.on.append(Elem(all_alpha=True))
                on = on[7:]
            elif on.startswith('<alnum>'):
                self.on.append(Elem(all_digit=True, all_alpha=True))
            elif on.startswith('<all>'):
                self.on.append(Elem(any_char=True))
            elif on.startswith('<blank>'):
                self.on.append(Elem(any_blank=True))
            elif on[0] == '[':
                end = on.index(']')
                lst = []
                for e in on[1:end]:
                    lst.append(e)
                self.on.append(Elem(class_chars=lst))
                on = on[end+1:]
            else:
                self.on.append(Elem(char=on[0]))
                on = on[1:]
        self.arrival = arrival
        self.pos = pos
        self.nex = nex
        self.take = take
        self.verse = verse # le contenu de l'état précédent est "versé" dans le nouveau, no new token et l'état suivant récup tous les élem

    def __len__(self):
        return len(self.on)

    def on_str(self):
        s = ''
        for o in self.on:
            s += str(o)
        return s

    def match(self, elem):
        res = True
        length = min(len(self.on), len(elem))
        if len(self.on) != len(elem):
            print(f'warning on= {self.on} and elem= {elem}')
        for i in range(length):
            res = self.on[i].match(elem[i])
            if not res:
                break
        return res

    def __str__(self):
        return f"{self.origin} -[{self.on})-> {self.arrival}"

#-------------------------------------------------------------------------------

lexerLua = Machine()

sInit = lexerLua.add('init')
sNum  = lexerLua.add('number')
sInt  = lexerLua.add('integer')
sInt2 = lexerLua.add('integer_binary')
sInt8 = lexerLua.add('integer_octal')
sInt16= lexerLua.add('integer_hexa')
sFlt  = lexerLua.add('float')
sStr  = lexerLua.add('string')
sId   = lexerLua.add('identifier')
sOp   = lexerLua.add('operator')
sSep  = lexerLua.add('separator')

sBoo  = sId.sub('boolean', ['true', 'false'])
sKey  = sId.sub('keyword',  ['if', 'while', 'do', 'then', 'elif', 'else', 'end'])

#sLst  = lexerLua.add('list')
#sDic  = lexerLua.add('dict')

sInit.add(' ', 'init')
sInit.add('<digit>', 'number')
sInit.add('<alpha>', 'identifier')
sInit.add('"', 'string')
sInit.add('+', 'operator')
sInit.add('-', 'operator')
sInit.add('*', 'operator')
sInit.add('/', 'operator')
sInit.add('%', 'operator')
sInit.add('>', 'operator')
sInit.add('<', 'operator')
sInit.add('.', 'operator')
sInit.add('=', 'operator')
sInit.add('0x', 'integer_hexa', take=True, verse=True)
sInit.add('0X', 'integer_hexa', take=True, verse=True)
sInit.add('0c', 'integer_octal', take=True, verse=True)
sInit.add('0C', 'integer_octal', take=True, verse=True)
sInit.add('0b', 'integer_binary', take=True, verse=True)
sInit.add('0B', 'integer_binary', take=True, verse=True)

#sInt2.add('0', 'integer_binary')
#sInt2.add('1', 'integer_binary')
sInt2.add('[01]', 'integer_binary')
sInt2.add(' ', 'init')

sInt8.add('0', 'integer_octal')
sInt8.add('1', 'integer_octal')
sInt8.add('2', 'integer_octal')
sInt8.add('3', 'integer_octal')
sInt8.add('4', 'integer_octal')
sInt8.add('5', 'integer_octal')
sInt8.add('6', 'integer_octal')
sInt8.add('7', 'integer_octal')
sInt8.add(' ', 'init')

sInt16.add('<digit>', 'integer_hexa')
sInt16.add('a', 'integer_hexa')
sInt16.add('A', 'integer_hexa')
sInt16.add('b', 'integer_hexa')
sInt16.add('B', 'integer_hexa')
sInt16.add('c', 'integer_hexa')
sInt16.add('C', 'integer_hexa')
sInt16.add('d', 'integer_hexa')
sInt16.add('D', 'integer_hexa')
sInt16.add('e', 'integer_hexa')
sInt16.add('E', 'integer_hexa')
sInt16.add('f', 'integer_hexa')
sInt16.add('F', 'integer_hexa')
sInt16.add(' ', 'init')

sNum.add('<digit>', 'number')
sNum.add('+', 'operator')
sNum.add('-', 'operator')
sNum.add('*', 'operator')
sNum.add('/', 'operator')
sNum.add('%', 'operator')
sNum.add('.<digit>', 'float', take=True, verse=True)
sNum.add('.<alpha>', 'operator')
sNum.add(' ', 'init')

sFlt.add('<digit>', 'float')
sFlt.add('+', 'operator')
sFlt.add('-', 'operator')
sFlt.add('*', 'operator')
sFlt.add('/', 'operator')
sFlt.add('%', 'operator')
sFlt.add(' ', 'init')

sId.add('<alpha>', 'identifier')
sId.add('+', 'operator')
sId.add('-', 'operator')
sId.add('*', 'operator')
sId.add('/', 'operator')
sId.add('%', 'operator')
sId.add(' ', 'init')

sOp.add('+', 'init', take=True)
sOp.add('-', 'init', take=True)
sOp.add('*', 'init', take=True)
sOp.add('**', 'init', take=True)
sOp.add('/', 'init', take=True)
sOp.add('//', 'init', take=True)
sOp.add('%', 'init', take=True)
sOp.add('>>', 'init', take=True)
sOp.add('<<', 'init', take=True)
sOp.add('.', 'init', take=True)
sOp.add('=', 'init', take=True)
sOp.add('+=', 'init', take=True)
sOp.add('-=', 'init', take=True)
sOp.add('*=', 'init', take=True)
sOp.add('**=', 'init', take=True)
sOp.add('/=', 'init', take=True)
sOp.add('//=', 'init', take=True)
sOp.add('%=', 'init', take=True)
sOp.add('<', 'init', take=True)
sOp.add('>', 'init', take=True)
sOp.add('!=', 'init', take=True)
sOp.add('<=', 'init', take=True)
sOp.add('>=', 'init', take=True)
sOp.add(' ', 'init')

print('------------------------------')
#content = "0b10"
content = "123 + 5 ** 2 + 1.abc/8.7 + 0b0101"
print(f'{content=}')
print('------------------------------')
tokens = lexerLua.run(content) #, discard=['init'])
print('------------------------------')
for t in tokens:
    print(t)
print('------------------------------')
lexerLua.dot('output.dot')

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    Jyx()

