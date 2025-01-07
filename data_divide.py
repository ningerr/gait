"""
数据集划分
分为训练集和测试集

"""
import os
import random
import shutil

import numpy as np


def save_data(file_path, save_dir, order_index):
    name = str(order_index) + '.txt'
    output_dir = os.path.join(save_dir, name)
    shutil.copy(file_path, output_dir)


def select_lable(path):
    selected = []
    unselected = []
    angles = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    for angle in angles:
        angle_path = os.path.join(rootpath, angle)
        if os.path.isdir(angle_path):
            people = [f for f in os.listdir(angle_path) if os.path.isdir(os.path.join(angle_path, f))]
            continue
        continue
    N = len(people) // 3
    i = 0
    for person in people:
        i += 1
        if i < N:
            selected.append(person)
        else:
            unselected.append(person)

    return selected, unselected


def dvd2(path):
    """
    针对 CASIA_B_2020数据集
    path--|000-|1-|1.txt
                 -|2.txt
                 ...
              -|2
              ...
        --|018
          ...
    :param path:
    :return:
    """
    angles = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    valid_count = 0
    test_count = 0
    p1, p2 = select_lable(path)
    train_count = {str(key): 0 for key in p1}
    test_count = {str(key): 0 for key in p1}

    for angle in angles:
        angle_path = os.path.join(rootpath, angle)
        people = [f for f in os.listdir(angle_path) if os.path.isdir(os.path.join(angle_path, f))]
        for person in people:
            # 预训练数据和训练数据1：2
            if person in p1:
                people_path = os.path.join(angle_path, person)
                if os.path.isdir(people_path):
                    datas = os.listdir(people_path)
                    # 4：1：1划分并保存
                    random.shuffle(datas)
                    train_data = datas[:len(datas) * 4 // 6]
                    valid_data = datas[len(datas) * 4 // 6:len(datas) * 4 // 6 + len(datas) // 6]
                    test_data = datas[len(datas) * 4 // 6 + len(datas) // 6:]
                    for data in train_data:
                        train_path = 'E:\\Dataset\\CASIB_dvd\\train\\' + person + '\\'
                        data_path = os.path.join(people_path, data)
                        os.makedirs(train_path, exist_ok=True)
                        train_count[person] += 1
                        save_data(data_path, train_path, train_count[person])
                    for data in test_data:
                        test_path = 'E:\\Dataset\\CASIB_dvd\\test\\' + person + '\\'
                        data_path = os.path.join(people_path, data)
                        os.makedirs(test_path, exist_ok=True)
                        test_count[person] += 1
                        save_data(data_path, test_path, test_count[person])


            else:
                people_path = os.path.join(angle_path, person)
                if os.path.isdir(people_path):
                    datas = os.listdir(people_path)


def dvd3(inpath, outpath):
    """
    ev-casia-A
    inpath--name1--00_1_1.txt
                 --00_1_2.txt
                 --45_1_1.txt
          --name2--……

    :param inpath:
    :param outpath:
    :return:
    """
    angles = ["00", "45"] #选取角度
    namelist = os.listdir(inpath)
    train_files = []
    test_files = []

    for name in namelist:
        namepath = os.path.join(inpath, name)
        txtfiles = os.listdir(namepath)

        for angle in angles:
            filtered_file = [f for f in txtfiles if os.path.basename(f).startswith(angle)]
            random.shuffle(filtered_file)
            train_size = len(filtered_file) * 3 // 4
            train_files.extend(filtered_file[:train_size])
            test_files.extend(filtered_file[train_size:])


        for f in train_files:
            out_path_t = os.path.join(outpath, "train", name, f)
            in_path = os.path.join(inpath, name, f)

            os.makedirs(os.path.dirname(out_path_t),exist_ok=True)

            with open(in_path, "r") as fr, open(out_path_t, "w") as fw:
                fw.write(fr.read())

        for f in test_files:
            out_path_t = os.path.join(outpath, "test", name, f)
            in_path = os.path.join(inpath, name, f)

            os.makedirs(os.path.dirname(out_path_t),exist_ok=True)

            with open(in_path, "r") as fr, open(out_path_t, "w") as fw:
                fw.write(fr.read())



if __name__ == '__main__':
    rootpath = "E:\Dataset\ev_CSISAA_sample4"
    out = "E:\Dataset\ev_CSISAA_sample"
    dvd3(rootpath,out)
