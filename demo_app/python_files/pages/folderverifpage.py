import cv2
import os
import random

import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QScrollArea, QWidget, QGridLayout
from python_files.functions.plotclasses import RegressionPlotWidget,SimilarityPlotWidget,PlotWidget,RocCurvePlotWidget,MagnitudePlotWidget

from uis.foldsverif_ui import Ui_FoldsVerifForm
from python_files.functions.fusion_funcs import ff_fold,ff_all,sf_fold,sf_all,hf_all,hf_fold
from python_files.functions.lfw_xqlfw_funcs import verif_fold,verif_all
from ..loading import LoadingScreen
from PyQt5.QtCore import QThread, pyqtSignal

class DegradationThread(QThread):
    finished = pyqtSignal(object)

    def __init__(self, page,fusiontype, rec_model, restorationmodels):
        super().__init__()

        self.page = page
        self.fusiontype = fusiontype
        self.rec_model = rec_model
        self.restorationmodels = restorationmodels

    def run(self):
        if not hasattr(self.page, 'reg_plot_widget'):
            self.page.reg_plot_widget = RegressionPlotWidget(self.fusiontype, self.rec_model, self.restorationmodels)
            self.page.ui.fusionregressionplot.setLayout(QGridLayout())

        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Create a container widget for the scroll area
        scroll_widget = QWidget()
        scroll_widget.setLayout(QGridLayout())

        # Add the RegressionPlotWidget to the container widget
        scroll_widget.layout().addWidget(self.page.reg_plot_widget)

        # Set the container widget as the scroll area's widget
        scroll_area.setWidget(scroll_widget)
        scroll_area.verticalScrollBar().setStyleSheet(
            """
            QScrollBar:vertical {
                background-color: #E0E0E0;
                width: 10px;
                border: 1px solid #999999;
                margin: 0px 0px 0px 0px;
            }

            QScrollBar::handle:vertical {
                background-color: #BDBDBD;
                border-radius: 5px;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                background-color: transparent;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background-color: transparent;
            }
            """
        )

        # Set the layout of the fusion regression plot widget
        self.page.ui.fusionregressionplot.layout().addWidget(scroll_area)

        self.page.reg_plot_widget.plot(self.fusiontype, self.rec_model, self.restorationmodels)
        result='Done'
        self.finished.emit(result)


