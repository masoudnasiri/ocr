import os
import cv2
from datetime import datetime

class TrainingManager:
    def __init__(self):
        self.training_dir = os.path.join("output", "train")
        os.makedirs(self.training_dir, exist_ok=True)
        self.valid_samples_dir = os.path.join("output", "valid_samples")
        os.makedirs(self.valid_samples_dir, exist_ok=True)

    def save_invalid_detection(self, roi, label, timestamp=None):
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
        # Ensure ROI is at maximum size for training
        max_size = 800  # You can adjust this value
        h, w = roi.shape[:2]
        if h > w:
            scale = min(max_size / h, max_size / w)
        else:
            scale = min(max_size / w, max_size / h)
            
        if scale < 1:
            roi = cv2.resize(roi, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        elif scale > 1:
            roi = cv2.resize(roi, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

        return {
            'roi': roi,
            'label': label,
            'timestamp': timestamp
        }

    def save_training_sample(self, roi, coords, class_id, confidence):
        """
        Save valid detections for future training
        Args:
            roi: Region of interest (image)
            coords: [x1, y1, x2, y2] coordinates
            class_id: 0 for cn-11, 1 for iso-type
            confidence: Detection confidence
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        class_name = "cn-11" if class_id == 0 else "iso-type"
        
        # Save image
        image_filename = f"{class_name}_{timestamp}_{confidence:.2f}.jpg"
        image_path = os.path.join(self.valid_samples_dir, image_filename)
        cv2.imwrite(image_path, roi, [cv2.IMWRITE_JPEG_QUALITY, 100])
        
        # Save annotation in YOLO format
        # YOLO format: <class> <x_center> <y_center> <width> <height>
        x1, y1, x2, y2 = coords
        img_height, img_width = roi.shape[:2]
        
        x_center = (x1 + x2) / (2 * img_width)
        y_center = (y1 + y2) / (2 * img_height)
        width = (x2 - x1) / img_width
        height = (y2 - y1) / img_height
        
        anno_filename = image_filename.rsplit('.', 1)[0] + '.txt'
        anno_path = os.path.join(self.valid_samples_dir, anno_filename)
        
        with open(anno_path, 'w') as f:
            f.write(f"{class_id} {x_center} {y_center} {width} {height}")

        return image_path

    def retrain_model(self):
        """
        Placeholder for model retraining logic.
        Currently just returns the path to the existing model.
        """
        # In a real implementation, this would:
        # 1. Collect all training samples
        # 2. Update dataset configuration
        # 3. Run training for N epochs
        # 4. Save and return path to new model
        return "models/bestold.pt"  # Return existing model for now
