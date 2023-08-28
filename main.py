import argparse
from tkinter import *

from config.config import *
from classes.ObjectDetector import ObjectDetector
from classes.LicenseReader import LicenseReader
from classes.UI import UI
from classes.Tracker import Tracker


def detect_license(frame):
    global APP, license_detector
    license_results = license_detector.detect(frame)
    licenses = []

    if len(license_results) > 0 and APP is not None:
        for license in license_results:
            text = license_reader.read(license)
            licenses.append(text)
            APP.set_licenselabel(license, text)
        APP.insert_licenses(licenses)


if __name__ == "__main__":
    # Car License Model
    license_detector = ObjectDetector(
        model_path=MODEL_PATH, labels=["license"], conf=0.85)
    license_reader = LicenseReader()
    traker=Tracker()

    cap = None

    # Tkinter
    window = Tk()

    # APP
    APP = UI(parent=window, cap=cap, detector=detect_license)

    window.mainloop()

"""
    parser = argparse.ArgumentParser(description="Car Plates Registration")
    parser.add_argument("--image", type=str,
                        help="insert an image to recongnize")
    parser.add_argument("--video", type=str,
                        help="insert a video to recognize")
    parser.add_argument("--cam", type=int, help="insert webcam id")
    args = parser.parse_args()
"""
