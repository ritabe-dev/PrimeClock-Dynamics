# Shrinking-Angle Gaussian Field Math Specification

Status: v1.1.0 public artifact math specification. This is not a DOI artifact,
Zenodo record, posted preprint, or peer-reviewed result.

## Complete-CRT Model

Let `T = R/Z`. For a prime `p` and angle `alpha in T`, define

```text
r_p(alpha) = floor(p alpha + 1/2) mod p.
```

For a cutoff `x`, set

```text
P_x = {p prime : p <= x}
M_x = product_{p <= x} p
D_x(n, alpha) = sum_{p <= x} 1_{n mod p = r_p(alpha)}.
```

The v1.1 theorem is in the complete-CRT model: `n` is uniform on
`Z/M_x Z`. Integer-time and diagonal transfer are outside this public artifact.

Define

```text
A_x = sum_{p <= x} 1/p
B_x^2 = sum_{p <= x} (1/p)(1 - 1/p).
```

## Collision Kernel

For possibly moving angles, define

```text
K_x(alpha, beta)
  = sum_{p <= x} (1_{r_p(alpha)=r_p(beta)} / p - 1/p^2).
```

This is exactly the complete-CRT covariance of `D_x(n, alpha)` and
`D_x(n, beta)`.

## Main Theorem Surface

For angle arrays `alpha_i(x)`, if

```text
K_x(alpha_i(x), alpha_j(x)) / B_x^2 -> kappa_ij
```

for all `i,j`, then

```text
((D_x(n, alpha_i(x)) - A_x) / B_x)_i
```

converges in distribution, in the complete-CRT model, to a centered Gaussian
vector with covariance matrix `kappa`.

## Zero-Ray Corollary

For

```text
alpha_x = 0,
beta_x = delta_x = exp(-(log x)^theta),
0 < theta < 1,
```

the half-open cell convention gives

```text
r_p(0)=r_p(delta_x)  iff  p delta_x < 1/2.
```

Using the reciprocal-prime estimate

```text
sum_{p <= y} 1/p = log log y + O(1),
```

and the convergence of `sum_p 1/p^2`, one obtains

```text
K_x(0, delta_x) / B_x^2 -> theta.
```

Therefore the two-point normalized complete-CRT vector converges to the
centered Gaussian vector with covariance matrix

```text
[[1, theta], [theta, 1]].
```
