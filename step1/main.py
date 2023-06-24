from cdta_ui import Ui_MainWindow
from degradationpage import DegPage
from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(1300, 850)

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
        current_page=self.ui.stackedWidget.currentWidget()

        if current_page == self.ui.degradationpage:
            #activate
            self.ui.degradation_btn.setStyleSheet(active_ss)
            #unactivate
            self.ui.restoration_btn.setStyleSheet(unactive_ss)
            self.ui.verification.setStyleSheet(unactive_ss)

        elif current_page==self.ui.pairrestorationpage or current_page== self.ui.foldsrestorationpage:
            # activate
            self.ui.restoration_btn.setStyleSheet(active_ss)
            # unactivate
            self.ui.degradation_btn.setStyleSheet(unactive_ss)
            self.ui.verification.setStyleSheet(unactive_ss)

        elif current_page==self.ui.pairsverifpage or current_page== self.ui.foldsverifpage:
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
"QPushButton:hover{background-color:rgb(28, 142, 178);")

    def pairs_verif_fun(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.pairsverifpage)
        self.activate_btn_menu()
        self.ui.pairs_verif_btn.setStyleSheet(
            "color: white;font-size:8pt; font-weight:bold;font-family: Georama;border:none; height: 30px}\n"
            "QPushButton:hover{background-color:rgb(28, 142, 178);")
        self.ui.folds_verif_btn.setStyleSheet(
            "color: grey;font-size:8pt; font-weight:bold;font-family: Georama;border:none; height: 30px}\n"
            "QPushButton:hover{background-color:rgb(28, 142, 178);")

    def folds_verif_fun(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.foldsverifpage)
        self.activate_btn_menu()
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
