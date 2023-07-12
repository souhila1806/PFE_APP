from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt,QTimer,QSize,QTimer
from PyQt5.QtGui import QPixmap,QRegExpValidator,QImage, QMovie
from PyQt5.QtWidgets import QApplication
import os


class LoadingScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1300, 850)
        # Create a vertical layout and add the QLabel widgets
        layout = QtWidgets.QVBoxLayout(self)

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground,on=True)
        self.setWindowOpacity(0.5)

        self.loading_animation = QtWidgets.QLabel(self)
        self.loading_animation.setAlignment(Qt.AlignCenter)
        self.loading_animation.setFixedSize(1250,200)
        script_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        gif_path = os.path.join(script_directory, "images\loading2.gif")
        print(gif_path)
        self.movie = QMovie(gif_path)
        self.movie.setScaledSize(QSize(100, 100))
        print(self.movie.isValid())
        self.loading_animation.setMovie(self.movie)

        layout.addWidget(self.loading_animation)
        self.setLayout(layout)

    def startLoading(self):
        self.show()
        self.movie.start()
    def stopLoading(self):

        self.movie.stop()
        delay = 1000  # milliseconds
        QTimer.singleShot(delay, self.close)
        #self.close()

if __name__ == "__main__":
    app = QApplication([])

    window = LoadingScreen()
    window.startLoading()
    app.exec_()
