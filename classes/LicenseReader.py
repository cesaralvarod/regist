import cv2 as cv
import skimage
import pytesseract

#  pytesseract.pytesseract.tesseract_cmd = ""


class LicenseReader:
    def __init__(self):
        self.image = None

    def grayscale(self, frame):
        return cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    def apply_threshold(self, frame):
        return cv.threshold(frame, 128, 255, cv.THRESH_BINARY_INV)[1]

    def adaptive_threshold(self, frame):
        return cv.adaptiveThreshold(
            frame, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 7, 13)

    def delete_borders(self, frame):
        return skimage.segmentation.clear_border(frame)

    def find_contours(self, frame):
        return cv.findContours(
            frame, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)[0]

    def read(self, image, psm=11):
        self.image = image

        alphanumeric = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        options = "-c tessedit_char_whitelist={}".format(alphanumeric)
        options += " --psm {}".format(psm)

        gray = self.grayscale(self.image)
        threshold = self.apply_threshold(gray)
        #  threshold = self.adaptive_threshold(gray)
        borderless = self.delete_borders(threshold)
        final = cv.bitwise_not(borderless)
        text = pytesseract.image_to_string(final, config=options)
        print(f"text={text}")
        # contours = self.find_contours(threshold)

        cv.imshow("Frame", self.image)
