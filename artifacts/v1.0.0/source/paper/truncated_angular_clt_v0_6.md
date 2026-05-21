# PrimeClock Dynamics v0.6 Fixed-Order Finite-Window Moment Bridge

Status: internal Gate C candidate proof packet. This is not a public artifact,
not a preprint, not a DOI artifact, not a Zenodo record, and not peer reviewed.

This note records the next proof stage after the v0.5 fixed-cutoff complete-CRT
Angular CLT. It moves from the complete CRT probability space to incomplete
integer windows. The purpose is to isolate the residue-counting error needed
before any finite-window CLT theorem or diagonal Angular Erdos-Kac theorem can
be claimed.

It does not claim a diagonal theorem, and it is not a finite-window CLT
theorem. It also does not claim a uniform-in-alpha theorem, a Gaussian field
theorem, a Mertens uncovered law, or a random/non-random theorem.

## Truncated Finite-Window Model

Fix an angle `alpha in R/Z`. For integers `N >= 1` and cutoffs `y <= N`, define

```text
P_y = {p prime : p <= y},
r_p(alpha) = floor(p alpha + 1/2) mod p,
D_y(n, alpha) = sum_{p <= y} 1_{n mod p = r_p(alpha)}.
```

The finite-window random variable is `D_y(n, alpha)` with `n` uniform on
`{1, 2, ..., N}`. The cutoff `y = y(N)` is allowed to grow, but this draft keeps
`y` smaller than `N` by an explicit moment-order condition.

As in v0.5, set

```text
A_y = sum_{p <= y} 1/p,
B_y^2 = sum_{p <= y} (1/p)(1 - 1/p).
```

## TFCLT-1: One Residue Class Per Prime

The half-open convention still gives exactly one selected residue class modulo
each prime:

```text
n mod p = r_p(alpha).
```

Unlike the complete CRT period, the residues `n mod p` are not exactly
independent when `n` is sampled from `{1, ..., N}`. The proof problem is to show
that, for sufficiently small truncation scale `y`, the incomplete-window
residue counts approximate the CRT probabilities well enough for fixed moment
orders.

## TFCLT-2: Incomplete-Window CRT Counting Lemma

Let `S` be a finite set of distinct primes, let

```text
q_S = prod_{p in S} p.
```

The congruences

```text
n mod p = r_p(alpha)  for p in S
```

determine one residue class modulo `q_S` by CRT. Therefore

```text
#{1 <= n <= N : n mod p = r_p(alpha) for every p in S}
= N / q_S + O(1).
```

Equivalently, for `n` uniform on `{1, ..., N}`,

```text
P(n mod p = r_p(alpha) for every p in S)
= 1 / q_S + O(1 / N).
```

The `O(1)` term is uniform in the residue class.

## TFCLT-3: Fixed-Order Factorial Moment Approximation

For a fixed integer `k >= 1`, the `k`th factorial moment of `D_y(n, alpha)` is
controlled by sums over distinct `k`-tuples of primes. Applying TFCLT-2 to each
tuple gives the complete-CRT main term plus an accumulated endpoint error.

A safe first sufficient condition for the fixed-order approximation is

```text
pi(y)^k / N -> 0.
```

The simpler condition

```text
y^k / N -> 0
```

also suffices and is the working v0.6 proof-budget condition. It is not expected
to be optimal.

Under this condition, for each fixed `k`,

```text
E[(D_y(n, alpha))_k]
= sum_{p_1, ..., p_k distinct <= y} 1 / (p_1 ... p_k) + o(1),
```

where `(z)_k` is the falling factorial.

## TFCLT-4: Fixed-Order Centered Moment Comparison

For fixed integer `m >= 1`, define

```text
X_p(n, alpha) = 1_{n mod p = r_p(alpha)},
Z_p(n, alpha) = X_p(n, alpha) - 1/p.
```

Then

```text
D_y(n, alpha) - A_y = sum_{p <= y} Z_p(n, alpha).
```

Expanding the `m`th centered moment over the finite window gives

```text
E_N[(D_y(n, alpha) - A_y)^m]
= sum_{p_1, ..., p_m <= y} E_N[Z_{p_1} ... Z_{p_m}].
```

For a fixed ordered tuple `P = (p_1, ..., p_m)`, expand

