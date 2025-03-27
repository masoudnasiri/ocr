import os
import csv
from datetime import datetime, timedelta
from collections import defaultdict

class DetectionLogger:
    def __init__(self, log_dir="output/logs"):
        self.log_dir = log_dir
        self.log_file = os.path.join(log_dir, "detections.csv")
        self.last_invalid_save = defaultdict(lambda: datetime.min)
        self.valid_count = defaultdict(int)
        self.invalid_count = defaultdict(int)
        self.initialize_log()

    def initialize_log(self):
        os.makedirs(self.log_dir, exist_ok=True)
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['date', 'time', 'label', 'value', 'valid', 'image_paths'])

    def can_save_invalid(self, label):
        now = datetime.now()
        if (now - self.last_invalid_save[label]) > timedelta(minutes=1):
            if self.invalid_count[label] >= 3:
                self.invalid_count[label] = 0
            self.last_invalid_save[label] = now
            self.invalid_count[label] += 1
            return True
        return False

    def can_save_valid(self, label):
        if self.valid_count[label] < 3:
            self.valid_count[label] += 1
            return True
        return False

    def log_detection(self, timestamp, label, value, is_valid, image_paths):
        # Convert timestamp to date and time
        dt = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
        date = dt.strftime("%Y-%m-%d")
        time = dt.strftime("%H:%M:%S")
        
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                date,
                time,
                label,
                value,
                'valid' if is_valid else 'invalid',
                '|'.join(image_paths)
            ])
