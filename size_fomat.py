"""
将大小归一化为128*128，txt文件
"""
import numpy as np

def normalize_coordinates(events, new_width=128, new_height=128):
    normalized_events = []

    timestamps, x_coords, y_coords, polarities = zip(*events)
    y_max = np.max(y_coords)
    y_min = np.min(y_coords)
    x_max = np.max(x_coords)
    x_min = np.min(x_coords)
    t_max = np.max(timestamps)
    t_min = np.min(timestamps)

    for event in events:
        timestamp, x, y, polarity = event
        # 归一化坐标
        new_x = int(new_height * (x - x_min) / (x_max - x_min))
        new_y = int(new_width * (y - y_min) / (y_max - y_min))
        normalized_events.append((timestamp, new_x, new_y, polarity))

    return normalized_events


def process_event_file(input_file, output_file):
    """
    读取事件文件，归一化坐标后写入新的文件。
    :param input_file
    :param output_file
    """
    events = []

    # 读取事件文件
    with open(input_file, 'r') as f:
        for line in f:
            if line.startswith("#"):  # 忽略注释行
                continue
            parts = line.strip().split()
            timestamp = float(parts[0])
            x_coord = int(parts[1])
            y_coord = int(parts[2])
            polarity = int(parts[3])
            events.append((timestamp, x_coord, y_coord, polarity))

    # 归一化坐标
    normalized_events = normalize_coordinates(events)

    # 将结果写入新的文件
    with open(output_file, 'w') as f:
        for event in normalized_events:
            f.write(f"{event[0]} {event[1]} {event[2]} {event[3]}\n")

    # print(f"文件已保存到 {output_file}")


# 使用示例
input_file = "E:\\Dataset\\ev_GaitDatasetA\\fyc\\00_1_downsampl.txt"
output_file = "E:\\Dataset\\ev_GaitDatasetA\\fyc\\00_1_normalized.txt"


process_event_file(input_file, output_file)
