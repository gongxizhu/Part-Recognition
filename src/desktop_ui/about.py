# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_About(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.ptb_ok = QtWidgets.QPushButton(Dialog)
        self.ptb_ok.setGeometry(QtCore.QRect(160, 260, 75, 23))
        self.ptb_ok.setObjectName("ptb_ok")
        self.l_version = QtWidgets.QLabel(Dialog)
        self.l_version.setGeometry(QtCore.QRect(30, 30, 241, 21))
        self.l_version.setStyleSheet("QLabel{\n"
"    font: 12pt \"Calibri\";\n"
"}")
        self.l_version.setObjectName("l_version")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.ptb_ok.setText(_translate("Dialog", "OK"))
        self.l_version.setText(_translate("Dialog", "Version 1.0"))

