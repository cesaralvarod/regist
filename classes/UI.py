from tkinter import *


class UI:
    def __init__(self, parent, title="REGIST", width="950", height="600") -> None:
        self.parent = parent
        self.title = title
        self.geometry = f"{width}x{height}"
        self.frame = None
        self.init_ui()

    def init_ui(self) -> None:
        # Root: self.parent
        self.parent.title(self.title)
        self.parent.geometry(self.geometry)
        self.parent.resizable(0, 0)

        self.create_frames()
        self.create_menu()
        self.create_labels()
        self.create_listbox()

    def create_frames(self) -> None:
        # Main Frame
        self.frame = Frame(self.parent)
        self.frame.grid()

        # Frame0
        self.frame0 = Frame(self.frame, padx=10, pady=10)
        self.frame0.grid(column=0, row=0)

        # Frame1
        self.frame1 = Frame(self.frame, padx=10, pady=10)
        self.frame1.grid(column=0, row=1)

        # Frame2
        self.frame2 = Frame(self.frame)
        self.frame2.grid(column=1, row=1)

    def create_menu(self) -> None:
       # Menu
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        # File Menu
        file_menu = Menu(menubar, tearoff=0)

        file_menu.add_command(label="Open Image")
        file_menu.add_command(label="Open Video")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.parent.destroy)

        # Help menu
        help_menu = Menu(menubar, tearoff=0)

        help_menu.add_command(label="Help")

        # Add the File menu to the menubar
        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Help", menu=help_menu)

    def create_labels(self) -> None:
        # Lbl0
        lbl0 = Label(self.frame0, text=self.title,
                     font=("Arial", 18), pady=5)
        lbl0.grid(column=0, row=0, columnspan=2, sticky=EW)

        # Lbl1
        lbl1 = Label(self.frame1, text="Car licenses found")
        lbl1.grid(column=0, row=0)

        # Lbl2
        self.webcamLbl = Label(
            self.frame2, text="", width=640, height=480)
        self.webcamLbl.grid(column=0, row=0)

        # Lbl2
        lbl2 = Label(self.frame1, text="Last car license:", pady=10)
        lbl2.grid(column=0, row=2)

        # Lbl4
        lbl4 = Label(self.frame1, text="Last license image", pady=20)
        lbl4.grid(column=0, row=3)

    def create_listbox(self) -> None:
        # Listbox
        self.listbox = Listbox(self.frame1, width=35, height=20)

        # Scroll
        scrollbar = Scrollbar(self.frame1, orient=VERTICAL)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        self.listbox.grid(column=0, row=1)
        scrollbar.grid(column=1, row=1, sticky=N+S)
        for i in range(190):
            self.listbox.insert(i, str(i))

    def set_webcamlabel(self, img, fn) -> None:
        self.webcamLbl.configure(image=img)
        self.webcamLbl.image = img
        self.webcamLbl.after(10, fn)
