"""
扩充数据集
采用的的方法是滑动时间窗口

"""
import os
import numpy as np


def txt_read(txt_path):  # read txt file， return list
    events = []
    f = open(txt_path, 'r')
    for line in f:
        if line.startswith("#"):
            continue
        parts = line.strip().split()
        timestamp = float(parts[0])
        x_coord = int(parts[1])
        y_coord = int(parts[2])
        polarity = int(parts[3])
        events.append((timestamp, x_coord, y_coord, polarity))
    return events


def txt_dn_write(data, path_origin):
    """
    input window mini datas，original data path
    return mini data path list
    """
    num = len(data)
    path_new = []
    for i in range(num):
        dataset_name = path_origin.split('\\')[-4]
        path_extend = path_origin.replace(dataset_name, dataset_name + '_extend_train')

        name = path_extend.split('.')[0] + '_' + str(i + 1)
        path_new.append(name + '.txt')
    for p in path_new:
        folder_path, file_name = os.path.split(p)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        idx = (p.split('.')[0]).split('_')[-1]
        with open(p, 'w') as file:
            for tuple_ in data[int(idx) - 1]:
                int_tuple = tuple(map(int, tuple_))
                file.write('\t'.join(map(str, int_tuple)) + '\n')
    return path_new


def flash_window_t(data, num):  # 输入数据和窗口数量 返回窗口数据列表
    events = np.array(data)
    timestamp = events[:, 0]
    timestamp = timestamp - min(timestamp)
    t_len = len(set(timestamp))
    t_max = max(timestamp)
    t = t_max / 1.5     # window length
    mini_data = []
    for i in range(num):
        print(f"第{i}个窗口数据...")
        start_t = np.random.uniform(0, t_max - t, 1)  # random window start time
        end_t = start_t + t  # window ending time
        # copy the events whose t during [start_t, end_t]
        window_data = events[(timestamp >= start_t) & (timestamp <= end_t)]
        # save
        mini_data.append(window_data)

    return mini_data




if __name__ == '__main__':

    dataset = "E:\\Dataset\\CASIB_dvd\\train"
    people = os.listdir(dataset)
    for person in people:
        events = os.listdir(os.path.join(dataset, person))
        for event in events:
            path = os.path.join(dataset, person, event)
            data = txt_read(path)
            num = 3
            mini_datas = flash_window_t(data, num)
            mini_paths = txt_dn_write(mini_datas, path)
            print(mini_paths)
