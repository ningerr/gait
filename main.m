%%
% path = 'E:\Dataset\ev_GaitDatasetA_prp_7_08\fyc\00_1.txt';
% outpath = 'E:\Dataset\ev_GaitDatasetA_prp_7_08\fyc\00_1_1';
% N=10;
% sample(path,outpath,N);
%%
% outpath_visible = outpath+".txt";
% visible3d(outpath_visible);

%%
clear;

% 输入输出路径
input_folder = 'E:\Dataset\ev_GaitDatasetA';
output_folder = 'E:\Dataset\ev_CSISAA_sample4';
N = 4; % 每个txt文件扩充的数量
N_sample = 10; %采样参数

% 获取所有子文件夹及文件
names = dir(input_folder); 
names = names([names.isdir]); % 筛选出文件夹
names = names(~ismember({names.name}, {'.', '..'})); % 排除 '.' 和 '..'

for i = 1:length(names)
    name_folder = fullfile(input_folder, names(i).name); % 当前name文件夹路径
    output_name_folder = fullfile(output_folder, names(i).name); % 对应输出路径
    if ~exist(output_name_folder, 'dir')
        mkdir(output_name_folder); 
    end
    
    %name下所有txt
    txt_files = dir(fullfile(name_folder, '*.txt'));
    
    for j = 1:length(txt_files)
        input_file = fullfile(name_folder, txt_files(j).name); % 输入txt文件路径
        [~, file_name, file_ext] = fileparts(input_file); % 获取文件名和扩展名
        
        % 调用 sample 函数，生成 N 个新的 txt 文件
        for k = 1:N
            output_file = fullfile(output_name_folder, sprintf('%s_%d%s', file_name, k)); % 输出文件路径
            sample(input_file, output_file, N_sample); % 调用sample函数
        end
    end
end
