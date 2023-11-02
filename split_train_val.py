'''
按照7:3的比例划分训练集和验证集
'''

from skimage import measure
import skimage
import numpy as np
import os
import cv2
import shutil

current_path = os.path.abspath(__file__)
image_father_path = current_path.split('src')[0] + 'crop_image_224'
files = os.listdir(image_father_path)
train_save_path = current_path.split('src')[0] + 'crop_image_224\\train'
val_save_path = current_path.split('src')[0] + 'crop_image_224\\val'
if not os.path.exists(train_save_path):
    os.mkdir(train_save_path)
if not os.path.exists(val_save_path):
    os.mkdir(val_save_path)
# 设置随机种子
np.random.seed(0)
   
# 按照7:3的比例划分训练集和验证集，同时三个类别的都按照这个比例划分
for image in files:
    if np.random.rand() < 0.8:
        shutil.copy(f'{image_father_path}\\{image}', f'{train_save_path}\\{image}')
    else:
        shutil.copy(f'{image_father_path}\\{image}', f'{val_save_path}\\{image}')

