#!/usr/bin/env python3
"""Check the recursive circulant solver for binary lattice prefixes.

Run with Python 3; no third-party packages are required:
    python3 author-notes/revision-proposal/verify_fft_prefixes.py

Conventions: a full H-point lattice is indexed in natural cyclic order,
C[i,j] = c[(i-j) % H], and its eigenvalues are fft(c), with the forward
transform using exp(-2*pi*i*j*k/H). H is a power of two. The first n points
in radical-inverse order correspond to natural indices bit_reverse(i),
0 <= i < n. Right-hand sides and returned solutions use that prefix order.

The solver takes a strictly positive real, even circulant spectrum. It
supports arbitrary real right-hand sides. At each level, restriction to
the even subgroup uses arithmetic means of paired eigenvalues; eliminating
that complete subgroup uses harmonic means. Constant right-hand sides use
an equivalent reduced-right-hand-side ratio that avoids subtracting a
number near one. This is a verification prototype, not a stability theorem.
In particular, an FFT of rounded kernel samples can corrupt small positive
eigenvalues. Invalid spectra are rejected, never clipped or regularized.
Roundoff-level mismatches of mirrored positive eigenvalues are averaged
solely to enforce the stipulated real symmetry.
"""

import argparse
import cmath
import math
import random
import sys
from fractions import Fraction as F

from verify_binary_blocks import kernel, levels, optimize, radical_inverse


