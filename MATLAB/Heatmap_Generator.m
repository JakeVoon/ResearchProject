% Data
Y = [0 0.5 2.0 4.5 6.5 11.0 7.9 5.4 2.1 0];

% Generate heatmap
imagesc(Z); 
axis equal
axis off; 
xlabel('Force (N)')
colorbar('southoutside');

%% 
% Data
Y = [0 0.5 2.0 4.5 6.5 11.0 7.9 5.4 2.1 0];

% Interpolate data, smoother heatmap
X = linspace(0,10,500);
Y = interp1(Y,X); 

Z = [Y;Y];
for n = 1:50 % Defines number of rows of the heatmap array (more = thicker bar)
    Z = [Z;Y];
end

% Generate heatmap
imagesc(Y); 
axis equal
axis off; 
xlabel('Force (N)')
colorbar('southoutside');