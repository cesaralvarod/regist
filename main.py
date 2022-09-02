import cv2 as cv
import argparse
import sys

from config.config import *
from classes.ObjectDetector import ObjectDetector
from classes.LicenseReader import LicenseReader
from helpers.helpers import *


car_detector = ObjectDetector(model_path="yolov5m.pt", labels=[
    "car", "motorcycle", "bus", "truck"])
license_detector = ObjectDetector(
    model_path="license_model.pt", labels=["license"])
license_reader = LicenseReader()


def detect_license(frame):
    global car_detector, license_detector
    #  car_results = car_detector.detect(frame)
    license_results = license_detector.detect(frame)
    #  license_reader.read(frame)
    for license in license_results:
        license_reader.read(license)


def open_webcam():
    cap = cv.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        detect_license(frame)

        cv.imshow("Regist", frame)

        if cv.waitKey(1) == 27:
            break

    cap.release()
    cv.destroyAllWindows()


def open_video(filename):
    if not file_exists(filename):
        sys.exit("Sorry the file we\'re looking for doesn\'t exist")

    cap = cv.VideoCapture(filename)

    while video.isOpened():
        ret, frame = cap.read()

        detect_license(frame)
        cv.imshow("Regist", frame)

        k = cv.waitKey(1)

        if k == 27:
            break

    cap.release()
    cv.destroyAllWindows()


def open_image(filename):
    if not file_exists(filename):
        sys.exit("Sorry the file we\'re looking for doesn\'t exist")

    frame = cv.imread(cv.samples.findFile(filename))

    if frame is None:
        sys.exit("Could not read the image")

    image = resize_image(frame)

    detect_license(image)

    #  cv.imshow("Regist", frame)

    k = cv.waitKey(0)
    #  if k == 27:
    #  return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Car Plates Registration")
    parser.add_argument("--image", type=str,
                        help="insert an image to recongnize")
    parser.add_argument("--video", type=str,
                        help="insert a video to recognize")
    parser.add_argument("--cam", type=int, help="insert webcam id")
    args = parser.parse_args()

    if args.image:
        open_image(args.image)
    elif args.video:
        open_video(args.video)
    else:
        open_webcam()
