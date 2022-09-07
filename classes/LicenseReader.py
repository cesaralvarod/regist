import cv2 as cv
import skimage
#  import pytesseract
import numpy as np
import easyocr

reader = easyocr.Reader(["en"], gpu=False)

# For windows
# pytesseract.pytesseract.tesseract_cmd = ""


class LicenseReader:
    def __init__(self):
        self.image = None

    # ------ Functions----------

    def grayscale(self, frame):
        return cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    def apply_threshold(self, frame):
        return cv.threshold(frame, 128, 255, cv.THRESH_BINARY_INV)[1]

    def threshold(self, img, thresh=130):
        return ((img > thresh)*255).astype("uint8")

    def adaptive_threshold(self, frame):
        return cv.adaptiveThreshold(
            frame, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 7, 13)

    def delete_borders(self, frame):
        return skimage.segmentation.clear_border(frame)

    def find_contours(self, frame):
        return cv.findContours(
            frame, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)[0]

    def read(self, image):
        # image is a frame of OpenCV
        self.image = image
        height, width, _ = self.image.shape

        license = ""

        #  psm = 11
        #  alphanumeric = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        #  options = "-c tessedit_char_whitelist={}".format(alphanumeric)
        #  options += " --psm {}".format(psm)

        if height >= 10 and width >= 10:
            """ gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)

            mask = cv.threshold(gray, 130, 255, cv.THRESH_BINARY_INV)[1]
            mask = cv.medianBlur(mask, 7)

            blue = np.matrix(self.image[:, :, 0])
            green = np.matrix(self.image[:, :, 1])
            red = np.matrix(self.image[:, :, 2])

            threshold = 130

            for col in range(0, height):
                for row in range(0, width):
                    maximo = max(
                        red[col, row], green[col, row], blue[col, row])

                    if 255 - maximo > threshold:
                        self.image[col, row] = 0
                    else:
                        self.image[col, row] = 255

            #  text = pytesseract.image_to_string(
            #  self.image, config=options)

            """

            text_readed = reader.readtext(self.image, paragraph=True)
            regex = " \\()*&^%$#@!~`\'\"[]{}<>/.,;-_=+"

            for line in text_readed:
                license = line[1]
                license = license.upper()
                license = ''.join(
                    x for x in license if x not in regex)

                if len(license) > 4:
                    license = license[:6]
                    break

        return license
