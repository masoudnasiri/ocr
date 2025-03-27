import os
import cv2
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel

class BatchProcessor(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        self.select_btn = QPushButton('Select Files')
        self.select_btn.clicked.connect(self.select_files)
        
        self.status_label = QLabel('No files selected')
        
        layout.addWidget(self.select_btn)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files", "", "Image Files (*.png *.jpg *.jpeg)")
        if files:
            self.status_label.setText(f'Selected {len(files)} files')

    def process_folder(self, folder_path):
        results = []
        for file in os.listdir(folder_path):
            if file.endswith(('.jpg', '.png')):
                image = cv2.imread(os.path.join(folder_path, file))
                results.append(image)
        return results
