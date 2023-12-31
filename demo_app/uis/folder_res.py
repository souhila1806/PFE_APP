# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'folder_res.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_foldersRestoration(object):
    def setupUi(self, foldersRestoration):
        foldersRestoration.setObjectName("foldersRestoration")
        foldersRestoration.resize(1100, 850)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(foldersRestoration.sizePolicy().hasHeightForWidth())
        foldersRestoration.setSizePolicy(sizePolicy)
        foldersRestoration.setMinimumSize(QtCore.QSize(1100, 850))
        foldersRestoration.setMaximumSize(QtCore.QSize(1100, 900))
        foldersRestoration.setStyleSheet("#MainFrame{\n"
"background-color:rgba(35, 33, 40, 1);\n"
"}\n"
"QLabel{\n"
"color:rgba(255, 255, 255, 1);\n"
"font-weight:bold;\n"
"font: 12pt \"Georgia\";\n"
"}\n"
"#selection{\n"
"font-size:15px;\n"
"font-weight:bold;\n"
"}\n"
"QPushButton {\n"
"border-radius: 13px; \n"
"}\n"
"\n"
"#ApplyFBT{\n"
"font-size:14px;\n"
"color:rgba(255, 255, 255, 1);\n"
"font-weight:bold;\n"
"background-color:rgba(168, 171, 179, 1);\n"
"}\n"
"\n"
"#tabsPages{\n"
"background-color:rgba(56, 64, 73, 0.8);\n"
"}\n"
"#perceptuel, #ssim, #psnr, #lpips{\n"
"background-color:rgba(56, 64, 73, 0.8);\n"
"}\n"
"QTabWidget::pane {\n"
"    background-color:rgba(56, 64, 73, 0.8); \n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    background-color:rgba(95, 107, 110, 1); /* Set the desired background color for the tab buttons */\n"
"    color: white; /* Set the desired text color for the tab buttons */\n"
"font-weight:bold;\n"
"width: 150px; /* Set the desired width of the tab buttons */\n"
"height: 28px;\n"
"border-top-right-radius: 10px; /* Set the desired border radius for the top-right corner */\n"
"border-top-left-radius: 10px;\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    background-color: rgba(90, 255, 231, 1); /* Set the desired background color for the selected tab button */\n"
"    color: white; /* Set the desired text color for the selected tab button */\n"
"font-weight:bold;\n"
"}\n"
"QComboBox {\n"
"    border-radius: 2px; /* Set the desired border radius for all corners */\n"
" background-color:rgba(231, 235, 244, 1);\n"
"    \n"
"}\n"
"QComboBox::item {\n"
"    background-color:rgba(231, 235, 244, 1); /* Set the desired background color for the item */\n"
"    color: white;\n"
"font-weight:bold;\n"
"font-size:12px;\n"
" /* Set the desired color for the item text */\n"
"}\n"
"\n"
"#ssim_plot,#psnr_plot,#lpips_plot{\n"
"background-color:rgba(168, 171, 179, 0.59);\n"
" border-radius: 6px; \n"
"\n"
"}\n"
"#details{\n"
"background-color:rgba(47, 61, 78, 1);\n"
"}\n"
"")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(foldersRestoration)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.MainFrame = QtWidgets.QFrame(foldersRestoration)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MainFrame.sizePolicy().hasHeightForWidth())
        self.MainFrame.setSizePolicy(sizePolicy)
        self.MainFrame.setMinimumSize(QtCore.QSize(1100, 850))
        self.MainFrame.setMaximumSize(QtCore.QSize(1100, 850))
        self.MainFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.MainFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.MainFrame.setObjectName("MainFrame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.MainFrame)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.up_menu = QtWidgets.QFrame(self.MainFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.up_menu.sizePolicy().hasHeightForWidth())
        self.up_menu.setSizePolicy(sizePolicy)
        self.up_menu.setMinimumSize(QtCore.QSize(1100, 80))
        self.up_menu.setMaximumSize(QtCore.QSize(1100, 80))
        self.up_menu.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.up_menu.setFrameShadow(QtWidgets.QFrame.Raised)
        self.up_menu.setObjectName("up_menu")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.up_menu)
        self.horizontalLayout.setContentsMargins(50, 20, 50, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.up_menu)
        self.label_2.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(":/images/images/details.png"))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.frame_3 = QtWidgets.QFrame(self.up_menu)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 70))
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 70))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.fold = QtWidgets.QComboBox(self.frame_3)
        self.fold.setGeometry(QtCore.QRect(520, 10, 101, 28))
        self.fold.setMinimumSize(QtCore.QSize(101, 28))
        self.fold.setMaximumSize(QtCore.QSize(102, 28))
        self.fold.setStyleSheet(" QComboBox {\n"
"        background-color: white;\n"
"        font: 10pt \"Georgia\";\n"
"        padding-bottom: 8px;\n"
"        padding-left: 5px;\n"
"        border-radius: 10px;\n"
"        align:justify\n"
"    }\n"
"    \n"
"    QComboBox::down-arrow {\n"
"        subcontrol-origin: content;\n"
"        subcontrol-position: bottom right;\n"
"        border-radius: 10px;\n"
"        text-align: center;\n"
"        image: url(:/icons/images/fleche-vers-le-bas.png);\n"
"        border:none\n"
"    }\n"
"    \n"
"    QComboBox QAbstractItemView {\n"
"        background-color: white;\n"
"    }\n"
"    \n"
"    QComboBox QAbstractItemView::item:hover {\n"
"        background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 rgba(90, 255, 231, 255), stop:1 rgba(21, 205, 202, 255));\n"
"        color: white;\n"
"    }\n"
"QComboBox QAbstractItemView {\n"
"    background-color: white;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::scrollbar:vertical {\n"
"    background-color: #E0E0E0;  /* Set the background color of the vertical scrollbar */\n"
"    width: 10px;                /* Set the width of the scrollbar */\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::scrollbar-handle:vertical {\n"
"    background-color: #BDBDBD;  /* Set the color of the scrollbar handle */\n"
"    border-radius: 5px;         /* Add rounded corners to the scrollbar handle */\n"
"}\n"
"\n"
"QScrollBar:vertical {border: 1px solid #999999; background:white; width:10px; margin: 0px 0px 0px 0px;}\n"
"\n"
"\n"
"QScrollBar::handle:vertical {background:rgb(47, 61, 78);  min-height: 0px; border-radius: 20px}")
        self.fold.setObjectName("fold")
        self.fold.addItem("")
        self.fold.addItem("")
        self.fold.addItem("")
        self.fold.addItem("")
        self.fold.addItem("")
        self.fold.addItem("")
        self.fold.addItem("")
        self.fold.addItem("")
        self.fold.addItem("")
        self.fold.addItem("")
        self.fold.addItem("")
        self.selection = QtWidgets.QLabel(self.frame_3)
        self.selection.setGeometry(QtCore.QRect(10, 10, 300, 28))
        self.selection.setMinimumSize(QtCore.QSize(300, 28))
        self.selection.setMaximumSize(QtCore.QSize(250, 28))
        self.selection.setStyleSheet("font-size:20px")
        self.selection.setObjectName("selection")
        self.ApplyFBT = QtWidgets.QPushButton(self.frame_3)
        self.ApplyFBT.setGeometry(QtCore.QRect(710, 0, 200, 40))
        self.ApplyFBT.setMinimumSize(QtCore.QSize(101, 37))
        self.ApplyFBT.setMaximumSize(QtCore.QSize(200, 40))
        self.ApplyFBT.setStyleSheet("background-color: rgb(170, 170, 170);border-radius: 10px;color:rgb(255, 255, 255);\n"
"font: 75 10pt \"Georgia\";")
        self.ApplyFBT.setObjectName("ApplyFBT")
        self.selection_2 = QtWidgets.QLabel(self.frame_3)
        self.selection_2.setGeometry(QtCore.QRect(310, 10, 200, 28))
        self.selection_2.setMinimumSize(QtCore.QSize(200, 28))
        self.selection_2.setMaximumSize(QtCore.QSize(200, 28))
        self.selection_2.setStyleSheet("font-size:16px")
        self.selection_2.setObjectName("selection_2")
        self.horizontalLayout.addWidget(self.frame_3)
        self.verticalLayout_2.addWidget(self.up_menu)
        self.tabs = QtWidgets.QFrame(self.MainFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabs.sizePolicy().hasHeightForWidth())
        self.tabs.setSizePolicy(sizePolicy)
        self.tabs.setMinimumSize(QtCore.QSize(1000, 620))
        self.tabs.setMaximumSize(QtCore.QSize(1100, 620))
        self.tabs.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tabs.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tabs.setObjectName("tabs")
        self.gridLayout = QtWidgets.QGridLayout(self.tabs)
        self.gridLayout.setContentsMargins(0, 0, 0, 9)
        self.gridLayout.setObjectName("gridLayout")
        self.tabsPages = QtWidgets.QTabWidget(self.tabs)
        self.tabsPages.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabsPages.sizePolicy().hasHeightForWidth())
        self.tabsPages.setSizePolicy(sizePolicy)
        self.tabsPages.setMinimumSize(QtCore.QSize(1000, 550))
        self.tabsPages.setMaximumSize(QtCore.QSize(1000, 550))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(56, 64, 73, 204))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(56, 64, 73, 204))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(56, 64, 73, 204))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(56, 64, 73, 204))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(56, 64, 73, 204))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(56, 64, 73, 204))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(56, 64, 73, 204))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(56, 64, 73, 204))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(56, 64, 73, 204))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.tabsPages.setPalette(palette)
        self.tabsPages.setStyleSheet("")
        self.tabsPages.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabsPages.setElideMode(QtCore.Qt.ElideNone)
        self.tabsPages.setUsesScrollButtons(True)
        self.tabsPages.setDocumentMode(False)
        self.tabsPages.setMovable(True)
        self.tabsPages.setObjectName("tabsPages")
        self.ssim = QtWidgets.QWidget()
        self.ssim.setMinimumSize(QtCore.QSize(0, 600))
        self.ssim.setObjectName("ssim")
        self.ssim_plot = QtWidgets.QFrame(self.ssim)
        self.ssim_plot.setGeometry(QtCore.QRect(10, 10, 980, 500))
        self.ssim_plot.setMinimumSize(QtCore.QSize(980, 500))
        self.ssim_plot.setMaximumSize(QtCore.QSize(980, 500))
        self.ssim_plot.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ssim_plot.setFrameShadow(QtWidgets.QFrame.Plain)
        self.ssim_plot.setObjectName("ssim_plot")
        self.tabsPages.addTab(self.ssim, "")
        self.psnr = QtWidgets.QWidget()
        self.psnr.setObjectName("psnr")
        self.psnr_plot = QtWidgets.QFrame(self.psnr)
        self.psnr_plot.setGeometry(QtCore.QRect(10, 10, 980, 500))
        self.psnr_plot.setMinimumSize(QtCore.QSize(980, 500))
        self.psnr_plot.setMaximumSize(QtCore.QSize(960, 480))
        self.psnr_plot.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.psnr_plot.setFrameShadow(QtWidgets.QFrame.Plain)
        self.psnr_plot.setObjectName("psnr_plot")
        self.tabsPages.addTab(self.psnr, "")
        self.lpips = QtWidgets.QWidget()
        self.lpips.setObjectName("lpips")
        self.lpips_plot = QtWidgets.QFrame(self.lpips)
        self.lpips_plot.setGeometry(QtCore.QRect(10, 10, 980, 500))
        self.lpips_plot.setMinimumSize(QtCore.QSize(980, 500))
        self.lpips_plot.setMaximumSize(QtCore.QSize(960, 480))
        self.lpips_plot.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.lpips_plot.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lpips_plot.setObjectName("lpips_plot")
        self.tabsPages.addTab(self.lpips, "")
        self.gridLayout.addWidget(self.tabsPages, 0, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.tabs)
        self.details = QtWidgets.QFrame(self.MainFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.details.sizePolicy().hasHeightForWidth())
        self.details.setSizePolicy(sizePolicy)
        self.details.setMinimumSize(QtCore.QSize(1100, 170))
        self.details.setMaximumSize(QtCore.QSize(1100, 170))
        self.details.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.details.setFrameShadow(QtWidgets.QFrame.Raised)
        self.details.setObjectName("details")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.details)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_2 = QtWidgets.QFrame(self.details)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 60))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_2.setStyleSheet("background-color: rgb(47, 61, 78);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.formLayout = QtWidgets.QFormLayout(self.frame_2)
        self.formLayout.setContentsMargins(9, 9, -1, 0)
        self.formLayout.setObjectName("formLayout")
        self.icon1 = QtWidgets.QLabel(self.frame_2)
        self.icon1.setMinimumSize(QtCore.QSize(50, 48))
        self.icon1.setMaximumSize(QtCore.QSize(40, 30))
        self.icon1.setAutoFillBackground(False)
        self.icon1.setText("")
        self.icon1.setPixmap(QtGui.QPixmap(":/images/images/details.png"))
        self.icon1.setScaledContents(True)
        self.icon1.setObjectName("icon1")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.icon1)
        self.label_4 = QtWidgets.QLabel(self.frame_2)
        self.label_4.setMinimumSize(QtCore.QSize(111, 50))
        self.label_4.setMaximumSize(QtCore.QSize(140, 100))
        self.label_4.setStyleSheet("ba\n"
"background-color: rgb(47, 61, 78);")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_4)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame = QtWidgets.QFrame(self.details)
        self.frame.setMinimumSize(QtCore.QSize(1100, 100))
        self.frame.setMaximumSize(QtCore.QSize(1000, 100))
        self.frame.setStyleSheet("background-color: rgb(47, 61, 78);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setContentsMargins(20, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setMaximumSize(QtCore.QSize(37, 16777215))
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setMinimumSize(QtCore.QSize(61, 21))
        self.label_5.setMaximumSize(QtCore.QSize(100, 25))
        self.label_5.setStyleSheet("background-color: rgb(47, 61, 78);")
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.mean_xqlfw = QtWidgets.QLabel(self.frame)
        self.mean_xqlfw.setMinimumSize(QtCore.QSize(100, 21))
        self.mean_xqlfw.setMaximumSize(QtCore.QSize(100, 16777215))
        self.mean_xqlfw.setObjectName("mean_xqlfw")
        self.horizontalLayout_2.addWidget(self.mean_xqlfw)
        self.label_10 = QtWidgets.QLabel(self.frame)
        self.label_10.setMinimumSize(QtCore.QSize(61, 20))
        self.label_10.setMaximumSize(QtCore.QSize(100, 20))
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_2.addWidget(self.label_10)
        self.mean_gfpgan = QtWidgets.QLabel(self.frame)
        self.mean_gfpgan.setMinimumSize(QtCore.QSize(100, 20))
        self.mean_gfpgan.setMaximumSize(QtCore.QSize(100, 25))
        self.mean_gfpgan.setStyleSheet("background-color: rgb(47, 61, 78);")
        self.mean_gfpgan.setObjectName("mean_gfpgan")
        self.horizontalLayout_2.addWidget(self.mean_gfpgan)
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setMinimumSize(QtCore.QSize(51, 20))
        self.label_6.setMaximumSize(QtCore.QSize(100, 25))
        self.label_6.setStyleSheet("background-color: rgb(47, 61, 78);")
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.mean_sgpn = QtWidgets.QLabel(self.frame)
        self.mean_sgpn.setMinimumSize(QtCore.QSize(100, 20))
        self.mean_sgpn.setMaximumSize(QtCore.QSize(100, 25))
        self.mean_sgpn.setStyleSheet("background-color: rgb(47, 61, 78);")
        self.mean_sgpn.setObjectName("mean_sgpn")
        self.horizontalLayout_2.addWidget(self.mean_sgpn)
        self.label_8 = QtWidgets.QLabel(self.frame)
        self.label_8.setMinimumSize(QtCore.QSize(51, 20))
        self.label_8.setMaximumSize(QtCore.QSize(100, 25))
        self.label_8.setStyleSheet("background-color: rgb(47, 61, 78);")
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_2.addWidget(self.label_8)
        self.mean_gpen = QtWidgets.QLabel(self.frame)
        self.mean_gpen.setMinimumSize(QtCore.QSize(100, 20))
        self.mean_gpen.setMaximumSize(QtCore.QSize(100, 25))
        self.mean_gpen.setStyleSheet("background-color: rgb(47, 61, 78);")
        self.mean_gpen.setObjectName("mean_gpen")
        self.horizontalLayout_2.addWidget(self.mean_gpen)
        self.verticalLayout.addWidget(self.frame)
        self.verticalLayout_2.addWidget(self.details)
        self.verticalLayout_3.addWidget(self.MainFrame)

        self.retranslateUi(foldersRestoration)
        self.tabsPages.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(foldersRestoration)

    def retranslateUi(self, foldersRestoration):
        _translate = QtCore.QCoreApplication.translate
        foldersRestoration.setWindowTitle(_translate("foldersRestoration", "Form"))
        self.fold.setItemText(0, _translate("foldersRestoration", "ALL"))
        self.fold.setItemText(1, _translate("foldersRestoration", "0"))
        self.fold.setItemText(2, _translate("foldersRestoration", "1"))
        self.fold.setItemText(3, _translate("foldersRestoration", "2"))
        self.fold.setItemText(4, _translate("foldersRestoration", "3"))
        self.fold.setItemText(5, _translate("foldersRestoration", "4"))
        self.fold.setItemText(6, _translate("foldersRestoration", "5"))
        self.fold.setItemText(7, _translate("foldersRestoration", "6"))
        self.fold.setItemText(8, _translate("foldersRestoration", "7"))
        self.fold.setItemText(9, _translate("foldersRestoration", "8"))
        self.fold.setItemText(10, _translate("foldersRestoration", "9"))
        self.selection.setText(_translate("foldersRestoration", "Vizualise IQA Plots"))
        self.ApplyFBT.setText(_translate("foldersRestoration", "Apply"))
        self.selection_2.setText(_translate("foldersRestoration", "Choose your XQLFW folder:"))
        self.tabsPages.setTabText(self.tabsPages.indexOf(self.ssim), _translate("foldersRestoration", "SSIM"))
        self.tabsPages.setTabText(self.tabsPages.indexOf(self.psnr), _translate("foldersRestoration", "PSNR"))
        self.tabsPages.setTabText(self.tabsPages.indexOf(self.lpips), _translate("foldersRestoration", "LPIPS"))
        self.label_4.setText(_translate("foldersRestoration", "Mean values"))
        self.label_5.setText(_translate("foldersRestoration", "XQLFW: "))
        self.mean_xqlfw.setText(_translate("foldersRestoration", "-"))
        self.label_10.setText(_translate("foldersRestoration", "GFPGAN: "))
        self.mean_gfpgan.setText(_translate("foldersRestoration", "-"))
        self.label_6.setText(_translate("foldersRestoration", "SGPN: "))
        self.mean_sgpn.setText(_translate("foldersRestoration", "-"))
        self.label_8.setText(_translate("foldersRestoration", "GPEN: "))
        self.mean_gpen.setText(_translate("foldersRestoration", "-"))
import ressources_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    foldersRestoration = QtWidgets.QWidget()
    ui = Ui_foldersRestoration()
    ui.setupUi(foldersRestoration)
    foldersRestoration.show()
    sys.exit(app.exec_())
