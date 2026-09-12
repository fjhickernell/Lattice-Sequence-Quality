% Efficient solution of Toeplitz linear systems using Levinson-Durbin algorithm

% Example usage
%n = 100;  % Larger matrix to demonstrate efficiency
%first_row = [2, 1, 0.5, 0.25, repmat(0.125, 1, n-4)];
n = 4; first_row = [2, 1, 0.5, 0.25];
first_col = first_row';
b = rand(n, 1);

% Measure computational time
tic;
x_efficient = efficient_toeplitz_solve(first_row, first_col, b);
time_efficient = toc;

tic;
A = toeplitz(first_row);
x_standard = A \ b;
time_standard = toc;

% Verify solution
disp('Maximum difference between solutions:');
disp(max(abs(x_efficient - x_standard)));

disp('Computational time (Efficient method):');
disp(time_efficient);

disp('Computational time (Standard method):');
disp(time_standard);