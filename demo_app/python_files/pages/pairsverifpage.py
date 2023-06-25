import numpy as np
import cv2
import os
import random
from utils import detect_face
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtGui import QPixmap,QRegExpValidator,QImage, QMovie

class PairsVerificationClass(QtWidgets.QMainWindow):
    def __init__(self,main_app):
        super().__init__()
        self.main_app = main_app