def fft(values):
    """Unnormalized radix-2 forward transform; complex input is allowed."""
    n = len(values)
    if n < 1 or n & (n - 1):
        raise ValueError("FFT length must be a positive power of two")
    if n == 1:
        return [complex(values[0])]
    even, odd = fft(values[::2]), fft(values[1::2])
    rotated = [cmath.exp(-2j * math.pi * k / n) * odd[k]
               for k in range(n // 2)]
    return ([even[k] + rotated[k] for k in range(n // 2)]
            + [even[k] - rotated[k] for k in range(n // 2)])


def ifft(values):
    return [z.conjugate() / len(values)
            for z in fft([complex(x).conjugate() for x in values])]


def bit_reverse_indices(size):
    """Natural cyclic indices of a complete radical-inverse prefix."""
    if size < 1 or size & (size - 1):
        raise ValueError("Lattice size must be a positive power of two")
    if size == 1:
        return [0]
    half = bit_reverse_indices(size // 2)
    return [2 * j for j in half] + [2 * j + 1 for j in half]


def _checked_spectrum(eigenvalues):
    size = len(eigenvalues)
    if size < 1 or size & (size - 1):
        raise ValueError("Spectrum length must be a positive power of two")
    result = [float(x) for x in eigenvalues]
    if any(not math.isfinite(x) or x <= 0 for x in result):
        raise ValueError("Every circulant eigenvalue must be finite and positive")
    tolerance = 128 * sys.float_info.epsilon * max(result)
    if any(abs(result[k] - result[-k % size]) > tolerance
           for k in range(size)):
        raise ValueError("A real symmetric circulant needs an even spectrum")
    # The stipulated real symmetry is exact mathematically. In particular,
    # tiny eigenvalues computed by FFT can have mirrored roundoff differences
    # that would otherwise introduce artificial imaginary solution components.
    # Check positivity BEFORE this averaging: a bad eigenvalue is not repaired.
    for k in range(1, size // 2):
        lo, hi = sorted((result[k], result[size - k]))
        result[k] = result[size - k] = lo + (hi - lo) / 2
    return result


def _real_values(values):
    """Check the imaginary roundoff before returning a real vector."""
    scale = max((abs(x) for x in values), default=0.0)
    tolerance = 256 * sys.float_info.epsilon * max(scale, sys.float_info.min)
    if any(not math.isfinite(x.real) or not math.isfinite(x.imag)
           or abs(x.imag) > tolerance for x in values):
        raise ArithmeticError("Nonfinite result or excessive imaginary residual")
    return [x.real for x in values]


def solve_circulant_prefix(eigenvalues, rhs):
    """Solve the n-point bit-reversed principal system, without forming it.

    The usual arithmetic count is O(H log H), with O(H) working storage.
    For the smallest dyadic ambient size H >= n, this is O(n log n).
    Numerical stability and conditioning are not established by this count.
    """
    spectrum = _checked_spectrum(eigenvalues)
    right = [float(x) for x in rhs]
    if not 1 <= len(right) <= len(spectrum):
        raise ValueError("Right-hand-side length must be between 1 and H")
    if any(not math.isfinite(x) for x in right):
        raise ValueError("Right-hand side must be finite")
    return _solve_prefix(spectrum, right)


def _solve_prefix(spectrum, rhs):
    size, n = len(spectrum), len(rhs)
    constant = all(x == rhs[0] for x in rhs)
    if n == size and constant:
        value = rhs[0] / spectrum[0]
        if not math.isfinite(value):
            raise ArithmeticError("Nonfinite constant solution")
        return [value] * n
    if n == size:
        order = bit_reverse_indices(size)
        natural_rhs = [0.0] * size
        for j, value in zip(order, rhs):
            natural_rhs[j] = value
        natural_solution = _real_values(ifft(
            [value / lam for value, lam in zip(fft(natural_rhs), spectrum)]))
        return [natural_solution[j] for j in order]

    half = size // 2
    # Means written this way avoid overflow of x+y for finite positive inputs.
    pairs = [(min(x, y), max(x, y))
             for x, y in zip(spectrum[:half], spectrum[half:])]
    subgroup = [lo + (hi - lo) / 2 for lo, hi in pairs]
    if n <= half:
        return _solve_prefix(subgroup, rhs)

    # In even/odd order C=[[A,B],[B*,A]]. In the half-size Fourier
    # basis, B/A has the following phase and signed spectral ratio.
    coupling = [cmath.exp(-1j * math.pi * k / half)
                * (((spectrum[k] - spectrum[k + half]) / subgroup[k]) / 2)
                for k in range(half)]
    # A-B* A^{-1}B: harmonic means avoid subtracting nearly equal terms.
    schur = [lo / (0.5 + 0.5 * (lo / hi)) for lo, hi in pairs]
    if any(not math.isfinite(x) or x <= 0 for x in schur):
        raise ArithmeticError("Nonpositive or nonfinite Schur eigenvalue")

    order = bit_reverse_indices(half)
    tail_size = n - half
    if constant:
        # 1-(lambda_0-lambda_half)/(lambda_0+lambda_half)
        # = lambda_half/subgroup_0; use the latter directly.
        reduced_value = rhs[0] * (spectrum[half] / subgroup[0])
        reduced_rhs = [reduced_value] * tail_size
        even_inverse_spectrum = [0j] * half
        even_inverse_spectrum[0] = half * (rhs[0] / subgroup[0])
    else:
        natural_even_rhs = [0.0] * half
        for j, value in zip(order, rhs[:half]):
            natural_even_rhs[j] = value
        even_rhs_spectrum = fft(natural_even_rhs)
        cross = _real_values(ifft([
            z.conjugate() * value
            for z, value in zip(coupling, even_rhs_spectrum)]))
        reduced_rhs = [rhs[half + i] - cross[order[i]]
                       for i in range(tail_size)]
        even_inverse_spectrum = [value / lam
                                 for value, lam in zip(even_rhs_spectrum, subgroup)]

    tail = _solve_prefix(schur, reduced_rhs)
    natural_tail = [0.0] * half
    for j, value in zip(order, tail):
        natural_tail[j] = value
    even_solution = _real_values(ifft([
        value - z * other
        for value, z, other in zip(even_inverse_spectrum, coupling,
                                   fft(natural_tail))]))
    return [even_solution[j] for j in order] + tail


def optimal_point_weights(eigenvalues, n):
    solution = solve_circulant_prefix(eigenvalues, [1.0] * n)
    total = math.fsum(solution)
    if not math.isfinite(total) or total <= 0:
        raise ArithmeticError("Nonpositive or nonfinite normalizing denominator")
    return [x / total for x in solution]


def spectrum_from_column(column):
    """Prototype kernel-sample path; does not repair inaccurate eigenvalues."""
    return _checked_spectrum(_real_values(fft(column)))


def dense_solve(matrix, rhs):
    """Independent dense elimination with partial pivoting, for checks only."""
    rows = [list(row) + [value] for row, value in zip(matrix, rhs)]
    n = len(rhs)
    for k in range(n):
        pivot = max(range(k, n), key=lambda i: abs(rows[i][k]))
        rows[k], rows[pivot] = rows[pivot], rows[k]
        if rows[k][k] == 0:
            raise ArithmeticError("Singular dense reference system")
        for i in range(k + 1, n):
            factor = rows[i][k] / rows[k][k]
            for j in range(k + 1, n + 1):
                rows[i][j] -= factor * rows[k][j]
    solution = [0.0] * n
    for i in reversed(range(n)):
        solution[i] = (rows[i][n] - math.fsum(
            rows[i][j] * solution[j] for j in range(i + 1, n))) / rows[i][i]
    return solution


def norm(values):
    return math.sqrt(math.fsum(x * x for x in values))


def relative_difference(actual, expected):
    return norm([x - y for x, y in zip(actual, expected)]) / norm(expected)


def relative_residual(matrix, solution, rhs):
    return norm([math.fsum(x * y for x, y in zip(row, solution)) - value
                 for row, value in zip(matrix, rhs)]) / norm(rhs)


def check_random_systems(max_size, trials, seed):
    rng = random.Random(seed)
    count, worst_difference, worst_residual = 0, 0.0, 0.0
    for exponent in range(max_size.bit_length()):
        size = 1 << exponent
        order = bit_reverse_indices(size)
        for _ in range(trials):
            raw = [math.exp(rng.uniform(-3, 3)) for _ in range(size)]
            spectrum = [(raw[k] + raw[-k % size]) / 2 for k in range(size)]
            column = _real_values(ifft(spectrum))
            for n in range(1, size + 1):
                matrix = [[column[(i - j) % size] for j in order[:n]]
                          for i in order[:n]]
                for rhs in ([1.0] * n, [rng.gauss(0, 1) for _ in range(n)]):
                    actual = solve_circulant_prefix(spectrum, rhs)
                    expected = dense_solve(matrix, rhs)
                    difference = relative_difference(actual, expected)
                    residual = relative_residual(matrix, actual, rhs)
                    worst_difference = max(worst_difference, difference)
                    worst_residual = max(worst_residual, residual)
                    assert difference < 5e-11 and residual < 5e-11, (
                        size, n, difference, residual)
                    count += 1
    return count, worst_difference, worst_residual


def check_korobov_systems():
    # These rational Bernoulli kernels have positive Korobov spectra. Their
    # coordinate scaling is documented in verify_binary_blocks.py.
    size = 16
    xs = [radical_inverse(i) for i in range(size)]
    count, worst_difference, worst_residual = 0, 0.0, 0.0
    worst_ratio, example_ratios = 0.0, []
    for alpha in (2, 3):
        for generator in ((1,), (1, 3, 5)):
            exact_gram = [[kernel(x - y, generator, alpha) - 1 for y in xs]
                          for x in xs]
            column = [float(kernel(F(j, size), generator, alpha))
                      for j in range(size)]
            spectrum = spectrum_from_column(column)
            ds = [sum(kernel(F(j, 1 << m), generator, alpha)
                      for j in range(1 << m)) / (1 << m) - 1
                  for m in range(size.bit_length())]
            for n in range(1, size + 1):
                matrix = [[float(value + 1) for value in row[:n]]
                          for row in exact_gram[:n]]
                weights = optimal_point_weights(spectrum, n)
                dense = dense_solve(matrix, [1.0] * n)
                dense_total = math.fsum(dense)
                dense_weights = [x / dense_total for x in dense]
                difference = relative_difference(weights, dense_weights)
                # The unnormalized solve is checked against the original K.
                solution = solve_circulant_prefix(spectrum, [1.0] * n)
                residual = relative_residual(matrix, solution, [1.0] * n)
                worst_difference = max(worst_difference, difference)
                worst_residual = max(worst_residual, residual)
                assert difference < 1e-6 and residual < 1e-9, (
                    alpha, generator, n, difference, residual)

                # Evaluate errors with exact rational kernel entries and exact
                # representations of the computed float weights. This avoids
                # masking comparisons by a rounded w^T K w - 1 subtraction.
                rational_weights = [F.from_float(w) for w in weights]
                error = sum(rational_weights[i] * rational_weights[j]
                            * exact_gram[i][j] for i in range(n) for j in range(n))
                error += (sum(rational_weights) - 1) ** 2
                block_error, _ = optimize(levels(n), ds)
                ratio = float(error / block_error)
                worst_ratio = max(worst_ratio, ratio)
                assert error >= 0 and ratio <= 1 + 1e-7, (
                    alpha, generator, n, ratio)
                if alpha == 2 and generator == (1,) and n in (5, 13):
                    example_ratios.append((n, ratio))
                count += 1
    return count, worst_difference, worst_residual, worst_ratio, example_ratios


def check_rejections():
    count = 0
    for spectrum in ([1.0, 0.0], [1.0, -1.0],
                     [1.0, math.nan], [1.0, math.inf]):
        try:
            solve_circulant_prefix(spectrum, [1.0])
        except ValueError:
            count += 1
        else:
            raise AssertionError("Invalid eigenvalue was not rejected")
    return count


def check_exact_five_point_example():
    """Exhibit the distinction between the block and unrestricted optima."""
    xs = [radical_inverse(i) for i in range(5)]
    gram = [[kernel(x - y, (1,), 2) - 1 for y in xs] for x in xs]
    block = [F(x, 552) for x in (137, 137, 137, 137, 4)]
    full = [F(x, 544) for x in (117, 139, 117, 139, 32)]
    assert sum(block) == sum(full) == 1
    squared_error = lambda w: sum(w[i] * gram[i][j] * w[j]
                                  for i in range(5) for j in range(5))
    full_error, block_error = squared_error(full), squared_error(block)
    # With positive definite Gram, constant A*w proves constrained optimality.
    assert all(sum(row[j] * full[j] for j in range(5)) == full_error
               for row in gram)
    ds = [sum(kernel(F(j, 1 << m), (1,), 2) for j in range(1 << m))
          / (1 << m) - 1 for m in range(4)]
    recursive_error, masses = optimize(levels(5), ds)
    assert block == [masses[0] / 4] * 4 + [masses[1]]
    assert block_error == recursive_error
    # For this kernel kappa=1-B_4, C=d_0=1/30.
    scale = F(1, 30)
    assert full_error / scale == F(121, 34816)
    assert block_error / scale == F(363, 94208)
    assert full_error / block_error == F(46, 51)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-size", type=int, default=32,
                        help="Largest random-test dyadic ambient size (default: 32)")
    parser.add_argument("--trials", type=int, default=3,
                        help="Random spectra per ambient size (default: 3)")
    parser.add_argument("--seed", type=int, default=20421)
    args = parser.parse_args()
    if args.max_size < 1 or args.max_size & (args.max_size - 1) or args.trials < 1:
        parser.error("--max-size must be a positive power of two; --trials >= 1")
    count, difference, residual = check_random_systems(
        args.max_size, args.trials, args.seed)
    print(f"PASS: {count} random SPD-circulant prefix solves "
          f"(all prefixes, H <= {args.max_size}; ones and random RHS).")
    print(f"  Worst relative dense-solution difference: {difference:.3e}; "
          f"relative residual: {residual:.3e}.")
    count, difference, residual, ratio, examples = check_korobov_systems()
    print(f"PASS: {count} Bernoulli/Korobov prefix weight checks "
          "(alpha=2,3; s=1,3; every n=1,...,16).")
    print(f"  Worst relative dense-weight difference: {difference:.3e}; "
          f"relative residual: {residual:.3e}.")
    print(f"  Largest computed full/block squared-error ratio: {ratio:.12g}.")
    for n, value in examples:
        print(f"  1D alpha=2, n={n}: full/block squared-error ratio {value:.12g}.")
    check_exact_five_point_example()
    print("PASS: exact n=5 block/full weight vectors, normalization, full "
          "stationarity, and squared-error ratio 46/51.")
    print(f"PASS: {check_rejections()} nonpositive/nonfinite spectra rejected.")
    print("Novelty, floating-point stability, and large-scale performance remain open.")


if __name__ == "__main__":
    main()
