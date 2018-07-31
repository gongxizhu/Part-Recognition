from feature_extractors.deep_extractor import *
from utils.global_variables import *

def build(feature_extractor_type):
    (ckpt_folder, image_size, network, network_arg_scope) = FEATURE_EXTRACTOR_MODEL_MAP[feature_extractor_type]
    return DeepExtractor(ckpt_folder, image_size, EMBEDDING_SIZE, network, network_arg_scope)