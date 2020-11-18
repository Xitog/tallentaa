#!/usr/bin/env python3

#
# Imports
#

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

import json # for loading/saving options
from datetime import datetime # for now()
import os # for getcwd()
import os.path # for basename()

#
# Globals and constants
#

# None

#
# Classes
#

class Jyx:

    TITLE = 'Jyx'
    RUN_COMMAND = 6
    CONFIG_FILE_NAME = 'jyx.json'
    VERSION = '0.0.1'
    
    def __init__(self):
        # Load data
        f = open(Jyx.CONFIG_FILE_NAME, 'r', encoding='utf8')
        self.data = json.load(f)
        f.close()
        # Init
        self.root = tk.Tk()
        self.root.protocol('WM_DELETE_WINDOW', self.exit)
        # Vars
        self.vars = {}
        self.prev = {}
        self.vars['tongue'] = tk.StringVar()
        self.vars['tongue'].set(self.data['options']['tongue'])
        self.vars['language'] = tk.StringVar()
        self.vars['language'].set(self.data['options']['default_language'])
        self.vars['confirm'] = tk.BooleanVar()
        self.vars['confirm'].set(self.data['options']['confirm'])
        self.vars['basename'] = tk.BooleanVar()
        self.vars['basename'].set(self.data['options']['basename'])
        for k, v in self.vars.items():
            self.prev[k] = v
        # UI components
        self.text = JyxText(self)
        self.menu = JyxMenu(self)
        self.root.config(menu=self.menu)
        # Updall vars, cannot be called until the menu is completed
        self.update_all_vars() 
        self.update_title()
        # Starting
        self.root.mainloop()

    def get_root(self):
        return self.root

    def update_title(self):
        dirty = ' *' if self.text.dirty else ''
        tongue = self.data['tongue']
        if self.text.file is None:
            file = self.data['menu'][tongue]['new']
        elif self.vars['basename'].get():
            file = os.path.basename(self.text.file)
        else:
            file = self.text.file
        self.root.wm_title(f"{Jyx.TITLE} {Jyx.VERSION} - {file}{dirty}")

    def update_status(self, event=None):
        self.menu.status_bar.configure(text=self.text.text.index(tk.INSERT))

    def update_all_vars(self):
        for varname in self.vars:
            self.update(varname, True)

    def update(self, varname, init=False):
        value = self.vars[varname].get()
        print(f"var {varname} = {value}")
        if varname in self.vars:
            self.data[varname] = value
            if varname == 'language':
                if not self.has(f"languages.{value}.support", "execute"):
                    self.menu.file_menu.entryconfig(Jyx.RUN_COMMAND, state=tk.DISABLED)
                else:
                    self.menu.file_menu.entryconfig(Jyx.RUN_COMMAND, state=tk.ACTIVE)
            elif varname == 'tongue' and not init:
                self.menu.relabel(old=self.prev[varname], new=value)
            elif varname == 'basename' and not init:
                self.update_title()
        else:
            raise Exception(f'Variable unknown: {varname}')
        self.prev[varname] = value

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
        tongue = self.vars['tongue'].get()
        if self.text.dirty and self.vars['confirm'].get():
            title = self.data['messages'][tongue]['unsaved']
            msg = self.data['messages'][tongue]['unsaved_msg']
            if messagebox.askyesno("Unsaved changes", msg, default=messagebox.NO):
                self.root.destroy()
        else:
            self.root.destroy()

    def new(self, event=None):
        pass

    def open(self, event=None):
        options = {}
        #options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*')]
        options['initialdir'] = os.getcwd()
        options['initialfile'] = 'myfile.' + self.vars['language'].get()
        options['parent'] = self.root
        options['title'] = 'Open file...'
        filename = filedialog.askopenfilename(**options)
        f = open(filename, mode='r', encoding='utf8')
        content = None
        try:
            content = f.read()
        except UnicodeDecodeError as ude:
            print("[ERROR] Encoding error: unable to open file: " + filename)
            print(ude)
        finally:
            f.close()
        if content is not None:
            if not self.text.dirty and self.text.file is None:
                self.text.load(filename, content)
        _, ext = os.path.splitext(filename)
        for key, lang in self.data['languages'].items():
            if ext in lang['extension']:
                self.vars['language'].set(key)
                self.update('language')

    def save(self, event=None):
        pass

    def run(self, event=None):
        pass

    def undo(self, event=None):
        pass

    def redo(self, event=None):
        pass

    def about(self, event=None):
        tongue = self.vars['tongue'].get()
        title = self.data['menu'][tongue]['about']
        msg = self.data['messages'][tongue]['about_msg']
        messagebox.showinfo(title, f"{Jyx.TITLE} - {Jyx.VERSION}\n{msg}\nDamien Gouteux\n2017 - {datetime.now().year}\n")


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
        tongue = self.jyx.vars['tongue'].get()
        languages = self.jyx.data['languages']
        
        self.file_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label=data['menu'][tongue]['file'], menu=self.file_menu)
        self.file_menu.add_command(label=data['menu'][tongue]['new'], command=self.jyx.new, accelerator="Ctrl+N")
        self.file_menu.add_command(label=data['menu'][tongue]['open'], command=self.jyx.open, accelerator="Ctrl+O")
        self.file_menu.add_command(label=data['menu'][tongue]['save'], command=self.jyx.save, accelerator="Ctrl+S")
        self.file_menu.add_command(label=data['menu'][tongue]['save as'], command=self.jyx.save, accelerator="Ctrl+Shift+S")
        self.file_menu.add_command(label=data['menu'][tongue]['save all'], command=self.jyx.save, accelerator="Ctrl+Alt+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label=data['menu'][tongue]['run'], command=self.jyx.run, accelerator="F5")
        self.file_menu.add_separator()
        self.file_menu.add_command(label=data['menu'][tongue]['exit'], command=self.jyx.exit, accelerator="Ctrl+Q")

        self.edit_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label=data['menu'][tongue]['edit'], menu=self.edit_menu)
        self.edit_menu.add_command(label=data['menu'][tongue]['undo'], command=self.jyx.undo, accelerator="Ctrl+Z")
        self.edit_menu.add_command(label=data['menu'][tongue]['redo'], command=self.jyx.redo, accelerator="Ctrl+Y")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label=data['menu'][tongue]['cut'], command=self.jyx.text.cut, accelerator="Ctrl+X")
        self.edit_menu.add_command(label=data['menu'][tongue]['copy'], command=self.jyx.text.copy, accelerator="Ctrl+C")
        self.edit_menu.add_command(label=data['menu'][tongue]['paste'], command=self.jyx.text.paste, accelerator="Ctrl+V")
        self.edit_menu.add_command(label=data['menu'][tongue]['select all'], command=self.jyx.text.select_all, accelerator="Ctrl+A")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label=data['menu'][tongue]['clear'], command=self.jyx.text.clear) #, accelerator="Ctrl+A")
        
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
                                            variable=self.jyx.vars['tongue'],
                                            value=tong,
                                            command=lambda: self.jyx.update('tongue'))
        self.options_menu.add_checkbutton(label=data['menu'][tongue]['confirm'], onvalue=True, offvalue=False,
                                          variable=self.jyx.vars['confirm'],
                                          command=lambda: self.jyx.update('confirm'))
        self.options_menu.add_checkbutton(label=data['menu'][tongue]['basename'], onvalue=True, offvalue=False,
                                          variable=self.jyx.vars['basename'],
                                          command=lambda: self.jyx.update('basename'))

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
                                          variable=self.jyx.vars['language'],
                                          value=lang,
                                          command=lambda: self.jyx.update('language'))
        self.langmenu.add_separator()
        for fam in sorted(families):
            menu = tk.Menu(self.langmenu, tearoff=0)
            self.langmenu.add_cascade(label=fam, menu=menu)
            for lang in sorted(families[fam]):
                menu.add_radiobutton(label=languages[lang]['label'],
                                     variable=self.jyx.vars['language'],
                                     value=lang,
                                     command=lambda: self.jyx.update('language'))#, indicatoron=0

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

