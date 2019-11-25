from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import json
import os
import cv2
from src.controllers.service_controller import *

app = Flask(__name__)
CORS(app)
controller = ServiceControllder()

# Base.metadata.create_all(engine)

@app.route('/')
def index():
    return 'Index Page'


@app.route('/classify', methods=['POST'])
def classify():
    # print(request.data)
    data = request.data
    path = os.path.join(os.path.dirname(__file__), 'test.jpg')
    recognized_name = 'no body'
    if(data):
        img = convert_to_img(data)
        # misc.imsave(path, img)
        #cv2.imwrite(path, cv2.cvtColor(img, cv2.COLOR_RGBA2BGR))
        # cv2.imwrite(path, img)
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        # img = img[:, :, 1:4]
        part_name, probability = controller.classify(img)

    return jsonify(part_name)


@app.route('/detect', methods=['POST'])
def detect():
    # print(request.data)
    data = request.data
    path = os.path.join(os.path.dirname(__file__), 'test.jpg')
    recognized_name = 'no body'
    if(data):
        img = convert_to_img(data)
        # misc.imsave(path, img)
        #cv2.imwrite(path, cv2.cvtColor(img, cv2.COLOR_RGBA2BGR))
        # cv2.imwrite(path, img)
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        # img = img[:, :, 1:4]
        coordinates = controller.detect(img)

    return jsonify(coordinates)


def convert_to_img(json_str):
    channel_num = 4
    img_size = len(json_str) / 4
    img = np.zeros((224, 224, channel_num))
    json_arr = json.loads(json_str)
    img_arr = []
    print(len(json_arr), np.shape(img_arr))
    # print(json_arr)
    for _, i in enumerate(json_arr):
        img_arr.append(json_arr[i])
    img = (np.array(img_arr).reshape((224, 224, 4)))
    img = img.astype(np.uint8)

    return img
    # print(len(json_arr))
    #print(img_arr)
    # for i in range(img_size):
    #     img[i][0] = json_str[i + 0][1]
    #     img[i][1] = json_str[i + 1][1]
    #     img[i][2] = json_str[i + 2][1]
    #     img[i][3] = json_str[i + 3][1]
    # cv2.imshow(img.)

if __name__ == "__main__":
    app.run()
