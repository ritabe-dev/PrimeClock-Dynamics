# PrimeClock Dynamics v0.8 Fixed-Angle Diagonal Angular Erdos-Kac Assembly Gate C Verified

Status: internal Gate C verified proof-route record built from the internal Gate
R passed proof-route packet and clean Gate C candidate extraction. This is not a
public artifact, not a preprint, not a DOI artifact, not a Zenodo record, and
not peer reviewed.

## Purpose

This packet records the v0.8 fixed-angle diagonal Angular Erdos-Kac assembly
step. It combines the previous internal stages:

```text
v0.5 fixed-cutoff complete-CRT Angular CLT
  -> v0.6 slow-truncation finite-window moment bridge
  -> v0.7 all-angle L1 diagonal tail removal
  -> v0.8 fixed-angle diagonal assembly.
```

This packet records the internally Gate C verified assembly route. It does not
make a public artifact, preprint, DOI, Zenodo, or peer-reviewed claim.

## DAEK-1: Target Dyadic Statement

Fix one angle `alpha in R/Z`. Let `n` be uniformly sampled from the dyadic
window

```text
N < n <= 2N.
```

The intended theorem candidate is

```text
(D_n(n, alpha) - A_{2N}) / B_{2N} => N(0,1),
```

where

```text
A_{2N} = sum_{p <= 2N} 1/p,
B_{2N}^2 = sum_{p <= 2N} (1/p)(1 - 1/p).
```

This is a fixed-angle dyadic statement. It is not uniform in `alpha`, not a
finite-dimensional field theorem, and not a shrinking-angle theorem.

## DAEK-2: Slow Truncation

Use the same slow cutoff fixed in v0.7:

```text
y(N)=floor(N^(1/log log N)).
```

For every fixed moment order `k`,

```text
y(N)^k/N = N^(k/log log N - 1) -> 0.
```

Thus the v0.6 fixed-order centered moment bridge applies to this single slow
cutoff for every fixed moment order.

## DAEK-3: Dyadic Finite-Window Counting

The dyadic version of the v0.6 counting lemma has the same form. If `S` is a
finite set of distinct primes and `q_S=prod_{p in S} p`, then the simultaneous
conditions

```text
n mod p = r_p(alpha)  for p in S
```

select one residue class modulo `q_S`. Therefore

```text
#{N < n <= 2N : n mod p = r_p(alpha) for every p in S}
= N/q_S + O(1),
```

uniformly in the selected residue class. This is the dyadic replacement for
the `{1,...,N}` count used in v0.6.

Consequently, the v0.6 fixed-order centered moment comparison applies on the
dyadic window with the same error form:

```text
E_{N<n<=2N}[(D_y-A_y)^m] - E_CRT[(D_y-A_y)^m]
= O_m(pi(y)^m/N).
```

At the slow cutoff `y(N)=floor(N^(1/log log N))`, the normalized comparison
condition holds for every fixed `m`:

```text
pi(y)^m/(N B_y^m) -> 0.
```

## DAEK-4: Complete-CRT Gaussian Moment Convergence

The complete-CRT side needs moment convergence, not only distributional
convergence. Under the complete CRT probability space, for fixed `alpha`,

```text
D_y(n, alpha)-A_y = sum_{p <= y} Z_p(n, alpha),
```

where the `Z_p` are independent, centered, uniformly bounded variables with

```text
sum_{p <= y} Var(Z_p) = B_y^2 -> infinity.
```

For every fixed `r >= 3`, the `r`th cumulant of the unnormalized sum is
`O_r(B_y^2)` because each centered Bernoulli coordinate has all fixed-order
cumulants bounded by `O_r(1/p)` and the coordinates are independent. After
normalization by `B_y`, the `r`th cumulant is therefore

```text
O_r(B_y^(2-r)) -> 0.
```

The first normalized cumulant is `0` and the second normalized cumulant is `1`.
Thus the normalized complete-CRT cumulants converge to the Gaussian cumulants,
and for every fixed `m`,

```text
E_CRT[((D_y-A_y)/B_y)^m] -> E[Z^m],
```

where `Z` is standard normal.

Short label: complete-CRT Gaussian moment convergence lemma.

## DAEK-5: Truncated Finite-Window CLT

The first v0.8 theorem obligation is to turn the fixed-order moment comparison
into a truncated finite-window CLT:

```text
(D_y(n, alpha) - A_y) / B_y => N(0,1)
```

for `n` uniform on `N < n <= 2N` and `y=y(N)`.

The intended proof route is:

1. DAEK-4 gives complete-CRT Gaussian moment convergence for `D_y`.
2. DAEK-3 gives normalized fixed-order moment agreement between the finite
   dyadic window and the complete-CRT model at the same slow cutoff.
3. The Gaussian moment sequence is determinate.
4. Therefore the truncated finite-window variables converge in distribution to
   `N(0,1)`.

The argument is a method-of-moments argument at the slow cutoff, using DAEK-4
for the complete-CRT Gaussian moments and DAEK-3 for finite-window moment
transfer.

The statement is `PCD-AK-TF-SLOW-CLT`. It is internally Gate C verified as a
proof-route component.

## DAEK-6: Tail Removal From v0.7

The v0.7 Gate C verified bridge gives

```text
E_{N < n <= 2N}[T_y(n, alpha)] = O(log log log N),
```

and hence

```text
T_y(n, alpha) / B_{2N} -> 0
```

in probability, where

```text
T_y(n, alpha)=D_n(n, alpha)-D_y(n, alpha).
```

It also records

```text
(A_{2N}-A_y)/B_{2N} -> 0,
B_y/B_{2N} -> 1.
```

## DAEK-7: Slutsky Assembly

If DAEK-5 is closed, then DAEK-6 gives

```text
(D_n(n, alpha) - A_{2N}) / B_{2N} => N(0,1)
```

by Slutsky's theorem.

This is the internally Gate C verified statement `PCD-AK-DIAG-ASM`.

## DAEK-8: Dyadic Normalization Equivalence

After the dyadic statement is closed, the final presentation translates the
normalization to the standard scale:

```text
A_{2N} = log log N + O(1),
B_{2N}^2 = log log N + O(1),
```

so that

```text
(D_n(n, alpha) - log log N) / sqrt(log log N) => N(0,1)
```

on dyadic windows. The equivalent `log log n` normalization should be handled
as final bookkeeping because `n in (N,2N]` implies `log log n = log log N +
o(sqrt(log log N))`.

This is the dyadic normalization equivalence lemma.

## Boundary

This v0.8 Gate C verified record does not claim:

- a public theorem artifact;
- a uniform-in-alpha theorem;
- a finite-dimensional Gaussian field theorem;
- a shrinking-angle theorem;
- a Mertens uncovered-measure law;
- a random/non-random theorem;
- a public release.

## Gate C Support Evidence

The deterministic support runner
`experiments/_workflow/build_diagonal_angular_ek_support.py` records
proof-budget rows for the slow cutoff. The rows check:

- `y(N)^k/N` for fixed moment orders;
- the dyadic variance scale;
- the `B_y/B_{2N}` scale ratio;
- the L1 tail and centering ratios relative to `B_{2N}`;
- the Slutsky tail target.

These rows are proof-budget sanity checks only. They are not statistical
evidence and not a theorem.

## Gate C Verified Summary

Gate C verified the dyadic finite-window moment bridge at the slow cutoff, the
complete-CRT Gaussian moment convergence input, the v0.7 L1 tail-removal input,
the Slutsky assembly, and the final dyadic normalization bookkeeping for one
fixed angle.
