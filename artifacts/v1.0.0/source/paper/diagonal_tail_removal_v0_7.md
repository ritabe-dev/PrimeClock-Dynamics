# PrimeClock Dynamics v0.7 All-Angle L1 Diagonal Tail Removal

Status: internal Gate C candidate proof packet for all-angle L1 diagonal tail
removal. This is not a public artifact, not a preprint, not a DOI artifact,
not a Zenodo record, and not peer reviewed.

Boundary summary: Gate C candidate for an all-angle L1 diagonal tail-removal
bridge. This is not a diagonal Angular Erdos-Kac theorem and not a public
artifact.
Short boundary: not a diagonal Angular Erdos-Kac theorem.

This note replaces the earlier irrational tail-moment route. The old rational
fixed-angle pointwise tail lemma remains as an optional stronger lemma, but the
main v0.7 route no longer needs an irrational high-moment tail estimate.

The long-term proof chain is now:

```text
v0.6 fixed-order finite-window moment bridge
  -> choose one slow truncation y(N)
  -> remove the diagonal tail in L1, hence in probability
  -> use Slutsky to prepare v0.8 fixed-angle diagonal Angular Erdos-Kac assembly.
```

It does not claim a diagonal Angular Erdos-Kac theorem, a finite-window CLT
theorem, a uniform-in-alpha theorem, a finite-dimensional Gaussian field
theorem, a shrinking-angle theorem, a Mertens uncovered-measure law, or a
random/non-random theorem.

## DT-1: Dyadic Diagonal And Truncated Variables

Fix one angle `alpha in R/Z`. v0.7 uses a dyadic window

```text
N < n <= 2N.
```

For `y < N`, write

```text
D_n(n, alpha) = sum_{p <= n} 1_{n mod p = r_p(alpha)}
D_y(n, alpha) = sum_{p <= y} 1_{n mod p = r_p(alpha)}
T_y(n, alpha) = D_n(n, alpha) - D_y(n, alpha).
```

Here `T_y` is the diagonal tail. The v0.7 Gate C candidate only proves that
this tail is negligible after Angular Erdos-Kac normalization in probability.

## DT-2: Slow Truncation

Set

```text
y(N) = floor(N^(1/log log N)).
```

All asymptotic statements in this packet are for `N` sufficiently large so
that `log log N > 1` and `y(N) >= 2`.

This single slow cutoff is independent of the moment order. For every fixed
integer `k >= 1`,

```text
y(N)^k / N = N^(k/log log N - 1) -> 0.
```

Thus the v0.6 fixed-order finite-window moment bridge can use this same
truncation for every fixed moment order. This is the key reason to replace the
old moment-dependent truncation `y_m(N)=floor(N^(1/(2m)))`.

## DT-3: Centering And Scale Comparisons

Define

```text
A_y = sum_{p <= y} 1/p,
A_{2N} = sum_{p <= 2N} 1/p,
B_y^2 = sum_{p <= y} (1/p)(1 - 1/p),
B_{2N}^2 = sum_{p <= 2N} (1/p)(1 - 1/p).
```

For the slow cutoff,

```text
log y = log N / log log N,
log log y = log log N - log log log N + o(1).
```

Therefore

```text
B_y / B_{2N} -> 1.
```

Also,

```text
A_{2N} - A_y = O(log log log N),
```

so

```text
(A_{2N} - A_y) / B_{2N} -> 0.
```

These are scale and centering bookkeeping statements for the later v0.8
assembly.

## DT-4: All-Angle L1 Tail Bound

For any fixed angle `alpha`, each prime `p` selects one residue class

```text
n mod p = r_p(alpha).
```

On a dyadic interval of length `N`, the number of integers in one selected
residue class modulo `p` is at most

```text
N/p + O(1).
```

Since

```text
T_y(n, alpha) <= sum_{y < p <= 2N} 1_{n mod p = r_p(alpha)},
```

we have

```text
E_{N < n <= 2N}[T_y(n, alpha)]
  <= sum_{y < p <= 2N} (1/p + O(1/N)).
```

