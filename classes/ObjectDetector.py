import torch
import cv2 as cv
import numpy as np

MODEL = "ultralytics/yolov5"
YOLO_VERSION = "yolov5m"
MODEL_PATH = "license_model.pt"


class ObjectDetector:
    def __init__(self, threshold=0.45, labels=[]):
        self.model = torch.hub.load(
            "ultralytics/yolov5", 'custom', path="license_model.pt", force_reload=True)
        self.results = None
        self.objects = []
        self.labels = labels
        self.threshold = threshold if threshold < 1 else 1.0

    def detect(self, frame, draw=True):
        self.frame = frame
        self.results = self.model(self.frame)
        self.objects = np.array(self.results.xyxy[0])
        self.draw_object()

    def get_results(self):
        return self.results

    def get_labels(self):
        return self.labels

    def read_text(self, roi):
        gray = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
        thresh = cv.threshold(gray, 170, 255, cv.THRESH_BINARY_INV)[1]
        cv.imshow("thresh", gray)

    def draw_object(self):
        print(self.model.names)
        for obj in self.objects:
            x1, y1, x2, y2, coincidence, type_obj = obj
            c1 = int(x1), int(y1)
            c2 = int(x2), int(y2)
            print(obj)
            # if coincidence >= self.threshold and type_obj in self.labels:
            label_text = self.set_labeltext(type_obj)
            roi = self.frame[int(y1):int(y2), int(x1):int(x2)]
            self.read_text(roi)
            cv.rectangle(self.frame, c1, c2, (0, 255, 0), 1)
            # cv.rectangle(self.frame, c1,
            #              (int(x1) + len(label_text) * 20 + 10, int(y1)-40), (0, 255, 0), -1)
            # cv.putText(self.frame, label_text, (int(x1)+10, int(y1)-10),
            #            cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv.LINE_AA)

    def set_labeltext(self, label):
        if label < len(self.model.names):
            return self.model.names[label]
        else:
            return "unidentified"
