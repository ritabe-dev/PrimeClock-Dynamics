# PrimeClock Dynamics v1.1.0: A Shrinking-Angle Gaussian Field

Status: v1.1.0 public research artifact manuscript. This is not a DOI
artifact, Zenodo record, posted preprint, or peer-reviewed result.

The artifact version is `v1.1.0`. Package metadata is aligned to `1.1.0` and
does not enlarge the theorem surface.

## Abstract

This manuscript records a complete-CRT shrinking-angle Gaussian theorem for
PrimeClock Dynamics. For moving angles, the covariance is governed by the exact
prime-indexed collision kernel. If the normalized collision-kernel matrix
converges, the normalized complete-CRT multiplicity vector converges to the
corresponding centered Gaussian vector. A zero-ray family
`delta_x = exp(-(log x)^theta)` gives an explicit shrinking-angle corollary
with limiting covariance parameter `theta`.

## 1. Model

For a prime `p` and an angle `alpha in R/Z`, define

```text
r_p(alpha) = floor(p alpha + 1/2) mod p.
```

For a cutoff `x`, write

```text
M_x = product_{p <= x} p,
D_x(n, alpha) = sum_{p <= x} 1_{n mod p = r_p(alpha)}.
```

The model in this manuscript is complete-CRT: `n` is uniform on `Z/M_x Z`.
Then the residues `n mod p` are independent and uniform as `p` ranges over
primes `p <= x`.

Set

```text
A_x = sum_{p <= x} 1/p,
B_x^2 = sum_{p <= x} (1/p)(1 - 1/p).
```

## 2. Collision Kernel

For two possibly moving angles, define

```text
K_x(alpha, beta)
  = sum_{p <= x} (1_{r_p(alpha)=r_p(beta)} / p - 1/p^2).
```

This is exactly the complete-CRT covariance of `D_x(n, alpha)` and
`D_x(n, beta)`. If the two angles select the same residue modulo `p`, the
prime contribution is `(1/p)(1-1/p)`. Otherwise it is `-1/p^2`.

## 3. Main Theorem

**Theorem A: kernel-conditioned complete-CRT Gaussian limit.**
Fix `d >= 1`. For each cutoff `x`, let

```text
alpha_1(x), ..., alpha_d(x) in R/Z
```

be an angle array. Suppose that, for all `1 <= i,j <= d`,

```text
K_x(alpha_i(x), alpha_j(x)) / B_x^2 -> kappa_ij.
```

Then `kappa` is positive semidefinite with diagonal entries `1`, and

```text
((D_x(n, alpha_i(x)) - A_x) / B_x)_{i=1}^d
  => N(0, kappa)
```

in the complete-CRT model.

## 4. Proof

Fix Cramer-Wold coefficients `t=(t_1,...,t_d)` and write

```text
S_x(t) = sum_i t_i (D_x(n, alpha_i(x)) - A_x)
       = sum_{p <= x} Z_{p,x}(t),
```

where

```text
Z_{p,x}(t)
  = sum_i t_i (1_{n mod p = r_p(alpha_i(x))} - 1/p).
```

The variables `Z_{p,x}(t)` are independent over primes, centered, and uniformly
bounded by a constant depending only on `t` and `d`. Their variance is

```text
V_x(t) = sum_{i,j} t_i t_j K_x(alpha_i(x), alpha_j(x)).
```

The kernel convergence assumption gives

```text
V_x(t) / B_x^2 -> t^T kappa t.
```

If `t^T kappa t > 0`, then `V_x(t) -> infinity`. Since the summands are
uniformly bounded, Lindeberg's condition is immediate, and

```text
S_x(t) / sqrt(V_x(t)) => N(0,1).
```

Slutsky's theorem gives

```text
S_x(t) / B_x => N(0, t^T kappa t).
```

If `t^T kappa t = 0`, then

```text
Var(S_x(t)/B_x) -> 0,
```

so `S_x(t)/B_x -> 0` in `L^2` and in probability. Thus every fixed
Cramer-Wold projection has the prescribed Gaussian limit, including degenerate
directions. Cramer-Wold proves the vector convergence. The limiting matrix is
positive semidefinite because it is the limit of normalized covariance
matrices, and its diagonal entries are `1` because
`K_x(alpha_i(x), alpha_i(x)) = B_x^2`.

## 5. Zero-Ray Shrinking Corollary

Let

```text
alpha_x = 0,
beta_x = delta_x = exp(-(log x)^theta),
0 < theta < 1.
```

With the half-open residue-cell convention,

```text
r_p(0)=r_p(delta_x)  iff  p delta_x < 1/2.
```

Therefore

```text
K_x(0, delta_x)
  = sum_{p <= x, p delta_x < 1/2} 1/p - sum_{p <= x} 1/p^2.
```

Endpoint conventions can affect only equality cases and do not change the
normalized limit. Since

```text
1/(2 delta_x) = (1/2) exp((log x)^theta),
```

the standard reciprocal-prime estimate

```text
sum_{p <= y} 1/p = log log y + O(1)
```

and convergence of `sum_p 1/p^2` imply

```text
K_x(0, delta_x) / B_x^2 -> theta.
```

By Theorem A,

```text
((D_x(n,0)-A_x)/B_x, (D_x(n,delta_x)-A_x)/B_x)
  => N(0, [[1, theta], [theta, 1]]).
```

This corollary is the concrete shrinking-angle content of v1.1. General
distance-only kernel laws remain outside the claim surface.

## 6. Boundary

This manuscript does not claim integer-time transfer, diagonal
shrinking-angle Angular Erdos-Kac, finite-beta Angular Kubilius Chaos, standard
Gaussian Multiplicative Chaos, uniform-in-alpha convergence, a full Gaussian
field theorem, arbitrary distance-only kernel asymptotics, diagonal Mertens
laws, high-point asymptotics, prime-time theorems, DOI, Zenodo publication,
posted preprint, or peer review.

## 7. References

- P. Erdos and M. Kac, The Gaussian law of errors in the theory of additive
  number theoretic functions, 1940.
- J. Kubilius, Probabilistic Methods in the Theory of Numbers, 1964.
- G. Tenenbaum, Introduction to Analytic and Probabilistic Number Theory.
- H. Halberstam and H.-E. Richert, Sieve Methods.
