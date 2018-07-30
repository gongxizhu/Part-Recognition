from src.detectors.detector import *
from src.utils.global_variables import *

def build(detector_type):
    (model_folder, num_of_class) = DETECTOR_MODEL_MAP[detector_type]
    model_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), FROZEN_MODELS_FOLDER, model_folder)
    return Detector(model_folder, num_of_class)