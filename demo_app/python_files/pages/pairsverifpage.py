import numpy as np
import cv2
import os
import random

import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout

from uis.pairsverif_ui import Ui_PairsVerifForm
from python_files.functions.lfw_xqlfw_funcs import verif_pair
from python_files.functions.fusion_funcs import ff_pair,sf_pair,hf_pair
from python_files.utils import detect_face
from python_files.pages.degradationpage import LoadingScreen
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtGui import QPixmap,QRegExpValidator,QImage, QMovie
from python_files.ruler import RulerWidget

class ImageViewer(QtWidgets.QLabel):
    def __init__(self,text):
        super().__init__()
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
        self.resize(40,40)
    def setPixmap(self, image):
        super().setPixmap(image)

    def set_image(self, file_path, change_path=True):
        desired_width = 350
        desired_height = 350

        if change_path:
            self.imagePath = file_path
            print(file_path)
        image = QImage(file_path)
        pixmap = QPixmap.fromImage(image).scaled(desired_width, desired_height, QtCore.Qt.KeepAspectRatio)
        self.setPixmap(pixmap)

class PairsVerificationClass(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PairsVerifForm()
        self.currentdataset=""
        self.ui.setupUi(self)
        self.setObjectName("pairsVerifPage")
        self.ui.rightmenubar.move(900, 0)
        lay1=self.ui.labelsnames
        lay2=self.ui.imagespace
        lay3 = self.ui.resultspace
        self.ui.workingspace.layout().removeWidget(lay1)
        self.ui.workingspace.layout().removeWidget(lay2)
        self.ui.workingspace.layout().removeWidget(lay3)
        self.ui.workingspace.layout().addWidget(lay2)
        self.ui.workingspace.layout().addWidget(lay1)
        self.ui.workingspace.layout().addWidget(lay3)
        self.ui.apply_pairs_verif_btn.clicked.connect(self.applyVerif)
        self.ui.randomHQ.clicked.connect(self.hqrandom)
        self.ui.randomLQ.clicked.connect(self.lqrandom)
        self.init_checkboxes()
        self.init_images()
        self.ruler = RulerWidget()
        lay1=self.ui.values
        self.ui.resultspace.layout().removeWidget(lay1)
        self.ui.resultspace.layout().addWidget(self.ruler)
        self.ui.resultspace.layout().addWidget(lay1)


    def lqrandom(self):
        self.ui.advancedwidget.setHidden(False)
        self.ui.rest_model_classic.clear()
        self.ui.rest_model_classic.addItem("GFPGAN")
        self.ui.rest_model_classic.addItem("GPEN")
        self.ui.rest_model_classic.addItem("SGPN")
        self.currentdataset = "xqlfw"
        csvfile = r"data\files\XQLFW_pairsVerif.csv"
        directory = r"data\images\XQLFW"
        filename1, filename2 = self.random_images(csvfile)
        imagePath1 = os.path.join(directory, filename1)
        imagePath2 = os.path.join(directory, filename2)
        self.photoViewerOne.set_image(imagePath1)
        self.photoViewerTwo.set_image(imagePath2)
        self.ui.name1.setText(filename1[:-9])
        self.ui.name2.setText(filename2[:-9])
        self.enableApplyFunc()
    def hqrandom(self):
        try:
            self.currentdataset="lfw"
            csvfile=r"data\files\LFW_pairsVerif.csv"
            directory = r"data\images\LFW"
            filename1,filename2=self.random_images(csvfile)
            imagePath1= os.path.join(directory, filename1)
            imagePath2 = os.path.join(directory, filename2)

            self.photoViewerOne.set_image(imagePath1)
            self.photoViewerTwo.set_image(imagePath2)
            self.ui.name1.setText(filename1[:-9])
            self.ui.name2.setText(filename2[:-9])
            self.ui.rest_model_classic.clear()
            self.ui.rest_model_classic.addItem("GFPGAN")
            self.ui.rest_model_classic.addItem("GPEN")
            self.ui.advancedwidget.setHidden(True)


            self.enableApplyFunc()
        except Exception as e:
            import traceback
            traceback.print_exc()


    def random_images(self, csvfile):
        df=pd.read_csv(csvfile)
        print(df.columns)
        randomline=df.iloc[random.randint(0, df.shape[0] - 1)]
        path1=f"{randomline.loc['name1']}_{randomline.loc['image1']:04d}.png"
        print(randomline.loc['recognition'],randomline.loc['restoration'])
        path2 = f"{randomline.loc['name2']}_{randomline.loc['image2']:04d}.png"
        return path1,path2
    def detection(self,rest):
        loading = LoadingScreen()
        loading.startLoading()
        first_path = self.photoViewerOne.imagePath
        second_path = self.photoViewerTwo.imagePath
        if rest != None:
            first_path=os.path.join(f"data\images\{self.currentdataset.upper()}_{rest.upper()}",first_path.split("\\")[-1])
            second_path=os.path.join(f"data\images\{self.currentdataset.upper()}_{rest.upper()}",second_path.split("\\")[-1])
        print(first_path,second_path)
        detector="MTCNN"
        firstimage = detect_face(first_path, detector)
        secondimage = detect_face(second_path, detector)
        cv2.imwrite(r"images\degradation_results\input_detected.jpg",
                    firstimage)
        cv2.imwrite(
            r"images\degradation_results\output_detected.jpg",
            secondimage)

        # set detected input image
        self.photoViewerOne.set_image(
            r"images\degradation_results\input_detected.jpg", False)
        # set detected output img
        self.photoViewerTwo.set_image(
            r"images\degradation_results\output_detected.jpg", False)
        loading.stopLoading()
    def applyVerif(self):
        try:
            acc=0
            threshold=0
            imgpath1=self.photoViewerOne.imagePath
            imgpath2 = self.photoViewerTwo.imagePath
            dataset=self.currentdataset
            model=self.ui.recognitionmodel.currentText()
            print(model)
            rest=None
            if self.ui.advancedcheckbox.isChecked():
                type=self.ui.typefusioncombobox.currentText()
                if type== "feature fusion":
                    restoration=self.ui.featurelevelcombobox.currentText()
                    if restoration=="ALL":
                        restoration_models=["GFPGAN","SGPN","GPEN"]
                    else:
                        restoration_models= restoration.split("_")
                    acc,threshold=ff_pair(imgpath1,imgpath2,restoration_models,model)
                elif type== "score fusion":
                    restoration = self.ui.scorelevelcombobox.currentText()
                    restoration_models = restoration.split("_")
                    acc, threshold = sf_pair(imgpath1, imgpath2, restoration_models, model)
                elif type == "hybrid fusion":
                    restorationl1 = self.ui.featurelevelcombobox.currentText()
                    if restorationl1 == "ALL":
                        restoration_modelsl1 = ["GFPGAN", "SGPN", "GPEN"]
                    else:
                        restoration_modelsl1 = restorationl1.split("_")

                    restorationl2 = self.ui.scorelevelcombobox.currentText()
                    print(restoration_modelsl1,restorationl2)
                    acc, threshold=hf_pair(imgpath1,imgpath2,restoration_modelsl1,restorationl2,model)
            else:
                if self.ui.classic_checkbox.isChecked():
                    rest=self.ui.rest_model_classic.currentText()
                acc,threshold,_,_=verif_pair(dataset,imgpath1,imgpath2,model,rest)

            self.detection(rest)
            self.ui.accuracy.setText(str(round(acc,4)))
            self.ui.threshold.setText(str(round(threshold,4)))
            if acc>threshold:
                self.ui.result.setText("Matched identity")
                self.ui.result.setStyleSheet('''color: rgb(0, 255, 0);
font: 12pt "Georgia";
padding-top:20px
''')
            else:
                self.ui.result.setText("Mismatched identities")
                self.ui.result.setStyleSheet('''color: rgb( 255,0, 0);
                font: 12pt "Georgia";
                padding-top:20px
                ''')
            self.ruler.set_values(acc,threshold)

        except Exception as e:
            import traceback
            traceback.print_exc()


    def init_images(self):
        try:
            self.photoViewerOne = ImageViewer("first image here")
            self.photoViewerTwo = ImageViewer("second image here")
            self.photoViewerOne.setFixedSize(400, 400)
            self.photoViewerTwo.setFixedSize(400, 400)
            self.ui.imagespacelayout.addWidget(self.photoViewerOne)
            self.ui.imagespacelayout.addWidget(self.photoViewerTwo)
        except Exception as e:
            import traceback
            traceback.print_exc()

    def init_checkboxes(self):
        try:
            self.ui.classic_checkbox.clicked.connect(lambda: self.handlecheckbox("classic"))
            self.ui.advancedcheckbox.clicked.connect(lambda: self.handlecheckbox("advanced"))
            self.ui.typefusioncombobox.currentIndexChanged.connect(self.handlecomboboxes)
        except Exception as e:
            import traceback
            traceback.print_exc()

    def handlecheckbox(self,type):
        try:
            if type=="classic":
                if self.ui.classic_checkbox.isChecked():
                    self.ui.rest_model_classic.setEnabled(True)
                    self.ui.advancedcheckbox.setChecked(False)
                    self.ui.featurelevelcombobox.setEnabled(False)
                    self.ui.scorelevelcombobox.setEnabled(False)
                    self.ui.typefusioncombobox.setEnabled(False)
                else:
                    self.ui.rest_model_classic.setEnabled(False)
            else:
                if self.ui.advancedcheckbox.isChecked():
                    self.ui.rest_model_classic.setEnabled(False)
                    self.ui.classic_checkbox.setChecked(False)
                    self.ui.featurelevelcombobox.setEnabled(True)
                    self.ui.typefusioncombobox.setCurrentText("feature fusion")
                    self.ui.scorelevelcombobox.setEnabled(False)
                    self.ui.typefusioncombobox.setEnabled(True)
                else:
                    self.ui.advancedcheckbox.setChecked(False)
                    self.ui.featurelevelcombobox.setEnabled(False)
                    self.ui.scorelevelcombobox.setEnabled(False)
                    self.ui.typefusioncombobox.setEnabled(False)
        except Exception as e:
            import traceback
            traceback.print_exc()

    def handlecomboboxes(self):
        selected_option = self.ui.typefusioncombobox.currentText()

        # Perform actions based on the selected option
        if selected_option == "feature fusion":
            self.ui.featurelevelcombobox.setEnabled(True)
            self.ui.scorelevelcombobox.setEnabled(False)
        elif selected_option == "score fusion":
            self.ui.featurelevelcombobox.setEnabled(False)
            self.ui.scorelevelcombobox.setEnabled(True)
            self.ui.scorelevelcombobox.clear()
            self.ui.scorelevelcombobox.addItem("GPEN_GFPGAN")
            self.ui.scorelevelcombobox.addItem("GPEN_SGPN")
            self.ui.scorelevelcombobox.addItem("SGPN_GFPGAN")
        elif selected_option == "hybrid fusion":
            self.ui.featurelevelcombobox.setEnabled(True)
            self.ui.scorelevelcombobox.setEnabled(True)
            self.ui.scorelevelcombobox.clear()
            self.ui.scorelevelcombobox.addItem("GFPGAN")
            self.ui.scorelevelcombobox.addItem("SGPN")
            self.ui.scorelevelcombobox.addItem("GPEN")
            self.ui.featurelevelcombobox.currentIndexChanged.connect(self.syncComboBoxIndices)
            self.ui.scorelevelcombobox.currentIndexChanged.connect(self.syncComboBoxIndices)
            self.ui.featurelevelcombobox.setCurrentIndex(0)
            self.ui.scorelevelcombobox.setCurrentIndex(0)

    def syncComboBoxIndices(self, index):
        sender = self.sender()  # Get the combo box that triggered the signal

        if sender == self.ui.featurelevelcombobox:
            if index==3 and self.ui.scorelevelcombobox.isEnabled():
                self.ui.scorelevelcombobox.setCurrentIndex(0)
            elif self.ui.scorelevelcombobox.isEnabled():
                self.ui.scorelevelcombobox.setCurrentIndex(index)
        elif sender == self.ui.scorelevelcombobox:
            if self.ui.featurelevelcombobox.isEnabled():
                self.ui.featurelevelcombobox.setCurrentIndex(index)

    def enableApplyFunc(self):
        self.ui.apply_pairs_verif_btn.setEnabled(True)
        self.ui.apply_pairs_verif_btn.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 rgba(90, 255, 231, 255), stop:1 rgba(21, 205, 202, 255));border-radius: 10px;color:rgb(255, 255, 255);\n"
            "font: 75 10pt \"Georgia\";")
    def disableApplyFunc(self):
        self.ui.apply_pairs_verif_btn.setEnabled(False)
        self.ui.apply_pairs_verif_btn.setStyleSheet(
            "background-color: rgb(170, 170, 170);border-radius: 10px;color:rgb(255, 255, 255);\n"
            "font: 75 10pt \"Georgia\";")

