import argparse
from tkinter import *

# Custom classes and functions
from config.config import *
from classes.ObjectDetector import ObjectDetector
from classes.LicenseReader import LicenseReader
from classes.UI import UI

#  from helpers.telegram import send_image

def detect_license(frame):
    global APP, license_detector
    #  car_results = car_detector.detect(frame)
    license_results = license_detector.detect(frame)
    licenses = []
    if len(license_results) > 0:
        for license in license_results:
            text = license_reader.read(license)
            licenses.append(text)
            APP.set_licenselabel(license, text)
        APP.insert_licenses(licenses)

    # Main
if __name__ == "__main__":
    # Objects
    #  car_detector = ObjectDetector(model_path="yolov5m.pt", labels=["car", "motorcycle", "bus", "truck"])
    license_detector = ObjectDetector(
        model_path="license_model.pt", labels=["license"], conf=0.85)
    license_reader = LicenseReader()

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

    # APP

    APP = UI(parent=window, cap=cap, detector=detect_license)

    window.mainloop()
