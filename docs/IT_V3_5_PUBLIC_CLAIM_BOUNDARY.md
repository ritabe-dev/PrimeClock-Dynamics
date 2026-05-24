# PrimeClock Dynamics v3.5.0 Public Claim Boundary

Status: public artifact claim boundary for slow-cutoff integer-time transfer.
This is not a posted preprint and is not peer reviewed.

## Included Claim Surface

The v3.5.0 public artifact records the slow-cutoff bridge from dyadic integer
windows to complete CRT period averages.

Notation:

```text
D_y(n, alpha) = sum_{p<=y} 1_{n mod p = r_p(alpha)},
U_y(n) = Leb{alpha in T : D_y(n, alpha)=0},
P_y = prod_{p<=y}(1-1/p),
M_y = prod_{p<=y}p,
F_y(n) = U_y(n)/P_y.
```

The retained claim IDs are:

- `PCD-IT-TV`: total-variation transfer from dyadic integer windows to uniform
  residues modulo `Q`.
- `PCD-IT-DIST`: bounded-test distributional transfer for `F_y` under
  `M_y/N -> 0`.
- `PCD-IT-MOM-m`: fixed `m` moment transfer under `M_y P_y^{-m}/N -> 0`,
  with Mertens-scale sufficient condition `M_y (log y)^m/N -> 0`.

## Diagnostic Surface

Conductor projection rows are diagnostic only. They do not claim a
high-conductor tail theorem, do not establish high-conductor tail decay, and do
not close the diagonal problem.

## Non-Claims

This public artifact does not claim:

- full diagonal Mertens transfer;
- a theorem for `U_n(n)`;
- distributional diagonal transfer;
- a conductor-tail theorem;
- a theorem beyond the slow-cutoff periodic regime;
- a posted preprint;
- peer review.
