import numpy as np
import cv2
import os
import random
from PyQt5 import QtCore, QtGui, QtWidgets
from uis.restoration_ui import Ui_Form
from python_files.utils import *
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtGui import QPixmap,QRegExpValidator,QImage, QMovie
class ImageDisplayClass:
    def __init__(self, frame):
        self.frame = frame
        self.image_label = None
        self.name_label = None
        self.image_name = ""

    def initialize_label(self,text):
        layout = QtWidgets.QVBoxLayout(self.frame)
        self.image_label = QtWidgets.QLabel()
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        self.image_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.image_label.setStyleSheet(
            '''background-color: gray;"
    "   border-radius: 5px;''')
        #self.image_label.setMaximumSize(self.frame.width(),self.frame.height() * 0.85)
        self.name_label = QtWidgets.QLabel(text)
        self.name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.name_label.setMaximumSize(int(self.frame.width()),int(self.frame.height() * 0.15))
        self.name_label.setStyleSheet(
            "background-color: rgba(0,0,0,0);")
        self.name_label.setAlignment(QtCore.Qt.AlignCenter)

        self.name_label.setFixedWidth(250)
        layout.addWidget(self.image_label)
        layout.addWidget(self.name_label)

    def display_image(self, image_path):
        width=240
        height=320

        # Create a QPixmap from the image file
        pixmap = QtGui.QPixmap(image_path)

        # Scale the image to fit the size of the frame (optional)
        scaled_pixmap = pixmap.scaled(width, height, QtCore.Qt.KeepAspectRatio)
        print(scaled_pixmap.size())
        # Set the pixmap on the image label
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setStyleSheet("background-color: rgba(0,0,0,0);")
        # Show the labels
        self.image_label.show()

    def display_text(self,text):
        # Update the image name label
        self.name_label.setText(text)
        self.name_label.show()
    def set_image_name(self, image_path):
        self.image_name = os.path.basename(image_path)

    def get_image_name(self):
        return self.image_name

