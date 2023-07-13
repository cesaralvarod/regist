from config.config import *
from classes.ObjectDetector import ObjectDetector

import cv2 as cv
import argparse
import os
import sys


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


def open_image(filename):
    if not file_exists(filename):
        sys.exit("Sorry the file we\'re looking for doesn\'t exist")
        return

    image = cv.imread(cv.samples.findFile(filename))

    if image is None:
        sys.exit("Could not read the image")

    detector = ObjectDetector(labels=OBJECTS_TO_DETECT)
    detector.detect(image)
    image = resize_image(image)
    cv.imshow("Image", image)

    k = cv.waitKey(0)
    if k == "ESC":
        return


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
