%sample used for dataset extend 

% test_path = "E:\Dataset\ev_GaitDatasetA\fyc\00_1.txt";
% test_save_path = 'E:\Dataset\ev_GaitDatasetA\fyc\00_1_1';
% down_sample(test_path, test_save_path, 200);

%%
% test_path = "E:\Dataset\ev_GaitDatasetA\fyc\00_1.txt";
% [folder, file_name, ext] = fileparts(test_path);
% new_file_path = fullfile(folder, file_name);
% for i =1:2
%     name = new_file_path + '_' + num2str(i) + '.txt';
% end

%%
function txt_path = sample(data_path, save_path, max_points)
fileId = fopen(data_path);    
data= textscan(fileId, '%f %f %f %f', 'Delimiter', ' ', 'CommentStyle', '#');
   
    t = data{1};
    t = t - min(t);
    x = data{2};
    y = data{3};
    p = data{4};
    data = [t, x, y, p];
    
    points = downsample(data, max_points);

    % save([save_path, '.mat'], 'points'); % save into mat

    % save into txt
    txt_path = [save_path,'.txt'];
    writematrix(points, txt_path, 'Delimiter', ' '); 
	
end

function [down_data] = downsample(data, max_points)
	time = data(:, 1);
	x = data(:, 2);
	y = data(:, 3);	
	p = data(:, 4);

	%convert to point cloud object
	points = [x, y, time];
	ptCloud = pointCloud(points);
	% down sample by using the functions from MATLAB
	ptCloudOut = pcdownsample(ptCloud, 'nonuniformGridSample', max_points);
	%extract the result from the original data
	points_downsample = ptCloudOut.Location;
	[~, pos] = ismember(points_downsample, points, 'rows');
	down_data = [];

	for i = pos
		% add event to down_data
		down_data = [down_data; time(i), x(i), y(i), p(i)];
		
    end
    %sort by time
    down_data = sortrows(down_data,1);
end

