from classifiers.svm_classifier import *
from utils.global_variables import *

def build(classifier_type):
    (model_file_name, classifier_constructor) = CLASSIFIER_MAP[classifier_type]
    return classifier_constructor(model_file_name, FROZEN_MODELS_FOLDER)