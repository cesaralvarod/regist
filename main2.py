from tkinter import *
from tkinter import filedialog, messagebox
import cv2 as cv
from PIL import ImageTk, Image
import imutils

from config.config import MODEL_PATH

# tkinter
window = Tk()
mode="webcam"
video_speed=10
el_video=None
el_listbox=None
el_lbllicense=None
el_lbltext=None

# opencv
cap=None
cam_num=1


def create_UI(title="SMRV",  w=960, h=620):
    global window, cap, mode, el_video, el_listbox, el_lbllicense,cam_num

    window.title(title)
    window.geometry(f"{w}x{h}")
    window.resizable(0, 0)

    # Create frames in window
    main_frame = Frame(window)
    main_frame.grid()

    frame0 = Frame(main_frame, padx=10, pady=10)
    frame0.grid(column=0, row=0)

    frame1 = Frame(main_frame, padx=10, pady=10)
    frame1.grid(column=0, row=1)

    frame2 = Frame(main_frame)
    frame2.grid(column=1, row=1)

    # Menu bar
    el_menubar = Menu(window)
    window.config(menu=el_menubar)

    el_filemenu = Menu(el_menubar, tearoff=0)
    el_filemenu.add_command(label="Open Image")
    el_filemenu.add_command(label="Open Video")
    el_filemenu.add_separator()
    el_filemenu.add_command(label="Open Camara")

    el_helpmenu = Menu(el_menubar, tearoff=0)
    el_helpmenu.add_command(label="Help")

    el_menubar.add_cascade(label="File", menu=el_filemenu)
    el_menubar.add_cascade(label="Help", menu=el_helpmenu)

    # Labels

    el_lbl0 = Label(frame0, text=title, font=("Arial", 18), pady=5)
    el_lbl0.grid(column=0, row=0, columnspan=2, sticky=EW)

    el_lbl1 = Label(frame1, text="Car license found")
    el_lbl1.grid(column=0, row=0)

    el_lbl2 = Label(frame1, text="Last car license detected:", pady=10)
    el_lbl2.grid(column=0, row=2)

    el_lbltext=Label(frame1, text="", pady=10, font=("Arial", 15, "bold"))
    el_lbltext.grid(column=0, row=3)

    el_lbllicense = Label(frame1, text="", pady=10, font=("Arial", 15, "bold"))
    el_lbllicense.grid(column=0, row=4)

    el_video = Label(frame2, text="", width=640, height=480)
    el_video.grid(column=0, row=0)

    # Listbox

    el_listbox = Listbox(frame1, width=35, height=20)

    el_scrollbar = Scrollbar(frame1, orient=VERTICAL)
    el_listbox.config(yscrollcommand=el_scrollbar.set)
    el_scrollbar.config(command=el_listbox.yview)

    el_listbox.grid(column=0, row=1)
    el_scrollbar.grid(column=1, row=1, sticky=N+S)

    # init webcam
    if mode=="webcam":
        init_webcam()

def init_webcam():
    global cap,cam_num

    if cap is None:
        cap=cv.VideoCapture(cam_num)

        if cap.isOpened() is False and cam_num>=0:
            cap=None
            cam_num = cam_num-1
            init_webcam()
        else:
            capture_webcam()


def capture_webcam():
    global mode, cap, video_speed, el_video

    if cap is not None and mode!="image":
        ret,cv_frame=cap.read()

        if ret is True:
            cv_frame=imutils.resize(cv_frame, width=640)
            cv_frame=cv.cvtColor(cv_frame,cv.COLOR_BGR2RGB)

            im=Image.fromarray(cv_frame)
            img=ImageTk.PhotoImage(image=im)

            if el_video is not None:
                el_video.configure(image=img)
                el_video.image=img

                el_video.after(video_speed, capture_webcam)


def open_image():
    global el_listbox

    filetypes=[("image", ".jpg"), ("image", ".jpeg"), ("image", ".png")]
    path_image=filedialog.askopenfilename(filetypes)

    if len(path_image)>0:
        el_listbox.delete(0,END)

def set_lbllicense(image, text=""):
    global el_lbllicense, el_lbltext

    if image is None:
        el_lbllicense.configure(image="")
        el_lbllicense.image=""
        el_lbltext["text"] = ""
        return

    image=imutils.resize(image, width=200)
    image=cv.cvtColor(image, cv.COLOR_BGR2RGB)

    im=Image.fromarray(image)
    img=ImageTk.PhotoImage(image=im)

    el_lbllicense.configure(image=img)
    el_lbllicense.image=img

    el_lbltext["text"] =text


def insert_licenses(items=[]):
    pass

if __name__ == "__main__":
    create_UI()
    window.mainloop()
