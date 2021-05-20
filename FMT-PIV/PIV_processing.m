clc; clear; close all;

%% Self-made Code Group 01

FoldRead = 'data\Alpha0_dt100\';
FileRead = 'B00001.tif';

pix_size =  4.40;           % [microns]
M = 0.0428;                 % magnification
dt = 100;                   % [microsec] time separation
ws = 32;                    % window size
ovlap = 50;                 % overlap percentage
window_shape={'square'};    % window shape

% Read mask
mask = load('WIDIM/Mask_Alpha_15');

% Read and split figures
image = imread([FoldRead FileRead]);

image_1 = image(1:size(image, 1)/2, :);
image_2 = image((size(image, 1)/2) + 1:end, :);

rows = 0;

% Create windows

ww = ws - (1-ovlap);        % window boundaries

wd_arr = 0;