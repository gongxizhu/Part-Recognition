import os
import cv2
import random
from shutil import copyfile


dst_file_prefix = 'part'
dst_file_suffix = '.jpg'
dataset_full_folder = r'dataset/full'
dataset_train_folder = r'dataset/train'
dataset_test_folder = r'dataset/test'
ratio_train = 0.7
ratio_test = 0.3
random_seed = 10

dataset_path = os.path.dirname(__file__)
source_image_folders = [sub_folder for sub_folder in os.listdir(os.path.join(dataset_path, dataset_full_folder))]

print(r'Starts to move images to target_folder...')

random.seed(random_seed)

# move images to train and test folder
for img_folder in source_image_folders:
    image_folder = os.path.join(dataset_path, dataset_full_folder, img_folder)
    imgs = [img for img in os.listdir(image_folder)]
    random.shuffle(imgs)
    count_train = int(len(imgs) * ratio_train)
    imgs_train = imgs[:count_train]
    imgs_test = imgs[count_train:]
    for x, img in enumerate(imgs_train):
        target_folder = os.path.join(dataset_path, dataset_train_folder, img_folder)
        if (not os.path.exists(target_folder)):
            os.mkdir(target_folder)
        src = os.path.join(image_folder, img)
        dst = os.path.join(target_folder, dst_file_prefix + '_' + str(x) + dst_file_suffix)
        raw_image = cv2.imread(src)
        # cvt_img = cv2.transpose(raw_image);
        # cvt_img = cv2.flip(cvt_img, 1);
        cv2.imwrite(dst, raw_image)

    for y, img in enumerate(imgs_test):
        target_folder = os.path.join(dataset_path, dataset_test_folder, img_folder)
        if(not os.path.exists(target_folder)):
            os.mkdir(target_folder)
        src = os.path.join(image_folder, img)
        dst = os.path.join(target_folder, dst_file_prefix + '_' + str(y) + dst_file_suffix)
        raw_image = cv2.imread(src)
        # cvt_img = cv2.transpose(raw_image);
        # cvt_img = cv2.flip(cvt_img, 1);
        cv2.imwrite(dst, raw_image)

print(r'All images are moved.')