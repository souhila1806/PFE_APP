from uis.cdta_ui import Ui_MainWindow
from python_files.pages.degradationpage import DegPage
from python_files.pages.pairsverifpage import PairsVerificationClass
from python_files.pages.folderverifpage import FoldsVerificationClass
from PyQt5 import QtWidgets
from python_files.pages.imageRestorationClass import ImageRestorationClass
from python_files.pages.foldsRestorationClass import FoldsRestorationClass
import sys
from PyQt5.QtGui import QIcon


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(1300, 850)
        # Set the window title
        self.setWindowTitle("G-Face+")
        # Set the application icon (logo)
        self.setWindowIcon(QIcon("images/Logo_notitle.png"))

        deg = DegPage(self)
        # PAGES
        self.initStackedWidget()
        # settings
        deg.initCheckBoxes()
        # Image viewers
        deg.initImageViewers()



    #############################################################################
    ############################## Functions#####################################
    #############################################################################

    # function to initialise stacked widget
    def initStackedWidget(self):
        self.activate_btn_menu()
        # Degradation Page
        self.ui.degradation_btn.clicked.connect(self.degradation_fun)

        # Pairs Restoration Page
        self.ui.pairs_rest_btn.clicked.connect(self.pairs_restoration_fun)

        # folds restoration Page
        self.ui.folds_rest_btn.clicked.connect(self.folds_restoration_fun)

        # Pairs verification Page
        self.ui.pairs_verif_btn.clicked.connect(self.pairs_verif_fun)

        # Pairs verification Page
        self.ui.folds_verif_btn.clicked.connect(self.folds_verif_fun)


    def activate_btn_menu(self):
        active_ss="background-color:rgb(28, 142, 178);color: rgb(255, 255, 255);font-size:8pt; font-weight:bold;font-family: Georama;border:none; height: 30px"
        unactive_ss="background-color:rgb(36, 40, 59);color: rgb(255, 255, 255);font-size:8pt; font-weight:bold;font-family: Georama;border:none; height: 30px"
        current_page=self.ui.stackedWidget.currentWidget().objectName()
        print(current_page)

        if current_page == "degradationpage":
            #activate
            self.ui.degradation_btn.setStyleSheet(active_ss)
            #unactivate
            self.ui.restoration_btn.setStyleSheet(unactive_ss)
            self.ui.verification.setStyleSheet(unactive_ss)

        elif current_page=="ImageResForm" or current_page== "FoldsResForm":
            # activate
            self.ui.restoration_btn.setStyleSheet(active_ss)
            # unactivate
            self.ui.degradation_btn.setStyleSheet(unactive_ss)
            self.ui.verification.setStyleSheet(unactive_ss)

        elif current_page=="pairsVerifPage" or current_page== "foldsVerifPage":
            # activate
            self.ui.verification.setStyleSheet(active_ss)
            # unactivate
            self.ui.degradation_btn.setStyleSheet(unactive_ss)
            self.ui.restoration_btn.setStyleSheet(unactive_ss)




    #############################################################################
    # functions to handle the stacked widget pages

    def degradation_fun(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.degradationpage)
        self.activate_btn_menu()

    def pairs_restoration_fun(self):
        page = ImageRestorationClass()
        self.ui.stackedWidget.addWidget(page)
        self.ui.stackedWidget.setCurrentWidget(page)
        self.activate_btn_menu()
        self.ui.pairs_rest_btn.setStyleSheet(
            "color: white;font-size:8pt; font-weight:bold;font-family: Georama;border:none; height: 30px}\n"
            "QPushButton:hover{background-color:rgb(28, 142, 178);")
        self.ui.folds_rest_btn.setStyleSheet(
            "color: grey;font-size:8pt; font-weight:bold;font-family: Georama;border:none; height: 30px}\n"
            "QPushButton:hover{background-color:rgb(28, 142, 178);")

    def folds_restoration_fun(self):
        page = FoldsRestorationClass()
        self.ui.stackedWidget.addWidget(page)
        self.ui.stackedWidget.setCurrentWidget(page)
        self.activate_btn_menu()
        self.ui.pairs_rest_btn.setStyleSheet(
            "color: grey;font-size:8pt; font-weight:bold;font-family: Georama;border:none; height: 30px}\n"
            "QPushButton:hover{background-color:rgb(28, 142, 178);")
        self.ui.folds_rest_btn.setStyleSheet(
            "color: white;font-size:8pt; font-weight:bold;font-family: Georama;border:none; height: 30px}\n"
            "QPushButton:hover{background-color:rgb(28, 142, 178);")


    '''def pairs_restoration_fun(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.pairrestorationpage)
        self.activate_btn_menu()
        self.ui.pairs_rest_btn.setStyleSheet("color: white;font-size:8pt; font-weight:bold;font-family: Georama;border:none; height: 30px}\n"
"QPushButton:hover{background-color:rgb(28, 142, 178);")
        self.ui.folds_rest_btn.setStyleSheet("color: grey;font-size:8pt; font-weight:bold;font-family: Georama;border:none; height: 30px}\n"
"QPushButton:hover{background-color:rgb(28, 142, 178);")

    def folds_restoration_fun(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.foldsrestorationpage)
        self.activate_btn_menu()
        self.ui.pairs_rest_btn.setStyleSheet("color: grey;font-size:8pt; font-weight:bold;font-family: Georama;border:none; height: 30px}\n"
"QPushButton:hover{background-color:rgb(28, 142, 178);")
        self.ui.folds_rest_btn.setStyleSheet("color: white;font-size:8pt; font-weight:bold;font-family: Georama;border:none; height: 30px}\n"
"QPushButton:hover{background-color:rgb(28, 142, 178);")'''

    def pairs_verif_fun(self):
        page = PairsVerificationClass()
        self.ui.stackedWidget.addWidget(page)
        self.ui.stackedWidget.setCurrentWidget(page)
        self.activate_btn_menu()
        self.ui.pairs_verif_btn.setStyleSheet(
            "color: white;font-size:8pt; font-weight:bold;font-family: Georama;border:none; height: 30px}\n"
            "QPushButton:hover{background-color:rgb(28, 142, 178);")
        self.ui.folds_verif_btn.setStyleSheet(
            "color: grey;font-size:8pt; font-weight:bold;font-family: Georama;border:none; height: 30px}\n"
            "QPushButton:hover{background-color:rgb(28, 142, 178);")


    def folds_verif_fun(self):
        page = FoldsVerificationClass()
        self.ui.stackedWidget.addWidget(page)
        self.ui.stackedWidget.setCurrentWidget(page)
        self.activate_btn_menu()
        self.ui.pairs_verif_btn.setStyleSheet(
            "color: grey;font-size:8pt; font-weight:bold;font-family: Georama;border:none; height: 30px}\n"
            "QPushButton:hover{background-color:rgb(28, 142, 178);")
        self.ui.folds_verif_btn.setStyleSheet(
            "color: white;font-size:8pt; font-weight:bold;font-family: Georama;border:none; height: 30px}\n"
            "QPushButton:hover{background-color:rgb(28, 142, 178);")


    # main function
if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        mw = MainWindow()
        mw.show()
        app.exec_()
    except Exception as e:
        import traceback
        traceback.print_exc()
