import cv2 as cv2


class CarLicenseReader:
    def __init__(self):
        self.image = None

    def apply_thresh(self):
        gray = cv.cvtColor(self.image, cv.COLORBGR2GRAY)
        thresh = cv.threshold(gray, 170, 255, cv.THRESH_BINARY_INV)[1]
        return thresh

    def get_contours(self):
        contours = cv.findContours(
            self.image, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)[0]

    def read_license(self, image):
        self.image = image
        self.image = self.apply_thresh()
