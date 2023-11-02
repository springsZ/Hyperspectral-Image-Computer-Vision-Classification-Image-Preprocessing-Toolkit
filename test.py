'''测试某个图片三个通道数据是否相同'''

import cv2
import numpy as np

# 读取图像
image = cv2.imread('HT.png')

# 分离通道
channels = cv2.split(image)

# 获取每个通道的最大值
max_values = []
for channel in channels:
    max_value = np.max(channel)
    max_values.append(max_value)

# 打印每个通道的最大值
for i, max_value in enumerate(max_values):
    print(f"通道 {i}: 最大值为 {max_value}")

if np.array_equal(channels[0], channels[1]) and np.array_equal(channels[1], channels[2]):
    print("三个通道内的数据相同")
else:
    print("三个通道内的数据不相同")
