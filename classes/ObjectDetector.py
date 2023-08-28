import torch
import cv2 as cv
import numpy as np
import os
import sys
import math


class ObjectDetector:

    def __init__(self, model_path="", conf=0.50, labels=[]):
        self.model_path = model_path
        self.conf = conf if conf < 1 and conf >= 0 else 1.0
        self.labels = labels
        self.objects = []
        self.obj_parameters=[]
        self.results = None
        self.center_points={}
        self.id_count=1

        self.load_model()

    def load_model(self):
        if not os.path.exists(self.model_path):
            sys.exit("Model not found")

        # Load model
        self.model = torch.hub.load(
            "ultralytics/yolov5", 'custom', self.model_path, force_reload=True)

    def detect(self, frame, draw=True):
        self.frame = frame
        self.results = self.model(self.frame)
        objects = np.array(self.results.xyxy[0])
        self.objects = []

        objects_id=[]

        for obj in objects:
            x1, y1, x2, y2, coincidence, type_obj = obj

            if coincidence >= self.conf and self.model.names[type_obj] in self.labels:
                self.objects.append(
                    self.frame[int(y1):int(y2), int(x1):int(x2)])

                if draw is True:
                    cv.rectangle(self.frame, (int(x1), int(y1)), (int(x2),int(y2)), (0,255,0), 2)
                    coincidence_text=round(coincidence*100,2)
                    cv.putText(self.frame, f"{coincidence_text}%", (int(x1)+10, int(y1)-10), 
                               cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv.LINE_AA)

        return self.objects

    def get_labels(self):
        return self.model.names
