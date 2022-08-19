import torch
import cv2 as cv
import numpy as np

MODEL = "ultralytics/yolov5"
YOLO_VERSION = "yolov5m"


class ObjectDetector:
    def __init__(self, threshold=0.45, labels=[]):
        self.model = torch.hub.load(MODEL, YOLO_VERSION)
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

    def draw_object(self):
        for obj in self.objects:
            x1, y1, x2, y2, coincidence, type_obj = obj
            c1 = int(x1), int(y1)
            c2 = int(x2), int(y2)
            if coincidence >= self.threshold and type_obj in self.labels:
                cv.rectangle(self.frame, c1, c2, (0, 255, 0), 1)
                label_text = self.set_labeltext(type_obj)
                # cv.rectangle(self.frame, c1,
                #              (int(x1) + len(label_text) * 20 + 10, int(y1)-40), (0, 255, 0), -1)
                # cv.putText(self.frame, label_text, (int(x1)+10, int(y1)-10),
                #            cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv.LINE_AA)

    def set_labeltext(self, label):
        if label < len(self.model.names):
            return self.model.names[label]
        else:
            return "unidentified"
