"""
扩充数据集
通过随机采样
env py3.7
"""
import matlab.engine
import os

eng = matlab.engine.start_matlab()
# eng.addpath(r'')  # matlab脚本路径

maxpoint = 100
sample = eng.sample
num = 2

dataset = ''
# data_path = os.listdir(dataset)
data_path = 'E:\\Dataset\\ev_GaitDatasetA\\fyc\\00_1.txt'
mini_name = (data_path.split('.')[0]).split('\\')[-1]

for i in range(num):
    name = mini_name + '_s_' + str(i)
    mini_path = ' ' + name
    mini_data_path = sample(data_path, mini_path, float(maxpoint), nargout=0)
    print(mini_data_path)