The endpoint term is

```text
O(pi(2N)/N) = O(1/log N),
```

and the prime harmonic term is

```text
sum_{y < p <= 2N} 1/p = O(log log log N)
```

for `y=floor(N^(1/log log N))`. Here we use the standard reciprocal-prime
estimate

```text
sum_{p <= x} 1/p = log log x + O(1).
```

Indeed,

```text
sum_{y < p <= 2N} 1/p
  = log log(2N) - log log y + O(1)
  = O(log log log N).
```

Hence

```text
E_{N < n <= 2N}[T_y(n, alpha)] = O(log log log N).
```

Since `B_{2N}^2 ~ log log N`,

```text
E[T_y(n, alpha)] / B_{2N} -> 0.
```

By Markov's inequality,

```text
T_y(n, alpha) / B_{2N} -> 0
```

in probability. This is the v0.7 Gate C candidate statement `PCD-AK-DT-L1`.
It uses only the fact that each prime selects one residue class, so it does not
split into rational and irrational angle cases.

## DT-5: Slutsky Bridge

If the truncated finite-window variables satisfy

```text
(D_y(n, alpha) - A_y) / B_y => N(0,1)
```

for the slow cutoff `y=floor(N^(1/log log N))`, then DT-3 and DT-4 imply

```text
(D_n(n, alpha) - A_{2N}) / B_{2N} => N(0,1)
```

by Slutsky's theorem. This v0.7 packet records the tail-removal bridge only; it
does not itself prove the truncated finite-window CLT or the final diagonal
Angular Erdos-Kac theorem.

## DT-6: Optional Rational-Angle Pointwise Lemma

The earlier rational-angle tail moment lemma remains useful as a stronger
optional statement. If `alpha=a/b in Q/Z`, then

```text
e_p = b r_p(alpha) - a p
```

takes only finitely many values, and a hit implies

```text
p | (b n - e_p).
```

On `N < n <= 2N`, each `|b n - e|` is at most `C_alpha N`, so the number of
prime factors larger than `N^(1/(2m))` is `O_m(1)`. Equivalently, if there are
`L` such distinct prime factors, then

```text
y_m(N)^L <= C_alpha N.
```

This gives

```text
E_{N < n <= 2N}[ |T_{y_m}(n, alpha)|^m ] = O_{m,alpha}(1)
```

for rational fixed angles and `y_m(N)=floor(N^(1/(2m)))`.

This optional lemma is recorded as `PCD-AK-DT-RAT`. It is not the main v0.7
route and is not needed for the all-angle L1 tail bridge. Short boundary: not
the main v0.7 route.

Short label: not the main v0.7 route.

## DT-7: Former Irrational Tail-Moment Route

The previous attempt asked for an arbitrary irrational-angle tail moment bound
via a Beatty-divisor or angular residue-packing lemma. That question is no
longer required for the diagonal CLT route, because L1 tail control plus
Slutsky is sufficient for distribution convergence.

Short conclusion: no longer required.

This packet does not claim an arbitrary irrational-angle tail moment bound.

## Gate C Support Evidence

The deterministic support runner
`experiments/_workflow/build_diagonal_tail_support.py` records proof-budget rows
for the slow cutoff `y=floor(N^(1/log log N))`.

The rows report:

- the window size `N`;
- the dyadic window `(N, 2N]`;
- a fixed moment order `k` used only to display the v0.6 asymptotic budget;
- the slow cutoff;
- the v0.6 asymptotic budget exponent `k/log log N - 1`;
- a prime-harmonic tail baseline `sum_{y < p <= 2N} 1/p`;
- the L1 tail baseline divided by `B_{2N}`;
- the centering comparison `(A_{2N} - A_y) / B_{2N}`;
- the scale comparison `B_y / B_{2N}`.

These rows are deterministic proof-budget sanity checks. They are not
statistical evidence and not a theorem. In short: not statistical evidence and
not a theorem. Short boundary: not statistical evidence and not a theorem.
