# le 21 dec, 15h09. Gtk c'est vraiment trop simple !

import pygtk
pygtk.require('2.0')
import gtk

# Windows

def on_quit(widget, event, data=None):
    print "quit event"
    return False

def quit(b):
     gtk.main_quit()

win = gtk.Window(gtk.WINDOW_TOPLEVEL)
win.connect("delete_event", on_quit)
win.connect("destroy", quit)

# Button

def hello(b):
    print "Hello, World!"
    b.set_label("Hi There")

button = gtk.Button("Hello World")
button.connect('clicked', hello)

# Assembly

win.add(button)
win.show_all()

gtk.main()

