# PrimeClock Dynamics v0.2.0 Fixed-Cutoff Foundation

Status: public v0.2.0 fixed-cutoff foundation artifact. This note is not a
preprint, not a peer-reviewed result, not a DOI artifact, and not a Zenodo
record.

## Purpose

PrimeClock Dynamics starts from a prime-indexed circle model. At integer time
`n`, each prime `p` contributes a half-open arc on `T = R/Z` centered at
`(n mod p) / p`.

The North Star is:

```text
The twelve-o'clock fiber recovers omega(n), while the full circle defines an
angular family of residue-class prime-counting functions.
```

This v0.2.0 artifact records only the fixed-cutoff finite CRT foundation. It
does not prove a diagonal theorem for `D(n, alpha) = D_n(n, alpha)` or
`U(n) = U_n(n)`.

All fixed-cutoff statements below assume a finite set of distinct primes.

## Definitions

For a prime `p`, integer residue time `n >= 0`, and angle `alpha in T`, let
`I_p(n)` denote the half-open arc of radius `1/(2p)` centered at `(n mod p)/p`.

For cutoff `x`, let

```text
P_x = {p <= x : p prime},
M_x = prod_{p <= x} p.
```

The fixed-cutoff multiplicity field is

```text
D_x(n, alpha) = sum_{p <= x} 1_{alpha in I_p(n)}.
```

The fixed-cutoff uncovered measure is

```text
U_x(n) = measure({alpha in T : D_x(n, alpha) = 0}).
```

The diagonal app-level models

```text
D(n, alpha) = D_n(n, alpha),
U(n) = U_n(n)
```

are future targets and are not part of the v0.2.0 claim surface.

## PCD-FC-0: Twelve-O'clock Fiber

For integer time `n >= 2`,

```text
D(n, 0) = omega(n),
```

where `omega(n)` is the number of distinct prime divisors of `n`.

The half-open convention makes the twelve-o'clock membership condition

```text
0 in I_p(n) iff p divides n.
```

Summing over active primes `p <= n` gives the identity.

## PCD-FC-1: Fixed-Angle Residue Selector

For fixed `alpha` and prime `p`, define

```text
r_p(alpha) = floor(p alpha + 1/2) mod p.
```

With the repository's half-open point-membership convention,

```text
alpha in I_p(n) iff n mod p = r_p(alpha).
```

Thus each fixed angle selects exactly one residue class modulo each prime.
Endpoint ties are handled by the half-open convention.

## PCD-FC-2: Fixed-Cutoff CRT Mean And Variance

For fixed cutoff `x` and fixed angle `alpha`,

```text
D_x(n, alpha) = sum_{p <= x} 1_{n mod p = r_p(alpha)}.
```

Over the complete CRT period `0 <= n < M_x`, the residue coordinates
`n mod p` are uniform and independent. Therefore

```text
E[D_x(n, alpha)] = sum_{p <= x} 1/p,
Var(D_x(n, alpha)) = sum_{p <= x} (1/p)(1 - 1/p).
```

This is a finite fixed-cutoff statement only. It is not an Erdos-Kac CLT.

## PCD-FC-3: Fixed-Cutoff Two-Angle Covariance

For fixed angles `alpha` and `beta`, the complete-period covariance of
`D_x(n, alpha)` and `D_x(n, beta)` is the sum over primes `p <= x` of
prime-indexed contributions:

```text
if r_p(alpha) = r_p(beta):  (1/p)(1 - 1/p)
if r_p(alpha) != r_p(beta): -1/p^2.
```

This is the finite CRT covariance formula for the fixed-cutoff field. It is not
a Gaussian field result and not a finite-dimensional distribution theorem.

## PCD-MG-1: Fixed-Cutoff CRT Average Identity

For fixed cutoff `x`,

```text
(1 / M_x) sum_{0 <= n < M_x} U_x(n)
= prod_{p <= x}(1 - 1/p).
```

Proof route:

1. Average over the finite CRT period and integrate over `alpha`.
2. For almost every `alpha`, each prime `p <= x` removes one residue class
   modulo `p`.
3. CRT independence gives uncovered probability `prod_{p <= x}(1 - 1/p)` for
   that `alpha`.
4. Endpoint exceptions have measure zero and do not affect `U_x`.

This identity is a fixed-cutoff CRT average identity. It is not called a
Mertens law; the diagonal Mertens-scale problem is reserved for
`U(n) = U_n(n)`.

## PCD-MG-2: Finite-Window Periodic Discrepancy Bound

For fixed cutoff `x` and an integer window `[A, B]`, define

```text
L = B - A + 1 = q M_x + r,  0 <= r < M_x.
```

Since `U_x(n)` is periodic with period `M_x`, the complete periods contribute
exactly the complete-period average. Only the `r` remaining terms can create a
discrepancy. Because `0 <= U_x(n) <= 1`,

```text
|window_average(U_x; A, B) - prod_{p <= x}(1 - 1/p)| <= r / L.
```

This is a finite periodicity bound for fixed cutoff `x`. It is not a theorem
about the diagonal model `U(n) = U_n(n)`.

## Non-Claims

This v0.2.0 artifact does not claim:

- an Erdos-Kac CLT;
- a Gaussian field theorem;
- a Mertens asymptotic law;
- a diagonal theorem for `D(n,alpha)=D_n(n,alpha)`;
- a diagonal theorem for `U(n)=U_n(n)`;
- a random-model or non-randomness theorem;
- visual app evidence as mathematical evidence;
- peer review.

The v0.3 diagonal bridge and v0.4 random-control diagnostics remain future
research directions and are not part of the v0.2.0 public claim surface.
