% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% AirChar - The in-the-Air Handwritten Dataset for
% Character Recognition Based on Acceleration (IMU) Data
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Laboratory of Electronics and Instrumentation (LEI)
% Portalegre Polytechnic University
% T. M. D. Correia, S. D. Correia, and J. P. Matos-Carvalho
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Copyright 2024 LEI. All Rights Reserved.
%
% Licensed under the Apache License, Version 2.0 (the "License");
% you may not use this file except in compliance with the License.
% You may obtain a copy of the License at
%
%     http://www.apache.org/licenses/LICENSE-2.0
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This code loads a CSV file with raw data and applies a low-pass 4th order
% IIR Butterworth filter, with a cut-off frequency of 5Hz.
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Initializations 
close all
clear
clc

%% Gets directory content files
cd Samples
listing = dir('*.CSV');
cd ..

%% Filters each file individualy
for i=1:length(listing)
    FileName = listing(i).name;
    AddFilter(FileName,1);
end
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%