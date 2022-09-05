import os
import cv2 as cv


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
