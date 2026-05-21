# PrimeClock Dynamics: An Angular Erdos-Kac Theorem and a Fixed-Cutoff Geometric Mertens Identity

Status: v1.0 public research artifact and preprint-style manuscript. It is
not peer reviewed. It is not a DOI artifact or Zenodo record unless a DOI/Zenodo
deposit is issued separately.

## Abstract

PrimeClock Dynamics studies a prime-indexed angular multiplicity field on the
circle. For each prime `p`, a fixed angle `alpha in R/Z` selects one residue
class `r_p(alpha) mod p`, and the diagonal multiplicity statistic is

```text
D_n(n,alpha)=sum_{p<=n} 1_{n mod p = r_p(alpha)}.
```

At the zero angle, the statistic recovers the classical prime-divisor counting
function `D_n(n,0)=omega(n)`. This manuscript proves a fixed-angle dyadic Angular
Erdos-Kac theorem: for every fixed finite set of pairwise distinct angles
`alpha_1,...,alpha_d`, with `n` uniformly sampled from `N < n <= 2N`,

```text
((D_n(n,alpha_j)-A_{2N})/B_{2N})_{j=1}^d
  => (Z_1,...,Z_d),
```

where `Z_1,...,Z_d` are independent standard normal variables and

```text
A_x=sum_{p<=x} 1/p,
B_x^2=sum_{p<=x} (1/p)(1-1/p).
```

The proof proceeds through a fixed-cutoff complete-CRT model, a slow-truncation
finite-window moment transfer with `y(N)=floor(N^(1/log log N))`, an L1
diagonal tail-removal estimate, and a Cramer-Wold argument. The manuscript also
records a fixed-cutoff geometric Mertens identity:

```text
E_{n in Z/M_xZ}[U_x(n)] = prod_{p<=x}(1-1/p),
```

and hence, by the classical Mertens product theorem,

```text
E[U_x] = (e^{-gamma}+o(1))/log x.
```

No diagonal Mertens uncovered-measure law, uniform-in-angle theorem,
shrinking-angle limit, log-correlated field theorem, or random/non-random
theorem is claimed. In particular, it is not presented as a new strengthening of the classical Erdos-Kac theorem, and it is not a diagonal Mertens law.

## 1. Introduction

The PrimeClock multiplicity field is a prime-indexed residue-class counting
model on the circle. Each prime `p` assigns one selected residue class modulo
`p` to a fixed angle `alpha`, and the statistic counts how often an integer
falls into those selected classes. At `alpha=0`, the selected class is the zero
class and the diagonal statistic recovers `omega(n)`, the number of distinct
prime divisors of `n`. For general fixed angles, the same construction gives a
natural angular extension of the Erdos-Kac setting: instead of asking whether
`p` divides `n`, it asks whether `n` hits the prime-indexed residue selected by
`alpha`.

The main result is a finite-dimensional fixed-angle Angular Erdos-Kac theorem
on dyadic windows. For any fixed finite set of pairwise distinct angles, the
normalized diagonal multiplicity vector converges to a vector of independent
standard Gaussian variables. The proof first treats the complete CRT
probability space, then transfers fixed moments to a slow finite-window cutoff,
removes the diagonal tail in probability by an L1 estimate, and finally applies
Cramer-Wold.

The paper also records a fixed-cutoff geometric Mertens identity. This identity
concerns the complete CRT average of the fixed-cutoff uncovered measure and,
combined with the classical Mertens product theorem, gives the corresponding
fixed-cutoff asymptotic. It is deliberately not a diagonal Mertens uncovered
measure law.

The main boundary is therefore sharp: the paper proves a fixed-angle and
finite-dimensional Angular Erdos-Kac route inside the PrimeClock model, while
leaving uniform-in-angle limits, shrinking-angle fields, log-correlated limits,
and diagonal Mertens laws as future work.

## 2. Model

Let `T=R/Z`. For each prime `p` and angle `alpha in T`, define the selected
residue

```text
r_p(alpha)=floor(p alpha + 1/2) mod p,
```

with the half-open convention specified in the model definition.

For `x>=2`, define

```text
D_x(n,alpha)=sum_{p<=x} 1_{n mod p = r_p(alpha)}.
```

The diagonal multiplicity is

```text
D_n(n,alpha)=sum_{p<=n} 1_{n mod p = r_p(alpha)}.
```

Set

```text
A_x=sum_{p<=x} 1/p,
B_x^2=sum_{p<=x} (1/p)(1-1/p).
```

The zero angle satisfies `D_n(n,0)=omega(n)`, where `omega(n)` is the number of
distinct prime divisors of `n`. Thus the `alpha=0` fiber recovers the classical
prime-divisor count. The theorem below includes `alpha=0` as a special case and
is consistent with the classical Erdos-Kac theorem; it is not presented as a
new strengthening of that classical result.

## 3. Main Theorem

