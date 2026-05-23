# PrimeClock Dynamics v2.0.0: Angular Kubilius Chaos via Holomorphic Generating Functionals

Status: v2.0.0 public artifact manuscript. This is not a posted preprint and
not peer reviewed. If this version is archived separately on Zenodo, cite the
issued DOI for that deposited version.

## AKC-P1: Scope

This manuscript records the complete-CRT finite-beta Angular Kubilius Chaos
theorem surface. It uses the v1.2 holomorphic generating functional as an
analytic engine and recovers the v1.1 shrinking-angle Gaussian field as the
small-beta Gaussian tangent.

The positive claim surface is:

- `PCD-AKC-MART`: martingale random measures;
- `PCD-AKC-QPOINT`: q-point local factor / moment formula;
- `PCD-AKC-L2`: finite-beta L2 total-mass bound;
- `PCD-AKC-LIMIT`: weak convergence of complete-CRT random finite measures;
- `PCD-AKC-TANGENT`: Gaussian tangent recovery.

## AKC-P2: Complete-CRT AKC Measure

Let `(R_p)_p` be independent random variables with `R_p` uniform on
`Z/pZ`. For a real parameter `beta`, set `a=e^beta-1` and define

```text
W_{p,beta}(alpha)
= exp(beta 1_{R_p=r_p(alpha)}) / (1+a/p).
```

For a cutoff `x`, define the random measure

```text
mu_{x,beta}(d alpha) = product_{p <= x} W_{p,beta}(alpha) d alpha.
```

Equivalently,

```text
mu_{x,beta}(d alpha)
= exp(beta D_x(R,alpha)) / Z_x(beta) d alpha,
Z_x(beta)=product_{p <= x} (1+(e^beta-1)/p).
```

This normalization gives `E W_{p,beta}(alpha)=1` pointwise in `alpha`.

## AKC-P3: Theorem A, Martingale Random Measures

For every bounded Borel test function `f`,

```text
mu_{x,beta}(f) = int_T f(alpha) mu_{x,beta}(d alpha)
```

is a martingale as `x` increases through prime cutoffs.

Proof. When a new prime `q` is added, condition on all earlier residue
coordinates. The new factor has conditional expectation one at every angle:

```text
E[W_{q,beta}(alpha)] = 1.
```

Fubini applies because the finite-cutoff density is bounded for fixed `x` and
`beta`. Therefore the conditional expectation of the next cutoff integral is
the previous cutoff integral.

## AKC-P4: Theorem B, q-Point Moment Formula

For fixed angles `alpha_1,...,alpha_q`,

```text
E product_{j=1}^q rho_{x,beta}(alpha_j)
= product_{p <= x} L_{p,beta}(alpha_1,...,alpha_q),
```

where `rho_{x,beta}` is the density of `mu_{x,beta}` and

```text
L_{p,beta}
=
[ (1/p) sum_{r mod p} exp(beta #{j:r_p(alpha_j)=r}) ]
/ [1+(e^beta-1)/p]^q.
```

This is the real finite-beta slice of the v1.2 complete-CRT holomorphic
generating functional. It follows from prime-wise independence and the
selected-residue partition of the angle set at each prime.

## AKC-P5: Lemma C1, Two-Point Local Factor Decomposition

For two angles `alpha,gamma`, write `a=e^beta-1`. If
`r_p(alpha)=r_p(gamma)`, then

```text
M_p^coll = [1+(2a+a^2)/p] / [1+a/p]^2.
```

If `r_p(alpha)!=r_p(gamma)`, then

```text
M_p^sep = [1+2a/p] / [1+a/p]^2.
```

For fixed real `beta`, the denominators are uniformly bounded away from zero
for primes `p>=2`. In the separated case there is the exact identity

```text
M_p^sep - 1 = -a^2 / [p^2 (1+a/p)^2].
```

Thus separated primes do not create growth. In particular,

```text
M_p^sep <= 1 + C_beta p^-2,
M_p^coll <= 1 + C_beta p^-1.
```

The separated factors are uniformly harmless because `sum_p p^-2 < infinity`.
Only collision primes can produce growth, and the collision growth is at most
first order in `1/p`.

## AKC-P6: Lemma C2, Collision-Sum Bound

For distinct `alpha,gamma in T`, let

```text
delta = ||alpha-gamma||_T in (0,1/2].
```

Then

```text
sum_{p <= x, r_p(alpha)=r_p(gamma)} 1/p
<= C0 + C1 log log min(x, C2/delta).
```

Proof. The selected residue is the half-open nearest-grid selector

```text
r_p(theta) = floor(p theta + 1/2) mod p.
```

