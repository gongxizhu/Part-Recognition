# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from utils.global_variables import *

class Ui_MainWindow(object):
    __timer_camera = None
    __cap_camera = None


    def setupUi(self, MainWindow):
        # UI Components
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 801, 551))
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
        self.pbtn_camera_on = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pbtn_camera_on.setCheckable(False)
        self.pbtn_camera_on.setObjectName("pbtn_camera_on")
        self.horizontalLayout.addWidget(self.pbtn_camera_on)
        self.pbtn_camera_off = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pbtn_camera_off.setObjectName("pbtn_camera_off")
        self.horizontalLayout.addWidget(self.pbtn_camera_off)
        self.pbtn_detect = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pbtn_detect.setObjectName("pbtn_detect")
        self.horizontalLayout.addWidget(self.pbtn_detect)
        self.pbtn_classify = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pbtn_classify.setObjectName("pbtn_classify")
        self.horizontalLayout.addWidget(self.pbtn_classify)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.l_status = QtWidgets.QLabel(self.verticalLayoutWidget)
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
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_train = QtWidgets.QAction(MainWindow)
        self.action_train.setObjectName("action_train")
        self.actionQuit_2 = QtWidgets.QAction(MainWindow)
        self.actionQuit_2.setObjectName("actionQuit_2")
        self.action_quit = QtWidgets.QAction(MainWindow)
        self.action_quit.setObjectName("action_quit")
        self.menuExit.addAction(self.action_train)
        self.menuExit.addSeparator()
        self.menuExit.addAction(self.action_quit)
        self.menubar.addAction(self.menuExit.menuAction())

        # Events
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # Others


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.l_video.setText(_translate("MainWindow", "<html><head/><body><p>Video</p></body></html>"))
        self.pbtn_camera_on.setText(_translate("MainWindow", "Camera On"))
        self.pbtn_camera_off.setText(_translate("MainWindow", "Camera Off"))
        self.pbtn_detect.setText(_translate("MainWindow", "Detect"))
        self.pbtn_classify.setText(_translate("MainWindow", "Recognize"))
        self.l_status.setText(_translate("MainWindow", "<html><head/><body><p>status</p></body></html>"))
        self.menuExit.setTitle(_translate("MainWindow", "File"))
        self.action_train.setText(_translate("MainWindow", "Train"))
        self.actionQuit_2.setText(_translate("MainWindow", "Quit"))
        self.action_quit.setText(_translate("MainWindow", "Quit"))

