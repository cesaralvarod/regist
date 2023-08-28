from tkinter import *
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import cv2 as cv
import imutils

class UI:
    def __init__(self, parent, cap=None, detector=None, title="SRMV", width="960", height="680"):
        self.parent = parent
        self.title = title
        self.geometry = f"{width}x{height}"
        self.frame = None
        self.cap = cap
        self.mode = "webcam"
        self.video_speed = 5
        self.detector = detector
        self.cam_num=1

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
        # Title
        lbl0 = Label(self.frame0, text=self.title,
                     font=("Arial", 18), pady=5)
        lbl0.grid(column=0, row=0, columnspan=2, sticky=EW)

        # Text
        lbl1 = Label(self.frame1, text="Car licenses found")
        lbl1.grid(column=0, row=0)

        # Text
        lbl2 = Label(self.frame1, text="Last car license detected:", pady=10)
        lbl2.grid(column=0, row=2)

        # Last License label
        self.licenseLbl = Label(
            self.frame1, text="", pady=20)
        self.licenseLbl.grid(column=0, row=3)

        # Lbl5
        self.textLicenseLbl = Label(
            self.frame1, text="", pady=10, font=("Arial", 15, "bold"))
        self.textLicenseLbl.grid(column=0, row=4)

        # webcam
        self.webcamLbl = Label(self.frame2, text="", width=640, height=480)
        self.webcamLbl.grid(column=0, row=0)

    def create_listbox(self):
        # Listbox
        self.listbox = Listbox(self.frame1, width=35, height=20)

        # Scroll
        scrollbar = Scrollbar(self.frame1, orient=VERTICAL)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        self.listbox.grid(column=0, row=1)
        scrollbar.grid(column=1, row=1, sticky=N+S)

    def init_webcam(self):
        if self.cap is None:
            self.video_speed = 10
            self.cap = cv.VideoCapture(self.cam_num)

            if self.cap.isOpened() is False:
                if self.cam_num>=0:
                    self.cap=None
                    self.cam_num= self.cam_num-1
                    self.init_webcam()
                else:
                    self.parent.destroy()
            else:
                self.capture_webcam()
                    

    # ----------- Capture webcam ---------------

    def capture_webcam(self):
        if self.cap is not None and self.mode != "image":
            ret, frame = self.cap.read()

            if ret is True:
                frame = imutils.resize(frame, width=640)
                frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

                # make area of interest
                (x1,y1),(x2,y2)=(20,120), (620,420)
                area_interesed=frame[y1:y2, x1:x2]
                
                self.detector(area_interesed)

                cv.rectangle(frame, (x1,y1), (x2, y2), (255,255,0), 1)

                im = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=im)

                self.set_webcamlabel(img, self.capture_webcam)

    # ---------------- Others functions for menu ----------------------

    def open_image(self):
        path_image = filedialog.askopenfilename(
            filetypes=[("image", ".jpg"), ("image", ".jpeg"), ("image", ".png")])

        if len(path_image) > 0:
            self.listbox.delete(0, END)
            self.set_licenselabel(img=None)

            self.cap = cv.imread(cv.samples.findFile(path_image))

            if self.cap is None:
                self.mode = "webcam"
                return

            self.detector(self.cap)

            self.mode = "image"

            img_show = imutils.resize(self.cap, width=640, height=480)
            img_show = cv.cvtColor(img_show, cv.COLOR_BGR2RGB)

            im = Image.fromarray(img_show)
            img = ImageTk.PhotoImage(image=im)

            self.webcamLbl.configure(image=img)
            self.webcamLbl.image = img

    def open_webcam(self):
        if self.mode != "webcam":
            self.listbox.delete(0, END)
            self.set_licenselabel(img=None)

            self.mode = "webcam"
            self.cap = None
            self.init_webcam()

    def open_video(self):
        path_video = filedialog.askopenfilename(
            filetypes=[("all video format", ".avi"), ("all video format", ".mp4")])

        if len(path_video) > 0:
            self.listbox.delete(0, END)
            self.set_licenselabel(img=None)

            self.cap = cv.VideoCapture(path_video)
            self.mode = "video"

            if self.cap is None:
                self.mode = "webcam"
                return

            self.video_speed = 40
            self.capture_webcam()

    def set_webcamlabel(self, img, fn=None):
        self.webcamLbl.configure(image=img)
        self.webcamLbl.image = img

        if fn is not None:
            self.webcamLbl.after(self.video_speed, fn)

    def set_licenselabel(self, img, text=""):
        if img is None:
            self.licenseLbl.configure(image="")
            self.licenseLbl.image = ""
            self.textLicenseLbl["text"] = ""
            return

        img_show = imutils.resize(img, width=200)
        img_show = cv.cvtColor(img_show, cv.COLOR_BGR2RGB)

        im = Image.fromarray(img_show)
        img = ImageTk.PhotoImage(image=im)

        self.licenseLbl.configure(image=img)
        self.licenseLbl.image = img

        self.textLicenseLbl["text"] = text

    def insert_licenses(self, items=[]):
        # self.listbox.delete(0, END)

        for index, item in enumerate(items, start=0):
            if item != "":
                self.listbox.insert(index, f"{index+1}. {item}")
