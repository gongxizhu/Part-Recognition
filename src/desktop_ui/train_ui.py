from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from desktop_ui.main import *
import cv2
import sys
import numpy as np
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
from utils.global_variables import *
from desktop_ui.train import *
from detectors.detector import *
from controllers import service_controller
import threading

class TrainUI(QtWidgets.QDialog, Ui_Dialog):
    __timer_camera = None
    __timer_detect = None
    __cap_camera = None
    __controller = None
    __is_detecting = False
    __count_samples = 0
    __part_number = ''

    def __init__(self, controller):
        super(TrainUI, self).__init__()
        try:
            self.setupUi(self)
            self.__timer_camera = QTimer()
            self.__timer_detect = QTimer()
            self.le_part_number.setPlaceholderText("Part Number")
            self.pbtn_close.clicked.connect(self._close)
            self.pbtn_sample.clicked.connect(self._sample)
            self.pbtn_train.clicked.connect(self._train)
            self.__timer_camera.timeout.connect(self._nextFrameSlot_Camera)
            self.__timer_detect.timeout.connect(self._nextFrameSlot_Detect)
            self.__timer_camera.start(TIMER_INTERVAL)

            self.__controller = controller
        except Exception as ex:
            print(ex)


    def _showWarningMessage(self, msg):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText(msg)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()


    def _sample(self):
        self.__count_samples = 0
        self.__part_number = self.le_part_number.text()
        if self.__part_number != "":
            self.__timer_detect.start(TIMER_INTERVAL_DETECT)
        else:
            self._showWarningMessage("Please input a valid part number")


    def _train(self):
        self.__part_number = self.le_part_number.text()
        if self.__part_number != "":
            class_name = DATA_PREFIX + self.__part_number
            data_dir = self._get_sample_dir(self.__part_number)
            image_paths = [os.path.join(data_dir, image_name) for image_name in os.listdir(data_dir)]
            print(data_dir)
            print(image_paths)
            # self.__controller.train_classifier(image_paths, class_name)
            self.__controller.train_classifier_from_scratch()
        else:
            self._showWarningMessage("Please input a valid part number")


    def _get_sample_dir(self, part_number):
        part_folder_name = DATA_PREFIX + part_number
        sample_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), DATASET_FOLDER, part_folder_name)
        if not os.path.exists(sample_dir):
            os.mkdir(sample_dir)
        # else:
        #     os.rmdir(sample_dir)
        #     os.mkdir(sample_dir)
        return sample_dir


    def _close(self):
        if self.__cap_camera != None:
            self.__cap_camera.release()
        self.close()


    def _nextFrameSlot_Camera(self):
        try:
            if self.__cap_camera == None:
                self.__cap_camera = cv2.VideoCapture(0)
            ret, img = self.__cap_camera.read()
            if(ret == True):
                # smallImg = cv2.resize(self.cvImage, (500, 400), None, 0, 0, cv2.INTER_CUBIC)

                img_new = cv2.resize(img, (TRAIN_WINDOW_WIDTH, TRAIN_WINDOW_HEIGHT), None, 0, 0, cv2.COLOR_BGR2RGB)
                height, width, byteValue = img_new.shape
                byteValue = byteValue * width

                qImage = QtGui.QImage(cv2.cvtColor(img_new, cv2.COLOR_BGR2RGB), width, height, byteValue, QtGui.QImage.Format_RGB888)
                pix = QtGui.QPixmap.fromImage(qImage)
                self.l_video.setPixmap(pix)
            else:
                self.__cap_camera = None
                self.__timer_camera.stop()
                return 0
        except Exception as ex:
            print(ex)
            self.__timer_camera.stop()
            self.__cap_camera.release()


    def _nextFrameSlot_Detect(self):
        if self.__cap_camera != None and not self.__is_detecting:
            ret, img = self.__cap_camera.read()
            if(ret == True):
                self.__is_detecting = True
                img_new = cv2.resize(img, (TRAIN_WINDOW_WIDTH, TRAIN_WINDOW_HEIGHT), None, 0, 0, cv2.COLOR_BGR2RGB)
                #self._detect(img_new)
                t = threading.Thread(target=self._detect, args=(img_new,))
                t.start()


    def _fill_sample_box(self, img):
        try:
            width, height = 130, 76
            img_new = cv2.resize(img, (width, height))
            _, _, byteValue = img_new.shape
            byteValue = byteValue * width
            qImage = QtGui.QImage(cv2.cvtColor(img_new, cv2.COLOR_BGR2RGB), width, height, byteValue, QtGui.QImage.Format_RGB888)
            pix = QtGui.QPixmap.fromImage(qImage)
            if self.__count_samples == 1:
                self.l_img1.setPixmap(pix)
            elif self.__count_samples == 2:
                self.l_img2.setPixmap(pix)
            elif self.__count_samples == 3:
                self.l_img3.setPixmap(pix)
            elif self.__count_samples == 4:
                self.l_img4.setPixmap(pix)
            elif self.__count_samples == 5:
                self.l_img5.setPixmap(pix)
            elif self.__count_samples == 6:
                self.l_img6.setPixmap(pix)
            elif self.__count_samples == 7:
                self.l_img7.setPixmap(pix)
            else:
                self.l_img8.setPixmap(pix)
        except Exception as ex:
            print(ex)

    def _detect(self, img):
        try:
            print('detecting')
            coordinates = self.__controller.detect(img)
            print(coordinates)
            if len(coordinates.items()) > 0:
                if self.__count_samples <= 8:
                    key, coordinate = coordinates.popitem()
                    img_cropped = self.__controller.crop(img, coordinate)
                    self.__count_samples += 1
                    print(key, coordinate)
                    sample_dir = self._get_sample_dir(self.__part_number)
                    file_path = os.path.join(sample_dir,DATA_PREFIX + str(self.__count_samples) + '.jpg')
                    cv2.imwrite(file_path, img_cropped)
                    self._fill_sample_box(img_cropped)
        except Exception as ex:
            print(ex)
        finally:
            self.__is_detecting = False