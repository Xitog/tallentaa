# http://www.pygtk.org/pygtk2tutorial/index.html                        reference
# http://stackoverflow.com/questions/8441136/pygtk-textview-problems    insert in TextView
# http://www.pygtk.org/docs/pygtk/class-gtkwidget.html                  grab_focus
# http://faq.pygtk.org/index.py?file=faq05.005.htp&req=edit             key_press_event et key_release_event
# 11h30 : console MARCHE. J'ajoute du texte via l'input et en clickant sur le bouton... Trop puissant ! GTK c'est archi simple et trop puissant.
# Comme quand j'avais fait l'arbre aussi. Cela avait tout d'un jeu d'enfants.
# 12h23 : YEAH!! Les styles marchent.

import pygtk
pygtk.require('2.0')
import gtk

class TutorialGTK:
    
    def hello(self, widget, data=None):
        text = self.input.get_text()
        print "Hello World! %s" % (text,)
        ti = self.output.get_buffer().get_end_iter()
        self.output.get_buffer().insert(ti, text + "\n")
        self.output.scroll_to_iter(ti, 0.1)
        self.input.set_text('')
        
        buf = self.output.get_buffer()
        iter_fin = buf.get_end_iter()
        iter_deb = iter_fin.copy()
        iter_deb.backward_cursor_positions(len(text) + 1)
        
        print iter_deb.get_text(iter_fin)
        buf.apply_tag_by_name("bg_green", iter_deb, iter_fin)
        
    def on_key_release_event(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        print "Key %s (%d) was pressed" % (keyname, event.keyval)
        if event.keyval == 65293:
            self.hello(None)
    
    def delete_event(self, widget, event, data=None):
        # if return False, windows is destroyed on "delete" event
        print "delete event occurred"
        return False

    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        gtk.main_quit()

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_default_size(500, 300)
        self.window.set_title("Console")
        
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.connect("key_release_event", self.on_key_release_event)

        self.window.set_border_width(10)
        self.button = gtk.Button("Hello World")

        self.button.connect("clicked", self.hello, None)
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
        
        # homogeneous, spacing
        vbox = gtk.VBox(False, 5)
        self.window.add(vbox)
        #vbox.pack_start(self.output, True, True, 0)
        vbox.pack_start(self.view, True, True, 0)
        vbox.pack_start(self.input, False, False, 0)
        vbox.pack_start(self.button, False, False, 0)
        # child, expand, fill, padding

        #self.window.add(self.button)
        
        self.output.show()
        self.input.show()
        self.button.show()
        vbox.show()
        self.window.show()
        
        self.input.grab_focus()
        
    def main(self):
        # loop
        gtk.main()

if __name__ == "__main__":
    basic = TutorialGTK()
    basic.main()

