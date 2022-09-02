import cv2 as cv


class LicenseReader:
    def __init__(self):
        self.image = None

    def grayscale(self, frame):
        return cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    def apply_threshold(self, frame):
        return cv.threshold(frame, 120, 255, cv.THRESH_BINARY_INV)[1]

    def find_contours(self, frame):
        return cv.findContours(
            frame, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)[0]

    def read(self, image):
        self.image = image

        gray = self.grayscale(self.image)
        threshold = self.apply_threshold(gray)
        #  contours = self.find_contours(threshold)

        cv.imshow("Frame", threshold)