### Theorem A: finite-dimensional fixed-angle Angular Erdos-Kac theorem

Let `alpha_1,...,alpha_d in T` be a fixed finite set of pairwise distinct
angles. Let `n` be uniformly sampled from the dyadic window `N < n <= 2N`.
Then

```text
((D_n(n,alpha_j)-A_{2N})/B_{2N})_{j=1}^d
  => (Z_1,...,Z_d),
```

where `Z_1,...,Z_d` are independent standard normal random variables.

Equivalently, using

```text
A_{2N}=log log N+O(1),
B_{2N}^2=log log N+O(1),
```

one may write

```text
((D_n(n,alpha_j)-log log N)/sqrt(log log N))_{j=1}^d
  => (Z_1,...,Z_d).
```

This theorem is for a fixed finite set of fixed angles. It is not uniform in
`alpha`, does not address shrinking angle separations, and does not prove a
log-correlated Gaussian field limit.

## 4. Fixed-Cutoff Complete-CRT Input

Let `M_x=prod_{p<=x} p`. If `n_x` is uniformly distributed on `Z/M_xZ`, CRT
gives independent uniform coordinates `n_x mod p` for `p<=x`. Hence, for every
fixed `alpha`,

```text
D_x(n_x,alpha)=sum_{p<=x} X_{p,alpha},
P(X_{p,alpha}=1)=1/p.
```

Therefore

```text
E[D_x(n_x,alpha)]=A_x,
Var[D_x(n_x,alpha)]=B_x^2.
```

Since `B_x^2 -> infinity` and the centered summands are uniformly bounded, the
Lindeberg condition is eventually trivial. Thus

```text
(D_x(n_x,alpha)-A_x)/B_x => N(0,1).
```

For later moment-transfer arguments, complete-CRT Gaussian moment convergence
is also used. For every fixed `m`,

```text
E_CRT[((D_x(n_x,alpha)-A_x)/B_x)^m] -> E[Z^m],
```

where `Z` is standard normal. One proof uses cumulants: fixed-order cumulants
of each centered Bernoulli coordinate are `O_m(1/p)`, so fixed cumulants of the
sum are `O_m(B_x^2)`, and after normalization all cumulants of order at least
three vanish.

## 5. Slow Cutoff and Finite-Window Moment Transfer

Let

```text
y=y(N)=floor(N^(1/log log N)).
```

For every fixed `m`,

```text
y^m/N = N^(m/log log N - 1) -> 0.
```

For `n` uniform on `N < n <= 2N`, and for any finite set `S` of distinct primes
with `q_S=prod_{p in S} p`, the conditions

```text
n mod p = r_p(alpha)  for p in S
```

select one residue class modulo `q_S`. Therefore

```text
#{N<n<=2N : n mod p = r_p(alpha) for all p in S}
  = N/q_S + O(1).
```

Expanding centered moments gives

```text
E_{N<n<=2N}[(D_y(n,alpha)-A_y)^m]
  - E_CRT[(D_y(n,alpha)-A_y)^m]
  = O_m(pi(y)^m/N).
```

After normalization, `pi(y)^m/(N B_y^m) -> 0`, so all fixed normalized centered
moments match the complete-CRT moments. By complete-CRT Gaussian moment
convergence and determinacy of Gaussian moments,

```text
(D_y(n,alpha)-A_y)/B_y => N(0,1)
```

for `n` uniform on `N < n <= 2N`.

## 6. Diagonal Tail Removal

Define

```text
T_y(n,alpha)=D_n(n,alpha)-D_y(n,alpha).
```

Since `n<=2N` on the dyadic window,

```text
T_y(n,alpha) <= sum_{y<p<=2N} 1_{n mod p = r_p(alpha)}.
```

For each prime `p`, the dyadic interval contains `N/p+O(1)` integers in a fixed
residue class modulo `p`. Therefore

```text
E_{N<n<=2N}[T_y(n,alpha)]
  <= sum_{y<p<=2N} (1/p + O(1/N))
  = O(log log log N).
```

Because `B_{2N} ~ sqrt(log log N)`, Markov's inequality gives

```text
T_y(n,alpha)/B_{2N} -> 0
```

in probability. The same slow cutoff also satisfies

```text
(A_{2N}-A_y)/B_{2N} -> 0,
B_y/B_{2N} -> 1.
```

Thus, by Slutsky's theorem,

```text
(D_n(n,alpha)-A_{2N})/B_{2N} => N(0,1).
```

## 7. Finite-Dimensional Extension

Let `alpha_1,...,alpha_d` be fixed and pairwise distinct. For any pair
`alpha_i != alpha_j`, put

```text
delta_ij = ||alpha_i-alpha_j||_T > 0.
```

