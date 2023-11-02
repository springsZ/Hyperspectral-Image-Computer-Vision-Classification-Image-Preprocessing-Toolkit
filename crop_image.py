'''
使用连通域分析算法去除图像中的空白部分
并将图像变为统一大小的正方形
'''

from skimage import measure
import skimage
import numpy as np
import os
import cv2

current_path = os.path.abspath(__file__)
# 待处理图片的路径
image_father_path = current_path.split('src')[0] + 'datapath'
files = os.listdir(image_father_path)
# 保存处理后的图片的路径
save_path = current_path.split('src')[0] + 'datapath'
if not os.path.exists(save_path):
    os.mkdir(save_path)
i=0
for image in files:
    # if i==2:
    #     break
    raw_image = cv2.imread(f'{image_father_path}\\{image}')
    # 1. 二值化
    gray_image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)
    ret, binary_image = cv2.threshold(gray_image, 1, 255, cv2.THRESH_BINARY)
    # 2. 连通域分析
    labels = measure.label(binary_image, connectivity=2)
    # 3. 找出最大的连通域
    properties = measure.regionprops(labels)
    max_area = 0
    i+=1
    print(len(properties))
    for prop in properties:
        print(prop.bbox, prop.area)
        if prop.area > max_area:
            max_area = prop.area
            max_prop = prop
    # 4. 找出最大连通域的最小外接矩形
    minr, minc, maxr, maxc = max_prop.bbox
    print(minr, minc, maxr, maxc)
    # 5. 将最小外接矩形的区域保存下来
    crop_image = raw_image[minr:maxr, minc:maxc]
    
    # 将图片变为统一大小的正方形
    crop_image = cv2.resize(crop_image, (224, 224))
    # 6. 保存图片
    cv2.imwrite(f'{save_path}\\{image.split(".")[0]}.png', crop_image)