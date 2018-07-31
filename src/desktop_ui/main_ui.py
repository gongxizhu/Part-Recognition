from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from desktop_ui.main import *
import cv2
import sys
import numpy as np
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
from utils.global_variables import *
from desktop_ui.train_ui import *

class MainUI(QtWidgets.QMainWindow, Ui_MainWindow):
    __timer_camera = None
    __timer_detect_obj = None
    __cap_camera = None
    __controller = None

    def __init__(self):
        super(MainUI, self).__init__()
        try:
            self.setupUi(self)
            self.__timer_camera = QTimer()
            self.__timer_detect_obj = QTimer()
            self.pbtn_camera_on.clicked.connect(self._pbtn_camera_on_click)
            self.pbtn_camera_off.clicked.connect(self._pbtn_camera_off_click)
            self.pbtn_detect.clicked.connect(self._on_detect)
            self.pbtn_classify.clicked.connect(self._on_classify)
            self.action_quit.triggered.connect(self._quit)
            self.action_train.triggered.connect(self._show_train_window)
            self.__timer_camera.timeout.connect(self._nextFrameSlot_Camera)
            self.__timer_detect_obj.timeout.connect(self._nextFrameSlot_detect)
            # init controller
            self.__controller = service_controller.ServiceControllder()
        except Exception as ex:
            print(ex)

    def _on_classify(self):
        ret, img = self.__cap_camera.read()
        if (ret == True):
            img_new = cv2.resize(img, (TRAIN_WINDOW_WIDTH, TRAIN_WINDOW_HEIGHT), None, 0, 0, cv2.COLOR_BGR2RGB)
            t = threading.Thread(target=self._classify, args=(img_new,))
            t.start()

    def _classify(self, img):
        coordinates = self.__controller.detect(img)
        if len(coordinates.items()) > 0:
            key, coordinate = coordinates.popitem()
            img_cropped = self.__controller.crop(img, coordinate)
            # print(np.asarray(img_cropped, dtype='uint8'))
            class_name, probability = self.__controller.classify(np.asarray(img_cropped, dtype="uint8"))
        else:
            class_name, probability = self.__controller.classify(np.asarray(img, dtype="uint8"))
        self.l_status.setText("Detected " + class_name + " with confidence: " + str(probability))

    def _on_detect(self):
        if self.__cap_camera == None:
            self.__cap_camera = cv2.VideoCapture(0)
        self.__timer_detect_obj.start(TIMER_INTERVAL)
        self.__timer_camera.stop()


    def _nextFrameSlot_detect(self):
        if self.__cap_camera != None:
            ret, img = self.__cap_camera.read()
            if (ret == True):
                img_new = cv2.resize(img, (MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT), None, 0, 0, cv2.COLOR_BGR2RGB)
                height, width, byteValue = img_new.shape
                self.__controller.detect(img_new)
                byteValue = byteValue * width

                qImage = QtGui.QImage(cv2.cvtColor(img_new, cv2.COLOR_BGR2RGB), width, height, byteValue,
                                      QtGui.QImage.Format_RGB888)
                pix = QtGui.QPixmap.fromImage(qImage)
                self.l_video.setPixmap(pix)


    def _quit(self):
        if self.__cap_camera != None:
            self.__cap_camera.release()
        app.exit(1)

    def _show_train_window(self):
        my_dialog = TrainUI(self.__controller)
        my_dialog.exec_()

    def _pbtn_camera_on_click(self):
        try:
            self.pbtn_camera_on.setEnabled(False)
            self.__timer_camera.start(TIMER_INTERVAL)
        except Exception as error:
            print(error.args)


    def _pbtn_camera_off_click(self):
        try:
            if self.__timer_camera != None:
                self.__timer_camera.stop()
            if self.__cap_camera != None:
                self.__cap_camera.release()
            self.pbtn_camera_on.setEnabled(True)
            self.l_video.setPixmap(QtGui.QPixmap(""))
        except Exception as error:
            print(error.args)


    def _nextFrameSlot_Camera(self):
        try:
            if self.__cap_camera == None:
                self.__cap_camera = cv2.VideoCapture(0)
            ret, img = self.__cap_camera.read()
            if(ret == True):
                # smallImg = cv2.resize(self.cvImage, (500, 400), None, 0, 0, cv2.INTER_CUBIC)

                img_new = cv2.resize(img, (MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT), None, 0, 0, cv2.COLOR_BGR2RGB)
                height, width, byteValue = img_new.shape
                byteValue = byteValue * width

                qImage = QtGui.QImage(cv2.cvtColor(img_new, cv2.COLOR_BGR2RGB), width, height, byteValue, QtGui.QImage.Format_RGB888)
                pix = QtGui.QPixmap.fromImage(qImage)
                self.l_video.setPixmap(pix)
            else:
                print(222)
                self.__cap_camera = None
                self.__timer_camera.stop()
                return 0
        except Exception as ex:
            print(ex)
            self.__timer_camera.stop()
            self.__cap_camera.release()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui_Main = MainUI()
    # ui_Main.resize(600, 480)
    ui_Main.show()
    sys.exit(app.exec_())