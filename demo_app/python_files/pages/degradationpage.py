import numpy as np
import cv2
import os
import random
from ..utils import detect_face
from ..functions.degradation_funcs import generate_noise, generate_blur,generate_lowresolution,generate_compression_artifact
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtGui import QPixmap,QRegExpValidator,QImage, QMovie
from python_files.loading import LoadingScreen
from PyQt5.QtCore import QThread, pyqtSignal


class ImageLabel(QtWidgets.QLabel):
    def __init__(self,text,main_app):
        super().__init__()
        self.main_app = main_app
        self.setAcceptDrops(True)
        self.imagePath = ""

        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setText(f'\n\n {text} \n\n')
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa;
                color:white;
                font: 14pt "Georgia";
            }
        ''')
        self.setFixedSize(20,20)
    def setPixmap(self, image):
        super().setPixmap(image)

    def dragEnterEvent(self, event):
        print("drag in degradation page")
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(QtCore.Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.set_image(file_path)

            event.accept()
        else:
            event.ignore()

    def set_image(self, file_path, change_path=True):
        desired_width = 350
        desired_height = 350

        if change_path:
            self.imagePath = file_path
            print(file_path)
        image = QImage(file_path)
        pixmap = QPixmap.fromImage(image).scaled(desired_width, desired_height, QtCore.Qt.KeepAspectRatio)
        self.setPixmap(pixmap)



class DegradationThread(QThread):
    finished = pyqtSignal(object)

    def __init__(self, input_path, params):
        super().__init__()
        print('inputpath in thread',input_path)

        self.input_path = input_path
        self.detector = params

    def run(self):
        inputimage = detect_face(self.input_path, self.detector)
        cv2.imwrite(r"images\degradation_results\input_detected.jpg", inputimage)
        outputimage = detect_face(r"images\degradation_results\degraded.jpg", self.detector)
        cv2.imwrite(r"images\degradation_results\output_detected.jpg", outputimage)
        result='Done'
        self.finished.emit(result)

class DegPage(QtWidgets.QMainWindow):
    def __init__(self,main_app):
        super().__init__()
        self.main_app = main_app
        self.main_app.ui.apply_deg_btn.clicked.connect(self.apply_deg)
        self.main_app.ui.select_random_deg_btn.clicked.connect(self.random_deg_image)




# functions to add a random image to image viewer input
    def random_deg_image(self):
        directory = r"data\images\LFW"
        imagePath=os.path.join(directory,self.random_image(directory))
        print(imagePath)
        self.main_app.photoViewerInput.set_image(imagePath)
        if self.main_app.ui.noisecheckBox.isChecked() or self.main_app.ui.blurcheckbox.isChecked() or self.main_app.ui.lrcheckbox.isChecked() or self.main_app.ui.compressioncheckbox.isChecked():
            self.enableApplyFunc()


    def random_image(self,directory):
        allImages=[]
        print('here')
        for img in os.listdir(directory):
            allImages.append(img)
        return allImages[random.randint(0, len(allImages) - 1)]


# function to apply degradation
    def apply_deg(self):
        self.detection=False
        # get image path from imageviewer input
        input_path=self.main_app.photoViewerInput.imagePath
        inputimage=cv2.imread(input_path)
        degraded_image = inputimage
        print (f"input image{input_path}")

        #handle noise degradation
        if self.main_app.ui.noisecheckBox.isChecked():
            mean = float(self.main_app.ui.meannoise.text())
            std = float(self.main_app.ui.stdnoise.text())
            degraded_image = generate_noise(degraded_image, mean, std)
        #handle blur degradation
        if self.main_app.ui.blurcheckbox.isChecked():
            kernel = int(self.main_app.ui.blurvalue.text())
            if kernel%2 == 0:
                kernel=kernel+1
                self.main_app.ui.blurvalue.setText(str(kernel))
            degraded_image = generate_blur(degraded_image, kernel)
        #handle compression degradation
        if self.main_app.ui.compressioncheckbox.isChecked():
            quality=int(self.main_app.ui.compressionvalue.text().rstrip('%'))
            if quality>100:
                quality=100
                self.main_app.ui.lowresvalue.setText(str(quality))
            print(f" degraded image shape {degraded_image.shape}")
            degraded_image= generate_compression_artifact(degraded_image,quality)
            print(f" degraded image shape {degraded_image.shape}")
        # handle lr degradation
        if self.main_app.ui.lrcheckbox.isChecked():
            percentage=int(self.main_app.ui.lowresvalue.text().rstrip('%'))
            if percentage>100:
                percentage=100
                self.main_app.ui.lowresvalue.setText(str(percentage))
            degraded_image= generate_lowresolution(degraded_image,percentage)

        cv2.imwrite(r"images\degradation_results\degraded.jpg", degraded_image)


        if self.main_app.ui.detectcheckBox.isChecked():
            detector = self.main_app.ui.detectcomboBox.currentText()
            self.degradation_thread = DegradationThread(input_path,detector)
            self.degradation_thread.finished.connect(self.handle_degradation_finished)

            # Start the thread
            self.loading_screen = LoadingScreen()
            self.loading_screen.startLoading()
            self.degradation_thread.start()
        if self.detection == False:
            self.main_app.photoViewerOutput.set_image(r"images\degradation_results\degraded.jpg", True)

    def handle_degradation_finished(self, degraded_image):
        # set detected input image
        self.main_app.photoViewerInput.set_image(r"images\degradation_results\input_detected.jpg", False)
        # set detected output img
        self.main_app.photoViewerOutput.set_image(r"images\degradation_results\output_detected.jpg", True)
        self.detection = True
        self.loading_screen.stopLoading()

        if self.detection == False:
            self.main_app.photoViewerOutput.set_image(r"images\degradation_results\degraded.jpg", True)
            self.loading_screen.stopLoading()

    ############################################################################
    # function to initialize settings checkboxes and edit texts
    def initCheckBoxes(self):
        # allow only floats for noise blur and low resolution text edits
        rx = QtCore.QRegExp("[0-9]*\.?[0-9]+")
        validator = QRegExpValidator(rx, self.main_app)

        self.main_app.ui.meannoise.setValidator(validator)
        self.main_app.ui.meannoise.setText("0.0")

        self.main_app.ui.stdnoise.setValidator(validator)
        self.main_app.ui.stdnoise.setText("0.0")

        rx2 = QtCore.QRegExp("[0-9]*")
        validator2 = QRegExpValidator(rx2, self.main_app)

        self.main_app.ui.blurvalue.setValidator(validator2)
        self.main_app.ui.blurvalue.setText("1")

        self.main_app.ui.lowresvalue.setValidator(validator2)
        self.main_app.ui.lowresvalue.setInputMask("000%")
        self.main_app.ui.lowresvalue.setText("100%")

        self.main_app.ui.compressionvalue.setValidator(validator2)
        self.main_app.ui.compressionvalue.setInputMask("000%")
        self.main_app.ui.compressionvalue.setText("100%")

        # handle check events in checkboxes
        self.main_app.ui.noisecheckBox.clicked.connect(lambda: self.handleCheckBox(self.main_app.ui.noisecheckBox))
        self.main_app.ui.blurcheckbox.clicked.connect(lambda: self.handleCheckBox(self.main_app.ui.blurcheckbox))
        self.main_app.ui.lrcheckbox.clicked.connect(lambda: self.handleCheckBox(self.main_app.ui.lrcheckbox))
        self.main_app.ui.compressioncheckbox.clicked.connect(lambda: self.handleCheckBox(self.main_app.ui.compressioncheckbox))
        self.main_app.ui.detectcheckBox.clicked.connect(lambda: self.handleCheckBox(self.main_app.ui.detectcheckBox))
    #################################################################
    # function to initialize image viewers
    def initImageViewers(self):
        self.main_app.setAcceptDrops(True)
        self.main_app.photoViewerInput = ImageLabel("Drop your face image here",self.main_app)
        self.main_app.photoViewerOutput = ImageLabel("Click apply!\nThe result will appear here",self.main_app)
        self.main_app.photoViewerInput.setFixedSize(400,400)
        self.main_app.photoViewerOutput.setFixedSize(400, 400)
        self.main_app.ui.imagesspace.addWidget(self.main_app.photoViewerInput)
        self.main_app.ui.imagesspace.addWidget(self.main_app.photoViewerOutput)
    ###################################################################################
    # function to handle enabling and disabling edit lines for corresponding checkboxes
    # and enable apply button if image exists in image viewer input
    def handleCheckBox(self,checkbox):
        # handle noise checkbox
        if checkbox==self.main_app.ui.noisecheckBox:
            if self.main_app.ui.noisecheckBox.isChecked():
                self.main_app.ui.meannoise.setEnabled(True)
                self.main_app.ui.stdnoise.setEnabled(True)
                if self.main_app.photoViewerInput.pixmap() is not None:
                    self.enableApplyFunc()
            else:
                self.main_app.ui.meannoise.setEnabled(False)
                self.main_app.ui.stdnoise.setEnabled(False)
                if self.main_app.ui.lrcheckbox.isChecked()==False and self.main_app.ui.blurcheckbox.isChecked()==False and self.main_app.ui.compressioncheckbox.isChecked()==False:
                    self.disableApplyFunc()

        # handle blur checkbox
        elif checkbox==self.main_app.ui.blurcheckbox:
            if self.main_app.ui.blurcheckbox.isChecked():
                self.main_app.ui.blurvalue.setEnabled(True)
                if self.main_app.photoViewerInput.pixmap() is not None:
                    self.enableApplyFunc()
            else:
                self.main_app.ui.blurvalue.setEnabled(False)
                if self.main_app.ui.lrcheckbox.isChecked()==False and self.main_app.ui.noisecheckBox.isChecked()==False and self.main_app.ui.compressioncheckbox.isChecked()==False:
                    self.disableApplyFunc()

        # handle low resolution checkbox
        elif checkbox==self.main_app.ui.lrcheckbox:
            if self.main_app.ui.lrcheckbox.isChecked():
                self.main_app.ui.lowresvalue.setEnabled(True)
                if self.main_app.photoViewerInput.pixmap() is not None:
                    self.enableApplyFunc()
            else:
                self.main_app.ui.lowresvalue.setEnabled(False)
                if self.main_app.ui.noisecheckBox.isChecked()==False and self.main_app.ui.blurcheckbox.isChecked()==False and self.main_app.ui.compressioncheckbox.isChecked()==False:
                    self.disableApplyFunc()
        elif checkbox==self.main_app.ui.compressioncheckbox:
            if self.main_app.ui.compressioncheckbox.isChecked():
                self.main_app.ui.compressionvalue.setEnabled(True)
                if self.main_app.photoViewerInput.pixmap() is not None:
                    self.enableApplyFunc()
            else:
                self.main_app.ui.compressionvalue.setEnabled(False)
                if self.main_app.ui.noisecheckBox.isChecked()==False and self.main_app.ui.blurcheckbox.isChecked()==False and self.main_app.ui.lrcheckbox.isChecked()==False:
                    self.disableApplyFunc()
        elif checkbox==self.main_app.ui.detectcheckBox:
            if self.main_app.ui.detectcheckBox.isChecked():
                self.main_app.ui.detectcomboBox.setEnabled(True)
            else:
                self.main_app.ui.detectcomboBox.setEnabled(False)



    ##############################################################################
    # functions to enable or disable apply button and change its style
    def enableApplyFunc(self):
        self.main_app.ui.apply_deg_btn.setEnabled(True)
        self.main_app.ui.apply_deg_btn.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 rgba(90, 255, 231, 255), stop:1 rgba(21, 205, 202, 255));border-radius: 10px;color:rgb(255, 255, 255);\n"
            "font: 75 10pt \"Georgia\";")
    def disableApplyFunc(self):
        self.main_app.ui.apply_deg_btn.setEnabled(False)
        self.main_app.ui.apply_deg_btn.setStyleSheet(
            "background-color: rgb(170, 170, 170);border-radius: 10px;color:rgb(255, 255, 255);\n"
            "font: 75 10pt \"Georgia\";")