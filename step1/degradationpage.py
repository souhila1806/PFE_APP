from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap,QRegExpValidator,QImage
class ImageLabel(QtWidgets.QLabel):
    def __init__(self,text,main_app):
        super().__init__()
        self.main_app = main_app
        self.setAcceptDrops(True)

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
            print(file_path)
            self.set_image(file_path)

            event.accept()
        else:
            event.ignore()

    def set_image(self, file_path):
        image = QImage(file_path)
        pixmap = QPixmap.fromImage(image)
        self.main_app.photoViewerInput.setPixmap(pixmap)
        if self.main_app.ui.noisecheckBox.isChecked() or self.main_app.ui.blurcheckbox.isChecked() or self.main_app.ui.lrcheckbox.isChecked():
            self.enableApplyFunc()


class DegPage(QtWidgets.QMainWindow):
    def __init__(self,main_app):
        super().__init__()
        self.main_app = main_app


    ############################################################################
    # function to initialize settings checkboxes and edit texts
    def initCheckBoxes(self):
        # allow only floats for noise blur and low resolution text edits
        rx = QtCore.QRegExp("[-+]?[0-9]*\.?[0-9]+")
        validator = QRegExpValidator(rx, self.main_app)

        self.main_app.ui.noisevalue.setValidator(validator)
        self.main_app.ui.noisevalue.setText("0.0")

        self.main_app.ui.blurvalue.setValidator(validator)
        self.main_app.ui.blurvalue.setText("0.0")

        self.main_app.ui.lowresvalue.setValidator(validator)
        self.main_app.ui.lowresvalue.setText("0.0")

        # handle check events in checkboxes
        self.main_app.ui.noisecheckBox.clicked.connect(lambda: self.handleCheckBox(self.main_app.ui.noisecheckBox))
        self.main_app.ui.blurcheckbox.clicked.connect(lambda: self.handleCheckBox(self.main_app.ui.blurcheckbox))
        self.main_app.ui.lrcheckbox.clicked.connect(lambda: self.handleCheckBox(self.main_app.ui.lrcheckbox))

    #################################################################
    # function to initialize image viewers
    def initImageViewers(self):
        self.main_app.setAcceptDrops(True)
        self.main_app.photoViewerInput = ImageLabel("Drop your face image here",self.main_app)
        self.main_app.photoViewerOutput = ImageLabel("Click apply!\nThe result will appear here",self.main_app)
        self.main_app.ui.imagesspace.addWidget(self.main_app.photoViewerInput)
        self.main_app.ui.imagesspace.addWidget(self.main_app.photoViewerOutput)
    ###################################################################################
    # function to handle enabling and disabling edit lines for corresponding checkboxes
    # and enable apply button if image exists in image viewer input
    def handleCheckBox(self,checkbox):
        # handle noise checkbox
        if checkbox==self.main_app.ui.noisecheckBox:
            if self.main_app.ui.noisecheckBox.isChecked():
                self.main_app.ui.noisevalue.setEnabled(True)
                if self.main_app.photoViewerInput.pixmap() is not None:
                    self.enableApplyFunc()
            else:
                self.main_app.ui.noisevalue.setEnabled(False)
                if self.main_app.ui.lrcheckbox.isChecked()==False and self.main_app.ui.blurcheckbox.isChecked()==False:
                    self.disableApplyFunc()

        # handle blur checkbox
        elif checkbox==self.main_app.ui.blurcheckbox:
            if self.main_app.ui.blurcheckbox.isChecked():
                self.main_app.ui.blurvalue.setEnabled(True)
                if self.main_app.photoViewerInput.pixmap() is not None:
                    self.enableApplyFunc()
            else:
                self.main_app.ui.blurvalue.setEnabled(False)
                if self.main_app.ui.lrcheckbox.isChecked()==False and self.main_app.ui.noisecheckBox.isChecked()==False:
                    self.disableApplyFunc()

        # handle low resolution checkbox
        elif checkbox==self.main_app.ui.lrcheckbox:
            if self.main_app.ui.lrcheckbox.isChecked():
                self.main_app.ui.lowresvalue.setEnabled(True)
                if self.main_app.photoViewerInput.pixmap() is not None:
                    self.enableApplyFunc()
            else:
                self.main_app.ui.lowresvalue.setEnabled(False)
                if self.main_app.ui.noisecheckBox.isChecked()==False and self.main_app.ui.blurcheckbox.isChecked()==False:
                    self.disableApplyFunc()


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