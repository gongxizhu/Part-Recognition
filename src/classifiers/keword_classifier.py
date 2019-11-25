import tensorflow as tf
from tensorflow.contrib.framework.python.ops import audio_ops as contrib_audio


sampling_rate = 8000
frozen_graph = r'C:\Tensorflow1.8\speech_command\speech_commands_train\frozen_graph.pb'
label_path = r'C:\Tensorflow1.8\speech_command\speech_commands_train\conv_labels.txt'


class KeywordClassifier(object):
    cap = None
    off = False


    def __init__(self, frozen_graph_path, label_path):
        self._load_labels(label_path)
        print(self.labels)
        self._load_graph(frozen_graph_path)
        self.sess = tf.Session(graph=tf.get_default_graph())


    def _load_graph(self, filename):
        with tf.gfile.FastGFile(filename, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            tf.import_graph_def(graph_def, name='')


    def _load_labels(self, filename):
        self.labels = [line.rstrip() for line in tf.gfile.GFile(filename)]


    def read_word(self, voice_string):
        return self._run_graph(voice_string)


    def _run_graph(self, wav_data, input_layer_name = "wav_data:0", output_layer_name = "labels_softmax:0", num_top_predictions = 1):
        # self.load_graph(frozen_graph)
        # with tf.Session() as sess:
        softmax_tensor = self.sess.graph.get_tensor_by_name(output_layer_name)
        predictions, = self.sess.run(softmax_tensor, {input_layer_name: wav_data})

        top_k = predictions.argsort()[-num_top_predictions:][::-1]
        for node_id in top_k:
            human_string = self.labels[node_id]
            score = predictions[node_id]
            print('%s (score = %.5f)' % (human_string, score))

        return self.labels[top_k[0]], predictions[top_k[0]]
