# PrimeClock Dynamics v3.0.0:
# The Mertens Boundary of Angular Kubilius Chaos

Subtitle: Mertens-Normalized Uncovered Measures in the Complete-CRT Model

Status: v3.0.0 public artifact manuscript. Gate C and Gate P reviews passed. This artifact is not a posted preprint and is not peer reviewed.

## MB-C1: Scope

This public artifact records the complete-CRT theorem surface for the hard
uncovered endpoint of v2.0 finite-beta Angular Kubilius Chaos.

The central object is

```text
nu_x(d alpha)
  = 1_{D_x(R, alpha)=0} / P_x d alpha,
P_x = product_{p <= x}(1 - 1/p).
```

The surface is complete-CRT only. It does not claim integer-time transfer,
diagonal Mertens laws, high-point theorems, Fisher-zero theorems, Lee-Yang
theorems, or a new proof of the classical Mertens product theorem.

## MB-C2: Definitions and Boundary Convention

Let

```text
Omega = product_p Z/pZ
```

with independent uniform coordinates `R_p`. Define

```text
D_x(R, alpha) = sum_{p <= x} 1_{R_p = r_p(alpha)}
P_x = product_{p <= x}(1 - 1/p)
V_p(alpha) = (1 - 1_{R_p = r_p(alpha)}) / (1 - 1/p)
nu_x(d alpha) = product_{p <= x} V_p(alpha) d alpha.
```

Equivalently, `nu_x(d alpha) = 1_{D_x(R,alpha)=0} P_x^{-1} d alpha`.

For each prime `p` and residue `r mod p`, the selected-residue cell is

```text
C_{p,r} = [(r - 1/2)/p, (r + 1/2)/p) mod 1.
```

Pointwise statements use this half-open convention:

```text
r_p(alpha) = floor(p alpha + 1/2) mod p.
```

For integrated quantities, endpoint assignments are immaterial. At finite
cutoff the boundary set is finite and has Lebesgue measure zero. Exact cell
integrals cut at all boundaries and evaluate any interior point of each open
cell.

## MB-C3: Theorem A, Martingale Random Measures

For every bounded Borel function `f`,

```text
nu_x(f) = int_T f(alpha) nu_x(d alpha)
```

is a nonnegative martingale in the prime cutoff filtration.

Proof. It is enough to add one new prime `q`. For fixed `alpha`,

```text
E[V_q(alpha)] = P(R_q != r_q(alpha)) / (1 - 1/q) = 1.
```

The new coordinate `R_q` is independent of the previous prime coordinates.
For bounded Borel `f`, conditional Fubini gives

```text
E[ int f(alpha) V_q(alpha) nu_x(d alpha) | F_x ]
  = int f(alpha) E[V_q(alpha)] nu_x(d alpha)
  = nu_x(f).
```

Nonnegativity follows from `V_p >= 0`.

## MB-C4: Theorem B, q-Point Hard Local Factor

For fixed angles `alpha_1,...,alpha_q`, set

```text
k_p = |{r_p(alpha_1),...,r_p(alpha_q)}|.
```

Then

```text
E product_{j=1}^q rho_x(alpha_j)
  = product_{p <= x} L_p^MB(alpha_1,...,alpha_q),
rho_x(alpha) = 1_{D_x(R,alpha)=0} / P_x,
```

where

```text
L_p^MB(alpha_1,...,alpha_q)
  = (1 - k_p/p) / (1 - 1/p)^q.
```

Proof. At prime `p`, all `q` angles are uncovered exactly when `R_p` avoids the
`k_p` selected residues. That probability is `1-k_p/p`. The normalization
contributes `(1-1/p)^{-q}`. Independence over primes gives the product.

## MB-C5: Two-Point Factors

At `q=2`, there are two cases.

Collision:

```text
r_p(alpha)=r_p(gamma)
L_p^coll = 1 / (1 - 1/p).
```

Separated:

```text
r_p(alpha)!=r_p(gamma)
L_p^sep = (1 - 2/p) / (1 - 1/p)^2
        = 1 - 1/(p-1)^2.
```

The `p=2` separated factor is zero. This is harmless for upper bounds: use
`0 <= L_p^sep <= 1` and apply logarithmic estimates only to the positive
collision-growth product.

## MB-C6: Collision-Sum Bound

Let `delta = ||alpha-gamma||_T`. If

```text
r_p(alpha)=r_p(gamma),
```

then both points lie in the same half-open selected-residue cell, whose length
is `1/p`. Endpoint assignment cannot create a same-cell collision for points
separated by more than a fixed multiple of that length. Hence, for an absolute
constant `C`,

