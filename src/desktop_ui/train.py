# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'train.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(669, 561)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 671, 561))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.l_video = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.l_video.setText("")
        self.l_video.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.l_video.setObjectName("l_video")
        self.verticalLayout_3.addWidget(self.l_video)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.l_img1 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.l_img1.sizePolicy().hasHeightForWidth())
        self.l_img1.setSizePolicy(sizePolicy)
        self.l_img1.setStyleSheet("border:1px solid black;")
        self.l_img1.setIndent(-1)
        self.l_img1.setObjectName("l_img1")
        self.horizontalLayout_2.addWidget(self.l_img1)
        self.l_img2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.l_img2.setStyleSheet("border:1px solid black;")
        self.l_img2.setObjectName("l_img2")
        self.horizontalLayout_2.addWidget(self.l_img2)
        self.l_img3 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.l_img3.setStyleSheet("border:1px solid black;")
        self.l_img3.setObjectName("l_img3")
        self.horizontalLayout_2.addWidget(self.l_img3)
        self.l_img4 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.l_img4.setStyleSheet("border:1px solid black;")
        self.l_img4.setObjectName("l_img4")
        self.horizontalLayout_2.addWidget(self.l_img4)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.l_img5 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.l_img5.setStyleSheet("border:1px solid black;")
        self.l_img5.setObjectName("l_img5")
        self.horizontalLayout_3.addWidget(self.l_img5)
        self.l_img6 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.l_img6.setStyleSheet("border:1px solid black;")
        self.l_img6.setObjectName("l_img6")
        self.horizontalLayout_3.addWidget(self.l_img6)
        self.l_img7 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.l_img7.setStyleSheet("border:1px solid black;")
        self.l_img7.setObjectName("l_img7")
        self.horizontalLayout_3.addWidget(self.l_img7)
        self.l_img8 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.l_img8.setStyleSheet("border:1px solid black;")
        self.l_img8.setObjectName("l_img8")
        self.horizontalLayout_3.addWidget(self.l_img8)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.pb_train = QtWidgets.QProgressBar(self.horizontalLayoutWidget)
        self.pb_train.setStyleSheet("QProgressBar {\n"
"    border: 2px bold grey;\n"
"    border-radius: 5px;\n"
"    text-align: center\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: rgb(23, 96, 255);\n"
"    width: 5px;\n"
"    margin: 1px;\n"
"}")
        self.pb_train.setProperty("value", 0)
        self.pb_train.setTextVisible(True)
        self.pb_train.setInvertedAppearance(False)
        self.pb_train.setObjectName("pb_train")
        self.verticalLayout_3.addWidget(self.pb_train)
        self.verticalLayout_3.setStretch(0, 5)
        self.verticalLayout_3.setStretch(1, 1)
        self.verticalLayout_3.setStretch(2, 1)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.le_part_number = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.le_part_number.setMinimumSize(QtCore.QSize(0, 20))
        self.le_part_number.setStyleSheet("QLineEdit {\n"
"    font: 12pt \"Calibri\";\n"
"    color: #555;\n"
"    background-color:#fff;\n"
"    border: 1px solid #ccc;\n"
"    border-radius:4px;\n"
"}")
        self.le_part_number.setInputMask("")
        self.le_part_number.setObjectName("le_part_number")
        self.verticalLayout.addWidget(self.le_part_number)
        self.pbtn_sample = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pbtn_sample.setMinimumSize(QtCore.QSize(0, 20))
        self.pbtn_sample.setStyleSheet("QPushButton {\n"
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
        self.pbtn_sample.setObjectName("pbtn_sample")
        self.verticalLayout.addWidget(self.pbtn_sample)
        self.pbtn_train = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pbtn_train.setMinimumSize(QtCore.QSize(0, 20))
        self.pbtn_train.setStyleSheet("QPushButton {\n"
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
        self.pbtn_train.setObjectName("pbtn_train")
        self.verticalLayout.addWidget(self.pbtn_train)
        self.pbtn_close = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pbtn_close.setMinimumSize(QtCore.QSize(0, 20))
        self.pbtn_close.setStyleSheet("QPushButton {\n"
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
        self.pbtn_close.setObjectName("pbtn_close")
        self.verticalLayout.addWidget(self.pbtn_close)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.l_info = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.l_info.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(255, 255, 255, 255));\n"
"border: 1px solid darkgrey;")
        self.l_info.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.l_info.setObjectName("l_info")
        self.verticalLayout_2.addWidget(self.l_info)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 1)
        self.verticalLayout.setStretch(4, 1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.setStretch(0, 5)
        self.horizontalLayout.setStretch(1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.l_img1.setText(_translate("Dialog", "1"))
        self.l_img2.setText(_translate("Dialog", "2"))
        self.l_img3.setText(_translate("Dialog", "3"))
        self.l_img4.setText(_translate("Dialog", "4"))
        self.l_img5.setText(_translate("Dialog", "5"))
        self.l_img6.setText(_translate("Dialog", "6"))
        self.l_img7.setText(_translate("Dialog", "7"))
        self.l_img8.setText(_translate("Dialog", "8"))
        self.le_part_number.setText(_translate("Dialog", "Part Number"))
        self.pbtn_sample.setText(_translate("Dialog", "Sample"))
        self.pbtn_train.setText(_translate("Dialog", "Train"))
        self.pbtn_close.setText(_translate("Dialog", "Close"))
        self.l_info.setText(_translate("Dialog", "Information"))

