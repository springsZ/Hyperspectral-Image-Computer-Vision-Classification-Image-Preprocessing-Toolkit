'''
对数据集进行数据扩充，这里使用了四种数据扩充方式。
还可以根据项目的具体情况进行其他的数据扩充操作，比如增加噪声、模糊、增强亮度等
这里进行了整体五倍的数据扩充以及单独对HT类进行了十倍的数据扩充，以到达数据平衡的目的，可根据需求自行更改
图像增强完成后调用generate_label函数生成对应的标签文件
'''



import cv2
import os
import numpy as np
from generate_label import generate_label


def data_augmentation(image, output_path):
    # 在这里进行数据扩充操作
    # 可以使用OpenCV提供的各种图像处理函数进行旋转、平移、缩放、翻转等操作
    # 设置种子
    np.random.seed(1)
    # 设置一个随机数，根据随机数的值，对图像进行不同的处理
    random_num = np.random.randint(1, 5)
    if random_num == 1:
        # 旋转90度
        augmented_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    elif random_num == 2:
        # 旋转180度
        augmented_image = cv2.rotate(image, cv2.ROTATE_180)
    elif random_num == 3:
        # 水平翻转
        augmented_image = cv2.flip(image, 1)
    elif random_num == 4:
        # 随机裁剪
        augmented_image = image[0:200, 0:200]
        # 缩放
        augmented_image = cv2.resize(image, (224, 224))
    # 保存增强后的图像
    cv2.imwrite(output_path, augmented_image)


# 原始数据集路径
current_path = os.path.abspath(__file__)
sub_path = 'datapath'
dataset_path = current_path.split(
    'src')[0] + f'{sub_path}\\train'
# 增强后的数据集保存路径
output_dataset_path = current_path.split(
    'src')[0] + f'{sub_path}\\augmented_image_224_train_all'
if not os.path.exists(output_dataset_path):
    os.mkdir(output_dataset_path)

# 遍历原始数据集
for root, dirs, files in os.walk(dataset_path):
    print(root)
    for file in files:
        # if 'HT' not in file:
        #     continue

        # 读取原始图像
        image_path = os.path.join(root, file)
        image = cv2.imread(image_path)
        output_path = os.path.join(output_dataset_path, file)
        cv2.imwrite(output_path, image)
        for i in range(5):
            # 定义增强后的图像路径
            output_path = os.path.join(
                output_dataset_path, str(i)+'-'+file)

            # 对原始图像进行数据扩充

            data_augmentation(image, output_path)

for root, dirs, files in os.walk(dataset_path):
    print(root)
    for file in files:
        if 'HT' not in file:
            continue

        # 读取原始图像
        image_path = os.path.join(root, file)
        image = cv2.imread(image_path)
        # output_path  = os.path.join(output_dataset_path,file)
        # cv2.imwrite(output_path, image)
        for i in range(10):
            # 定义增强后的图像路径
            output_path = os.path.join(output_dataset_path, str(i+5)+'-'+file)

            # 对原始图像进行数据扩充

            data_augmentation(image, output_path)

generate_label(output_dataset_path, 'train')
val_path = current_path.split(
    'src')[0] + f'{sub_path}\\val'
generate_label(val_path, 'val')
