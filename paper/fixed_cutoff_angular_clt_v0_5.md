# PrimeClock Dynamics v0.5 Fixed-Cutoff Angular CLT

Status: internal Gate R proof packet. This is not a public artifact, not a preprint,
not a DOI artifact, not a Zenodo record, and not peer reviewed.

This note is the next proof-stage target after the public v0.2.0 fixed-cutoff
foundation. It proves only a complete-CRT fixed-cutoff central limit theorem for
one fixed angle. It does not claim a diagonal theorem, a Mertens asymptotic law,
a Gaussian field theorem, or a random/non-random theorem.

The purpose is narrow: close the first Angular Erdos-Kac proof step on the
finite CRT probability space before returning to truncated finite-window or
diagonal arguments.

## Complete-CRT Probability Space

Fix an angle `alpha in R/Z` and a cutoff `x`. Let

```text
P_x = {p prime : p <= x},
M_x = prod_{p <= x} p,
r_p(alpha) = floor(p alpha + 1/2) mod p,
D_x(n, alpha) = sum_{p <= x} 1_{n mod p = r_p(alpha)}.
```

The random variable is `D_x(n, alpha)` with `n` uniform on the complete CRT
period `Z/M_xZ`.

Define

```text
A_x = sum_{p <= x} 1/p,
B_x^2 = sum_{p <= x} (1/p)(1 - 1/p).
```

All limits below use any sequence of cutoffs `x -> infinity`. Equivalently, one
may enumerate the prime sets `P_x` as a triangular array indexed by `x`.

## FCLT-1: Fixed-Angle Residue Selector

For each prime `p`, the half-open arc convention selects exactly one residue
class for a fixed angle `alpha`:

```text
r_p(alpha) = floor(p alpha + 1/2) mod p.
```

The selected class may depend on `alpha` and `p`, but it is always a single
class in `Z/pZ`. Therefore a uniform residue modulo `p` hits that selected class
with probability exactly `1/p`.

## FCLT-2: CRT Bernoulli Decomposition

For fixed `x`, the CRT map

```text
Z/M_xZ -> prod_{p <= x} Z/pZ
```

is a bijection. Under the uniform measure on `Z/M_xZ`, the coordinates
`n mod p` are independent and uniform on `Z/pZ`. Therefore

```text
X_{p,alpha}(n) = 1_{n mod p = r_p(alpha)}
```

are independent Bernoulli random variables with parameter `1/p`, and

```text
D_x(n, alpha) = sum_{p <= x} X_{p,alpha}(n).
```

This decomposition is independent of the specific fixed angle except through
the selected residue class.

## FCLT-3: Mean And Variance

From the decomposition,

```text
E[D_x(n, alpha)] = A_x,
Var(D_x(n, alpha)) = B_x^2.
```

The variance diverges because

```text
B_x^2 = sum_{p <= x} 1/p - sum_{p <= x} 1/p^2
```

and the classical divergence of `sum_p 1/p` dominates the convergent series
`sum_p 1/p^2`.

In particular, `B_x -> infinity`.

## FCLT-4: Lindeberg Condition

Let

```text
Z_{p,x} = X_{p,alpha} - 1/p.
```

Then `E[Z_{p,x}] = 0`, `sum_{p <= x} Var(Z_{p,x}) = B_x^2`, and

```text
|Z_{p,x}| <= 1
```

for every `p <= x`. For any fixed `epsilon > 0`, since `B_x -> infinity`, there
exists `x_0(epsilon)` such that `epsilon B_x > 1` for all
`x >= x_0(epsilon)`. For those `x`,

```text
|Z_{p,x}| > epsilon B_x
```

is impossible for every `p <= x`. Hence the Lindeberg sum

```text
(1 / B_x^2) sum_{p <= x}
E[Z_{p,x}^2 1_{|Z_{p,x}| > epsilon B_x}]
```

is exactly zero for all sufficiently large `x`.

This verifies the Lindeberg condition for the independent triangular array
`{Z_{p,x} / B_x : p <= x}`.

## Theorem FCLT-5: Fixed-Cutoff Angular CLT

For every fixed angle `alpha in R/Z`, let `n_x` be uniformly distributed on the
complete CRT period `Z/M_xZ`. Then

```text
(D_x(n_x, alpha) - A_x) / B_x  =>  N(0,1)
```

as `x -> infinity`. This is a fixed-cutoff theorem only, not a diagonal theorem.

Proof. By FCLT-1 and FCLT-2,

```text
D_x(n, alpha) - A_x = sum_{p <= x} Z_{p,x}.
```

The summands are independent and centered, with total variance `B_x^2`. By
FCLT-3, `B_x -> infinity`. By FCLT-4, the normalized array satisfies the
Lindeberg condition. The Lindeberg-Feller central limit theorem therefore gives

```text
(1 / B_x) sum_{p <= x} Z_{p,x}  =>  N(0,1),
```

which is the stated convergence.

## Angle Dependence

The proof is uniform in the following limited sense: for each fixed `alpha`,
only the selected residues `r_p(alpha)` change. The Bernoulli parameters remain
`1/p`, the variance sum remains `B_x^2`, and the Lindeberg bound remains
`|Z_{p,x}| <= 1`. This packet does not prove a uniform-in-alpha theorem, a
shrinking-angle theorem, or a finite-dimensional field theorem.

## Gate R Support Evidence

The deterministic support runner
`experiments/_workflow/build_fixed_cutoff_clt_support.py` records finite-cutoff
checks for:

- the variance sum `B_x^2`;
- the maximum centered summand ratio `1 / B_x`;
- the point where the Lindeberg sum is zero for `epsilon = 1`;
- a Lyapunov-style third-moment ratio as a secondary numerical sanity check.

These rows are support evidence for the proof packet, not statistical evidence
for the diagonal model.

## Boundary

This fixed-cutoff theorem is a complete-CRT probability-space result. It is not
a theorem for the diagonal model

```text
D(n, alpha) = D_n(n, alpha).
```

It also does not prove a Mertens uncovered law for

```text
U(n) = U_n(n).
```

Those remain later proof stages. In the current program, this note is the
candidate proof foundation for a later diagonal Angular Erdos-Kac theorem.

## Next Proof Step

The next proof stage is a truncated finite-window theorem for
`D_{N^theta}(n, alpha)` with `n` uniform on an integer interval. That stage will
need residue-class counting over incomplete intervals and is not included in
this fixed-cutoff packet.
