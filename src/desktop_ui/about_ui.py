from PyQt5 import QtCore, QtGui, QtWidgets
from about import Ui_Dialog_About


class AboutUI(QtWidgets.QDialog, Ui_Dialog_About):

    def __init__(self):
        super(AboutUI, self).__init__()
        self.setupUi(self)