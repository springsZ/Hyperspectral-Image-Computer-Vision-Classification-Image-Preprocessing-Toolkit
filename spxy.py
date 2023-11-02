'''使用spxy算法对数据进行分割，分割成训练集和验证集,并保存图片对应的名称，引入spxy_image函数，将图片也分割成对应的训练集和验证集'''

import numpy as np
import os
import pandas as pd
from spxy_image import spxy_image


def spxy(x, y, indexx, test_size=0.2):
    """
    :param x: shape (n_samples, n_features)
    :param y: shape (n_sample, )
    :param test_size: the ratio of test_size
    :return: spec_train :(n_samples, n_features)
             spec_test: (n_samples, n_features)
             target_train: (n_sample, )
             target_test: (n_sample, )
    """
    x_backup = x
    y_backup = y
    # print(index)
    M = x.shape[0]
    N = round((1-test_size) * M)
    samples = np.arange(M)

    y = (y - np.mean(y))/np.std(y)
    D = np.zeros((M, M))
    Dy = np.zeros((M, M))

    for i in range(M-1):
        xa = x[i, :]
        ya = y[i]
        for j in range((i+1), M):
            xb = x[j, :]
            yb = y[j]
            D[i, j] = np.linalg.norm(xa-xb)
            Dy[i, j] = np.linalg.norm(ya - yb)

    Dmax = np.max(D)
    Dymax = np.max(Dy)
    D = D/Dmax + Dy/Dymax

    maxD = D.max(axis=0)
    index_row = D.argmax(axis=0)
    index_column = maxD.argmax()

    m = np.zeros(N)
    m[0] = index_row[index_column]
    m[1] = index_column
    m = m.astype(int)

    dminmax = np.zeros(N)
    dminmax[1] = D[m[0], m[1]]

    for i in range(2, N):
        pool = np.delete(samples, m[:i])
        dmin = np.zeros(M-i)
        for j in range(M-i):
            indexa = pool[j]
            d = np.zeros(i)
            for k in range(i):
                indexb = m[k]
                if indexa < indexb:
                    d[k] = D[indexa, indexb]
                else:
                    d[k] = D[indexb, indexa]
            dmin[j] = np.min(d)
        dminmax[i] = np.max(dmin)
        index = np.argmax(dmin)
        m[i] = pool[index]

    m_complement = np.delete(np.arange(x.shape[0]), m)
    spec_train = x[m, :]
    target_train = y_backup[m]
    spec_test = x[m_complement, :]
    target_test = y_backup[m_complement]
    index_train = indexx[m]
    index_test = indexx[m_complement]

    return spec_train, spec_test, target_train, target_test, index_train, index_test


if __name__ == '__main__':
    current_file_path = os.path.abspath(__file__)
    print(current_file_path)
    file_path = current_file_path.split('src')[0] + 'raw.xlsx'
    data = pd.read_excel(file_path)
    # 其中x是除了前三列的所有列，y是第三列，index记录第一列的值
    x = data.iloc[:, 3:].values
    y = data.iloc[:, 2].values
    indexx = data.iloc[:, 0].values
    spec_train, spec_test, target_train, target_test, index_train, index_test = spxy(
        x, y, indexx, test_size=0.2)
    # 拿到data的列名
    columns = data.columns.values.tolist()
    # 拿到x的列名
    columns_x = columns[3:]
    columns_y = columns[2]
    # print(index_train)
    # print(len(index_train), len(index_test))
    print(spec_train)
    # 将训练集和验证集以及index都保存下来
    train = pd.DataFrame(spec_train, columns=columns_x)
    train[columns_y] = target_train
    train['index'] = index_train
    # 把index列放到第一列
    cols = train.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    # 保存为xlsx文件
    train = train[cols]
    train.to_excel(current_file_path.split('src')[
                   0] + '\\train.xlsx', index=False)

    test = pd.DataFrame(spec_test, columns=columns_x)
    test[columns_y] = target_test
    test['index'] = index_test
    cols = test.columns.tolist() 
    cols = cols[-1:] + cols[:-1]
    test = test[cols]
    test.to_excel(current_file_path.split('src')[
                  0] + '\\test.xlsx', index=False)

    spxy_image('crop_image_224', 'spxy_224')
