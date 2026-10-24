function [x] = efficient_toeplitz_solve(first_row, first_col, b)
    % Levinson-Durbin algorithm for solving Toeplitz systems
    % Complexity: O(n^2)

    n = length(b);
    x = zeros(n, 1);

    % Initial conditions
    f = zeros(n, n);  % Forward prediction error
    b_temp = zeros(n, n);  % Temporary storage

    f(1,1) = 1 / first_row(1);
    x(1) = b(1) * f(1,1);

    % Iterative solution
    for k = 2:n
        % Compute reflection coefficient
        lambda = 0;
        for j = 1:k-1
            lambda = lambda - first_row(k-j+1) * f(k-1,j);
        end
        lambda = lambda / first_row(1);

        % Update prediction error filter
        f(k,k) = -lambda;
        for j = 1:k-1
            f(k,j) = f(k-1,j) + lambda * f(k-1,k-j);
        end

        % Compute solution
        x(k) = b(k);
        for j = 1:k-1
            x(k) = x(k) - first_row(k-j+1) * x(j);
        end
        x(k) = x(k) * f(k,k);

        % Update previous solutions
        for j = 1:k-1
            x(j) = x(j) + f(k,k) * x(k-j);
        end
    end
end
