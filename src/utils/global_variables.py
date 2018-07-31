from networks import resnet_v2
from classifiers import svm_classifier

DETECTOR_MODEL_MAP = {
    'faster_rcnn_inception_resnet_v2_atrous_lowproposals_oid': ("faster_rcnn_inception_resnet_v2_open_images", 600),
    'ssd_mobilenet_v2_coco': ("ssd_mobilenet_v2_coco", 100),
}

FEATURE_EXTRACTOR_MODEL_MAP = {
    'resnet_v2_101': ("resnet_v2_101", 224, resnet_v2.resnet_v2_101, resnet_v2.resnet_arg_scope)
}

CLASSIFIER_MAP = {
    'SVM': ("SVMClassifier", svm_classifier.SVMClassifier)
}

EMBEDDING_SIZE = 1001
FROZEN_MODELS_FOLDER = 'frozen_models'
FROZEN_MODELS_FILE_NAME = 'frozen_inference_graph.pb'
FROZEN_MODELS_LABELS_FILE_NAME = 'frozen_inference_labels.pbtxt'
FROZEN_EMBEDDING_FILE_NAME = r'frozen_embeddings/embeddings'
FEATURE_EXTRACTOR_CHECKPOINT_FILE_NAME = 'model.ckpt'
DATASET_FOLDER = 'dataset'
DATA_PREFIX = 'part_'
MAIN_WINDOW_WIDTH = 800
MAIN_WINDOW_HEIGHT = 600
TRAIN_WINDOW_WIDTH = 551
TRAIN_WINDOW_HEIGHT = 389
TIMER_INTERVAL = 50
TIMER_INTERVAL_DETECT = 1500