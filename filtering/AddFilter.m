% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Function that applies the filter considering the file name
% 
% PLOT definition willl create charts qith the acceleration and angular
% velocity
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function fileID = AddFilter(FileName, PLOT)

close all 

%% Initializations 
startRow = 18;              % Start of data points
Fs = 100;                   % Sampling frequency (Hz) 


%% Read the content of the CSV file

% *** HEADER ***
cd Samples
fileID = fopen(FileName, 'r');
Header = cell(startRow-1, 1);
for i = 1:startRow-1
    Header{i} = fgetl(fileID);
end
fclose(fileID);

% Preprocessing Filter: Yes
Header{12} = regexprep(Header{12}, 'No', 'Yes');

% New file name
NewFileName = regexprep(FileName, 'p0', 'p1');
Header{7} = regexprep(Header{7}, 'p0', 'p1');

% *** DATA VALUES ***
dataF = readtable(FileName,'NumHeaderLines',startRow-1);
data = table2array(dataF(:,1:6));
Labels = table2array(dataF(:,7));

% Display the original raw data
[L nC] = size(data);
t = (0:L-1)./Fs;

if (PLOT==1)
    figure
    %subplot(2,1,1);
    plot(t,data(:,1:3).*9.8)
    % title('IMU Raw Data [Acceleration]');
    grid
    xlabel('t');
    ylabel('Acceleration (m/s^2)')
    legend('A_x','A_y','A_z');
    
    figure
    %subplot(2,1,2)
    plot(t,data(:,4:6)*0.017453)
    % title('IMU Raw Data [Angular Velocity]');
    grid
    xlabel('t');
    ylabel('Angular Velocity (rad/s)')
    legend('\omega_x','\omega_y','\omega_z');
end

%% Implements the Filter
Fc = 10;                     % cutoff frequency (Hz)
Wn = Fc / (Fs / 2);         % Normalize the cutoff frequency
[b, a] = butter(4, Wn);     % 4th order Butterworth filter

% Apply the filter to each column of the data
filteredData = filtfilt(b, a, data);
filteredData = [filteredData Labels];

if (PLOT==1)
    figure
    %subplot(2,1,1);
    plot(t,filteredData(:,1:3).*9.8)
    % title('Filtered Data (4^{th} Order Butterworth, f_s=5Hz) [Acceleration]');
    grid
    xlabel('t');
    ylabel('Acceleration (m/s^2)')
    legend('A_x','A_y','A_z');
    
    figure
    %subplot(2,1,2)
    plot(t,filteredData(:,4:6)*0.017453)
    % title('Filtered Data (4^{th} Order Butterworth, f_s=5Hz) [Angular Velocity]');
    grid
    xlabel('t');
    ylabel('Angular Velocity (rad/s)')
    legend('\omega_x','\omega_y','\omega_z');
end

%% Saves the new filtered data on a new file
cd Filtered
writelines(Header,NewFileName);
writematrix(filteredData,NewFileName,'WriteMode','append','Delimiter',';');

cd ..
cd ..

end
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%