```text
prod_{i=1}^m Z_{p_i}
= sum_{J subset {1,...,m}}
  (-1)^{m-|J|}
  (prod_{i notin J} 1/p_i)
  prod_{i in J} X_{p_i}.
```

For each subset `J`, the product `prod_{i in J} X_{p_i}` imposes residue
conditions only on the distinct primes appearing among `{p_i : i in J}`. If the
same prime appears more than once, the repeated condition is identical because
the selected residue class is fixed. Thus the event is either the empty event
when `J` is empty, or one CRT residue class modulo the product `q_T` of the
distinct primes in that subset.

The finite-window probability of each such event differs from the complete-CRT
probability by `O(1/N)` by TFCLT-2. The expansion has at most `2^m` terms and
all coefficient magnitudes are at most `1`, so each ordered tuple contributes
error `O_m(1/N)`. Summing over at most `pi(y)^m` ordered tuples gives

```text
E_N[(D_y - A_y)^m] - E_CRT[(D_y - A_y)^m]
= O_m(pi(y)^m / N).
```

Consequently, the normalized centered moments agree when

```text
pi(y)^m / (N B_y^m) -> 0.
```

The stronger condition `pi(y)^m / N -> 0`, and hence the simpler sufficient
condition `y^m / N -> 0`, also works. The `y^m / N` condition remains a safe
proof budget, not an optimal statement.

This Gate C candidate records the fixed-order centered moment bridge as the
closed candidate statement `PCD-AK-TF-MOMENT`.

## TFCLT-5: Method-of-Moments Implication

If, for every fixed `m >= 1`, the normalized centered moment comparison in
TFCLT-4 holds and the complete-CRT normalized moments converge to the Gaussian
moments, then the truncated finite-window variables

```text
(D_y(n, alpha) - A_y) / B_y
```

converge in distribution to `N(0,1)`, provided the Gaussian moment sequence is
determinate.

This packet does not yet close this implication for a single fixed polynomial
scale `y = N^theta`. The simple incomplete-window error budget supports
fixed-order moment control. A full CLT proof must specify a growth regime for
`y(N)` or use a moment-order-dependent truncation strategy.

## TFCLT-6: Slow Truncation Compatibility

The v0.7 L1 tail-removal route uses one slow cutoff

```text
y(N)=floor(N^(1/log log N)).
```

For every fixed moment order `k`,

```text
y(N)^k/N = N^(k/log log N - 1) -> 0.
```

Therefore the fixed-order bridge in TFCLT-4 is compatible with this same slow
cutoff for all fixed moment orders. This does not change the v0.6 claim
surface: v0.6 remains a fixed-order centered moment comparison, not a completed
finite-window CLT theorem.

Short compatibility statement: compatible with this same slow cutoff.

## Gate C Candidate Target

Gate C candidate status covers the incomplete-window fixed-order centered
moment bridge as the right next proof surface after v0.5. It does not promote a
completed finite-window CLT theorem:

```text
complete CRT CLT
  -> truncated finite-window fixed-order moment control
  -> diagonal tail removal
  -> fixed-angle diagonal Angular Erdos-Kac theorem candidate.
```

The next draft after Gate C should choose a moment-order-dependent truncation
strategy, or a single slow truncation such as `y(N)=floor(N^(1/log log N))`,
and study diagonal tail removal.

## Boundary

This v0.6 draft is not the diagonal Angular Erdos-Kac theorem for

```text
D(n, alpha) = D_n(n, alpha).
```

It also does not prove a diagonal Mertens uncovered law for

```text
U(n) = U_n(n).
```

The diagonal step will require removing the tail

```text
D_n(n, alpha) - D_y(n, alpha),
```

after a truncated finite-window theorem is closed.

## Gate R Support Evidence

The deterministic support runner
`experiments/_workflow/build_truncated_angular_clt_support.py` records sample
rows for the proof budget:

- the window size `N`;
- the cutoff `y`;
- a fixed moment order `m`;
- the safe ratio `y^m / N`;
- the sharper ratio `pi(y)^m / N`;
- the normalized comparison ratio `pi(y)^m / (N B_y^m)`;
- the variance baseline `B_y^2`.

These rows are proof-budget sanity checks only. They are not statistical
evidence for a diagonal theorem.