class ImageRestorationClass(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setObjectName("ImageResForm")
        self.initImageViewrsFrames()
        self.disableApplyFunc()
        self.enableSelectFunc()
        self.ui.ApplyBT.clicked.connect(self.apply_restoration)
        self.ui.LQBT.clicked.connect(self.random_lq_image)
        self.ui.HQBT.clicked.connect(self.random_hq_image)



    def initImageViewrsFrames(self):
        self.org=ImageDisplayClass(self.ui.orginalImg)
        self.org.initialize_label("Input image")
        self.gfpgan=ImageDisplayClass(self.ui.gfpganImg)
        self.gfpgan.initialize_label("GFP-GAN")
        self.sgpn = ImageDisplayClass(self.ui.sgpnImg)
        self.sgpn.initialize_label("SGPN")
        self.gpen = ImageDisplayClass(self.ui.gpenImg)
        self.gpen.initialize_label("GPEN")
        self.type=""

    def random_lq_image(self):
        directory = r"data\datasets\XQLFW_200"
        imagePath = os.path.join(directory, self.random_image(directory))

        self.org.display_image(imagePath)
        self.org.set_image_name(imagePath)
        self.org.display_text(self.org.image_name[:-9])
        self.type="LQ"
        self.enableApplyFunc()


    def random_hq_image(self):
        print('test test')
        directory = r"data\datasets\LFW_200"
        imagePath = os.path.join(directory, self.random_image(directory))
        print(imagePath)
        self.org.display_image(imagePath)
        self.org.set_image_name(imagePath)
        self.org.display_text(self.org.image_name[:-9])
        self.type = "HQ"
        self.enableApplyFunc()


    def random_image(self, directory):
        allImages = []
        print('here')
        for img in os.listdir(directory):
            allImages.append(img)
        return allImages[random.randint(0, len(allImages) - 1)]


    def apply_restoration(self):
        lpips_model = lpips.LPIPS(net='alex')
        self.gfpgan.display_text('GFPGAN')
        self.gpen.display_text('GPEN')
        self.sgpn.display_text('SGPN')
        image_name=self.org.get_image_name()
        lfw = os.path.join(r"data\datasets\LFW_200", image_name)
        xqlfw = os.path.join(r"data\datasets\XQLFW_200", image_name)
        if self.type=="HQ":

            gfpganPath = os.path.join(r"data\datasets\LFW_200_GFPGAN", image_name)
            gpenPath = os.path.join(r"data\datasets\LFW_200_GPEN", image_name)
            sgpnPath = os.path.join(r"data\datasets\LFW_200_GPEN", image_name)
            lpips1 = '/'
            lpipssg= round(calculate_lpips_lfw(lfw, sgpnPath, lpips_model), 3)
            ssim1='/'
            ssimsg=round(calculate_ssim_crop(lfw, sgpnPath), 3)
            psnr1='/'
            psnrsg=round(calculate_psnr_crop(lfw, sgpnPath), 3)
        else:

            gfpganPath = os.path.join(r"data\datasets\XQLFW_200_GFPGAN", image_name)
            gpenPath = os.path.join(r"data\datasets\XQLFW_200_GPEN", image_name)
            sgpnPath = os.path.join(r"data\datasets\XQLFW_200_SGPN", image_name)
            lpips1= round(calculate_lpips_xqlf(lfw,xqlfw,lpips_model),3)
            lpipssg=round(calculate_lpips_xqlf(lfw,sgpnPath,lpips_model),3)
            ssim1=round(calculate_ssim(lfw,xqlfw),3)
            ssimsg=round(calculate_ssim(lfw,sgpnPath),3)
            psnr1 = round(calculate_psnr(lfw,xqlfw), 3)
            psnrsg = round(calculate_psnr(lfw,sgpnPath), 3)


        lpipsgf = round(calculate_lpips_lfw(lfw, gfpganPath, lpips_model), 3)
        lpipsgp = round(calculate_lpips_lfw(lfw, gpenPath, lpips_model), 3)
        ssimgf=round(calculate_ssim_crop(lfw, gfpganPath),3)
        ssimgp = round(calculate_ssim_crop(lfw, gpenPath), 3)
        psnrgf=round(calculate_psnr_crop(lfw, gfpganPath), 3)
        psnrgp=round(calculate_psnr_crop(lfw, gpenPath), 3)
        self.gfpgan.set_image_name(gfpganPath)
        self.gfpgan.display_image(gfpganPath)
        self.gpen.set_image_name(gpenPath)
        self.gpen.display_image(gpenPath)
        self.sgpn.set_image_name(sgpnPath)
        self.sgpn.display_image(sgpnPath)
        # Display metrics
        # List of lpips values
        lpips_values = [lpips1, lpipsgf, lpipssg, lpipsgp]
        print(lpips_values)
        # List of ssim values
        ssim_values = [ssim1, ssimgf, ssimsg, ssimgp]
        # List of psnr values
        psnr_values = [psnr1, psnrgf, psnrsg, psnrgp]

        # Map of label names to values
        lpips_labels = {
            "lo": lpips1,
            "lgf": lpipsgf,
            "ln": lpipssg,
            "lppn": lpipsgp
        }

        ssim_labels = {
            "sso": ssim1,
            "ssgf": ssimgf,
            "ssn": ssimsg,
            "sspn": ssimgp
        }

        psnr_labels = {
            "po": psnr1,
            "pgf": psnrgf,
            "pn": psnrsg,
            "ppn": psnrgp
        }

        # Set maximum and minimum colors for lpips values
        if lpips_values[0]=='/':
            max_lpips = max(lpips_values[1:])
            min_lpips = min(lpips_values[1:])
        else:
            max_lpips = max(lpips_values)
            min_lpips = min(lpips_values)

        for label_name, value in lpips_labels.items():
            label = getattr(self.ui, label_name)
            label.setText(str(value))
            if value!='/':
                if value == max_lpips:
                    label.setStyleSheet("color: green;")
                elif value == min_lpips:
                    label.setStyleSheet("color: red;")
                else:
                    label.setStyleSheet("color: white;")
                    print(f"norm = {value}")

        # Set maximum and minimum colors for ssim values
        if ssim_values[0] == '/':
            max_ssim = max(ssim_values[1:])
            min_ssim = min(ssim_values[1:])
        else:
            max_ssim = max(ssim_values)
            min_ssim = min(ssim_values)

        for label_name, value in ssim_labels.items():
            label = getattr(self.ui, label_name)
            label.setText(str(value))
            if value != '/':
                if value == max_ssim:
                    label.setStyleSheet("color: green;")
                elif value == min_ssim:
                    label.setStyleSheet("color: red;")
                else:
                    label.setStyleSheet("color: white;")
                    print(f"norm = {value}")

        # Set maximum and minimum colors for psnr values
        if psnr_values[0] == '/':
            max_psnr = max(psnr_values[1:])
            min_psnr = min(psnr_values[1:])
        else:
            max_psnr = max(psnr_values)
            min_psnr = min(psnr_values)

        for label_name, value in psnr_labels.items():
            label = getattr(self.ui, label_name)
            label.setText(str(value))
            if value != '/':
                if value == max_psnr:
                    label.setStyleSheet("color: green;")
                    print(f"max = {value}")
                elif value == min_psnr:
                    label.setStyleSheet("color: red;")
                    print(f"min = {value}")
                else:
                    label.setStyleSheet("color: white;")
                    print(f"norm = {value}")

    # functions to enable or disable apply button and change its style
    def enableApplyFunc(self):
        self.ui.ApplyBT.setEnabled(True)
        self.ui.ApplyBT.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 rgba(90, 255, 231, 255), stop:1 rgba(21, 205, 202, 255));border-radius: 10px;color:rgb(255, 255, 255);\n"
            "font: 75 10pt \"Georgia\";")

    def enableSelectFunc(self):
        print('enableSelect')
        self.ui.HQBT.setEnabled(True)
        self.ui.HQBT.setStyleSheet (
             "background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0.628821 rgba(105, 85, 163, 255), stop:1 rgba(231, 235, 244, 255));"
            "border-radius: 10px;"
            "color: rgb(255, 255, 255);"
            "font: 11pt \"Georgia\";")
        self.ui.LQBT.setEnabled(True)
        self.ui.LQBT.setStyleSheet(
             "background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0.628821 rgba(105, 85, 163, 255), stop:1 rgba(231, 235, 244, 255));"
            "border-radius: 10px;"
            "color: rgb(255, 255, 255);"
            "font: 11pt \"Georgia\";")

    def disableApplyFunc(self):
        print('enableSelect')
        self.ui.ApplyBT.setEnabled(False)
        self.ui.ApplyBT.setStyleSheet(
            "background-color: rgb(170, 170, 170);border-radius: 10px;color:rgb(255, 255, 255);\n"
            "border-radius: 10px;"
            "color: rgb(255, 255, 255);"
            "font: 11pt \"Georgia\";")