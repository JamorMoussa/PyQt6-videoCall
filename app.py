from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
import cv2


class VideoCall(QMainWindow):
    def __init__(self):
        super(VideoCall, self).__init__()
        uic.loadUi("./videocall.ui", self)
        self.gui_init()

    
    def gui_init(self):
        self.resize(800, 500)
        self.setWindowTitle("VideoCall App")

        self.camera = cv2.VideoCapture(0)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  

    def update_frame(self):
        ret, frame = self.camera.read()
        if ret:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.cameraLabel.setPixmap(pixmap)

    def closeEvent(self, event):
        self.camera.release()
        event.accept()



if __name__ == "__main__":
    import sys 
    app = QApplication(sys.argv)

    win = VideoCall()
    win.show()

    app.exec()

