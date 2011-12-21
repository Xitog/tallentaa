import pygtk
pygtk.require('2.0')
import gtk

# Windows

def on_quit(widget, event, data=None):
    print "quit"
    return False

def on_focus_in(widget, event, data=None):
    print "focus in"

def on_focus_out(widget, event, data=None):
    print "focus out"

def quit(b):
     gtk.main_quit()

def on_key_pressed(widget, event, data=None):
    print event.keyval

win = gtk.Window(gtk.WINDOW_TOPLEVEL)
win.connect("delete_event", on_quit)
win.connect("destroy", quit)
win.connect("focus_in_event", on_focus_in)
win.connect("focus_out_event", on_focus_out)
win.connect("key_press_event", on_key_pressed)

# Button

def hello(b):
    print "Hello, World!"
    b.set_label("Hi There")

button = gtk.Button("Hello World")
button.connect('clicked', hello)

# Text Entry line

entry = gtk.Entry(max=10)
entry.set_text("hllo")
entry.insert_text("e", 1)
print entry.get_text()
entry.set_editable(True)
print entry.select_region(2, 3)

# Text View buffer

textview = gtk.TextView()
textview.set_editable(True)
textview.set_cursor_visible(True)

# Assembly

vbox = gtk.VBox(False, 0)
win.add(vbox)

vbox.add(button)
vbox.add(entry)
vbox.add(textview)

win.show_all()

gtk.main()