Each selected-residue cell for the nearest-grid selector has circular diameter
at most `1/p`. Therefore, if two non-identical angles lie in the same selected
cell, their circular distance is at most `1/p`, up to an absolute endpoint
constant caused by the half-open convention. Hence a collision implies
`p ||alpha-gamma||_T <= C`. The endpoint ambiguity affects only the assignment
of boundary points to half-open cells and is absorbed into the absolute
constant `C`; these boundary assignments also form a Lebesgue-null set in the
later two-point integration. Thus collision primes are contained in
`{p <= min(x, C / ||alpha-gamma||_T)}`. The reciprocal-prime estimate

```text
sum_{p <= y} 1/p = log log y + O(1)
```

then gives the bound, after enlarging constants for small `y`.

## AKC-P7: Theorem C, L2 Total-Mass Bound

For each fixed real `beta`,

```text
sup_x E[mu_{x,beta}(T)^2] < infinity.
```

Proof. By Fubini and the q-point formula,

```text
E[mu_{x,beta}(T)^2]
= int_T int_T E[rho_{x,beta}(alpha) rho_{x,beta}(gamma)] d alpha d gamma.
```

By Lemma C1, non-collision primes contribute a uniformly bounded product.
Collision primes contribute at most `1+C_beta/p` after absorbing finitely many
small primes. Hence

```text
E[rho_{x,beta}(alpha) rho_{x,beta}(gamma)]
<= C_beta exp(C_beta sum_{p <= x, collision} 1/p).
```

Using Lemma C2,

```text
E[rho_{x,beta}(alpha) rho_{x,beta}(gamma)]
<= C_beta (1 + log(1/delta))^{C_beta}
```

for `0<delta<=1/2`, uniformly in `x`. The diagonal has Lebesgue measure zero,
and

```text
int_0^{1/2} (1+log(1/t))^c dt < infinity
```

for every fixed finite `c`. This proves the uniform L2 total-mass bound.

## AKC-P8: Theorem D, Weak Convergence

For each fixed real `beta`, there is a random finite Borel measure `mu_beta`
on `T` such that

```text
mu_{x,beta} => mu_beta
```

weakly as `x` increases through prime cutoffs.

Proof. Let `V` be a countable `Q`-vector subspace of `C(T)`, containing `1`,
that is sup-norm dense in `C(T)`. For example, take rational trigonometric
polynomials or rational piecewise-linear functions on rational meshes.

For every `f in V`, Theorem A makes `mu_{x,beta}(f)` a martingale. The L2
total-mass bound gives

```text
sup_x E |mu_{x,beta}(f)|^2
<= ||f||_infty^2 sup_x E mu_{x,beta}(T)^2 < infinity.
```

Thus `mu_{x,beta}(f)` converges almost surely and in L2 for every `f in V`, on
a single probability-one event after taking a countable intersection. Denote
the limit by `L(f)`. Linearity and positivity pass to the limit on `V`.
Moreover,

```text
|L(f)| <= ||f||_infty L(1).
```

Therefore `L` extends uniquely to a positive bounded linear functional on
`C(T)`. By the Riesz representation theorem, `L` is integration against a
random finite Borel measure `mu_beta`.

For arbitrary `f in C(T)`, approximate `f` uniformly by elements of `V`. Since
`mu_{x,beta}(1)` converges to `L(1)=mu_beta(T)` on the same probability-one
event, the finite-cutoff total masses are eventually bounded there. The
uniform approximation error is controlled by that eventual bound and
`mu_beta(T)`, and then `epsilon -> 0` gives `mu_{x,beta}(f)->mu_beta(f)`.
This is weak convergence on the compact circle.

## AKC-P9: Theorem E, Gaussian Tangent Recovery

The small-beta second-order expansion of the q-point formula recovers the v1.1
collision kernel. Equivalently, the Hessian of the v1.2 HCGF at zero recovers
the complete-CRT covariance:

```text
partial_i partial_j log G_x(0;alpha)
= K_x(alpha_i, alpha_j),  i != j.
```

Thus v1.1 is the Gaussian tangent, v1.2 is the holomorphic generating engine,
and v2.0 is the finite-beta AKC random-measure theorem surface.

## AKC-P10: Support Evidence

The public artifact includes deterministic support rows for:

1. martingale interval checks;
2. q-point moment formula exact enumeration;
3. L2 total-mass stability diagnostics;
4. two-point kernel integrability diagnostics;
5. weak convergence test-function diagnostics;
6. Gaussian tangent recovery diagnostics.

These support rows are reproducibility checks, not additional theorem claims.

## AKC-P11: Explicit Non-Claims

This public artifact manuscript does not claim integer-time finite-beta transfer,
diagonal Mertens uncovered-measure theorem, beta-to-negative-infinity uncovered
theorem, high-point theorem, Fisher-zero theorem, Lee-Yang theorem, prime-time
theorem, standard Gaussian Multiplicative Chaos, a result about prime gaps, a
result about the Riemann hypothesis, posted preprint, or peer review.
