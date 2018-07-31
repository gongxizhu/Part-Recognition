import os
import PIL.Image as Image
import cv2
import numpy as np
import tensorflow as tf
from google.protobuf import text_format
from protobufs import string_int_label_map_pb2
from utils.global_variables import *
# sys.path.append("..")
from utils import visualization as vis_util


class Detector():
    __detection_graph = None
    __category_index = None

    def __init__(self, model_folder_path, num_of_class):
        self.__detection_graph = tf.Graph()
        #frozen_models_dir, _ = os.path.join(os.path.dirname(os.path.dirname(__file__)), FROZEN_MODELS_FOLDER)
        model_path = os.path.join(model_folder_path, FROZEN_MODELS_FILE_NAME)
        labels_path = os.path.join(model_folder_path, FROZEN_MODELS_LABELS_FILE_NAME)
        print(model_path, labels_path, model_folder_path)
        print('Loading Model...')
        with self.__detection_graph.as_default():
            self._load_model_from_file(model_path)
            label_map = self._load_labelmap(labels_path)
            categories = self._convert_label_map_to_categories(label_map, max_num_classes=num_of_class, use_display_name=True)
            self.__category_index = self._create_category_index(categories)

    def _load_model_from_file(self, frozen_model_path):
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(frozen_model_path, 'rb') as fid:
            od_graph_def.ParseFromString(fid.read())
            tf.import_graph_def(od_graph_def, name='')

    def _load_labelmap(self, path):
        with tf.gfile.GFile(path, 'r') as fid:
            label_map_string = fid.read()
            label_map = string_int_label_map_pb2.StringIntLabelMap()
            try:
                text_format.Merge(label_map_string, label_map)
            except text_format.ParseError:
                label_map.ParseFromString(label_map_string)

        return label_map

    def _convert_label_map_to_categories(self, label_map, max_num_classes, use_display_name=True):
        categories = []
        list_of_ids_already_added = []
        if not label_map:
            label_id_offset = 1
            for class_id in range(max_num_classes):
                categories.append({
                    'id': class_id + label_id_offset,
                    'name': 'category_{}'.format(class_id + label_id_offset)
                })
            return categories
        for item in label_map.item:
            if not 0 < item.id <= max_num_classes:
                continue
            if use_display_name and item.HasField('display_name'):
                name = item.display_name
            else:
                name = item.name
            if item.id not in list_of_ids_already_added:
                list_of_ids_already_added.append(item.id)
                categories.append({'id': item.id, 'name': name})

        return categories

    def _create_category_index(self, categories):
        category_index = {}
        for cat in categories:
            category_index[cat['id']] = cat

        return category_index

    def detect(self, image):
        with self.__detection_graph.as_default():
            with tf.Session(graph=self.__detection_graph) as sess:
                image_expanded = np.expand_dims(image, axis=0)
                boxes = self.__detection_graph.get_tensor_by_name('detection_boxes:0')
                scores = self.__detection_graph.get_tensor_by_name('detection_scores:0')
                classes = self.__detection_graph.get_tensor_by_name('detection_classes:0')
                num_detections = self.__detection_graph.get_tensor_by_name('num_detections:0')
                image_tensor = self.__detection_graph.get_tensor_by_name('image_tensor:0')
                print('Start Inference...')
                (boxes, scores, classes, num_detections) = sess.run(
                    [boxes, scores, classes, num_detections],
                    feed_dict={image_tensor: image_expanded})

                image_processed, box_coordinates = vis_util.visualize_boxes_and_labels_on_image_array(
                    image,
                    np.squeeze(boxes),
                    np.squeeze(classes).astype(np.int32),
                    np.squeeze(scores),
                    self.__category_index,
                    use_normalized_coordinates=True,
                    line_thickness=8)

                return box_coordinates

    def crop(self, image, coordinates):
        image_pil = Image.fromarray(image)
        im_width, im_height = image_pil.size
        (ymin, xmin, ymax, xmax) = coordinates
        (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                      ymin * im_height, ymax * im_height)
        cropped_img = image[int(top):int(bottom), int(left):int(right)]
        # cv2.imshow("cropped", cropped_img)
        return cropped_img
