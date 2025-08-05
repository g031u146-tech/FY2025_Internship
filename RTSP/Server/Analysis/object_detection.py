from ultralytics import YOLO
from logging import getLogger


class ObjectDetect():
    
    def __init__(self):
        # モデルの読み込み
        self.model = YOLO("yolov8n.pt")
        
    def detection(self, frame):
        logger = getLogger('ultralytics')
        logger.disabled = True
        results = self.model(frame)
        frame = results[0].plot()

        return frame