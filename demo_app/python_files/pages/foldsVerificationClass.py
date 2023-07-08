import numpy as np
import cv2
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from uis.folder_verif import Ui_foldersVerif
from python_files.utils import *
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtGui import QPixmap,QRegExpValidator,QImage, QMovie
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QVBoxLayout

class FoldsVerificationClass(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_foldersVerif()
        self.ui.setupUi(self)
        self.setObjectName("FoldsVerifForm")
        self.ui.icon.setPixmap(QtGui.QPixmap("images/details.png"))
        self.ui.icon1.setPixmap(QtGui.QPixmap("images/reglages.png"))