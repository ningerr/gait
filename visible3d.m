function picpath = visible3d(path)
    fileID = fopen(path, 'r');

    % 使用 textscan 读取数据，跳过以 # 开头的行
    data = textscan(fileID, '%f %f %f %f', 'Delimiter', ' ', 'CommentStyle', '#');

    % 关闭文件
    fclose(fileID);

    % 提取时间、x坐标和y坐标
    t = data{1};
    t = t - min(t);
    x = data{2};
    y = data{3};

    % 绘制三维图
    figure;
    scatter3(t, x, y,  1, t); % 使用散点图
    % ylim([0, 120]);
    ylabel('X坐标');
    zlabel('Y坐标');
    xlabel('时间');
    % title('采样前数据');
    % colorbar; % 添加颜色条
    [~, name, ~] = fileparts(path);
    disp(name);
    picpath = ['E:\Dataset\' name];
    saveas(gcf,picpath)

end
     
