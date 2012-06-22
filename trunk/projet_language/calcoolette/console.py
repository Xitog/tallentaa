# http://www.pygtk.org/pygtk2tutorial/index.html

import pygtk
pygtk.require('2.0')
import gtk

class Console:
    
    def write(self, text, style=None):
        self.nblines += 1
        #print '%s at %i'  % (text, self.nblines)
        print text        
        buf = self.output.get_buffer()
        ti = buf.get_end_iter()
        buf.insert(ti, text + "\n")
        iter_fin = buf.get_end_iter()
        self.output.scroll_to_iter(iter_fin, 0.1)
        
        if style is not None:
            iter_deb = iter_fin.copy()
            iter_deb.backward_cursor_positions(len(text) + 1)
            #print "{{{ %s }}}" % (iter_deb.get_text(iter_fin),)
            buf.apply_tag_by_name(style, iter_deb, iter_fin)
        
        mk = self.output.get_buffer().get_mark("insert"); # 15h40. PUTAIN ENFIN !!! http://www.gtkforums.com/viewtopic.php?t=1307
        self.output.scroll_to_mark(mk, 0.1)
        
    def on_click_exec(self, widget, data=None):
        text = self.input.get_text()
        self.input.set_text('')
        self.write(text, "bg_green")        
        ### Point of contact
        r = self.todo(self, text)
    
    def on_key_release_event(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        #print "Key %s (%d) was pressed" % (keyname, event.keyval)
        if event.keyval == 65293:
            self.on_click_exec(None)
    
    def delete_event(self, widget, event, data=None):
        # if return False, windows is destroyed on "delete" event
        print "delete event occurred"
        return False

    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        gtk.main_quit()

    def __init__(self, todo):
        self.todo = todo
        self.nblines = 0
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_default_size(500, 300)
        self.window.set_title("Console")
        
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.connect("key_release_event", self.on_key_release_event)

        self.window.set_border_width(10)

        #self.button.connect_object("clicked", gtk.Widget.destroy, self.window)
        
        self.input = gtk.Entry(40)
        self.input.set_text("hello")
        self.input.select_region(0, len("hello"))
        
        self.output = gtk.TextView()
        self.output.set_editable(False)
        self.output.set_cursor_visible(False)
        
        self.view = gtk.ScrolledWindow()
        self.view.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.view.add(self.output)
        self.view.show()

        self.output.get_buffer().create_tag("bg_green", background="green", foreground="white")
        self.output.get_buffer().create_tag("fg_blue", foreground="blue")
        self.output.get_buffer().create_tag("fg_red", foreground="red")
        
        # homogeneous, spacing
        vbox = gtk.VBox(False, 5)
        self.window.add(vbox)
        vbox.pack_start(self.view, True, True, 0)        
        vbox.pack_start(self.input, False, False, 0)        
        ##
        hbox = gtk.HBox(False, 5)
        ####
        button = gtk.Button("Exec")
        button.connect("clicked", self.on_click_exec, None)
        hbox.pack_start(button, True, True, 0)
        button.show()
        ####
        button = gtk.Button("Tokens")
        button.connect("clicked", self.on_click_exec, None)
        hbox.pack_start(button, True, True, 0)
        button.show()
        #####       
        button = gtk.Button("Tree")
        button.connect("clicked", self.on_click_exec, None)
        hbox.pack_start(button, True, True, 0)
        button.show()
        #####        
        button = gtk.Button("Draw")
        button.connect("clicked", self.on_click_exec, None)
        hbox.pack_start(button, True, True, 0)
        button.show()
        ####
        hbox.show()
        ##
        vbox.pack_start(hbox, False, False, 0)    
        # child, expand, fill, padding
                
        self.output.show()
        self.input.show()
        vbox.show()
        self.window.show()
        
        self.input.grab_focus()
        
    def main(self):
        # loop
        gtk.main()

