# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(803, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("QWidget#centralwidget {\n"
"    background-color: none;\n"
"    border: 1px solid;\n"
"}\n"
"\n"
"")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 801, 561))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.l_video = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.l_video.setEnabled(True)
        self.l_video.setMinimumSize(QtCore.QSize(779, 257))
        self.l_video.setObjectName("l_video")
        self.verticalLayout_2.addWidget(self.l_video)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pbtn_detect = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pbtn_detect.setMinimumSize(QtCore.QSize(0, 20))
        self.pbtn_detect.setStyleSheet("QPushButton {\n"
"    font-size: 14px;\n"
"    color: #fff;\n"
"    background-color: rgb(133, 129, 255);\n"
"    font: 75 12pt \"Calibri\";\n"
"    border: 1px solid transparent;\n"
"    border-color: #357ebd;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(224, 232, 246);\n"
"}\n"
"\n"
"")
        self.pbtn_detect.setAutoExclusive(True)
        self.pbtn_detect.setObjectName("pbtn_detect")
        self.horizontalLayout.addWidget(self.pbtn_detect)
        self.pbtn_classify = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pbtn_classify.setMinimumSize(QtCore.QSize(0, 20))
        self.pbtn_classify.setStyleSheet("QPushButton {\n"
"    font-size: 14px;\n"
"    color: #fff;\n"
"    background-color: rgb(133, 129, 255);\n"
"    font: 75 12pt \"Calibri\";\n"
"    border: 1px solid transparent;\n"
"    border-color: #357ebd;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(224, 232, 246);\n"
"}\n"
"")
        self.pbtn_classify.setAutoExclusive(True)
        self.pbtn_classify.setObjectName("pbtn_classify")
        self.horizontalLayout.addWidget(self.pbtn_classify)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.l_status = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.l_status.setMinimumSize(QtCore.QSize(0, 30))
        self.l_status.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(255, 255, 255, 255));\n"
"border: 1px solid darkgrey;")
        self.l_status.setObjectName("l_status")
        self.horizontalLayout_3.addWidget(self.l_status)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.setStretch(0, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 803, 21))
        self.menubar.setObjectName("menubar")
        self.menuExit = QtWidgets.QMenu(self.menubar)
        self.menuExit.setObjectName("menuExit")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_train = QtWidgets.QAction(MainWindow)
        self.action_train.setObjectName("action_train")
        self.action_quit = QtWidgets.QAction(MainWindow)
        self.action_quit.setObjectName("action_quit")
        self.action_camera = QtWidgets.QAction(MainWindow)
        self.action_camera.setCheckable(True)
        self.action_camera.setObjectName("action_camera")
        self.action_about = QtWidgets.QAction(MainWindow)
        self.action_about.setObjectName("action_about")
        self.menuExit.addAction(self.action_train)
        self.menuExit.addAction(self.action_camera)
        self.menuExit.addSeparator()
        self.menuExit.addAction(self.action_quit)
        self.menuHelp.addAction(self.action_about)
        self.menubar.addAction(self.menuExit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pbtn_detect.setText(_translate("MainWindow", "Detect"))
        self.pbtn_classify.setText(_translate("MainWindow", "Recognize"))
        self.l_status.setText(_translate("MainWindow", "Part Number: 10506\n"
"Stock on hand: 20\n"
"Confidence: 95%"))
        self.menuExit.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.action_train.setText(_translate("MainWindow", "Train"))
        self.action_quit.setText(_translate("MainWindow", "Quit"))
        self.action_camera.setText(_translate("MainWindow", "Camera"))
        self.action_about.setText(_translate("MainWindow", "About"))

