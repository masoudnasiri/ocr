import cv2
from PyQt5.QtCore import QThread, pyqtSignal, QMutex
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QImage, QPixmap

class VideoStream(QWidget):
    def __init__(self, rtsp_url, camera_name):
        super().__init__()
        self.rtsp_url = rtsp_url
        self.camera_name = camera_name
        self.init_ui()
        self.init_stream()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.video_label = QLabel()
        self.layout.addWidget(self.video_label)
        self.setLayout(self.layout)

    def init_stream(self):
        self.thread = StreamThread(self.rtsp_url, self.camera_name)
        self.thread.frame_update.connect(self.update_frame)
        self.thread.error_signal.connect(self.handle_error)
        self.thread.start()

    def update_frame(self, frame, camera_name):
        self.video_label.setPixmap(QPixmap.fromImage(frame))

    def handle_error(self, camera_name, error_message):
        print(f"Error from {camera_name}: {error_message}")

class StreamThread(QThread):
    frame_update = pyqtSignal(QImage, str)
    detection_update = pyqtSignal(QImage, str, str)
    extraction_update = pyqtSignal(str, str)
    error_signal = pyqtSignal(str, str)

    def __init__(self, rtsp_url, camera_name):
        super().__init__()
        self.rtsp_url = rtsp_url
        self.camera_name = camera_name
        self.running = True
        self.mutex = QMutex()
        self.detection_active = False
        self.extraction_active = False
        self.original_frame = None
        self.cap = None

    def run(self):
        try:
            self.cap = cv2.VideoCapture(self.rtsp_url)
            if not self.cap.isOpened():
                self.error_signal.emit(self.camera_name, "Failed to open camera stream")
                return

            while self.running:
                ret, frame = self.cap.read()
                if ret:
                    self.original_frame = frame.copy()
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h, w, ch = rgb_frame.shape
                    qt_frame = QImage(rgb_frame.data, w, h, ch * w, QImage.Format_RGB888)
                    self.frame_update.emit(qt_frame, self.camera_name)
                else:
                    self.error_signal.emit(self.camera_name, "Failed to read frame")
                    break
        except Exception as e:
            self.error_signal.emit(self.camera_name, f"Stream error: {str(e)}")
        finally:
            if self.cap is not None:
                self.cap.release()

    def stop(self):
        self.mutex.lock()
        self.running = False
        self.mutex.unlock()
        if self.cap is not None:
            self.cap.release()
        self.wait()

    def toggle_detection(self, active):
        self.detection_active = active

    def toggle_extraction(self, active):
        self.extraction_active = active
