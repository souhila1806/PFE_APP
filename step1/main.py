from cdta_ui import Ui_MainWindow
from degradationpage import DegPage
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtGui import QPixmap,QRegExpValidator
from PyQt5.uic import loadUi
'''
class ImageLabel(QtWidgets.QLabel):
    def __init__(self,text):
        super().__init__()

        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setText(f'\n\n {text} \n\n')
        self.setStyleSheet("
            QLabel{
                border: 4px dashed #aaa;
                color:white;
                font: 14pt "Georgia";
            }")
        self.resize(50,50)
    def setPixmap(self, image):
        super().setPixmap(image)
        '''

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(1400, 900)

        deg= DegPage(self)
        # PAGES
        self.initStackedWidget()
        #settings
        deg.initCheckBoxes()
        # Image viewers
        deg.initImageViewers()



    #############################################################################
    ############################## Functions#####################################
    #############################################################################

    # function to initialise stacked widget
    def initStackedWidget(self):
        # Degradation Page
        self.ui.degradation_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.degradationpage))

        # Pairs Restoration Page
        self.ui.pairs_rest_btn.clicked.connect(self.pairs_restoration_fun)

        # folds restoration Page
        self.ui.folds_rest_btn.clicked.connect(self.folds_restoration_fun)

        # Pairs verification Page
        self.ui.pairs_verif_btn.clicked.connect(self.pairs_verif_fun)

        # Pairs verification Page
        self.ui.folds_verif_btn.clicked.connect(self.folds_verif_fun)



 #############################################################################
    # functions to handle the stacked widget pages
    def pairs_restoration_fun(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.pairrestorationpage)
        self.ui.pairs_rest_btn.setStyleSheet("color: white;font-size:8pt; font-weight:bold;font-family: Georama;border:none; height: 30px}\n"
"QPushButton:hover{background-color:rgb(28, 142, 178);")
        self.ui.folds_rest_btn.setStyleSheet("color: grey;font-size:8pt; font-weight:bold;font-family: Georama;border:none; height: 30px}\n"
"QPushButton:hover{background-color:rgb(28, 142, 178);")

    def folds_restoration_fun(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.foldsrestorationpage)
        self.ui.pairs_rest_btn.setStyleSheet("color: grey;font-size:8pt; font-weight:bold;font-family: Georama;border:none; height: 30px}\n"
"QPushButton:hover{background-color:rgb(28, 142, 178);")
        self.ui.folds_rest_btn.setStyleSheet("color: white;font-size:8pt; font-weight:bold;font-family: Georama;border:none; height: 30px}\n"
"QPushButton:hover{background-color:rgb(28, 142, 178);")

    def pairs_verif_fun(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.pairsverifpage)
        self.ui.pairs_verif_btn.setStyleSheet(
            "color: white;font-size:8pt; font-weight:bold;font-family: Georama;border:none; height: 30px}\n"
            "QPushButton:hover{background-color:rgb(28, 142, 178);")
        self.ui.folds_verif_btn.setStyleSheet(
            "color: grey;font-size:8pt; font-weight:bold;font-family: Georama;border:none; height: 30px}\n"
            "QPushButton:hover{background-color:rgb(28, 142, 178);")

    def folds_verif_fun(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.foldsverifpage)
        self.ui.pairs_verif_btn.setStyleSheet(
            "color: grey;font-size:8pt; font-weight:bold;font-family: Georama;border:none; height: 30px}\n"
            "QPushButton:hover{background-color:rgb(28, 142, 178);")
        self.ui.folds_verif_btn.setStyleSheet(
            "color: white;font-size:8pt; font-weight:bold;font-family: Georama;border:none; height: 30px}\n"
            "QPushButton:hover{background-color:rgb(28, 142, 178);")


    # main function
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    app.exec_()
