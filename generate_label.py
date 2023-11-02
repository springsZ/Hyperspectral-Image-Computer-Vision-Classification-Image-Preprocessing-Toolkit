# 在使用 DataLoader 加载数据集时，标签应该与每个数据样本相关联，并存储在数据集的相应位置。常见的做法是将标签作为数据集中每个样本的第二个元素，即(image, label) 对。

# 在 PyTorch 中，可以使用 ImageFolder 数据集类来方便地组织带标签的数据集。ImageFolder 期望数据集的目录结构符合以下方式：

# Copy
# root/class1/image1.jpg
# root/class1/image2.jpg
# ...
# root/class2/image1.jpg
# root/class2/image2.jpg
# ...
# 这样，ImageFolder 将自动为每个图像分配一个类别标签，并将其存储在 data_loader 返回的数据对中。
'''
根据图片标签将图片复制到指定文件夹，生成dataloader需要的格式
'''

import os
import shutil


def move_and_rename_image(image_path, destination_folder, new_filename):
    """
    将图片移动到指定文件夹，并且重命名
    :param image_path: 图片路径
    :param destination_folder: 目标文件夹
    :param new_filename: 新的文件名
    :return:
    """
   # 提取原始文件名和扩展名
    original_filename, extension = os.path.splitext(image_path)
    if os.path.exists(destination_folder) == False:
        os.makedirs(destination_folder)
    # 构建目标路径
    destination_path = os.path.join(
        destination_folder, new_filename + extension)

    # 移动并重命名图片
    shutil.copy(image_path, destination_path)


def generate_label(data_path, type='train'):

    # 获取当前文件的绝对路径
    current_file_path = os.path.abspath(__file__)
    print(current_file_path)
    image_father_path = data_path

    print(image_father_path)

    files = os.listdir(image_father_path)
    # 将图片复制到指定文件夹中并重命名
    for i in range(len(files)):
        target_path = f"{ current_file_path.split('src')[0]}data\\{type}"

        if files[i].find('HT') != -1:
            move_and_rename_image(image_father_path + '\\' + files[i],
                                  target_path+'\\0', str(i))
        elif files[i].find('NH') != -1:
            print('NH', files[i])
            move_and_rename_image(image_father_path + '\\' + files[i],
                                  target_path+'\\1', str(i))
        elif files[i].find('PY') != -1:
            print('PY', files[i])
            move_and_rename_image(image_father_path + '\\' + files[i],
                                  target_path+'\\2', str(i))
