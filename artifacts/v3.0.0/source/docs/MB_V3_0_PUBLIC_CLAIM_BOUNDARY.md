# PrimeClock Dynamics v3.0.0 Public Claim Boundary

Status: public artifact claim-boundary note. Gate C and Gate P reviews passed. This artifact is not a posted preprint and is not peer reviewed.

Gate C review result: PASS.

## Title

PrimeClock Dynamics v3.0:
The Mertens Boundary of Angular Kubilius Chaos

Subtitle:
Mertens-Normalized Uncovered Measures in the Complete-CRT Model

## Included Claim Surface

- `PCD-MB-MART`: Mertens-normalized uncovered random measures are martingales.
- `PCD-MB-QPOINT`: q-point hard local factor formula.
- `PCD-MB-L2`: finite L2 total-mass bound for the normalized uncovered measure.
- `PCD-MB-LIMIT`: weak convergence of complete-CRT Mertens-boundary random finite measures.
- `PCD-MB-FB-ENDPOINT`: fixed-cutoff compatibility with `beta -> -infinity` finite-beta AKC.

## Boundary Convention

Pointwise formulas use the half-open selected-residue cells

```text
C_{p,r} = [(r - 1/2)/p, (r + 1/2)/p) mod 1.
```

Integrated quantities such as `U_x(R)` and
`int_T u^{D_x(R,alpha)} d alpha` are insensitive to endpoint assignments,
because finite-cutoff boundary sets are finite and have Lebesgue measure zero.

## Non-Claims

This public artifact does not claim:

- integer-time transfer;
- diagonal Mertens uncovered-measure theorem;
- `U_n(n) log n -> e^{-gamma}`;
- `beta -> +infinity` high-point theorem;
- Fisher-zero theorem;
- Lee-Yang theorem;
- standard Gaussian Multiplicative Chaos;
- prime-time theorem;
- a new proof of the classical Mertens product theorem;
- peer review.

## Routing

v3.5 is reserved
for slow integer-time transfer, v4.0 for diagonal Mertens transfer, and v5.0
for high-point or extremal-field questions.
