import torch
import cv2 as cv
import numpy as np
import os
import sys


class ObjectDetector:

    def __init__(self, model_path="", conf=0.50, labels=[]):
        self.model_path = model_path
        self.conf = conf if conf < 1 and conf >= 0 else 1.0
        self.labels = labels
        self.objects = []
        self.results = None

        self.load_model()

    def load_model(self):
        if not os.path.exists(self.model_path):
            sys.exit("Model not found")

        self.model = torch.hub.load(
            "ultralytics/yolov5", 'custom', self.model_path, force_reload=True)

    def detect(self, frame, draw=True):
        self.frame = frame
        self.results = self.model(self.frame)
        objects = np.array(self.results.xyxy[0])
        self.objects = []

        for obj in objects:
            x1, y1, x2, y2, coincidence, type_obj = obj

            if coincidence >= self.conf and self.model.names[type_obj] in self.labels:
                self.draw_rectangle((int(x1), int(y1)),
                                    (int(x2), int(y2)), thickness=2)
                self.objects.append(obj.tolist())

                # Write text

                # label_text = self.set_labeltext(type_obj)
                # roi = self.frame[int(y1):int(y2), int(x1):int(x2)]
                # cv.rectangle(self.frame, c1,
                #              (int(x1) + len(label_text) * 20 + 10, int(y1)-40), (0, 255, 0), -1)
                # cv.putText(self.frame, label_text, (int(x1)+10, int(y1)-10),
                #            cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv.LINE_AA)

        return self.objects

    def draw_rectangle(self, c1, c2, color=(0, 255, 0), thickness=1):
        cv.rectangle(self.frame, c1, c2, color, thickness)

    def get_labels(self):
        return self.model.names
