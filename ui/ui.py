# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(330, 194)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(330, 194))
        MainWindow.setMaximumSize(QtCore.QSize(330, 216))
        MainWindow.setAutoFillBackground(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(330, 175))
        self.centralwidget.setMaximumSize(QtCore.QSize(330, 175))
        self.centralwidget.setObjectName("centralwidget")
        self.mainFrame = QtWidgets.QFrame(self.centralwidget)
        self.mainFrame.setGeometry(QtCore.QRect(0, 0, 330, 175))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainFrame.sizePolicy().hasHeightForWidth())
        self.mainFrame.setSizePolicy(sizePolicy)
        self.mainFrame.setMinimumSize(QtCore.QSize(330, 175))
        self.mainFrame.setMaximumSize(QtCore.QSize(330, 175))
        self.mainFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mainFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mainFrame.setObjectName("mainFrame")
        self.botFrame = QtWidgets.QFrame(self.mainFrame)
        self.botFrame.setGeometry(QtCore.QRect(0, 150, 330, 25))
        self.botFrame.setMinimumSize(QtCore.QSize(330, 25))
        self.botFrame.setMaximumSize(QtCore.QSize(330, 25))
        self.botFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.botFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.botFrame.setObjectName("botFrame")
        self.hLine = QtWidgets.QFrame(self.botFrame)
        self.hLine.setGeometry(QtCore.QRect(0, 0, 330, 2))
        self.hLine.setMinimumSize(QtCore.QSize(330, 2))
        self.hLine.setMaximumSize(QtCore.QSize(330, 2))
        self.hLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.hLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.hLine.setObjectName("hLine")
        self.vLine = QtWidgets.QFrame(self.botFrame)
        self.vLine.setGeometry(QtCore.QRect(250, 0, 2, 25))
        self.vLine.setMinimumSize(QtCore.QSize(2, 25))
        self.vLine.setMaximumSize(QtCore.QSize(2, 25))
        self.vLine.setFrameShape(QtWidgets.QFrame.VLine)
        self.vLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.vLine.setObjectName("vLine")
        self.versionLbl = QtWidgets.QLabel(self.botFrame)
        self.versionLbl.setGeometry(QtCore.QRect(260, 2, 60, 21))
        self.versionLbl.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.versionLbl.setText("")
        self.versionLbl.setAlignment(QtCore.Qt.AlignCenter)
        self.versionLbl.setObjectName("versionLbl")
        self.infoLbl = QtWidgets.QLabel(self.botFrame)
        self.infoLbl.setGeometry(QtCore.QRect(10, 2, 230, 21))
        self.infoLbl.setText("")
        self.infoLbl.setObjectName("infoLbl")
        self.folderBtn = QtWidgets.QPushButton(self.mainFrame)
        self.folderBtn.setGeometry(QtCore.QRect(25, 20, 75, 30))
        self.folderBtn.setObjectName("folderBtn")
        self.fileBtn = QtWidgets.QPushButton(self.mainFrame)
        self.fileBtn.setGeometry(QtCore.QRect(230, 20, 75, 30))
        self.fileBtn.setObjectName("fileBtn")
        self.srcLbl = QtWidgets.QLabel(self.mainFrame)
        self.srcLbl.setGeometry(QtCore.QRect(10, 70, 40, 20))
        font = QtGui.QFont()
        font.setItalic(False)
        self.srcLbl.setFont(font)
        self.srcLbl.setObjectName("srcLbl")
        self.srcEntryLbl = QtWidgets.QLabel(self.mainFrame)
        self.srcEntryLbl.setGeometry(QtCore.QRect(55, 70, 260, 20))
        font = QtGui.QFont()
        font.setItalic(True)
        self.srcEntryLbl.setFont(font)
        self.srcEntryLbl.setFrameShape(QtWidgets.QFrame.Panel)
        self.srcEntryLbl.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.srcEntryLbl.setText("")
        self.srcEntryLbl.setObjectName("srcEntryLbl")
        self.startbtn = QtWidgets.QToolButton(self.mainFrame)
        self.startbtn.setEnabled(False)
        self.startbtn.setGeometry(QtCore.QRect(135, 15, 60, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.startbtn.setFont(font)
        self.startbtn.setObjectName("startbtn")
        self.progressBar = QtWidgets.QProgressBar(self.mainFrame)
        self.progressBar.setGeometry(QtCore.QRect(10, 120, 311, 15))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName("progressBar")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 330, 21))
        self.menubar.setObjectName("menubar")
        self.menuOptimization = QtWidgets.QMenu(self.menubar)
        self.menuOptimization.setObjectName("menuOptimization")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAccept_all_Optimizations = QtWidgets.QAction(MainWindow)
        self.actionAccept_all_Optimizations.setCheckable(True)
        self.actionAccept_all_Optimizations.setChecked(True)
        self.actionAccept_all_Optimizations.setObjectName("actionAccept_all_Optimizations")
        self.actionAccept_O1 = QtWidgets.QAction(MainWindow)
        self.actionAccept_O1.setCheckable(True)
        self.actionAccept_O1.setObjectName("actionAccept_O1")
        self.actionAccept_O2 = QtWidgets.QAction(MainWindow)
        self.actionAccept_O2.setCheckable(True)
        self.actionAccept_O2.setObjectName("actionAccept_O2")
        self.actionAccept_O3 = QtWidgets.QAction(MainWindow)
        self.actionAccept_O3.setCheckable(True)
        self.actionAccept_O3.setObjectName("actionAccept_O3")
        self.actionAccept_O0 = QtWidgets.QAction(MainWindow)
        self.actionAccept_O0.setCheckable(True)
        self.actionAccept_O0.setObjectName("actionAccept_O0")
        self.actionAccept_Ofast = QtWidgets.QAction(MainWindow)
        self.actionAccept_Ofast.setCheckable(True)
        self.actionAccept_Ofast.setObjectName("actionAccept_Ofast")
        self.actionAccept_Og = QtWidgets.QAction(MainWindow)
        self.actionAccept_Og.setCheckable(True)
        self.actionAccept_Og.setObjectName("actionAccept_Og")
        self.actionAccept_Os = QtWidgets.QAction(MainWindow)
        self.actionAccept_Os.setCheckable(True)
        self.actionAccept_Os.setObjectName("actionAccept_Os")
        self.menuOptimization.addAction(self.actionAccept_all_Optimizations)
        self.menuOptimization.addAction(self.actionAccept_Os)
        self.menuOptimization.addAction(self.actionAccept_O1)
        self.menuOptimization.addAction(self.actionAccept_O2)
        self.menuOptimization.addAction(self.actionAccept_O3)
        self.menuOptimization.addAction(self.actionAccept_O0)
        self.menuOptimization.addAction(self.actionAccept_Ofast)
        self.menuOptimization.addAction(self.actionAccept_Og)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuOptimization.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.folderBtn.setText(_translate("MainWindow", "Select Folder"))
        self.fileBtn.setText(_translate("MainWindow", "Select File"))
        self.srcLbl.setText(_translate("MainWindow", "Source:"))
        self.startbtn.setText(_translate("MainWindow", "Go"))
        self.menuOptimization.setTitle(_translate("MainWindow", "Optimization"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAccept_all_Optimizations.setText(_translate("MainWindow", "Accept all Optimizations"))
        self.actionAccept_O1.setText(_translate("MainWindow", "Accept \'-O1\'"))
        self.actionAccept_O2.setText(_translate("MainWindow", "Accept \'-O2\'"))
        self.actionAccept_O3.setText(_translate("MainWindow", "Accept \'-O3\'"))
        self.actionAccept_O0.setText(_translate("MainWindow", "Accept \'-O0\'"))
        self.actionAccept_Ofast.setText(_translate("MainWindow", "Accept \'-Ofast\'"))
        self.actionAccept_Og.setText(_translate("MainWindow", "Accept \'-Og\'"))
        self.actionAccept_Os.setText(_translate("MainWindow", "Accept \'-Os\'"))