from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import cv2 as cv
import os
import imutils


class UI:
    def __init__(self, parent, cap=None, title="REGIST", width="950", height="600") -> None:
        self.parent = parent
        self.title = title
        self.geometry = f"{width}x{height}"
        self.frame = None
        self.cap = cap
        self.mode = "webcam"
        self.video_speed = 10

        self.init_ui()

    def init_ui(self):
        # Root: self.parent
        self.parent.title(self.title)
        self.parent.geometry(self.geometry)
        self.parent.resizable(0, 0)

        self.create_frames()
        self.create_menu()
        self.create_listbox()
        self.create_labels()

        self.init_webcam()

    def init_webcam(self):
        if self.cap is None:
            print("hola estamos aca")
            if self.mode == "webcam" or self.mode == "video":
                self.video_speed = 10
                self.cap = cv.VideoCapture(0)
                self.capture_webcam()

    # -------- Widgets ---------------

    def create_frames(self):
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

    def create_menu(self):
       # Menu
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        # File Menu
        file_menu = Menu(menubar, tearoff=0)

        file_menu.add_command(label="Open Image", command=self.open_image)
        file_menu.add_command(label="Open Video", command=self.open_video)
        file_menu.add_command(label="Open Webcam", command=self.open_webcam)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.parent.destroy)

        # Help menu
        help_menu = Menu(menubar, tearoff=0)

        help_menu.add_command(label="Help")

        # Add the menus to the menubar
        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Help", menu=help_menu)

    def create_labels(self):
        # Lbl0
        lbl0 = Label(self.frame0, text=self.title,
                     font=("Arial", 18), pady=5)
        lbl0.grid(column=0, row=0, columnspan=2, sticky=EW)

        # Lbl1
        lbl1 = Label(self.frame1, text="Car licenses found")
        lbl1.grid(column=0, row=0)

        # Lbl2
        self.webcamLbl = Label(self.frame2, text="", width=640, height=480)
        self.webcamLbl.grid(column=0, row=0)

        # Lbl2
        lbl2 = Label(self.frame1, text="Last car license:", pady=10)
        lbl2.grid(column=0, row=2)

        # Lbl4
        lbl4 = Label(self.frame1, text="Last license image", pady=20)
        lbl4.grid(column=0, row=3)

    def create_listbox(self):
        # Listbox
        self.listbox = Listbox(self.frame1, width=35, height=20)

        # Scroll
        scrollbar = Scrollbar(self.frame1, orient=VERTICAL)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        self.listbox.grid(column=0, row=1)
        scrollbar.grid(column=1, row=1, sticky=N+S)

        #  for i in range(190):
        #  self.listbox.insert(i, str(i))

    # ----------- Capture webcam ---------------

    def capture_webcam(self):
        if self.cap is not None:
            if self.mode != "image":

                ret, frame = self.cap.read()

                if ret is True:
                    frame = imutils.resize(frame, width=640)
                    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

                    im = Image.fromarray(frame)
                    img = ImageTk.PhotoImage(image=im)

                    self.set_webcamlabel(img, self.capture_webcam)

    # ---------------- Others functions ----------------------

    def open_image(self):
        path_image = filedialog.askopenfilename(
            filetypes=[("image", ".jpg"), ("image", ".jpeg"), ("image", ".png")])

        if len(path_image) > 0:
            self.cap = cv.imread(path_image)

            if self.cap is None:
                self.mode = "webcam"
                return

            self.mode = "image"

            img_show = imutils.resize(self.cap, width=640, height=480)
            img_show = cv.cvtColor(img_show, cv.COLOR_BGR2RGB)

            im = Image.fromarray(img_show)
            img = ImageTk.PhotoImage(image=im)

            self.webcamLbl.configure(image=img)
            self.webcamLbl.image = img

    def open_webcam(self):
        self.mode = "webcam"
        self.cap = cv.VideoCapture(0)
        self.capture_webcam()

    def open_video(self):
        path_video = filedialog.askopenfilename(
            filetypes=[("all video format", ".avi"), ("all video format", ".mp4")])

        if len(path_video) > 0:
            self.cap = cv.VideoCapture(path_video)

            if self.cap is None:
                self.mode = "webcam"
                return

            self.mode = "video"
            self.video_speed = 40
            self.capture_webcam()

    def set_webcamlabel(self, img, fn=None):
        self.webcamLbl.configure(image=img)
        self.webcamLbl.image = img
        if fn is not None:
            self.webcamLbl.after(self.video_speed, fn)
