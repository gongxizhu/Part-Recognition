import os
from src.classifiers.keword_classifier import *
from src.utils.global_variables import *

def build():
    model_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), FROZEN_MODELS_FOLDER,
                                KEYWORD_MODEL_FOLDER)
    frozen_graph_path = os.path.join(model_folder, KEYWORD_MODEL)
    label_path = os.path.join(model_folder, KEYWORD_FILE)

    return KeywordClassifier(frozen_graph_path, label_path)