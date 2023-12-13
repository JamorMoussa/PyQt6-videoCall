import sys
import threading
from vidstream import CameraClient
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, QTimer

class VideoStreamClient:
    def __init__(self, server_ip, server_port):
        self.client = CameraClient(server_ip, server_port, show_video_window=False)
        self.thread = threading.Thread(target=self.start_stream, daemon=True)
        self.thread.start()

    def start_stream(self):
        self.client.start_stream()

    def get_frame(self):
        return self.client.get_frame()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.video_stream_client = VideoStreamClient('your_server_ip', 9999)  # Replace with your server IP

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.start_button = QPushButton('Start Stream', self)
        self.start_button.clicked.connect(self.start_stream)

        self.stop_button = QPushButton('Stop Stream', self)
        self.stop_button.clicked.connect(self.stop_stream)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.stop_button)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_image)
        self.timer.start(50)  # Adjust the interval as needed

    def start_stream(self):
        # Start the video stream when the "Start Stream" button is clicked
        pass

    def stop_stream(self):
        # Stop the video stream when the "Stop Stream" button is clicked
        pass

    def update_image(self):
        frame = self.video_stream_client.get_frame()
        if frame:
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100, 100, 800, 600)
    window.setWindowTitle("Camera Chat Application")
    window.show()
    sys.exit(app.exec())
