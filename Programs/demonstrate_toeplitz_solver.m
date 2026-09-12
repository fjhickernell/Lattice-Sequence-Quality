function demonstrate_toeplitz_solver()
    % Test cases with different matrix sizes
    test_sizes = [3, 5, 10, 20];

    for n = test_sizes
        % Create a symmetric positive definite Toeplitz matrix
        c = [2; 1 * ones(n-1, 1)];  % First column
        r = c';  % First row (symmetric)

        % Create random right-hand side
        b = rand(n, 1);

        % Construct full matrix for comparison
        A = toeplitz(c);

        % Solve using our method
        x_levinson = stable_toeplitz_solve(c, r, b);

        % Solve using standard backslash
        x_standard = A \ b;

        % Compute and display error
        fprintf('Matrix size: %d\n', n);
        fprintf('Max absolute difference: %e\n', max(abs(x_levinson - x_standard)));
        fprintf('Relative error: %e\n\n', norm(x_levinson - x_standard) / norm(x_standard));
    end
end
