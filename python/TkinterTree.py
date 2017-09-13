# Created the ‎lundi ‎6 ‎juin ‎2016 (début des tests tkinter)

import tkinter # as tk
from tkinter import ttk # not found in 2.7.11 but found in 3.5.1 :-)
from tkinter import filedialog
from tkinter import messagebox   
from tkinter import font
import configparser
import os.path

class Logger:
    
    def __init__(self, exit_on_error = True):
        self.exit_on_error = exit_on_error
    
    def warn(self, msg):
        print('[WARNING] ' + str(msg))
    
    def info(self, msg):
        print('[INFO] ' + str(msg))
    
    def error(self, msg):
        print('[ERROR] ' + str(msg))
        if self.exit_on_error:
            exit()


class RessourceManager:
    
    def __init__(self, logger):
        self.ressources = {}
        self.log = logger
    
    def from_file(self, filepath):
        key = os.path.splitext(os.path.basename(filepath))[0] # suppress .extension
        if os.path.isfile(filepath):
            self.ressources[key] = filepath
            self.log.info('Ressource registered from file: ' + filepath)
        else:
            self.ressources[key] = None
            self.log.error('Ressource could not be found: ' + filepath)
    
    def get(self, key):
        return self.ressources[key]
    
    def getAsImage(self, key):
        if self.found(key):
            return tkinter.PhotoImage(file=self.ressources[key])
        else:
            raise Exception("Ressource could not be found")
    
    def found(self, key):
        return self.ressources[key] is not None


