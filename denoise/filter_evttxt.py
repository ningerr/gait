"""
读取txt文档中的事件
按照密度进行噪声过滤
并保存为新的文档
时间为整数
"""
import time
import numpy as np


def event_txt_filter(txt, threshold):  # denoise filter

    data = np.array(txt)
    data[:, 0] = data[:, 0] - min(data[:, 0])

    # set the size of block
    time_block_size = np.floor((max(data[:, 0]) - min(data[:, 0])) / timeblock[0])  # time
    x_block_size = np.floor(max(data[:, 1]) / xblock[0])  # x
    y_block_size = np.floor(max(data[:, 2]) / yblock[0])  # y

    # get the block id of event
    time_bins = np.floor(data[:, 0] / time_block_size).astype(int)
    x_bins = np.floor(data[:, 1] / x_block_size).astype(int)
    y_bins = np.floor(data[:, 2] / y_block_size).astype(int)

    blocks = np.vstack((time_bins, x_bins, y_bins)).T

    # count events of each block
    unique_blocks, counts = np.unique(blocks, axis=0, return_counts=True)

    # mask of events keep
    mask = np.zeros(len(data), dtype=bool)

    # compare with threshold and keep the events
    for block, count in zip(unique_blocks, counts):
        if count >= threshold:
            block_mask = np.all(blocks == block, axis=1)
            mask[block_mask] = True

    filtered_data = data[mask]
    filtered_data = filtered_data.astype(int)

    return filtered_data


def event_txt_filter_2r(txt, threshold):  # denoise filter

    data = np.array(txt)
    data[:, 0] = data[:, 0] - min(data[:, 0])

    # set the size of block
    time_block_size = np.floor((max(data[:, 0]) - min(data[:, 0])) / timeblock[0])  # time
    x_block_size = np.floor(max(data[:, 1]) / xblock[0])  # x
    y_block_size = np.floor(max(data[:, 2]) / yblock)[0]  # y

    # get the block id of event
    time_bins = np.floor(data[:, 0] / time_block_size).astype(int)
    x_bins = np.floor(data[:, 1] / x_block_size).astype(int)
    y_bins = np.floor(data[:, 2] / y_block_size).astype(int)

    blocks = np.vstack((time_bins, x_bins, y_bins)).T

    # count events of each block
    unique_blocks, counts = np.unique(blocks, axis=0, return_counts=True)

    # mask of events keep
    mask = np.zeros(len(data), dtype=bool)

    # compare with threshold and keep the events
    for block, count in zip(unique_blocks, counts):
        if count >= threshold[0]:  # Keep all events in the block
            block_mask = np.all(blocks == block, axis=1)
            mask[block_mask] = True
        elif count < threshold[1]:  # Discard all events in the block
            continue
        else:  # Subdivide and apply subblock filtering
            # print("00")
            block_mask = np.all(blocks == block, axis=1)
            block_data = data[block_mask]

            # Subdividing the block
            subblock_factors = [timeblock[1], xblock[1], yblock[1]]
            time_factor, x_factor, y_factor = subblock_factors
            sub_time_block_size = time_block_size / time_factor
            sub_x_block_size = x_block_size / x_factor
            sub_y_block_size = y_block_size / y_factor

            # Get subblock indices
            sub_time_bins = np.floor(block_data[:, 0] / sub_time_block_size).astype(int)
            sub_x_bins = np.floor(block_data[:, 1] / sub_x_block_size).astype(int)
            sub_y_bins = np.floor(block_data[:, 2] / sub_y_block_size).astype(int)

            sub_blocks = np.vstack((sub_time_bins, sub_x_bins, sub_y_bins)).T

            # Count events in each subblock
            unique_sub_blocks, sub_counts = np.unique(sub_blocks, axis=0, return_counts=True)

            # Retain events in subblocks with enough points
            for sub_block, sub_count in zip(unique_sub_blocks, sub_counts):
                if sub_count >= count / 10:
                    sub_block_mask = np.all(sub_blocks == sub_block, axis=1)
                    indices = np.where(block_mask)[0]  # 找到 block_mask 为 True 的索引
                    mask[indices[sub_block_mask]] = True

    filtered_data = data[mask]
    filtered_data = filtered_data.astype(int)

    return filtered_data


def txt_dn_write(denoise_file, src_path):  # 数据写入文件
    dn_path = src_path.split('.')
    # dn_path = dn_path[0] + '_dn' + '.' + dn_path[1]
    dn_path = dn_path[0] + '_dn_2r' + '.' + dn_path[1]
    # dn_path
    with open(dn_path, 'w') as file:
        for tuple_ in denoise_file:
            file.write('\t'.join(map(str, tuple_)) + '\n')
    return dn_path


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


if __name__ == '__main__':
    path = "E:\\Dataset\\CASIA_B_2020\\000\\1\\1.txt"
    # threhold = 100
    # number of block
    # timeblock = 50
    # xblock = 15
    # yblock = 15
    threshold = [100, 5]
    timeblock = [50, 1]
    xblock = [8, 3]
    yblock = [8, 3]
    srcfile = txt_read(path)
    start_time = time.time()

    # denoise_file = event_txt_filter(srcfile, 5)
    # 阈值较小，因此设置两种半径意义不大
    # 为了观察效果差异，将时间维度直接归一，再设置两种半径，比较效果
    denoise_file = event_txt_filter_2r(srcfile, threshold)

    txt_file = txt_dn_write(denoise_file, path)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Write the txt in {txt_file}")
    print(f"Time：{elapsed_time:.4f} seconds")
