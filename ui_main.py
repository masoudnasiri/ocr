from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget, 
    QPushButton, QLabel, QSplitter, QTextEdit, QScrollArea, QFrame,
    QLineEdit, QListWidget, QFileDialog,QListWidgetItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from video_stream import VideoStream
import json

class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_camera_config()
        self.camera_info = {}
        
        # Create central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.init_ui()
    
    def load_camera_config(self):
        with open('camera_config.json', 'r') as f:
            self.camera_config = json.load(f)
    
    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # Header (keep existing header code)
        header_layout = self.create_header()
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Create main tab
        self.main_tab = self.create_main_tab()
        self.tab_widget.addTab(self.main_tab, "Main")
        
        # Create settings tab
        self.settings_tab = self.create_settings_tab()
        self.tab_widget.addTab(self.settings_tab, "Settings")
        
        # Create batch processing tab
        self.batch_tab = self.create_batch_tab()
        self.tab_widget.addTab(self.batch_tab, "Batch OCR")
        
        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.tab_widget)
        
        self.central_widget.setLayout(main_layout)
        self.setWindowTitle("Container Recognition System")
        self.resize(1200, 800)

    def create_header(self):
        header_layout = QHBoxLayout()
        logo_label = QLabel()
        try:
            logo_pixmap = QPixmap('company_logo.png')
            if not logo_pixmap.isNull():
                logo_label.setPixmap(logo_pixmap.scaled(50, 50, Qt.KeepAspectRatio))
            else:
                logo_label.setText("Logo")  # Fallback text if image fails to load
        except:
            logo_label.setText("Logo")  # Fallback text if file doesn't exist
        
        title_label = QLabel("Container Recognition System")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        return header_layout

    def create_main_tab(self):
        main_tab = QWidget()
        layout = QVBoxLayout()
        
        # Create splitter for main content
        splitter = QSplitter(Qt.Horizontal)
        
        # Left side - Video streams
        self.video_widget = QWidget()
        self.video_layout = QVBoxLayout()
        self.video_widget.setLayout(self.video_layout)
        
        video_scroll = QScrollArea()
        video_scroll.setWidget(self.video_widget)
        video_scroll.setWidgetResizable(True)
        video_scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Right side - Logs
        log_widget = self.create_log_widget()
        
        splitter.addWidget(video_scroll)
        splitter.addWidget(log_widget)
        
        layout.addWidget(splitter)
        main_tab.setLayout(layout)
        
        # Setup cameras
        for camera in self.camera_config['cameras']:
            self.create_camera_ui(camera['name'], camera['rtsp_url'])
            
        return main_tab

    def create_log_widget(self):
        log_widget = QWidget()
        log_layout = QVBoxLayout()
        
        self.detection_log = QTextEdit()
        self.detection_log.setReadOnly(True)
        self.extraction_log = QTextEdit()
        self.extraction_log.setReadOnly(True)
        
        log_layout.addWidget(QLabel("Detection Log"))
        log_layout.addWidget(self.detection_log)
        log_layout.addWidget(QLabel("Extraction Results"))
        log_layout.addWidget(self.extraction_log)
        
        log_widget.setLayout(log_layout)
        return log_widget

    def create_settings_tab(self):
        settings_tab = QWidget()
        layout = QVBoxLayout()
        
        # Camera configuration
        self.camera_name_input = QLineEdit()
        self.camera_name_input.setPlaceholderText("Camera Name")
        
        self.rtsp_url_input = QLineEdit()
        self.rtsp_url_input.setPlaceholderText("RTSP URL")
        
        self.add_camera_button = QPushButton("Add Camera")
        self.add_camera_button.clicked.connect(self.add_camera)
        
        self.camera_list = QListWidget()
        
        # Tesseract settings
        self.psm_list = QListWidget()
        for psm in ["0", "1", "3", "6", "7"]:
            item = QListWidgetItem(psm)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.psm_list.addItem(item)
        
        layout.addWidget(QLabel("Add New Camera"))
        layout.addWidget(self.camera_name_input)
        layout.addWidget(self.rtsp_url_input)
        layout.addWidget(self.add_camera_button)
        layout.addWidget(QLabel("Cameras"))
        layout.addWidget(self.camera_list)
        layout.addWidget(QLabel("Tesseract PSM Modes"))
        layout.addWidget(self.psm_list)
        
        settings_tab.setLayout(layout)
        return settings_tab

    def create_batch_tab(self):
        batch_tab = QWidget()
        layout = QVBoxLayout()
        
        # Folder selection
        folder_layout = QHBoxLayout()
        self.folder_path_label = QLabel("No folder selected")
        select_folder_btn = QPushButton("Select Folder")
        select_folder_btn.clicked.connect(self.select_folder)
        folder_layout.addWidget(self.folder_path_label)
        folder_layout.addWidget(select_folder_btn)
        
        # Preview area
        self.preview_scroll = QScrollArea()
        self.preview_label = QLabel()
        self.preview_label.setMinimumSize(800, 600)
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_scroll.setWidget(self.preview_label)
        
        # Control buttons
        control_layout = QHBoxLayout()
        self.start_batch_btn = QPushButton("Start Processing")
        self.stop_batch_btn = QPushButton("Stop Processing")
        self.progress_label = QLabel("0/0 images processed")
        
        control_layout.addWidget(self.start_batch_btn)
        control_layout.addWidget(self.stop_batch_btn)
        control_layout.addWidget(self.progress_label)
        
        # Results area
        self.batch_results = QTextEdit()
        self.batch_results.setReadOnly(True)
        
        layout.addLayout(folder_layout)
        layout.addWidget(self.preview_scroll)
        layout.addLayout(control_layout)
        layout.addWidget(self.batch_results)
        
        batch_tab.setLayout(layout)
        return batch_tab

    # Add necessary methods for batch processing
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Images Folder")
        if folder:
            self.folder_path_label.setText(folder)
            # ... implement folder processing logic ...

    def add_camera(self):
        name = self.camera_name_input.text()
        rtsp_url = self.rtsp_url_input.text()
        if name and rtsp_url:
            self.camera_list.addItem(f"{name} ({rtsp_url})")
            self.create_camera_ui(name, rtsp_url)
            self.save_config()
            self.camera_name_input.clear()
            self.rtsp_url_input.clear()

    def create_camera_ui(self, name, rtsp_url):
        container = QFrame()
        container.setFrameStyle(QFrame.Panel | QFrame.Raised)
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QVBoxLayout()
        
        # Video display
        video_label = QLabel()
        video_label.setMinimumSize(320, 240)  # Minimum size
        video_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        video_label.setStyleSheet("background-color: black;")
        video_label.setAlignment(Qt.AlignCenter)  # Center the image
        # Remove setScaledContents to handle aspect ratio manually
        
        # Controls
        controls = QHBoxLayout()
        start_btn = QPushButton("Start Stream")
        detect_btn = QPushButton("Start Detection")
        extract_btn = QPushButton("Start Extraction")
        
        controls.addWidget(start_btn)
        controls.addWidget(detect_btn)
        controls.addWidget(extract_btn)
        
        # Name label with fixed height
        name_label = QLabel(name)
        name_label.setFixedHeight(30)
        
        layout.addWidget(name_label)
        layout.addWidget(video_label, 1)  # Add stretch factor
        layout.addLayout(controls)
        container.setLayout(layout)
        
        # Make the container stretch
        container.setMinimumWidth(400)
        
        self.video_layout.addWidget(container)
        
        # Store camera info
        self.camera_info[name] = {
            'frame': video_label,
            'rtsp_url': rtsp_url,
            'stream': None,
            'buttons': {
                'start': start_btn,
                'detect': detect_btn,
                'extract': extract_btn
            }
        }
        
        # Connect buttons
        start_btn.clicked.connect(lambda: self.toggle_stream(name))
        detect_btn.clicked.connect(lambda: self.toggle_detection(name))
        extract_btn.clicked.connect(lambda: self.toggle_extraction(name))

    def toggle_stream(self, name):
        """Toggle camera stream on/off"""
        info = self.camera_info.get(name)
        if not info:
            return

        try:
            if info['stream'] is None:
                # Start stream
                stream = VideoStream(info['rtsp_url'], name)
                info['stream'] = stream
                stream.thread.frame_update.connect(
                    lambda frame, cam_name: self.update_camera_frame(frame, cam_name))
                stream.thread.error_signal.connect(
                    lambda cam_name, error: self.handle_camera_error(cam_name, error))
                info['buttons']['start'].setText("Stop Stream")
                info['buttons']['detect'].setEnabled(True)
                info['buttons']['extract'].setEnabled(True)
            else:
                # Stop stream
                if info['stream'].thread:
                    info['stream'].thread.stop()
                info['stream'] = None
                info['buttons']['start'].setText("Start Stream")
                info['buttons']['detect'].setEnabled(False)
                info['buttons']['extract'].setEnabled(False)
                info['frame'].clear()
                info['frame'].setStyleSheet("background-color: black;")
        except Exception as e:
            self.handle_camera_error(name, f"Stream toggle error: {str(e)}")

    def update_camera_frame(self, frame, camera_name):
        """Update camera frame display with aspect ratio preservation"""
        info = self.camera_info.get(camera_name)
        if info and info['frame']:
            label = info['frame']
            # Get label size
            label_size = label.size()
            # Get image size
            image_size = frame.size()
            
            # Calculate scaling factors
            w_ratio = label_size.width() / image_size.width()
            h_ratio = label_size.height() / image_size.height()
            
            # Use the smaller ratio to fit the image in the label
            scale_factor = min(w_ratio, h_ratio)
            
            # Calculate new size maintaining aspect ratio
            new_width = int(image_size.width() * scale_factor)
            new_height = int(image_size.height() * scale_factor)
            
            # Scale the image
            scaled_pixmap = QPixmap.fromImage(frame).scaled(
                new_width, 
                new_height,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            
            label.setPixmap(scaled_pixmap)

    def handle_camera_error(self, camera_name, error):
        """Handle camera errors"""
        info = self.camera_info.get(camera_name)
        if info:
            self.detection_log.append(f"Camera {camera_name} error: {error}")
            # Reset stream state without calling toggle_stream to avoid recursion
            if info['stream'] and info['stream'].thread:
                try:
                    info['stream'].thread.stop()
                except:
                    pass
            info['stream'] = None
            info['buttons']['start'].setText("Start Stream")
            info['buttons']['detect'].setEnabled(False)
            info['buttons']['extract'].setEnabled(False)
            info['frame'].clear()
            info['frame'].setStyleSheet("background-color: black;")

    def toggle_detection(self, name):
        """Toggle detection processing for camera stream"""
        info = self.camera_info.get(name)
        if not info or not info['stream']:
            return

        try:
            btn = info['buttons']['detect']
            if btn.text() == "Start Detection":
                info['stream'].thread.toggle_detection(True)
                btn.setText("Stop Detection")
                self.detection_log.append(f"Started detection for {name}")
            else:
                info['stream'].thread.toggle_detection(False)
                btn.setText("Start Detection")
                self.detection_log.append(f"Stopped detection for {name}")
        except Exception as e:
            self.detection_log.append(f"Detection toggle error for {name}: {str(e)}")

    def toggle_extraction(self, name):
        """Toggle text extraction for camera stream"""
        info = self.camera_info.get(name)
        if not info or not info['stream']:
            return

        try:
            btn = info['buttons']['extract']
            if btn.text() == "Start Extraction":
                info['stream'].thread.toggle_extraction(True)
                btn.setText("Stop Extraction")
                self.extraction_log.append(f"Started extraction for {name}")
            else:
                info['stream'].thread.toggle_extraction(False)
                btn.setText("Start Extraction")
                self.extraction_log.append(f"Stopped extraction for {name}")
        except Exception as e:
            self.extraction_log.append(f"Extraction toggle error for {name}: {str(e)}")