```text
r_p(alpha)=r_p(gamma) => p delta <= C.
```

Therefore

```text
sum_{p <= x, r_p(alpha)=r_p(gamma)} 1/p
  <= C_0 + C_1 log log min(x, C_2/delta).
```

This follows by bounding the collision primes by `p <= C/delta` and applying
the standard reciprocal-prime estimate.

The diagonal case `alpha=gamma` may be assigned the value `+infinity` in the
pointwise kernel bound. It is irrelevant for the L2 estimate because the
diagonal in `T x T` has Lebesgue measure zero.

## MB-C7: Theorem C, L2 Total-Mass Bound

For the complete-CRT hard endpoint,

```text
sup_x E[nu_x(T)^2] < infinity.
```

Proof. By Theorem B at `q=2`,

```text
E[nu_x(T)^2]
  = int_T int_T E[rho_x(alpha) rho_x(gamma)] d alpha d gamma.
```

The separated local factors are bounded by an absolutely convergent product,
using `0 <= L_p^sep <= 1` when needed. Collision factors satisfy

```text
L_p^coll = 1/(1-1/p) <= exp(C/p).
```

Thus

```text
E[rho_x(alpha) rho_x(gamma)]
  <= C exp(C sum_{collision p <= x} 1/p).
```

The collision-sum bound gives

```text
E[rho_x(alpha) rho_x(gamma)]
  <= C (1 + log(1/||alpha-gamma||_T))^C.
```

Finally,

```text
int_0^{1/2} (1 + log(1/t))^C dt < infinity,
```

so the two-point density is uniformly integrable on `T x T`.

## MB-C8: Theorem D, Weak Convergence

The measures `nu_x` converge weakly, almost surely along the cutoff filtration
and in the complete-CRT random finite-measure sense, to a random finite Borel
measure `nu`.

Proof route. Let `V` be a countable `Q`-vector subspace of `C(T)` containing
`1` and dense in sup norm. For each `f in V`, Theorem A gives a martingale
`nu_x(f)`. The L2 total-mass bound gives

```text
sup_x E|nu_x(f)|^2 <= ||f||_infty^2 sup_x E[nu_x(T)^2] < infinity.
```

Hence `nu_x(f)` converges almost surely and in L2 for every `f in V`; taking a
countable intersection gives simultaneous convergence on `V`. Linearity and
positivity pass to the limit. Also

```text
|L(f)| <= ||f||_infty L(1).
```

Thus the limit extends to a bounded positive linear functional on `C(T)`.
Riesz representation gives a random finite Borel measure `nu`, and uniform
approximation extends convergence to all continuous test functions. Since
`nu_x(T)` converges on the same probability-one event, the approximation step
is controlled by the limiting total mass.

## MB-C9: Theorem E, Fixed-Cutoff beta Endpoint Compatibility

For fixed cutoff `x`, v2.0 finite-beta AKC satisfies

```text
mu_{x,beta}(d alpha)
  = exp(beta D_x(R, alpha)) / Z_x(beta) d alpha.
```

As `beta -> -infinity`,

```text
exp(beta D_x(R, alpha)) -> 1_{D_x(R, alpha)=0}
Z_x(beta) -> P_x.
```

Therefore `mu_{x,beta}` converges to `nu_x` as finite measures for each fixed
cutoff `x`. This theorem does not claim interchange of the `x -> infinity` and
`beta -> -infinity` limits.

For support computations,

```text
P_{x,R}(u) = int_T u^{D_x(R,alpha)} d alpha
mu_{x,beta}(T) = P_{x,R}(e^beta) / Z_x(beta),
```

which avoids endpoint-grid bias.

## MB-C10: Support Evidence

public support keeps six theorem-facing experiments:

1. one-prime hard normalizer;
2. q-point hard local factor exactness;
3. exact cell polynomial and `u=0` endpoint;
4. Mertens-normalized total mass;
5. two-point L2 route diagnostics;
6. negative-beta fixed-cutoff endpoint from exact cell polynomial.

Slow integer-time transfer is deferred to v3.5 and is not part of the v3.0
public claim surface.

## MB-C11: Non-Claims

This public artifact manuscript does not claim integer-time transfer, diagonal Mertens
uncovered-measure theorem, `U_n(n) log n -> e^{-gamma}`, high-point theorem,
Fisher-zero theorem, Lee-Yang theorem, standard Gaussian Multiplicative Chaos,
prime-time theorem, a new proof of the classical Mertens product theorem, or peer review.
