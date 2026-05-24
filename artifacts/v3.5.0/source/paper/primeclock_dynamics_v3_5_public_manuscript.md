# PrimeClock Dynamics v3.5.0: Slow-Cutoff Integer-Time Transfer

Status: public artifact manuscript. This is not a posted preprint and is not
peer reviewed.

## IT-P1: Scope

The v3.5.0 object is a slow-cutoff integer-time transfer theorem for the
Mertens-normalized uncovered mass

```text
D_y(n, alpha) = sum_{p<=y} 1_{n mod p = r_p(alpha)},
U_y(n) = Leb{alpha in T : D_y(n, alpha)=0},
F_y(n) = U_y(n) / P_y,
P_y = prod_{p<=y} (1 - 1/p),
M_y = prod_{p<=y} p.
```

For fixed cutoff `y`, `F_y(n)` is `M_y`-periodic. The v3.5 transfer compares
dyadic integer averages over `N < n <= 2N` with complete CRT period averages
modulo `M_y`. This is a finite-conductor bridge toward the later diagonal
program, not the diagonal theorem itself.

## IT-P2: Dyadic Residue Distribution

Let `Dyad_{N,Q}` be the law of `n mod Q` when `n` is uniformly sampled from
`N < n <= 2N`. Let `Unif_Q` be the uniform law on `Z/QZ`.

Write `N=aQ+b` with `0<=b<Q`. In the interval `N < n <= 2N`, each residue
class modulo `Q` occurs either `a` or `a+1` times, up to a cyclic shift. Hence

```text
||Dyad_{N,Q} - Unif_Q||_TV
  = b(Q-b)/(NQ)
  <= Q/(4N)
```

when `Q<=N`. In all cases the weaker total variation estimate
`||Dyad_{N,Q} - Unif_Q||_TV <= min(1, C Q/N)` holds with an absolute constant.

## IT-P3: Theorem PCD-IT-TV

For every `Q >= 1` and every bounded function `G: Z/QZ -> C`,

```text
|E_{N<n<=2N} G(n mod Q) - E_{a mod Q} G(a)|
  <= 2 ||G||_infty ||Dyad_{N,Q} - Unif_Q||_TV
  <= C Q ||G||_infty / N.
```

The support implementation records the conservative bound
`2Q||G||_infty/N`.

## IT-P4: Corollary PCD-IT-DIST

Let `phi` be a bounded test function on the range of `F_y`. Since `F_y` is
`M_y`-periodic,

```text
|E_{N<n<=2N} phi(F_y(n)) - E_{a mod M_y} phi(F_y(a))|
  <= C M_y ||phi||_infty / N.
```

Thus bounded-test distributional transfer holds in every slow-cutoff regime
with `M_y/N -> 0`.

## IT-P5: Corollary PCD-IT-MOM-m

For each fixed integer `m >= 1`,

```text
0 <= F_y(n)^m <= P_y^{-m}.
```

Applying `PCD-IT-TV` with `G(a)=F_y(a)^m` gives

```text
|E_{N<n<=2N} F_y(n)^m - E_{a mod M_y} F_y(a)^m|
  <= C M_y P_y^{-m} / N.
```

Using `P_y^{-1}=O(log y)`, a sufficient slow-cutoff condition is

```text
M_y (log y)^m / N -> 0.
```

## IT-P6: Conductor Diagnostic

The conductor projection computation groups discrete Fourier power of `F_y` by
the conductor `M_y/gcd(k,M_y)`. It is retained only as a diagnostic for the
future diagonal program. It is not a conductor-tail theorem, does not establish
high-conductor tail decay, and does not imply diagonal transfer.

## IT-P7: Support Evidence

The public support runner records:

- exact total-variation residue audits;
- bounded test-function transfer checks;
- moment transfer sweeps for `m=1,2,3,4`;
- symbolic cutoff budget rows for `M_y (log y)^m/N`;
- conductor projection diagnostics marked diagnostic only.

Support output is deterministic and uses stable float formatting.

## IT-P8: Non-Claims

This public artifact does not claim:

- full diagonal Mertens transfer;
- a theorem for `U_n(n)`;
- distributional diagonal transfer;
- a conductor-tail theorem;
- a theorem beyond the slow-cutoff periodic regime;
- a posted preprint;
- peer review.
