'''
将三个波段下的灰度图合并成伪彩图，丰富图像信息，此处的灰度图为三个通道（R G B）都是相同值的灰度图
'''


import cv2
import numpy as np
import os

def get_image(image_name):
    current_file_path = os.path.abspath(__file__)
    image_father_path = current_file_path.split('src')[0] + 'RGB\\'
    gray_image_path_1 = image_father_path + f'blue\\{image_name}.png'
    gray_image_path_2 = image_father_path + f'green\\{image_name}.png'
    gray_image_path_3 = image_father_path + f'red\\{image_name}.png'
    gray_image_1 = cv2.imread(gray_image_path_1)
    gray_image_2 = cv2.imread(gray_image_path_2)
    gray_image_3 = cv2.imread(gray_image_path_3)
    return gray_image_1, gray_image_2, gray_image_3


current_file_path = os.path.abspath(__file__)
image__dir = current_file_path.split('src')[0] + 'blue'
imagelist = os.listdir(image__dir)
merged_image_path = current_file_path.split('src')[0] + 'merged_image'
if not os.path.exists(merged_image_path):
    os.mkdir(merged_image_path)
for image_name in imagelist:
    gray_image_1, gray_image_2, gray_image_3 = get_image(image_name.split('.')[0])
    # 创建具有三个通道的空白图像
    merged_image = np.zeros(
        (gray_image_1.shape[0], gray_image_1.shape[1], 3), dtype=np.uint8)

    # 将灰度图像复制到相应的通道
    merged_image[:, :, 0] = gray_image_1[:, :, 0]
    merged_image[:, :, 1] = gray_image_2[:, :, 0]
    merged_image[:, :, 2] = gray_image_3[:, :, 0]

    # 保存合并的图像
    cv2.imwrite(f'{merged_image_path}\\{image_name}.png', merged_image)








