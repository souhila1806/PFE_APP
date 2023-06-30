import numpy as np
import cv2
import os
import random
from PyQt5 import QtCore, QtGui, QtWidgets
from demo_app.uis.pairsverif_ui import Ui_PairsVerifForm
from demo_app.python_files.functions.lfw_xqlfw_funcs import verif_pair
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtGui import QPixmap,QRegExpValidator,QImage, QMovie

class PairsVerificationClass(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PairsVerifForm()
        self.ui.setupUi(self)
        self.setObjectName("pairsVerifPage")
        self.ui.apply_pairs_verif_btn.clicked.connect(self.applyVerif)


    def applyVerif(self):
        imgpath1="demo_app/data/images/XQLFW/Nathalie_Baye_0002.jpg"
        imgpath2 = "demo_app/data/images/XQLFW/Nathalie_Baye_0004.jpg"
        acc,threshold=verif_pair("lfw",imgpath1,imgpath2,"adaface")
        self.ui.accuracy.setText(str(acc))
        self.ui.threshold.setText(str(threshold))
        print("holla")