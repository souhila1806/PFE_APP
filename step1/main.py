from cdta_ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtGui import QPixmap,QRegExpValidator
from PyQt5.uic import loadUi

class ImageLabel(QtWidgets.QLabel):
    def __init__(self,text):
        super().__init__()

        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setText(f'\n\n {text} \n\n')
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa;
                color:white;
                font: 14pt "Georgia";
            }
        ''')
        self.resize(50,50)
    def setPixmap(self, image):
        super().setPixmap(image)
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(1400, 900)

        # PAGES
        self.initStackedWidget()
        #settings
        self.initCheckBoxes()
        # Image viewers
        self.initImageViewers()



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


    ############################################################################"
    # function to initialize settings checkboxes and edit texts
    def initCheckBoxes(self):
        # allow only floats for noise blur and low resolution text edits
        rx = QtCore.QRegExp("[-+]?[0-9]*\.?[0-9]+")
        validator = QRegExpValidator(rx, self)

        self.ui.noisevalue.setValidator(validator)
        self.ui.noisevalue.setText("0.0")

        self.ui.blurvalue.setValidator(validator)
        self.ui.blurvalue.setText("0.0")

        self.ui.lowresvalue.setValidator(validator)
        self.ui.lowresvalue.setText("0.0")

        # handle check events in checkboxes
        self.ui.noisecheckBox.clicked.connect(lambda: self.handleCheckBox(self.ui.noisecheckBox))
        self.ui.blurcheckbox.clicked.connect(lambda: self.handleCheckBox(self.ui.blurcheckbox))
        self.ui.lrcheckbox.clicked.connect(lambda: self.handleCheckBox(self.ui.lrcheckbox))

    #################################################################
    # function to initialize image viewers
    def initImageViewers(self):
        self.setAcceptDrops(True)
        self.photoViewerInput = ImageLabel("Drop your face image here")
        self.photoViewerOutput = ImageLabel("Click apply!\nThe result will appear here")
        self.ui.imagesspace.addWidget(self.photoViewerInput)
        self.ui.imagesspace.addWidget(self.photoViewerOutput)
    ###################################################################################
    # function to handle enabling and disabling edit lines for corresponding checkboxes
    # and enable apply button if image exists in image viewer input
    def handleCheckBox(self,checkbox):
        # handle noise checkbox
        if checkbox==self.ui.noisecheckBox:
            if self.ui.noisecheckBox.isChecked():
                self.ui.noisevalue.setEnabled(True)
                if self.photoViewerInput.pixmap() is not None:
                    self.enableApplyFunc()
            else:
                self.ui.noisevalue.setEnabled(False)
                if self.ui.lrcheckbox.isChecked()==False and self.ui.blurcheckbox.isChecked()==False:
                    self.disableApplyFunc()

        # handle blur checkbox
        elif checkbox==self.ui.blurcheckbox:
            if self.ui.blurcheckbox.isChecked():
                self.ui.blurvalue.setEnabled(True)
                if self.photoViewerInput.pixmap() is not None:
                    self.enableApplyFunc()
            else:
                self.ui.blurvalue.setEnabled(False)
                if self.ui.lrcheckbox.isChecked()==False and self.ui.noisecheckBox.isChecked()==False:
                    self.disableApplyFunc()

        # handle low resolution checkbox
        elif checkbox==self.ui.lrcheckbox:
            if self.ui.lrcheckbox.isChecked():
                self.ui.lowresvalue.setEnabled(True)
                if self.photoViewerInput.pixmap() is not None:
                    self.enableApplyFunc()
            else:
                self.ui.lowresvalue.setEnabled(False)
                if self.ui.noisecheckBox.isChecked()==False and self.ui.blurcheckbox.isChecked()==False:
                    self.disableApplyFunc()

    #############################################################################
    # functions to handle drag and drop events on image viewer input
    def dragEnterEvent(self, event):
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
            print(file_path)
            self.set_image(file_path)

            event.accept()
        else:
            event.ignore()

    def set_image(self, file_path):
        self.photoViewerInput.setPixmap(QPixmap(file_path))
        if self.ui.noisecheckBox.isChecked() or self.ui.noisecheckBox.isChecked() or self.ui.noisecheckBox.isChecked():
            self.enableApplyFunc()


##############################################################################
    # functions to enable or disable apply button and change its style
    def enableApplyFunc(self):
        self.ui.apply_deg_btn.setEnabled(True)
        self.ui.apply_deg_btn.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 rgba(90, 255, 231, 255), stop:1 rgba(21, 205, 202, 255));border-radius: 10px;color:rgb(255, 255, 255);\n"
            "font: 75 10pt \"Georgia\";")
    def disableApplyFunc(self):
        self.ui.apply_deg_btn.setEnabled(False)
        self.ui.apply_deg_btn.setStyleSheet(
            "background-color: rgb(170, 170, 170);border-radius: 10px;color:rgb(255, 255, 255);\n"
            "font: 75 10pt \"Georgia\";")

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
