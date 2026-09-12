function [x] = stable_toeplitz_solve(c, r, b)
    % Robust Levinson-Durbin algorithm for solving Toeplitz systems
    % Inputs:
    %   c: First column of Toeplitz matrix
    %   r: First row of Toeplitz matrix
    %   b: Right-hand side vector

    n = length(b);

    % Validate inputs
    if length(c) ~= n || length(r) ~= n
        error('Input vector lengths must match');
    end

    % Ensure first elements of c and r are identical (symmetric matrix)
    if c(1) ~= r(1)
        error('First elements of column and row must be the same');
    end

    % Initialize arrays
    x = zeros(n, 1);
    a = zeros(n, n);  % Reflection coefficients
    v = zeros(n+1, 1);  % Forward prediction errors

    % Initial conditions
    v(1) = 1;
    v(2) = -r(2) / c(1);
    a(1,1) = v(2);
    x(1) = b(1) / c(1);

    % Iterative solution
    for k = 2:n
        % Compute reflection coefficient
        lambda = 0;
        for j = 1:k-1
            lambda = lambda - r(k+1-j) * a(k-1, j);
        end
        lambda = lambda / c(1);

        % Update v vector
        v(k+1) = -lambda;
        for j = 1:k-1
            v(k+1-j) = v(k+1-j) + lambda * v(k+1-j+1);
        end

        % Store reflection coefficient
        a(k,k) = lambda;
        for j = 1:k-1
            a(k,j) = a(k-1,j) + lambda * a(k-1,k-j);
        end

        % Compute solution
        x(k) = b(k);
        for j = 1:k-1
            x(k) = x(k) - r(k+1-j) * x(j);
        end
        x(k) = x(k) / c(1);

        % Update previous solutions
        for j = 1:k-1
            x(j) = x(j) + lambda * x(k-j+1);
        end
    end
end
