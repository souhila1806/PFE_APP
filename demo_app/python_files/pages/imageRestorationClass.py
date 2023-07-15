import numpy as np
import cv2
import os
import random
from PyQt5 import QtCore, QtGui, QtWidgets
from uis.restoration_ui import Ui_Form
from python_files.utils import *
from PyQt5.QtCore import QThread, pyqtSignal
from ..loading import LoadingScreen


class DegradationThread(QThread):
    finished = pyqtSignal(object)

    def __init__(self,typeImage,lpips_model,image_name,lfw,xqlfw,ui,page):
        super().__init__()
        self.type = typeImage
        self.lpips_model=lpips_model
        self.image_name=image_name
        self.lfw=lfw
        self.xqlfw=xqlfw
        self.ui=ui
        self.page=page

    def run(self):
        if self.type == "HQ":

            gfpganPath = os.path.join(r"data\images\LFW_GFPGAN_IQA", self.image_name)
            gpenPath = os.path.join(r"data\images\LFW_GPEN_IQA", self.image_name)
            sgpnPath = os.path.join(r"data\images\LFW_SGPN_IQA", self.image_name)
            lpips1 = '/'
            lpipssg = round(calculate_lpips_lfw(self.lfw, sgpnPath, self.lpips_model), 3)
            ssim1 = '/'
            ssimsg = round(calculate_ssim_crop(self.lfw, sgpnPath), 3)
            psnr1 = '/'
            psnrsg = round(calculate_psnr_crop(self.lfw, sgpnPath), 3)
        else:

            gfpganPath = os.path.join(r"data\images\XQLFW_GFPGAN", self.image_name)
            gpenPath = os.path.join(r"data\images\XQLFW_GPEN", self.image_name)
            sgpnPath = os.path.join(r"data\images\XQLFW_SGPN", self.image_name)
            lpips1 = round(calculate_lpips_lfw(self.lfw, self.xqlfw, self.lpips_model), 3)
            lpipssg = round(calculate_lpips_xqlf(self.lfw, sgpnPath, self.lpips_model), 3)
            ssim1 = round(calculate_ssim(self.lfw, self.xqlfw), 3)
            ssimsg = round(calculate_ssim(self.lfw, sgpnPath), 3)
            psnr1 = round(calculate_psnr(self.lfw, self.xqlfw), 3)
            psnrsg = round(calculate_psnr(self.lfw, sgpnPath), 3)

        lpipsgf = round(calculate_lpips_lfw(self.lfw, gfpganPath, self.lpips_model), 3)
        lpipsgp = round(calculate_lpips_lfw(self.lfw, gpenPath, self.lpips_model), 3)
        ssimgf = round(calculate_ssim_crop(self.lfw, gfpganPath), 3)
        ssimgp = round(calculate_ssim_crop(self.lfw, gpenPath), 3)
        psnrgf = round(calculate_psnr_crop(self.lfw, gfpganPath), 3)
        psnrgp = round(calculate_psnr_crop(self.lfw, gpenPath), 3)
        self.page.gfpgan.set_image_name(gfpganPath)
        self.page.gfpgan.display_image(gfpganPath)
        self.page.gpen.set_image_name(gpenPath)
        self.page.gpen.display_image(gpenPath)
        self.page.sgpn.set_image_name(sgpnPath)
        self.page.sgpn.display_image(sgpnPath)
        # Display metrics
        # List of lpips values
        lpips_values = [lpips1, lpipsgf, lpipssg, lpipsgp]
        print('lpips',lpips_values)
        # List of ssim values
        ssim_values = [ssim1, ssimgf, ssimsg, ssimgp]
        print('ssim',ssim_values)
        # List of psnr values
        psnr_values = [psnr1, psnrgf, psnrsg, psnrgp]
        print('psnr', psnr_values)
        # Map of label names to values

        result = (lpips_values, ssim_values, psnr_values)
        self.finished.emit(result)

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
        directory = r"data\images\XQLFW"
        imagePath = os.path.join(directory, self.random_image(directory))

        self.org.display_image(imagePath)
        self.org.set_image_name(imagePath)
        self.org.display_text(self.org.image_name[:-9])
        self.type="LQ"
        self.enableApplyFunc()


    def random_hq_image(self):
        print('test test')
        directory = r"data\images\LFW_IQA"
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
        lfw = os.path.join(r"data\images\LFW_IQA", image_name)
        xqlfw = os.path.join(r"data\images\XQLFW", image_name)
        self.degradation_thread = DegradationThread(self.type, lpips_model,image_name,lfw,xqlfw,self.ui,self)
        self.degradation_thread.finished.connect(self.handle_degradation_finished)

        # Start the thread
        self.loading_screen = LoadingScreen()
        self.loading_screen.startLoading()
        self.degradation_thread.start()

    def handle_degradation_finished(self,result):
        lpips_values, ssim_values, psnr_values = result
        lpips_labels = {
            "lo": lpips_values[0],
            "lgf": lpips_values[1],
            "ln": lpips_values[2],
            "lppn": lpips_values[3]
        }

        ssim_labels = {
            "sso": ssim_values[0],
            "ssgf": ssim_values[1],
            "ssn": ssim_values[2],
            "sspn": ssim_values[3]
        }

        psnr_labels = {
            "po": psnr_values[0],
            "pgf": psnr_values[1],
            "pn": psnr_values[2],
            "ppn": psnr_values[3]
        }

        # Set maximum and minimum colors for lpips values
        if lpips_values[0] == '/':
            max_lpips = max(lpips_values[1:])
            min_lpips = min(lpips_values[1:])
        else:
            max_lpips = max(lpips_values)
            min_lpips = min(lpips_values)

        for label_name, value in lpips_labels.items():
            label = getattr(self.ui, label_name)
            label.setText(str(value))
            if value != '/':
                if value == min_lpips:
                    label.setStyleSheet("color: green;")
                elif value == max_lpips:
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
        self.loading_screen.stopLoading()
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