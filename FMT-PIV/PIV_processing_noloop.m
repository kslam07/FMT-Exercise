clc; clear; close all;

%% Self-made Code Group 01

AoA = 15;
FoldRead = ['data\Alpha' int2str(AoA) '_dt100\'];
FileRead = 'B00020.tif';

pix_size =  4.40;           % [microns]
M = 0.0428;                 % magnification
dt = 100;                   % [microsec] time separation
ws = 32;                    % window size
ovlap = 0.5;                % overlap percentage
window_shape={'square'};    % window shape
xo = 133;                   % x origin in pixels
yo = 527;                   % y origin in pixels

% Read and split figures
image_both = imread([FoldRead FileRead]);

image_1 = image_both(1:size(image_both, 1)/2, :);
image_2 = image_both((size(image_both, 1)/2) + 1:end, :);

image_1 = double(image_1);
image_2 = double(image_2);

rows = size(image_1, 1);
cols = size(image_1, 2);

% Read mask
mask = load(['WIDIM/Mask_Alpha_' int2str(AoA)]);
mask = poly2mask(mask.xmask, mask.ymask, rows, cols);

% Size windows
wb = ws * (1 - ovlap);                      % window boundaries

ncols_wdw = floor((cols - wb)/(ws - wb));   % number of windows in x-dir
nrows_wdw = floor((rows - wb)/(ws - wb));   % number of windows in y-dir

% Compute cross-correlation

xshift_array = zeros(nrows_wdw, ncols_wdw);
yshift_array = zeros(nrows_wdw, ncols_wdw);
mask_array = zeros(nrows_wdw, ncols_wdw);
center_array = zeros(nrows_wdw, ncols_wdw, 2);

for i = 1:nrows_wdw
    
    for j = 1:ncols_wdw
        
        % Index to select correct window
        row_idx = 1 + (i - 1)*wb;
        col_idx = 1 + (j - 1)*wb;
        
        % Create windows
        wdw_1 = image_1(row_idx:row_idx + (ws - 1), col_idx:col_idx + (ws - 1));
        wdw_2 = image_2(row_idx:row_idx + (ws - 1), col_idx:col_idx + (ws - 1));
        
        % Remove mean
        wdw_1 = wdw_1 - mean(wdw_1, 'all');
        wdw_2 = wdw_2 - mean(wdw_2, 'all');

        % Calculate correlation
        phi = xcorr2(wdw_1, wdw_2);
        phi_norm = normxcorr2(wdw_1, wdw_2);
        
        % Locate peak
        [peak_value, loc] = max(phi(:));
        [y_loc, x_loc] = ind2sub(size(phi), loc);
        corr_offset = [(y_loc - size(wdw_1, 1)) (x_loc - size(wdw_2, 2))];
        
        % Store displacement
        x_shift = corr_offset(2);
        y_shift = corr_offset(1);
        
        xshift_array(i, j) = x_shift;
        yshift_array(i, j) = y_shift;
        
        % Compute SNR???
        % Subpixel interpolation???
        
        % Create airfoil mask + reflection zones
        wdw_mask = mask(row_idx:row_idx + (ws - 1), col_idx:col_idx + (ws - 1));
        
        if mean(wdw_mask, 'all') > 0
            
            mask_array(i, j) = 1;
            
        end
        
        center_array(i, j, :) = [row_idx + (ws/2), col_idx + (ws/2)];  

    end
    
end

% Plot last correlation distribution
norm = false;
if norm
    phi = phi_norm 
end

figure();
xrange = floor(size(phi, 1)/2);
yrange = floor(size(phi, 2)/2);
[X,Y] = meshgrid(-xrange:xrange, -yrange:yrange);
Z = phi;
surf(X,Y,Z)
xlabel('$\Delta x [px]$', 'Interpreter', 'latex')
ylabel('$\Delta y [px]$', 'Interpreter', 'latex')
title('Cross-Correlation')

% Compute velocity magnitude
u = -(xshift_array .* pix_size)/(M * dt);
v = -(yshift_array .* pix_size)/(M * dt);

v_map = sqrt(u.^2 + v.^2);

% Apply mask
mask_array = logical(mask_array);

u(mask_array) = NaN;
v(mask_array) = NaN;
v_map(mask_array) = NaN;
u(u > 14) = 14;
v_map(v_map > 14) = 14;

% Visualize velocity vectors and contours
% figure();
% imagesc(v_map);
% hold on
% colormap('parula')
% cbar = colorbar();
% set(get(cbar, 'Title'), 'String', 'Velocity Magnitude [m/s]')
% %v = zeros(size(u));
% quiver(u, v, 'k');
% xlabel('$X [mm]$', 'Interpreter', 'latex')
% ylabel('$Y [mm]$', 'Interpreter', 'latex')
% title('u [m/s], Mean')

xrange = (center_array(:, :, 2) - xo) * pix_size * 1e-3/M;
yrange = (center_array(:, :, 1) - yo) * pix_size * 1e-3/M;

figure();
contourf(xrange, yrange, u, 20, 'Linestyle', 'none'), axis equal, axis tight
hold on
quiver(xrange, yrange, u, v,'k');
colorbar;
caxis([-6, 13]);
set(gca, 'YDir','reverse')
xlabel('X [mm]','FontSize',14)
ylabel('Y [mm]','FontSize',14)
title(['u [m/s], Instantaneous'],'FontSize',14)
set(gca,'FontSize',12);