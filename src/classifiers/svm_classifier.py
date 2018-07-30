import pickle
import numpy as np
import os
from sklearn.svm import SVC
#from utils.global_variables import *

class SVMClassifier():
    __model = None
    __class_names= None
    __classifier_file_name = None
    __model_path = None

    def __init__(self, model_file_name, frozen_folder):
        self.__model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), frozen_folder, model_file_name)
        print(self.__model_path)
        if(os.path.exists(self.__model_path)):
            self._load_model()
        else:
            self.__model = SVC(kernel='linear', probability=True)


    def train(self, emb_array, labels, class_names):
        self.__class_names = class_names
        self.__model.fit(emb_array, labels)
        with open(self.__model_path, 'wb') as outfile:
            pickle.dump((self.__model, self.__class_names), outfile)

    def evaluate(self, emb_array_test, labels_test, class_names):
        self.__class_names = class_names
        predictions = self.__model.predict(emb_array_test)
        best_class_indices = np.argmax(predictions, axis=1)
        best_class = [self.__class_names[i] for i in best_class_indices]
        accuracy = np.mean(best_class == labels_test)

        return accuracy

    def classify(self, embedding, class_names):
        self.__class_names = class_names
        emb_array = embedding
        predictions = self.__model.predict_proba(emb_array)
        print(predictions)
        print(self.__class_names)
        best_class_indices = np.argmax(predictions, axis=1)
        best_class_probabilities = predictions[np.arange(len(best_class_indices)), best_class_indices]
        print(best_class_probabilities)
        class_and_proba = [(self.__class_names[i], best_class_probabilities[0]) for i in best_class_indices]
        return class_and_proba

    def classify_batch(self, emb_array, class_names):
        self.__class_names = class_names
        predictions = self.__model.predict_proba(emb_array)
        best_class_indices = np.argmax(predictions, axis=1)
        best_class_probabilities = predictions[np.arange(len(best_class_indices)), best_class_indices]
        class_and_proba = [(self.__class_names[i], best_class_probabilities[i]) for i in best_class_indices]
        return class_and_proba

    def _load_model(self):
        with open(self.__model_path, 'rb') as infile:
            (self.__model, self.__class_names) = pickle.load(infile)