class Application:
    
    def __init__(self):
        self.log = Logger(False)
        self.rc = RessourceManager(self.log)
        self.rc.from_file(r'icons\iconyellowcube16x19_F5i_icon.ico')
        self.title = 'Pyx'
        
        # config
        self.options = {}
        # base options
        self.options['display_tree'] = True
        self.options['lang'] = 'txt'
        # try to load options
        if os.path.isfile('TkinterTree.ini'):
            config = configparser.ConfigParser()
            config.read('TkinterTree.ini')
            if 'MAIN' in config:
                if 'display_tree' in config['MAIN']:
                    self.options['display_tree'] = (config['MAIN']['display_tree'] == 'True')
                    self.log.info('Display tree is : ' + str(self.options['display_tree']))
        # create default option file
        else:
            self.write_options()
        self.start()
    
    def write_options(self):
        config = configparser.ConfigParser()
        config['MAIN'] = { 'display_tree' : str(self.options['display_tree']) }
        with open('TkinterTree.ini', 'w') as configfile:
            config.write(configfile)
    
    def update(self):
        self.after_id = self.root.after(1000, self.update)
    
    def update_status_bar(self, event):
        s = self.text.index(tkinter.INSERT)
        self.status_bar.config(text=s)
        
    def set_title(self, filename=None):
        if filename is None:
            self.root.wm_title(self.title + " - New *")
        else:
            self.root.wm_title(self.title + " - " + filename)
    
    def make_menu(self):
        "Build the menu"
        self.menu = tkinter.Menu(self.root)
        self.root.config(menu=self.menu)
        self.filemenu = tkinter.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="New", command=self.menu_new, accelerator="Ctrl+N")
        self.filemenu.add_command(label="Open...", command=self.menu_open, accelerator="Ctrl+O")
        self.filemenu.add_command(label="Save As...", command=self.menu_save, accelerator="Ctrl+S")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.menu_exit, accelerator="Ctrl+Q")
        
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
        
        self.options_menu = tkinter.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Options", menu=self.options_menu)
        self.options_menu.add_checkbutton(label="Display Tree", onvalue=True, offvalue=False, variable=self.display_tree, command=self.restart)
        
        self.lang = tkinter.StringVar()
        self.lang.set(self.options['lang'])
        
        self.langmenu = tkinter.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Language", menu=self.langmenu)
        self.langmenu.add_radiobutton(label="Plain text", variable=self.lang, value="txt", command=self.update_lang)#, indicatoron=0
        self.langmenu.add_separator()
        self.langmenu.add_radiobutton(label="Python", variable=self.lang, value="py", command=self.update_lang)#, indicatoron=0
        self.langmenu.add_separator()
        self.langmenu.add_radiobutton(label="JSON", variable=self.lang, value="json", command=self.update_lang)#, indicatoron=0
        self.langmenu.add_radiobutton(label="XML", variable=self.lang, value="xml", command=self.update_lang)#, indicatoron=0
        
        self.helpmenu = tkinter.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=self.helpmenu)
        self.helpmenu.add_command(label="About...", command=self.menu_about)
        
        self.root.bind('<Control-n>', self.menu_new)
        self.root.bind('<Control-o>', self.menu_open)
        self.root.bind('<Control-s>', self.menu_save)
        self.root.bind('<Control-q>', self.menu_exit)
        self.root.bind('<Control-a>', self.menu_select_all)
        
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
        self.set_title()
        if self.rc.found('iconyellowcube16x19_F5i_icon'):
            self.root.iconbitmap(self.rc.get('iconyellowcube16x19_F5i_icon'))
        self.root.minsize(width=800, height=600)
        #root.title("Jyx")
        #root.geometry("600x400")
        self.frame = MyFrame(self)
        self.text = self.frame.text
        self.make_menu()
        self.make_status_bar()
        self.update()
    
    def restart(self):
        content = self.text.get(1.0, tkinter.END)
        self.options['display_tree'] = self.display_tree.get()
        self.root.after_cancel(self.after_id)
        self.menu_exit()
        self.write_options()
        self.start()
        self.text.insert("1.0", content)
        
    def run(self):
        self.frame.mainloop()
    
    #-------------------------------------------------------
    # Menu functions
    #-------------------------------------------------------
    
    def menu_about(self):
        messagebox.showinfo("About", self.title + " - Damien Gouteux, 2017\nMade with ❤")

    def menu_exit(self, event=None):
        self.root.destroy()
        #root.quit()
        #exit(0)

    def menu_new(self, event=None):
        self.new()
    
    def menu_open(self, event=None):
        """Returns an opened file in read mode."""
        options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('text files', '.txt'), ('python files', '.py'), ('lua files', '.lua'), ('all files', '.*')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'myfile.txt'
        options['parent'] = self.root
        options['title'] = 'Open file...'
        self.load(filedialog.askopenfilename(**options)) # mode='r', 

    def menu_save(self, event=None):
        options = {}
        #options['defaultextension'] = '.txt'
        options['filetypes'] = [('text files', '.txt'), ('python files', '.py'), ('lua files', '.lua'), ('all files', '.*')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'myfile.txt'
        options['parent'] = self.root
        options['title'] = 'Save file...'
        filename = filedialog.asksaveasfilename(**options) # mode='w', 
        if filename:
            self.save(filename)
    
    def menu_undo(self, event=None):
        try:
            self.text.edit_undo()
        except tkinter.TclError as tk:
            self.log.warn("Nothing to undo")
    
    def menu_redo(self, event=None):
        try:
            self.text.edit_redo()
        except tkinter.TclError as tk:
            self.log.warn("Nothing to redo")
    
    def menu_cut(self, event=None):
        self.text.event_generate("<<Cut>>")
    
    def menu_copy(self, event=None):
        self.text.event_generate("<<Copy>>")
    
    def menu_paste(self, event=None):
        self.text.event_generate("<<Paste>>")
    
    def menu_select_all(self, event=None):
        self.frame.escape_refresh(2)
        self.text.tag_add(tkinter.SEL, "1.0", tkinter.END)
    
    #-------------------------------------------------------
    # Text functions
    #-------------------------------------------------------

    def new(self):
        self.clear()
        self.set_title()
    
    def clear(self):
        self.text.delete("1.0", tkinter.END)

    def load(self, filename : str):
        self.text.delete("1.0", tkinter.END)
        f = open(filename, mode='r')
        content = f.read()
        f.close()
        self.clear()
        self.text.insert("1.0", content) # or END, content
        self.set_title(filename)

    def save(self, filename : str):
        f = open(filename, mode='w')
        content = self.text.get(1.0, tkinter.END)
        f.write(content)
        f.close()
        self.set_title(filename)


class Token:
    
    SEPARATOR = "sep"
    KEYWORD = "kw"
    TEXT = "txt"
    STRING = "str"
    
    def __init__(self, content, start, length, typ):
        self.content = content
        self.start = start
        self.length = length
        self.type = typ

    def __str__(self):
        return "%s [%d +%d] (%s)" % (self.content, self.start, self.length, self.type)


class Tokenizer:
    
    def __init__(self):
        pass
    
    def lex(self, content):
        print('---')
        for s in content:
            if s == '\n':
                s = 'NL'
            elif s == '\r':
                s = 'CR'
            print('[' + s + ']')
        print('---')
        keyword = ('if', 'else', 'for')
        separators = (' ', '(', ')', ':', '.', ';', ',', '\n')
        discard = (' ',)
        replace = {'\n' : 'NEWLINE'}
        word = ''
        start = 0
        tokens = []
        for i in range(0, len(content)):
            char = content[i]
            if char in separators:
                if len(word)>0:
                    if word in keyword:
                        tokens.append(Token(word, start, len(word), Token.KEYWORD))
                    else:
                        tokens.append(Token(word, start, len(word), Token.TEXT))
                    word = ''
                start = i+1 # bug was here
                if char not in discard and char not in replace:
                    tokens.append(Token(char, i, 1, Token.SEPARATOR))
                if char in replace:
                    tokens.append(Token(replace[char], i, 1, Token.SEPARATOR))
            else:
                word += char
        if len(word)>0:
            if word in keyword:
                tokens.append(Token(word, start, len(word), Token.KEYWORD))
            else:
                tokens.append(Token(word, start, len(word), Token.TEXT))
        return tokens


class MyFrame(tkinter.Frame):
    """ Extend a Frame, a global container"""
    
    def __init__(self, app):
        tkinter.Frame.__init__(self, app.root)
        self.pack(fill=tkinter.BOTH, expand=tkinter.YES) # make it visible
        self.app = app
        self.build()
        self._escape_refresh = 0
        
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
        treeview = ttk.Treeview(self)
        treeview["columns"] = ("text",)
        treeview.column("#0", width=120)
        treeview.heading("#0", text="Nodes")
        treeview.column("text", width=80)
        treeview.heading("text", text="Tag")
        treeview.insert("", 0, text="First entry")
        if self.app.rc.found('Crystal_Clear_device_blockdevice16'):
            treeview.insert("", 1, text=" Second entry", image=self.app.rc.getAsImage(Crystal_Clear_device_blockdevice16))
        else:
            treeview.insert("", 1, text=" Second entry")
        if self.app.rc.found('IconYellowCube16x19'):
            sub1 = treeview.insert("", 2, text=" Third entry", image=self.app.rc.getAsImage('IconYellowCube16x19'))
        else:
            sub1 = treeview.insert("", 2, text=" Third entry")
        if self.app.rc.found('IconBlueCube16x19'):
            treeview.insert(sub1, 0, text=" 2-1 Entry", image=self.app.rc.getAsImage('IconBlueCube16x19'))
        else:
            treeview.insert(sub1, 0, text=" 2-1 Entry")
        if self.app.rc.found('IconMagentaCube16x19'):
            treeview.insert(sub1, 1, text=" 2-2 Entry", image=self.app.rc.getAsImage('IconMagentaCube16x19'))
        else:
            treeview.insert(sub1, 1, text=" 2-2 Entry")
        # or
        treeview.insert("", 3, "sub2", text="Fourth entry")
        if self.app.rc.found('IconYellowCube16x19'):
            treeview.insert("sub2", 0, text=" 3-1 Entry", image=self.app.rc.getAsImage('IconYellowCube16x19'))
        else:
            treeview.insert("sub2", 0, text=" 3-1 Entry")
        treeview.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.YES)
        
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
        content = self.text.get(1.0, tkinter.END)
        tokens = Tokenizer().lex(content)
        # Clear all tags
        for tag in self.text.tag_names():
            self.text.tag_remove(tag, 1.0)
        # Put tags
        for t in tokens:
            if t.type == Token.KEYWORD:
                print(t)
                deb = '1.0+%ic' % t.start
                print(deb)
                end = '1.0+%ic' % (t.start + t.length)
                print(end)
                self.text.tag_add("keyword", deb, end)
    
    # There is a bug when doing Ctrl+A : the refresh (call to key function) "let" the first character outside the selected area!
    # To prevent this, we do this
    def escape_refresh(self, nb):
        self._escape_refresh = nb
    
    def key(self, event):
        #print("pressed", repr(event.char))
        #print(dir(event))
        print('>>>', self._escape_refresh)
        if self._escape_refresh > 0:
            self._escape_refresh -= 1
            return
        self.tokenizer()
        s = self.text.get(1.0, tkinter.END)
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
                self.text.tag_add("keyword", deb, end)
                w = ''
                start = i
                print(w, len(w))

    def update_text(self, event):
        self.key(event)
        self.app.update_status_bar(event)
        
    def make_text(self: tkinter.Frame): # with grid: ok :-)
        self.text_frame = tkinter.Frame(self, bd=2, relief=tkinter.SUNKEN)

        self.text_frame.grid_rowconfigure(0, weight=1)
        self.text_frame.grid_columnconfigure(0, weight=1)

        #self.xscrollbar = tkinter.Scrollbar(self.text_frame, orient=tkinter.HORIZONTAL)
        #self.xscrollbar.grid(row=1, column=0, sticky=tkinter.E+tkinter.W)

        self.yscrollbar = tkinter.Scrollbar(self.text_frame)
        self.yscrollbar.grid(row=0, column=1, sticky=tkinter.N+tkinter.S)

        self.text = tkinter.Text(self.text_frame, wrap=tkinter.NONE, bd=0,
                    #xscrollcommand=self.xscrollbar.set,
                    yscrollcommand=self.yscrollbar.set)
        self.text.config(font=("consolas", 12), undo=True, wrap='word')
        
        self.text.grid(row=0, column=0, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)

        #self.xscrollbar.config(command=self.text.xview)
        self.yscrollbar.config(command=self.text.yview)

        self.text_frame.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=tkinter.YES)

        # Tags        
        pol_cn_bold = font.Font(family='Courier New', size=10, weight='bold')
        tag_keyword = self.text.tag_config("keyword", foreground="blue", font=pol_cn_bold)
        
        # Tabs
        def tab(arg):
            print("tab pressed")
            self.text.insert(tkinter.INSERT, " " * 4)
            return 'break' # Prevent normal behavior 
    
        # Key bindings
        self.text.bind("<Tab>", tab)
        self.text.bind("<KeyRelease>", self.update_text)
        self.text.bind("<ButtonRelease-1>", self.app.update_status_bar)
        
    def build(self):
        if self.app.options['display_tree']:
            self.make_tree()
        self.make_text()


if __name__ == "__main__":
    Application().run()

