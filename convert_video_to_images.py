import os
import sys
import tensorflow as tf
import cv2
import numpy as np
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw

sys.path.append("..")
from google.protobuf import text_format
import src.utils.visualization as vis_util
from object_detection.protos import string_int_label_map_pb2
import argparse


def load_labelmap(path):
    with tf.gfile.GFile(path, 'r') as fid:
        label_map_string = fid.read()
        label_map = string_int_label_map_pb2.StringIntLabelMap()
        try:
            text_format.Merge(label_map_string, label_map)
        except text_format.ParseError:
            label_map.ParseFromString(label_map_string)
    validate_label_map(label_map)

    return label_map


def validate_label_map(label_map):
    for item in label_map.item:
        if item.id < 0:
            raise ValueError('Label map ids should be >= 0.')
        if (item.id == 0 and item.name != 'background' and
                    item.display_name != 'background'):
            raise ValueError('Label map id 0 is reserved for the background label')


def convert_label_map_to_categories(label_map, max_num_classes, use_display_name=True):
    categories = []
    list_of_ids_already_added = []
    if not label_map:
        label_id_offset = 1
        for class_id in range(max_num_classes):
            categories.append({
                'id': class_id + label_id_offset,
                # 'name': 'category_{}'.format(class_id + label_id_offset)
                'name': 'Part'
            })
        return categories
    for item in label_map.item:
        if not 0 < item.id <= max_num_classes:
            print('Ignore item %d since it falls outside of requested '
                  'label range.', item.id)
            continue
        if use_display_name and item.HasField('display_name'):
            name = item.display_name
        else:
            name = item.name
        if item.id not in list_of_ids_already_added:
            list_of_ids_already_added.append(item.id)
            #categories.append({'id': item.id, 'name': name})
            categories.append({'id': item.id, 'name': 'Part'})
    return categories


def create_category_index(categories):
    category_index = {}
    for cat in categories:
        category_index[cat['id']] = cat
    return category_index


def show_video(video_path, target_path, frozen_model_path, labels_path, num_per_step = 2, num_classes=100):
    #print(video_path)
    if not os.path.exists(video_path):
        raise ValueError("Not a valid path")
    video_list = [video_name for video_name in os.listdir(video_path) if video_name.endswith('mp4')]
    # for video_name in video_list:
    #     class_name = video_name.replace('p', 'part_', 1).replace('.mp4', '')
    #     print(class_name)
    # return
    label_map = load_labelmap(labels_path)
    categories = convert_label_map_to_categories(label_map, max_num_classes=num_classes, use_display_name=True)
    category_index = create_category_index(categories)
    current_box_coordinates = {}
    with tf.Graph().as_default() as detection_graph:
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(frozen_model_path, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

        with tf.Session(graph=detection_graph) as sess:
            for video_name in video_list:
                class_name = video_name.replace('p', 'part_', 1).replace('.mp4', '')
                target_folder = os.path.join(target_path, class_name)
                video_file_path = os.path.join(video_path, video_name)
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)
                cap = cv2.VideoCapture(video_file_path)
                frame_num = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                y, x, y_max, x_max = 0, 0, 0, 0
                suffix_index = 1
                for index in range(int(frame_num)):
                    ret, image_np = cap.read()
                    if (ret == False):
                        break
                    # image_np = cv2.transpose(image_np);
                    # image_np = cv2.flip(image_np, 1);
                    image_np = cv2.resize(image_np, (800, 600), None, 0, 0, cv2.INTER_CUBIC)
                    image_ori = image_np.copy()
                    image_to_save = image_ori
                    if index % num_per_step == 0:
                        image_np_expanded = np.expand_dims(image_np, axis=0)
                        boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                        scores = detection_graph.get_tensor_by_name('detection_scores:0')
                        classes = detection_graph.get_tensor_by_name('detection_classes:0')
                        num_detections = detection_graph.get_tensor_by_name('num_detections:0')
                        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                        (boxes, scores, classes, num_detections) = sess.run(
                            [boxes, scores, classes, num_detections],
                            feed_dict={image_tensor: image_np_expanded})
                        image_new, box_coordinates = vis_util.visualize_boxes_and_labels_on_image_array(
                            image_np,
                            np.squeeze(boxes),
                            np.squeeze(classes).astype(np.int32),
                            np.squeeze(scores),
                            category_index,
                            use_normalized_coordinates=True,
                            line_thickness=8)
                        current_image = image_np
                    if len(box_coordinates) > 0:
                        current_box_coordinates = box_coordinates
                        # print(coordinates.popitem())
                        _, (y, x ,y_max, x_max) = current_box_coordinates.popitem()
                        x = int(x * 800)
                        x_max = int(x_max * 800)
                        y = int(y * 600)
                        y_max = int(y_max * 600)
                        #print(x, y , x_max, y_max)
                        image_to_save = image_ori[y:y_max, x:x_max]
                    if index % num_per_step == 0:
                        image_file_name = os.path.join(target_folder, 'part_' + str(suffix_index) + '.jpg')
                        print(image_file_name)
                        cv2.imwrite(image_file_name, image_to_save)
                        suffix_index += 1
                    cv2.rectangle(image_ori, (x, y), (x_max, y_max), (0, 0, 255), 2)
                    cv2.imshow('object detection', cv2.resize(image_ori, (800, 600)))
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        cv2.destroyAllWindows()
                        break


if __name__ == '__main__':
    video_path = os.path.join(r'C:\my_repo\Part-Recognition\videos')
    target_path = os.path.join(r'C:\my_repo\Part-Recognition\raw_data')
    frozen_model_path = os.path.join(r'C:\my_repo\Part-Recognition\frozen_models\ssd_mobilenet_v2_coco',
                                     'frozen_inference_graph.pb')
    labels_path = os.path.join(r'C:\my_repo\Part-Recognition\frozen_models\ssd_mobilenet_v2_coco',
                               'frozen_inference_labels.pbtxt')
    show_video(video_path, target_path, frozen_model_path, labels_path)
