from config.config import *
from classes.ObjectDetector import ObjectDetector

import cv2 as cv
import torch
import math
import numpy as np
import argparse
import os
import sys

car_detector = ObjectDetector(model_path="yolov5m.pt", labels=[
    "car", "motorcycle", "bus", "truck"])
license_detector = ObjectDetector(
    model_path="license_model.pt", labels=["license"])


def file_exists(filename):
    return os.path.exists(filename)


def resize_image(image, scale_percent=100):
    if image.shape[1] > 640:
        scale_percent = 50
    elif image.shape[1] > 480:
        scale_percent = 100
    else:
        scale_percent = 200
    dim = (int(image.shape[1]*scale_percent/100),
           int(image.shape[0]*scale_percent/100))
    return cv.resize(image, dsize=dim, interpolation=cv.INTER_AREA)


def view_webcam():
    return


def open_webcam():
    print("webcam")


def open_video(filename):
    if not file_exists(filename):
        sys.exit("Sorry the file we\'re looking for doesn\'t exist")

    video = cv.VideoCapture(filename)

    while video.isOpened():
        ret, frame = video.read()

        if ret == True:
            car_results = car_detector.detect(frame)
            license_results = license_detector.detect(frame)
            cv.imshow("Video", frame)

        k = cv.waitKey(0)

        if k == 27:
            break

    video.release()
    cv.destroyAllWindows()


def open_image(filename):
    if not file_exists(filename):
        sys.exit("Sorry the file we\'re looking for doesn\'t exist")

    global car_detector

    image = cv.imread(cv.samples.findFile(filename))

    if image is None:
        sys.exit("Could not read the image")

    car_results = car_detector.detect(image)
    image = resize_image(image)
    cv.imshow("Image", image)

    k = cv.waitKey(0)
    # if k == "ESC":
    #     return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Car Plates Registration")
    parser.add_argument("--image", type=str,
                        help="insert an image to recongnize")
    parser.add_argument("--video", type=str,
                        help="insert a video to recognize")
    args = parser.parse_args()
    if args.image:
        open_image(args.image)
    elif args.video:
        open_video(args.video)
    else:
        open_webcam()
