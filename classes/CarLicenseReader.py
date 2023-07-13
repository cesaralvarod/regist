import cv2 as cv2


class CarLicenseReader:
    def __init__(self):
        self.image = None

    def apply_thresh(self):
        gray = cv2.cvtColor(self.image, cv2.COLORBGR2GRAY)
        thresh = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY_INV)[1]
        return thresh

    def get_contours(self):
        contours = cv2.findContours(
            self.image, cv2.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)[0]

    def read_license(self, image):
        self.image = image
        self.image = self.apply_thresh()
