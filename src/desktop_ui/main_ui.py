from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from main import *
import cv2
import sys
import numpy as np
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
from src.utils.global_variables import *
from train_ui import *
from about_ui import *
#from src.controllers.audio_reader import *
#import wave
#from pyaudio import PyAudio, paInt16


class MainUI(QtWidgets.QMainWindow, Ui_MainWindow):
    __timer_camera = None
    __timer_detect_obj = None
    __timer_audio = None
    __cap_camera = None
    __controller = None
    __audio_reader = None
    __last_word = ''
    __current_image = []
    __current_box_coordinates = {}

    def __init__(self):
        super(MainUI, self).__init__()
        try:
            self.setupUi(self)
            self.__timer_camera = QTimer()
            self.__timer_detect_obj = QTimer()
            # self.__timer_audio = QTimer()
            # self.pbtn_camera_on.clicked.connect(self._pbtn_camera_on_click)
            # self.pbtn_camera_off.clicked.connect(self._pbtn_camera_off_click)
            self.pbtn_detect.clicked.connect(self._on_detect)
            self.pbtn_classify.clicked.connect(self._on_classify)
            self.action_quit.triggered.connect(self._quit)
            self.action_train.triggered.connect(self._show_train_window)
            self.action_camera.triggered.connect(self._switch_camera)
            self.action_about.triggered.connect(self._show_about_window)
            self.l_video.mousePressEvent = self._on_l_video_click
            self.__timer_camera.timeout.connect(self._nextFrameSlot_Camera)
            self.__timer_detect_obj.timeout.connect(self._nextFrameSlot_detect)
            # self.__timer_audio.timeout.connect(self._nextFrameSlot_audio)
            # init controller
            self.__controller = service_controller.ServiceControllder()
            # self.__audio_reader = AudioReader()
            #self.__timer_audio.start(3000)
        except Exception as ex:
            print(ex)

    def _on_l_video_click(self, event):
        try:
            if event.button() == 1 and len(self.__current_image) > 0:
                x = event.pos().x()
                y = event.pos().y()
                print(x, y)
                refPt = [x, y]
                image_pil = Image.fromarray(self.__current_image)
                im_width, im_height = image_pil.size
                (left_f, right_f, top_f, bottom_f) = (0, 0, 0, 0)
                area_min = 0.0
                for key, item in self.__current_box_coordinates.items():
                    #(key, item) = coordinate
                    (ymin, xmin, ymax, xmax) = item
                    (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                                  ymin * im_height, ymax * im_height)
                    area = (right - left) * (top - bottom)
                    if area_min == 0.0:
                        area_min = area
                        (left_f, right_f, top_f, bottom_f) = (left, right, top, bottom)

                    if x > left and x < right and y < top and y > bottom and area < area_min:
                        (left_f, right_f, top_f, bottom_f) = (left, right, top, bottom)
                print(left_f, right_f, top_f, bottom_f)
                roi = self.__current_image[int(top_f):int(bottom_f), int(left_f):int(right_f)]
                cv2.destroyWindow("ROI")
                cv2.imshow("ROI", roi)
                t = threading.Thread(target=self._classify_by_click, args=(roi,))
                t.start()
                #self._classify_by_click(roi)
        except Exception as error:
            print(error.args)


    def _on_classify(self):
        ret, img = self.__cap_camera.read()
        if ret == True:
            img_new = cv2.resize(img, (TRAIN_WINDOW_WIDTH, TRAIN_WINDOW_HEIGHT), None, 0, 0, cv2.COLOR_BGR2RGB)
            t = threading.Thread(target=self._classify, args=(img_new,))
            t.start()

    def _switch_camera(self):
        if self.action_camera.isChecked():
            self._pbtn_camera_on_click()
        else:
            self._pbtn_camera_of_click()

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


    def _classify_by_click(self, img):
        class_name, probability = self.__controller.classify(np.asarray(img, dtype="uint8"))
        self.l_status.setText(class_name + ", confidence: " + str(probability))


    def _on_detect(self):
        if self.__cap_camera == None:
            self.__cap_camera = cv2.VideoCapture(0)
        # self.__timer_detect_obj.start(TIMER_INTERVAL)
        self.__timer_detect_obj.start(100)
        self.__timer_camera.stop()


    def _nextFrameSlot_detect(self):
        if self.__cap_camera == None:
            self.__cap_camera = cv2.VideoCapture(0)
        if self.__cap_camera != None:
            ret, img = self.__cap_camera.read()
            if (ret == True):
                img_new = cv2.resize(img, (MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT), None, 0, 0, cv2.COLOR_BGR2RGB)
                height, width, byteValue = img_new.shape
                self.__current_image = img_new
                box_coordinates = self.__controller.detect(img_new)
                self.__current_box_coordinates = box_coordinates
                byteValue = byteValue * width

                qImage = QtGui.QImage(cv2.cvtColor(img_new, cv2.COLOR_BGR2RGB), width, height, byteValue,
                                      QtGui.QImage.Format_RGB888)
                pix = QtGui.QPixmap.fromImage(qImage)
                self.l_video.setPixmap(pix)


    def _nextFrameSlot_audio(self):
        try:
            wav_data = self.__audio_reader.read_audio()
            self._save_wav(wav_data, "./keywords.wav")
            with open(r"./keywords.wav", 'rb') as wav_file:
                wav_data_tf = wav_file.read()
            word, score = self.__controller.read_word(wav_data_tf)
            if word == 'visual' and self.__last_word == 'visual' and score > 0.7:
                self._show_train_window()
            self.__last_word = word
        except Exception as error:
            print(error.args)


    def _save_wav(self, voice_string, filename):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(self.__audio_reader.sampling_rate)
        wf.writeframes(np.array(voice_string).tostring())
        wf.close()

    def _quit(self):
        if self.__cap_camera != None:
            self.__cap_camera.release()
        app.exit(1)

    def _show_train_window(self):
        my_dialog = TrainUI(self.__controller)
        my_dialog.exec_()

    def _show_about_window(self):
        my_dialog = AboutUI()
        my_dialog.exec_()

    def _pbtn_camera_on_click(self):
        try:
            #self.pbtn_camera_on.setEnabled(False)
            self.__timer_camera.start(TIMER_INTERVAL)
        except Exception as error:
            print(error.args)


    def _pbtn_camera_off_click(self):
        try:
            if self.__timer_camera != None:
                self.__timer_camera.stop()
            if self.__cap_camera != None:
                self.__cap_camera.release()
            #self.pbtn_camera_on.setEnabled(True)
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
                self.__cap_camera = None
                self.__timer_camera.stop()
                return 0
        except Exception as ex:
            print(ex)
            self.__timer_camera.stop()
            self.__cap_camera.release()

    '''
    def _click_and_crop(self, event, x, y, flags, param):
        # grab references to the global variables
        global refPt, cropping
        # print(111)
        # if the left mouse button was clicked, record the starting
        # (x, y) coordinates and indicate that cropping is being
        # performed
        if event == cv2.EVENT_LBUTTONDOWN:
            refPt = [x, y]
            cv2.destroyWindow("ROI")
            cropping = True

        # check to see if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
            # record the ending (x, y) coordinates and indicate that
            # the cropping operation is finished
            refPt = [x, y]
            image_pil = Image.fromarray(self.__current_image)
            im_width, im_height = image_pil.size
            (key, item) = self.__current_box_coordinates.popitem()
            print(item)
            (ymin, xmin, ymax, xmax) = item
            (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                          ymin * im_height, ymax * im_height)
            if self._is_in_box(x, y, ymin, xmin, ymax, xmax):
                # roi = image_pil.crop((left, right, top, bottom))
                print(left, right, top, bottom)
                roi = self.__current_image[int(top):int(bottom), int(left):int(right)]
                cv2.imshow("ROI", roi)
            print(refPt)
            cropping = False
    '''


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui_Main = MainUI()
    # ui_Main.resize(600, 480)
    ui_Main.show()
    sys.exit(app.exec_())