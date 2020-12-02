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
        # Put tags
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
