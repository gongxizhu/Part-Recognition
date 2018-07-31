import os
import math
import pickle
import numpy as np
import tensorflow as tf
import tensorflow.contrib.slim as slim
from tensorflow.python.platform import gfile
from src.utils import inception_preprocessing
from src.utils.global_variables import *


os.environ["CUDA_VISIBLE_DEVICES"] = '1'


class DeepExtractor():
    __embeddings = None
    __image_size = 0
    __embedding_size = 0
    __images_placeholder = None
    __batch_size = 10
    __graph = None

    def __init__(self, ckpt_folder, image_size, embedding_size, network, network_arg_scope):
        ckpt_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), FROZEN_MODELS_FOLDER, ckpt_folder)
        self.__ckpt_dir = ckpt_dir
        print(ckpt_dir)
        self._load_model_from_file(ckpt_dir, image_size, embedding_size, network, network_arg_scope)

    def _load_model_from_file(self, ckpt_dir, image_size, embedding_size, network, network_arg_scope):
        self.__image_size = image_size
        self.__embedding_size = embedding_size
        with tf.Graph().as_default():
            with tf.Session() as sess:
                self.__images_placeholder = tf.placeholder(tf.float32, [None, image_size, image_size, 3])
                with slim.arg_scope(network_arg_scope()):
                    prelogits, _ = network(self.__images_placeholder, num_classes=embedding_size,
                                                         is_training=False, reuse=tf.AUTO_REUSE)
                self.__embeddings = tf.nn.l2_normalize(prelogits, 1, 1e-10, name='embeddings')

                saver = tf.train.Saver()
                saver.restore(sess, os.path.join(ckpt_dir, FEATURE_EXTRACTOR_CHECKPOINT_FILE_NAME))
                self.__graph = sess.graph

    def encode(self, image):
        images = np.zeros((1, self.__image_size, self.__image_size, 3))
        image = tf.convert_to_tensor(image, dtype=tf.uint8)
        emb_array = np.zeros((1, self.__embedding_size))
        with tf.Session() as sess:
            processed_image = inception_preprocessing.preprocess_image(image, self.__image_size, self.__image_size, is_training=False)
            processed_image = processed_image.eval()
            processed_image = self._prewhiten(processed_image)
            images[0, :, :, :] = processed_image
        with tf.Session(graph=self.__graph) as sess:
            saver = tf.train.Saver()
            saver.restore(sess, os.path.join(self.__ckpt_dir, FEATURE_EXTRACTOR_CHECKPOINT_FILE_NAME))
            feed_dict = {self.__images_placeholder: images}
            emb_array[0, :] = sess.run(self.__embeddings, feed_dict=feed_dict)

        return emb_array

    def batch_encode(self, image_paths):
        # image_paths = os.listdir(image_dir)
        nr_of_images = len(image_paths)
        nr_of_batches_per_epoch = int(math.ceil(1.0 * nr_of_images / self.__batch_size))
        emb_array = np.zeros((nr_of_images, self.__embedding_size))
        with tf.Session(graph=self.__graph) as sess:
            saver = tf.train.Saver()
            saver.restore(sess, os.path.join(self.__ckpt_dir, FEATURE_EXTRACTOR_CHECKPOINT_FILE_NAME))
            for i in range(nr_of_batches_per_epoch):
                start_index = i * self.__batch_size
                end_index = min((i + 1) * self.__batch_size, nr_of_images)
                paths_batch = image_paths[start_index:end_index]
                images = self._load_images(paths_batch, False, False, self.__image_size)
                print(np.shape(images))
                feed_dict = {self.__images_placeholder: images}
                emb_array[start_index:end_index, :] = sess.run(self.__embeddings, feed_dict=feed_dict)

        return emb_array

    def _load_images(self, image_paths, do_random_crop, do_random_flip, image_size, do_prewhiten=True):
        nr_of_samples = len(image_paths)
        images = np.zeros((nr_of_samples, image_size, image_size, 3))
        output_list = []
        print(nr_of_samples)
        for i in range(nr_of_samples):
            img = tf.image.decode_jpeg(tf.read_file(image_paths[i]), channels=3)
            processed_image = inception_preprocessing.preprocess_image(img, image_size, image_size, is_training=False)
            processed_image = processed_image.eval()
            if do_prewhiten:
                processed_image = self._prewhiten(processed_image)
            output_list.append(processed_image)
            images[i, :, :, :] = processed_image

        return images

    def _to_rgb(self, img):
        w, h = img.shape
        ret = np.empty((w, h, 3), dtype=np.uint8)
        ret[:, :, 0] = ret[:, :, 1] = ret[:, :, 2] = img
        return ret

    def _flip(self, image, random_flip):
        if random_flip and np.random.choice([True, False]):
            image = np.fliplr(image)
        return image

    def _prewhiten(self, x):
        mean = np.mean(x)
        std = np.std(x)
        std_adj = np.maximum(std, 1.0 / np.sqrt(x.size))
        y = np.multiply(np.subtract(x, mean), 1 / std_adj)
        return y