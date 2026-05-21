# PrimeClock Dynamics v0.9 Finite-Dimensional Angular Erdos-Kac Gate C Verified

Status: internal Gate C verified proof-route packet built from the internal
Gate R passed route. This is not a public artifact, not a preprint, not a DOI
artifact, not a Zenodo record, and not peer reviewed.

## Purpose

This packet records that the v0.8 fixed-angle diagonal Angular Erdos-Kac
assembly extends cleanly to a finite set of fixed distinct angles. The verified
scope is deliberately narrow:

```text
alpha_1, ..., alpha_d in R/Z fixed and pairwise distinct,
d fixed.
```

It does not address uniform-in-alpha convergence, shrinking-angle limits,
log-correlated fields, or any Mertens uncovered-measure law.

## FDEK-1: Target Joint Statement

For fixed pairwise distinct angles `alpha_1,...,alpha_d`, let `n` be uniformly
sampled from the dyadic window `N < n <= 2N`. The Gate C verified statement is
that

```text
((D_n(n, alpha_j)-A_{2N})/B_{2N})_{j=1}^d
```

converges in distribution to a vector of independent standard normal random variables.

Short label: `PCD-AK-FD-JOINT`.

## FDEK-2: Pairwise Residue-Collision Bound

For two fixed distinct angles `alpha` and `beta`, let

```text
delta = ||alpha-beta||_{R/Z} > 0.
```

The selected residues can agree modulo `p` only when `alpha` and `beta` lie in
the same half-open `p`-grid cell. Each such cell has circle length `1/p`.
Therefore, up to the endpoint convention,

```text
delta < 1/p.
```

Equivalently, same-residue collisions can occur only for primes satisfying
`p < 1/delta`; the integer safe bound `p <= ceil(1/delta)` is sufficient for
proof bookkeeping.

Thus each fixed pair of distinct angles has only finitely many possible
same-prime residue collisions. For all larger primes, one prime coordinate can
hit at most one of the two angles.

This is the main new bookkeeping beyond v0.8.

## FDEK-3: Complete-CRT Covariance Structure

Under the complete CRT probability space at cutoff `x`, each prime coordinate
is independent. For two fixed distinct angles, the same-prime covariance is:

```text
same selected residue:      (1/p)(1-1/p),
different selected residue: -1/p^2.
```

The same-residue case occurs for only finitely many primes by FDEK-2. Therefore
the complete-CRT covariance between two distinct fixed angles is bounded as
`x -> infinity`, while each coordinate variance is

```text
B_x^2 = sum_{p <= x} (1/p)(1-1/p) ~ log log x.
```

After normalization by `B_x`, every off-diagonal covariance tends to `0`.

## FDEK-4: Cramer-Wold Reduction

For fixed coefficients `t_1,...,t_d`, consider the linear statistic

```text
sum_{j=1}^d t_j (D_y(n, alpha_j)-A_y).
```

At each prime `p`, this is a bounded centered prime-coordinate contribution.
Let `V_y(t)` be the complete-CRT variance of this Cramer-Wold projection. The
complete-CRT covariance structure gives

```text
V_y(t) = (sum_{j=1}^d t_j^2) B_y^2 + O_{alpha,t}(1),
```

because all off-diagonal covariance contributions are bounded. If
`sum_j t_j^2 > 0`, then

```text
V_y(t)^(1/2)/B_y -> (sum_{j=1}^d t_j^2)^(1/2).
```

The projection normalized by `V_y(t)^(1/2)` is Gaussian by the same bounded
Lindeberg or cumulant argument used in v0.8. The equivalent `B_y`
normalization gives the desired limiting variance `sum_j t_j^2`.

This gives the complete-CRT Gaussian limit for every fixed Cramer-Wold
projection, with limiting variance `sum_j t_j^2`.

## FDEK-5: Finite-Window Transfer at the Slow Cutoff

Use the same slow cutoff as v0.8:

```text
y(N)=floor(N^(1/log log N)).
```

For any fixed moment order `m`, the expansion of a fixed Cramer-Wold projection
uses only finitely many angle-prime residue conditions per term. CRT still
turns each compatible finite condition set into one residue class modulo the
product of the distinct primes involved.

After expanding centered factors into constants and indicator products, each
event term either imposes compatible residue conditions and is counted by the
CRT residue-class estimate, or imposes two different residue classes modulo the same prime
and vanishes in both the finite-window and complete-CRT models.
Otherwise, CRT reduces the compatible conditions to one residue class modulo
the product of the distinct primes involved. Therefore the v0.6
moment-transfer budget has the same form:

```text
O_m(pi(y)^m/N).
```

At the slow cutoff, `y(N)^m/N -> 0` for every fixed `m`, so the finite-window
moments of each projection match the complete-CRT moments.

## FDEK-6: Diagonal Tail and Slutsky

The v0.7 all-angle L1 tail removal applies separately to each fixed angle.
For a fixed finite set of angles, the union bound gives

```text
max_{1 <= j <= d} |D_n(n, alpha_j)-D_y(n, alpha_j)| / B_{2N} -> 0
```

in probability. Therefore every fixed Cramer-Wold projection has negligible
diagonal tail after normalization.

Combining FDEK-4, FDEK-5, and FDEK-6 gives the Gate C verified route to the
finite fixed-angle joint CLT.

## Boundary

This v0.9 Gate C verified packet does not claim:

- uniform-in-alpha convergence;
- a shrinking-angle theorem;
- a log-correlated Gaussian field;
- a Mertens uncovered-measure law;
- a random/non-random theorem;
- a public release.

## Gate C Verified Summary

Gate C verified the finite collision bookkeeping, bounded off-diagonal
covariance, Cramer-Wold projection argument, v0.6 finite-window moment
transfer, and v0.7 finite union-bound tail transfer for fixed finite sets of
pairwise distinct angles.
