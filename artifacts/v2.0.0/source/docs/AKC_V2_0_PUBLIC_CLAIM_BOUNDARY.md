# PrimeClock Dynamics v2.0.0 Public Claim Boundary

Status: public artifact claim-boundary note. This is not a posted preprint and
not peer reviewed. If this version is archived separately on Zenodo, cite the
issued DOI for that deposited version.

## Positive Claim Surface

The v2.0.0 public artifact surface is restricted to complete-CRT finite-beta AKC:

- `PCD-AKC-MART`: complete-CRT AKC martingale random measures;
- `PCD-AKC-QPOINT`: q-point local factor / moment formula;
- `PCD-AKC-L2`: finite-beta L2 total-mass bound;
- `PCD-AKC-LIMIT`: weak convergence of complete-CRT random finite measures;
- `PCD-AKC-TANGENT`: Gaussian tangent recovery.

The central object is the normalized finite-beta complete-CRT random measure

```text
mu_{x,beta}(d alpha)
= product_{p <= x}
  exp(beta 1_{R_p=r_p(alpha)}) / (1+(e^beta-1)/p) d alpha.
```

## Dependency Structure

```text
v1.1 Shrinking-Angle Gaussian Field
  -> collision kernel / Gaussian tangent
v1.2 Complete-CRT Holomorphic Generating Functional
  -> q-point factors / cumulants / HCGF engine
v2.0 Angular Kubilius Chaos
  -> finite-beta complete-CRT random measure
  -> martingale + L2 total mass + weak convergence
```

## Non-Claims

This public artifact does not claim integer-time finite-beta transfer,
diagonal Mertens uncovered-measure theorem, beta-to-negative-infinity uncovered
theorem, high-point or extremal theorem, Fisher-zero theorem, Lee-Yang theorem,
prime-time theorem, standard Gaussian Multiplicative Chaos, a result about
prime gaps, a result about the Riemann hypothesis, posted preprint, or peer
review.

v3.0 Mertens boundary, v4.0 integer-time diagonal Mertens, and v5.0
high-point/extremal directions are future targets only.
