clc; clear; close all;

%% statistical analysis of the velocity field data
% folder containing the velocity fields
FoldRead='./data/Alpha15_dt100/PIV_32x32_50%ov/'; % (*** fill in ***)
first=1;    % (*** fill in ***) first velocity field to be analyzed
last=100;     % (*** fill in ***) last velocity field to be analyzed

% do not modify the three lines below
FileRoot = 'B0';
FileApp = '.dat';
ZeroStr = '0000';

%% processing
for i=first:last
    iStr = num2str(i);
    fprintf([iStr '\n']);
    FileRead = [FileRoot ZeroStr(1:end-length(iStr)) iStr FileApp];
    [x,y,u,v,I,J] = ReadDat_2C([FoldRead FileRead]);
    % initialization
    if i==1
        uTot = zeros(J,I,last-first+1);
        vTot = zeros(J,I,last-first+1);
    end    

    uTot(:,:,i) = u;
    vTot(:,:,i) = v;
end

% compute the mean velocity components and the fluctuations
% root-mean-square (*** fill in ***)
uMean = mean(uTot,3);
uStd = std(uTot,0,3);
vMean = mean(vTot,3);
vStd = std(vTot,0,3);

%% create the folder foldw (where the data are written) if it doesn't exist
%% do not modify this part
FoldWrite = [FoldRead 'Stat' num2str(first) '-' num2str(last) '\'];
if exist(FoldWrite,'dir')~=7
    mkdir(FoldWrite);
end

%% write the data files (do not modify this part) 
xw = x'; yw=y'; uMeanw=uMean'; uStdw=uStd'; vMeanw=vMean'; vStdw=vStd'; 
savematrix=[xw(:) yw(:) uMeanw(:) vMeanw(:)];
savematrix(isnan(savematrix)) = 0;
fid=fopen([FoldWrite 'Mean' FileApp],'w');
fprintf(fid,'%s\n',['TITLE = "Mean"']);
fprintf(fid,'%s\n','VARIABLES = "X [mm]", "Y [mm]", "Vx [m/s]", "Vy [m/s]"');
fprintf(fid,'%s\n',['ZONE T="Frame 1", I=' num2str(I) ', J=' num2str(J) ', F=POINT']);
fprintf(fid,'%.3f %.3f %.5f %.5f\n',savematrix');
fclose(fid);

% Std
savematrix=[xw(:) yw(:) uStdw(:) vStdw(:)];
savematrix(isnan(savematrix)) = 0;
fid=fopen([FoldWrite 'Std' FileApp],'w');
fprintf(fid,'%s\n',['TITLE = "Std"']);
fprintf(fid,'%s\n','VARIABLES = "X [mm]", "Y [mm]", "Vx [m/s]", "Vy [m/s]"');
fprintf(fid,'%s\n',['ZONE T="Frame 1", I=' num2str(I) ', J=' num2str(J) ', F=POINT']);
fprintf(fid,'%.3f %.3f %.5f %.5f\n',savematrix');
fclose(fid);

%% figures

mask = load('WIDIM/Mask_Alpha_15');

% INSTANTENOUS U

figure(1)
subplot(1,2,1), contourf(x,y,u, 20, 'Linestyle', 'none'), axis equal, axis tight
colorbar;
xlabel('X [mm]','FontSize',14)
ylabel('Y [mm]','FontSize',14)
title(['u [m/s], Instantaneous'],'FontSize',14)
set(gca,'FontSize',12,'Ydir','normal');
hold on
quiver(x,y,u,v,'k');

% MEAN U

subplot(1,2,2), contourf(x,y,uMean, 20, 'Linestyle', 'none'), axis equal, axis tight
colorbar;
xlabel('X [mm]','FontSize',14)
ylabel('Y [mm]','FontSize',14)
title(['u [m/s], Mean'],'FontSize',14)
set(gca,'FontSize',12,'Ydir','normal');
hold on
quiver(x,y,uMean,vMean,'k');

% RMS FLUCTUATIONS

% subplot(1,2,2), contourf(x,y,sqrt(uStd.^2+vStd.^2), 20, 'Linestyle', 'none'), axis equal, axis tight
% colorbar;
% xlabel('X [mm]','FontSize',14)
% ylabel('Y [mm]','FontSize',14)
% title(['V'' RMS [m/s], Mean'],'FontSize',14)
% set(gca,'FontSize',12,'Ydir','normal');

% set(gcf, 'Position', get(0, 'Screensize'));
% set(gcf,'color','w')
% %exportgraphics(gcf,'prof_AoA_15_20s.eps','ContentType','vector')
% exportgraphics(gcf,'prof_AoA_15_20s.png')

%% study effect of time step

% % Read second data file
% FoldRead='./data/Alpha15_dt6/PIV_32x32_50%ov/'; % (*** fill in ***)
% first=20;    % (*** fill in ***) first velocity field to be analyzed
% last=20;     % (*** fill in ***) last velocity field to be analyzed
% 
% for i=first:last
%     iStr = num2str(i);
%     fprintf([iStr '\n']);
%     FileRead = [FileRoot ZeroStr(1:end-length(iStr)) iStr FileApp];
%     [x2,y2,u2,v2,I,J] = ReadDat_2C([FoldRead FileRead]);
% end
% 
% mask = load('WIDIM/Mask_Alpha_15');
% 
% % dt 6 vs. dt 100
% 
% figure(2)
% subplot(1,2,1), contourf(x2,y2,u2, 20, 'Linestyle', 'none'), axis equal, axis tight
% colorbar;
% xlabel('X [mm]','FontSize',14)
% ylabel('Y [mm]','FontSize',14)
% title(['dt = 6 [$\mu$s]'],'FontSize',14, 'Interpreter', 'latex')
% set(gca,'FontSize',12,'Ydir','normal');
% hold on
% quiver(x2,y2,u2,v2,'k');
% 
% subplot(1,2,2), contourf(x,y,u, 20, 'Linestyle', 'none'), axis equal, axis tight
% colorbar;
% xlabel('X [mm]','FontSize',14)
% ylabel('Y [mm]','FontSize',14)
% title(['dt = 100 [$\mu$s]'],'FontSize',14, 'Interpreter', 'latex')
% set(gca,'FontSize',12,'Ydir','normal');
% hold on
% quiver(x,y,u,v,'k');
% 
% set(gcf, 'Position', get(0, 'Screensize'));
% set(gcf,'color','w')
% %exportgraphics(gcf,'comp_dt.eps','ContentType','vector')
% exportgraphics(gcf,'comp_dt.png')

%% study effect of window size

% % Read second data file
% FoldRead='./data/Alpha0_dt100/PIV_16x16_50%ov/'; % (*** fill in ***)
% first=20;    % (*** fill in ***) first velocity field to be analyzed
% last=20;     % (*** fill in ***) last velocity field to be analyzed
% 
% for i=first:last
%     iStr = num2str(i);
%     fprintf([iStr '\n']);
%     FileRead = [FileRoot ZeroStr(1:end-length(iStr)) iStr FileApp];
%     [x2,y2,u2,v2,I,J] = ReadDat_2C([FoldRead FileRead]);
%     % initialization
% end
% 
% % Read third data file
% FoldRead='./data/Alpha0_dt100/PIV_64x64_50%ov/'; % (*** fill in ***)
% first=20;    % (*** fill in ***) first velocity field to be analyzed
% last=20;     % (*** fill in ***) last velocity field to be analyzed
% 
% for i=first:last
%     iStr = num2str(i);
%     fprintf([iStr '\n']);
%     FileRead = [FileRoot ZeroStr(1:end-length(iStr)) iStr FileApp];
%     [x3,y3,u3,v3,I,J] = ReadDat_2C([FoldRead FileRead]);
%     % initialization
% end
% 
% mask = load('WIDIM/Mask_Alpha_0');
% 
% % window size 16 vs 32 vs 64
% 
% figure(3)
% subplot(1,3,1), contourf(x2,y2,u2, 20, 'Linestyle', 'none'), axis equal, axis tight
% colorbar;
% caxis([min(u2,[],'all'), 12]);
% xlabel('X [mm]','FontSize',14)
% ylabel('Y [mm]','FontSize',14)
% title(['window size = 16 x 16 [px]'],'FontSize',14, 'Interpreter', 'latex')
% set(gca,'FontSize',12,'Ydir','normal');
% hold on
% quiver(x2,y2,u2,v2,'k');
% 
% subplot(1,3,2), contourf(x,y,u, 20, 'Linestyle', 'none'), axis equal, axis tight
% colorbar;
% caxis([min(u,[],'all'), 12]);
% xlabel('X [mm]','FontSize',14)
% ylabel('Y [mm]','FontSize',14)
% title(['window size = 32 x 32 [px]'],'FontSize',14, 'Interpreter', 'latex')
% set(gca,'FontSize',12,'Ydir','normal');
% hold on
% quiver(x,y,u,v,'k');
% 
% subplot(1,3,3), contourf(x3,y3,u3, 20, 'Linestyle', 'none'), axis equal, axis tight
% colorbar;
% caxis([min(u3,[],'all'), 12]);
% xlabel('X [mm]','FontSize',14)
% ylabel('Y [mm]','FontSize',14)
% title(['window size = 64 x 64 [px]'],'FontSize',14, 'Interpreter', 'latex')
% set(gca,'FontSize',12,'Ydir','normal');
% hold on
% quiver(x3,y3,u3,v3,'k');
% 
% set(gcf, 'Position', get(0, 'Screensize'));
% set(gcf,'color','w')
% %exportgraphics(gcf,'comp_ws.eps','ContentType','vector')
% exportgraphics(gcf,'comp_ws.png')

%% study effect of ensemble size

% % Compute second mean
% uMean2 = mean(uTot(:,:,1:10),3);
% vMean2 = mean(vTot(:,:,1:10),3);
% 
% mask = load('WIDIM/Mask_Alpha_15');
% 
% % ensemble size 10 vs. 100
% 
% figure(4)
% subplot(1,2,1), contourf(x,y,uMean2, 20, 'Linestyle', 'none'), axis equal, axis tight
% colorbar;
% caxis([-4, 12]);
% xlabel('X [mm]','FontSize',14)
% ylabel('Y [mm]','FontSize',14)
% title(['ensemble size = 10'],'FontSize',14, 'Interpreter', 'latex')
% set(gca,'FontSize',12,'Ydir','normal');
% hold on
% quiver(x,y,uMean2,vMean2,'k');
% 
% subplot(1,2,2), contourf(x,y,uMean, 20, 'Linestyle', 'none'), axis equal, axis tight
% colorbar;
% caxis([-4, 12]);
% xlabel('X [mm]','FontSize',14)
% ylabel('Y [mm]','FontSize',14)
% title(['ensemble size = 100'],'FontSize',14, 'Interpreter', 'latex')
% set(gca,'FontSize',12,'Ydir','normal');
% hold on
% quiver(x,y,uMean,vMean,'k');
% 
% set(gcf, 'Position', get(0, 'Screensize'));
% set(gcf,'color','w')
% %exportgraphics(gcf,'comp_ensemble.eps','ContentType','vector')
% exportgraphics(gcf,'comp_ensemble.png')