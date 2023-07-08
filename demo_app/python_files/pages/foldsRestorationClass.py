import numpy as np
import cv2
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from uis.folder_res import Ui_foldersRestoration
from python_files.utils import *
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtGui import QPixmap,QRegExpValidator,QImage, QMovie
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QVBoxLayout

class FoldsRestorationClass(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_foldersRestoration()
        self.ui.setupUi(self)
        self.setObjectName("FoldsResForm")
        self.ui.icon1.setPixmap(QtGui.QPixmap("images/details.png"))
        self.selected_tab=''
        self.fold=''
        self.disableApplyFunc()
        self.ui.tabsPages.currentChanged.connect(self.tab_changed)
        self.ui.fold.activated.connect(self.combo_box_clicked)
        self.ui.ApplyFBT.clicked.connect(lambda: self.calculate_metrics(self.selected_tab, self.fold))

    def tab_changed(self, index):
        current_tab = self.ui.tabsPages.currentWidget()
        self.selected_tab = self.ui.tabsPages.tabText(index)
        self.ui.mean_gfpgan.setStyleSheet("color: white;")
        self.ui.mean_gpen.setStyleSheet("color: white;")
        self.ui.mean_sgpn.setStyleSheet("color: white;")
        self.ui.mean_xqlfw.setStyleSheet("color: white;")

    def combo_box_clicked(self,index):
        self.fold= self.ui.fold.currentText()
        self.enableApplyFunc()
        self.ui.mean_gfpgan.setStyleSheet("color: white;")
        self.ui.mean_gpen.setStyleSheet("color: white;")
        self.ui.mean_sgpn.setStyleSheet("color: white;")
        self.ui.mean_xqlfw.setStyleSheet("color: white;")

    def calculate_metrics(self, tab, fold):
        print("Selected tab:", tab)
        print('Fold:', fold)
        if tab == 'SSIM':
            plot = self.ui.ssim_plot
            title='SSIM boxplot diagram'
        elif tab == 'PSNR':
            plot = self.ui.psnr_plot
            title = 'PSNR boxplot diagram'
        elif tab == 'LPIPS':
            plot = self.ui.lpips_plot
            title = 'LPIPS boxplot diagram'
        else:
            print('else')

        df = get_data(fold, tab)
        means,index1,index2=calculate_column_means(df, tab)
        self.ui.mean_xqlfw.setText(str(round(means[3],3)))
        self.ui.mean_gfpgan.setText(str(round(means[0],3)))
        self.ui.mean_sgpn.setText(str(round(means[2],3)))
        self.ui.mean_gpen.setText(str(round(means[1],3)))
        if index1 ==0:
            self.ui.mean_gfpgan.setStyleSheet("color: green;")
        elif index1 == 1:
            self.ui.mean_gpen.setStyleSheet("color: green;")
        elif index1 ==2:
            self.ui.mean_sgpn.setStyleSheet("color: green;")
        elif index1==3:
            self.ui.mean_xqlfw.setStyleSheet("color: green;")
        else:
            print('no ')
        if index2 ==0:
            self.ui.mean_gfpgan.setStyleSheet("color: red;")
        elif index2 == 1:
            self.ui.mean_gpen.setStyleSheet("color: red;")
        elif index2 ==2:
            self.ui.mean_sgpn.setStyleSheet("color: red;")
        elif index2==3:
            self.ui.mean_xqlfw.setStyleSheet("color: red;")
        else:
            print('no ')
        fig_width = plot.size().width() / 80
        fig_height = plot.size().height() / 80
        fig = Figure(figsize=(fig_width, fig_height), facecolor='#E7EBF4')
        ax = fig.add_subplot(111)

        # Define the colors for each box plot
        box_colors = ['skyblue', 'lightgreen', 'mediumpurple', 'mediumaquamarine']

        # Plot the box plots with custom colors
        bp = ax.boxplot(df.values, patch_artist=True)
        ax.set_facecolor('#E7EBF4')

        # Set the face color for each box
        for patch, color in zip(bp['boxes'], box_colors):
            patch.set_facecolor(color)

        # Set the x-axis tick labels
        ax.set_xticklabels(['GFP-GAN', 'GPEN', 'SGPN','XQLFW'])

        # Set the y-axis label
        ax.set_ylabel('Values')

        # Set the plot title
        ax.set_title(title)
        # Create the canvas to display the plot
        canvas = FigureCanvas(fig)

        # Set a QVBoxLayout for the plot frame
        layout = QVBoxLayout(plot)
        layout.addWidget(canvas)

    def enableApplyFunc(self):
        self.ui.ApplyFBT.setEnabled(True)
        self.ui.ApplyFBT.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 rgba(90, 255, 231, 255), stop:1 rgba(21, 205, 202, 255));border-radius: 10px;color:rgb(255, 255, 255);\n"
            "font: 75 10pt \"Georgia\";")
    def disableApplyFunc(self):
        self.ui.ApplyFBT.setEnabled(False)
        self.ui.ApplyFBT.setStyleSheet(
            "background-color: rgb(170, 170, 170);border-radius: 10px;color:rgb(255, 255, 255);\n"
            "font: 75 10pt \"Georgia\";")

