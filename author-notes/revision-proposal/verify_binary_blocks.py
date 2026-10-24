#!/usr/bin/env python3
"""Exact rational checks, not a substitute for proofs or large-scale experiments.

The rational Bernoulli factors define positive-spectrum Korobov kernels.
Their coordinate scaling differs from the manuscript's gamma convention;
the covariance/recursion identities are invariant under that choice.
Run with Python 3; no third-party packages are required.
"""
from fractions import Fraction as F


def bernoulli(x, alpha):
    if alpha == 2:
        return x**4 - 2*x**3 + x**2 - F(1, 30)
    if alpha == 3:
        return x**6 - 3*x**5 + F(5, 2)*x**4 - F(1, 2)*x**2 + F(1, 42)
    raise ValueError(alpha)


def kernel(x, h, alpha):
    value = F(1)
    for j, hj in enumerate(h, 1):
        t = (x * hj) % 1
        value *= 1 + (-1)**(alpha+1) * F(1, j*j) * bernoulli(t, alpha)
    return value


def radical_inverse(i):
    result, digit = F(0), F(1, 2)
    while i:
        result += (i % 2) * digit
        i //= 2
        digit /= 2
    return result


def levels(n):
    return [m for m in reversed(range(n.bit_length())) if n & (1 << m)]


def covariances(ms, ds):
    return [[ds[m] if r == q else
             2*ds[ms[min(r, q)]+1] - ds[ms[min(r, q)]]
             for q in range(len(ms))] for r, m in enumerate(ms)]


def optimize(ms, ds):
    e = ds[ms[-1]]
    ts = {}
    for r in reversed(range(len(ms)-1)):
        d = ds[ms[r]]
        c = 2*ds[ms[r]+1] - d
        assert e >= d > c
        denom = d + e - 2*c
        ts[r] = (e-c) / denom
        e = (d*e-c*c) / denom
    masses, remaining = [], F(1)
    for r in range(len(ms)-1):
        masses.append(remaining * ts[r])
        remaining *= 1-ts[r]
    masses.append(remaining)
    return e, masses


def quadratic(a, masses):
    return sum(masses[r]*a[r][q]*masses[q]
               for r in range(len(masses)) for q in range(len(masses)))


def main():
    checks = 0
    for alpha in (2, 3):
        for h in ((1,), (1, 3, 5)):
            maxn = 31
            xs = [radical_inverse(i) for i in range(maxn)]
            gram = [[kernel(x-y, h, alpha)-1 for y in xs] for x in xs]
            ds = [sum(kernel(F(j, 2**m), h, alpha)
                      for j in range(2**m)) / 2**m - 1 for m in range(6)]
            for n in range(1, maxn+1):
                ms = levels(n)
                a = covariances(ms, ds)
                blocks, start = [], 0
                for m in ms:
                    blocks.append(range(start, start+2**m))
                    start += 2**m
                for r, block in enumerate(blocks):
                    for q, other in enumerate(blocks):
                        direct = sum(gram[i][j] for i in block for j in other) / (
                            len(block)*len(other))
                        assert direct == a[r][q], (alpha, h, n, r, q)
                e, masses = optimize(ms, ds)
                assert sum(masses) == 1 and min(masses) > 0
                assert quadratic(a, masses) == e
                # Stationarity + positive definiteness verifies the same
                # constrained optimum as the dense HKKN12 expression.
                assert all(sum(row[q]*masses[q] for q in range(len(ms))) == e
                           for row in a)
                assert e <= ds[ms[0]]
                if len(ms) > 1:
                    assert e < ds[ms[0]]
                for power in (1, 2, 3, 4):
                    sizes = [F((2**m)**power) for m in ms]
                    trial = [x/sum(sizes) for x in sizes]
                    assert e <= quadratic(a, trial)
                checks += 1
    # 1D alpha=2, normalized by C=2*gamma^4*zeta(4).
    ds = [F(1, 2**(4*m)) for m in range(6)]
    e3, t3 = optimize([1, 0], ds)
    assert (e3, t3) == (F(13, 256), [F(9, 10), F(1, 10)])
    assert e3 > F(1, 3**4)  # Same dyadic leading constant is impossible.
    e13, t13 = optimize([3, 2, 0], ds)
    assert e13 == F(4421, 22347776)
    assert t13 == [F(613, 682), F(137, 1364), F(1, 1364)]
    assert e13/ds[3] == F(4421, 5456)
    # Banach objective is convex piecewise linear, with breakpoints 0, 1/2.
    for alpha in (2, 3):
        q = F(1, 2**alpha)
        p = lambda t: q*q + q*(1-q)*abs(1-2*t) + (1-q)*abs(t)
        assert p(F(0)) == q
        assert p(F(1, 2)) > q
        assert (1-q)*(1-2*q) > 0
    print(f"PASS: {checks} exact block-covariance, positivity, optimality, "
          "truncation, and power-weight comparisons.")
    print("PASS: n=3 and n=13 exact examples; Banach obstruction checks.")
    print("Novelty, floating-point stability, and large-scale performance remain open.")


if __name__ == "__main__":
    main()
