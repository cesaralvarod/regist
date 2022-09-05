import cv2 as cv
import argparse
import sys
from tkinter import *
import imutils
from PIL import Image, ImageTk

# Custom classes and functions
from config.config import *
from classes.ObjectDetector import ObjectDetector
from classes.LicenseReader import LicenseReader
from classes.UI import UI
from helpers.helpers import *

# Objects
#  car_detector = ObjectDetector(model_path="yolov5m.pt", labels=[
#  "car", "motorcycle", "bus", "truck"])
#  license_detector = ObjectDetector(
#  model_path="license_model.pt", labels=["license"])
#  license_reader = LicenseReader()


#  def detect_license(frame):
#  global car_detector, license_detector
#  #  car_results = car_detector.detect(frame)
#  license_results = license_detector.detect(frame)
#  for license in license_results:
#  license_reader.read(license)


#  def open_webcam():
#  cap = cv.VideoCapture(0)

#  while True:
#  ret, frame = cap.read()

#  detect_license(frame)

#  cv.imshow("Regist", frame)

#  if cv.waitKey(1) == 27:
#  break

#  cap.release()
#  cv.destroyAllWindows()


#  def open_video(filename):
#  if not file_exists(filename):
#  sys.exit("Sorry the file we\'re looking for doesn\'t exist")

#  cap = cv.VideoCapture(filename)

#  while video.isOpened():
#  ret, frame = cap.read()

#  detect_license(frame)
#  cv.imshow("Regist", frame)

#  k = cv.waitKey(1)

#  if k == 27:
#  break

#  cap.release()
#  cv.destroyAllWindows()


#  def open_image(filename):
#  if not file_exists(filename):
#  sys.exit("Sorry the file we\'re looking for doesn\'t exist")

#  frame = cv.imread(cv.samples.findFile(filename))

#  if frame is None:
#  sys.exit("Could not read the image")

#  image = resize_image(frame)

#  detect_license(image)

#  #  cv.imshow("Regist", frame)

#  k = cv.waitKey(0)


#  def view_webcam():
    #  global cap
    #  if cap is not None:
        #  ret, frame = cap.read()

        #  if ret == True:
            #  frame = imutils.resize(frame, width=640)
            #  frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

            #  im = Image.fromarray(frame)
            #  img = ImageTk.PhotoImage(image=im)

            #  APP.set_webcamlabel(img, view_webcam)


#  def init_webcam(cam):
    #  global cap
    #  cap = cv.VideoCapture(cam)
    #  view_webcam()


if __name__ == "__main__":
    cap = None

    # Tkinter
    window = Tk()

    # Arguments
    parser = argparse.ArgumentParser(description="Car Plates Registration")
    parser.add_argument("--image", type=str,
                        help="insert an image to recongnize")
    parser.add_argument("--video", type=str,
                        help="insert a video to recognize")
    parser.add_argument("--cam", type=int, help="insert webcam id")
    args = parser.parse_args()

    # Args conditional

    if args.image:
        pass
    elif args.video:
        pass
    else:
        # Working!
        APP = UI(parent=window, cap=cap)
        #  init_webcam(0)

    window.mainloop()
