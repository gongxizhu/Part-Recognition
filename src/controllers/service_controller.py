from src.detectors import detector
from src.builders import detector_builder
from src.builders import feature_extractor_builder
from src.builders import classifier_builder
from src.builders import keyword_classifier_builder
from src.utils.global_variables import *
import cv2
import os
import pickle

class ServiceControllder():
    __detector = None
    __feature_extractor = None
    __classifier = None
    __keyword_classifier = None
    __emb_array = []
    __class_names = []
    __labels = []


    def __init__(self):
        #self.__detector = detector_builder.build('faster_rcnn_inception_resnet_v2_atrous_lowproposals_oid')
        self.__detector = detector_builder.build("ssd_mobilenet_v2_coco")
        self.__feature_extractor = feature_extractor_builder.build('resnet_v2_101')
        self.__classifier = classifier_builder.build('SVM')
        # self.__keyword_classifier = keyword_classifier_builder.build()


    def _load_pretrained_embeddings(self):
        file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), FROZEN_EMBEDDING_FILE_NAME)
        with open(file_path, 'rb') as infile:
            (self.__emb_array, self.__class_names, self.__labels) = pickle.load(infile)


    def read_word(self, voice_string):
        return self.__keyword_classifier.read_word(voice_string)


    def detect(self, image):
        coordinates = self.__detector.detect(image)
        return coordinates


    def crop(self, image, coordinate):
        img_cropped = self.__detector.crop(image, coordinate)
        return img_cropped


    def classify(self, image):
        embedding = self.__feature_extractor.encode(image)
        _, _, _, self.__class_names = self._load_dataset()
        results = self.__classifier.classify(embedding, self.__class_names)
        (class_name, probability) = results[0]
        return class_name, probability

    def train_classifier(self, image_paths, class_name):
        file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), FROZEN_EMBEDDING_FILE_NAME)
        print(file_path)
        self._load_pretrained_embeddings()
        print(self.__class_names)
        print(self.__labels)
        self.__class_names.append(class_name)
        emb_array = self.__feature_extractor.batch_encode(image_paths)
        for embedding in emb_array:
            self.__emb_array.append(embedding)
            self.__labels.append(class_name)
        self.__classifier.train(self.__emb_array, self.__labels, self.__class_names)
        with open(file_path, 'wb') as outfile:
            pickle.dump((self.__emb_array, self.__labels, self.__class_names), outfile)
        print('Training completes!')


    def train_classifier_from_scratch(self):
        file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), FROZEN_EMBEDDING_FILE_NAME)
        nr_of_images, image_paths, labels, class_names = self._load_dataset()
        emb_array = self.__feature_extractor.batch_encode(image_paths)
        self.__classifier.train(emb_array, labels, class_names)
        with open(file_path, 'wb') as outfile:
            pickle.dump((nr_of_images, image_paths, labels, class_names), outfile)
        print('Training completes!')


    def _load_dataset(self):
        dataset_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), DATASET_FOLDER, 'train')
        sub_folder_array = [sub_folder for sub_folder in os.listdir(dataset_dir)]
        image_paths = []
        labels = []
        class_names = []
        for sub_folder in sub_folder_array:
            class_name = sub_folder
            sub_folder_path = os.path.join(dataset_dir, sub_folder)
            for image_name in os.listdir(sub_folder_path):
                image_path = os.path.join(dataset_dir, sub_folder, image_name)
                image_paths.append(image_path)
                labels.append(class_name)
            class_names.append(class_name)

        nr_of_images = len(image_paths)

        return nr_of_images, image_paths, labels, class_names




# if __name__ == '__main__':
#     controller = ServiceControllder()
#     controller.train_classifier_from_scratch()
    # print('Cropping images')
    # print(coordinates)
    # if(coordinates.__len__() > 0):
    #     for item in coordinates.items():
    #         (key, coordinate) = item
    #         print(coordinate)
    #         detector.crop(img, coordinate)
    #     while True:
    #         if cv2.waitKey(25) & 0xFF == ord('q'):
    #             cv2.destroyAllWindows()
    #             break
    print('End!')
    # print(coordinates)