'''根据spxy算法得出的训练集和测试集对应的标签对图像数据集也进行一一对应划分'''
import skimage
import numpy as np
import os
import cv2
import shutil
import pandas as pd
# raw_path = 'crop_image_224' save_path = 'spxy_224'


def spxy_image(raw_path, save_path):
    current_path = os.path.abspath(__file__)
    image_father_path = current_path.split(
        'src')[0] + f'{raw_path}'
    files = os.listdir(image_father_path)
    train_save_path = current_path.split(
        'src')[0] + f'{save_path}\\train'
    val_save_path = current_path.split(
        'src')[0] + f'{save_path}\\val'
    if not os.path.exists(train_save_path):
        os.mkdir(train_save_path)
    if not os.path.exists(val_save_path):
        os.mkdir(val_save_path)

    df_train = pd.read_excel(current_path.split('src')[
        0] + 'train.xlsx')
    df_test = pd.read_excel(current_path.split('src')[
        0] + 'test.xlsx')

    train_index = df_train['index'].tolist()
    # print(train_index)
    test_index = df_test['index'].tolist()
    # print(test_index)

    for image in files:
        find_image = image.split('.')[0] + '.npy'
        if find_image in train_index:
            shutil.copy(f'{image_father_path}\\{image}',
                        f'{train_save_path}\\{image}')
        elif find_image in test_index:
            shutil.copy(f'{image_father_path}\\{image}',
                        f'{val_save_path}\\{image}')
