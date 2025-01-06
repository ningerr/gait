"""
turn events txt file into video
sometimes upsidedown for dataset GaitDatasetA
"""

import numpy as np
import cv2 as cv


def draw_normal128(events):
    """
    将数据归一化为128*128查看
    """
    timestamps, x_coords, y_coords, polarities = zip(*events)
    # 归一化为128*128的图像
    x_pic = 128
    y_pic = 128

    y_max = np.max(y_coords)
    y_min = np.min(y_coords)
    x_max = np.max(x_coords)
    x_min = np.min(x_coords)
    t_max = np.max(timestamps)
    t_min = np.min(timestamps)
    image = np.zeros((x_pic+1, y_pic+1, 3), dtype=np.uint8)
    N=500
    cnts = np.zeros(N)   # number of frames
    cnt = 0
    color = np.array([[0, 0, 255],
                      [0, 255, 0]])
    dt = (t_max-t_min) / N
    t = dt

    for event in events:
        timestamp, x_coord, y_coord, polarity = event
        timestamp = timestamp - t_min
        x_coord = int(x_pic * (x_coord-x_min)/(x_max-x_min))
        y_coord = int(y_pic * (y_coord-y_min) / (y_max-y_min))
        # y_coord = y_max - y_coord
        image[y_coord][x_coord] = color[polarity]

        if timestamp > t:
            cv.imshow(txtfile, image)
            cv.waitKey(1)
            t = t + dt
            cnt = cnt + 1  # index of frame
            image = np.zeros((y_pic+1, x_pic+1, 3), dtype=np.uint8)
        cnts[cnt] = cnts[cnt] + 1


def draw(events):
    timestamps, x_coords, y_coords, polarities = zip(*events)
    y_max = np.max(y_coords)
    x_max = np.max(x_coords)
    t_max = np.max(timestamps)
    t_min = np.min(timestamps)
    image = np.zeros((y_max+1, x_max+1, 3), dtype=np.uint8)
    N=500
    cnts = np.zeros(N)   # number of frames
    cnt = 0
    color = np.array([[0, 0, 255],
                      [0, 255, 0]])
    dt = (t_max-t_min) / N
    t = dt
    for event in events:
        timestamp, x_coord, y_coord, polarity = event
        timestamp = timestamp - t_min
        # y_coord = y_max - y_coord
        image[y_coord][x_coord] = color[polarity]

        if timestamp > t:
            cv.imshow(txtfile, image)
            cv.waitKey(1)
            t = t + dt
            cnt = cnt + 1  # index of frame
            image = np.zeros((y_max+1, x_max+1, 3), dtype=np.uint8)
        cnts[cnt] = cnts[cnt] + 1


if __name__ == "__main__":
    events = []
    # txtfile = "E:\Dataset\ev_GaitDatasetA\\fyc\\00_1_dvs128.txt"  #采样前 40W
    # txtfile = "E:\Dataset\ev_GaitDatasetA\\fyc\\00_1_downsample_100.txt" 采样后 1W6
    # txtfile = "E:\Dataset\ev_GaitDatasetA\\fyc\\00_1_downsampl.txt" #采样后 6W
    txtfile = "E:\\Dataset\\ev_GaitDatasetA\\fyc\\00_1_dvs128_dsp.txt"
    # image = np.zeros((240, 352, 3), dtype=np.uint8)
    f = open(txtfile, 'r')
    for line in f:
        if line.startswith("#"):
            continue
        parts = line.strip().split()
        timestamp = float(parts[0])
        x_coord = int(parts[1])
        y_coord = int(parts[2])
        polarity = int(parts[3])
        events.append((timestamp, x_coord, y_coord, polarity))

    events_sorted = sorted(events, key=lambda event: event[0])

    draw(events_sorted)