class JyxText: #(tk.Text):

    def __init__(self, parent):
        #tk.Text.__init__(self, parent.get_root())
        self.jyx = parent
        self.dirty = False
        self.file = None
        
        frame = ttk.Frame(self.jyx.root) #, bd=2, relief=tk.SUNKEN)
        # To make the element at 0,0 grows with the window
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        horizontal_scrollbar = ttk.Scrollbar(frame)
        horizontal_scrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)
        self.text = tk.Text(frame, wrap=tk.NONE, bd=0,
                            yscrollcommand=horizontal_scrollbar.set)
        horizontal_scrollbar.configure(command=self.text.yview)
        self.text.config(font=('consolas', 12), undo=True, wrap='word')
        self.text.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.text.bind('<<Paste>>', self.paste)
        self.text.bind('<<Cut>>', self.cut)
        self.text.bind('<<Copy>>', self.copy)
        self.text.bind('<KeyPress>', self.update_text_before)
        self.text.bind('<KeyRelease>', self.update_text_after)
        self.text.bind('<ButtonRelease-1>', self.jyx.update_status)
        
        self.text.tag_config("a", foreground="blue", underline=1)

        self.start = None
        
        frame.pack(fill=tk.BOTH, expand=tk.YES)
        self.text.focus_force()

    #
    # Handling of state
    #
    def load(self, file, content):
        self.clear()
        self.text.insert('1.0', content)
        self.dirty = False
        self.file = file
        self.jyx.update_title()
        self.text.see(tk.INSERT)
    
    def write(self, content, at=tk.INSERT):
        self.text.insert(at, content)
        self.dirty = True
        self.jyx.update_title()

    def delete(self, first, last=None):
        self.text.delete(first, last)
        self.dirty = True
        self.jyx.update_title()

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
    # Basic functions (called from menu without event)
    #
    def paste(self, event=None):
        content =  self.jyx.root.clipboard_get()
        self.text.insert(tk.INSERT, content)
        return 'break'

    def cut(self, event=None):
        self.copy(event)
        self.selection_delete()
        return 'break'

    def copy(self, event=None):
        self.jyx.root.clipboard_clear()
        self.jyx.root.clipboard_append(self.selection_get())
        return 'break'

    def select_all(self, event=None):
        self.selection_clear()
        self.selection_set('1.0', tk.END)
        return 'break'

    def clear(self, event=None):
        self.select_all(event)
        self.selection_delete()
        
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
            self.jyx.update_status()
            return 'break'
        elif event.keysym == 'BackSpace':
            if len(text.tag_ranges('sel')) > 0:
                self.selection_delete()
            else:
                text.mark_set(tk.INSERT, 'insert-1c')
                self.delete(tk.INSERT)
            self.jyx.update_status()
            return 'break'
        elif event.keysym == 'Delete':
            if len(text.tag_ranges('sel')) > 0:
                self.selection_delete()
            self.jyx.update_status()
            return 'break'
        elif event.keysym == 'Escape':
            self.selection_clear()
            self.jyx.update_status()
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
        self.jyx.update_status()
        return 'break'

    def update_text_after(self, event):
        language = self.jyx.vars['language'].get()
        if self.jyx.has(f"languages.{language}.support", "tokenize"):
            print("tokens available!")
        else:
            print("no tokens")
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

