
def callback():
    print("called the callback!")

if mode == 'CANVAS':
    try:
        # Only for windows
        root.state("zoomed")
    except Exception as e:
        print(e)

# root.minsize(root.winfo_screenwidth(), root.winfo_screenheight())
# print(root.wm_maxsize())
# toplevel = root.winfo_toplevel()

#------------------------------------------------
# Text
#------------------------------------------------

if mode == 'TEXT':

    options = {}
    
    frame = Frame(root, width=600, height=600)
    frame.pack(fill="both", expand=True)
    # ensure a consistent GUI size
    frame.grid_propagate(False)
    # implement stretchability
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    
    txt = Text(frame, borderwidth=3, relief="sunken")
    #config
    txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
    
#------------------------------------------------
# Canvas
#------------------------------------------------

elif mode == 'CANVAS':
    
    w = Canvas(root, width=200, height=100)
    w.pack()

    w.create_line(0, 0, 200, 100)
    w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))

    w.create_rectangle(50, 25, 150, 75, fill="blue")


