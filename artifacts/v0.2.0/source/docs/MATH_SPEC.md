# Mathematical Specification

PrimeClock Dynamics studies the integer-time version of the original visual
Prime Clock app model. It is not the finite PRC certificate model.

## Circle

Let

```text
T = R/Z
```

with coordinates normalized to `[0, 1)`. The twelve-o'clock direction is
represented by `alpha = 0`.

## Diagonal App-Time Primes

At integer time `n >= 2`, the active prime set is

```text
P(n) = { p : p is prime and p <= n }.
```

Each prime `p` first appears at integer time `p`.

## Residue-Time And Diagonal-Time Arcs

For fixed-cutoff CRT calculations, the residue-time center is defined for any
integer `n >= 0` and any prime `p`:

```text
c_p^res(n) = (n mod p) / p.
```

The residue-time arc is

```text
I_p^res(n) = [c_p^res(n) - 1/(2p), c_p^res(n) + 1/(2p)] in T.
```

For the diagonal app-level model, the same center formula is used only at
integer app times `n >= 2`, and only primes `p <= n` are active:

```text
I_p^diag(n) = I_p^res(n), active only for p <= n.
```

For pointwise multiplicity, this repository uses a half-open boundary convention:
the left endpoint is included and the right endpoint is excluded after choosing
the shortest circular representative. This removes endpoint double-counting at
`alpha = 0` and makes Theorem 0 exact.

For uncovered measure, endpoints have measure zero, so exact rational union
calculations may use closed intervals without changing `U(n)`.

## Multiplicity Field

The Prime Clock Multiplicity Field is

```text
D(n, alpha) = sum_{p <= n} 1_{alpha in I_p^diag(n)}.
```

Under the half-open convention,

```text
D(n, 0) = omega(n),
```

where `omega(n)` is the number of distinct prime divisors of `n`.

For proof work it is useful to separate the time parameter from the prime
cutoff. For `x >= 2`, define

```text
D_x(n, alpha) = sum_{p <= x} 1_{alpha in I_p^res(n)}.
```

This fixed-cutoff object is a residue-time CRT model and may include primes
`p > n`. The repository-level app model is the diagonal case
`D(n, alpha) = D_n(n, alpha)`, where the cutoff and app time are tied together.
The v0.2.0 artifact studies fixed `x`; later work may compare it with the
diagonal model on dyadic windows such as `n in [N, 2N]`.

## Uncovered Measure

The uncovered set is

```text
{ alpha in T : D(n, alpha) = 0 }.
```

Its normalized one-dimensional measure is

```text
U(n) = measure({ alpha in T : D(n, alpha) = 0 }).
```

The cutoff uncovered measure is

```text
U_x(n) = measure({ alpha in T : D_x(n, alpha) = 0 }).
```

Again, `U_x(n)` is the residue-time fixed-cutoff model, while the repository-level
app model is the diagonal case `U(n) = U_n(n)`.

The main experimental comparison baseline is the Mertens product

```text
prod_{p <= n} (1 - 1/p).
```

The Poissonized random-arc baseline is

```text
exp(-sum_{p <= n} 1/p).
```

## Continuous Time

The visual app has a continuous-time process in which prime `p` rotates with
period `p`. This repository starts with the integer-time restriction because it gives
the exact residue model `(n mod p)/p` and the identity `D(n,0)=omega(n)`.

## Angle Metadata

Some experiment runners use configured angles such as `zero`, `one_tenth`, and
`sqrt2_mod1`. The `sqrt2_mod1` value is a float64 approximation used for
diagnostics. It is not treated as an exact symbolic irrational angle claim.