class FoldsVerificationClass(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_FoldsVerifForm()
        self.ui.setupUi(self)
        self.setObjectName("foldsVerifPage")
        self.ui.rightmenubar.move(900, 0)
        self.init_checkboxes()
        self.ui.advancedwidget.setHidden(True)
        self.ui.tabsPages.setTabEnabled(4, False)
        self.enableApplyFunc()
        self.ui.apply_folds_verif_btn.clicked.connect(self.setverifvalue)
        self.ui.datasetcombobox.currentIndexChanged[str].connect(self.handledatasetcombobox)

    def handledatasetcombobox(self,dataset):
        if dataset=="LFW":
            self.ui.advancedwidget.setHidden(True)
            self.ui.rest_model_classic.clear()
            self.ui.rest_model_classic.addItem("GFPGAN")
            self.ui.rest_model_classic.addItem("GPEN")
        else:
            self.ui.advancedwidget.setHidden(False)
            self.ui.rest_model_classic.clear()
            self.ui.rest_model_classic.addItem("GFPGAN")
            self.ui.rest_model_classic.addItem("GPEN")
            self.ui.rest_model_classic.addItem("SGPN")
    def setverifvalue(self):
        try:
            model = self.ui.recognitionmodel.currentText()
            dataset=self.ui.datasetcombobox.currentText().lower()
            acc = 0
            threshold = 0
            far=0
            frr=0
            rest=None
            train=pd.DataFrame()
            fold=self.ui.foldcombobox.currentText()
            # control the magnitude and similarity tabs
            if dataset=="xqlfw" and model =="MagFace":
                self.ui.tabsPages.setTabEnabled(2, True)
            else:
                self.ui.tabsPages.setTabEnabled(2, False)

            if dataset=="xqlfw" and self.ui.classic_checkbox.isChecked():
                self.ui.tabsPages.setTabEnabled(3, True)
            else:
                self.ui.tabsPages.setTabEnabled(3, False)
            #if advanced restoration
            if self.ui.advancedcheckbox.isChecked():
                fusion_type = self.ui.typefusioncombobox.currentText()

                if fusion_type == "feature fusion":
                    restoration = self.ui.featurelevelcombobox.currentText()

                    # get the restoration models list
                    if restoration == "ALL":
                        restoration_models = ["GFPGAN", "SGPN", "GPEN"]
                    else:
                        restoration_models = restoration.split("_")

                    #get the accuracy and threshold
                    if fold=="ALL":
                        acc, threshold,far,frr,train=ff_all(restoration_models,model)
                    else:
                        acc, threshold, far, frr,train = ff_fold(int(fold),restoration_models,model)

                elif fusion_type == "score fusion":

                    #get the restoration models
                    restoration = self.ui.scorelevelcombobox.currentText()
                    restoration_models = restoration.split("_")

                    #get the accuracy and threshold
                    if fold == "ALL":
                        acc, threshold, far, frr,train = sf_all(restoration_models, model)
                    else:
                        acc, threshold, far, frr,train = sf_fold(int(fold), restoration_models, model)

                    #draw regression plot
                    self.regressionplot("score",restoration_models,model)

                elif fusion_type == "hybrid fusion":

                    #get the first level restoration model
                    restorationl1 = self.ui.featurelevelcombobox.currentText()
                    if restorationl1 == "ALL":
                        restoration_modelsl1 = ["GFPGAN", "SGPN", "GPEN"]
                    else:
                        restoration_modelsl1 = restorationl1.split("_")

                    #get the second level restoration model
                    restorationl2 = self.ui.scorelevelcombobox.currentText()

                    #get accuracy and threshold
                    if fold=="ALL":
                        acc, threshold,far,frr,train=hf_all(restoration_modelsl1,restorationl2,model)
                    else:
                        acc, threshold,far,frr,train=hf_fold(int(fold),restoration_modelsl1,restorationl2,model)

                    #draw regression plot
                    self.regressionplot("hybrid", restoration_modelsl1, model)
            #if classic or no restoration
            else:
                if self.ui.classic_checkbox.isChecked():
                    rest = self.ui.rest_model_classic.currentText()

                #get the accuracy and threshold
                if fold == "ALL":
                    acc, threshold, far, frr,train = verif_all(dataset,model,rest)
                else:
                    acc, threshold, far, frr,train = verif_fold(dataset,int(fold), model, rest)

            # write the infos in labels
            self.ui.accuracy.setText(str(round(acc, 4)))
            self.ui.threshold.setText(str(round(threshold, 4)))
            self.ui.FA.setText(str(round(far,4)))
            self.ui.FR.setText(str(round(frr,4)))

            #draw other plots
            self.plots(train,model)
        except Exception as e:
            import traceback
            traceback.print_exc()
    def plots(self,train,model):
            if not hasattr(self, 'dist_plot_widget'):
                self.dist_plot_widget = PlotWidget(train)
                self.ui.dist_plot.setLayout(self.dist_plot_widget.layout())
            self.dist_plot_widget.plot(train)
            if not hasattr(self, 'roc_plot_widget'):
                self.roc_plot_widget = RocCurvePlotWidget(train)
                self.ui.roccurve_plot.setLayout(self.roc_plot_widget.layout())
            self.roc_plot_widget.plot(train)
            is_enabled = self.ui.tabsPages.isTabEnabled(2)
            if is_enabled:
                if self.ui.classic_checkbox.isChecked():
                    rest = self.ui.rest_model_classic.currentText().lower()
                elif self.ui.advancedcheckbox.isChecked():
                    rest = None
                else:
                    rest = "xqlfw"
                if not hasattr(self, 'mag_plot_widget'):
                    self.mag_plot_widget = MagnitudePlotWidget(rest)
                    self.ui.magnitudeplot.setLayout(self.mag_plot_widget.layout())
                self.mag_plot_widget.plot(rest)
            is_enabled = self.ui.tabsPages.isTabEnabled(3)
            if is_enabled:
                if self.ui.classic_checkbox.isChecked():
                    rest = self.ui.rest_model_classic.currentText().lower()
                else:
                    rest = None
                if not hasattr(self, 'sim_plot_widget'):
                    self.sim_plot_widget = SimilarityPlotWidget(model,rest)
                    self.ui.simindexplot.setLayout(self.sim_plot_widget.layout())
                self.sim_plot_widget.plot(model,rest)



    def regressionplot(self, fusiontype, restorationmodels, rec_model):
        is_enabled = self.ui.tabsPages.isTabEnabled(4)
        if is_enabled:
            self.degradation_thread = DegradationThread(self,fusiontype, rec_model, restorationmodels)
            self.degradation_thread.finished.connect(self.handle_degradation_finished)

            # Start the thread
            self.loading_screen = LoadingScreen()
            self.loading_screen.startLoading()
            self.degradation_thread.start()


    def handle_degradation_finished(self):

        self.loading_screen.stopLoading()
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
                self.ui.tabsPages.setTabEnabled(4, False)
                if self.ui.classic_checkbox.isChecked():
                    self.ui.tabsPages.setTabEnabled(2, True)
                    self.ui.rest_model_classic.setEnabled(True)
                    self.ui.advancedcheckbox.setChecked(False)
                    self.ui.featurelevelcombobox.setEnabled(False)
                    self.ui.scorelevelcombobox.setEnabled(False)
                    self.ui.typefusioncombobox.setEnabled(False)
                else:
                    self.ui.rest_model_classic.setEnabled(False)
            else:
                if self.ui.advancedcheckbox.isChecked():
                    self.ui.tabsPages.setTabEnabled(2, False)
                    self.ui.rest_model_classic.setEnabled(False)
                    self.ui.classic_checkbox.setChecked(False)
                    self.ui.featurelevelcombobox.setEnabled(True)
                    self.ui.typefusioncombobox.setCurrentText("feature fusion")
                    self.ui.scorelevelcombobox.setEnabled(False)
                    self.ui.typefusioncombobox.setEnabled(True)
                else:
                    self.ui.tabsPages.setTabEnabled(2, True)
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
            self.ui.tabsPages.setTabEnabled(4, False)
            self.ui.featurelevelcombobox.setEnabled(True)
            self.ui.scorelevelcombobox.setEnabled(False)
        elif selected_option == "score fusion":
            self.ui.tabsPages.setTabEnabled(4, True)
            self.ui.featurelevelcombobox.setEnabled(False)
            self.ui.scorelevelcombobox.setEnabled(True)
            self.ui.scorelevelcombobox.clear()
            self.ui.scorelevelcombobox.addItem("GPEN_GFPGAN")
            self.ui.scorelevelcombobox.addItem("GPEN_SGPN")
            self.ui.scorelevelcombobox.addItem("SGPN_GFPGAN")
        elif selected_option == "hybrid fusion":
            self.ui.tabsPages.setTabEnabled(4, True)
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
        self.ui.apply_folds_verif_btn.setEnabled(True)
        self.ui.apply_folds_verif_btn.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 rgba(90, 255, 231, 255), stop:1 rgba(21, 205, 202, 255));border-radius: 10px;color:rgb(255, 255, 255);\n"
            "font: 75 10pt \"Georgia\";")
    def disableApplyFunc(self):
        self.ui.apply_folds_verif_btn.setEnabled(False)
        self.ui.apply_folds_verif_btn.setStyleSheet(
            "background-color: rgb(170, 170, 170);border-radius: 10px;color:rgb(255, 255, 255);\n"
            "font: 75 10pt \"Georgia\";")