If `r_p(alpha_i)=r_p(alpha_j)`, then the two angles lie in the same half-open
`p`-grid cell of length `1/p`. Hence, up to the endpoint convention,
`delta_ij < 1/p`. Same-residue collisions therefore occur for only finitely many
primes, safely bounded by `p < 1/delta_ij`.

On the complete-CRT side, the off-diagonal covariance for a prime `p` is
`(1/p)(1-1/p)` if the two angles select the same residue, and `-1/p^2`
otherwise. The same-residue terms are finite in number and the different
residue terms are summable, so off-diagonal covariance is `O_alpha(1)`. Since
the coordinate variance is `B_y^2 -> infinity`, normalized off-diagonal
covariance vanishes.

For a fixed Cramer-Wold vector `t=(t_1,...,t_d)`, the complete-CRT variance of
the projection satisfies

```text
V_y(t) = (sum_{j=1}^d t_j^2) B_y^2 + O_{alpha,t}(1).
```

If `t != 0`, the projection has a complete-CRT Gaussian limit by the same
bounded Lindeberg or cumulant argument. The finite-window moment transfer
extends to each fixed projection: after expanding centered factors into
constants and indicator products, each event term either imposes compatible
residue conditions and is counted by the CRT residue-class estimate, or imposes
incompatible residue classes modulo the same prime and vanishes in both models.

The L1 tail-removal estimate applies coordinatewise. Since `d` is fixed, a
finite union bound makes all coordinate tails negligible, hence every fixed
Cramer-Wold projection has the diagonal Gaussian limit. Cramer-Wold gives
Theorem A.

## 8. Fixed-Cutoff Geometric Mertens Identity

Let `U_x(n)` be the uncovered measure of the fixed-cutoff circle model. Over
the complete CRT period,

```text
E_{n in Z/M_xZ}[U_x(n)] = prod_{p<=x}(1-1/p).
```

Proof. By finite Fubini, average the uncovered indicator first over the
complete CRT period and then over angle. For each fixed angle and each prime
`p<=x`, the covered arc condition excludes exactly one residue class modulo
`p`, up to endpoint conventions on a measure-zero set of angles. Under uniform
measure on `Z/M_xZ`, CRT makes the residue coordinates modulo the primes
`p<=x` independent. Hence the probability that no prime excludes the point is
the product of the local probabilities `(1-1/p)`. Integrating over angle gives
the stated identity.

By the classical Mertens product theorem,

```text
prod_{p<=x}(1-1/p) = (e^{-gamma}+o(1))/log x.
```

Therefore

```text
E[U_x] = (e^{-gamma}+o(1))/log x.
```

This is a fixed-cutoff complete-CRT identity and corollary. It is not a
diagonal Mertens law for `U(n)=U_n(n)`, not a pointwise uncovered-measure
theorem, and not a new proof of Mertens' theorem.

## 9. Claim Boundary

This manuscript does not claim:

- uniform-in-angle convergence;
- a shrinking-angle theorem;
- a log-correlated Gaussian field theorem;
- a full Gaussian field theorem;
- diagonal Mertens uncovered-measure asymptotics;
- pointwise or typical laws for `U(n)`;
- a random/non-random theorem;
- a result about prime gaps;
- a result about the Riemann hypothesis;
- a result about classical covering systems.

The `alpha=0` fiber recovers the classical prime-divisor count. The theorem is
consistent with the classical Erdos-Kac theorem and gives the corresponding
dyadic statement inside the PrimeClock framework, but it is not presented as a
new strengthening of the classical theorem.

## 10. References

The following references record the background results and nearby literature
used by this manuscript. A journal-facing version should convert them to the
target venue's bibliography style.

- G. H. Hardy and S. Ramanujan, The normal number of prime factors of a number
  `n`, Quarterly Journal of Mathematics 48 (1917), 76--92.
- P. Erdos and M. Kac, The Gaussian law of errors in the theory of additive
  number theoretic functions, American Journal of Mathematics 62 (1940),
  738--742.
- P. Erdos and A. Wintner, Additive arithmetical functions and statistical
  independence, American Journal of Mathematics 61 (1939), 713--721.
- J. Kubilius, Probabilistic Methods in the Theory of Numbers, American
  Mathematical Society, 1964.
- G. Tenenbaum, Introduction to Analytic and Probabilistic Number Theory,
  Cambridge University Press, third edition, 2015.
- H. Halberstam and H.-E. Richert, Sieve Methods, Academic Press, 1974.
- F. Mertens, Ein Beitrag zur analytischen Zahlentheorie, Journal fur die
  reine und angewandte Mathematik 78 (1874), 46--62.
- A. Granville and K. Soundararajan, Sieving and the Erdos-Kac theorem, in
  Equidistribution in Number Theory, An Introduction, NATO Science Series II
  237, Springer, 2007, 15--27.

No new proof of the classical Erdos-Kac theorem or Mertens product theorem is
claimed here; these references identify the background results used by the
PrimeClock fixed-angle and fixed-cutoff formulations.
