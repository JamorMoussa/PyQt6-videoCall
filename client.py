import cv2
import socket
import pickle
import struct
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget

class ImageClient(QMainWindow):
    def __init__(self):
        super().__init__()

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addWidget(self.image_label)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('127.0.0.1', 12345))  # Replace 'SERVER_IP' with the server's IP address

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.receive_and_display)
        self.timer.start(30)  # Update every 30 milliseconds

    def receive_and_display(self):
        data = b""
        payload_size = struct.calcsize('>L')

        while len(data) < payload_size:
            data += self.client_socket.recv(4096)

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack('>L', packed_msg_size)[0]

        while len(data) < msg_size:
            data += self.client_socket.recv(4096)

        img_data = data[:msg_size]
        data = data[msg_size:]

        img_encoded = pickle.loads(img_data)
        img = cv2.imdecode(img_encoded, cv2.IMREAD_COLOR)

        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        self.image_label.setPixmap(pixmap)

    def closeEvent(self, event):
        self.client_socket.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication([])
    client_window = ImageClient()
    client_window.setGeometry(100, 100, 800, 600)
    client_window.setWindowTitle("Image Client")
    client_window.show()
    app.exec()
