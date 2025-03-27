from ultralytics import YOLO

class DetectionThread:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
    
    def detect(self, frame):
        return self.model(frame)
